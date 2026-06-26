#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check init1 settings and try alternative configurations.
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

log = {"status": "init_probe", "info": []}

# Check init1 properties
init1 = semi.feature("init1")
for prop in ["SpecifyInitialValues", "V", "N", "P", "Efn", "Efp"]:
    try:
        val = str(init1.getString(prop))
        log["info"].append({"prop": prop, "value": val})
    except Exception as e:
        log["info"].append({"prop": prop, "error": str(e)})

# Try setting SpecifyInitialValues to "user"
try:
    init1.set("SpecifyInitialValues", "user")
    log["info"].append({"action": "set_user_init", "status": "ok"})
except Exception as e:
    log["info"].append({"action": "set_user_init", "error": str(e)})

# Try removing and re-adding init
try:
    semi.feature().remove("init1")
    init_new = semi.feature().create("init1", "init")
    init_new.selection().set([1,2,3,4,5,6])
    init_new.set("SpecifyInitialValues", "user")
    init_new.set("V", "0")
    init_new.set("N", "semi.Nd")
    init_new.set("P", "semi.Na")
    log["info"].append({"action": "recreate_init", "status": "ok"})
except Exception as e:
    log["info"].append({"action": "recreate_init", "error": str(e)})

# Save and test solve
model.save(str(mph_file))

# Remove solver and re-solve
log["info"].append({"step": "resolving"})
try:
    jm.sol().remove("sol1")
    model.build()
    model.solve()
    log["info"].append({"step": "resolve", "status": "ok"})
    
    # Check message
    sol = jm.sol("sol1")
    s1 = sol.feature("s1")
    log["info"].append({"solver_message": str(s1.getString("message"))})
    
    # Try evaluate
    for expr in ["semi.I_1", "semi.normJ"]:
        try:
            data = model.evaluate(expr, inner="first")
            log["info"].append({"expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:200]})
        except Exception as e:
            log["info"].append({"expr": expr, "error": str(e)})
except Exception as e:
    log["info"].append({"step": "resolve", "error": str(e)})

model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


