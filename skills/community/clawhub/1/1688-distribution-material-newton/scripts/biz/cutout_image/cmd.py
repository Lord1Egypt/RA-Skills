#!/usr/bin/env python3
"""抠图（生成白底图）— CLI 入口"""

COMMAND_NAME = "cutout_image"
COMMAND_DESC = "抠图（生成白底图 / 白底裁剪图）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from biz.cutout_image.service import cutout_image


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法进行抠图。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="抠图（生成白底图）")
    parser.add_argument("--image_url", "-i", required=True,
                        help="单张图片 URL")
    parser.add_argument("--prompt", "-p", required=True, help="用户提文（原封不动传入）")
    args = parser.parse_args()

    try:
        result = cutout_image(
            image_url=args.image_url,
            prompt=args.prompt,
        )

        white_img = result.get("white_img", "")
        white_img_cropped = result.get("white_img_cropped", "")

        lines = ["抠图完成！\n"]
        if white_img:
            lines.append("**白底图（原始尺寸）：**\n")
            lines.append(f"![白底图]({white_img})\n")
        if white_img_cropped:
            lines.append("**白底裁剪图（紧凑裁剪）：**\n")
            lines.append(f"![白底裁剪图]({white_img_cropped})\n")

        print_output(True, "\n".join(lines), {
            "white_img": white_img,
            "white_img_cropped": white_img_cropped,
            "mask_img": result.get("mask_img", ""),
        })
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
