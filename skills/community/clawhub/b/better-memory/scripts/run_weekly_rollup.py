#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from refine_memory import run_weekly_rollup


def main() -> int:
    parser = argparse.ArgumentParser(description="Run weekly L2 -> L3 memory rollup.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    result = run_weekly_rollup(workspace)

    print(f"Workspace: {workspace}")
    print(f"MEMORY file: {result['memory_file']}")
    print(
        "Weekly topics: "
        f"experience={result['topics_experience']}, value={result['topics_value']}, standard={result['topics_standard']}"
    )
    print(f"Conflicts: {result['conflicts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
