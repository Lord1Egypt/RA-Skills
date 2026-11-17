#!/usr/bin/env python3
"""竞品（商品级）结构下钻 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse

from _output import print_output, print_error
from _compete import enrich_no_data_error

from capabilities.compete_offer_drill.service import drill_compete_offer

COMMAND_NAME = "compete_offer_drill"
COMMAND_DESC = "竞品结构下钻（引流词+流量来源+买家结构七维，商品可指定或自动从监控池选）"


def main():
    parser = argparse.ArgumentParser(description="竞品（商品级）结构下钻")
    parser.add_argument("--cate_id", "-c", required=True,
                        help="类目ID，须来自 compete_category")
    parser.add_argument("--offer_id", "-o", default=None,
                        help="竞品商品ID（须在竞品监控池内）；"
                             "不传则自动取池内交易水平最高的竞品")
    parser.add_argument("--offer_id2", default=None,
                        help="第二个竞品商品ID（可选，用于三方买家结构对比）")
    parser.add_argument("--my_offer_id", default=None,
                        help="本店对位商品ID（须在监控池内）；"
                             "不传则自动匹配同叶子类目的本店商品")
    parser.add_argument("--cate_level", "-l", type=int, default=1,
                        help="类目层级，需与 cate_id 同层级，默认 1")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        help="时间粒度 RECENT_7 / RECENT_30，默认 RECENT_7")
    parser.add_argument("--top", "-t", type=int, default=10,
                        help="词榜取前 N 条，默认 10")
    args = parser.parse_args()

    try:
        result = drill_compete_offer(
            cate_id=args.cate_id,
            offer_id=args.offer_id,
            offer_id2=args.offer_id2,
            my_offer_id=args.my_offer_id,
            cate_level=args.cate_level,
            date_type=args.date_type,
            top=args.top,
        )
        offers = result["offers"]
        auto = offers["autoPicked"]
        rival_names = "、".join(
            f"{r['shopName']}({r['offerId']})" for r in offers["rivals"])
        basis_desc = {
            "sameLeafCate": "同类目对位",
            "titleOverlap": "标题词重合近似对位",
            "priceProximity": "价位接近近似对位",
            "tradeIndex": "按交易水平对位",
        }
        picked = []
        if auto["rival"]:
            picked.append("竞品自动选取")
        if auto["myOffer"]:
            picked.append("本店商品自动匹配："
                          + basis_desc.get(auto["matchBasis"], auto["matchBasis"]))
        warn = ""
        if not auto["comparable"]:
            warn = ("；⚠️ 两个商品不属同一叶子类目（监控池内无同类目本店商品），"
                    "对比可比性有限，建议用 --my_offer_id / --offer_id 指定同品类商品")
        pool = result["pool"]
        msg = (f"竞品下钻完成：本店商品 {offers['myOffer']['offerId']} vs {rival_names}"
               + (f"（{'、'.join(picked)}）" if picked else "")
               + f"；监控池共 {pool['total']} 个（本店 {pool['myOfferCount']} / "
                 f"竞品 {pool['rivalOfferCount']}），"
               + f"本店词榜 {result['keywords']['myTotal']} 词，"
                 f"买家结构 {len(result['buyer'])} 维"
               + warn)
        print_output(True, msg, {"data": result})
    except Exception as e:
        print_error(enrich_no_data_error(e, "竞品结构下钻"), {"data": {}})


if __name__ == "__main__":
    main()
