#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get COMSOL version and check for model warnings.
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

client = mph.start()
log = {"status": "version_probe", "info": []}

# Get COMSOL version
try:
    version = client.version()
    log["info"].append({"comsol_version": str(version)})
except Exception as e:
    log["info"].append({"version_error": str(e)})

# Load model and check for warnings
mph_file = SKILL_DIR / "output" / "optoelectronic" / "opto_result.mph"
model = client.load(str(mph_file))
jm = model.java

# Check model messages / warnings
try:
    log["info"].append({"model_info": str(jm)})
except Exception as e:
    log["info"].append({"model_info_error": str(e)})

# Try to get warnings from physics
comp = jm.component("comp1")
semi = comp.physics("semi")
try:
    log["info"].append({"semi_info": str(semi)})
except Exception as e:
    log["info"].append({"semi_info_error": str(e)})

# Check geometry dimension
geom = comp.geom("geom1")
try:
    log["info"].append({"geom_info": str(geom)})
    # Get space dimension
    dim = geom.getSDim()
    log["info"].append({"space_dimension": int(dim)})
except Exception as e:
    log["info"].append({"geom_dim_error": str(e)})

# Check if physics was created with correct dimension
try:
    log["info"].append({"semi_dim": str(semi.getString("sdim"))})
except Exception as e:
    log["info"].append({"semi_dim_error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


