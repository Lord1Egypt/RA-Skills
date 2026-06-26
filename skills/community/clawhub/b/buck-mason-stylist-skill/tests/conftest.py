"""Pytest config — adds scripts/ and scripts/lib/ to the Python path.

The scripts in scripts/ are designed as standalone executables; for unit
testing we want to import their helper modules (lib/profile.py, etc.) and
run the scripts as subprocesses for end-to-end-ish tests.
"""
import pathlib, sys

REPO_ROOT   = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

# scripts/lib is importable as `lib.<module>`
sys.path.insert(0, str(SCRIPTS_DIR))
