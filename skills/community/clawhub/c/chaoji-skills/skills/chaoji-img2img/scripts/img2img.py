#!/usr/bin/env python3
"""
ChaoJi Image-to-Image - 潮际图生图（素材生成）
根据参考图和文字描述生成新图片
"""

import argparse
import json
import os
import sys
from typing import List, Optional

# Add chaoji-tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chaoji-tools', 'scripts', 'lib'))
from executor import run_command


def img2img(
    img: List[str],
    prompt: str,
    ratio: str = "auto",
    resolution: str = "1k",
    poll: bool = True,
    auto_download: bool = True
) -> dict:
    """
    图生图（素材生成）

    Args:
        img: 参考图列表（1~14 张，本地路径/URL/OSS Path）
        prompt: 生成图片的文字描述
        ratio: 生图比例（默认 auto）
        resolution: 生成分辨率（默认 1k）
        poll: 是否轮询等待结果
        auto_download: 是否自动下载输出图片

    Returns:
        API 响应结果
    """
    input_params = {
        "img": img,
        "prompt": prompt,
        "ratio": ratio,
        "resolution": resolution,
    }

    result = run_command("image2image", input_params, poll=poll)

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
        filename = f"img2img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    local_path = os.path.join(output_dir, filename)

    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"下载图片失败：{e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='潮际图生图（素材生成）- 根据参考图和文字描述生成新图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python img2img.py --img ref.jpg --prompt "电商主图，白色背景"
  python img2img.py --img ref1.jpg --img ref2.jpg --prompt "时尚海报" --ratio 3:4 --resolution 2k
'''
    )

    parser.add_argument('--img', dest='imgs', action='append', required=True,
                        help='参考图（可多次指定，最多 14 张）')
    parser.add_argument('--prompt', required=True,
                        help='生成图片的文字描述')
    parser.add_argument('--ratio', default='auto',
                        choices=['auto', '1:1', '3:4', '4:3', '9:16', '16:9', '2:3', '3:2', '21:9'],
                        help='生图比例（默认 auto）')
    parser.add_argument('--resolution', default='1k',
                        choices=['1k', '2k'],
                        help='生成分辨率（默认 1k）')
    parser.add_argument('--no-download', action='store_true',
                        help='不自动下载输出图片')
    parser.add_argument('--no-poll', action='store_true',
                        help='不轮询等待结果')

    args = parser.parse_args()

    if len(args.imgs) > 14:
        parser.error('参考图最多支持 14 张')

    try:
        result = img2img(
            img=args.imgs,
            prompt=args.prompt,
            ratio=args.ratio,
            resolution=args.resolution,
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
