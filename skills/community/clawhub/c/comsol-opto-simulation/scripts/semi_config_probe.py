#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed probe of Semiconductor physics configuration.
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

log = {"status": "semi_config_probe", "features": []}

# List all features in semi physics
feat_list = semi.feature()
for feat in feat_list:
    tag = str(feat.tag())
    ftype = str(feat.getType())
    info = {"tag": tag, "type": ftype}
    
    # Try to get selection
    try:
        sel = feat.selection()
        ents = list(sel.entities())
        info["selection_entities"] = [int(e) for e in ents]
    except Exception as e:
        info["selection_error"] = str(e)
    
    # Try to get properties
    try:
        props = feat.properties()
        info["properties"] = [str(p) for p in props]
    except Exception as e:
        info["properties_error"] = str(e)
    
    # Try to get specific property values
    if ftype == "SemiconductorMaterialModel":
        for prop in ["Eg0", "chi0", "mun", "mup", "Nc", "Nv", "donorConcentration", "acceptorConcentration"]:
            try:
                val = str(feat.getString(prop))
                info[prop] = val
            except Exception:
                pass
    
    if ftype == "MetalContact":
        for prop in ["V0", "ContactType"]:
            try:
                val = str(feat.getString(prop))
                info[prop] = val
            except Exception:
                pass
    
    log["features"].append(info)

# Check if semi is active on any domain
try:
    sel = semi.selection()
    ents = list(sel.entities())
    log["semi_selection"] = [int(e) for e in ents]
except Exception as e:
    log["semi_selection_error"] = str(e)

# Check number of DOFs from solver message
sol = jm.sol("sol1")
s1 = sol.feature("s1")
log["solver_message"] = str(s1.getString("message"))

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


