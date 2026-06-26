#!/usr/bin/env python3
"""
二维码生成工具 - 生成在线二维码 URL
纯 Python 实现，无外部依赖，使用免费 API

用法:
  python3 qrcode.py --url "https://xxx"
  python3 qrcode.py -u "https://xxx" -s 400
"""

import argparse
import urllib.parse


def get_qrcode_url(url: str, size: int = 300) -> str:
    """
    生成二维码图片的 URL（使用免费 API）

    Args:
        url: 需要编码的链接
        size: 图片尺寸（像素）

    Returns:
        二维码图片的 URL
    """
    encoded_url = urllib.parse.quote(url, safe='')
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded_url}"


def main():
    parser = argparse.ArgumentParser(
        description='生成二维码 URL，方便手机扫码访问预订链接'
    )
    parser.add_argument(
        '--url', '-u',
        required=True,
        help='需要编码的链接'
    )
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=300,
        help='图片尺寸（像素），默认 300'
    )

    args = parser.parse_args()

    qrcode_url = get_qrcode_url(args.url, args.size)
    print(qrcode_url)


if __name__ == '__main__':
    main()
