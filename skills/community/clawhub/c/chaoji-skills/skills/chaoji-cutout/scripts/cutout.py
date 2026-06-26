#!/usr/bin/env python3
"""
ChaoJi Cutout - 潮际智能抠图
支持人像抠图、服装分割、图案抠图、通用抠图、智能抠图
"""

import argparse
import json
import os
import sys
from typing import Optional

# Add chaoji-tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chaoji-tools', 'scripts', 'lib'))
from executor import run_command


def cutout(
    image: str,
    method: str = "auto",
    cate_token: Optional[str] = None,
    auto_download: bool = True
) -> dict:
    """
    智能抠图

    Args:
        image: 待抠图图片（本地路径/URL/OSS Path）
        method: 抠图模式（auto/seg/clothseg/patternseg/generalseg）
        cate_token: 服装类别，仅 clothseg 生效（upper/lower/overall）
        auto_download: 是否自动下载输出图片

    Returns:
        API 响应结果（同步返回）
    """
    input_params = {
        "image": image,
        "method": method,
    }

    if method == 'clothseg' and cate_token:
        input_params["cate_token"] = cate_token

    # 同步接口，poll 参数不影响
    result = run_command("cutout", input_params, poll=False)

    if not result.get('ok'):
        return result

    # 自动下载结果图片
    if auto_download:
        data = result.get('result', {}).get('data', {})
        output_dir = os.path.expanduser('~/.openclaw/media/outbound')
        os.makedirs(output_dir, exist_ok=True)

        downloaded_paths = []
        for key in ('view_image', 'image_mask'):
            url = data.get(key)
            if url:
                local_path = download_image(url, output_dir, suffix=key)
                if local_path:
                    downloaded_paths.append(local_path)

        result['downloaded_paths'] = downloaded_paths

    return result


def download_image(url: str, output_dir: str, suffix: str = "") -> Optional[str]:
    """下载图片到本地"""
    import urllib.request
    from datetime import datetime

    filename = os.path.basename(url.split("?")[0])
    if not filename:
        filename = f"cutout_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    local_path = os.path.join(output_dir, filename)

    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"下载图片失败：{e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='潮际智能抠图 - 支持多种抠图模式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python cutout.py photo.jpg
  python cutout.py photo.jpg --method seg
  python cutout.py model.jpg --method clothseg --cate-token upper
'''
    )

    parser.add_argument('image', help='待抠图图片（本地路径、URL 或 OSS Path）')
    parser.add_argument('--method', default='auto',
                        choices=['auto', 'seg', 'clothseg', 'patternseg', 'generalseg'],
                        help='抠图模式（默认 auto）')
    parser.add_argument('--cate-token', default=None,
                        choices=['upper', 'lower', 'overall'],
                        help='服装类别，仅 clothseg 模式生效')
    parser.add_argument('--no-download', action='store_true',
                        help='不自动下载输出图片')

    args = parser.parse_args()

    try:
        result = cutout(
            image=args.image,
            method=args.method,
            cate_token=args.cate_token,
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
