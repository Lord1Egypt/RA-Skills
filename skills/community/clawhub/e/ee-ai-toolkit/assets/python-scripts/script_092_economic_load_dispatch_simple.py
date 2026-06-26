# Script 92: Economic Load Dispatch

cost_A = 10 # $/MW
cost_B = 15

demand = float(input("Total Demand (MW): "))

# Use cheaper generator first
gen_A = min(demand, 100)
gen_B = demand - gen_A

cost = gen_A * cost_A + gen_B * cost_B

print(f"Generator A: {gen_A} MW")
print(f"Generator B: {gen_B} MW")
print(f"Total Cost = ${cost:.2f}")
