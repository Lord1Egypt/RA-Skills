#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import platform
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_browser import browser_fetch_json
from mj_alpha import (
    enrich_config_from_cookie,
    extract_auth_claims_from_cookie,
    get_user_state,
    load_config,
    load_usage_log,
    print_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate local Midjourney Alpha config and summarize safe defaults.")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--fetch-user-state", action="store_true", help="Also call /api/user-mutable-state")
    parser.add_argument("--transport", choices=["auto", "browser", "http"], default="auto", help="Request transport")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = enrich_config_from_cookie(load_config(args.dotenv))
    claims = extract_auth_claims_from_cookie(config.cookie)
    usage_log = load_usage_log(config)

    result = {
        "config": {
            "has_cookie": bool(config.cookie),
            "channel_id": config.channel_id,
            "user_id": config.user_id,
            "submit_url": config.submit_url,
            "user_state_url": config.user_state_url,
            "recent_jobs_url": config.recent_jobs_url,
            "mode": config.mode,
            "private": config.private,
            "min_submit_interval_seconds": config.min_submit_interval_seconds,
            "max_submits_per_hour": config.max_submits_per_hour,
            "max_submits_per_day": config.max_submits_per_day,
        },
        "runtime": {
            "platform": platform.system(),
            "chrome_app": os.getenv("MJ_CHROME_APP", ""),
            "cdp_port": os.getenv("MJ_CDP_PORT", "9222"),
            "cdp_profile_dir": os.getenv("MJ_CDP_PROFILE_DIR", ".chrome-cdp-profile"),
        },
        "cookie_claims_preview": {
            "midjourney_id": claims.get("midjourney_id") if claims else None,
            "email": claims.get("email") if claims else None,
            "name": claims.get("name") if claims else None,
        },
        "recent_submit_count": len(usage_log),
    }

    if args.fetch_user_state and config.cookie:
        try:
            if args.transport in {"auto", "browser"}:
                try:
                    result["user_state"] = browser_fetch_json(
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
                    result["user_state"] = get_user_state(config)
            else:
                result["user_state"] = get_user_state(config)
        except Exception as exc:
            result["user_state_error"] = str(exc)

    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
