#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep probe: inspect solution data structure and try to find valid variables.
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

log = {"status": "deep_probe", "info": []}

# 1. Get available solution datasets
try:
    ds_list = jm.result().dataset()
    for ds in ds_list:
        tag = str(ds.tag())
        info = {"dataset_tag": tag}
        # Try to get data shape
        try:
            data = ds.getData()
            info["data_type"] = str(type(data))
            if hasattr(data, 'shape'):
                info["shape"] = str(data.shape)
        except Exception as e:
            info["data_error"] = str(e)
        log["info"].append(info)
except Exception as e:
    log["dataset_error"] = str(e)

# 2. List all expressions in model via mph
log["info"].append({"step": "mph_expressions"})
try:
    # Try to get expressions from model
    exprs = model.expressions()
    log["info"].append({"expressions_count": len(exprs), "sample": exprs[:50]})
except Exception as e:
    log["info"].append({"expressions_error": str(e)})

# 3. Try to export solution data directly
try:
    results = jm.result()
    # Create a table with parameter values
    table = results.table().create("tbl1", "Table")
    # Try to populate with V_bias and some expression
    
    # Alternative: try to get all variables in sol1
    sol = jm.sol("sol1")
    log["info"].append({"sol_features": []})
    
    # Try to get solution data as numpy array via mph
    for expr in ["V_bias", "x", "y", "z"]:
        try:
            data = model.evaluate(expr)
            log["info"].append({"expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:100]})
        except Exception as e:
            log["info"].append({"expr": expr, "error": str(e)})
except Exception as e:
    log["info"].append({"export_error": str(e)})

# 4. Try to evaluate on a specific boundary
try:
    # Get boundary dataset
    bdset = jm.result().dataset().create("dset_bd", "Boundary")
    bdset.selection().named("sel_bottom")
    
    for expr in ["semi.Jn", "semi.Jp", "semi.Jtot"]:
        try:
            data = model.evaluate(expr, dataset="dset_bd")
            log["info"].append({"boundary_expr": expr, "shape": str(data.shape) if hasattr(data, 'shape') else "N/A", "sample": str(data)[:200]})
        except Exception as e:
            log["info"].append({"boundary_expr": expr, "error": str(e)})
except Exception as e:
    log["info"].append({"boundary_dataset_error": str(e)})

# 5. Try direct Java API to get solution data
log["info"].append({"step": "java_api_probe"})
try:
    sol = jm.sol("sol1")
    # Try to get solution vectors
    sol_data = sol.getSolutionData()
    log["info"].append({"sol_data_type": str(type(sol_data)), "sol_data_str": str(sol_data)[:200]})
except Exception as e:
    log["info"].append({"java_sol_data_error": str(e)})

# 6. Try to get parameter list from solution
try:
    sol = jm.sol("sol1")
    # Get parameter names and values
    param_names = sol.getParamNames()
    param_values = sol.getParam()
    log["info"].append({"param_names": [str(p) for p in param_names], "param_values": str(param_values)[:200]})
except Exception as e:
    log["info"].append({"param_error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


