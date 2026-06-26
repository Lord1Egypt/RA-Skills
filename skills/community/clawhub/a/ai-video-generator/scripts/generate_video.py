#!/usr/bin/env python3
"""
AI Video Generator - 支持 Luma、Runway、Kling 等多个平台
"""

import argparse
import os
import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


def get_timestamp():
    """生成时间戳字符串"""
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def get_api_key(platform, args_key):
    """获取 API Key"""
    if args_key:
        return args_key
    
    env_vars = {
        'luma': 'LUMA_API_KEY',
        'runway': 'RUNWAY_API_KEY',
        'kling': 'KLING_API_KEY'
    }
    
    env_var = env_vars.get(platform.lower())
    if env_var:
        return os.environ.get(env_var)
    
    return None


def generate_luma(prompt, filename, duration=5, api_key=None, input_image=None):
    """使用 Luma Dream Machine 生成视频"""
    if not api_key:
        print("Error: LUMA_API_KEY not provided")
        print("Set environment variable LUMA_API_KEY or use --api-key")
        sys.exit(1)
    
    print(f"🎬 开始生成 Luma 视频...")
    print(f"   Prompt: {prompt}")
    print(f"   Duration: {duration}s")
    if input_image:
        print(f"   Input Image: {input_image}")
    
    # Luma API 端点
    url = "https://api.lumalabs.ai/dream-machine/v1/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "duration": duration
    }
    
    if input_image:
        # 读取图片并转为 base64
        with open(input_image, "rb") as f:
            import base64
            image_base64 = base64.b64encode(f.read()).decode()
            data["image"] = f"data:image/png;base64,{image_base64}"
    
    try:
        # 创建生成任务
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            generation_id = result.get("id")
            
        if not generation_id:
            print("Error: Failed to create generation task")
            sys.exit(1)
        
        print(f"   Task ID: {generation_id}")
        print("   等待视频生成完成...")
        
        # 轮询检查状态
        max_wait = 300  # 最多等 5 分钟
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)
            
            status_url = f"{url}/{generation_id}"
            status_req = urllib.request.Request(status_url, headers=headers)
            
            with urllib.request.urlopen(status_req, timeout=30) as resp:
                status_result = json.loads(resp.read().decode())
                state = status_result.get("state", "pending")
            
            print(f"   状态：{state}")
            
            if state == "completed":
                video_url = status_result.get("video", {}).get("url")
                if video_url:
                    # 下载视频
                    print(f"   下载视频：{video_url}")
                    urllib.request.urlretrieve(video_url, filename)
                    print(f"✅ 视频已保存：{os.path.abspath(filename)}")
                    return True
            elif state == "failed":
                print("Error: Generation failed")
                sys.exit(1)
        
        print("Error: Generation timeout")
        sys.exit(1)
        
    except urllib.error.HTTPError as e:
        print(f"Error: API request failed - {e.code}")
        try:
            error_body = json.loads(e.read().decode())
            print(f"   {error_body}")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def generate_runway(prompt, filename, api_key=None, input_image=None):
    """使用 Runway ML 生成视频"""
    if not api_key:
        print("Error: RUNWAY_API_KEY not provided")
        print("Set environment variable RUNWAY_API_KEY or use --api-key")
        sys.exit(1)
    
    print(f"🎬 开始生成 Runway 视频...")
    print(f"   Prompt: {prompt}")
    
    # Runway Gen-2 API
    url = "https://api.runwayml.com/v1/generations/video"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "model": "gen2"
    }
    
    if input_image:
        with open(input_image, "rb") as f:
            import base64
            image_base64 = base64.b64encode(f.read()).decode()
            data["image"] = f"data:image/png;base64,{image_base64}"
    
    try:
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            generation_id = result.get("id")
        
        print(f"   Task ID: {generation_id}")
        print("   等待视频生成完成...")
        
        # 轮询
        max_wait = 300
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)
            
            status_url = f"{url}/{generation_id}"
            status_req = urllib.request.Request(status_url, headers=headers)
            
            with urllib.request.urlopen(status_req, timeout=30) as resp:
                status_result = json.loads(resp.read().decode())
                state = status_result.get("state", "pending")
            
            print(f"   状态：{state}")
            
            if state == "completed":
                video_url = status_result.get("video_url")
                if video_url:
                    urllib.request.urlretrieve(video_url, filename)
                    print(f"✅ 视频已保存：{os.path.abspath(filename)}")
                    return True
            elif state == "failed":
                print("Error: Generation failed")
                sys.exit(1)
        
        print("Error: Generation timeout")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def generate_kling(prompt, filename, api_key=None, input_image=None):
    """使用 Kling AI（可灵）生成视频"""
    if not api_key:
        print("Error: KLING_API_KEY not provided")
        print("Set environment variable KLING_API_KEY or use --api-key")
        sys.exit(1)
    
    print(f"🎬 开始生成 Kling（可灵）视频...")
    print(f"   Prompt: {prompt}")
    
    # Kling API (示例端点，实际需根据官方文档调整)
    url = "https://api.klingai.com/v1/videos"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "duration": 5
    }
    
    if input_image:
        data["image_url"] = input_image  # Kling 支持图片 URL
    
    try:
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            generation_id = result.get("id")
        
        print(f"   Task ID: {generation_id}")
        print("   等待视频生成完成...")
        
        # 轮询
        max_wait = 300
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(5)
            
            status_url = f"{url}/{generation_id}"
            status_req = urllib.request.Request(status_url, headers=headers)
            
            with urllib.request.urlopen(status_req, timeout=30) as resp:
                status_result = json.loads(resp.read().decode())
                state = status_result.get("state", "pending")
            
            print(f"   状态：{state}")
            
            if state == "completed":
                video_url = status_result.get("video_url")
                if video_url:
                    urllib.request.urlretrieve(video_url, filename)
                    print(f"✅ 视频已保存：{os.path.abspath(filename)}")
                    return True
            elif state == "failed":
                print("Error: Generation failed")
                sys.exit(1)
        
        print("Error: Generation timeout")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="AI Video Generator")
    parser.add_argument("--platform", required=True, choices=["luma", "runway", "kling"],
                        help="视频生成平台")
    parser.add_argument("--prompt", required=True, help="视频描述 prompt")
    parser.add_argument("--filename", required=True, help="输出文件名")
    parser.add_argument("--duration", type=int, default=5, choices=[5, 10],
                        help="视频时长（秒）")
    parser.add_argument("--input-image", help="输入图片路径（图生视频）")
    parser.add_argument("--api-key", help="API Key（也可通过环境变量设置）")
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = get_api_key(args.platform, args.api_key)
    
    # 生成描述性文件名
    if args.filename:
        filename = args.filename
    else:
        desc = args.prompt.lower().replace(" ", "-")[:30]
        filename = f"{get_timestamp()}-{args.platform}-{desc}.mp4"
    
    # 根据平台调用对应函数
    if args.platform == "luma":
        generate_luma(args.prompt, filename, args.duration, api_key, args.input_image)
    elif args.platform == "runway":
        generate_runway(args.prompt, filename, api_key, args.input_image)
    elif args.platform == "kling":
        generate_kling(args.prompt, filename, api_key, args.input_image)


if __name__ == "__main__":
    main()
