# Script 13: Unit Converter

def convert(value, from_unit, to_unit):
    units = {
    "kW": 1000,
    "MW": 1000000,
    "W": 1
    }
    return value * units[from_unit] / units[to_unit]

value = float(input("Enter value: "))
from_unit = input("From unit (W/kW/MW): ")
to_unit = input("To unit (W/kW/MW): ")

result = convert(value, from_unit, to_unit)

print(f"{result:.2f} {to_unit}")
