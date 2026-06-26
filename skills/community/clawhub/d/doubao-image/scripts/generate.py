"""
豆包图片生成脚本
使用火山引擎豆包模型生成图片
"""

import os
import sys
import time
import json
import requests
import argparse

# 环境变量名
API_KEY_ENV = "VOLCENGINE_IMAGE_API_KEY"

# API 配置
API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

DEFAULT_MODEL = "doubao-seedream-4-0-250828"
DEFAULT_SIZE = "1024x1024"

def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        print(f"错误：请设置环境变量 {API_KEY_ENV}")
        print("获取方式：火山引擎控制台 → 点击顶部 API Key")
        sys.exit(1)
    return api_key

def generate_image(prompt, model=DEFAULT_MODEL, size=DEFAULT_SIZE, num=1):
    """生成图片"""
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer; {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "num": num
    }
    
    print(f"正在生成: {prompt}")
    print(f"模型: {model}, 尺寸: {size}")
    
    response = requests.post(API_BASE_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"错误: {response.status_code}")
        print(f"响应: {response.text}")
        return None
    
    result = response.json()
    
    # 检查是否有图片 URL
    if "data" in result and len(result.get("data", [])) > 0:
        img_url = result["data"][0].get("url")
        return img_url
    elif "error" in result:
        print(f"API 错误: {result['error']}")
        return None
    else:
        print(f"未知响应: {result}")
        return None

def download_image(url, save_path):
    """下载图片"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="豆包图片生成")
    parser.add_argument("prompt", help="图片描述")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="图片尺寸")
    parser.add_argument("--num", type=int, default=1, help="生成数量")
    
    args = parser.parse_args()
    
    # 生成图片
    img_url = generate_image(args.prompt, args.model, args.size, args.num)
    
    if not img_url:
        print("图片生成失败")
        sys.exit(1)
    
    print(f"图片 URL: {img_url}")
    
    # 下载图片
    output_dir = "C:/Users/zcf/.openclaw/workspace/downloads/images"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"douban_{int(time.time())}.png"
    save_path = os.path.join(output_dir, filename)
    
    if download_image(img_url, save_path):
        print(f"图片已保存: {save_path}")
    else:
        print("图片下载失败")

if __name__ == "__main__":
    main()
