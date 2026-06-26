# Script 32: Power Triangle

import math

P = float(input("Real Power (kW): "))
PF = float(input("Power Factor: "))

S = P / PF
Q = math.sqrt(S**2 - P**2)

print(f"Apparent Power = {S:.2f} kVA")
print(f"Reactive Power = {Q:.2f} kVAR")
