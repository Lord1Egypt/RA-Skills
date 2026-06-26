#!/usr/bin/env python3
"""
Doubao API Toolkit - Python Implementation
豆包 API 工具包 - Python 实现

A cross-platform toolkit for Doubao (Volcengine ARK) API.
支持文生图、图生图、文生视频、视频分析、视觉理解等功能。

Author: OpenClaw User
Version: 1.0.0
"""

import os
import sys
import json
import time
import base64
import requests
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

# API Configuration
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
API_KEY = os.getenv("ARK_API_KEY", "")

# Model IDs / 模型ID
MODELS = {
    "text2image": "doubao-seedream-3-0-t2i-250415",
    "image2image": "doubao-seededit-3-0-i2i-250628",
    "text2video": "doubao-seedance-1-0-pro-250528",
    "image2video": "doubao-seedance-1-0-pro-250528",
    "vision": "doubao-1-5-vision-pro-32k-250115",
    "chat": "doubao-1-5-pro-32k-250115"
}

class DoubaoClient:
    """Doubao API Client / 豆包API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("ARK_API_KEY environment variable not set / ARK_API_KEY 环境变量未设置")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.output_dir = Path.home() / ".openclaw" / "workspace" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1) -> Dict[str, Any]:
        """
        Generate image from text / 文生图
        
        Args:
            prompt: Text description / 文本描述
            size: Image size (1024x1024, 1024x1536, 1536x1024) / 图片尺寸
            n: Number of images / 生成数量
            
        Returns:
            Dict with image_url and local_path / 包含图片链接和本地路径的字典
        """
        print(f"🎨 Generating image / 生成图片: {prompt[:50]}...")
        
        payload = {
            "model": MODELS["text2image"],
            "prompt": prompt,
            "n": n,
            "size": size
        }
        
        response = requests.post(
            f"{BASE_URL}/images/generations",
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result["data"][0]["url"]
            
            # Download image / 下载图片
            local_path = self._download_file(image_url, "img")
            
            return {
                "status": "success",
                "image_url": image_url,
                "local_path": str(local_path),
                "prompt": prompt
            }
        else:
            return {"status": "error", "error": response.text}
    
    def generate_video(self, prompt: str, duration: int = 5, ratio: str = "16:9", 
                      image_url: Optional[str] = None, sync: bool = True) -> Dict[str, Any]:
        """
        Generate video from text or image / 文生视频或图生视频
        
        Args:
            prompt: Text description / 文本描述
            duration: Video duration in seconds (2-12) / 视频时长（秒）
            ratio: Aspect ratio (16:9, 4:3, 1:1, 9:16) / 宽高比
            image_url: Optional image URL for image-to-video / 可选的图片URL（图生视频）
            sync: Wait for completion if True / 是否等待完成
            
        Returns:
            Dict with task info or video URL / 包含任务信息或视频链接的字典
        """
        print(f"🎬 Generating video / 生成视频: {prompt[:50]}...")
        
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
        print(f"📋 Task created / 任务创建成功: {task_id}")
        
        if not sync:
            return {"status": "pending", "task_id": task_id}
        
        # Poll for completion / 轮询等待完成
        print("⏳ Waiting for video generation... / 等待视频生成...")
        while True:
            time.sleep(5)
            status_result = self.get_video_status(task_id)
            
            if status_result["status"] == "succeeded":
                video_url = status_result["content"]["video_url"]
                local_path = self._download_file(video_url, "vid", ext="mp4")
                print(f"✅ Video generated / 视频生成成功!")
                return {
                    "status": "success",
                    "task_id": task_id,
                    "video_url": video_url,
                    "local_path": str(local_path)
                }
            elif status_result["status"] == "failed":
                return {"status": "error", "error": "Video generation failed / 视频生成失败"}
            else:
                print(f"   Status: {status_result['status']}...")
    
    def get_video_status(self, task_id: str) -> Dict[str, Any]:
        """Get video generation status / 获取视频生成状态"""
        response = requests.get(
            f"{BASE_URL}/contents/generations/tasks/{task_id}",
            headers=self.headers,
            timeout=30
        )
        return response.json() if response.status_code == 200 else {"status": "error"}
    
    def analyze_image(self, image_url: str, prompt: str = "描述这张图片") -> str:
        """
        Analyze image content / 分析图片内容
        
        Args:
            image_url: URL of the image / 图片URL
            prompt: Analysis prompt / 分析提示词
            
        Returns:
            Analysis result / 分析结果
        """
        print(f"👁️ Analyzing image / 分析图片...")
        
        payload = {
            "model": MODELS["vision"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 2000
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error / 错误: {response.text}"
    
    def analyze_video(self, video_path: str, prompt: str = "分析这个视频的内容") -> str:
        """
        Analyze video content / 分析视频内容 (本地文件)
        
        Args:
            video_path: Path to local video file / 本地视频文件路径
            prompt: Analysis prompt / 分析提示词
            
        Returns:
            Analysis result / 分析结果
        """
        print(f"🎥 Analyzing video / 分析视频: {video_path}")
        
        # Read and encode video / 读取并编码视频
        with open(video_path, "rb") as f:
            video_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Get MIME type / 获取MIME类型
        ext = Path(video_path).suffix.lower()
        mime_types = {".mp4": "video/mp4", ".mov": "video/quicktime", ".avi": "video/x-msvideo"}
        mime_type = mime_types.get(ext, "video/mp4")
        
        payload = {
            "model": MODELS["vision"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "video_url",
                            "video_url": {
                                "url": f"data:{mime_type};base64,{video_base64}"
                            }
                        },
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 2000
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error / 错误: {response.text}"
    
    def _download_file(self, url: str, prefix: str, ext: str = "jpeg") -> Path:
        """Download file from URL / 从URL下载文件"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{ext}"
        local_path = self.output_dir / filename
        
        response = requests.get(url, timeout=120)
        with open(local_path, "wb") as f:
            f.write(response.content)
        
        return local_path

def main():
    parser = argparse.ArgumentParser(
        description="Doubao API Toolkit / 豆包API工具包",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands / 可用命令")
    
    # Image generation / 图片生成
    img_parser = subparsers.add_parser("img", help="Generate image from text / 文生图")
    img_parser.add_argument("prompt", help="Text prompt / 文本提示词")
    img_parser.add_argument("--size", default="1024x1024", help="Image size / 图片尺寸")
    
    # Video generation / 视频生成
    vid_parser = subparsers.add_parser("vid", help="Generate video from text / 文生视频")
    vid_parser.add_argument("prompt", help="Text prompt / 文本提示词")
    vid_parser.add_argument("--duration", type=int, default=5, help="Duration in seconds / 时长（秒）")
    vid_parser.add_argument("--ratio", default="16:9", help="Aspect ratio / 宽高比")
    vid_parser.add_argument("--image", help="Image URL for image-to-video / 图生视频的图片URL")
    vid_parser.add_argument("--async", action="store_true", dest="async_mode", help="Async mode / 异步模式")
    
    # Image analysis / 图片分析
    analyze_img_parser = subparsers.add_parser("analyze-img", help="Analyze image / 分析图片")
    analyze_img_parser.add_argument("image_url", help="Image URL / 图片URL")
    analyze_img_parser.add_argument("--prompt", default="描述这张图片", help="Analysis prompt / 分析提示词")
    
    # Video analysis / 视频分析
    analyze_vid_parser = subparsers.add_parser("analyze-vid", help="Analyze video / 分析视频")
    analyze_vid_parser.add_argument("video_path", help="Video file path / 视频文件路径")
    analyze_vid_parser.add_argument("--prompt", default="分析这个视频的内容", help="Analysis prompt / 分析提示词")
    
    # Check video status / 检查视频状态
    status_parser = subparsers.add_parser("status", help="Check video status / 检查视频状态")
    status_parser.add_argument("task_id", help="Task ID / 任务ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = DoubaoClient()
    
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
    
    elif args.command == "analyze-img":
        result = client.analyze_image(args.image_url, args.prompt)
        print(result)
    
    elif args.command == "analyze-vid":
        result = client.analyze_video(args.video_path, args.prompt)
        print(result)
    
    elif args.command == "status":
        result = client.get_video_status(args.task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
