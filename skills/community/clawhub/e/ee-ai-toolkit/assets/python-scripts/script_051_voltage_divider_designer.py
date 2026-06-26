# Script 51: Voltage Divider Designer

Vin = float(input("Input Voltage (V): "))
Vout = float(input("Desired Output Voltage (V): "))
R1 = float(input("Choose R1 value (Ohm): "))

R2 = (Vout * R1) / (Vin - Vout)

print(f"Required R2 = {R2:.2f} Ohm")
