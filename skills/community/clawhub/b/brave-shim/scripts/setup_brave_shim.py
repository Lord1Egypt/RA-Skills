#!/usr/bin/env python3
"""Setup brave_shim: clone repo, create venv, install dependencies."""

import os, sys, subprocess, shutil

REPO_URL = "https://github.com/asoraruf/brave_shim"
DEST = os.path.join(os.path.dirname(__file__), "..", "brave_shim_repo")
VENV_DIR = os.path.join(DEST, "venv")

def run(cmd, check=True, **kwargs):
    print(f"Running: {cmd}")
    r = subprocess.run(cmd, shell=True, **kwargs)
    if check and r.returncode != 0:
        sys.exit(f"Failed: {cmd}")
    return r

def main():
    # Clone
    if os.path.exists(DEST):
        print(f"Already exists at {DEST}, skipping clone")
    else:
        run(f'git clone {REPO_URL} "{DEST}"')

    # Detect Python
    py = "python" if sys.platform == "win32" else "python3"
    activate = os.path.join(VENV_DIR, "Scripts" if sys.platform == "win32" else "bin", "python")

    # Create venv
    if not os.path.exists(VENV_DIR):
        run(f"{py} -m venv \"{VENV_DIR}\"")

    # Install deps
    pip = os.path.join(VENV_DIR, "Scripts" if sys.platform == "win32" else "bin", "pip")
    run(f'"{pip}" install fastapi uvicorn ddgs pyyaml')

    print(f"\nSetup complete!")
    print(f"Start shim:   {activate} \"{os.path.join(DEST, 'brave_shim.py')}\"")
    print(f"Or activate:   {os.path.join(DEST, 'venv', 'Scripts', 'activate')}")

if __name__ == "__main__":
    main()
