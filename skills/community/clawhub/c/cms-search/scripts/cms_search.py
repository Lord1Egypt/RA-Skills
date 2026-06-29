#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime

CMS_URL = "https://xg-cwork-web.mediportal.com.cn/filegpt/third/nologin/webSearch"


def cms_search(keyword: str, source: str | None, user_datetime: str | None = None):
    user_key = os.environ.get("CMS_USER_KEY", "").strip()
    if not user_key:
        raise SystemExit("Missing CMS_USER_KEY environment variable.")

    # 组装 keyword：用户输入 + 指定时间（若有）
    if user_datetime:
        keyword = f"{keyword} {user_datetime}"

    payload = {"keyword": keyword}
    if source:
        payload["source"] = source

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        CMS_URL,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "userKey": user_key,
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=300) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"CMS returned non-JSON: {body[:300]}")

    return obj


def to_markdown(obj: dict) -> str:
    result = (obj.get("result") or "").strip()
    source = (obj.get("source") or "").strip()
    lines = []
    if result:
        lines.append(result)
    if source:
        lines.append(f"\n来源: {source}")
    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keyword", required=True, help="搜索关键词")
    ap.add_argument(
        "--source",
        default=None,
        choices=["tavily", "glm", "minimax", "bocha"],
        help="指定搜索渠道（可选）",
    )
    ap.add_argument(
        "--format",
        default="raw",
        choices=["raw", "md"],
        help="输出格式: raw（JSON）| md（Markdown）",
    )
    ap.add_argument(
        "--datetime",
        default=None,
        help="指定搜索时间，格式如 2025-06-18 或 2025-06-18 13:55:00",
    )
    args = ap.parse_args()

    res = cms_search(
        keyword=args.keyword,
        source=args.source,
        user_datetime=args.datetime,
    )

    if args.format == "md":
        sys.stdout.write(to_markdown(res))
        return

    json.dump(res, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
