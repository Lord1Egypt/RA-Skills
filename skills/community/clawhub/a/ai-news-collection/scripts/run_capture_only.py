from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run capture only for the AI news pipeline.")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root containing config, data, reports, and state directories.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()

    env = os.environ.copy()
    env["AI_NEWS_WORKSPACE"] = str(workspace)
    command = [sys.executable, str(SCRIPT_DIR / "collect_feeds.py")]
    subprocess.run(command, check=True, cwd=workspace, env=env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
