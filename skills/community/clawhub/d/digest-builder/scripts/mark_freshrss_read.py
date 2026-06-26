#!/usr/bin/env python3
"""Mark processed FreshRSS items as read via Google Reader API."""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def load_config() -> dict[str, Any]:
    config = {
        "base_url": os.getenv("FRESHRSS_BASE_URL", ""),
        "username": os.getenv("FRESHRSS_USERNAME", ""),
        "api_password": os.getenv("FRESHRSS_API_PASSWORD", ""),
    }
    missing = [key for key, value in config.items() if not value]
    if missing:
        raise SystemExit(f"Missing FreshRSS config: {', '.join(missing)}")
    return config


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def client_login(base_url: str, username: str, api_password: str) -> str:
    login_url = f"{normalize_base_url(base_url)}/api/greader.php/accounts/ClientLogin"
    payload = urllib.parse.urlencode({"Email": username, "Passwd": api_password}).encode("utf-8")
    request = urllib.request.Request(login_url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"FreshRSS login failed: HTTP {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"FreshRSS login failed: {exc}") from exc

    for line in content.splitlines():
        if line.startswith("Auth="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("FreshRSS login failed: missing Auth token in response")


def parse_timezone(value: str) -> timezone:
    if value in {"Asia/Shanghai", "UTC+08:00", "+08:00"}:
        return timezone(timedelta(hours=8))
    if value in {"UTC", "+00:00"}:
        return timezone.utc
    raise SystemExit(f"Unsupported timezone value: {value}")


def collect_item_ids(source_json: Path, date_str: str | None, tz: timezone) -> list[str]:
    data = json.loads(source_json.read_text(encoding="utf-8"))
    items = data.get("items", [])
    if not isinstance(items, list):
        raise SystemExit("Source JSON is missing items list")

    selected: list[str] = []
    for item in items:
        item_id = item.get("id")
        if not item_id:
            continue
        if date_str:
            published = item.get("published")
            if not published:
                continue
            dt = datetime.fromtimestamp(int(published), tz=timezone.utc).astimezone(tz)
            if dt.strftime("%Y-%m-%d") != date_str:
                continue
        selected.append(item_id)
    return selected


def batched(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def mark_read_batch(base_url: str, auth_token: str, item_ids: list[str], timeout: int, retries: int) -> None:
    pairs: list[tuple[str, str]] = [("a", "user/-/state/com.google/read"), ("async", "true")]
    for item_id in item_ids:
        pairs.append(("i", item_id))
    payload = urllib.parse.urlencode(pairs).encode("utf-8")
    url = f"{normalize_base_url(base_url)}/api/greader.php/reader/api/0/edit-tag"
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"GoogleLogin auth={auth_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8", errors="replace").strip()
            if body != "OK":
                raise SystemExit(f"FreshRSS mark read failed: unexpected response {body!r}")
            return
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(f"FreshRSS mark read failed: HTTP {exc.code} {body}") from exc
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(attempt, 3))
    raise SystemExit(f"FreshRSS mark read failed after {retries} attempts: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark FreshRSS items as read.")
    parser.add_argument("--source-json", required=True, help="Path to fetched FreshRSS JSON.")
    parser.add_argument("--date", default=None, help="Only mark items from YYYY-MM-DD as read.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="Timezone for --date filtering.")
    parser.add_argument("--batch-size", type=int, default=1, help="Items per edit-tag request.")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=3, help="Retries per batch on transient failures.")
    parser.add_argument("--dry-run", action="store_true", help="Only print selected count.")
    args = parser.parse_args()

    source_json = Path(args.source_json)
    if not source_json.exists():
        raise SystemExit(f"Source JSON not found: {source_json}")

    tz = parse_timezone(args.timezone)
    item_ids = collect_item_ids(source_json, args.date, tz)
    item_ids = list(dict.fromkeys(item_ids))

    print(f"Selected {len(item_ids)} items to mark as read")
    if args.dry_run or not item_ids:
        return 0

    config = load_config()
    auth_token = client_login(config["base_url"], config["username"], config["api_password"])
    for batch in batched(item_ids, args.batch_size):
        mark_read_batch(config["base_url"], auth_token, batch, args.timeout, args.retries)

    print(f"Marked {len(item_ids)} items as read")
    return 0


if __name__ == "__main__":
    sys.exit(main())
