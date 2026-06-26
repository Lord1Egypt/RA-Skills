"""
豆包图片生成脚本
使用火山引擎豆包模型生成图片
支持多模型自动切换
"""

import os
import sys
import time
import json
import requests
import argparse

# 环境变量名
API_KEY_ENV = "VOLCENGINE_IMAGE_API_KEY"
OUTPUT_DIR_ENV = "DOUBAO_IMAGE_OUTPUT_DIR"

# API 配置
API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

# 支持的模型列表（按优先级排序）
SUPPORTED_MODELS = [
    "doubao-seedream-4-0-250828",  # 默认模型
    "doubao-seedream-4-5-251128",
    "doubao-seedream-5-0-260128",
    "doubao-seedream-3-0-t2i-250415"
]

DEFAULT_SIZE = "1024x1024"

# 支持的尺寸
SUPPORTED_SIZES = [
    "1024x1024",
    "1280x720",
    "720x1280",
    "1024x768",
    "768x1024",
]

def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        sys.stdout.write(f"Error: Please set env var {API_KEY_ENV}\n")
        sys.stdout.write("Get API Key: https://console.volces.com/\n")
        sys.exit(1)
    return api_key

def get_output_dir():
    """获取输出目录"""
    # 优先从环境变量读取，其次使用默认路径
    output_dir = os.environ.get(OUTPUT_DIR_ENV)
    if not output_dir:
        # 尝试从 workspace 获取路径
        workspace = os.environ.get("OPENCLAW_WORKSPACE")
        if workspace:
            output_dir = os.path.join(workspace, "downloads", "images")
        else:
            # 默认路径
            output_dir = "C:/Users/zcf/.openclaw/workspace/downloads/images"
    return output_dir

def generate_image(prompt, model=None, size=DEFAULT_SIZE, num=1):
    """生成图片（支持多模型自动切换）"""
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 确定要尝试的模型列表
    if model:
        models_to_try = [model] + [m for m in SUPPORTED_MODELS if m != model]
    else:
        models_to_try = SUPPORTED_MODELS.copy()
    
    payload = {
        "prompt": prompt,
        "size": size,
        "n": num
    }
    
    last_error = None
    
    for attempt_model in models_to_try:
        payload["model"] = attempt_model
        sys.stdout.write(f"Trying model: {attempt_model}\n")
        sys.stdout.flush()
        
        try:
            response = requests.post(API_BASE_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # 检查是否有图片 URL
                if "data" in result and len(result.get("data", [])) > 0:
                    img_url = result["data"][0].get("url")
                    sys.stdout.write(f"[OK] Model {attempt_model} success\n")
                    sys.stdout.flush()
                    return {
                        "url": img_url,
                        "model": attempt_model,
                        "size": size,
                        "prompt": prompt
                    }
                elif "error" in result:
                    error_msg = result["error"].get("message", "Unknown error")
                    sys.stdout.write(f"[X] Model {attempt_model} error: {error_msg}\n")
                    sys.stdout.flush()
                    last_error = error_msg
                    # 如果是模型不支持的错误，继续尝试下一个模型
                    if "not support" in error_msg.lower() or "invalid model" in error_msg.lower():
                        continue
                    break
                else:
                    sys.stdout.write(f"[X] Model {attempt_model} unknown response\n")
                    sys.stdout.flush()
                    last_error = str(result)
            else:
                error_msg = f"HTTP {response.status_code}"
                sys.stdout.write(f"[X] Model {attempt_model} {error_msg}\n")
                sys.stdout.flush()
                last_error = error_msg
                
        except requests.exceptions.Timeout:
            sys.stdout.write(f"[X] Model {attempt_model} timeout\n")
            sys.stdout.flush()
            last_error = "timeout"
            continue
        except Exception as e:
            sys.stdout.write(f"[X] Model {attempt_model} exception: {str(e)}\n")
            sys.stdout.flush()
            last_error = str(e)
            continue
    
    # 所有模型都失败了
    sys.stdout.write(f"\nError: All models failed, last error: {last_error}\n")
    sys.stdout.flush()
    return None

def download_image(url, save_path):
    """下载图片"""
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            sys.stdout.write(f"Download failed: HTTP {response.status_code}\n")
            return False
    except Exception as e:
        sys.stdout.write(f"Download exception: {str(e)}\n")
        return False

def main():
    parser = argparse.ArgumentParser(description="Doubao Image Generation")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--model", default=None, help=f"Model name (default: {SUPPORTED_MODELS[0]})")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"Image size (default: {DEFAULT_SIZE})")
    parser.add_argument("--num", type=int, default=1, help="Number of images")
    parser.add_argument("--url-only", action="store_true", help="Only return URL, don't download")
    
    args = parser.parse_args()
    
    sys.stdout.write("=" * 50 + "\n")
    sys.stdout.write(f"Prompt: {args.prompt}\n")
    sys.stdout.write(f"Size: {args.size}\n")
    sys.stdout.write(f"Num: {args.num}\n")
    sys.stdout.write("=" * 50 + "\n")
    sys.stdout.flush()
    
    # 生成图片
    result = generate_image(args.prompt, args.model, args.size, args.num)
    
    if not result:
        sys.stdout.write("\nGeneration failed\n")
        sys.exit(1)
    
    # 输出结果
    sys.stdout.write("\n" + "=" * 50 + "\n")
    sys.stdout.write("Success!\n")
    sys.stdout.write(f"Model: {result['model']}\n")
    sys.stdout.write(f"URL: {result['url']}\n")
    sys.stdout.write("=" * 50 + "\n")
    sys.stdout.flush()
    
    # 如果只需要 URL，不下载
    if args.url_only:
        sys.stdout.write(f"\n[URL_ONLY] {result['url']}\n")
        return
    
    # 下载图片
    output_dir = get_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    timestamp = int(time.time())
    filename = f"doubao_{timestamp}.jpeg"
    save_path = os.path.join(output_dir, filename)
    
    sys.stdout.write(f"\nDownloading to: {save_path}\n")
    
    if download_image(result['url'], save_path):
        file_size = os.path.getsize(save_path)
        sys.stdout.write(f"[OK] Saved: {save_path}\n")
        sys.stdout.write(f"  Size: {file_size / 1024:.1f} KB\n")
        sys.stdout.write(f"\n[FILE_PATH] {save_path}\n")
    else:
        sys.stdout.write("[X] Download failed\n")
        sys.stdout.write(f"\nPlease download manually: {result['url']}\n")

if __name__ == "__main__":
    main()
