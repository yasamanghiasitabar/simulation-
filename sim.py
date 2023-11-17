import simpy
import random


def exponential(mean):
    return random.expovariate(1 / mean)


def network_queue_simulation(env, arrival_rate, service_rate1, service_rate2, service_rate3):
    queue1 = simpy.Resource(env, capacity=1)
    queue2 = simpy.Resource(env, capacity=1)
    queue3 = simpy.Resource(env, capacity=1)
    total_customers = 0
    total_time_in_system = 0

    while True:
        inter_arrival_time = exponential(arrival_rate)
        yield env.timeout(inter_arrival_time)

        customer = total_customers + 1
        total_customers += 1
        arrival_time = env.now

        with queue1.request() as req1:
            yield req1
            service_time1 = exponential(service_rate1)
            yield env.timeout(service_time1)

            with queue2.request() as req2:
                yield req2
                if random.random() < 0.4:
                    yield env.timeout(exponential(service_rate2))
                else:
                    with queue3.request() as req3:
                        yield req3
                        yield env.timeout(exponential(service_rate3))

            departure_time = env.now
            total_time_in_system += (departure_time - arrival_time)

            
            env.process(collect_data(total_customers, total_time_in_system))


def collect_data(customers, time_in_system):
    yield env.timeout(0)  # Yield an event to save data at the end of this step
    global total_customers, total_time_in_system
    total_customers = customers
    total_time_in_system = time_in_system


env = simpy.Environment()
arrival_rate = 1
service_rate1 = 1
service_rate2 = 4
service_rate3 = 3


process = env.process(network_queue_simulation(env, arrival_rate, service_rate1, service_rate2, service_rate3))
env.run(until=10000)


L1 = total_customers / env.now
LQ1 = L1
W1 = total_time_in_system / total_customers
WQ1 = W1
P1 = service_rate1 / arrival_rate

R = W1
N = L1
w = total_time_in_system / env.now

print(f"L1: {L1}")
print(f"LQ1: {LQ1}")
print(f"W1: {W1}")
print(f"WQ1: {WQ1}")
print(f"P1: {P1}")
print(f"R: {R}")
print(f"N: {N}")
print(f"w: {w}")
