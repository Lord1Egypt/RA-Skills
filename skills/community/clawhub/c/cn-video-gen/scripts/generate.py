#!/usr/bin/env python3
"""
国产AI视频生成脚本
支持：通义万相（Wan2.6 T2V/I2V）
用法：
  python3 generate.py --prompt "描述文字" [--duration 5] [--size 1280*720] [--mode t2v|i2v] [--image_url URL]
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"


def create_t2v_task(prompt, duration=5, size="1280*720", multi_shot=False, audio_url=None):
    """创建文生视频任务"""
    url = f"{BASE_URL}/services/aigc/video-generation/video-synthesis"
    
    payload = {
        "model": "wan2.6-t2v",
        "input": {"prompt": prompt},
        "parameters": {
            "size": size,
            "duration": duration,
            "prompt_extend": True,
            "shot_type": "multi" if multi_shot else "single"
        }
    }
    
    if audio_url:
        payload["input"]["audio_url"] = audio_url
    
    return _post(url, payload, async_mode=True)


def create_i2v_task(image_url, prompt="", duration=5, size="1280*720"):
    """创建图生视频任务"""
    url = f"{BASE_URL}/services/aigc/video-generation/video-synthesis"
    
    payload = {
        "model": "wan2.6-i2v",
        "input": {
            "image_url": image_url,
            "prompt": prompt
        },
        "parameters": {
            "size": size,
            "duration": duration,
            "prompt_extend": True
        }
    }
    
    return _post(url, payload, async_mode=True)


def poll_task(task_id, max_wait=600, interval=10):
    """轮询任务状态，直到完成或超时"""
    url = f"{BASE_URL}/tasks/{task_id}"
    elapsed = 0
    
    print(f"⏳ 任务提交成功，task_id: {task_id}")
    print(f"   预计等待 1-5 分钟...")
    
    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        
        result = _get(url)
        status = result.get("output", {}).get("task_status", "UNKNOWN")
        
        print(f"   [{elapsed}s] 状态: {status}")
        
        if status == "SUCCEEDED":
            video_url = result["output"].get("video_url", "")
            print(f"\n✅ 生成成功！")
            print(f"🎬 视频URL: {video_url}")
            return video_url
        elif status == "FAILED":
            msg = result.get("output", {}).get("message", "未知错误")
            print(f"\n❌ 生成失败: {msg}")
            return None
    
    print(f"\n⚠️ 超时（{max_wait}秒），任务仍在进行中")
    print(f"   可手动查询：GET {url}")
    return None


def download_video(video_url, output_path=None):
    """下载视频到本地"""
    if not output_path:
        timestamp = int(time.time())
        output_path = f"/tmp/video_{timestamp}.mp4"
    
    print(f"📥 下载视频到: {output_path}")
    urllib.request.urlretrieve(video_url, output_path)
    print(f"✅ 下载完成: {output_path}")
    return output_path


def _post(url, payload, async_mode=False):
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    if async_mode:
        headers["X-DashScope-Async"] = "enable"
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP错误 {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def _get(url):
    headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP错误 {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="通义万相视频生成")
    parser.add_argument("--prompt", required=True, help="描述文字")
    parser.add_argument("--mode", choices=["t2v", "i2v"], default="t2v", help="t2v=文生视频, i2v=图生视频")
    parser.add_argument("--image_url", help="图生视频时的参考图URL（需HTTP链接）")
    parser.add_argument("--duration", type=int, default=5, choices=[5, 10, 15], help="时长（秒）")
    parser.add_argument("--size", default="1280*720", choices=["1280*720", "1920*1080", "720*1280"], help="分辨率")
    parser.add_argument("--multi_shot", action="store_true", help="多镜头模式（分镜师专用）")
    parser.add_argument("--audio_url", help="自定义音频URL")
    parser.add_argument("--output", help="下载路径（不指定则只显示URL）")
    parser.add_argument("--task_id", help="直接查询已有任务状态")
    
    args = parser.parse_args()
    
    if not DASHSCOPE_API_KEY:
        print("❌ 请设置环境变量 DASHSCOPE_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    # 直接查询已有任务
    if args.task_id:
        video_url = poll_task(args.task_id, max_wait=1, interval=1)
        if video_url and args.output:
            download_video(video_url, args.output)
        return
    
    # 创建新任务
    if args.mode == "t2v":
        print(f"🎬 文生视频: {args.prompt[:50]}...")
        result = create_t2v_task(
            args.prompt,
            duration=args.duration,
            size=args.size,
            multi_shot=args.multi_shot,
            audio_url=args.audio_url
        )
    else:
        if not args.image_url:
            print("❌ 图生视频模式需要 --image_url 参数", file=sys.stderr)
            sys.exit(1)
        print(f"🖼️ 图生视频: {args.image_url}")
        result = create_i2v_task(
            args.image_url,
            prompt=args.prompt,
            duration=args.duration,
            size=args.size
        )
    
    task_id = result.get("output", {}).get("task_id")
    if not task_id:
        print(f"❌ 任务创建失败: {result}", file=sys.stderr)
        sys.exit(1)
    
    video_url = poll_task(task_id)
    
    if video_url and args.output:
        download_video(video_url, args.output)


if __name__ == "__main__":
    main()
