"""RedFox：获取微信公众号内容。

子命令：
    search <keyword>     搜索公众号文章（searchArticle，按关键词，如人物姓名/主题）
    work   <workUuid>    查询公众号作品详情（queryWork，按作品 uuid）

用法示例：
    python scripts/redfox_gzh.py search "张维迎" --sort _2 --pages 2 --out gzh_zwy.json
    python scripts/redfox_gzh.py work 7018B165C5D5BF9BE0B9D3158EBE47EA

排序 sortType：_0 默认(相关性) / _2 最新(发布时间倒序) / _4 最热(阅读数倒序)
环境变量：REDFOX_API_KEY（请求头同名）
文档：
    searchArticle  https://redfox.hk/apis/gongzhonghao/PW97QFBS
    queryWork      https://redfox.hk/apis/gongzhonghao/XEO0QQNF
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

SEARCH_ARTICLE = "/story/api/gzhData/searchArticle"
QUERY_WORK = "/story/api/gzhData/queryWork"


def query_work(api_key: str, work_uuid: str) -> dict:
    """queryWork：按作品 uuid 查询单篇文章详情。"""
    body = {"workUuid": work_uuid}
    return request_json(
        "POST", REDFOX_BASE + QUERY_WORK, headers=redfox_headers(api_key), json_body=body
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="RedFox 公众号")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="搜索公众号文章（searchArticle）")
    p_search.add_argument("keyword", help="搜索关键词（如人物姓名/主题）")
    p_search.add_argument("--sort", default="_0", help="排序 sortType：_0 默认 / _2 最新 / _4 最热")
    p_search.add_argument("--pages", type=int, default=2, help="翻页数，每页 20 条（默认 2）")
    add_common_args(p_search)

    p_work = sub.add_parser("work", help="查询公众号作品详情（queryWork）")
    p_work.add_argument("work_uuid", help="作品 uuid（workUuid）")
    add_common_args(p_work)

    args = parser.parse_args()
    api_key = require_key("REDFOX_API_KEY", "RedFox 公众号", REDFOX_SIGNUP)

    if args.command == "search":
        data = redfox_search(api_key, SEARCH_ARTICLE, args.keyword, args.sort, args.pages)
        sys.stderr.write(f"[RedFox/公众号] 「{args.keyword}」抓取文章 {data['count']} 条\n")
        emit(data, args.out)
        return

    if args.command == "work":
        data = query_work(api_key, args.work_uuid)
        emit(data, args.out)
        return


if __name__ == "__main__":
    main()
