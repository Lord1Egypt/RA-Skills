#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probe all available expressions related to current in the solved model.
"""
import sys, json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

try:
    import mph
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"mph not found: {e}"}))
    sys.exit(1)

mph_file = SKILL_DIR / "output" / "optoelectronic" / "opto_result.mph"
client = mph.start()
model = client.load(str(mph_file))

log = {"status": "probing_expressions", "results": []}

# Try various current expressions
expressions = [
    "semi.I_1",
    "semi.I_2", 
    "semi.I_ec1",
    "semi.I_ec2",
    "semi.I1",
    "semi.I2",
    "semi.I_1_0",
    "semi.I_1_1",
    "comp1.semi.I_1",
    "comp1.semi.I_2",
    "semi.normJ",
    "semi.Jn",
    "semi.Jp",
    "semi.Jtot",
    "ec1.I0",
    "ec2.I0",
    "Jx",
    "Jy",
    "semi.ee.I_1",
]

for expr in expressions:
    try:
        data = model.evaluate(expr)
        shape = str(data.shape) if hasattr(data, 'shape') else "N/A"
        sample = str(data)[:200]
        log["results"].append({"expr": expr, "shape": shape, "sample": sample, "status": "ok"})
    except Exception as e:
        log["results"].append({"expr": expr, "status": "error", "error": str(e)[:200]})

# Also try to get parameter values from solution
try:
    params = model.parameters()
    log["parameters"] = {k: str(v) for k, v in params.items()}
except Exception as e:
    log["parameters_error"] = str(e)

# Try to get solution info
jm = model.java
try:
    sol = jm.sol("sol1")
    # Get number of parameter values
    log["sol_info"] = str(sol)
except Exception as e:
    log["sol_info_error"] = str(e)

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


