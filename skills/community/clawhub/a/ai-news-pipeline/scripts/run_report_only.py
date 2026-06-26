from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def default_report_window() -> str:
    now = datetime.now()
    yesterday = (now.date() - timedelta(days=1)).isoformat()
    today = now.date().isoformat()
    return f"{yesterday} 00:00 to {today} 08:00"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run report generation only for the AI news pipeline.")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root containing config, data, reports, and state directories.",
    )
    parser.add_argument(
        "--time-window",
        type=str,
        default="",
        help="Optional natural-language time window string. Defaults to yesterday 00:00 to today 08:00.",
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
    time_window = args.time_window.strip() or default_report_window()

    print(f"=== Report window: {time_window} ===", flush=True)

    import generate_company_report
    import generate_international_report

    original_argv = sys.argv[:]
    try:
        print("=== Step 1: Build China report and merge Word brief ===", flush=True)
        sys.argv = ["generate_company_report.py", "--time-window", time_window]
        if args.disable_ai:
            sys.argv.append("--disable-ai")
        china_code = generate_company_report.main()
        if china_code:
            return china_code

        print("=== Step 2: Build international report and refresh Word brief ===", flush=True)
        sys.argv = ["generate_international_report.py", "--time-window", time_window]
        if args.disable_ai:
            sys.argv.append("--disable-ai")
        return generate_international_report.main()
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    raise SystemExit(main())
