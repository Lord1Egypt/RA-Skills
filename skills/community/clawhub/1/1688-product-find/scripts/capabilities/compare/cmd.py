#!/usr/bin/env python3
"""商品比价 CLI 入口"""

COMMAND_NAME = "compare"
COMMAND_DESC = "商品比价 - 基于商品图片搜索同款并自动对比"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error, format_compare_table

from capabilities.compare.service import compare_products


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未就绪。请先执行 `cli.py get_ak` 自动获取 AK；如自动获取失败，再执行 `cli.py configure YOUR_AK` 手动配置。\n\n获取 AK: https://clawhub.1688.com/",
                     {"data": {}, "action": "run_get_ak"})
        return

    parser = argparse.ArgumentParser(description="商品比价 - 基于商品图片或链接搜索同款并自动对比")
    parser.add_argument("--image", "-i", default=None, help="商品图片 URL 或本地路径（与 --url 二选一）")
    parser.add_argument("--url", "-u", default=None, help="商品链接或商品 ID（自动提取主图，与 --image 二选一）")
    parser.add_argument("--query", "-q", default=None, help="附加关键词（规格、品类等，可选）")
    parser.add_argument("--platform", "-p", default="1688", help="目标平台，默认 1688")
    parser.add_argument("--limit", "-l", type=int, default=3, help="对比商品数量，默认 3")
    parser.add_argument("--sort", "-s", default=None, 
                        choices=["price_asc", "price_desc", "sold_desc", "yx_desc"],
                        help="排序方式：price_asc(价格低→高)、price_desc(价格高→低)、sold_desc(销量高→低)、yx_desc(严选指数高→低)")
    parser.add_argument("--score-level", default="high",
                        choices=["high", "medium", "low"],
                        help="相关性档位：high(高)、medium(中)、low(低)，默认 high")
    parser.add_argument("--purchase-amount", type=int, default=1,
                        help="采购件数，默认 1")
    parser.add_argument("--tags", default="4306497",
                        help="TC标（品池标签），英文逗号分隔，默认 4306497")
    parser.add_argument("--ic-tags", default=None,
                        help="IC标（品池标签），英文逗号分隔")
    args = parser.parse_args()

    # 校验：--image 和 --url 至少提供一个
    if not args.image and not args.url:
        parser.error("必须提供 --image 或 --url 参数（二选一）")

    try:
        result = compare_products(
            image=args.image,
            url=args.url,
            query=args.query,
            platform=args.platform,
            limit=args.limit,
            sort_type=args.sort,
            score_level=args.score_level,
            purchase_amount=args.purchase_amount,
            tags=args.tags,
            ic_tags=args.ic_tags,
        )

        # 构建输出
        compared = result.get("compare_products", [])
        total_candidates = result.get("total_candidates", 0)

        if compared:
            count = len(compared)
            if count == 1:
                header = f"### 同款比价结果\n\n从 {total_candidates} 个同款中综合评估，以下商品在多个维度均表现最优："
            else:
                header = f"### 同款比价结果\n\n从 {total_candidates} 个同款中选出 {count} 款对比："
            message = format_compare_table(compared, header)
        else:
            message = "未找到可比价的同款商品"

        print_output(True, message, {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
