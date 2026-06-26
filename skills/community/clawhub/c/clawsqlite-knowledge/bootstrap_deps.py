#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install dependencies for the clawknowledge skill.

This skill is a thin wrapper around the public `clawsqlite` PyPI package.
It does **not** vendor source code or clone git repositories.
"""
from __future__ import annotations

import os
import subprocess
import sys
import sysconfig
import textwrap
from pathlib import Path


def _workspace_prefix() -> Path:
    return Path(__file__).resolve().parent.parent / ".clawsqlite-venv"


def _site_packages(prefix: Path) -> Path:
    vars_map = {"base": str(prefix), "platbase": str(prefix)}
    return Path(sysconfig.get_path("purelib", vars=vars_map))


def main() -> int:
    # Require clawsqlite>=1.0.2 so older installs get upgraded when the
    # skill is updated. Both the base env and the workspace prefix use
    # the same requirement string to avoid version skew.
    requirement = "clawsqlite>=1.0.2"

    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", requirement]
    proc = subprocess.run(cmd)
    if proc.returncode == 0:
        return 0

    prefix = _workspace_prefix()
    prefix_cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        requirement,
        f"--prefix={prefix}",
    ]
    proc2 = subprocess.run(prefix_cmd)
    site_packages = _site_packages(prefix)
    if proc2.returncode == 0:
        print(
            textwrap.dedent(
                f"""
                NEXT: clawsqlite installed under workspace prefix:
                  {prefix}
                Runtime note:
                  This skill will auto-add:
                    {site_packages}
                  to PYTHONPATH when it exists.
                For manual CLI use, append:
                  PYTHONPATH={site_packages}{os.pathsep}$PYTHONPATH
                """
            ).strip()
        )
        return 0

    print(
        textwrap.dedent(
            f"""
            ERROR: Failed to install clawsqlite via pip.

            NEXT:
              - Try installing into the workspace prefix manually:
                  python -m pip install --upgrade "clawsqlite>=1.0.2" --prefix="{prefix}"
              - Then ensure PYTHONPATH includes:
                  {site_packages}
            """
        ).strip()
    )
    return proc2.returncode or 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
