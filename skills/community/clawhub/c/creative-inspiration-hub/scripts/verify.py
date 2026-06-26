#!/usr/bin/env python3
"""Release verification for Creative Inspiration Hub."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.2.0"


def main():
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for file_name in ["skill.json", "package.json", "clawhub.json", "_meta.json"]:
        data = json.loads((ROOT / file_name).read_text(encoding="utf-8"))
        if data["version"] != EXPECTED_VERSION:
            raise SystemExit(f"{file_name} version is not {EXPECTED_VERSION}")
    if f"version: {EXPECTED_VERSION}" not in skill_md:
        raise SystemExit("SKILL.md frontmatter version mismatch")

    print("[verify] compiling")
    subprocess.run([sys.executable, "-m", "py_compile", "handler.py", "scripts/test.py"], cwd=ROOT, check=True)

    print("[verify] testing branches")
    subprocess.run([sys.executable, "scripts/test.py"], cwd=ROOT, check=True)

    print("[verify] ok")


if __name__ == "__main__":
    main()
