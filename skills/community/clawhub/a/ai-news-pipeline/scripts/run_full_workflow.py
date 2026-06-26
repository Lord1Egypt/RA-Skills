from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


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


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    os.environ["AI_NEWS_WORKSPACE"] = str(workspace)

    import collect_feeds
    import run_report_only

    print("=== Step 1: Collect RSS feeds ===", flush=True)
    capture_code = collect_feeds.main()
    if capture_code:
        return capture_code

    print("=== Step 2: Build reports ===", flush=True)
    original_argv = sys.argv[:]
    try:
        sys.argv = ["run_report_only.py", "--workspace", str(workspace)]
        if args.time_window:
            sys.argv.extend(["--time-window", args.time_window])
        if args.disable_ai:
            sys.argv.append("--disable-ai")
        report_code = run_report_only.main()
        if report_code:
            return report_code
    finally:
        sys.argv = original_argv

    print("=== Workflow complete ===", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
