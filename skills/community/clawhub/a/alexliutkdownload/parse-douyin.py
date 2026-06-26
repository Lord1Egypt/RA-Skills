#!/usr/bin/env python3
"""
抖音无水印视频解析和下载脚本
使用方法: python3 parse-douyin.py <抖音链接>
"""
import requests
import re
import json
import urllib.request
import urllib.error
import sys
import os

def parse_and_download(url):
    """解析抖音链接并下载无水印视频"""
    
    # 提取视频 ID (支持多种格式)
    patterns = [
        r'video/(\d{19})',
        r'modal_id=(\d{19})',
        r'/(\d{19})',
    ]
    video_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break
    
    if not video_id:
        return None, "无法识别视频 ID"
    
    video_id = match.group(1)
    share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        response = requests.get(share_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        pattern = re.compile(r'window\._ROUTER_DATA\s*=\s*(.*?)</script>', re.DOTALL)
        find_res = pattern.search(response.text)
        
        if not find_res:
            return None, "解析页面失败"
        
        data = json.loads(find_res.group(1).strip())
        
        # 获取视频信息
        video_data = data["loaderData"]["video_(id)/page"]["videoInfoRes"]["item_list"][0]
        video_url = video_data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
        desc = video_data.get("desc", "").strip() or f"douyin_{video_id}"
        desc = re.sub(r'[\\/:*?"<>|]', '_', desc)[:50]
        
        # 下载视频
        output = f"/tmp/douyin_{video_id}.mp4"
        req = urllib.request.Request(video_url, headers={'User-Agent': HEADERS['User-Agent']})
        
        with urllib.request.urlopen(req) as resp, open(output, 'wb') as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
        
        size = os.path.getsize(output)
        
        return {
            "title": desc,
            "video_id": video_id,
            "path": output,
            "size_mb": size / 1024 / 1024,
            "url": url
        }, None
        
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 请提供抖音视频链接")
        print("使用方式: python3 parse-douyin.py <抖音链接>")
        sys.exit(1)
    
    url = sys.argv[1]
    result, error = parse_and_download(url)
    
    if error:
        print(f"❌ 错误: {error}")
        sys.exit(1)
    
    print(f"✅ 标题: {result['title']}")
    print(f"📥 文件: {result['path']}")
    print(f"📦 大小: {result['size_mb']:.1f} MB")
    print(f"PATH: {result['path']}")
