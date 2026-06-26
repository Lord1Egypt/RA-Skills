#!/usr/bin/env python3
"""
Initialize local settings for AlphaPai skill consumers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_DIR / "config"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize AlphaPai local config")
    parser.add_argument(
        "--output-dir",
        default="~/.openclaw/data/alphapai-scraper",
        help="Base output directory",
    )
    parser.add_argument(
        "--default-hours",
        type=float,
        default=1,
        help="Default lookback window in hours",
    )
    parser.add_argument(
        "--feishu-webhook",
        default="",
        help="Optional Feishu webhook URL",
    )
    parser.add_argument(
        "--custom-requirements",
        default="",
        help="Optional custom summary formatting requirements",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = {
        "auth": {
            "methods": ["storage_state", "token", "cookies", "credentials", "profile"],
            "token_file": "config/token.local.json",
            "cookies_file": "config/cookies.local.json",
            "credentials_file": "config/credentials.local.json",
        },
        "scrape": {
            "default_lookback_hours": args.default_hours,
        },
        "output": {
            "base_dir": args.output_dir,
            "raw_format": "md",
            "report_format": "md",
        },
        "feishu": {
            "enabled": bool(args.feishu_webhook),
            "webhook_url": args.feishu_webhook,
            "title_prefix": "Alpha派摘要",
        },
        "ai": {
            "custom_requirements": args.custom_requirements,
        },
    }

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    settings_path = CONFIG_DIR / "settings.local.json"
    settings_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for example_name, target_name in [
        ("token.example.json", "token.local.json"),
        ("cookies.example.json", "cookies.local.json"),
        ("credentials.example.json", "credentials.local.json"),
    ]:
        example_path = CONFIG_DIR / example_name
        target_path = CONFIG_DIR / target_name
        if example_path.exists() and not target_path.exists():
            target_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")

    print(settings_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
