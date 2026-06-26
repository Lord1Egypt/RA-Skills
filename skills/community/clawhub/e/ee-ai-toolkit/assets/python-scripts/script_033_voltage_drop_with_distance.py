# Script 33: Voltage Drop with Distance

def voltage_drop(I, R_per_km, length_km):
    return I * R_per_km * length_km

I = float(input("Current (A): "))
R = float(input("Resistance per km (Ohm): "))
L = float(input("Length (km): "))

Vdrop = voltage_drop(I, R, L)

print(f"Voltage Drop = {Vdrop:.2f} V")
