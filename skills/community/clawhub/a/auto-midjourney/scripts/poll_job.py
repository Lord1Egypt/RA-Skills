#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_alpha import enrich_config_from_cookie, load_config, poll_job, print_json, require_config, save_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Poll one Midjourney Alpha job.")
    parser.add_argument("job_id", help="Midjourney job UUID")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--attempts", type=int, default=60, help="Max poll attempts")
    parser.add_argument("--interval", type=float, help="Override MJ_POLL_INTERVAL_SECONDS")
    parser.add_argument("--once", action="store_true", help="Fetch only one status response")
    parser.add_argument("--output", help="Write JSON result to file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = enrich_config_from_cookie(load_config(args.dotenv))
    require_config(config, need_status=True, need_channel_id=False)

    result = poll_job(
        config,
        args.job_id,
        attempts=args.attempts,
        interval_seconds=args.interval,
        once=args.once,
    )

    if args.output:
        save_json(args.output, result)
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
