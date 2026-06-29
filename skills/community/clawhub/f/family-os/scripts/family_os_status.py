#!/usr/bin/env python3
"""Print a compact status view for a Family OS workspace."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


DASHBOARD_FILES = [
    "01-dashboard/household-overview.md",
    "01-dashboard/current-priorities.md",
    "01-dashboard/this-month.md",
    "01-dashboard/risks-and-reminders.md",
]


def preview(path: Path, max_lines: int) -> list[str]:
    if not path.exists():
        return ["[missing]"]
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[:max_lines]


def count_children(path: Path) -> int:
    if not path.exists():
        return 0
    return len([p for p in path.iterdir() if not p.name.startswith(".")])


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Family OS workspace status.")
    parser.add_argument("--workspace", default=os.environ.get("FAMILY_OS_HOME", str(Path.home() / "family-os-workspace")))
    parser.add_argument("--lines", type=int, default=20)
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    print(f"# Family OS Status")
    print(f"workspace: {workspace}")
    print(f"inbox_items: {count_children(workspace / '00-inbox')}")
    print(f"projects: {count_children(workspace / '03-projects')}")
    print(f"decisions: {count_children(workspace / '04-decisions')}")
    print()

    for rel in DASHBOARD_FILES:
        print(f"## {rel}")
        for line in preview(workspace / rel, args.lines):
            print(line)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
