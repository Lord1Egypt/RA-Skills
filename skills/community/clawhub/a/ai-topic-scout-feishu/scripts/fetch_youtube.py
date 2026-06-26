#!/usr/bin/env python3
"""
AI Topic Scout - YouTube 内容抓取工具
使用 yt-dlp 抓取指定频道的最新视频信息
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta

def fetch_youtube_videos(channel_id: str, days: int = 7, max_items: int = 20):
    """
    抓取 YouTube 频道最新视频
    
    Args:
        channel_id: 频道 ID (如 @channelname 或 UCxxxxxx)
        days: 抓取最近 N 天的视频
        max_items: 最多抓取数量
    
    Returns:
        List of video dicts with: title, url, views, published_date, description
    """
    
    # 计算日期过滤
    date_after = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
    
    # yt-dlp 命令
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", '{"title": "%(title)s", "url": "%(url)s", "views": %(view_count)s, "published": "%(upload_date)s", "description": "%(description)s"}',
        "--dateafter", date_after,
        "--playlist-end", str(max_items),
        f"https://www.youtube.com/{channel_id}/videos"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=60
        )
        
        videos = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    video = json.loads(line)
                    # 转换日期格式
                    pub_date = video["published"]
                    video["published_date"] = f"{pub_date[:4]}-{pub_date[4:6]}-{pub_date[6:]}"
                    videos.append(video)
                except json.JSONDecodeError:
                    continue
        
        return videos
    
    except subprocess.TimeoutExpired:
        print(f"Error: Timeout fetching {channel_id}", file=sys.stderr)
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error: yt-dlp failed for {channel_id}: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Error: yt-dlp not installed. Run: pip install yt-dlp", file=sys.stderr)
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_youtube.py <channel_id> [days] [max_items]")
        sys.exit(1)
    
    channel_id = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    max_items = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    
    videos = fetch_youtube_videos(channel_id, days, max_items)
    print(json.dumps(videos, ensure_ascii=False, indent=2))
