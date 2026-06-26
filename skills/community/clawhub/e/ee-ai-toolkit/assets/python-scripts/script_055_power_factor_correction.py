# Script 55: Power Factor Correction

import math

P = float(input("Real Power (kW): "))
pf1 = float(input("Initial PF: "))
pf2 = float(input("Desired PF: "))

Q1 = P * math.tan(math.acos(pf1))
Q2 = P * math.tan(math.acos(pf2))

Qc = Q1 - Q2

print(f"Required Capacitor kVAR = {Qc:.2f}")
