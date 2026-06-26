#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix solver settings and re-run optoelectronic simulation with better convergence.
Strategy: single-point first (0V), then parametric sweep.
"""
import sys, json, os
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

log = {"status": "fixing", "steps": []}

# Step 1: Remove old study and solver to start fresh
try:
    # Remove old study if exists
    try:
        jm.study().remove("std1")
        log["steps"].append("removed_old_study_std1")
    except Exception:
        pass
    # Remove old solver if exists
    try:
        jm.sol().remove("sol1")
        log["steps"].append("removed_old_solver_sol1")
    except Exception:
        pass
except Exception as e:
    log["steps"].append({"step": "cleanup", "error": str(e)})

# Step 2: Create new study with stationary solver
study = jm.study().create("std1")
stat = study.feature().create("stat1", "Stationary")

# Step 3: Configure solver for semiconductor module
# COMSOL Semiconductor requires specific solver settings
sol = jm.sol().create("sol1")
sol.study("std1")

# Create solver sequence
sol_feat = sol.feature()
sol_feat.create("st1", "StudyStep")
sol_feat("st1").set("study", "std1")

# Variables step
sol_feat.create("v1", "Variables")

# Stationary solver with better convergence settings
stat_solver = sol_feat.create("s1", "Stationary")

# Increase maximum iterations and enable damping
stat_solver.set("maxiter", "100")
stat_solver.set("ntolfact", "10")
stat_solver.set("rhob", "0.9")

# For semiconductor, enable segregated solver or fully coupled
# Try fully coupled first
fc = stat_solver.feature().create("fc1", "FullyCoupled")
fc.set("linsolver", "direct")  # Use direct solver for small 2D problem

# Alternative: try segregated solver if fully coupled fails
# seg = stat_solver.feature().create("seg1", "Segregated")

# Step 4: Run solver
log["steps"].append("solver_configured")

try:
    sol.run()
    log["steps"].append("solver_run_success")
except Exception as e:
    log["steps"].append({"step": "solver_run", "error": str(e)})

# Step 5: Check solution data
try:
    datasets = list(jm.result().dataset())
    dataset_tags = [str(d.tag()) for d in datasets]
    log["steps"].append({"datasets": dataset_tags, "count": len(dataset_tags)})
except Exception as e:
    log["steps"].append({"step": "dataset_check", "error": str(e)})

# Step 6: Try to extract current at 0V
try:
    # Create Global Evaluation
    results = jm.result()
    gev = results.create("gev1", "Global")
    gev.set("expr", "semi.I_1")
    
    # Get data
    data = gev.getData()
    log["steps"].append({"current_I1_at_0V": str(data), "type": str(type(data))})
except Exception as e:
    log["steps"].append({"step": "current_extraction", "error": str(e)})

# Save
model.save(str(mph_file))
print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


