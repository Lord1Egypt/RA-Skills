#!/usr/bin/env python3
"""获取商品主图信息 — CLI 入口"""

COMMAND_NAME = "image_info"
COMMAND_DESC = "获取商品主图信息"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from biz.image_info.service import get_image_info


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法获取商品信息。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="获取商品主图信息")
    parser.add_argument("--offer_id", "-o", required=True, help="1688 商品 ID")
    args = parser.parse_args()

    try:
        result = get_image_info(args.offer_id)
        main_urls = result.get("main_image_urls", [])
        white_url = result.get("white_image_url", "")

        lines = [f"商品 {args.offer_id} 的主图信息：\n"]
        for i, url in enumerate(main_urls):
            label = "（默认主图）" if i == 0 else ""
            lines.append(f"{i + 1}. {label}![主图{i + 1}]({url})")
        if white_url:
            lines.append(f"\n白底图：![白底图]({white_url})")

        print_output(True, "\n".join(lines), {
            "main_image_urls": main_urls,
            "white_image_url": white_url,
        })
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
