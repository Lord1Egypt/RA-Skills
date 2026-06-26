# -*- coding: utf-8 -*-
"""
完整示例：使用 Pillow + ffmpeg 制作带字幕的视频

流程：
1. 用 Pillow 在图片上绘制字幕
2. 用 ffmpeg 将图片序列转为视频
"""

import subprocess
import os
from ffmpeg_subtitle import add_subtitle_to_image


def get_audio_duration(audio_path: str) -> float:
    """获取音频时长"""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 5.0


def create_video_with_subtitle(
    image_path: str,
    audio_path: str,
    subtitle_text: str,
    output_path: str,
    width: int = 1280,
    height: int = 1024,
    temp_dir: str = "temp"
):
    """
    创建带字幕的视频片段
    
    Args:
        image_path: 输入图片路径
        audio_path: 输入音频路径
        subtitle_text: 字幕文本
        output_path: 输出视频路径
        width: 视频宽度
        height: 视频高度
        temp_dir: 临时文件目录
    """
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. 获取音频时长
    duration = get_audio_duration(audio_path)
    print(f"音频时长: {duration:.2f}秒")
    
    # 2. 在图片上添加字幕
    sub_image_path = os.path.join(temp_dir, "subtitle_image.png")
    add_subtitle_to_image(
        image_path=image_path,
        subtitle_text=subtitle_text,
        output_path=sub_image_path
    )
    print(f"字幕图片已生成: {sub_image_path}")
    
    # 3. 用 ffmpeg 创建视频
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", sub_image_path,
        "-i", audio_path,
        "-t", str(duration),
        "-vf", f"scale={width}:{height}",
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    if result.returncode == 0:
        print(f"视频创建成功: {output_path}")
    else:
        print(f"视频创建失败: {result.stderr}")
    
    return output_path


def concat_videos(video_paths: list, output_path: str, temp_dir: str = "temp"):
    """合并多个视频"""
    list_file = os.path.join(temp_dir, "video_list.txt")
    with open(list_file, 'w', encoding='utf-8') as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-c:a", "aac",
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, encoding='utf-8', errors='replace')
    return output_path


def add_bgm(
    video_path: str,
    bgm_path: str,
    output_path: str,
    bgm_volume: float = 0.4,
    video_volume: float = 0.8
):
    """添加背景音乐"""
    # 获取视频时长
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    video_duration = float(result.stdout.strip())
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[0:a]volume={video_volume}[a1];"
        f"[1:a]volume={bgm_volume},afade=t=in:st=0:d=2,afade=t=out:st={video_duration-3}:d=3[a2];"
        f"[a1][a2]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:v", "copy", "-c:a", "aac",
        "-shortest",
        output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, encoding='utf-8', errors='replace')
    return output_path


# 使用示例
if __name__ == "__main__":
    # 示例：创建单个带字幕的视频片段
    create_video_with_subtitle(
        image_path="cover.png",
        audio_path="intro.mp3",
        subtitle_text="欢迎观看本期视频",
        output_path="output.mp4"
    )
