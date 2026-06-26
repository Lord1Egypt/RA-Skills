# Script 53: Motor Starter Sizing

power = float(input("Motor Power (kW): "))

current = power * 1000 / (400 * 0.8 * 1.732)

print(f"Estimated Motor Current = {current:.2f} A")

if current < 20:
    starter = "DOL Starter"
else:
    starter = "Star-Delta Starter"

print("Recommended Starter:", starter)
