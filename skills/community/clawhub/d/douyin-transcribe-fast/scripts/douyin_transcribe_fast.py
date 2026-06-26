#!/usr/bin/env python3
"""
抖音视频快速转文字脚本（优化版）
本地 Whisper 转录，无需 API Key

用法:
  python douyin_transcribe_fast.py <抖音链接或视频文件> [--model MODEL]

示例:
  python douyin_transcribe_fast.py "https://v.douyin.com/xxxxx/"
  python douyin_transcribe_fast.py "video.mp4" --model base
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# 配置
DEFAULT_MODEL = "tiny"  # tiny, base, small, medium
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "douyin-transcripts"

def run_command(cmd, cwd=None, timeout=300):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"

def check_ffmpeg():
    """检查 ffmpeg 是否安装"""
    return_code, _, _ = run_command("ffmpeg -version", timeout=10)
    return return_code == 0

def check_whisper():
    """检查 whisper 是否安装"""
    return_code, _, _ = run_command("whisper --help", timeout=10)
    return return_code == 0

def extract_douyin_info(share_link):
    """使用 douyin-mcp 提取视频信息"""
    print(f"[INFO] 正在解析抖音链接: {share_link}")
    
    # 构建 mcporter 命令
    cmd = f'mcporter call douyin-mcp.parse_douyin_video_info share_link="{share_link}"'
    
    return_code, stdout, stderr = run_command(cmd, timeout=30)
    
    if return_code != 0:
        print(f"[ERROR] 解析失败: {stderr}")
        return None
    
    # 解析输出，提取视频 URL
    video_url = None
    title = "未知标题"
    
    for line in stdout.split('\n'):
        if '下载链接:' in line or 'video_id=' in line:
            match = re.search(r'https?://[^\s<>"\\]+', line)
            if match:
                video_url = match.group(0).replace('\\u002F', '/')
        if '标题:' in line:
            title = line.split(':', 1)[-1].strip() if ':' in line else line.strip()
    
    if not video_url:
        print("[ERROR] 无法提取视频下载链接")
        return None
    
    return {
        'title': title,
        'video_url': video_url,
        'share_link': share_link
    }

def download_audio(video_url, output_path):
    """使用 ffmpeg 下载音频流"""
    print("[INFO] 正在提取音频...")
    
    cmd = (
        f'ffmpeg -i "{video_url}" '
        f'-vn '
        f'-acodec pcm_s16le '
        f'-ar 16000 '
        f'-ac 1 '
        f'-y '
        f'"{output_path}"'
    )
    
    return_code, stdout, stderr = run_command(cmd, timeout=120)
    
    if return_code != 0:
        print(f"[ERROR] 音频提取失败: {stderr}")
        return False
    
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[OK] 音频提取成功: {size_mb:.2f} MB")
        return True
    
    return False

def transcribe_audio(audio_path, model=DEFAULT_MODEL, output_dir=OUTPUT_DIR):
    """使用 Whisper 转录音频"""
    print(f"[INFO] 正在转录音频（使用 {model} 模型）...")
    print("[INFO] 这可能需要几分钟，请耐心等待...")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = (
        f'whisper "{audio_path}" '
        f'--model {model} '
        f'--language Chinese '
        f'--output_format txt '
        f'--output_dir "{output_dir}"'
    )
    
    start_time = time.time()
    return_code, stdout, stderr = run_command(cmd, timeout=600)
    elapsed = time.time() - start_time
    
    if return_code != 0:
        print(f"[ERROR] 转录失败: {stderr}")
        return None
    
    print(f"[OK] 转录完成！耗时: {elapsed:.1f} 秒")
    
    audio_name = Path(audio_path).stem
    txt_file = output_dir / f"{audio_name}.txt"
    
    if txt_file.exists():
        with open(txt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None

def main():
    parser = argparse.ArgumentParser(description='抖音视频快速转文字')
    parser.add_argument('input', help='抖音链接或视频文件路径')
    parser.add_argument('--model', default=DEFAULT_MODEL, 
                       choices=['tiny', 'base', 'small', 'medium'],
                       help='Whisper 模型选择 (默认: tiny)')
    parser.add_argument('--output-dir', default=str(OUTPUT_DIR),
                       help=f'输出目录 (默认: {OUTPUT_DIR})')
    
    args = parser.parse_args()
    
    # 检查依赖
    print("[INFO] 检查环境依赖...")
    if not check_ffmpeg():
        print("[ERROR] 未找到 ffmpeg，请先安装: winget install Gyan.FFmpeg")
        sys.exit(1)
    
    if not check_whisper():
        print("[ERROR] 未找到 whisper，请先安装: pip install openai-whisper")
        sys.exit(1)
    
    print("[OK] 环境检查通过")
    
    # 判断输入类型
    input_path = args.input
    is_url = input_path.startswith('http')
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, 'audio.wav')
        
        if is_url:
            # 抖音链接
            info = extract_douyin_info(input_path)
            if not info:
                sys.exit(1)
            
            print(f"[INFO] 标题: {info['title']}")
            
            # 下载音频
            if not download_audio(info['video_url'], audio_path):
                sys.exit(1)
        else:
            # 本地视频文件
            if not os.path.exists(input_path):
                print(f"[ERROR] 文件不存在: {input_path}")
                sys.exit(1)
            
            print(f"[INFO] 处理本地视频: {input_path}")
            
            # 提取音频
            cmd = (
                f'ffmpeg -i "{input_path}" '
                f'-vn -acodec pcm_s16le -ar 16000 -ac 1 '
                f'-y "{audio_path}"'
            )
            return_code, _, stderr = run_command(cmd, timeout=120)
            if return_code != 0:
                print(f"[ERROR] 音频提取失败: {stderr}")
                sys.exit(1)
        
        # 转录音频
        transcript = transcribe_audio(audio_path, args.model, Path(args.output_dir))
        
        if transcript:
            print("\n" + "="*50)
            print("转录结果:")
            print("="*50)
            print(transcript)
            print("="*50)
            
            # 保存到文件
            output_file = Path(args.output_dir) / f"transcript_{int(time.time())}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                if is_url and info:
                    f.write(f"标题: {info['title']}\n")
                    f.write(f"链接: {input_path}\n")
                    f.write("="*50 + "\n\n")
                f.write(transcript)
            
            print(f"\n[OK] 结果已保存: {output_file}")
        else:
            print("[ERROR] 转录失败")
            sys.exit(1)

if __name__ == '__main__':
    main()
