#!/usr/bin/env python3
"""询盘对话配置 CLI 入口 -- 配置询盘的对话轮次/AI 自动回复能力"""

COMMAND_NAME = "inquiry_config"
COMMAND_DESC = "询盘对话配置（配置对话轮次/AI 自动回复）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.inquiry_config.service import inquiry_config


def main():
    parser = argparse.ArgumentParser(description="询盘对话配置 - 配置对话轮次/AI 自动回复能力")
    parser.add_argument("--multi-round", action="store_true",
                        help="多轮对话开关。用户明确要求支持多轮对话/AI 自动多轮回复时加此参数（orderSingleRound=false）；不加则默认单轮（orderSingleRound=true）")
    args = parser.parse_args()

    try:
        # 默认单轮（order_single_round=True）；显式要求多轮时置 False
        order_single_round = not args.multi_round

        result = inquiry_config(order_single_round=order_single_round)

        mode = "单轮对话（不自动多轮回复）" if order_single_round else "多轮对话（AI 自动回复）"
        message = "对话配置已更新为{}，耗时 {}s。".format(
            mode,
            result.get("elapsed_seconds", ""),
        )
        output_data = {
            "success": result.get("success", False),
            "orderSingleRound": result.get("orderSingleRound", ""),
            "elapsed_seconds": result.get("elapsed_seconds", 0),
        }
        print_output(True, message, output_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
