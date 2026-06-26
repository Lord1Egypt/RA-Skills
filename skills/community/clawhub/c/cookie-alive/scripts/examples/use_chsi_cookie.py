#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib import request


DEFAULT_URL = "https://account.chsi.com.cn/account/account!show.action"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/146.0.0.0 Safari/537.36"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def cookie_alive_script() -> Path:
    return repo_root() / "scripts" / "cookie_alive.py"


def pull_cookie(db_name: str, profile: str, refresh: bool, output_format: str) -> str:
    command = [
        sys.executable,
        str(cookie_alive_script()),
        "--db-name",
        db_name,
        "pull",
        "--profile",
        profile,
        "--format",
        output_format,
    ]
    if refresh:
        command.append("--refresh")
    return subprocess.check_output(command, text=True, stderr=subprocess.PIPE).strip()


def fetch_page(url: str, cookie_header: str, referer: str, user_agent: str, timeout_seconds: int) -> dict[str, object]:
    http_request = request.Request(
        url,
        headers={
            "Cookie": cookie_header,
            "Referer": referer,
            "User-Agent": user_agent,
        },
        method="GET",
    )
    with request.urlopen(http_request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8", errors="replace")
        return {
            "status_code": response.status,
            "final_url": response.geturl(),
            "content_type": response.headers.get("Content-Type"),
            "body_preview": body[:400],
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Example external client that refreshes a stored CHSI cookie and reuses it in an HTTP request.",
    )
    parser.add_argument("--db-name", default="chsi")
    parser.add_argument("--profile", default="main")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--referer", default="https://www.chsi.com.cn/")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--no-refresh", action="store_true", help="Reuse the stored cookie without refreshing first.")
    parser.add_argument(
        "--cookie-format",
        choices=("header", "json", "record"),
        default="header",
        help="Format returned by cookie_alive pull. Use header for direct HTTP requests.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        cookie_output = pull_cookie(
            db_name=args.db_name,
            profile=args.profile,
            refresh=not args.no_refresh,
            output_format=args.cookie_format,
        )
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        return exc.returncode or 1
    print("cookie_alive output:")
    print(cookie_output)

    if args.cookie_format != "header":
        print("\nHTTP request skipped because --cookie-format is not 'header'.")
        return 0

    response_payload = fetch_page(
        url=args.url,
        cookie_header=cookie_output,
        referer=args.referer,
        user_agent=args.user_agent,
        timeout_seconds=args.timeout_seconds,
    )
    print("\nrequest result:")
    print(json.dumps(response_payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
