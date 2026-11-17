#!/usr/bin/env python3
"""CLI entrypoint for the unified item diagnosis context query."""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")))

from _output import print_error, print_output
from capabilities.get_item_diagnosis_context.service import get_item_diagnosis_context

COMMAND_NAME = "alibaba.1688.get.item.diagnosis.context"
COMMAND_DESC = "按商品ID聚合查询已校验身份的商品诊断上下文"


def _parse_args():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--item_id", required=True, help="至少 10 位的 1688 商品 ID")
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        print_output(True, "商品诊断上下文查询成功", get_item_diagnosis_context(args.item_id))
    except SystemExit:
        raise
    except Exception as exc:
        print_error(exc, getattr(exc, "data", None))


if __name__ == "__main__":
    main()
