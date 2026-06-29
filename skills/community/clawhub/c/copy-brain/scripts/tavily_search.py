"""Tavily 搜索（在 agent 内置搜索不佳时使用：结果偏旧 / 不支持多语言 / 关键词匹配差）。

仅暴露 3 个搜索参数：query（必填）、search_depth、time_range（均可选其二）。
如需查看搜索结果的全文，请改用 agent 内置的网页提取工具，对结果 URL 提取。

用法示例：
    python scripts/tavily_search.py "Elon Musk biography"
    python scripts/tavily_search.py "马斯克 最新观点" --search-depth advanced --time-range month
    python scripts/tavily_search.py "Sam Altman interview" --out tavily_raw.json

环境变量：TAVILY_API_KEY
文档：https://docs.tavily.com/documentation/api-reference/endpoint/search
"""
from __future__ import annotations

import argparse
import sys

from common import (
    add_common_args,
    emit,
    request_json,
    require_key,
)

API_URL = "https://api.tavily.com/search"
SIGNUP_URL = "https://app.tavily.com"


def main() -> None:
    parser = argparse.ArgumentParser(description="Tavily 搜索")
    parser.add_argument("query", help="搜索查询语句（必填）")
    parser.add_argument(
        "--search-depth",
        choices=["basic", "advanced", "fast", "ultra-fast"],
        default="basic",
        help="搜索深度（可选，默认 basic；advanced 相关性最高但消耗 2 credits）",
    )
    parser.add_argument(
        "--time-range",
        choices=["day", "week", "month", "year"],
        default=None,
        help="按发布/更新时间过滤（可选）：day / week / month / year",
    )
    add_common_args(parser)
    args = parser.parse_args()

    api_key = require_key("TAVILY_API_KEY", "Tavily Search", SIGNUP_URL)

    body: dict = {
        "query": args.query,
        "search_depth": args.search_depth,
    }
    if args.time_range:
        body["time_range"] = args.time_range

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = request_json("POST", API_URL, headers=headers, json_body=body)

    results = data.get("results", []) or []
    sys.stderr.write(f"[Tavily] 查询「{args.query}」返回 {len(results)} 条结果\n")
    emit(data, args.out)


if __name__ == "__main__":
    main()
