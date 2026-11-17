#!/usr/bin/env python3
"""Search Douyin by topic, then read the videos you pick (LinkDigest API).

    python3 douyin_search.py "露营装备"                 # list the videos (free)
    python3 douyin_search.py "露营装备" --read 2        # also read the first 2
    python3 douyin_search.py "camping gear" --limit 8 --format json

Standard library only. Reads LINKDIGEST_API_KEY; talks only to linkdigest.dev.
The reads go through the bundled linkdigest.py (202 queue + polling handled).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkdigest as ld  # noqa: E402

SEARCH = "https://linkdigest.dev/api/v1/search"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="抖音按话题搜视频，再读成逐字稿 / Search Douyin, then read the videos")
    p.add_argument("query", help="话题，中文或英文，如 露营装备、AI 编程、camping gear")
    p.add_argument("--limit", type=int, default=5, help="最多返回几条（1–10，默认 5）")
    p.add_argument("--read", type=int, default=0, help="接着读前 N 条（按条计费，1 分钟视频 2 积分）")
    p.add_argument("--max-credits", type=int, help="每条最多花多少积分，超过的不读、不扣费")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = p.parse_args(argv)

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key:
        ld.log(f"搜索需要 LINKDIGEST_API_KEY：在 {ld.KEYS_URL} 创建（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return ld.EXIT_USAGE
    if not 1 <= args.limit <= 10 or args.read < 0:
        ld.log("--limit 是 1 到 10；--read 不能是负数")
        return ld.EXIT_USAGE

    try:
        status, headers, payload = ld.call(
            "POST", SEARCH, key, {"query": args.query, "platform": "douyin", "limit": args.limit}, timeout=120
        )
    except (urllib.error.URLError, OSError) as err:
        ld.log(f"连不上 linkdigest.dev: {err}{ld.net_hint(err)}")
        return ld.EXIT_ERROR
    if status == 401:
        ld.log(f"Key 无效（401）。在 {ld.KEYS_URL} 重新创建。")
        return ld.EXIT_AUTH
    if status == 429:
        ld.log(f"搜索太频繁或今天的免费搜索额度用完了（429）：{ld.field(payload, 'error', '')}")
        return ld.EXIT_RATE_LIMITED
    if status != 200:
        ld.log(f"搜索失败（HTTP {status}）：{ld.field(payload, 'error', payload)}")
        return ld.EXIT_ERROR

    results = ld.field(payload, "results", []) or []
    if args.format == "json" and not args.read:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"## 抖音搜索：{args.query}（{len(results)} 条，搜索 0 积分）\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.get('title') or '(无标题)'}\n   {r.get('url')}")
    if not results:
        ld.log("没有找到网页已收录的抖音视频。换一个更具体的中文说法试试。")
        return ld.EXIT_OK

    code = ld.EXIT_OK
    for i, r in enumerate(results[: args.read], 1):
        print(f"\n---\n\n# {i}. {r.get('title') or r.get('url')}\n", flush=True)
        extra = ["--format", args.format] + (["--max-credits", str(args.max_credits)] if args.max_credits else [])
        code = ld.main([r["url"], *extra])
        if code == ld.EXIT_PAYMENT:
            ld.log("积分不够，后面的不读了。付款链接在上面；买完重跑同一条命令，读过的走缓存不再扣费。")
            return code
    return code


if __name__ == "__main__":
    sys.exit(main())
