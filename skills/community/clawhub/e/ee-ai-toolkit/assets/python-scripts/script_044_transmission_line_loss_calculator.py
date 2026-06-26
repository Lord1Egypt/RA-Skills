# Script 44: Transmission Loss

I = float(input("Current (A): "))
R = float(input("Resistance (Ohm): "))

loss = I**2 * R

print(f"Power Loss = {loss:.2f} W")
