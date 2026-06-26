#!/usr/bin/env python3
"""
抖音视频下载脚本
支持：
  - 短链接: https://v.douyin.com/xxxxx/
  - 分享文本（含短链）
  - 视频直链: https://www.douyin.com/video/1234567890

用法:
  python3 douyin_download.py <链接或分享文本> [输出文件名]

示例:
  python3 douyin_download.py "https://v.douyin.com/FKWYQmtQ79E/"
  python3 douyin_download.py "7.15 复制打开抖音... https://v.douyin.com/FKWYQmtQ79E/" my_video.mp4
"""

import sys
import re
import json
import urllib.request
import urllib.error
import os

MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"


def extract_url(text: str) -> str:
    """从分享文本中提取第一个 URL"""
    m = re.search(r'https?://[^\s]+', text)
    if not m:
        raise ValueError("未找到有效链接")
    return m.group(0)


def resolve_short_url(url: str) -> str:
    """跟随重定向，拿到最终 URL"""
    req = urllib.request.Request(url, headers={"User-Agent": MOBILE_UA})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.url
    except urllib.error.HTTPError as e:
        return e.url or url


def extract_video_id(url: str) -> str:
    """从 URL 中提取 video ID"""
    m = re.search(r'/video/(\d+)', url)
    if not m:
        raise ValueError(f"无法从 URL 提取 video ID: {url}")
    return m.group(1)


def get_play_uri(video_id: str) -> tuple[str, str]:
    """
    访问分享页，从 _ROUTER_DATA 中提取播放 URI 和视频标题
    返回 (uri, title)
    """
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}/"
    req = urllib.request.Request(share_url, headers={
        "User-Agent": MOBILE_UA,
        "Referer": "https://www.douyin.com/",
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode("utf-8", errors="ignore")

    # 提取 _ROUTER_DATA JSON
    m = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.+?\})\s*</script>', html, re.DOTALL)
    if not m:
        raise ValueError("页面中未找到 _ROUTER_DATA，可能需要登录")

    data = json.loads(m.group(1))

    def find_item_list(obj, depth=0):
        if depth > 10:
            return None
        if isinstance(obj, dict):
            if 'item_list' in obj:
                return obj['item_list']
            for v in obj.values():
                r = find_item_list(v, depth + 1)
                if r:
                    return r
        elif isinstance(obj, list):
            for item in obj:
                r = find_item_list(item, depth + 1)
                if r:
                    return r
        return None

    items = find_item_list(data)
    if not items:
        raise ValueError("未找到视频信息")

    item = items[0]
    title = item.get('desc', video_id)[:50]  # 截断避免文件名过长
    aweme_type = item.get('aweme_type')

    video = item.get('video', {})
    play_addr = video.get('play_addr', {})
    uri = play_addr.get('uri', '')

    if not uri:
        raise ValueError(f"未找到播放地址（aweme_type={aweme_type}，可能是图文笔记）")

    # 如果 uri 已经是完整 URL，直接返回；否则拼接
    if uri.startswith('http'):
        return uri, title
    return uri, title


def download_video(uri: str, output_path: str):
    """下载视频到本地文件"""
    # uri 可能是完整 URL，也可能是 video_id 字符串
    if uri.startswith('http'):
        play_url = uri
    else:
        play_url = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={uri}&ratio=720p&line=0"

    print(f"下载地址: {play_url}")
    req = urllib.request.Request(play_url, headers={"User-Agent": MOBILE_UA})

    with urllib.request.urlopen(req, timeout=60) as resp, open(output_path, 'wb') as f:
        total = int(resp.headers.get('Content-Length', 0))
        downloaded = 0
        chunk = 64 * 1024
        while True:
            data = resp.read(chunk)
            if not data:
                break
            f.write(data)
            downloaded += len(data)
            if total:
                pct = downloaded / total * 100
                print(f"\r  进度: {pct:.1f}% ({downloaded // 1024 // 1024}MB / {total // 1024 // 1024}MB)", end='', flush=True)
        print()


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = name.strip()
    return name or "video"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_text = sys.argv[1]
    output_arg = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"[1/4] 提取链接...")
    url = extract_url(input_text)
    print(f"  URL: {url}")

    # 如果是短链，先展开
    if 'v.douyin.com' in url or len(url) < 50:
        print(f"[2/4] 解析短链...")
        url = resolve_short_url(url)
        print(f"  展开: {url}")
    else:
        print(f"[2/4] 跳过短链解析")

    print(f"[3/4] 提取视频 ID 和播放地址...")
    video_id = extract_video_id(url)
    print(f"  Video ID: {video_id}")

    uri, title = get_play_uri(video_id)
    print(f"  标题: {title}")
    print(f"  URI: {uri[:80]}...")

    # 确定输出路径
    if output_arg:
        output_path = output_arg
    else:
        safe_title = sanitize_filename(title)
        output_path = f"{safe_title}.mp4"

    print(f"[4/4] 下载视频 → {output_path}")
    download_video(uri, output_path)

    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"\n✅ 完成！文件: {output_path} ({size_mb:.1f}MB)")


if __name__ == '__main__':
    main()
