#!/usr/bin/env python3
"""图片优化（AI 生图）— CLI 入口"""

COMMAND_NAME = "image_optimize"
COMMAND_DESC = "图片优化（AI 生图，含异步轮询）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from biz.image_optimize.service import submit_and_wait


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法进行图片优化。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="图片优化（AI 生图）")
    parser.add_argument("--image_urls", "-i", required=True,
                        help="图片 URL 列表，英文逗号分隔。第 1 张为主图，后续为参考图")
    parser.add_argument("--prompt", "-p", required=True, help="用户提文（原封不动传入）")
    parser.add_argument("--size", "-s", default="", help="输出比例：1:1 / 2:3 / 9:16（可选）")
    parser.add_argument("--offer_id", "-o", default="", help="商品 ID（可选）")
    args = parser.parse_args()

    try:
        result = submit_and_wait(
            image_urls=args.image_urls,
            prompt=args.prompt,
            size=args.size,
            offer_id=args.offer_id,
        )

        gen_url = result.get("gen_image_url", "")
        reasoning = result.get("reasoning_context", "")
        time_cost = result.get("time_cost", "")

        lines = ["图片优化完成！\n"]
        if gen_url:
            lines.append(f"![优化后的图片]({gen_url})\n")
        if time_cost:
            lines.append(f"耗时：{time_cost} 秒\n")
        if reasoning:
            lines.append(f"**优化说明：**\n{reasoning}")

        print_output(True, "\n".join(lines), {
            "gen_image_url": gen_url,
            "reasoning_context": reasoning,
            "instance_id": result.get("instance_id", ""),
            "time_cost": time_cost,
            "raw_output": result.get("raw_output", {}),
        })
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
