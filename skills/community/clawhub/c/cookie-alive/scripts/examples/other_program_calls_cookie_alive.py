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


def build_pull_command(
    python_executable: str,
    db_name: str,
    profile: str,
    refresh: bool,
    output_format: str,
) -> list[str]:
    command = [
        python_executable,
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
    return command


def pull_cookie_via_subprocess(
    python_executable: str,
    db_name: str,
    profile: str,
    refresh: bool,
    output_format: str,
) -> str:
    command = build_pull_command(
        python_executable=python_executable,
        db_name=db_name,
        profile=profile,
        refresh=refresh,
        output_format=output_format,
    )
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"cookie_alive failed: {result.returncode}")
    return result.stdout.strip()


def fetch_with_cookie(
    url: str,
    cookie_header: str,
    referer: str,
    user_agent: str,
    timeout_seconds: int,
) -> dict[str, object]:
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
        description="Example external program that calls cookie_alive through subprocess and reuses the returned cookie.",
    )
    parser.add_argument("--python-executable", default=sys.executable)
    parser.add_argument("--db-name", default="chsi")
    parser.add_argument("--profile", default="main")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--referer", default="https://www.chsi.com.cn/")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--no-refresh", action="store_true")
    parser.add_argument("--skip-request", action="store_true", help="Only demonstrate pulling the cookie from cookie_alive.")
    parser.add_argument("--show-command", action="store_true", help="Print the subprocess command before executing it.")
    parser.add_argument(
        "--cookie-format",
        choices=("header", "json", "record"),
        default="header",
        help="Format requested from cookie_alive. Use header for direct HTTP requests.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = build_pull_command(
        python_executable=args.python_executable,
        db_name=args.db_name,
        profile=args.profile,
        refresh=not args.no_refresh,
        output_format=args.cookie_format,
    )

    if args.show_command:
        print("subprocess command:")
        print(" ".join(command))
        print()

    try:
        cookie_output = pull_cookie_via_subprocess(
            python_executable=args.python_executable,
            db_name=args.db_name,
            profile=args.profile,
            refresh=not args.no_refresh,
            output_format=args.cookie_format,
        )
    except RuntimeError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    print("cookie_alive stdout:")
    print(cookie_output)

    if args.skip_request or args.cookie_format != "header":
        return 0

    response_payload = fetch_with_cookie(
        url=args.url,
        cookie_header=cookie_output,
        referer=args.referer,
        user_agent=args.user_agent,
        timeout_seconds=args.timeout_seconds,
    )
    print("\nfollow-up request result:")
    print(json.dumps(response_payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
