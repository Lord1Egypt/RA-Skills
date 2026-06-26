#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install mph into workspace-local vendor directory."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"


def _pythonpath_with_vendor() -> str:
    existing = os.environ.get("PYTHONPATH", "")
    parts = [str(VENDOR_DIR)]
    if existing:
        parts.append(existing)
    return os.pathsep.join(parts)


def _run(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, check=False, env=env)


def _verify_import() -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = _pythonpath_with_vendor()
    return _run([
        sys.executable, "-c",
        "import mph; print('mph', mph.__version__); print('path', mph.__file__)"
    ], env=env)


def main() -> None:
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)

    # Install mph + dependencies (JPype1 required for Java bridge)
    command = [
        sys.executable, "-m", "pip", "install",
        "mph", "JPype1", "numpy", "scipy", "matplotlib",
        "--target", str(VENDOR_DIR),
        "--disable-pip-version-check",
        "--no-warn-script-location",
    ]
    install_proc = _run(command)
    verify_proc = _verify_import()

    status = "ok" if install_proc.returncode == 0 and verify_proc.returncode == 0 else "error"
    result = {
        "status": status,
        "vendor_dir": str(VENDOR_DIR),
        "install_returncode": install_proc.returncode,
        "verify_returncode": verify_proc.returncode,
    }
    if install_proc.stdout.strip():
        result["install_stdout"] = install_proc.stdout.strip()[-500:]
    if install_proc.stderr.strip():
        result["install_stderr"] = install_proc.stderr.strip()[-500:]
    if verify_proc.stdout.strip():
        result["verify_stdout"] = verify_proc.stdout.strip()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return status == "ok"


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
