# Script 38: Capacitor Energy

C = float(input("Capacitance (Farads): "))
V = float(input("Voltage (V): "))

E = 0.5 * C * V**2

print(f"Energy Stored = {E:.2f} Joules")
