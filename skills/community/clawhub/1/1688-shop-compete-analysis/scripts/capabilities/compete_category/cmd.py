#!/usr/bin/env python3
"""竞争分析类目树查询 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse

from _output import print_output, print_error
from _compete import enrich_no_data_error

from capabilities.compete_category.service import get_compete_category

COMMAND_NAME = "compete_category"
COMMAND_DESC = "获取竞争分析可用类目树（cateId 唯一合法来源）"


def main():
    parser = argparse.ArgumentParser(description="竞争分析类目树")
    parser.add_argument("--with_children", action="store_true",
                        help="返回二/三级子类目（默认只返一级）")
    args = parser.parse_args()

    try:
        result = get_compete_category(
            with_children=args.with_children,
        )
        if result["needUserChoice"]:
            names = "、".join(c["cateName"] or "-" for c in result["level1"])
            msg = f"该店铺有 {len(result['level1'])} 个一级类目（{names}），请让用户选择要分析哪个类目"
        else:
            c = result["level1"][0]
            msg = f"类目已确定：{c['cateName']}（cateId={c['cateId']}, cateLevel=1）"
        print_output(True, msg, {"data": result})
    except Exception as e:
        print_error(enrich_no_data_error(e, "类目树"), {"data": {}})


if __name__ == "__main__":
    main()
