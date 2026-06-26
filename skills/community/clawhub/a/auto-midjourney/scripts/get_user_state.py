#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_browser import browser_fetch_json
from mj_alpha import enrich_config_from_cookie, get_user_state, load_config, print_json, require_config, save_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch Midjourney Alpha user-mutable-state.")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--transport", choices=["auto", "browser", "http"], default="auto", help="Request transport")
    parser.add_argument("--output", help="Write JSON result to file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = enrich_config_from_cookie(load_config(args.dotenv))
    require_config(config, need_channel_id=False)

    response = None
    if args.transport in {"auto", "browser"}:
        try:
            response = browser_fetch_json(
                config.user_state_url,
                headers={
                    "accept": "*/*",
                    "content-type": "application/json",
                    "x-csrf-protection": config.csrf_protection,
                },
                timeout_seconds=config.timeout_seconds,
            )
        except Exception:
            if args.transport == "browser":
                raise
    if response is None:
        response = get_user_state(config)

    result = {
        "user_state_url": config.user_state_url,
        "response": response,
    }

    if args.output:
        save_json(args.output, result)
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
