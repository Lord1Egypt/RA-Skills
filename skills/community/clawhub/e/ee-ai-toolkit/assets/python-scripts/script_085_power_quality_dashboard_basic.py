# Script 85: Power Quality Dashboard

voltage = float(input("Voltage (V): "))
frequency = float(input("Frequency (Hz): "))
harmonics = float(input("THD (%): "))

print("\n--- Power Quality ---")
print("Voltage:", voltage)
print("Frequency:", frequency)
print("THD:", harmonics)

if voltage < 210 or voltage > 240:
    print("Voltage Out of Range!")

if frequency < 49 or frequency > 51:
    print("Frequency Out of Range!")
