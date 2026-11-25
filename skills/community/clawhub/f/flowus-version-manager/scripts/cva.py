#!/usr/bin/env python3
"""Run from an installed self-contained skill or the development source tree."""
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
if not (here / "flowus_version_manager").is_dir():
    sys.path.insert(0, str(here.parents[2]))

from flowus_version_manager.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
