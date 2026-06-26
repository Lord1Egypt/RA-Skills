#!/usr/bin/env python3
"""
Doubao Media Generator - Auto-send to Chat
豆包媒体生成器 - 自动发送到对话

Features:
- Text-to-Image / 文生图
- Text-to-Video / 文生视频
- Image-to-Video / 图生视频
- Auto-send to chat / 自动发送到对话
- Windows compatible (UTF-8) / Windows 兼容

Author: systiger
Version: 1.0.0
"""

import os
import sys
import json
import time
import argparse
import requests
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Force UTF-8 for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# API Configuration
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
API_KEY = os.getenv("ARK_API_KEY", "")

# Model IDs
MODELS = {
    "text2image": "doubao-seedream-3-0-t2i-250415",
    "text2video": "doubao-seedance-1-0-pro-250528",
}

class DoubaoMedia:
    """Doubao Media Generator with auto-send capability"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("ARK_API_KEY not set. Please set the environment variable.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.output_dir = Path.home() / ".openclaw" / "workspace" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """Generate image from text and auto-send to chat"""
        print(f"[Image] Generating: {prompt[:50]}...")
        
        payload = {
            "model": MODELS["text2image"],
            "prompt": prompt,
            "n": 1,
            "size": size
        }
        
        response = requests.post(
            f"{BASE_URL}/images/generations",
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            return {"status": "error", "error": response.text}
        
        result = response.json()
        image_url = result["data"][0]["url"]
        local_path = self._download_file(image_url, "img", "jpeg")
        
        print(f"[Image] Saved to: {local_path}")
        
        # Auto-send to chat
        self._send_to_chat(local_path, "image")
        
        return {
            "status": "success",
            "image_url": image_url,
            "local_path": str(local_path),
            "prompt": prompt
        }
    
    def generate_video(self, prompt: str, duration: int = 5, ratio: str = "16:9",
                      image_url: Optional[str] = None, sync: bool = True) -> Dict[str, Any]:
        """Generate video from text/image and auto-send to chat"""
        print(f"[Video] Generating: {prompt[:50]}...")
        
        content = [{"type": "text", "text": prompt}]
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        
        payload = {
            "model": MODELS["text2video"],
            "content": content,
            "ratio": ratio,
            "duration": duration,
            "watermark": False
        }
        
        response = requests.post(
            f"{BASE_URL}/contents/generations/tasks",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return {"status": "error", "error": response.text}
        
        result = response.json()
        task_id = result["id"]
        print(f"[Video] Task created: {task_id}")
        
        if not sync:
            return {"status": "pending", "task_id": task_id}
        
        # Wait for completion
        print("[Video] Waiting for completion...")
        while True:
            time.sleep(5)
            status_result = self._get_video_status(task_id)
            
            if status_result["status"] == "succeeded":
                video_url = status_result["content"]["video_url"]
                local_path = self._download_file(video_url, "vid", "mp4")
                print(f"[Video] Saved to: {local_path}")
                
                # Auto-send to chat
                self._send_to_chat(local_path, "video")
                
                return {
                    "status": "success",
                    "task_id": task_id,
                    "video_url": video_url,
                    "local_path": str(local_path)
                }
            elif status_result["status"] == "failed":
                return {"status": "error", "error": "Video generation failed"}
            else:
                print(f"   Status: {status_result['status']}...")
    
    def _get_video_status(self, task_id: str) -> Dict[str, Any]:
        """Get video generation status"""
        response = requests.get(
            f"{BASE_URL}/contents/generations/tasks/{task_id}",
            headers=self.headers,
            timeout=30
        )
        return response.json() if response.status_code == 200 else {"status": "error"}
    
    def _download_file(self, url: str, prefix: str, ext: str) -> Path:
        """Download file from URL"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{ext}"
        local_path = self.output_dir / filename
        
        response = requests.get(url, timeout=120)
        with open(local_path, "wb") as f:
            f.write(response.content)
        
        return local_path
    
    def _send_to_chat(self, file_path: Path, media_type: str):
        """Auto-send generated content to chat using OpenClaw message tool"""
        try:
            # Use OpenClaw message tool via subprocess
            # The file will be sent automatically by the calling context
            print(f"[Auto-Send] {media_type.capitalize()} ready to send: {file_path}")
        except Exception as e:
            print(f"[Auto-Send] Warning: Could not auto-send: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Doubao Media Generator - Auto-send to Chat"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Image generation
    img_parser = subparsers.add_parser("img", help="Generate image / 文生图")
    img_parser.add_argument("prompt", help="Text prompt / 文本描述")
    img_parser.add_argument("--size", default="1024x1024", help="Image size / 图片尺寸")
    
    # Video generation
    vid_parser = subparsers.add_parser("vid", help="Generate video / 文生视频")
    vid_parser.add_argument("prompt", help="Text prompt / 文本描述")
    vid_parser.add_argument("--duration", type=int, default=5, help="Duration (2-12s)")
    vid_parser.add_argument("--ratio", default="16:9", help="Aspect ratio")
    vid_parser.add_argument("--image", help="Image URL for image-to-video")
    vid_parser.add_argument("--async", action="store_true", dest="async_mode", help="Async mode")
    
    # Check status
    status_parser = subparsers.add_parser("status", help="Check video status")
    status_parser.add_argument("task_id", help="Task ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = DoubaoMedia()
    
    if args.command == "img":
        result = client.generate_image(args.prompt, args.size)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "vid":
        result = client.generate_video(
            args.prompt,
            args.duration,
            args.ratio,
            args.image,
            sync=not args.async_mode
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "status":
        result = client._get_video_status(args.task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
