"""ScrapeBadger：获取公众人物在 X（Twitter）平台的内容。

子命令：
    profile <username>          获取用户资料（粉丝数、简介、认证等）
    tweets  <username>          获取用户时间线最新推文（支持翻页）
    search  "<query>"           高级搜索推文（支持 from:user since: min_faves: 等算子）

用法示例：
    python scripts/scrapebadger.py profile elonmusk
    python scripts/scrapebadger.py tweets elonmusk --pages 3 --out musk_tweets.json
    python scripts/scrapebadger.py search "from:sama lang:en" --type Latest --pages 2

环境变量：SCRAPEBADGER_API_KEY
文档：https://docs.scrapebadger.com/api-reference/introduction
"""
from __future__ import annotations

import argparse
import sys

from common import add_common_args, emit, request_json, require_key

BASE = "https://scrapebadger.com"
SIGNUP_URL = "https://scrapebadger.com/dashboard"


def headers(api_key: str) -> dict[str, str]:
    return {"x-api-key": api_key, "Content-Type": "application/json"}


def fetch_profile(api_key: str, username: str) -> dict:
    url = f"{BASE}/v1/twitter/users/{username}/by_username"
    return request_json("GET", url, headers=headers(api_key))


def paginate(api_key: str, url: str, base_params: dict, pages: int) -> dict:
    """按 next_cursor 翻页，合并 data 列表。"""
    all_items: list = []
    cursor = None
    last: dict = {}
    for _ in range(max(1, pages)):
        params = dict(base_params)
        if cursor:
            params["cursor"] = cursor
        last = request_json("GET", url, headers=headers(api_key), params=params)
        items = last.get("data") or []
        all_items.extend(items)
        cursor = last.get("next_cursor")
        if not cursor or not items:
            break
    return {"data": all_items, "count": len(all_items), "last_cursor": cursor}


def main() -> None:
    parser = argparse.ArgumentParser(description="ScrapeBadger X/Twitter 抓取")
    sub = parser.add_subparsers(dest="command", required=True)

    p_profile = sub.add_parser("profile", help="获取用户资料")
    p_profile.add_argument("username", help="X 用户名（不含 @）")
    add_common_args(p_profile)

    p_tweets = sub.add_parser("tweets", help="获取用户最新推文")
    p_tweets.add_argument("username", help="X 用户名（不含 @）")
    p_tweets.add_argument("--pages", type=int, default=2, help="翻页数（默认 2）")
    add_common_args(p_tweets)

    p_search = sub.add_parser("search", help="高级搜索推文")
    p_search.add_argument("query", help="搜索语句，支持 Twitter 高级算子")
    p_search.add_argument(
        "--type",
        dest="query_type",
        choices=["Top", "Latest", "Media"],
        default="Top",
    )
    p_search.add_argument("--count", type=int, default=20, help="每页条数（1-100）")
    p_search.add_argument("--pages", type=int, default=2, help="翻页数（默认 2）")
    add_common_args(p_search)

    args = parser.parse_args()
    api_key = require_key("SCRAPEBADGER_API_KEY", "ScrapeBadger", SIGNUP_URL)

    if args.command == "profile":
        data = fetch_profile(api_key, args.username)
        emit(data, args.out)
        return

    if args.command == "tweets":
        url = f"{BASE}/v1/twitter/users/{args.username}/latest_tweets"
        data = paginate(api_key, url, {}, args.pages)
        sys.stderr.write(f"[ScrapeBadger] @{args.username} 抓取推文 {data['count']} 条\n")
        emit(data, args.out)
        return

    if args.command == "search":
        url = f"{BASE}/v1/twitter/tweets/advanced_search"
        params = {"query": args.query, "query_type": args.query_type, "count": args.count}
        data = paginate(api_key, url, params, args.pages)
        sys.stderr.write(f"[ScrapeBadger] 搜索「{args.query}」命中 {data['count']} 条\n")
        emit(data, args.out)
        return


if __name__ == "__main__":
    main()
