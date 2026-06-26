# Script 50: Solar Power

area = float(input("Panel Area (m^2): "))
irradiance = float(input("Irradiance (W/m^2): "))
efficiency = float(input("Efficiency (0–1): "))

power = area * irradiance * efficiency

print(f"Solar Power Output = {power:.2f} W")
