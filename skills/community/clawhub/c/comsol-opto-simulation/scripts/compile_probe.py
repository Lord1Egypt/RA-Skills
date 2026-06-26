#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Force equation compilation and check DOF count.
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

log = {"status": "compile_probe", "steps": []}

# Try to compile equations manually
log["steps"].append("compiling")
try:
    study = jm.study("std1")
    # Try to get compiled equations
    eq = study.getEquations("stat1")
    log["steps"].append({"compiled_equations": str(eq)[:500]})
except Exception as e:
    log["steps"].append({"compile_error": str(e)})

# Alternative: try to get number of DOFs from sol info
log["steps"].append("checking_sol_info")
try:
    sol = jm.sol("sol1")
    # Try to get feature "st1" and check its properties
    st1 = sol.feature("st1")
    for prop in ["studystep", "useinitsol", "initsol", "initsoluse"]:
        try:
            val = str(st1.getString(prop))
            log["steps"].append({"prop": prop, "value": val})
        except Exception:
            pass
except Exception as e:
    log["steps"].append({"sol_info_error": str(e)})

# Check if mesh exists and has elements
log["steps"].append("checking_mesh")
try:
    mesh = jm.component("comp1").mesh("mesh1")
    log["steps"].append({"mesh_info": str(mesh)})
    
    # Try to get number of elements
    try:
        stats = mesh.getStatistics()
        log["steps"].append({"mesh_stats": str(stats)})
    except Exception as e:
        log["steps"].append({"mesh_stats_error": str(e)})
except Exception as e:
    log["steps"].append({"mesh_error": str(e)})

# Try model.clear() and rebuild from scratch
log["steps"].append("clearing_model")
try:
    model.clear()
    log["steps"].append("cleared")
except Exception as e:
    log["steps"].append({"clear_error": str(e)})

# Rebuild
log["steps"].append("rebuilding")
try:
    model.build()
    log["steps"].append("rebuilt")
except Exception as e:
    log["steps"].append({"rebuild_error": str(e)})

# Re-solve
log["steps"].append("resolving")
try:
    model.solve()
    log["steps"].append("resolved")
except Exception as e:
    log["steps"].append({"resolve_error": str(e)})

# Check solver message after resolve
try:
    sol = jm.sol("sol1")
    s1 = sol.feature("s1")
    msg = str(s1.getString("message"))
    log["steps"].append({"solver_message_after_resolve": msg})
except Exception as e:
    log["steps"].append({"solver_msg_error": str(e)})

model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


