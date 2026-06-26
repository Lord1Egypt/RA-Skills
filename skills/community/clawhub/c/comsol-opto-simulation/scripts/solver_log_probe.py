#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get solver log and convergence info from COMSOL.
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

log = {"status": "solver_log_probe", "info": []}

# 1. Try to get solver sequence log
try:
    sol = jm.sol("sol1")
    # Try various methods to get log
    log["info"].append({"sol_str": str(sol)})
    
    # Get solver feature details
    s1 = sol.feature("s1")
    log["info"].append({"s1_str": str(s1)})
    
    # Try to get iteration log
    try:
        iter_log = s1.getIterLog()
        log["info"].append({"iter_log": str(iter_log)[:500]})
    except Exception as e:
        log["info"].append({"iter_log_error": str(e)})
        
    # Try to get feature properties
    try:
        props = s1.properties()
        log["info"].append({"s1_properties": [str(p) for p in props]})
    except Exception as e:
        log["info"].append({"properties_error": str(e)})
        
except Exception as e:
    log["info"].append({"sol_access_error": str(e)})

# 2. Try to get COMSOL log via mph client
try:
    log_text = client.caught_stdout()
    log["info"].append({"client_stdout": log_text[-2000:] if log_text else "empty"})
except Exception as e:
    log["info"].append({"stdout_error": str(e)})

# 3. Check if solution has actual data for any variable
# Try a simple expression that should exist in any model
try:
    data = model.evaluate("1")
    log["info"].append({"constant_eval": str(data)[:200]})
except Exception as e:
    log["info"].append({"constant_eval_error": str(e)})

# 4. Try model.inner() to get all inner variables
try:
    inner_vars = model.inner()
    log["info"].append({"inner_count": len(inner_vars), "sample": inner_vars[:30]})
except Exception as e:
    log["info"].append({"inner_error": str(e)})

# 5. Try to get solution at a specific parameter value
try:
    # model.evaluate with inner parameter
    data = model.evaluate("V_bias", inner={"V_bias": 0})
    log["info"].append({"V_bias_at_0": str(data)})
except Exception as e:
    log["info"].append({"V_bias_at_0_error": str(e)})

print(json.dumps(log, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()


