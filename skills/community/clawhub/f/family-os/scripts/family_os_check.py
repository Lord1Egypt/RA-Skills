#!/usr/bin/env python3
"""Check basic Family OS workspace health."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


REQUIRED_PATHS = [
    "00-inbox",
    "01-dashboard/household-overview.md",
    "01-dashboard/current-priorities.md",
    "01-dashboard/this-month.md",
    "01-dashboard/risks-and-reminders.md",
    "02-areas",
    "03-projects",
    "04-decisions",
    "05-memory/household-facts.md",
    "05-memory/family-values.md",
    "05-memory/preferences.md",
    "05-memory/important-people.md",
    "90-reviews/weekly",
    "90-reviews/monthly",
    "90-reviews/yearly",
    "99-archive",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Family OS workspace.")
    parser.add_argument("--workspace", default=os.environ.get("FAMILY_OS_HOME", str(Path.home() / "family-os-workspace")))
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    missing = [rel for rel in REQUIRED_PATHS if not (workspace / rel).exists()]

    inbox = workspace / "00-inbox"
    inbox_items = []
    if inbox.exists():
        inbox_items = [p.name for p in inbox.iterdir() if not p.name.startswith(".")]

    print(f"workspace: {workspace}")
    print(f"missing: {len(missing)}")
    for rel in missing:
        print(f"  - {rel}")
    print(f"inbox_items: {len(inbox_items)}")
    for name in inbox_items[:20]:
        print(f"  - {name}")
    if len(inbox_items) > 20:
        print(f"  ... {len(inbox_items) - 20} more")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
