#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_alpha import enrich_config_from_cookie, load_config, print_json, require_config, save_json, submit_imagine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit one Midjourney Alpha imagine job.")
    parser.add_argument("prompt", help="Full prompt to submit")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--channel-id", help="Override MJ_CHANNEL_ID")
    parser.add_argument("--mode", help="Override MJ_MODE, for example fast")
    parser.add_argument("--private", action="store_true", help="Submit as private/stealth")
    parser.add_argument("--public", action="store_true", help="Submit as public")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without submitting")
    parser.add_argument("--output", help="Write JSON result to file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.private and args.public:
        parser.error("Choose either --private or --public, not both")

    private = None
    if args.private:
        private = True
    elif args.public:
        private = False

    config = enrich_config_from_cookie(load_config(args.dotenv))
    if args.channel_id:
        config.channel_id = args.channel_id
    require_config(config, need_cookie=not args.dry_run)

    result = submit_imagine(
        config,
        args.prompt,
        mode=args.mode,
        private=private,
        channel_id=args.channel_id,
        dry_run=args.dry_run,
    )

    if args.output:
        save_json(args.output, result)
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
