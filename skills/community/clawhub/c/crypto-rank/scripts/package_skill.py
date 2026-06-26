#!/usr/bin/env python3
"""Package the ClawHub skill directory into a zip archive."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    output_dir = skill_root / "dist"
    output_dir.mkdir(exist_ok=True)

    version = "1.0.0"
    archive = output_dir / f"{skill_root.name}-{version}.zip"

    ignored = {"dist", "__pycache__", ".DS_Store"}
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zf:
        for path in skill_root.rglob("*"):
            relative = path.relative_to(skill_root)
            if any(part in ignored for part in relative.parts):
                continue
            if path.is_file():
                zf.write(path, arcname=str(relative))

    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
