from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full AI news workflow.")
    parser.add_argument(
        "--time-window",
        type=str,
        default="",
        help="Optional natural-language time window string.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root containing config, data, reports, and state directories.",
    )
    parser.add_argument(
        "--disable-ai",
        action="store_true",
        help="Skip AI generation in both domestic and international report steps.",
    )
    return parser.parse_args()


def run_step(script_name: str, args: list[str], workspace: Path) -> None:
    env = os.environ.copy()
    env["AI_NEWS_WORKSPACE"] = str(workspace)
    command = [sys.executable, str(SCRIPT_DIR / script_name), *args]
    subprocess.run(command, check=True, cwd=workspace, env=env)


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()

    step_args: list[str] = []
    if args.time_window:
        step_args.extend(["--time-window", args.time_window])
    if args.disable_ai:
        step_args.append("--disable-ai")

    print("=== Step 1: Collect RSS feeds ===")
    run_step("collect_feeds.py", [], workspace)

    print("=== Step 2: Build domestic report and refresh Word brief ===")
    run_step("generate_company_report.py", step_args, workspace)

    print("=== Step 3: Build international report and refresh Word brief ===")
    run_step("generate_international_report.py", step_args, workspace)

    print("=== Workflow complete ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())