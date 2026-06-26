#!/usr/bin/env python3
"""
ChaoJi Try-On - 潮际虚拟试衣
使用 ChaoJi API 将服装图片穿到模特身上
"""

import argparse
import json
import os
import sys
from typing import Optional

# Add chaoji-tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chaoji-tools', 'scripts', 'lib'))
from executor import run_command


def tryon(
    cloth_input: str,
    human_input: str,
    cloth_length: str = "overall",
    dpi: int = 300,
    output_format: str = "jpg",
    batch_size: int = 1,
    poll: bool = True,
    auto_download: bool = True
) -> dict:
    """
    虚拟试衣
    
    Args:
        cloth_input: 服装图片（本地路径、URL 或 OSS Path）
        human_input: 模特图片（本地路径、URL 或 OSS Path）
        cloth_length: 上身区域（upper/lower/overall）
        dpi: 输出图像 DPI
        output_format: 输出格式（jpg/png）
        batch_size: 生成图片数量
        poll: 是否轮询等待结果
        auto_download: 是否自动下载输出图片
    
    Returns:
        API 响应结果
    """
    # 准备输入参数
    input_params = {
        "image_cloth": cloth_input,
        "list_images_human": [human_input],
        "cloth_length": cloth_length,
        "dpi": dpi,
        "output_format": output_format,
        "batch_size": batch_size,
    }
    
    # 调用统一执行器
    result = run_command("model_tryon_quick", input_params, poll=poll)
    
    # 处理结果
    if not result.get('ok'):
        # 返回错误信息
        return result
    
    # 自动下载输出图片
    if auto_download and result.get('outputs'):
        outputs = result['outputs']
        output_dir = os.path.expanduser('~/.openclaw/media/outbound')
        os.makedirs(output_dir, exist_ok=True)
        
        downloaded_paths = []
        for i, output in enumerate(outputs):
            url = output.get('workOutputUrl')
            if url:
                # 下载图片
                local_path = download_image(url, output_dir)
                if local_path:
                    downloaded_paths.append(local_path)
                    outputs[i]['localPath'] = local_path
        
        result['downloaded_paths'] = downloaded_paths
    
    return result


def download_image(url: str, output_dir: str) -> Optional[str]:
    """
    下载图片到本地
    
    Args:
        url: 图片 URL
        output_dir: 输出目录
    
    Returns:
        本地文件路径，下载失败返回 None
    """
    import urllib.request
    from datetime import datetime
    
    # 确定文件名
    filename = os.path.basename(url.split("?")[0])
    if not filename:
        filename = f"tryon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    
    local_path = os.path.join(output_dir, filename)
    
    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"下载图片失败：{e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description='潮际虚拟试衣 - 将服装图片穿到模特身上',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
参数说明:
  cloth_input   服装图像（本地路径、URL 或 OSS Path）
  human_input   模特图像（本地路径、URL 或 OSS Path）

可选参数:
  --cloth-length  上身区域：upper(上装), lower(下装), overall(全身)
  --dpi           输出图像 DPI
  --format        输出格式：jpg 或 png
  --batch-size    生成图片数量 [1, 8]
  --no-download   不自动下载输出图片
  --no-poll       不轮询等待结果（异步模式）

示例:
  python tryon.py /path/to/cloth.jpg /path/to/model.jpg
  python tryon.py https://example.com/cloth.jpg https://example.com/model.jpg
  python tryon.py marketing/image/xxx/cloth.jpg marketing/image/xxx/model.jpg
  python tryon.py cloth.jpg model.jpg --batch-size 4 --cloth-length upper
'''
    )

    parser.add_argument('cloth_input', help='服装图像（本地路径、URL 或 OSS Path）')
    parser.add_argument('human_input', help='模特图像（本地路径、URL 或 OSS Path）')
    parser.add_argument('--cloth-length', type=str, default='overall', 
                        choices=['upper', 'lower', 'overall'],
                        help='上身区域')
    parser.add_argument('--dpi', type=int, default=300, help='输出图像 DPI')
    parser.add_argument('--format', type=str, default='jpg', 
                        choices=['jpg', 'png'], help='输出格式')
    parser.add_argument('--batch-size', type=int, default=1, 
                        help='生成图片数量')
    parser.add_argument('--no-download', action='store_true', 
                        help='不自动下载输出图片')
    parser.add_argument('--no-poll', action='store_true', 
                        help='不轮询等待结果（异步模式）')

    args = parser.parse_args()

    try:
        result = tryon(
            cloth_input=args.cloth_input,
            human_input=args.human_input,
            cloth_length=args.cloth_length,
            dpi=args.dpi,
            output_format=args.format,
            batch_size=args.batch_size,
            poll=not args.no_poll,
            auto_download=not args.no_download
        )

        # 输出结果
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 如果有下载的图片，输出路径
        if result.get('downloaded_paths'):
            print("\n下载的图片路径:", file=sys.stderr)
            for path in result['downloaded_paths']:
                print(f"  - {path}", file=sys.stderr)

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
