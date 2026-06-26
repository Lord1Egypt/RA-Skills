#!/usr/bin/env python3
"""Copy the DR Memory Foundation templates into the current workspace."""

from __future__ import annotations

import argparse
import shutil
import textwrap
from datetime import datetime, timezone
from pathlib import Path


def copy_templates(workspace: Path, templates: Path) -> list[str]:
    actions = []
    for src in sorted(templates.rglob("*")):
        rel = src.relative_to(templates)
        dest = workspace / rel
        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue
        if dest.exists():
            actions.append(f"SKIP {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            actions.append(f"ADD  {dest}")
    return actions


def ensure_daily_log(workspace: Path) -> str | None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = workspace / "memory" / f"{today}.md"
    if daily.exists():
        return None
    daily.parent.mkdir(parents=True, exist_ok=True)
    stub = textwrap.dedent(
        f"""# {today} — Daily log (auto-generated)

- Initialized dr-memory-foundation on {today} (UTC).
- This stub exists so watchdogs see a >200-byte file immediately.
- Replace it with real notes as soon as you start working in this workspace.
"""
    )
    daily.write_text(stub)
    return f"ADD  {daily}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install DR Memory Foundation templates into the current workspace")
    parser.add_argument("--workspace", default=".", help="Workspace root (default: current directory)")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "references" / "templates"

    if not templates.exists():
        raise SystemExit(f"Template folder not found: {templates}")

    actions = copy_templates(workspace, templates)
    daily_action = ensure_daily_log(workspace)
    if daily_action:
        actions.append(daily_action)

    print(f"Workspace: {workspace}")
    print(f"Templates: {templates}")
    if actions:
        print("\nChanges:")
        for line in actions:
            print(f"  {line}")
    else:
        print("\nTemplates already in place; nothing to do.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
