#!/usr/bin/env python3
"""
音视频合并工具。

使用ffmpeg将音频和视频合并。
需要安装：ffmpeg（系统工具）

用法:
  python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4
  python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4 --mode replace
  python merge_audio_video.py --video video.mp4 --audio audio.wav --output final.mp4 --mode mix
"""

import argparse
import subprocess
import sys
import os

def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def merge_audio_video(video_path, audio_path, output_path, mode="replace"):
    """
    合并音频和视频
    
    参数:
        video_path: 视频文件路径
        audio_path: 音频文件路径
        output_path: 输出文件路径
        mode: 合并模式
            - replace: 替换原视频音频
            - mix: 与原视频音频混合
    """
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误: 视频文件不存在: {video_path}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(audio_path):
        print(f"错误: 音频文件不存在: {audio_path}", file=sys.stderr)
        sys.exit(1)
    
    # 检查ffmpeg
    if not check_ffmpeg():
        print("错误: ffmpeg未安装或不可用", file=sys.stderr)
        print("请安装ffmpeg: https://ffmpeg.org/download.html", file=sys.stderr)
        sys.exit(1)
    
    # 构建ffmpeg命令
    if mode == "replace":
        # 替换模式：替换原视频音频
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_path
        ]
        print(f"合并模式: 替换原视频音频", file=sys.stderr)
    elif mode == "mix":
        # 混合模式：与原视频音频混合
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=longest",
            "-c:v", "copy",
            output_path
        ]
        print(f"合并模式: 与原视频音频混合", file=sys.stderr)
    else:
        print(f"错误: 未知的合并模式: {mode}", file=sys.stderr)
        sys.exit(1)
    
    # 执行ffmpeg命令
    print(f"正在合并音视频...", file=sys.stderr)
    print(f"视频: {video_path}", file=sys.stderr)
    print(f"音频: {audio_path}", file=sys.stderr)
    print(f"输出: {output_path}", file=sys.stderr)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"合并完成: {output_path}", file=sys.stderr)
            # 显示输出文件信息
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"文件大小: {size / 1024 / 1024:.2f} MB", file=sys.stderr)
        else:
            print(f"ffmpeg执行失败:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"执行ffmpeg时发生错误: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="音视频合并工具")
    parser.add_argument("--video", "-v", required=True, help="视频文件路径")
    parser.add_argument("--audio", "-a", required=True, help="音频文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--mode", "-m", choices=["replace", "mix"], default="replace",
                        help="合并模式: replace(替换原音频) 或 mix(混合原音频)")
    
    args = parser.parse_args()
    
    merge_audio_video(
        video_path=args.video,
        audio_path=args.audio,
        output_path=args.output,
        mode=args.mode
    )

if __name__ == "__main__":
    main()