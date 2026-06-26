# Script 59: Battery Backup

capacity = float(input("Battery Capacity (Ah): "))
voltage = float(input("Battery Voltage (V): "))
load = float(input("Load (W): "))

energy = capacity * voltage
backup_time = energy / load

print(f"Backup Time ≈ {backup_time:.2f} hours")
