# Script 1: Power Calculator

def calculate_power(voltage, current):
    return voltage * current

if __name__ == "__main__":
    V = float(input("Enter Voltage (V): "))
    I = float(input("Enter Current (A): "))

    P = calculate_power(V, I)
    print(f"Power = {P:.2f} Watts")
