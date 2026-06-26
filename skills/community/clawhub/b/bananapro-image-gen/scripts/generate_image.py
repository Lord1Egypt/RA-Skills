#!/usr/bin/env python3
"""
Banana Pro Image Generation Script
使用 Gemini 图像模型生成图片
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("请先安装 requests: pip install requests")
    sys.exit(1)


def generate_image(
    prompt: str,
    filename: str,
    api_key: str = None,
    api_url: str = None,
    model: str = "gemini-2.0-flash-exp-image-generation",
    resolution: str = "1K",
    input_image: str = None,
):
    """
    生成图片
    
    Args:
        prompt: 图片描述
        filename: 输出文件名
        api_key: API密钥
        api_url: API端点
        model: 模型名称
        resolution: 分辨率 (1K/2K/4K)
        input_image: 输入图片路径（用于编辑）
    """
    # 获取 API Key
    api_key = api_key or os.environ.get("NEXTAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 错误：请设置 API Key")
        print("方式1: export NEXTAI_API_KEY='your-key'")
        print("方式2: --api-key 'your-key'")
        sys.exit(1)
    
    # 默认 API 端点
    if not api_url:
        api_url = os.environ.get("NEXTAI_API_URL", "https://generativelanguage.googleapis.com/v1beta")
    
    # 构造请求 URL
    url = f"{api_url.rstrip('/')}/models/{model}:generateContent?key={api_key}"
    
    print(f"正在生成图片...")
    print(f"提示词: {prompt}")
    print(f"模型: {model}")
    print(f"分辨率: {resolution}")
    
    # 构造请求体
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["image", "text"]
        }
    }
    
    # 如果有输入图片，添加到请求中
    if input_image and os.path.exists(input_image):
        with open(input_image, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        # 获取 MIME 类型
        ext = Path(input_image).suffix.lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}
        mime_type = mime_map.get(ext, "image/jpeg")
        payload["contents"][0]["parts"].insert(0, {
            "inline_data": {
                "mime_type": mime_type,
                "data": image_data
            }
        })
        print(f"输入图片: {input_image}")
    
    # 发送请求
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"❌ API 错误: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        result = response.json()
        
        # 解析响应
        for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                # 解码并保存图片
                image_data = base64.b64decode(part["inlineData"]["data"])
                with open(filename, "wb") as f:
                    f.write(image_data)
                file_size = os.path.getsize(filename) / 1024
                print(f"✅ 图片已成功生成并保存到: {filename}")
                print(f"文件大小: {file_size:.2f} KB")
                return filename
        
        print("❌ 响应中没有找到图片数据")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="使用 Gemini 生成图片")
    parser.add_argument("--prompt", required=True, help="图片描述")
    parser.add_argument("--filename", help="输出文件名")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--api-url", help="API端点")
    parser.add_argument("--model", default="gemini-2.0-flash-exp-image-generation", help="模型名称")
    parser.add_argument("--resolution", choices=["1K", "2K", "4K"], default="1K", help="分辨率")
    parser.add_argument("--input-image", help="输入图片路径（用于编辑）")
    
    args = parser.parse_args()
    
    # 生成默认文件名
    if not args.filename:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        args.filename = f"{timestamp}-generated.png"
    
    generate_image(
        prompt=args.prompt,
        filename=args.filename,
        api_key=args.api_key,
        api_url=args.api_url,
        model=args.model,
        resolution=args.resolution,
        input_image=args.input_image,
    )


if __name__ == "__main__":
    main()
