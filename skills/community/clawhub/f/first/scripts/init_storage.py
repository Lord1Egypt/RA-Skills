#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import ensure_storage

path = ensure_storage()
print("✓ Firstprinciples storage initialized")
print(" ", path)
