#!/usr/bin/env python3
"""初步竞店分析 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse

from _output import print_output, print_error
from _compete import enrich_no_data_error

from capabilities.compete_shop_analysis.service import analyze_compete_shop

COMMAND_NAME = "compete_shop_analysis"
COMMAND_DESC = "初步竞店分析（本店定位+行业排行+流失去向+监控清单，一次取全）"


def main():
    parser = argparse.ArgumentParser(description="初步竞店分析")
    parser.add_argument("--cate_id", "-c", required=True,
                        help="类目ID，须来自 compete_category")
    parser.add_argument("--cate_level", "-l", type=int, default=1,
                        help="类目层级，需与 cate_id 同层级，默认 1")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        help="时间粒度 RECENT_7 / RECENT_30，默认 RECENT_7")
    parser.add_argument("--top", "-t", type=int, default=10,
                        help="行业榜/流失榜各取前 N 条，默认 10")
    args = parser.parse_args()

    try:
        result = analyze_compete_shop(
            cate_id=args.cate_id,
            cate_level=args.cate_level,
            date_type=args.date_type,
            top=args.top,
        )
        rank = result["industryRank"]
        my_rank = rank["myRank"]
        focus = rank["focusCompetitor"]
        msg = (f"{result['myShop']['shopName']} 行业排名 "
               f"{my_rank if my_rank else '未进榜'}/{rank['totalCount']}"
               + (f"，重点竞店：{focus['shopName']}" if focus else "")
               + f"，流失竞店 {len(result['lossTop']['rows'])} 家")
        print_output(True, msg, {"data": result})
    except Exception as e:
        print_error(enrich_no_data_error(e, "行业店铺排行"), {"data": {}})


if __name__ == "__main__":
    main()
