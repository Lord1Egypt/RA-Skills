#!/usr/bin/env python3
"""88查招投标搜索 CLI 入口"""

COMMAND_NAME = "bidding_search"
COMMAND_DESC = "招投标搜索"

import os
import sys
import argparse
import re
import time

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.bidding_search.service import bid_search


def _strip_html(text: str) -> str:
    """去除 HTML 标签"""
    return re.sub(r'<[^>]+>', '', text) if text else ''


def _fmt_amount(val) -> str:
    """格式化金额字段"""
    return str(val) if val else '-'


def _build_markdown(result: dict, keyword: str, pageNo: str, pageSize: str) -> str:
    """将搜索结果格式化为 markdown 表格"""
    items = []
    if isinstance(result, dict):
        items = result.get("data", []) or []

    if not items:
        return f"未找到与「{keyword}」相关的招投标信息。"

    lines = [f"搜索「{keyword}」的招投标信息（第 {pageNo} 页，每页 {pageSize} 条）：\n"]
    lines.append("| # | 标题 | 类型 | 发布日期 | 地区 | 招标单位 | 中标单位 | 招标产品 | 中标金额 |")
    lines.append("|---|------|------|----------|------|----------|----------|----------|----------|")

    for i, item in enumerate(items, 1):
        title = _strip_html(item.get("title", ""))
        bid_type = item.get("subBidType", "") or item.get("bidType", "")
        publish_date = item.get("publishDate", "")
        province = item.get("province", "")
        city = item.get("city", "")
        region = f"{province}{city}" if province and city else province or city or "-"
        bid_unit_name = _strip_html((item.get("bidUnit") or {}).get("name", ""))
        win_bid_name = _strip_html((item.get("winBidUnit") or {}).get("name", ""))
        tender_products = item.get("tenderProducts", "")
        win_amount = _fmt_amount(item.get("winBidAmount"))

        lines.append(
            f"| {i} | {title} | {bid_type} | {publish_date} | {region} "
            f"| {bid_unit_name} | {win_bid_name} | {tender_products} | {win_amount} |"
        )

    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "AK 未配置。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="88查招投标搜索")
    parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    parser.add_argument("--pageNo", "-n", default="1", help="页码（默认 1）")
    parser.add_argument("--pageSize", "-s", default="10", help="每页条数（默认 10）")
    parser.add_argument("--provinces", nargs="*", default=None, help="省份筛选（多个用空格分隔）")
    parser.add_argument("--cities", nargs="*", default=None, help="城市筛选（多个用空格分隔）")
    parser.add_argument("--regions", nargs="*", default=None, help="区域筛选（多个用空格分隔）")
    parser.add_argument("--startTime", type=int, default=None, help="起始时间戳（毫秒），筛选发布日期 >= startTime")
    parser.add_argument("--endTime", type=int, default=None, help="截止时间戳（毫秒），筛选发布日期 <= endTime")
    args = parser.parse_args()

    try:
        result = bid_search(args.keyword, args.pageNo, args.pageSize,
                            provinces=args.provinces, cities=args.cities,
                            regions=args.regions,
                            startTime=args.startTime, endTime=args.endTime)
        markdown = _build_markdown(result, args.keyword, args.pageNo, args.pageSize)
        print_output(True, markdown, {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
