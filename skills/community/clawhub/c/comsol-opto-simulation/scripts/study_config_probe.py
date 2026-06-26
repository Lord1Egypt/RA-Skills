#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check study configuration and physics inclusion.
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

log = {"status": "study_config_probe", "info": []}

# Check study features
study = jm.study("std1")
for feat_tag in ["stat1"]:
    try:
        feat = study.feature(feat_tag)
        log["info"].append({"study_feat": feat_tag, "type": str(feat.getType())})
        
        # Check which physics are included
        try:
            phys_list = feat.getPhysics()
            log["info"].append({"study_feat": feat_tag, "physics": [str(p) for p in phys_list]})
        except Exception as e:
            log["info"].append({"study_feat": feat_tag, "physics_error": str(e)})
            
        # Check disabled physics
        try:
            disabled = feat.getDisabledPhysics()
            log["info"].append({"study_feat": feat_tag, "disabled_physics": [str(p) for p in disabled]})
        except Exception as e:
            log["info"].append({"study_feat": feat_tag, "disabled_physics_error": str(e)})
            
        # Check physics control
        try:
            ctrl = feat.getString("physicscontrol")
            log["info"].append({"study_feat": feat_tag, "physics_control": ctrl})
        except Exception as e:
            log["info"].append({"study_feat": feat_tag, "physics_control_error": str(e)})
            
    except Exception as e:
        log["info"].append({"study_feat": feat_tag, "error": str(e)})

# Check if semi physics is active in component
try:
    semi = jm.component("comp1").physics("semi")
    log["info"].append({"semi_active": str(semi.isActive())})
except Exception as e:
    log["info"].append({"semi_active_error": str(e)})

# Check model's feature list
log["info"].append({"step": "model_features"})
try:
    mf = jm.feature()
    while mf.hasNext():
        f = mf.next()
        log["info"].append({"model_feat": str(f.tag()), "type": str(f.getType())})
except Exception as e:
    log["info"].append({"model_feat_error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


