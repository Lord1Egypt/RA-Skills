#!/usr/bin/env python3
"""
video_audio.py - 从视频提取音频（支持B站 + 抖音 + YouTube + 小红书 + 本地文件）

用法:
    python3 video_audio.py <视频链接或本地文件> [输出目录]

支持的链接格式:
    - B站: bilibili.com/video/BVxxx 或 BVxxx
    - 抖音: douyin.com/video/xxx 或 v.douyin.com/xxx
    - YouTube: youtube.com/watch?v=xxx 或 youtu.be/xxx
    - 小红书: xiaohongshu.com/explore/xxx 或 xhslink.com/xxx
    - 本地文件: /path/to/video.mp4

依赖:
    - yt-dlp (brew install yt-dlp)    — 在线视频
    - ffmpeg  (brew install ffmpeg)    — 本地视频

输出:
    下载 m4a 音频文件，输出 JSON 到 stdout（包含音频路径和视频信息）
"""

import sys
import os
import json
import subprocess
import re
import shutil
import urllib.request
from pathlib import Path

# 查找外部工具
YTDLP = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def detect_platform(text: str) -> str:
    """识别链接平台：bilibili / douyin / youtube / xiaohongshu / local_file / unknown"""
    # 先检查是否是本地文件
    expanded = os.path.expanduser(text)
    if os.path.isfile(expanded):
        return "local_file"

    t = text.lower()
    if "bilibili.com" in t or re.search(r"(BV[0-9A-Za-z]{10})", t, re.IGNORECASE):
        return "bilibili"
    if "douyin.com" in t or "tiktok.com" in t:
        return "douyin"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"
    if "xiaohongshu.com" in t or "xhslink.com" in t or "xhs.cn" in t:
        return "xiaohongshu"
    return "unknown"


def resolve_douyin_url(short_url: str) -> str:
    """解析抖音短链接"""
    try:
        req = urllib.request.Request(short_url, headers={
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"),
        })
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=10)
        return resp.url
    except Exception as e:
        print(f"[!] 解析短链接失败: {e}", file=sys.stderr)
        return short_url


def generate_video_id(text: str, platform: str) -> str:
    """为视频生成唯一 ID"""
    if platform == "local_file":
        expanded = os.path.expanduser(text)
        return f"local_{Path(expanded).stem}"
    if platform == "bilibili":
        m = re.search(r"(BV[0-9A-Za-z]{10})", text, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    if platform == "douyin":
        m = re.search(r"/video/(\d+)", text)
        if m:
            return f"dy_{m.group(1)}"
        m = re.search(r"note/(\d+)", text)
        if m:
            return f"dy_{m.group(1)}"
    if platform == "youtube":
        # 提取 YouTube video ID
        m = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", text)
        if m:
            return f"yt_{m.group(1)}"
    if platform == "xiaohongshu":
        m = re.search(r"/(?:explore|discovery/item)/([a-f0-9]+)", text)
        if m:
            return f"xhs_{m.group(1)}"
        m = re.search(r"xhslink\.com/([a-zA-Z0-9]+)", text)
        if m:
            return f"xhs_{m.group(1)}"
    return f"{platform}_{hash(text) % 100000000:08d}"


def download_with_ytdlp(url: str, audio_path: str) -> dict:
    """使用 yt-dlp 下载在线视频音频"""
    if not YTDLP or not os.path.exists(YTDLP):
        return {"error": "yt-dlp 未安装。请运行: brew install yt-dlp"}

    cmd = [
        YTDLP,
        "--no-playlist",
        "-f", "bestaudio",
        "-x", "--audio-format", "m4a",
        "--audio-quality", "0",
        "-o", audio_path,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        # 尝试直接下载不转码
        alt_cmd = [
            YTDLP,
            "--no-playlist",
            "-f", "bestaudio",
            "-o", audio_path,
            url,
        ]
        result = subprocess.run(alt_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"error": f"下载失败: {result.stderr[-500:]}"}
    return {}


def extract_from_local(video_path: str, audio_path: str) -> dict:
    """从本地视频文件提取音频"""
    if not FFMPEG or not os.path.exists(FFMPEG):
        return {"error": "ffmpeg 未安装。请运行: brew install ffmpeg"}

    cmd = [FFMPEG, "-i", video_path, "-vn", "-acodec", "copy", "-y", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0 or not os.path.exists(audio_path):
        # 尝试重新编码
        cmd = [FFMPEG, "-i", video_path, "-vn", "-acodec", "aac", "-b:a", "128k", "-y", audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0 or not os.path.exists(audio_path):
            return {"error": f"提取音频失败: {result.stderr[-300:]}"}
    return {}


def run(url_or_file: str, output_dir: str = None):
    platform = detect_platform(url_or_file)
    if platform == "unknown":
        print("[!] 无法识别输入类型。支持：bilibili.com / douyin.com / youtube.com / xiaohongshu.com / 本地文件", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 平台: {platform}", file=sys.stderr)

    # 抖音短链接需要先解析
    if platform == "douyin" and "v.douyin.com" in url_or_file:
        url_or_file = resolve_douyin_url(url_or_file)
        print(f"[*] 抖音实际链接: {url_or_file}", file=sys.stderr)

    video_id = generate_video_id(url_or_file, platform)

    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache", "audio")
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, f"{video_id}.m4a")

    # 如果已存在，跳过
    if os.path.exists(audio_path):
        print(f"[*] 音频已存在: {audio_path}", file=sys.stderr)
    else:
        print(f"[*] 正在提取音频...", file=sys.stderr)
        if platform == "local_file":
            err = extract_from_local(os.path.expanduser(url_or_file), audio_path)
        else:
            err = download_with_ytdlp(url_or_file, audio_path)

        if "error" in err:
            print(json.dumps({"error": err["error"]}))
            sys.exit(1)

    # 获取文件信息
    info = {"platform": platform, "video_id": video_id, "audio_path": audio_path}
    if audio_path and os.path.exists(audio_path):
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        info["file_size_mb"] = round(size_mb, 2)
        ffprobe = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
        if os.path.exists(ffprobe):
            try:
                dur_cmd = [ffprobe, "-v", "quiet", "-show_entries", "format=duration",
                           "-of", "csv=p=0", audio_path]
                dur_out = subprocess.run(dur_cmd, capture_output=True, text=True, timeout=10)
                info["duration_sec"] = round(float(dur_out.stdout.strip()))
            except Exception:
                pass

    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 video_audio.py <视频链接或本地文件> [输出目录]", file=sys.stderr)
        print("支持: bilibili.com | douyin.com | youtube.com | xiaohongshu.com | 本地.mp4/.mkv 文件", file=sys.stderr)
        sys.exit(1)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    run(sys.argv[1], out_dir)
