#!/usr/bin/env python3
"""Fetch unread items from FreshRSS Google Reader API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def load_config(config_path: str | None) -> dict[str, Any]:
    config: dict[str, Any] = {}
    if config_path:
        with open(config_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)

    env_map = {
        "base_url": "FRESHRSS_BASE_URL",
        "username": "FRESHRSS_USERNAME",
        "api_password": "FRESHRSS_API_PASSWORD",
        "output_json": "FRESHRSS_OUTPUT_JSON",
        "output_md": "FRESHRSS_OUTPUT_MD",
        "limit": "FRESHRSS_LIMIT",
        "page_size": "FRESHRSS_PAGE_SIZE",
        "include_read": "FRESHRSS_INCLUDE_READ",
    }

    for key, env_name in env_map.items():
        value = os.getenv(env_name)
        if value not in (None, ""):
            config[key] = value

    if "limit" in config:
        config["limit"] = int(config["limit"])
    if "page_size" in config:
        config["page_size"] = int(config["page_size"])
    if "include_read" in config:
        include_read = config["include_read"]
        if not isinstance(include_read, bool):
            config["include_read"] = str(include_read).lower() in {"1", "true", "yes", "on"}

    required = ["base_url", "username", "api_password"]
    missing = [key for key in required if not config.get(key)]
    if missing:
        missing_text = ", ".join(missing)
        raise SystemExit(f"Missing FreshRSS config: {missing_text}")

    config.setdefault("output_json", "digests/raw-freshrss.json")
    config.setdefault("output_md", "digests/raw-freshrss.md")
    config.setdefault("limit", 0)
    config.setdefault("page_size", 1000)
    config.setdefault("include_read", False)

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


def fetch_stream_page(
    base_url: str,
    auth_token: str,
    include_read: bool,
    page_size: int,
    continuation: str | None,
) -> dict[str, Any]:
    params = {"output": "json", "n": str(page_size)}
    if not include_read:
        params["xt"] = "user/-/state/com.google/read"
    if continuation:
        params["c"] = continuation

    query = urllib.parse.urlencode(params)
    stream_url = (
        f"{normalize_base_url(base_url)}/api/greader.php/reader/api/0/stream/contents/"
        f"reading-list?{query}"
    )

    request = urllib.request.Request(
        stream_url,
        headers={"Authorization": f"GoogleLogin auth={auth_token}"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"FreshRSS unread fetch failed: HTTP {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"FreshRSS unread fetch failed: {exc}") from exc


def fetch_unread_items(
    base_url: str,
    auth_token: str,
    include_read: bool,
    page_size: int,
    limit: int,
) -> dict[str, Any]:
    all_items: list[dict[str, Any]] = []
    continuation: str | None = None
    first_payload: dict[str, Any] | None = None

    while True:
        payload = fetch_stream_page(base_url, auth_token, include_read, page_size, continuation)
        if first_payload is None:
            first_payload = payload

        items = payload.get("items", [])
        if not isinstance(items, list):
            raise SystemExit("FreshRSS unread fetch failed: response missing items list")

        all_items.extend(items)
        if limit > 0 and len(all_items) >= limit:
            all_items = all_items[:limit]
            break

        continuation = payload.get("continuation")
        if not continuation or not items:
            break

    if first_payload is None:
        first_payload = {"items": []}

    first_payload["items"] = all_items
    if continuation:
        first_payload["continuation"] = continuation
    return first_payload


def build_markdown(items: list[dict[str, Any]], source_url: str) -> str:
    lines = [
        "# FreshRSS 未读列表",
        "",
        f"- 来源：`{source_url}`",
        f"- 条目数：`{len(items)}`",
        "",
    ]

    if not items:
        lines.append("当前没有未读条目。")
        return "\n".join(lines) + "\n"

    for index, item in enumerate(items, start=1):
        canonical = item.get("canonical", [])
        link = ""
        if canonical and isinstance(canonical, list):
            first = canonical[0]
            if isinstance(first, dict):
                link = first.get("href", "")

        title = item.get("title") or "(无标题)"
        origin = item.get("origin", {}) or {}
        origin_title = origin.get("title") or origin.get("streamId") or "未知来源"
        published = item.get("published") or ""
        summary = ""
        raw_summary = item.get("summary", {}) or {}
        if isinstance(raw_summary, dict):
            summary = raw_summary.get("content", "") or ""
        summary = " ".join(summary.split())
        if len(summary) > 280:
            summary = summary[:277] + "..."

        lines.extend(
            [
                f"## {index}. {title}",
                "",
                f"- 来源：{origin_title}",
                f"- 发布时间：{published}",
                f"- 链接：{link}",
                f"- 条目 ID：{item.get('id', '')}",
                "",
            ]
        )
        if summary:
            lines.append(summary)
            lines.append("")

    return "\n".join(lines)


def ensure_parent(path_str: str) -> Path:
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch unread FreshRSS items.")
    parser.add_argument("--config", help="Path to JSON config file.", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    auth_token = client_login(config["base_url"], config["username"], config["api_password"])
    payload = fetch_unread_items(
        config["base_url"],
        auth_token,
        bool(config["include_read"]),
        int(config["page_size"]),
        int(config["limit"]),
    )

    items = payload.get("items", [])
    if not isinstance(items, list):
        raise SystemExit("FreshRSS unread fetch failed: response missing items list")

    output_json = ensure_parent(config["output_json"])
    output_md = ensure_parent(config["output_md"])

    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(
        build_markdown(items, f"{normalize_base_url(config['base_url'])}/api/greader.php"),
        encoding="utf-8",
    )

    print(f"Fetched {len(items)} FreshRSS items")
    print(f"JSON written to: {output_json}")
    print(f"Markdown written to: {output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
