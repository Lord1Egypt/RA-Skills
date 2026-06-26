"""Bootstrap a local venv and install script dependencies.

This is optional; you can also run:
    python3 -m pip install -r scripts/requirements.txt
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = root / "scripts"
    req = scripts / "requirements.txt"
    venv_dir = root / ".venv"

    if not req.exists():
        print(f"requirements not found: {req}")
        return 1

    # Create venv
    if not venv_dir.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])

    py = _venv_python(venv_dir)
    if not py.exists():
        print(f"venv python not found: {py}")
        return 1

    # Install deps
    subprocess.check_call([str(py), "-m", "pip", "install", "-U", "pip"])
    subprocess.check_call([str(py), "-m", "pip", "install", "-r", str(req)])

    print("ok")
    print(f"venv: {venv_dir}")
    print(f"run: {py} {scripts / 'fetch_crypto.py'} --symbol BTC/USDT")
    print(f"run: {py} {scripts / 'fetch_ashare.py'} --code 600519")
    print(f"run: {py} {scripts / 'fetch_morning.py'} --date 20260311")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
