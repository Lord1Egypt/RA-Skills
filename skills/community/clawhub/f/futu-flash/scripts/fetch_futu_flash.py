#!/home/loveni/apps/anaconda3/bin/python
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import json
import sys

import requests

API = "https://news.futunn.com/news-site-api/main/get-flash-list"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fetch latest Futu flash news")
    p.add_argument("--limit", type=int, default=10, help="max items to fetch (1-10)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    limit = max(1, min(args.limit, 10))

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://news.futunn.com/main/live",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    try:
        r = requests.get(API, params={"pageSize": limit}, headers=headers, timeout=20)
    except Exception as exc:
        print(json.dumps({"status": "error", "message": f"request_failed: {exc}"}, ensure_ascii=False))
        sys.exit(1)

    if r.status_code != 200:
        print(json.dumps({"status": "error", "message": f"http_status={r.status_code}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        payload = r.json()
    except Exception:
        print(json.dumps({"status": "error", "message": "invalid_json"}, ensure_ascii=False))
        sys.exit(1)

    if payload.get("code") != 0:
        print(json.dumps({"status": "error", "message": f"api_code={payload.get('code')}", "raw": payload}, ensure_ascii=False))
        sys.exit(1)

    news = ((payload.get("data") or {}).get("data") or {}).get("news") or []
    out = []
    tz = dt.timezone(dt.timedelta(hours=8))

    for item in news[:limit]:
        ts = int(item.get("time") or 0)
        t = dt.datetime.fromtimestamp(ts, dt.timezone.utc).astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        text = (item.get("title") or item.get("content") or "").replace("\n", " ").strip()
        out.append(
            {
                "id": item.get("id"),
                "time_bj": t,
                "text": text,
                "detail_url": item.get("detailUrl"),
            }
        )

    print(json.dumps({"status": "ok", "count": len(out), "results": out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
