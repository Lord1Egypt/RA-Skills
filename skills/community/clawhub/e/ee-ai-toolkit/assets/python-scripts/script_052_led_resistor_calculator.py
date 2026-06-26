# Script 52: LED Resistor

Vs = float(input("Supply Voltage (V): "))
Vled = float(input("LED Voltage Drop (V): "))
I = float(input("LED Current (A): "))

R = (Vs - Vled) / I

print(f"Required Resistor = {R:.2f} Ohm")
