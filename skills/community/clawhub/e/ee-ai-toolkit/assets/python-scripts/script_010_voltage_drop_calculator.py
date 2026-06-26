# Script 10: Voltage Drop

def voltage_drop(current, resistance):
    return current * resistance

I = float(input("Enter Current (A): "))
R = float(input("Enter Resistance (Ohm): "))

Vdrop = voltage_drop(I, R)

print(f"Voltage Drop = {Vdrop:.2f} V")
