# Script 45: Short Circuit Current

V = float(input("System Voltage (V): "))
Z = float(input("Impedance (Ohm): "))

Isc = V / Z

print(f"Short Circuit Current = {Isc:.2f} A")
