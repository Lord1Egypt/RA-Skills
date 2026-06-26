# Script 15: Report Generator

def generate_report(voltage, current):
    power = voltage * current
    report = f"""
    --- Electrical Report ---
    Voltage: {voltage} V
    Current: {current} A
    Power: {power} W
    -------------------------
    """
    return report

V = float(input("Voltage: "))
I = float(input("Current: "))

print(generate_report(V, I))
