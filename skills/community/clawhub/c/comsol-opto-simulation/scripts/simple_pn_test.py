#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplest possible test: Si p-n junction in COMSOL.
If this works, our heterostructure model has a config issue.
If this doesn't work, COMSOL Semiconductor module has a deeper problem.
"""
import sys, json
import re
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
model = client.create("pn_junction_test")
jm = model.java

log = {"status": "simple_pn_test", "steps": []}


def set_userdef(feature, key, value):
    try:
        feature.set(f"{key}_mat", "userdef")
    except Exception:
        pass
    feature.set(key, value)


def add_doping(semi, tag, domain, dopant_type, concentration):
    dop = semi.feature().create(tag, "AnalyticDopingModel")
    dop.selection().set([domain])
    dop.set("FeatureType", "Doping")
    dop.set("impurityType", dopant_type)
    if dopant_type == "donor":
        dop.set("NDc", concentration)
    else:
        dop.set("NAc", concentration)


def parse_dof(message):
    match = re.search(r"自由度数：(\d+)", message)
    if match:
        return int(match.group(1))
    match = re.search(r"degrees of freedom:\s*(\d+)", message, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

# 1. Create 2D geometry with two rectangles
comp = jm.component().create("comp1", True)
geom = comp.geom().create("geom1", 2)

# p-region rectangle
rect_p = geom.feature().create("rect_p", "Rectangle")
rect_p.set("size", ["500[nm]", "500[nm]"])
rect_p.set("pos", ["0[nm]", "0[nm]"])

# n-region rectangle
rect_n = geom.feature().create("rect_n", "Rectangle")
rect_n.set("size", ["500[nm]", "500[nm]"])
rect_n.set("pos", ["500[nm]", "0[nm]"])

geom.run()

# 2. Create mesh
mesh = comp.mesh().create("mesh1")
mesh.feature().create("size1", "Size")
mesh.feature("size1").set("hmax", "50[nm]")
mesh.feature().create("ftri1", "FreeTri")
mesh.run()

# 3. Create Semiconductor physics
semi = comp.physics().create("semi", "Semiconductor", "geom1")

# 4. Add material models
# p-region
mat_p = semi.feature().create("mat_p", "SemiconductorMaterialModel")
mat_p.selection().set([1])
set_userdef(mat_p, "Eg0", "1.12[eV]")
set_userdef(mat_p, "chi0", "4.05[eV]")
set_userdef(mat_p, "mun", "1000[cm^2/(V*s)]")
set_userdef(mat_p, "mup", "500[cm^2/(V*s)]")
set_userdef(mat_p, "Nc", "2.8e19[1/cm^3]")
set_userdef(mat_p, "Nv", "1.04e19[1/cm^3]")
set_userdef(mat_p, "epsilonr", "11.7")
add_doping(semi, "dop_p", 1, "acceptor", "1e16[1/cm^3]")

# n-region
mat_n = semi.feature().create("mat_n", "SemiconductorMaterialModel")
mat_n.selection().set([2])
set_userdef(mat_n, "Eg0", "1.12[eV]")
set_userdef(mat_n, "chi0", "4.05[eV]")
set_userdef(mat_n, "mun", "1000[cm^2/(V*s)]")
set_userdef(mat_n, "mup", "500[cm^2/(V*s)]")
set_userdef(mat_n, "Nc", "2.8e19[1/cm^3]")
set_userdef(mat_n, "Nv", "1.04e19[1/cm^3]")
set_userdef(mat_n, "epsilonr", "11.7")
add_doping(semi, "dop_n", 2, "donor", "1e16[1/cm^3]")

# 5. Add MetalContacts
anode = semi.feature().create("anode", "MetalContact")
anode.selection().set([1])  # Left boundary
cathode = semi.feature().create("cathode", "MetalContact")
cathode.selection().set([7])  # Right boundary - need to verify

# 6. Create study
study = jm.study().create("std1")
stat = study.feature().create("stat1", "Stationary")

# 7. Solve
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

# 8. Check results
log["steps"].append("checking_results")
try:
    sol = jm.sol("sol1")
    s1 = sol.feature("s1")
    message = str(s1.getString("message"))
    log["steps"].append({"dof": parse_dof(message), "solver_message": message})
    
    for expr in ["semi.I_1", "semi.I_2", "V", "semi.normJ"]:
        try:
            data = model.evaluate(expr, inner="first")
            log["steps"].append({"expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:200]})
        except Exception as e:
            log["steps"].append({"expr": expr, "error": str(e)})
except Exception as e:
    log["steps"].append({"result_check_error": str(e)})

# Save test model
test_file = SKILL_DIR / "output" / "optoelectronic" / "pn_test.mph"
model.save(str(test_file))

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


