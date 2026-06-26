#!/usr/bin/env python3
"""Start the brave_shim server. Run from skill directory or provide brave_shim path."""

import os, sys, subprocess

# Default path - assume brave_shim_repo is next to this skill folder
SKILL_DIR = os.path.dirname(__file__)
DEFAULT_SHIM = os.path.join(SKILL_DIR, "..", "brave_shim_repo", "brave_shim.py")

def main():
    shim_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SHIM
    if not os.path.exists(shim_path):
        print(f"brave_shim.py not found at {shim_path}")
        print("Run scripts/setup_brave_shim.py first, or pass path as argument")
        sys.exit(1)

    venv_python = os.path.join(os.path.dirname(shim_path), "venv", "Scripts" if sys.platform == "win32" else "bin", "python")
    if not os.path.exists(venv_python):
        venv_python = "python"  # fallback to system python

    print(f"Starting brave_shim from {shim_path}...")
    subprocess.run(f'"{venv_python}" "{shim_path}"', shell=True)

if __name__ == "__main__":
    main()
