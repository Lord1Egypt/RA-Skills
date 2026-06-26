#!/usr/bin/env python3
"""Placeholder content producer for the brand marketing skill."""
from __future__ import annotations
import json
import sys


def main() -> int:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    brand = payload.get("brand_name", "Brand")
    print(json.dumps({
        "topics": [f"{brand} origin story", f"{brand} use case story"],
        "titles": [f"{brand}: a simple introduction"],
        "posts": ["Draft post placeholder"],
        "scripts": ["Draft short-form script placeholder"],
        "comment_replies": ["Reply template placeholder"],
        "platform_variants": ["xiaohongshu", "weibo", "douyin"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
