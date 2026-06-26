#!/usr/bin/env python3
"""
Simple Discounted Cash Flow (DCF) model.

Usage:
    python dcf_model.py <input.json> <output.xlsx>

Input JSON format (example):
{
    "periods": 5,
    "fcf": [100, 120, 140, 160, 180],
    "terminal_growth": 0.02,
    "wacc": 0.1
}
"""
import sys, json
from pathlib import Path

try:
    input_path, output_path = sys.argv[1], sys.argv[2]
except IndexError:
    print("Usage: python dcf_model.py <input.json> <output.xlsx>")
    sys.exit(1)

with open(input_path) as f:
    data = json.load(f)

periods = data["periods"]
fcf = data["fcf"]
terminal_growth = data.get("terminal_growth", 0.02)
wacc = data["wacc"]

# Discount cash flows
pv_fcf = [cf / ((1 + wacc) ** (i + 1)) for i, cf in enumerate(fcf)]

# Terminal value using perpetuity growth
last_fcf = fcf[-1]
terminal_value = last_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
pv_terminal = terminal_value / ((1 + wacc) ** periods)

enterprise_value = sum(pv_fcf) + pv_terminal

# Write simple Excel output
import xlsxwriter
workbook = xlsxwriter.Workbook(output_path)
ws = workbook.add_worksheet("DCF Model")
ws.write(0, 0, "Period")
ws.write(0, 1, "FCF")
ws.write(0, 2, "PV of FCF")
for i in range(periods):
    ws.write(i + 1, 0, i + 1)
    ws.write(i + 1, 1, fcf[i])
    ws.write(i + 1, 2, pv_fcf[i])
ws.write(periods + 2, 0, "Terminal Value")
ws.write(periods + 2, 1, terminal_value)
ws.write(periods + 2, 2, pv_terminal)
ws.write(periods + 4, 0, "Enterprise Value")
ws.write(periods + 4, 1, enterprise_value)
workbook.close()
print(f"Enterprise Value: {enterprise_value:.2f}")
