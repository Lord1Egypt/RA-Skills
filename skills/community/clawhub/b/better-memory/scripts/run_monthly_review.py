#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from refine_memory import run_monthly_review


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate monthly conflict/bloat review report.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    result = run_monthly_review(workspace)

    print(f"Workspace: {workspace}")
    print(f"Report file: {result['report_file']}")
    print(f"Plan file: {result['plan_file']}")
    print(f"Plan actions: {result['plan_actions']}")
    print(f"Conflicts: {result['conflicts']}")
    print(f"Bloat topics: {result['bloat_topics']}")
    print(f"Redundant groups: {result['redundant_groups']}")
    print(f"Stale or superseded candidates: {result['stale_or_superseded']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
