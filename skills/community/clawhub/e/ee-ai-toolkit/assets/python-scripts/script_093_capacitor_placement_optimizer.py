# Script 93: Capacitor Placement

buses = [1, 2, 3, 4]
voltages = [0.95, 0.92, 0.97, 0.90]

min_voltage = min(voltages)
index = voltages.index(min_voltage)

print(f"Place capacitor at Bus {buses[index]} (Lowest Voltage)")
