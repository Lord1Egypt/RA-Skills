#!/usr/bin/env python3
"""链接搜索 CLI入口"""

COMMAND_NAME = "link_search"
COMMAND_DESC = "链接找同款"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import (
    append_next_actions_markdown,
    # [DISABLED] 可视化商品墙已暂时禁用
    # append_visual_hint_markdown,
    # build_products_view_html,
    format_products_table,
    print_error,
    print_output,
    # write_products_html_file,
)

from capabilities.link_search.service import link_search, link_search_with_image


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未就绪。请先执行 `cli.py get_ak` 自动获取 AK；如自动获取失败，再执行 `cli.py configure YOUR_AK` 手动配置。\n\n获取 AK: https://clawhub.1688.com/",
                     {"data": {}, "action": "run_get_ak"})
        return

    parser = argparse.ArgumentParser(description="链接搜索 - 通过商品链接找同款")
    parser.add_argument("--url", "-u", required=True, help="商品链接或商品 ID")
    parser.add_argument("--image", "-i", help="商品图片 URL（当自动获取失败时使用）")
    parser.add_argument("--platform", "-p", default="1688", help="目标平台，默认 1688")
    parser.add_argument("--limit", "-l", type=int, default=10, help="返回数量，默认 10")
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

    try:
        # 如果提供了图片 URL，直接使用图片搜索
        if args.image:
            result = link_search_with_image(
                image_url=args.image,
                limit=args.limit,
                sort_type=args.sort,
                score_level=args.score_level,
                purchase_amount=args.purchase_amount,
                tags=args.tags,
                ic_tags=args.ic_tags,
            )
        else:
            result = link_search(
                url=args.url,
                platform=args.platform,
                limit=args.limit,
                sort_type=args.sort,
                score_level=args.score_level,
                purchase_amount=args.purchase_amount,
                tags=args.tags,
                ic_tags=args.ic_tags,
            )
        
        # 检查是否需要用户输入图片 URL
        if not result.get("success") and result.get("action") == "need_image_url":
            message = f"⚠️ {result.get('message')}\n\n"
            message += "请使用 `--image` 参数提供商品图片 URL：\n"
            message += f"python cmd.py --url \"{args.url}\" --image \"图片URL\""
            print_output(False, message, {"data": result})
            return
        
        # 构建输出消息
        total = result.get("total_results", 0)
        products = result.get("similar_products", [])
        
        if total > 0:
            header = f"✅ 找到 {total} 个同款/匹配商品"
            if result.get("source_image"):
                header += f"\n\n📷 商品主图: {result.get('source_image')}"
            message = format_products_table(products, header)
            # [DISABLED] 可视化商品墙已暂时禁用
            # sub_parts = []
            # if result.get("source_url"):
            #     sub_parts.append(f"来源链接：{result.get('source_url')}")
            # if result.get("source_image"):
            #     sub_parts.append(f"主图：{result.get('source_image')}")
            # html = build_products_view_html(
            #     products,
            #     page_title="1688 链接找同款结果",
            #     subtitle="\n".join(sub_parts),
            # )
            # html_path = write_products_html_file(html) if html else None
            # if html_path:
            #     message = append_visual_hint_markdown(message, html_path)
            #     result = dict(result)
            #     result["visual_html_path"] = html_path
            message = append_next_actions_markdown(message, total)
        else:
            message = "未找到匹配商品"
        
        print_output(True, message, {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
