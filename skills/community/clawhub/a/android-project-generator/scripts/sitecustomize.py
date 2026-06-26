#!/usr/bin/env python3
"""
Python startup customization for direct script execution from the scripts/ directory.

This file is discovered automatically by Python before normal imports when
running commands like `python scripts/generate_report.py`.
"""

import os
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = PROJECT_ROOT / "cache"
PYCACHE_ROOT = CACHE_ROOT / "pycache"
TMP_ROOT = CACHE_ROOT / "tmp" / "python"

CACHE_ROOT.mkdir(parents=True, exist_ok=True)
PYCACHE_ROOT.mkdir(parents=True, exist_ok=True)
TMP_ROOT.mkdir(parents=True, exist_ok=True)

sys.pycache_prefix = str(PYCACHE_ROOT)
os.environ["PYTHONPYCACHEPREFIX"] = str(PYCACHE_ROOT)
tempfile.tempdir = str(TMP_ROOT)
