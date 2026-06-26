#!/usr/bin/env python3
"""
抖音视频分析工具
功能：
1. 提取视频元数据（标题、作者、数据）
2. 下载视频封面并分析
3. 提取视频帧并分析画面
4. 获取评论（需要第三方API）
"""

import json
import re
import requests
import base64
import subprocess
import os
from urllib.parse import unquote

def extract_video_id(url):
    """从抖音URL提取视频ID"""
    # 处理短链接
    if 'v.douyin.com' in url:
        resp = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }, allow_redirects=True)
        url = resp.url
    
    # 提取视频ID
    match = re.search(r'video/(\d+)', url)
    if match:
        return match.group(1)
    return None

def fetch_video_info(url):
    """获取视频基础信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    resp = requests.get(url, headers=headers)
    html = resp.text
    
    # 从HTML中提取_ROUTER_DATA
    match = re.search(r'window\._ROUTER_DATA\s*=\s*({.*?})</script>', html)
    if not match:
        match = re.search(r'_ROUTER_DATA\s*=\s*({.*?})</script>', html)
    
    if match:
        data = json.loads(match.group(1))
        
        # 提取视频信息
        video_info = {}
        
        try:
            loader_data = data.get('loaderData', {})
            for key in loader_data:
                if 'videoInfoRes' in loader_data[key]:
                    item = loader_data[key]['videoInfoRes']['item_list'][0]
                    
                    video_info = {
                        'video_id': item.get('aweme_id'),
                        'title': item.get('desc', ''),
                        'author': item.get('author', {}).get('nickname', ''),
                        'author_signature': item.get('author', {}).get('signature', ''),
                        'duration_ms': item.get('video', {}).get('duration', 0),
                        'create_time': item.get('create_time', 0),
                        'statistics': {
                            'digg_count': item.get('statistics', {}).get('digg_count', 0),
                            'comment_count': item.get('statistics', {}).get('comment_count', 0),
                            'share_count': item.get('statistics', {}).get('share_count', 0),
                            'collect_count': item.get('statistics', {}).get('collect_count', 0),
                        },
                        'cover_url': item.get('video', {}).get('cover', {}).get('url_list', [''])[0],
                        'hashtags': [tag.get('hashtag_name', '') for tag in item.get('text_extra', [])],
                        'video_url': item.get('video', {}).get('play_addr', {}).get('url_list', [''])[0],
                    }
                    break
        except Exception as e:
            print(f"解析错误: {e}")
        
        return video_info
    
    return None

def download_cover(cover_url, output_path):
    """下载视频封面"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Referer': 'https://www.douyin.com/'
    }
    
    resp = requests.get(cover_url, headers=headers)
    if resp.status_code == 200 and len(resp.content) > 1000:
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return True
    return False

def analyze_cover_with_api(image_path, api_key=None):
    """使用视觉模型分析封面图片"""
    # 使用 Dashscope 或其他视觉API
    if api_key is None:
        return None
    
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    # 调用视觉模型
    resp = requests.post(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen-vl-max",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "详细分析这张图片：1.画面主体 2.构图特点 3.色调氛围 4.视觉焦点 5.内容类型（实拍/渲染/合成）"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }]
        }
    )
    
    if resp.status_code == 200:
        return resp.json()['choices'][0]['message']['content']
    return None

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python video_analysis.py <douyin_url>")
        return
    
    url = sys.argv[1]
    print(f"分析视频: {url}")
    
    # 获取视频信息
    info = fetch_video_info(url)
    if info:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print("无法获取视频信息")

if __name__ == '__main__':
    main()