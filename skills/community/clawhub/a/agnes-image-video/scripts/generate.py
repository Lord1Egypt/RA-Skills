#!/usr/bin/env python3
"""
Agnes Image & Video Generation Helper Script

Usage:
    python generate.py --mode image --prompt "一只可爱的小狗" --size 1024x1024
    python generate.py --mode video --prompt "日落时海滩上的猫散步" --height 768 --width 1152 --num_frames 121 --frame_rate 24

Environment:
    AGNES_API_KEY  - Your Agnes AI API key (required)
"""

import argparse
import httpx
import json
import os
import sys
import time
from pathlib import Path


API_BASE = "https://apihub.agnes-ai.com/v1"


def get_api_key():
    key = os.environ.get("AGNES_API_KEY")
    if not key:
        print("错误: 请设置环境变量 AGNES_API_KEY")
        sys.exit(1)
    return key


def generate_image(api_key, prompt, size="1024x1024", seed=None, image_urls=None):
    """Generate or edit an image."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "agnes-image-2.0-flash",
        "prompt": prompt,
        "size": size,
    }
    if seed is not None:
        payload["seed"] = seed

    # Image-to-image or multi-image composition
    if image_urls:
        payload["tags"] = ["img2img"]
        payload["extra_body"] = {"image": image_urls, "response_format": "url"}

    print(f"正在生成图片... (模型: agnes-image-2.0-flash)")
    resp = httpx.post(f"{API_BASE}/images/generations", headers=headers, json=payload)
    data = resp.json()

    if "data" in data:
        url = data["data"][0]["url"]
        print(f"图片生成成功: {url}")
        return url
    else:
        print(f"生成失败: {json.dumps(data, ensure_ascii=False)}")
        sys.exit(1)


def generate_video(api_key, prompt, height=768, width=1152, num_frames=121,
                   frame_rate=24, negative_prompt=None, image=None, mode=None):
    """Generate a video (async, with polling)."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "agnes-video-v2.0",
        "prompt": prompt,
        "height": height,
        "width": width,
        "num_frames": num_frames,
        "frame_rate": frame_rate,
    }
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if image:
        payload["image"] = image
    if mode:
        payload["mode"] = mode

    # Step 1: Create task
    print(f"正在创建视频任务... (模型: agnes-video-v2.0)")
    create_resp = httpx.post(f"{API_BASE}/videos", headers=headers, json=payload)
    create_data = create_resp.json()

    if "task_id" not in create_data:
        print(f"创建任务失败: {json.dumps(create_data, ensure_ascii=False)}")
        sys.exit(1)

    task_id = create_data["task_id"]
    print(f"任务已创建: {task_id}")

    # Step 2: Poll for result
    print("正在等待视频生成...")
    while True:
        result = httpx.get(
            f"{API_BASE}/videos/{task_id}",
            headers=headers
        )
        data = result.json()
        status = data.get("status")

        if status == "completed":
            video_url = data.get("remixed_from_video_id")
            print(f"视频生成成功: {video_url}")
            return video_url
        elif status == "failed":
            print(f"生成失败: {data.get('error')}")
            sys.exit(1)
        else:
            progress = data.get("progress", "?")
            print(f"  状态: {status}, 进度: {progress}%")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Agnes Image & Video Generation")
    parser.add_argument("--mode", required=True, choices=["image", "video"], help="生成模式")
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--size", default="1024x1024", help="图片尺寸 (仅图片)")
    parser.add_argument("--seed", type=int, default=None, help="随机种子 (仅图片)")
    parser.add_argument("--image-urls", nargs="*", default=None, help="输入图像 URL 列表 (图生图/多图合成)")
    parser.add_argument("--height", type=int, default=768, help="视频高度 (仅视频)")
    parser.add_argument("--width", type=int, default=1152, help="视频宽度 (仅视频)")
    parser.add_argument("--num-frames", type=int, default=121, help="视频帧数 (仅视频, 必须满足 8n+1)")
    parser.add_argument("--frame-rate", type=int, default=24, help="视频帧率 (仅视频)")
    parser.add_argument("--negative-prompt", default=None, help="负向提示词 (仅视频)")
    parser.add_argument("--output-dir", default="generated-media", help="输出目录")

    args = parser.parse_args()

    api_key = get_api_key()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.mode == "image":
        url = generate_image(api_key, args.prompt, args.size, args.seed, args.image_urls)
        # Download the image
        resp = httpx.get(url)
        ext = "jpg" if b"JPEG" in resp.content else "png"
        file_path = output_dir / f"image_{int(time.time())}.{ext}"
        file_path.write_bytes(resp.content)
        print(f"图片已保存: {file_path}")

    elif args.mode == "video":
        video_url = generate_video(
            api_key,
            args.prompt,
            height=args.height,
            width=args.width,
            num_frames=args.num_frames,
            frame_rate=args.frame_rate,
            negative_prompt=args.negative_prompt,
        )
        # Download the video
        print("正在下载视频...")
        resp = httpx.get(video_url)
        file_path = output_dir / f"video_{int(time.time())}.mp4"
        file_path.write_bytes(resp.content)
        print(f"视频已保存: {file_path}")


if __name__ == "__main__":
    main()
