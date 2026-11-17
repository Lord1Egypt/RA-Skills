#!/usr/bin/env python3
"""Copy the bundled Feishu invoice approval project into a safe target directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a Feishu invoice approval bot project."
    )
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        help="New or empty destination directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    template_dir = skill_dir / "assets" / "template"
    target = args.target.expanduser().resolve()

    if not template_dir.is_dir():
        print(f"Template directory is missing: {template_dir}", file=sys.stderr)
        return 2
    if target == template_dir or template_dir in target.parents:
        print("Target cannot be the bundled template or a directory inside it.", file=sys.stderr)
        return 2
    if target.exists() and not target.is_dir():
        print(f"Target exists and is not a directory: {target}", file=sys.stderr)
        return 2
    if target.exists() and any(target.iterdir()):
        print(f"Target must be new or empty: {target}", file=sys.stderr)
        return 2

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_dir, target, dirs_exist_ok=True)
    (target / "config" / "scaffold-env.txt").replace(target / ".env.example")
    (target / "config" / "scaffold-gitignore.txt").replace(target / ".gitignore")
    for script in (target / "scripts").glob("*.sh"):
        script.chmod(script.stat().st_mode | 0o111)

    print(f"Created Feishu invoice approval bot project at {target}")
    print("Next:")
    print(f"  1. cp {target / '.env.example'} {target / '.env'}")
    print(
        "  2. cp "
        f"{target / 'config' / 'approval_mapping.example.json'} "
        f"{target / 'config' / 'approval_mapping.json'}"
    )
    print(f"  3. Configure the files, then run {target / 'scripts' / 'setup-lark.sh'}")
    print(
        f"  4. cd {target} && "
        "PYTHONPATH=src python3 -m invoice_approval_bot.cli validate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
