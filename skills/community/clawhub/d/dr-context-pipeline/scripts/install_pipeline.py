#!/usr/bin/env python3
"""Install/sync the context_pipeline bundle into the workspace."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def collect_files(root: Path):
    for item in sorted(root.rglob("*")):
        if item.is_file():
            yield item


def main() -> int:
    script_path = Path(__file__).resolve()
    skill_root = script_path.parents[1]
    workspace_root = script_path.parents[3]

    default_target = workspace_root / "context_pipeline"
    assets_root = skill_root / "assets" / "context_pipeline"

    parser = argparse.ArgumentParser(description="Install/sync context_pipeline")
    parser.add_argument("--target", default=str(default_target), help="Destination folder (default: workspace/context_pipeline)")
    parser.add_argument("--assets-root", default=str(assets_root), help="Source bundle (default: skill assets)")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    source = Path(args.assets_root).resolve()

    if not source.exists():
        raise SystemExit(f"Source bundle not found: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)

    files = list(collect_files(target))
    summary = []
    for file in files:
        rel = file.relative_to(target)
        summary.append((str(rel), sha256(file)))

    print(f"Installed context pipeline files into {target}")
    print(f"Total files: {len(files)}")
    preview = summary[:5]
    for rel_path, digest in preview:
        print(f" - {rel_path}: {digest}")
    remaining = len(summary) - len(preview)
    if remaining > 0:
        print(f" ... {remaining} more files hashed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
