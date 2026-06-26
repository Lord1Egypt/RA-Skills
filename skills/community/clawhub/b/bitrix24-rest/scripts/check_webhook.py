#!/usr/bin/env python3
"""Check Bitrix24 webhook availability from saved config or explicit URL."""

from __future__ import annotations

import argparse
import json
import socket
import sys
from pathlib import Path
from typing import Any
from urllib import error, request

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bitrix24_config import load_url, mask_url, normalize_url, validate_url  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a Bitrix24 webhook URL.")
    parser.add_argument("--skip-http", action="store_true", help="Skip user.current probe")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds")
    return parser.parse_args()


def resolve_dns(host: str) -> tuple[bool, list[str], str | None]:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        return False, [], str(exc)

    ips = sorted({info[4][0] for info in infos if info[4]})
    return True, ips, None


def probe_user_current(url: str, timeout: float) -> tuple[bool, int | None, dict[str, Any] | None, str | None]:
    target = url + "user.current.json"
    req = request.Request(target, headers={"Accept": "application/json"})
    try:
        with request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            payload = response.read().decode("utf-8", errors="replace")
    except error.HTTPError as exc:
        try:
            payload = exc.read().decode("utf-8", errors="replace")
        except Exception:
            payload = ""
        return False, exc.code, safe_json(payload), f"HTTP {exc.code}"
    except Exception as exc:
        return False, None, None, str(exc)

    data = safe_json(payload)
    if isinstance(data, dict) and data.get("error"):
        return False, status, data, str(data.get("error_description") or data["error"])
    return True, status, data, None


def safe_json(payload: str) -> dict[str, Any] | None:
    if not payload:
        return None
    try:
        value = json.loads(payload)
    except Exception:
        return None
    return value if isinstance(value, dict) else {"raw": value}


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    raw_url, source = load_url()
    result: dict[str, Any] = {
        "source": source,
        "url_found": raw_url is not None,
        "format_ok": False,
        "dns_ok": False,
        "http_ok": None if args.skip_http else False,
    }

    if not raw_url:
        result["error"] = "BITRIX24_WEBHOOK_URL env var is not set"
        return result

    normalized = normalize_url(raw_url)
    result["masked_url"] = mask_url(normalized)

    try:
        validate_url(normalized)
    except ValueError:
        result["error"] = "Webhook format is invalid"
        return result

    parts = normalized.split("/")
    host = parts[2]
    user_id = parts[4]
    result["format_ok"] = True
    result["host"] = host
    result["user_id"] = user_id

    dns_ok, ips, dns_error = resolve_dns(host)
    result["dns_ok"] = dns_ok
    result["dns_ips"] = ips
    if dns_error:
        result["dns_error"] = dns_error
        return result

    if args.skip_http:
        return result

    http_ok, status, payload, http_error = probe_user_current(normalized, args.timeout)
    result["http_ok"] = http_ok
    result["http_status"] = status
    if payload is not None:
        result["http_payload"] = payload
    if http_error:
        result["http_error"] = http_error
    return result


def print_plain(result: dict[str, Any]) -> None:
    for key in [
        "source",
        "url_found",
        "format_ok",
        "host",
        "user_id",
        "dns_ok",
        "dns_ips",
        "dns_error",
        "http_ok",
        "http_status",
        "http_error",
        "error",
    ]:
        if key in result:
            print(f"{key}: {result[key]}")
    if "http_payload" in result:
        print("http_payload:")
        print(json.dumps(result["http_payload"], ensure_ascii=True, indent=2))


def main() -> int:
    args = parse_args()
    result = build_result(args)

    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print_plain(result)

    if not result.get("url_found"):
        return 1
    if not result.get("format_ok"):
        return 1
    if not result.get("dns_ok"):
        return 1
    if result.get("http_ok") is False:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
