#!/usr/bin/env python3
"""Check that all dependencies are available for rice phenotype prediction."""
import sys

OK = True

def check(name, min_ver=None):
    global OK
    try:
        mod = __import__(name)
        ver = getattr(mod, "__version__", "?")
        print(f"  [OK] {name} {ver}")
    except ImportError:
        print(f"  [MISSING] {name} — pip install {name}")
        OK = False

print("Checking dependencies...")
check("torch")
check("numpy")
check("pandas")
check("sklearn")
check("scipy")
check("requests")

print()

import torch
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)} (cuda:0)")
else:
    print("GPU: not available, will use CPU (slower but works)")

print()

import os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base, "data")
checks = [
    ("data/vae_features.csv", "Built-in genotype features"),
    ("data/season_history.csv", "Historical season data"),
    ("data/grid_points.json", "Grid point definitions"),
    ("data/models_gene/wh.pt", "Genotype model (sample)"),
    ("data/models_env/hd.pt", "Environment model (sample)"),
]
print("Checking data files...")
for path, desc in checks:
    full = os.path.join(base, path)
    if os.path.exists(full):
        print(f"  [OK] {desc}")
    else:
        print(f"  [MISSING] {desc}: {full}")
        OK = False

print()
if OK:
    print("All checks passed. Ready to use.")
else:
    print("Some checks failed. Install missing packages: pip install -r requirements.txt")
    sys.exit(1)
