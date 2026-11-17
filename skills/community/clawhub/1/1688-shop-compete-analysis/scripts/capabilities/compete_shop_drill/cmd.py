#!/usr/bin/env python3
"""竞店结构下钻 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse

from _output import print_output, print_error
from _compete import enrich_no_data_error

from capabilities.compete_shop_drill.service import drill_compete_shop

COMMAND_NAME = "compete_shop_drill"
COMMAND_DESC = "竞店结构下钻（核心指标对比+热销商品+价格带+引流词对比+买家结构六维，一次取全）"


def main():
    parser = argparse.ArgumentParser(description="竞店结构下钻")
    parser.add_argument("--member_id", "-m", required=True,
                        help="目标竞店会员ID，须已在竞店监控清单内"
                             "（来自 compete_shop_analysis 的行业榜/监控清单）")
    parser.add_argument("--cate_id", "-c", required=True,
                        help="类目ID，须来自 compete_category")
    parser.add_argument("--cate_level", "-l", type=int, default=1,
                        help="类目层级，需与 cate_id 同层级，默认 1")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        help="时间粒度 RECENT_7 / RECENT_30，默认 RECENT_7")
    parser.add_argument("--top", "-t", type=int, default=10,
                        help="商品榜/词榜各取前 N 条，默认 10")
    args = parser.parse_args()

    try:
        result = drill_compete_shop(
            member_id=args.member_id,
            cate_id=args.cate_id,
            cate_level=args.cate_level,
            date_type=args.date_type,
            top=args.top,
        )
        kw = result["keywords"]
        core = result.get("coreIndex")
        core_msg = ""
        if core:
            lead = sum(1 for m in core["metrics"]
                       if m["myLeadRate"] is not None and m["myLeadRate"] > 0)
            total = sum(1 for m in core["metrics"] if m["myLeadRate"] is not None)
            core_msg = f"核心指标本店领先 {lead}/{total} 项，"
        msg = (f"竞店下钻完成：{core_msg}"
               f"热销商品双方各 {len(result['topItems']['myShop'])}/"
               f"{len(result['topItems']['competitor'])} 条，"
               f"引流词共有 {kw['bothCount']} 个"
               f"（本店落后 {kw['behindCount']} 个、缺失 {kw['missingCount']} 个），"
               f"买家结构 {len(result['buyer'])} 维"
               + ("；⚠️ 部分维度无数据：" + "；".join(result["warnings"])
                  if result.get("warnings") else ""))
        print_output(True, msg, {"data": result})
    except Exception as e:
        print_error(enrich_no_data_error(e, "竞店结构下钻"), {"data": {}})


if __name__ == "__main__":
    main()
