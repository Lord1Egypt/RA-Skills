#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频批量转写器 - V2 (Portable, Secure & Robust)
"""

import os
import sys
import json
import time
import tempfile
import argparse
import whisper
import requests
from datetime import datetime
import io
import re
import subprocess
from pathlib import Path
from typing import Optional

# ==================== 配置区域 (V2 - 动态与安全) ====================

def find_openclaw_root() -> Optional[Path]:
    """健壮地向上查找 .openclaw 根目录。"""
    current_path = Path(__file__).resolve().parent
    for _ in range(5):
        if (current_path / 'config.json').exists() and (current_path / 'skills').is_dir():
            return current_path
        if current_path.parent == current_path: break
        current_path = current_path.parent
    home_path = Path.home() / '.openclaw'
    return home_path if home_path.exists() else None

OPENCLAW_ROOT = find_openclaw_root()

if not OPENCLAW_ROOT:
    print("致命错误：无法定位 .openclaw 根目录。", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = OPENCLAW_ROOT / 'config.json'
DEFAULT_OUTPUT_DIR = OPENCLAW_ROOT / "workspace" / "data" / "video-transcriber"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
WHISPER_MODEL = "base"

# ==================== 辅助函数 ====================
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_final_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException as e:
        print(f"  无法跟踪链接跳转 {url}: {e}", file=sys.stderr)
        return url

def extract_audio(video_path, audio_path):
    """
    调用 ffmpeg 提取音频。
    依赖于 ffmpeg 在系统的 PATH 环境变量中。
    """
    cmd = [
        'ffmpeg', '-i', video_path, '-vn',
        '-acodec', 'libmp3lame', '-y', audio_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', check=False)
        if result.returncode != 0:
            if "ffmpeg: not found" in result.stderr or "不是内部或外部命令" in result.stderr:
                 raise FileNotFoundError("错误：'ffmpeg' 未在系统 PATH 中找到。请安装 ffmpeg 并将其添加到环境变量中。")
            print(f"  ffmpeg 错误: {result.stderr}", file=sys.stderr)
            return False
        return os.path.exists(audio_path) and os.path.getsize(audio_path) > 0
    except FileNotFoundError as e:
        print(f"  致命错误: {e}", file=sys.stderr)
        # 向上抛出，让主程序捕获并停止
        raise e
    except Exception as e:
        print(f"  音频提取异常: {e}", file=sys.stderr)
        return False


def transcribe_audio(audio_path):
    try:
        model = whisper.load_model(WHISPER_MODEL)
        print(f"  正在使用 Whisper ({WHISPER_MODEL}) 转写...", file=sys.stderr)
        result = model.transcribe(audio=audio_path, language='zh', initial_prompt="以下是普通话的句子。")
        return result['text'].strip()
    except Exception as e:
        print(f"  转写失败: {e}", file=sys.stderr)
        return None

# ==================== 抖音下载逻辑 ====================
TIKHUB_VIDEO_API = "https://api.tikhub.io/api/v1/douyin/web/fetch_one_video"

def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """从 config.json 安全地读取配置值"""
    if not CONFIG_PATH.exists(): return default
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        return config.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default

def get_tikhub_token():
    """从配置中安全地获取 TikHub Token"""
    token = get_config_value('tikhub_api_token', os.getenv('TIKHUB_API_TOKEN'))
    if not token:
        raise ValueError("错误：未在 config.json 或环境变量中配置 'tikhub_api_token'")
    return token

def extract_modal_id(text):
    final_url = get_final_url(text)
    print(f"  解析后链接: {final_url}", file=sys.stderr)
    patterns = [r'/video/(\d+)', r'modal_id[=:]([\d]+)', r'^(\d{16,})$']
    for pattern in patterns:
        match = re.search(pattern, final_url)
        if match:
            return match.group(1)
    return None

def get_video_download_url(modal_id, token):
    url = f"{TIKHUB_VIDEO_API}?aweme_id={modal_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    aweme_detail = data.get("aweme_detail", {})
    if not aweme_detail:
        raise ValueError("API响应中缺少 'aweme_detail' 字段")
    
    play_url_list = aweme_detail.get("video", {}).get("play_addr", {}).get("url_list")
    if play_url_list:
        return play_url_list[0]
        
    raise ValueError(f"无法从API响应中找到视频播放地址: {str(data)[:500]}")


def download_video(url, output_path):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.douyin.com/"}
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return output_path

# ==================== 主程序 ====================
def main():
    parser = argparse.ArgumentParser(description="抖音视频批量转写技能 (V2)")
    parser.add_argument("--url", dest="urls", action="append", required=True, help="抖音视频分享链接 (可多次使用)")
    parser.add_argument("--output-file", help=f"统一输出的Markdown文件路径 (默认: {DEFAULT_OUTPUT_DIR}/<timestamp>_report.md)")
    args = parser.parse_args()

    # 动态确定输出文件路径
    if args.output_file:
        output_file = Path(args.output_file)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = DEFAULT_OUTPUT_DIR / f"{timestamp}_transcription_report.md"
    
    ensure_dir(output_file.parent)

    try:
        tikhub_token = get_tikhub_token()
    except ValueError as e:
        print(f"致命错误：{e}", file=sys.stderr)
        sys.exit(1)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 视频批量转写报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    video_files_to_clean = []
    
    for i, url in enumerate(args.urls):
        print(f"\n{'='*20} 正在处理视频 {i+1}/{len(args.urls)} {'='*20}", file=sys.stderr)
        try:
            print(f"[步骤1] 解析链接: {url}", file=sys.stderr)
            modal_id = extract_modal_id(url)
            if not modal_id:
                raise ValueError("无法提取视频ID")
            download_url = get_video_download_url(modal_id, tikhub_token)
            
            video_filename = f"douyin_{modal_id}_{int(time.time())}.mp4"
            video_path = Path(tempfile.gettempdir()) / video_filename
            video_files_to_clean.append(video_path)

            print(f"[步骤2] 下载视频到: {video_path}", file=sys.stderr)
            download_video(download_url, video_path)

            print(f"[步骤3] 提取音频并转写...", file=sys.stderr)
            audio_temp_path = Path(tempfile.gettempdir()) / f"{video_filename}.mp3"
            
            if not extract_audio(video_path, audio_temp_path):
                raise Exception("音频提取失败")
            
            transcription = transcribe_audio(audio_temp_path)
            os.unlink(audio_temp_path)
            
            if transcription is None:
                raise Exception("语音转文字失败")
            
            md_content = f"## 视频 {i+1}: {url}\n\n---\n\n{transcription}\n\n"
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(md_content)
            print(f"✅ 转写结果已追加至: {output_file}", file=sys.stderr)

        except FileNotFoundError as e:
            # ffmpeg 未找到的特定错误处理
            print(f"❌ 处理失败，依赖缺失: {e}", file=sys.stderr)
            sys.exit(1) # 中止整个任务
        except Exception as e:
            print(f"❌ 处理失败: {e}", file=sys.stderr)
            error_content = f"## ❌ 视频 {i+1} 处理失败: {url}\n\n错误详情: `{e}`\n\n"
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(error_content)
    
    print("\n[清理] 删除临时视频文件...", file=sys.stderr)
    for f in video_files_to_clean:
        if os.path.exists(f):
            os.remove(f)
            print(f"  已删除: {f}", file=sys.stderr)

    print(f"\n🎉 批量转写完成! 最终报告文件: {output_file}")
    print(f"TRANSCRIPTION_PATH:{output_file}")

if __name__ == "__main__":
    main()
