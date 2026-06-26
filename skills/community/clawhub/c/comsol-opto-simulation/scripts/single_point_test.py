#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test single-point solve (0V, no parametric sweep) and get solver message.
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
jm = model.java

log = {"status": "single_point_test", "steps": []}

# Step 1: Remove parametric sweep, keep only stationary
try:
    study = jm.study("std1")
    study.feature().remove("param1")
    log["steps"].append("removed_parametric")
except Exception as e:
    log["steps"].append({"remove_parametric_error": str(e)})

# Step 2: Remove old solver
try:
    jm.sol().remove("sol1")
    log["steps"].append("removed_old_solver")
except Exception as e:
    log["steps"].append({"remove_solver_error": str(e)})

# Step 3: Build and solve via mph (auto-generates solver)
log["steps"].append("building")
try:
    model.build()
    log["steps"].append("build_ok")
except Exception as e:
    log["steps"].append({"build_error": str(e)})

log["steps"].append("solving")
try:
    model.solve()
    log["steps"].append("solve_ok")
except Exception as e:
    log["steps"].append({"solve_error": str(e)})

# Step 4: Check datasets
try:
    ds_list = jm.result().dataset()
    datasets = []
    for ds in ds_list:
        datasets.append(str(ds.tag()))
    log["steps"].append({"datasets": datasets})
except Exception as e:
    log["steps"].append({"dataset_error": str(e)})

# Step 5: Try to get solver message
sol = jm.sol("sol1")
s1 = sol.feature("s1")
log["steps"].append({"solver_message": str(s1.getString("message"))})

# Step 6: Try to evaluate with inner="first"
for expr in ["semi.I_1", "semi.normJ", "semi.V", "V_bias"]:
    try:
        data = model.evaluate(expr, inner="first")
        log["steps"].append({"expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:200]})
    except Exception as e:
        log["steps"].append({"expr": expr, "error": str(e)})

# Save
model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


