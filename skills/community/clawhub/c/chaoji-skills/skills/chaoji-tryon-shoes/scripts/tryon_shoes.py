#!/usr/bin/env python3
"""
ChaoJi Shoes Try-On - 潮际鞋靴试穿
使用 tryon_shoes API 将鞋商品图穿到模特脚上
"""

import argparse
import json
import os
import sys
from typing import List, Optional

# Add chaoji-tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chaoji-tools', 'scripts', 'lib'))
from executor import run_command


def tryon_shoes(
    list_images_shoe: List[str],
    human_input: str,
    poll: bool = True,
    auto_download: bool = True
) -> dict:
    """
    鞋靴试穿

    Args:
        list_images_shoe: 鞋商品图列表（1~3 张，本地路径/URL/OSS Path）
        human_input: 模特图片（本地路径/URL/OSS Path）
        poll: 是否轮询等待结果
        auto_download: 是否自动下载输出图片

    Returns:
        API 响应结果
    """
    input_params = {
        "list_images_shoe": list_images_shoe,
        "list_images_human": [human_input],
    }

    result = run_command("tryon_shoes", input_params, poll=poll)

    if not result.get('ok'):
        return result

    if auto_download and result.get('outputs'):
        outputs = result['outputs']
        output_dir = os.path.expanduser('~/.openclaw/media/outbound')
        os.makedirs(output_dir, exist_ok=True)

        downloaded_paths = []
        for i, output in enumerate(outputs):
            url = output.get('workOutputUrl')
            if url:
                local_path = download_image(url, output_dir)
                if local_path:
                    downloaded_paths.append(local_path)
                    outputs[i]['localPath'] = local_path

        result['downloaded_paths'] = downloaded_paths

    return result


def download_image(url: str, output_dir: str) -> Optional[str]:
    """下载图片到本地"""
    import urllib.request
    from datetime import datetime

    filename = os.path.basename(url.split("?")[0])
    if not filename:
        filename = f"tryon_shoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    local_path = os.path.join(output_dir, filename)

    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"下载图片失败：{e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='潮际鞋靴试穿 - 将鞋商品图穿到模特脚上',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 单张鞋图
  python tryon_shoes.py model.jpg --shoe shoe.jpg

  # 多张鞋图（效果更好）
  python tryon_shoes.py model.jpg --shoe front.jpg --shoe side1.jpg --shoe side2.jpg
'''
    )

    parser.add_argument('human_input', help='模特图像（本地路径、URL 或 OSS Path）')
    parser.add_argument('--shoe', dest='shoes', action='append', required=True,
                        help='鞋商品图（可多次指定，最多 3 张）')
    parser.add_argument('--no-download', action='store_true',
                        help='不自动下载输出图片')
    parser.add_argument('--no-poll', action='store_true',
                        help='不轮询等待结果')

    args = parser.parse_args()

    if len(args.shoes) > 3:
        parser.error('鞋商品图最多支持 3 张')

    try:
        result = tryon_shoes(
            list_images_shoe=args.shoes,
            human_input=args.human_input,
            poll=not args.no_poll,
            auto_download=not args.no_download
        )

        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get('downloaded_paths'):
            print("\n下载的图片路径:", file=sys.stderr)
            for path in result['downloaded_paths']:
                print(f"  - {path}", file=sys.stderr)

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
