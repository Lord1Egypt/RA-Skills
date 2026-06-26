#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct diagnostic of opto_result.mph - no config needed.
"""
import sys, json, os
from pathlib import Path

# Ensure mph on path
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
if not mph_file.exists():
    print(json.dumps({"status": "error", "message": f"File not found: {mph_file}"}))
    sys.exit(1)

client = mph.start()
model = client.load(str(mph_file))
jm = model.java

log = {"file": str(mph_file), "size_MB": round(mph_file.stat().st_size/1e6, 2), "checks": []}

# Check 1: FormUnion
comp = jm.component("comp1")
geom = comp.geom("geom1")
try:
    fin = geom.feature("fin")
    action = str(fin.getString("action"))
    log["checks"].append({"item": "form_union", "action": action})
except Exception as e:
    log["checks"].append({"item": "form_union", "error": str(e)})

# Check 2: Physics features - list tags only
semi = comp.physics("semi")
try:
    feat_iter = semi.feature()
    feature_tags = []
    while feat_iter.hasNext():
        feature_tags.append(str(feat_iter.next().tag()))
    log["checks"].append({"item": "physics_features", "count": len(feature_tags), "tags": feature_tags})
except Exception as e:
    log["checks"].append({"item": "physics_features", "error": str(e)})

# Check 3: MetalContact selections
for tag in ["top_contact", "bottom_contact"]:
    try:
        feat = semi.feature(tag)
        sel = feat.selection()
        ents = list(sel.entities())
        log["checks"].append({"item": f"contact_{tag}", "entities": [int(e) for e in ents], "count": len(ents)})
    except Exception as e:
        log["checks"].append({"item": f"contact_{tag}", "error": str(e)})

# Check 4: Studies
study_tags = []
try:
    study_iter = jm.study()
    while study_iter.hasNext():
        study_tags.append(str(study_iter.next().tag()))
    log["checks"].append({"item": "studies", "tags": study_tags})
except Exception as e:
    log["checks"].append({"item": "studies", "error": str(e)})

# Check 5: Solutions
sol_tags = []
try:
    sol_iter = jm.sol()
    while sol_iter.hasNext():
        sol_tags.append(str(sol_iter.next().tag()))
    log["checks"].append({"item": "solutions", "tags": sol_tags})
except Exception as e:
    log["checks"].append({"item": "solutions", "error": str(e)})

# Check 6: Datasets
dataset_tags = []
try:
    if hasattr(jm, 'result') and jm.result():
        ds_iter = jm.result().dataset()
        while ds_iter.hasNext():
            dataset_tags.append(str(ds_iter.next().tag()))
        log["checks"].append({"item": "datasets", "tags": dataset_tags, "count": len(dataset_tags)})
    else:
        log["checks"].append({"item": "datasets", "status": "no_result_node"})
except Exception as e:
    log["checks"].append({"item": "datasets", "error": str(e)})

# Check 7: Try to run study if exists
for st in study_tags:
    try:
        jm.study(st).run()
        log["checks"].append({"item": f"run_study_{st}", "status": "success"})
    except Exception as e:
        log["checks"].append({"item": f"run_study_{st}", "status": "failed", "error": str(e)})

# Check 8: Re-check datasets after run
dataset_tags_after = []
try:
    if hasattr(jm, 'result') and jm.result():
        ds_iter = jm.result().dataset()
        while ds_iter.hasNext():
            dataset_tags_after.append(str(ds_iter.next().tag()))
        log["checks"].append({"item": "datasets_after_run", "tags": dataset_tags_after, "count": len(dataset_tags_after)})
    else:
        log["checks"].append({"item": "datasets_after_run", "status": "no_result_node"})
except Exception as e:
    log["checks"].append({"item": "datasets_after_run", "error": str(e)})

# Save
model.save(str(mph_file))

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


