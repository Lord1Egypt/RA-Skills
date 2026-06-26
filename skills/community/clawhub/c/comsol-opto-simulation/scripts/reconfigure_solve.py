#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconfigure solver for better convergence and re-run.
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

log = {"status": "reconfiguring", "steps": []}

# Step 1: Remove parametric sweep, do single point first
try:
    study = jm.study("std1")
    # Remove parametric feature
    try:
        study.feature().remove("param1")
        log["steps"].append("removed_parametric")
    except Exception as e:
        log["steps"].append({"step": "remove_parametric", "error": str(e)})
except Exception as e:
    log["steps"].append({"step": "study_access", "error": str(e)})

# Step 2: Remove old solver and recreate
try:
    jm.sol().remove("sol1")
    log["steps"].append("removed_old_sol1")
except Exception as e:
    log["steps"].append({"step": "remove_sol1", "error": str(e)})

# Step 3: Create fresh solver
sol = jm.sol().create("sol1")
sol.study("std1")

# Step 4: Configure solver features
sol_feat = sol.feature()
st = sol_feat.create("st1", "StudyStep")
st.set("study", "std1")

v = sol_feat.create("v1", "Variables")

s = sol_feat.create("s1", "Stationary")

# Try to get inner feature list and configure
inner = s.feature()

# Remove auto-generated fc1 if exists, try segregated for semiconductor
try:
    inner.remove("fc1")
    log["steps"].append("removed_auto_fc1")
except Exception:
    pass

# Add segregated solver - better for semiconductor
seg = inner.create("seg1", "Segregated")
seg.set("segtermauto", "on")
seg.set("segtermmax", "100")

# Add segregated steps for semiconductor variables
seg_step1 = seg.feature().create("ss1", "SegregatedStep")
seg_step1.set("segvar", "comp1_semi_V")

seg_step2 = seg.feature().create("ss2", "SegregatedStep")
seg_step2.set("segvar", "comp1_semi_n")

seg_step3 = seg.feature().create("ss3", "SegregatedStep")
seg_step3.set("segvar", "comp1_semi_p")

# Direct linear solver for each step (small 2D problem)
seg.set("linsolver", "direct")

log["steps"].append("solver_reconfigured_with_segregated")

# Step 5: Run
log["steps"].append("starting_solve")
try:
    sol.run()
    log["steps"].append("solve_completed")
except Exception as e:
    log["steps"].append({"step": "solve", "error": str(e)})

# Step 6: Check datasets
try:
    ds_list = jm.result().dataset()
    datasets = []
    for ds in ds_list:
        datasets.append(str(ds.tag()))
    log["steps"].append({"datasets_after_solve": datasets})
except Exception as e:
    log["steps"].append({"step": "dataset_check", "error": str(e)})

# Step 7: Try current extraction
try:
    results = jm.result()
    gev = results.create("gev_iv", "Global")
    gev.set("expr", "semi.I_1")
    # Try to get data string
    data_str = str(gev.getData())
    log["steps"].append({"current_I1": data_str[:500]})
except Exception as e:
    log["steps"].append({"step": "current_extraction", "error": str(e)})

# Save
model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


