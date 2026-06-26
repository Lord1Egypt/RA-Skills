#!/usr/bin/env python3
"""Quick probe: check if opto_result.mph has a valid solution."""
import sys, json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph

mph_file = SKILL_DIR / "opto_result.mph"
if not mph_file.exists():
    print(json.dumps({"status": "error", "message": f"File not found: {mph_file}"}))
    sys.exit(1)

client = mph.start()
model = client.load(str(mph_file))
jm = model.java

# Check studies and solutions
studies = list(jm.study())
sols = list(jm.sol())

result = {
    "file": str(mph_file),
    "file_size_MB": round(mph_file.stat().st_size / 1e6, 2),
    "studies": [],
    "solutions": [],
    "has_solution_data": False,
}

for s in studies:
    result["studies"].append({
        "tag": str(s),
        "name": str(jm.study(s).name()),
    })

for s in sols:
    sol = jm.sol(s)
    info = {"tag": str(s), "name": str(sol.name())}
    # Try to get solution dataset info
    try:
        datasets = list(sol.dataset()) if hasattr(sol, 'dataset') else []
        info["datasets"] = [str(d) for d in datasets]
    except Exception as e:
        info["dataset_error"] = str(e)
    result["solutions"].append(info)

# Check if any dataset has actual data
if hasattr(jm, 'result') and jm.result():
    datasets = list(jm.result().dataset())
    result["result_datasets"] = [str(d) for d in datasets]
    for d in datasets:
        try:
            ds = jm.result().dataset(d)
            # Try to read data shape
            if hasattr(ds, 'getName'):
                result["has_solution_data"] = True
                break
        except Exception:
            pass

# Also check via model.dataset()
try:
    all_datasets = list(model.datasets())
    result["model_datasets"] = all_datasets
    if all_datasets:
        result["has_solution_data"] = True
except Exception as e:
    result["model_datasets_error"] = str(e)

print(json.dumps(result, indent=2, ensure_ascii=False))
model.clear()
client.disconnect()
