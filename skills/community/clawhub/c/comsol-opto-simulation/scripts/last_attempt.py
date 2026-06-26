#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last resort: check if the issue is that study step doesn't include semi physics.
Try to explicitly add physics to study step.
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

log = {"status": "last_attempt", "steps": []}

# Step 1: Check study feature properties for physics inclusion
study = jm.study("std1")
stat1 = study.feature("stat1")

# Try various property names for physics control
for prop_name in ["physics", "physicscontrol", "usephysics", "activate", "disphysics"]:
    try:
        val = str(stat1.getString(prop_name))
        log["steps"].append({"prop": prop_name, "value": val})
    except Exception as e:
        log["steps"].append({"prop": prop_name, "error": str(e)[:100]})

# Try to set physics to include semi
log["steps"].append({"step": "try_set_physics"})
try:
    # In some COMSOL versions, you can set physics as a string list
    stat1.set("physics", "semi")
    log["steps"].append({"action": "set_physics_to_semi", "status": "ok"})
except Exception as e:
    log["steps"].append({"action": "set_physics_to_semi", "error": str(e)[:200]})

# Step 2: Remove solver and re-solve
log["steps"].append({"step": "resolving"})
try:
    jm.sol().remove("sol1")
    model.build()
    model.solve()
    log["steps"].append({"step": "resolve", "status": "ok"})
    
    sol = jm.sol("sol1")
    s1 = sol.feature("s1")
    log["steps"].append({"solver_message": str(s1.getString("message"))})
    
    # Try evaluate
    for expr in ["semi.I_1", "semi.normJ", "V_bias"]:
        try:
            data = model.evaluate(expr, inner="first")
            log["steps"].append({"expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:200]})
        except Exception as e:
            log["steps"].append({"expr": expr, "error": str(e)})
except Exception as e:
    log["steps"].append({"step": "resolve", "error": str(e)})

model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


