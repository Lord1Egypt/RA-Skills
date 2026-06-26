#!/usr/bin/env python3
"""
图片生成脚本 - 生成后自动下载到本地
"""
import requests
import json
import sys
import os
import time
import tempfile

API_KEY = os.environ.get("AIPING_API_KEY", "")
API_BASE = "https://aiping.cn/api/v1"

DEFAULT_MODEL = "Doubao-Seedream-5.0-lite"

def generate_image(model: str = "", prompt: str = "", negative_prompt: str = "", 
                  image_url: str = "", aspect_ratio: str = "", timeout: int = 60,
                  download: bool = True) -> dict:
    """
    生成图片，默认模型: Doubao-Seedream-5.0-lite
    download=True: 生成后自动下载到本地 /tmp/，返回 local_path
    download=False: 只返回 CDN URL
    """
    if not model:
        model = DEFAULT_MODEL
    if not prompt:
        raise ValueError("prompt 不能为空")
    api_key = os.environ.get("AIPING_API_KEY", API_KEY)
    if not api_key:
        raise EnvironmentError("请设置环境变量 AIPING_API_KEY")
    payload = {
        "model": model,
        "prompt": prompt
    }
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if image_url:
        payload["image"] = image_url
    if aspect_ratio:
        payload["aspect_ratio"] = aspect_ratio
    
    resp = requests.post(
        f"{API_BASE}/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=timeout
    )
    resp.raise_for_status()
    data = resp.json()
    
    result = {
        "model": model,
        "provider": data.get("provider", "")
    }
    
    if "data" in data and len(data["data"]) > 0:
        cdn_url = data["data"][0]["url"]
        result["url"] = cdn_url
        
        if download:
            # 自动下载到本地
            try:
                local_path = download_image(cdn_url)
                result["local_path"] = local_path
            except Exception as e:
                result["download_error"] = str(e)
    
    return result

def download_image(url: str) -> str:
    """下载图片到本地 /tmp/ 目录"""
    resp = requests.get(url, timeout=60, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    resp.raise_for_status()
    
    # 从 URL 推断扩展名
    if ".png" in url.lower():
        ext = "png"
    elif ".gif" in url.lower():
        ext = "gif"
    elif ".webp" in url.lower():
        ext = "webp"
    else:
        ext = "jpg"
    
    local_path = f"/tmp/aiping_img_{os.getpid()}_{int(time.time())}.{ext}"
    with open(local_path, "wb") as f:
        f.write(resp.content)
    
    return local_path

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print(f"用法: python3 generate_image.py <prompt> [model] [negative_prompt] [image_url] [aspect_ratio] [nodownload]")
        print(f"默认模型: {DEFAULT_MODEL}")
        sys.exit(1)
    
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else ""
    negative = sys.argv[3] if len(sys.argv) > 3 else ""
    image_url = sys.argv[4] if len(sys.argv) > 4 else ""
    aspect = sys.argv[5] if len(sys.argv) > 5 else ""
    download = "nodownload" not in sys.argv
    
    result = generate_image(model, prompt, negative, image_url, aspect, download=download)
    print(json.dumps(result, ensure_ascii=False, indent=2))
