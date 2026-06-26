# Script 3: Transformer Efficiency

def efficiency(output_power, input_power):
    return (output_power / input_power) * 100

if __name__ == "__main__":
    Pin = float(input("Enter Input Power (kW): "))
    Pout = float(input("Enter Output Power (kW): "))

    eff = efficiency(Pout, Pin)
    print(f"Efficiency = {eff:.2f}%")
