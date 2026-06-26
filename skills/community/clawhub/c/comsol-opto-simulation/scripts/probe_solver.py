#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probe solver configuration in existing model.
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

log = {"status": "probing_solver", "info": {}}

# Study info
try:
    study = jm.study("std1")
    log["info"]["study_std1"] = str(study)
    
    # List study features
    feat_tags = []
    feat_list = study.feature()
    for f in feat_list:
        feat_tags.append({"tag": str(f.tag()), "type": str(f.getType())})
    log["info"]["study_features"] = feat_tags
except Exception as e:
    log["info"]["study_error"] = str(e)

# Solver info
try:
    sol = jm.sol("sol1")
    log["info"]["sol1"] = str(sol)
    
    # List solver features
    sol_feat_tags = []
    sol_feat_list = sol.feature()
    for f in sol_feat_list:
        sol_feat_tags.append({"tag": str(f.tag()), "type": str(f.getType())})
    log["info"]["solver_features"] = sol_feat_tags
except Exception as e:
    log["info"]["solver_error"] = str(e)

# Check if study has computed
try:
    log["info"]["study_computed"] = str(study.hasComputed())
except Exception as e:
    log["info"]["study_computed_error"] = str(e)

# Check solution info
try:
    sol = jm.sol("sol1")
    log["info"]["sol_info"] = str(sol.getInfo())
except Exception as e:
    log["info"]["sol_info_error"] = str(e)

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


