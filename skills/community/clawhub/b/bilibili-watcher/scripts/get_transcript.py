#!/usr/bin/env python3
"""
Bilibili Video Transcript Fetcher
获取 B 站视频字幕/转录文本

Usage:
    python get_transcript.py "https://www.bilibili.com/video/BV1xx411c7mD"
"""

import sys
import json
import subprocess
import re
from pathlib import Path

def extract_video_id(url):
    """从 B 站 URL 提取视频 ID"""
    # 支持多种 B 站 URL 格式
    patterns = [
        r'bilibili\.com/video/(BV\w+)',  # BV 号
        r'bilibili\.com/video/av(\d+)',   # av 号
        r'b23\.tv/(\w+)',                  # 短链接
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_transcript(video_url):
    """获取 B 站视频字幕"""
    try:
        # 使用 yt-dlp 获取字幕
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--write-sub',
            '--write-auto-sub',
            '--sub-format', 'json',
            '--sub-lang', 'zh-Hans,zh-CN,zh',
            '--print', 'subtitle',
            video_url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            # 解析字幕数据
            subtitle_data = result.stdout
            
            if subtitle_data:
                try:
                    subtitles = json.loads(subtitle_data)
                    
                    # 提取字幕文本
                    transcript = []
                    for segment in subtitles.get('segments', []):
                        text = segment.get('text', '').strip()
                        if text:
                            transcript.append(text)
                    
                    return '\n'.join(transcript)
                except json.JSONDecodeError:
                    return subtitle_data
            else:
                return "未找到字幕数据"
        else:
            return f"错误：{result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "错误：获取超时"
    except Exception as e:
        return f"错误：{str(e)}"

def get_video_info(video_url):
    """获取视频基本信息"""
    try:
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--print', 'title',
            '--print', 'channel',
            '--print', 'upload_date',
            video_url
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return {
                'title': lines[0] if len(lines) > 0 else '未知',
                'channel': lines[1] if len(lines) > 1 else '未知',
                'upload_date': lines[2] if len(lines) > 2 else '未知'
            }
        else:
            return None
    
    except Exception as e:
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python get_transcript.py <B 站视频 URL>")
        print("示例：python get_transcript.py \"https://www.bilibili.com/video/BV1xx411c7mD\"")
        sys.exit(1)
    
    video_url = sys.argv[1]
    
    # 验证 URL
    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"错误：无效的 B 站 URL: {video_url}")
        print("支持的格式:")
        print("  - https://www.bilibili.com/video/BV1xx411c7mD")
        print("  - https://www.bilibili.com/video/av12345678")
        print("  - https://b23.tv/xxxxxx")
        sys.exit(1)
    
    print(f"正在获取 B 站视频信息...")
    print(f"视频 ID: {video_id}")
    print()
    
    # 获取视频信息
    video_info = get_video_info(video_url)
    if video_info:
        print(f"标题：{video_info['title']}")
        print(f"UP 主：{video_info['channel']}")
        print(f"上传日期：{video_info['upload_date']}")
        print()
    
    # 获取字幕
    print("正在获取字幕...")
    transcript = get_transcript(video_url)
    
    print("\n" + "="*60)
    print("视频字幕内容:")
    print("="*60)
    print(transcript)
    print("="*60)

if __name__ == "__main__":
    main()
