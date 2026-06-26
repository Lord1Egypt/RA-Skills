# Script 39: RL Time Constant

L = float(input("Inductance (H): "))
R = float(input("Resistance (Ohm): "))

tau = L / R

print(f"Time Constant = {tau:.4f} seconds")
