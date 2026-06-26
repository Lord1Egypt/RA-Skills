#!/usr/bin/env python3
"""
bilibili_audio.py - 从B站视频提取音频

用法:
    python3 bilibili_audio.py <B站链接或BV号> [输出目录]

依赖:
    - yt-dlp (brew install yt-dlp)
    - ffmpeg  (brew install ffmpeg)

输出:
    下载 m4a 音频文件，输出 JSON 到 stdout（包含音频路径和视频信息）
"""

import sys
import os
import json
import subprocess
import re
import shutil

# 查找 yt-dlp
YTDLP = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"


def extract_bvid(text: str) -> str:
    m = re.search(r"(BV[0-9A-Za-z]{10})", text)
    if m:
        return m.group(1)
    raise ValueError(f"无法从 '{text}' 中提取 BV 号")


def run(url_or_bvid: str, output_dir: str = None):
    bvid = extract_bvid(url_or_bvid)
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache", "audio")
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, f"{bvid}.m4a")

    # 如果已存在，跳过下载
    if os.path.exists(audio_path):
        print(f"[*] 音频已存在: {audio_path}", file=sys.stderr)
    else:
        print(f"[*] 正在下载音频: {url_or_bvid}", file=sys.stderr)
        cmd = [
            YTDLP,
            "--no-playlist",
            "-f", "bestaudio",
            "-x", "--audio-format", "m4a",
            "--audio-quality", "0",
            "-o", audio_path,
            url_or_bvid,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            # 尝试直接下载不转码
            alt_cmd = [
                YTDLP,
                "--no-playlist",
                "-f", "bestaudio",
                "-o", audio_path,
                url_or_bvid,
            ]
            result = subprocess.run(alt_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"[!] 下载失败: {result.stderr[-500:]}", file=sys.stderr)
                # 输出错误但继续
                audio_path = ""

    # 获取文件大小和时长
    info = {"bvid": bvid, "audio_path": audio_path}
    if audio_path and os.path.exists(audio_path):
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        info["file_size_mb"] = round(size_mb, 2)
        # 用 ffprobe 获取时长
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
        print("用法: python3 bilibili_audio.py B站链接或BV号 [输出目录]", file=sys.stderr)
        sys.exit(1)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    run(sys.argv[1], out_dir)
