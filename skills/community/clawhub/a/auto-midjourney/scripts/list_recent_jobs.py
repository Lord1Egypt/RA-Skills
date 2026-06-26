#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlencode

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_browser import browser_fetch_json
from mj_alpha import (
    enrich_config_from_cookie,
    load_config,
    print_json,
    request_recent_jobs,
    require_config,
    save_json,
    summarize_job_images,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List recent Midjourney jobs using the experimental recent-jobs endpoint.")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--transport", choices=["auto", "browser", "http"], default="auto", help="Request transport")
    parser.add_argument("--user-id", help="Override MJ_USER_ID")
    parser.add_argument("--page", type=int, default=1, help="Recent jobs page number")
    parser.add_argument("--amount", type=int, default=25, help="Jobs per page")
    parser.add_argument("--order-by", default="new", help="Order parameter")
    parser.add_argument("--job-status", help="Optional jobStatus filter")
    parser.add_argument("--job-type", help="Optional jobType filter")
    parser.add_argument("--output", help="Write JSON result to file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = enrich_config_from_cookie(load_config(args.dotenv))
    if args.user_id:
        config.user_id = args.user_id
    require_config(config, need_channel_id=False)

    response = None
    resolved_user_id = args.user_id or config.user_id
    if args.transport in {"auto", "browser"}:
        try:
            params = {
                "userId": resolved_user_id,
                "page": str(args.page),
                "amount": str(args.amount),
                "orderBy": args.order_by,
                "dedupe": "true",
                "refreshApi": "0",
            }
            params["jobStatus"] = args.job_status or "completed"
            if args.job_type:
                params["jobType"] = args.job_type
            url = f"{config.recent_jobs_url}?{urlencode(params)}"
            response = browser_fetch_json(
                url,
                page_url="https://www.midjourney.com/",
                headers={"accept": "*/*", "content-type": "application/json"},
                timeout_seconds=config.timeout_seconds,
            )
        except Exception:
            if args.transport == "browser":
                raise
    if response is None:
        response = request_recent_jobs(
            config,
            user_id=args.user_id,
            page=args.page,
            amount=args.amount,
            order_by=args.order_by,
            job_status=args.job_status,
            job_type=args.job_type,
        )
    jobs = response if isinstance(response, list) else []
    result = {
        "recent_jobs_url": config.recent_jobs_url,
        "user_id": config.user_id,
        "count": len(jobs),
        "summary": [summarize_job_images(job) for job in jobs if isinstance(job, dict)],
        "response": response,
    }

    if args.output:
        save_json(args.output, result)
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
