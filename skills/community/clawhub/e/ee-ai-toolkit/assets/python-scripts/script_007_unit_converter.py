# Script 7: Unit Converter

def convert_kw_to_mw(kw):
    return kw / 1000

kw = float(input("Enter power in kW: "))
mw = convert_kw_to_mw(kw)

print(f"{mw} MW")
