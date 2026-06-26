# Script 96: Transformer Load Balance

loads = list(map(float, input("Enter loads: ").split()))

avg = sum(loads) / len(loads)

balanced = [avg for _ in loads]

print("Balanced Loads:", balanced)
