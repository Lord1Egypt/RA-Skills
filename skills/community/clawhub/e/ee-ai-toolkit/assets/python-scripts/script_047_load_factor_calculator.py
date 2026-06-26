# Script 47: Load Factor

average = float(input("Average Load (MW): "))
peak = float(input("Peak Load (MW): "))

lf = average / peak

print(f"Load Factor = {lf:.2f}")
