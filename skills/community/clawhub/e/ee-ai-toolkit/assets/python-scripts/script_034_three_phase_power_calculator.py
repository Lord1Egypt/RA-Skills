# Script 34: Three-Phase Power

import math

V = float(input("Line Voltage (V): "))
I = float(input("Current (A): "))
PF = float(input("Power Factor: "))

P = math.sqrt(3) * V * I * PF

print(f"Three-phase Power = {P/1000:.2f} kW")
