# Script 95: Renewable Mix

solar = float(input("Solar Output (MW): "))
wind = float(input("Wind Output (MW): "))
cost_solar = 5
cost_wind = 7

total_cost = solar * cost_solar + wind * cost_wind

print(f"Total Cost = {total_cost}")
