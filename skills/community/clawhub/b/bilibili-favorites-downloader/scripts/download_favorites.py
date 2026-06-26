#!/usr/bin/env python3
"""
Bilibili 收藏夹视频下载脚本
- 从收藏夹API获取所有视频（支持分页）
- 下载小于指定大小的视频
- 使用最高可用清晰度
- 支持断点续传
"""

import subprocess
import json
import os
import sys
import time
import re
import argparse
from pathlib import Path
import urllib.request
import urllib.parse


def get_favorite_videos(fid, pn=1, ps=20):
    """
    从Bilibili API获取收藏夹视频列表
    fid: 收藏夹ID
    pn: 页码
    ps: 每页数量
    """
    url = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={fid}&pn={pn}&ps={ps}&keyword=&order=mtime&type=0&tid=0&platform=web"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://space.bilibili.com/'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('code') == 0:
                return data.get('data', {})
    except Exception as e:
        print(f"获取收藏夹视频失败: {e}")
    
    return None


def get_all_favorite_videos(fid):
    """获取收藏夹中的所有视频"""
    all_videos = []
    pn = 1
    ps = 20  # 每页20个
    
    print(f"正在获取收藏夹 {fid} 的所有视频...")
    
    while True:
        data = get_favorite_videos(fid, pn, ps)
        if not data:
            break
        
        medias = data.get('medias', [])
        if not medias:
            break
        
        for media in medias:
            title = media.get('title', '')
            bvid = media.get('bvid', '')
            duration = media.get('duration', 0)  # 秒
            
            if title and bvid:
                all_videos.append({
                    'title': title,
                    'bvid': bvid,
                    'duration': duration
                })
        
        # 检查是否还有下一页
        info = data.get('info', {})
        total = info.get('media_count', 0)
        has_more = data.get('has_more', False)
        
        print(f"  第 {pn} 页: 获取 {len(medias)} 个视频，总计 {len(all_videos)}/{total}")
        
        # 使用 has_more 字段判断是否还有更多页面
        if not has_more:
            print(f"  API 返回 has_more=False，停止获取")
            break
        
        pn += 1
        time.sleep(0.5)  # 避免请求过快
    
    return all_videos


def get_video_info(bvid):
    """获取视频信息，包括文件大小和可用格式"""
    url = f"https://www.bilibili.com/video/{bvid}"
    
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-playlist",
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return info
    except Exception as e:
        print(f"获取视频信息失败 {bvid}: {e}")
    
    return None


def estimate_size_mb(info):
    """估算视频大小（MB）"""
    if not info:
        return float('inf')
    
    filesize = info.get('filesize') or info.get('filesize_approx')
    if filesize:
        return filesize / (1024 * 1024)
    
    duration = info.get('duration', 0)
    estimated_size = (duration * 2000) / 8 / 1024
    
    return estimated_size


def clean_filename(title):
    """清理文件名中的非法字符"""
    cleaned = re.sub(r'[<>:"/\\|?*]', '', title)
    cleaned = cleaned.replace(' ', '_')
    cleaned = cleaned[:80]  # 限制长度
    return cleaned


def download_video(title, bvid, output_dir, max_size_mb):
    """下载单个视频，使用最高可用清晰度"""
    url = f"https://www.bilibili.com/video/{bvid}"
    
    safe_title = clean_filename(title)
    output_template = str(output_dir / f"{safe_title}_{bvid}.%(ext)s")
    
    # 检查是否已存在
    existing_files = list(output_dir.glob(f"{safe_title}_{bvid}.*"))
    if existing_files:
        print(f"   ⏭️ 已存在，跳过: {title}")
        return True, "existed"
    
    # 获取视频信息并检查大小
    info = get_video_info(bvid)
    if info:
        size_mb = estimate_size_mb(info)
        if size_mb > max_size_mb:
            print(f"   ⚠️ 跳过: 文件过大 ({size_mb:.2f} MB > {max_size_mb} MB)")
            return False, "too_large"
    
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", "bestvideo*+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--no-warnings",
        url
    ]
    
    print(f"\n正在下载: {title}")
    print(f"BV号: {bvid}")
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ 下载成功: {title}")
            return True, "downloaded"
        else:
            print(f"❌ 下载失败: {title}")
            return False, "failed"
    except Exception as e:
        print(f"❌ 下载出错 {title}: {e}")
        return False, "error"


def parse_fav_url(url):
    """从收藏夹URL解析fid和mid"""
    # 匹配 https://space.bilibili.com/{mid}/favlist?fid={fid}
    pattern = r'space\.bilibili\.com/(\d+)/favlist.*fid=(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(2), match.group(1)  # fid, mid
    return None, None


def main():
    parser = argparse.ArgumentParser(description='下载 Bilibili 收藏夹视频')
    parser.add_argument('--url', '-u', help='收藏夹URL')
    parser.add_argument('--fid', '-f', help='收藏夹ID')
    parser.add_argument('--mid', '-m', help='用户ID')
    parser.add_argument('--max-size', '-s', type=int, default=500, help='最大文件大小(MB)，默认500')
    parser.add_argument('--output', '-o', help='下载目录，默认 ~/Downloads/bilibili_favorites/')
    parser.add_argument('--list-only', action='store_true', help='仅获取视频列表，不下载视频')
    parser.add_argument('--max-download', '-n', type=int, default=None, help='最大下载视频数量，默认无限制')

    args = parser.parse_args()
    
    # 获取收藏夹ID
    fid = args.fid
    if args.url:
        fid, mid = parse_fav_url(args.url)
        if not fid:
            print("无法从URL解析收藏夹ID")
            return
    
    if not fid:
        print("请提供收藏夹URL或收藏夹ID")
        parser.print_help()
        return
    
    # 设置下载目录
    if args.output:
        download_dir = Path(args.output)
    else:
        download_dir = Path.home() / "Downloads" / "bilibili_favorites"
    
    download_dir.mkdir(parents=True, exist_ok=True)
    max_size_mb = args.max_size
    
    print("=" * 70)
    print("Bilibili 收藏夹视频下载工具")
    print("=" * 70)
    print(f"收藏夹ID: {fid}")

    if args.list_only:
        print("模式: 仅获取视频列表")
    else:
        print(f"下载目录: {download_dir}")
        print(f"大小限制: {max_size_mb} MB")
        if args.max_download:
            print(f"最大下载数量: {args.max_download}")
    print("=" * 70)

    # 获取所有视频
    videos = get_all_favorite_videos(fid)

    if not videos:
        print("未获取到任何视频，请检查收藏夹ID是否正确")
        return

    print(f"\n共获取到 {len(videos)} 个视频")
    print("=" * 70)

    # 如果指定了 --list-only，仅打印列表并退出
    if args.list_only:
        print("\n视频列表:")
        for i, video in enumerate(videos, 1):
            duration_min = video['duration'] // 60
            duration_sec = video['duration'] % 60
            print(f"{i}. {video['title']}")
            print(f"   BV号: {video['bvid']}, 时长: {duration_min}分{duration_sec}秒")
        print(f"\n共 {len(videos)} 个视频")
        return

    # 限制下载数量
    videos_to_download = videos
    if args.max_download and args.max_download < len(videos):
        videos_to_download = videos[:args.max_download]
        print(f"\n将下载前 {args.max_download} 个视频（共 {len(videos)} 个）")
    print("=" * 70)

    downloaded = []
    skipped = []
    failed = []
    existed = []

    for i, video in enumerate(videos_to_download, 1):
        title = video['title']
        bvid = video['bvid']

        print(f"\n[{i}/{len(videos_to_download)}] 处理: {title}")

        success, status = download_video(title, bvid, download_dir, max_size_mb)

        if status == "downloaded":
            downloaded.append((title, bvid))
        elif status == "existed":
            existed.append((title, bvid))
        elif status == "too_large":
            skipped.append((title, bvid))
        else:
            failed.append((title, bvid))

        # 短暂休息，避免请求过快
        time.sleep(1)

    # 打印总结
    print("\n" + "=" * 70)
    print("下载完成总结")
    print("=" * 70)
    print(f"✅ 成功下载: {len(downloaded)} 个")
    print(f"⏭️ 已存在: {len(existed)} 个")
    print(f"⚠️ 跳过 (大于 {max_size_mb}MB): {len(skipped)} 个")
    print(f"❌ 下载失败: {len(failed)} 个")

    if skipped:
        print("\n跳过的视频 (文件过大):")
        for title, bvid in skipped[:10]:
            print(f"  - {title[:50]}...")
        if len(skipped) > 10:
            print(f"  ... 还有 {len(skipped) - 10} 个")

    if failed:
        print("\n下载失败的视频:")
        for title, bvid in failed:
            print(f"  - {title[:50]}...")

    print(f"\n下载目录: {download_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
