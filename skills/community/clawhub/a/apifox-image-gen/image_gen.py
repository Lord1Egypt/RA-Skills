#!/usr/bin/env python3
"""
Apifox Image Generation
使用jyapi.AI-WX.CN图像生成API
"""

import urllib.request
import urllib.parse
import json
import os
import uuid
import sys

# API配置
API_KEY = "sk-hJP0yrKv2H7A4mjy39D8C3D5Dd17492494A65f4bCbE9859e"
BASE_URL = "https://jyapi.AI-WX.CN"

def generate_image(prompt, model="gpt-image-1.5", size="1024x1024", n=1, image=None):
    """生成图片"""
    url = f"{BASE_URL}/v1/images/generations"
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "size": size,
        "n": n,
        "prompt": prompt
    }
    
    if image:
        data["image"] = image
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        return {"error": str(e)}

def download_image(url, save_path=None):
    """下载图片"""
    if not save_path:
        save_path = f"/tmp/image_{uuid.uuid4().hex[:8]}.png"
    
    try:
        urllib.request.urlretrieve(url, save_path)
        return save_path
    except Exception as e:
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='图像生成工具')
    parser.add_argument('--prompt', '-p', required=True, help='图片描述')
    parser.add_argument('--model', '-m', default='gpt-image-1.5', help='模型 (gpt-image-1.5 或 grok-4-1-image)')
    parser.add_argument('--size', '-s', default='1024x1024', help='尺寸 (1024x1024, 1536x1024, 1024x1536, 1:1, 2:3, 3:2, 9:16, 16:9)')
    parser.add_argument('--n', '-n', type=int, default=1, help='生成数量')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    print(f"🎨 正在生成图片...")
    print(f"   Prompt: {args.prompt}")
    print(f"   Model: {args.model}")
    print(f"   Size: {args.size}")
    
    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        n=args.n
    )
    
    if "error" in result:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)
    
    if "data" in result:
        images = result["data"]
        for i, img in enumerate(images):
            img_url = img.get("url")
            if img_url:
                if args.output:
                    save_path = args.output
                else:
                    save_path = f"/tmp/generated_image_{i+1}_{uuid.uuid4().hex[:8]}.png"
                
                downloaded = download_image(img_url, save_path)
                if downloaded:
                    print(f"✅ 图片{i+1}已保存: {downloaded}")
                else:
                    print(f"❌ 图片{i+1}下载失败")
        
        if "usage" in result:
            usage = result["usage"]
            print(f"📊 Token使用: {usage.get('total_tokens', 'N/A')}")
    else:
        print(f"❌ 未知错误: {result}")

if __name__ == "__main__":
    main()
