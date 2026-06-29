"""RedFox：获取小红书内容。

子命令：
    search <keyword>     搜索小红书作品（searchArticle，按关键词，如公众人物姓名）
    detail               查询小红书作品详情（queryWorkDetail，按 workId 或 workLink）

用法示例：
    python scripts/redfox_xhs.py search "董宇辉" --pages 2 --out xhs_dyh.json
    python scripts/redfox_xhs.py detail --id 6a03be1b0000000035033163
    python scripts/redfox_xhs.py detail --link "https://www.xiaohongshu.com/explore/xxxx"

环境变量：REDFOX_API_KEY（请求头同名）
文档：
    searchArticle    https://redfox.hk/apis/xiaohongshu/384C6W6B
    queryWorkDetail  https://redfox.hk/apis/xiaohongshu/KR1LPTBF
"""
from __future__ import annotations

import argparse
import sys

from common import (
    REDFOX_BASE,
    REDFOX_SIGNUP,
    add_common_args,
    emit,
    redfox_headers,
    redfox_search,
    request_json,
    require_key,
)

SEARCH_ARTICLE = "/story/api/xhsUser/searchArticle"
QUERY_WORK_DETAIL = "/story/api/xhsUser/queryWorkDetail"


def query_work_detail(api_key: str, work_id: str | None, work_link: str | None) -> dict:
    """queryWorkDetail：按 workId 或 workLink 查询单个作品详情。"""
    body: dict[str, str] = {}
    if work_id:
        body["workId"] = work_id
    if work_link:
        body["workLink"] = work_link
    return request_json(
        "POST", REDFOX_BASE + QUERY_WORK_DETAIL, headers=redfox_headers(api_key), json_body=body
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="RedFox 小红书")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="搜索小红书作品（searchArticle）")
    p_search.add_argument("keyword", help="搜索关键词（如人物姓名）")
    p_search.add_argument("--sort", default="default", help="排序方式 sortType（默认 default）")
    p_search.add_argument("--pages", type=int, default=2, help="翻页数，每页 20 条（默认 2）")
    add_common_args(p_search)

    p_detail = sub.add_parser("detail", help="查询小红书作品详情（queryWorkDetail）")
    p_detail.add_argument("--id", dest="work_id", help="作品 id（workId）")
    p_detail.add_argument("--link", dest="work_link", help="作品链接（workLink）")
    add_common_args(p_detail)

    args = parser.parse_args()
    api_key = require_key("REDFOX_API_KEY", "RedFox 小红书", REDFOX_SIGNUP)

    if args.command == "search":
        data = redfox_search(api_key, SEARCH_ARTICLE, args.keyword, args.sort, args.pages)
        sys.stderr.write(f"[RedFox/小红书] 「{args.keyword}」抓取作品 {data['count']} 条\n")
        emit(data, args.out)
        return

    if args.command == "detail":
        if not args.work_id and not args.work_link:
            parser.error("detail 至少需要 --id 或 --link 其中之一")
        data = query_work_detail(api_key, args.work_id, args.work_link)
        emit(data, args.out)
        return


if __name__ == "__main__":
    main()
