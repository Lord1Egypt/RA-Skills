#!/usr/bin/env python3
"""
get_accompaniment.py — 伴奏生成工具

从 YouTube 搜索下载音频 → AI 分离人声/伴奏

用法:
  # 搜索 YouTube 下载（自动使用浏览器 cookies）
  python3 get_accompaniment.py "晴天" "周杰伦"

  # 直接提供视频 URL
  python3 get_accompaniment.py --url "https://youtube.com/watch?v=xxx"

  # 显式指定 cookies 文件
  python3 get_accompaniment.py "晴天" "周杰伦" --cookies cookies.txt

  # 处理本地音频文件（不需要网络）
  python3 get_accompaniment.py --file /path/to/song.mp3

  # JSON 输出（供 agent 解析）
  python3 get_accompaniment.py "晴天" "周杰伦" --json

💡 无需手动导出 cookies！脚本会自动从本地 Chrome 浏览器提取登录态。
  如果 Chrome 不可用，再通过 --cookies 手动指定 cookies 文件。

依赖:
  pip install yt-dlp
  pip install demucs
  ffmpeg (系统安装: apt install ffmpeg / brew install ffmpeg)
"""

import sys
import os
import json
import re
import time
import glob
import shutil
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path


def log(msg):
    print(msg, flush=True)


def find_audio_files(dir_path):
    exts = ['*.mp3', '*.wav', '*.flac', '*.m4a', '*.opus', '*.ogg', '*.webm', '*.aac']
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(dir_path, ext)))
    return files


def convert_to_mp3(input_file, output_file=None):
    """ffmpeg 转 mp3"""
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.mp3'
    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', input_file, '-q:a', '2', output_file],
            capture_output=True, text=True, timeout=120, check=True
        )
        return output_file if os.path.exists(output_file) else None
    except Exception:
        return None


# ─── YouTube 搜索（无需 cookies） ───

def search_youtube(query, max_results=5):
    """抓取 YouTube 搜索结果，不需要 cookies"""
    url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(query)}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        ids = re.findall(r'"videoId":"([^"]+)"', html)
        if not ids:
            return []
        seen = set()
        results = []
        for vid in ids:
            if vid not in seen:
                seen.add(vid)
                results.append({'id': vid, 'url': f'https://www.youtube.com/watch?v={vid}'})
                if len(results) >= max_results:
                    break
        return results
    except Exception as e:
        log(f"⚠️  搜索失败: {e}")
        return []


# ─── YouTube 音频下载 ───

def download_youtube_audio(video_url, output_path, cookies_file=None):
    """下载 YouTube 音频。优先使用浏览器 cookies，fallback 到 cookies 文件。"""
    cmd = [
        'yt-dlp', '-f', 'bestaudio/best',
        '--extract-audio', '--audio-format', 'mp3',
        '--audio-quality', '192k',
        '-o', os.path.join(output_path, '%(title)s.%(ext)s'),
        '--no-warnings',
    ]

    # YouTube 可能需要指定客户端类型以配合 cookies
    cmd.extend(['--extractor-args', 'youtube:player_client=web_safari'])

    # 添加 JS 运行时（用于 YouTube 签名解算）
    deno_path = os.path.expanduser("~/.deno/bin/deno")
    if os.path.exists(deno_path):
        cmd.extend(['--js-runtimes', f'deno:{deno_path}'])

    # cookies 策略：优先 cookies-from-browser，其次手动指定
    if cookies_file:
        resolved = os.path.abspath(cookies_file) if not os.path.isabs(cookies_file) else cookies_file
        if os.path.exists(resolved):
            cmd.extend(['--cookies', resolved])
        else:
            log(f"⚠️  cookies 文件不存在: {resolved}")
            return None, "COOKIES_FILE_NOT_FOUND"
    else:
        # 默认使用浏览器 cookies（最省事）
        cmd.extend(['--cookies-from-browser', 'chrome'])

    cmd.append(video_url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            files = find_audio_files(output_path)
            if files:
                return files[0], None
            return None, "NO_AUDIO_FILE"
        else:
            err = result.stderr or ""
            if "Sign in" in err or "bot" in err:
                return None, "NEEDS_COOKIES"
            return None, f"YT_DLP_ERROR: {err[-200:]}"
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"

    cmd.append(video_url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            files = find_audio_files(output_path)
            if files:
                return files[0], None
            return None, "NO_AUDIO_FILE"
        else:
            err = result.stderr or ""
            if "Sign in" in err or "bot" in err:
                return None, "NEEDS_COOKIES"
            return None, f"YT_DLP_ERROR: {err[-200:]}"
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"


# ─── Demucs 人声/伴奏分离 ───

def find_demucs():
    """查找 Demucs 安装位置"""
    import importlib.util

    # 优先使用当前 Python 解释器
    if importlib.util.find_spec("demucs"):
        return sys.executable

    # 搜索常见位置
    candidates = [
        os.path.expanduser("~/.local/bin/python3"),
        "python3",
        "python",
    ]
    for py in candidates:
        full_path = py if os.path.isabs(py) else py
        try:
            r = subprocess.run(
                [full_path, '-m', 'demucs', '--help'],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode == 0:
                return full_path
        except Exception:
            continue
    return None


def separate_audio(audio_file, output_path):
    """用 Demucs 分离人声和伴奏"""
    demucs_python = find_demucs()
    if not demucs_python:
        log("❌ Demucs 未安装。请运行: pip install demucs")
        return None, None

    log("🎛️  分离人声/伴奏（Demucs，约 1-5 分钟）...")
    cmd = [
        demucs_python, '-m', 'demucs',
        '--two-stems', 'vocals',
        '-o', os.path.join(output_path, 'demucs_out'),
        '--mp3', '--mp3-bitrate', '192',
        audio_file,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            log(f"❌ Demucs 失败: {(result.stderr or '')[-200:]}")
            return None, None

        # 查找分离结果
        demucs_base = os.path.join(output_path, 'demucs_out', 'htdemucs')
        if os.path.isdir(demucs_base):
            subdirs = sorted(os.listdir(demucs_base))
            for sub in reversed(subdirs):
                sp = os.path.join(demucs_base, sub)
                if os.path.isdir(sp):
                    acc = os.path.join(sp, 'no_vocals.mp3')
                    voc = os.path.join(sp, 'vocals.mp3')
                    if os.path.exists(acc):
                        return (acc, voc if os.path.exists(voc) else None)

        # fallback: 全局搜索
        for root, dirs, files in os.walk(os.path.join(output_path, 'demucs_out')):
            for f in files:
                if f == 'no_vocals.mp3':
                    return (os.path.join(root, f),
                            os.path.join(root, 'vocals.mp3')
                            if os.path.exists(os.path.join(root, 'vocals.mp3'))
                            else None)
        return None, None

    except subprocess.TimeoutExpired:
        log("⏰ Demucs 超时（请尝试更短的音频或使用 GPU）")
        return None, None


# ─── 主流程 ───

def main():
    parser = argparse.ArgumentParser(
        description='伴奏生成工具：从 YouTube 或本地文件分离人声和伴奏',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('song', nargs='?', help='歌名（与歌手搭配使用）')
    parser.add_argument('artist', nargs='?', default='', help='歌手名')
    group.add_argument('--url', help='直接提供视频 URL')
    group.add_argument('--file', '-f', help='处理本地音频文件')

    parser.add_argument('--output', '-o', default=os.path.expanduser('~/accompaniment_output'),
                        help='输出目录 (默认: ~/accompaniment_output)')
    parser.add_argument('--cookies', help='YouTube cookies 文件路径')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()
    if not args.url and not args.file and not args.song:
        parser.print_help()
        sys.exit(1)

    output_base = os.path.abspath(args.output)
    os.makedirs(output_base, exist_ok=True)

    song_name = ""
    audio_file = None

    # ── 模式 A: 处理本地文件 ──
    if args.file:
        local_file = os.path.abspath(args.file)
        if not os.path.exists(local_file):
            log(f"❌ 文件不存在: {local_file}")
            sys.exit(1)

        song_name = os.path.splitext(os.path.basename(local_file))[0]

        if not local_file.endswith('.mp3'):
            log("🔄 转换为 MP3...")
            mp3_file = os.path.join(output_base, f"_tmp_{int(time.time())}.mp3")
            converted = convert_to_mp3(local_file, mp3_file)
            audio_file = converted or local_file
        else:
            audio_file = local_file

        log(f"🎵 本地文件: {os.path.basename(audio_file)}")
        log(f"📦 {os.path.getsize(audio_file)/1024/1024:.1f} MB")

    # ── 模式 B: YouTube 下载 ──
    else:
        song_name = args.song or ""
        artist = args.artist or ""

        video_url = args.url
        if not video_url:
            query = f"{song_name} {artist}".strip()
            log(f"🔍 搜索 YouTube: {query}")
            results = search_youtube(query)
            if not results:
                log("❌ 搜索无结果")
                sys.exit(1)
            video_url = results[0]['url']
            log(f"✅ 找到: {video_url}")

        ts = time.strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', (song_name or "audio"))[:30]
        safe_artist = re.sub(r'[^a-zA-Z0-9_]', '_', artist)[:20] if artist else ""
        job_name = f"{safe_name}_{safe_artist}_{ts}" if safe_artist else f"{safe_name}_{ts}"
        dl_path = os.path.join(output_base, job_name)
        os.makedirs(dl_path, exist_ok=True)

        log(f"⬇️  下载音频...")
        audio_file, err = download_youtube_audio(video_url, dl_path, args.cookies)

        if err == "NEEDS_COOKIES":
            print("""
❌ YouTube 需要登录认证。

💡 请确保已在 Chrome 中登录 Google 账号，脚本会自动提取浏览器 cookies。
   运行命令: yt-dlp --cookies-from-browser chrome ...

   如果 Chrome 不可用，用 --cookies cookies.txt 手动指定 cookies 文件:
   1. Chrome 扩展 "Get cookies.txt LOCALLY" → 导出
   2. python3 get_accompaniment.py --cookies cookies.txt
""")
            sys.exit(1)

        if audio_file is None:
            log(f"❌ 下载失败: {err}")
            sys.exit(1)

        log(f"✅ 下载完成: {os.path.basename(audio_file)}")
        log(f"📦 {os.path.getsize(audio_file)/1024/1024:.1f} MB")

    # ── 分离 ──
    log("")
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe_out = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', song_name)[:30]
    job_path = os.path.join(output_base, f"{safe_out}_{ts}")
    os.makedirs(job_path, exist_ok=True)

    accompaniment, vocals = separate_audio(audio_file, job_path)

    if accompaniment is None:
        log("❌ 伴奏分离失败")
        sys.exit(1)

    final_acc = os.path.join(job_path, f"{song_name}_伴奏.mp3")
    shutil.copy2(accompaniment, final_acc)
    final_voc = None
    if vocals:
        final_voc = os.path.join(job_path, f"{song_name}_人声.mp3")
        shutil.copy2(vocals, final_voc)

    # ── 输出 ──
    result = {
        "success": True,
        "song": song_name,
        "accompaniment": final_acc,
        "vocals": final_voc,
        "accompaniment_size_mb": round(os.path.getsize(final_acc) / 1024 / 1024, 1),
    }
    if final_voc:
        result["vocals_size_mb"] = round(os.path.getsize(final_voc) / 1024 / 1026, 1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"\n{'='*40}")
        print("🎉 完成！")
        print(f"{'='*40}")
        print(f"🎶 伴奏: {final_acc}  ({result['accompaniment_size_mb']} MB)")
        if final_voc:
            print(f"🎤 人声: {final_voc}  ({result['vocals_size_mb']} MB)")


if __name__ == '__main__':
    main()
