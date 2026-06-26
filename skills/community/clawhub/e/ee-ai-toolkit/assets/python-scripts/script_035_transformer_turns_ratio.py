# Script 35: Transformer Ratio

Vp = float(input("Primary Voltage (V): "))
ratio = float(input("Turns Ratio (Np/Ns): "))

Vs = Vp / ratio

print(f"Secondary Voltage = {Vs:.2f} V")
