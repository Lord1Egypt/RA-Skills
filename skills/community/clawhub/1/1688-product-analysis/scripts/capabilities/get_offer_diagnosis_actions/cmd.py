#!/usr/bin/env python3
"""商品库明细行动点查询 CLI 入口。"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_error, print_output
from capabilities.get_offer_diagnosis_actions.service import get_offer_diagnosis_actions

COMMAND_NAME = "get_offer_diagnosis_actions"
COMMAND_DESC = "查询商品库明细的AI分析与优化行动点"


def _parse_args():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--offer_id", required=True, help="1688 商品 ID")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="店铺登录ID，指定查询的店铺")
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        result = get_offer_diagnosis_actions(args.offer_id, args.NEWTON_SHOP_LOGIN_ID)
        print_output(True, "商品库行动点查询成功", result)
    except SystemExit:
        raise
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
