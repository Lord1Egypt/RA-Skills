# Script 58: Ground Resistance

rho = float(input("Soil Resistivity (Ohm-m): "))
L = float(input("Rod Length (m): "))

R = rho / (2 * 3.14 * L)

print(f"Ground Resistance ≈ {R:.2f} Ohm")
