# Script 99: Maintenance Scheduler

equipment = ["Transformer", "Breaker", "Cable"]
priority = [3, 1, 2]

schedule = sorted(zip(equipment, priority), key=lambda x: x[1])

print("Maintenance Schedule:")
for e in schedule:
    print(e[0])
