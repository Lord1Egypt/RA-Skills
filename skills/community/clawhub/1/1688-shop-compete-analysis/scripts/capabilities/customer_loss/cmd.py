#!/usr/bin/env python3
"""买家流失商品分析 CLI 入口（裸调全景 + 发散多品佐证 + 交叉汇总）"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse

from _output import print_output, print_error

from capabilities.customer_loss.service import analyze_customer_loss

COMMAND_NAME = "customer_loss"
COMMAND_DESC = "买家流失商品分析（裸调全景+发散多品佐证+交叉汇总，dataSource=ITEM）"


def main():
    parser = argparse.ArgumentParser(description="买家流失商品识别与竞对对比")
    parser.add_argument("--item_ids", default=None,
                        help="指定下钻的流失商品ID，逗号分隔（本店商品，纯数字）；"
                             "不传则自动从「流失商品ID列表」取样")
    parser.add_argument("--sample_n", type=int, default=5,
                        help="发散取样品数（不含裸调随机命中品），默认 5，最大 20")
    args = parser.parse_args()

    item_ids = ([s.strip() for s in args.item_ids.split(",") if s.strip()]
                if args.item_ids else None)

    try:
        result = analyze_customer_loss(
            item_ids=item_ids,
            sample_n=args.sample_n,
        )
        s = result["summary"]
        msg = (f"买家流失分析完成：流失商品共 {result['overview']['totalLossItems']} 个，"
               f"本次下钻 {s['probed']} 品（含数据 {s['withData']}、"
               f"含竞对对比 {s['withRival']}，items 已按流失严重度降序）；"
               f"价格可比（±30% 内）{s['priceCompared']} 品中竞对更便宜 {s['rivalCheaper']}、"
               f"本店更便宜 {s['myCheaper']}、"
               f"价差超 ±30% 不可对标 {s['incomparablePriceGap']}（未计入便宜占比）"
               + (f"；⚠️ {'；'.join(result['warnings'])}" if result['warnings'] else ""))
        print_output(True, msg, {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
