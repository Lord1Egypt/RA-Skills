#!/usr/bin/env python3
"""
Optional Feishu webhook sender.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib import request

from common import load_settings


def send_feishu_report(
    report_file: str,
    settings: dict[str, Any],
    lookback_hours: float,
) -> dict[str, Any]:
    feishu_settings = settings["feishu"]
    if not feishu_settings.get("enabled"):
        return {"sent": False, "reason": "feishu.enabled=false"}

    webhook_url = str(feishu_settings.get("webhook_url") or "").strip()
    if not webhook_url:
        return {"sent": False, "reason": "未配置 webhook_url"}

    text = Path(report_file).read_text(encoding="utf-8")
    title_prefix = feishu_settings.get("title_prefix") or "Alpha派摘要"
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"{title_prefix} | 最近 {lookback_hours:g} 小时\n\n{text[:3500]}"
        },
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as resp:
            response_text = resp.read().decode("utf-8", errors="ignore")
        return {"sent": True, "reason": "", "response": response_text}
    except Exception as exc:
        return {"sent": False, "reason": str(exc)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send AlphaPai report to Feishu")
    parser.add_argument("report_file")
    parser.add_argument("--hours", type=float, default=1)
    parser.add_argument("--settings")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = load_settings(args.settings)
    result = send_feishu_report(args.report_file, settings, args.hours)
    if result["sent"]:
        print("sent")
        return 0
    print(result["reason"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
