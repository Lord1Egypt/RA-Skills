# Script 57: Relay Pickup

load_current = float(input("Load Current (A): "))
safety_factor = 1.2

pickup = load_current * safety_factor

print(f"Relay Pickup Current = {pickup:.2f} A")
