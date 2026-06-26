#!/usr/bin/env python3
"""
NVIDIA Black Forest Labs Flux.2 Klein 4B 图像生成调用脚本
支持 --prompt, --width, --height 三个必需参数
响应体会以时间戳格式存到 /tmp/cs-free-image-generator/nv/ 目录下
"""

import argparse
import json
import os
import time
from datetime import datetime

import requests

# 尝试加载 dotenv（标准方式读取 .env 文件）
try:
    import dotenv
    dotenv.load_dotenv(os.path.expanduser("~/.openclaw/.env"), override=True)
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(
        description="调用 NVIDIA Flux.2 klein-4b 图像生成 API"
    )
    parser.add_argument(
        "--prompt", "-p", required=True,
        help="图像描述文本（必需）"
    )
    parser.add_argument(
        "--width", "-w", required=True, type=int,
        help="图像宽度像素值（必需）"
    )
    parser.add_argument(
        "--height", "-H", required=True, type=int,
        help="图像高度像素值（必需）"
    )
    args = parser.parse_args()

    # 校验宽高范围
    if args.width < 1 or args.width > 4096:
        raise ValueError("--width 必须在 1-4096 之间")
    if args.height < 1 or args.height > 4096:
        raise ValueError("--height 必须在 1-4096 之间")

    invoke_url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"

    headers = {
        "Authorization": f"Bearer {os.environ.get('NVIDIA_API_KEY', '')}",
        "Accept": "application/json",
    }

    payload = {
        "prompt": args.prompt,
        "width": args.width,
        "height": args.height,
        "seed": 0,
        "steps": 4,
    }

    response = requests.post(invoke_url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    response_body = response.json()

    # 打印响应
    print(json.dumps(response_body, ensure_ascii=False, indent=2))

    # 保存到文件
    output_dir = "/tmp/cs-free-image-generator/nv/"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = int(time.time())
    output_file = os.path.join(output_dir, f"{timestamp}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(response_body, f, ensure_ascii=False, indent=2)

    print(f"\n响应已保存到: {output_file}", flush=True)


if __name__ == "__main__":
    main()
