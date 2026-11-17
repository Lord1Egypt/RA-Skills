"""build_tool_url — CLI 入口

接收命令行参数，调用 service.build_tool_url，输出透传 JSON。
"""

COMMAND_NAME = "build_tool_url"
COMMAND_DESC = "构建图片工具页面 URL（--type main|carousel|detail|matting|replaceSubject|outpainting|digitalModel）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.build_tool_url.service import build_tool_url


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--type", required=True, dest="type_",
                        help="图片类型: main(主图优化) / carousel(轮播图) / detail(详情图) / "
                             "matting(白底图) / replaceSubject(背景替换) / outpainting(扩图) / "
                             "digitalModel(数字模特)")
    parser.add_argument("--offer-id", default=None,
                        help="商品 ID")
    parser.add_argument("--img-url", default=None,
                        help="单张图片路径/URL（type=main 时使用）")
    parser.add_argument("--img-url-list", default=None,
                        help="多张图片路径/URL，逗号分隔（type=carousel/detail 时使用）")

    args = parser.parse_args()

    try:
        result = build_tool_url(
            type_=args.type_,
            offer_id=args.offer_id,
            img_url=args.img_url,
            img_url_list=args.img_url_list,
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    main()
