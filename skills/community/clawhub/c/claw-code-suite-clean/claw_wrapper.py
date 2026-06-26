#!/usr/bin/env python3
# Moved to scripts/claw_wrapper.py
# This file is kept for compatibility.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from scripts.claw_wrapper import main

if __name__ == "__main__":
    sys.exit(main())