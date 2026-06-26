#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_env.py — Helper for checking Python and installing pyFAI environments
install_env.py — 用于检查 Python 并安装 pyFAI 环境的辅助脚本
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run(command: list[str], dry_run: bool) -> None:
    """Run or print a command. / 执行或打印命令。"""
    print(json.dumps({"event": "command", "argv": command}, ensure_ascii=False), flush=True)
    if dry_run:
        return
    subprocess.run(command, check=True)


def main() -> int:
    """CLI entrypoint. / 命令行入口。"""
    parser = argparse.ArgumentParser(
        description="Check Python and create a pyFAI-ready virtual environment"
    )
    parser.add_argument("--venv", default=".venv-pyfai", help="Virtualenv directory")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use")
    parser.add_argument(
        "--extras",
        nargs="*",
        default=["pyFAI>=2024.1", "fabio>=2024.1", "h5py>=3.7", "numpy>=1.22"],
        help="Packages to install",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands only")
    args = parser.parse_args()

    python_path = shutil.which(args.python) if args.python != sys.executable else args.python
    if not python_path:
        print(
            json.dumps(
                {
                    "event": "missing_python",
                    "message": "Python not found. Install Python 3.10+ first.",
                    "windows": "https://www.python.org/downloads/windows/",
                    "macos": "brew install python or python.org installer",
                    "linux": "Use apt/yum/mamba/conda to install python3 and python3-venv",
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return 1

    venv_dir = Path(args.venv)
    _run([python_path, "-m", "venv", str(venv_dir)], args.dry_run)

    if sys.platform.startswith("win"):
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    packages = [str(pkg) for pkg in args.extras]
    _run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        args.dry_run,
    )
    _run([str(venv_python), "-m", "pip", "install", *packages], args.dry_run)

    print(
        json.dumps(
            {
                "event": "done",
                "venv": str(venv_dir),
                "python": str(venv_python),
                "activate_windows": str(venv_dir / "Scripts" / "activate"),
                "activate_posix": f"source {venv_dir}/bin/activate",
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
