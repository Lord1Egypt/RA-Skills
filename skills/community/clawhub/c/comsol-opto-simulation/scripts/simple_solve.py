#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplest approach: use mph model.solve() which handles solver automatically.
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

log = {"status": "simple_solve", "steps": []}

# Step 1: Build geometry and mesh
log["steps"].append("building")
try:
    model.build()
    log["steps"].append("build_ok")
except Exception as e:
    log["steps"].append({"build_error": str(e)})

# Step 2: Solve
log["steps"].append("solving")
try:
    model.solve()
    log["steps"].append("solve_ok")
except Exception as e:
    log["steps"].append({"solve_error": str(e)})

# Step 3: Check datasets
jm = model.java
try:
    ds_list = jm.result().dataset()
    datasets = []
    for ds in ds_list:
        datasets.append(str(ds.tag()))
    log["steps"].append({"datasets": datasets})
except Exception as e:
    log["steps"].append({"dataset_error": str(e)})

# Step 4: Extract current
try:
    data = model.evaluate("semi.I_1")
    log["steps"].append({"current_I1": str(data)[:500]})
except Exception as e:
    log["steps"].append({"current_error": str(e)})

# Save
model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


