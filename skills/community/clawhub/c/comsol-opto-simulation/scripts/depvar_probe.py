#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probe dependent variables and equation settings.
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

log = {"status": "depvar_probe", "info": []}

# Check dependent variables of semi physics
try:
    dv = semi.field()
    log["info"].append({"field": str(dv), "type": str(type(dv))})
except Exception as e:
    log["info"].append({"field_error": str(e)})

# Check variable list
try:
    vars = semi.variables()
    log["info"].append({"variables": [str(v) for v in vars], "count": len(vars)})
except Exception as e:
    log["info"].append({"variables_error": str(e)})

# Try to get equation form
for feat_tag in ["smm1", "mat0", "mat1", "mat2"]:
    try:
        feat = semi.feature(feat_tag)
        for prop in ["EquilibriumCondition", "V0_bias", "Q0_tot"]:
            try:
                val = str(feat.getString(prop))
                log["info"].append({"tag": feat_tag, "prop": prop, "value": val})
            except Exception:
                pass
    except Exception as e:
        log["info"].append({"tag": feat_tag, "error": str(e)})

# Check if there are any equations defined
log["info"].append({"step": "equation_probe"})
try:
    eq = semi.equation()
    log["info"].append({"equation": str(eq), "type": str(type(eq))})
except Exception as e:
    log["info"].append({"equation_error": str(e)})

# Check node group / scope
try:
    scope = semi.scope()
    log["info"].append({"scope": str(scope)})
except Exception as e:
    log["info"].append({"scope_error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


