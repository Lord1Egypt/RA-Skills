#!/usr/bin/env python3
"""1688招商活动商品信息及建议价查询 CLI入口"""

COMMAND_NAME = "1688_enroll_offer_query"
COMMAND_DESC = "查询商品信息和建议提报价"

import importlib
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_raw
from _output import make_output, print_output, print_error
_service = importlib.import_module("capabilities.1688_enroll_offer_query.service")
query_enroll_offer = _service.query_enroll_offer


def main():
    if not get_ak_raw():
        print_output(make_output(
            success=False,
            markdown="❌ AK 未配置，无法查询商品信息。\n\n运行: `cli.py configure YOUR_AK`",
            data={"data": {}},
        ))
        return

    parser = argparse.ArgumentParser(description="查询商品信息和建议提报价")
    parser.add_argument("--activityId", "-a", type=int, required=True, help="活动Id")
    parser.add_argument("--itemId", "-i", type=int, required=True, help="商品Id")
    args = parser.parse_args()

    try:
        result = query_enroll_offer(args.activityId, args.itemId)
#         title = result.get("title", "")
#         sku_list = result.get("skuList") or []
#
#         lines = [f"**{title}**（商品ID: {result.get('itemId', args.itemId)}）\n"]
#
#         if sku_list:
#             lines.append(f"**SKU 明细**（共 {len(sku_list)} 个）：\n")
#             for sku in sku_list:
#                 sku_id = sku.get("skuId", "")
#                 sku_title = sku.get("title", "")
#                 sku_price = sku.get("price", "")
#                 sku_suggest = sku.get("suggestPrice", "")
#                 lines.append(f"- {sku_title}（SKU: {sku_id}）：当前价 {sku_price}，建议提报价 {sku_suggest}")
#         else:
#             price = result.get("price", "")
#             suggest_price = result.get("suggestPrice", "")
#             lines.append(f"- **当前价格**: {price}")
#             lines.append(f"- **建议提报价**: {suggest_price}")

#         markdown = "\n".join(lines)
        print_output(make_output(success=True, data=result))
    except Exception as exc:
        print_error(exc, {"data": {}})


if __name__ == "__main__":
    main()
