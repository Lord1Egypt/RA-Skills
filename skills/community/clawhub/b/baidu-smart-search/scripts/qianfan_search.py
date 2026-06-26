#!/usr/bin/env python3
import argparse
import json
import os
import sys
from urllib import request, error

DEFAULT_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"


def build_payload(args):
    payload = {
        "messages": [{"content": args.query, "role": "user"}],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [
            {"type": "web", "top_k": args.web_top_k},
            {"type": "video", "top_k": args.video_top_k},
            {"type": "image", "top_k": args.image_top_k},
            {"type": "aladdin", "top_k": args.aladdin_top_k},
        ],
    }
    if args.site:
        payload["search_filter"] = {"match": {"site": args.site}}
    if args.recency:
        payload["search_recency_filter"] = args.recency
    return payload


def main():
    p = argparse.ArgumentParser(description="Call Baidu Qianfan web search API")
    p.add_argument("query", help="search query, ideally within 72 chars")
    p.add_argument("--api-key", help="AppBuilder API key; defaults to QIANFAN_APPBUILDER_API_KEY")
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--web-top-k", type=int, default=10)
    p.add_argument("--video-top-k", type=int, default=0)
    p.add_argument("--image-top-k", type=int, default=0)
    p.add_argument("--aladdin-top-k", type=int, default=0)
    p.add_argument("--site", action="append", default=[])
    p.add_argument("--recency", choices=["week", "month", "semiyear", "year"])
    p.add_argument("--raw", action="store_true", help="print full raw JSON")
    args = p.parse_args()

    api_key = args.api_key or os.environ.get("QIANFAN_APPBUILDER_API_KEY")
    if not api_key:
        print("Missing API key: pass --api-key or set QIANFAN_APPBUILDER_API_KEY", file=sys.stderr)
        sys.exit(2)

    payload = build_payload(args)
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        args.url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Appbuilder-Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    obj = json.loads(body)
    if args.raw:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
        return

    # Best-effort result extraction from documented response patterns
    items = []
    candidates = []
    if isinstance(obj, dict):
        for key in ("data", "result", "results", "search_results"):
            val = obj.get(key)
            if isinstance(val, list):
                candidates.extend(val)
        if not candidates:
            for v in obj.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    candidates.extend(v)

    for item in candidates:
        title = item.get("title") or item.get("web_anchor") or ""
        url = item.get("url") or ""
        content = item.get("content") or item.get("summary") or ""
        date = item.get("date") or item.get("page_time") or ""
        if title or url or content:
            items.append({"title": title, "url": url, "content": content, "date": date})

    print(json.dumps({
        "query": args.query,
        "count": len(items),
        "items": items[: max(args.web_top_k, 1)],
        "raw_keys": list(obj.keys()) if isinstance(obj, dict) else [],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
