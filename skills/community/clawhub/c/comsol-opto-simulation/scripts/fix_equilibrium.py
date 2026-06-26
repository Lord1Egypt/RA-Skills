#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix EquilibriumCondition and re-solve.
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
comp = jm.component("comp1")
semi = comp.physics("semi")

log = {"status": "fix_equilibrium", "steps": []}

# Step 1: Set EquilibriumCondition to "none" for all material models
feat_list = semi.feature()
for feat in feat_list:
    ftype = str(feat.getType())
    if ftype == "SemiconductorMaterialModel":
        tag = str(feat.tag())
        try:
            feat.set("EquilibriumCondition", "none")
            log["steps"].append({"action": "set_none", "tag": tag, "status": "ok"})
        except Exception as e:
            log["steps"].append({"action": "set_none", "tag": tag, "error": str(e)})

# Step 2: Remove old solver and recreate
log["steps"].append("removing_old_solver")
try:
    jm.sol().remove("sol1")
    log["steps"].append("removed_sol1")
except Exception as e:
    log["steps"].append({"remove_sol1_error": str(e)})

# Step 3: Build and solve
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

# Step 4: Check datasets and DOFs
sol = jm.sol("sol1")
s1 = sol.feature("s1")
log["steps"].append({"solver_message": str(s1.getString("message"))})

try:
    ds_list = jm.result().dataset()
    datasets = [str(ds.tag()) for ds in ds_list]
    log["steps"].append({"datasets": datasets})
except Exception as e:
    log["steps"].append({"dataset_error": str(e)})

# Step 5: Try to evaluate current
for expr in ["semi.I_1", "semi.I_2", "semi.normJ"]:
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


