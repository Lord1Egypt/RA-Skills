#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract I-V and key metrics from COMSOL optoelectronic simulation result.
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
if not mph_file.exists():
    print(json.dumps({"status": "error", "message": f"File not found: {mph_file}"}))
    sys.exit(1)

client = mph.start()
model = client.load(str(mph_file))
jm = model.java

log = {"status": "probing", "checks": []}

# Check 1: Parametric sweep values
try:
    param = jm.param()
    log["checks"].append({"item": "param_V_bias", "value": str(param.get("V_bias"))})
except Exception as e:
    log["checks"].append({"item": "param_V_bias", "error": str(e)})

# Check 2: Try to get current from various expressions
expressions_to_try = [
    "semi.I_1",  # Current at first metal contact
    "semi.I_2",  # Current at second metal contact
    "semi.I_top_contact", 
    "semi.I_bottom_contact",
    "semi.I_ec1",  # Terminal current
    "ec1.I0",  # Alternative
    "comp1.semi.I_1",
    "comp1.semi.I_2",
]

# Check available expressions in semi
semi = jm.component("comp1").physics("semi")
feature_tags = []
try:
    feat_list = semi.feature()
    for f in feat_list:
        feature_tags.append(str(f.tag()))
    log["checks"].append({"item": "semi_features", "tags": feature_tags})
except Exception as e:
    log["checks"].append({"item": "semi_features", "error": str(e)})

# Try to evaluate current via Global Evaluation or Point Evaluation
# First, create a dataset and evaluate expression
for expr in expressions_to_try:
    try:
        # Create a Global Evaluation node
        results = jm.result()
        eval_tag = f"gev_test_{expr.replace('.', '_')}"
        try:
            gev = results.create(eval_tag, "Global")
        except Exception:
            # If already exists, use it
            gev = results(eval_tag)
        gev.set("expr", expr)
        # Run evaluation - this might require solution dataset
        # Try to get data
        data = gev.getData()
        log["checks"].append({"item": f"eval_{expr}", "data_shape": str(data.shape) if hasattr(data, 'shape') else str(type(data)), "sample": str(data)[:200]})
    except Exception as e:
        log["checks"].append({"item": f"eval_{expr}", "error": str(e)[:200]})

# Alternative: try to get data via model.evaluate()
try:
    # Get all solution datasets
    datasets = []
    ds_list = jm.result().dataset()
    for ds in ds_list:
        datasets.append(str(ds.tag()))
    log["checks"].append({"item": "datasets", "tags": datasets})
    
    if datasets:
        # Try to evaluate semi.I_1 on first dataset
        dataset_tag = datasets[0]
        for expr in ["semi.I_1", "semi.I_2"]:
            try:
                data = model.evaluate(expr, dataset=dataset_tag)
                log["checks"].append({"item": f"model_eval_{expr}", "data_type": str(type(data)), "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:300]})
            except Exception as e:
                log["checks"].append({"item": f"model_eval_{expr}", "error": str(e)[:200]})
except Exception as e:
    log["checks"].append({"item": "datasets_probe", "error": str(e)})

# Check 3: Get V_bias sweep values from parametric solution
try:
    # Try to get parameter values from solution
    sol = jm.sol("sol1")
    log["checks"].append({"item": "sol1_info", "info": str(sol)})
except Exception as e:
    log["checks"].append({"item": "sol1_info", "error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


