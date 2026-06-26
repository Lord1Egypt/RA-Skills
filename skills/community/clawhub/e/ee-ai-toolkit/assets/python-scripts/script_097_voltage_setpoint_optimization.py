# Script 97: Voltage Setpoint

voltages = list(map(float, input("Enter voltages: ").split()))

target = sum(voltages) / len(voltages)

print(f"Recommended Voltage Setpoint = {target:.2f} V")
