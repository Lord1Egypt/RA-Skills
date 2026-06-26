# -*- coding: utf-8 -*-
"""合成视频：幻灯片 + 配音"""

import argparse
import subprocess
import os
import glob

def find_ffmpeg():
    """查找ffmpeg路径"""
    # Windows常见路径
    paths = [
        r"C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        "ffmpeg",  # 系统PATH中
    ]
    
    for path in paths:
        if os.path.exists(path) or subprocess.run([path, "-version"], 
                                                   capture_output=True).returncode == 0:
            return path
    
    raise FileNotFoundError("未找到ffmpeg，请安装或指定路径")

def synthesize_video(slides_dir, audio_file, output_file, ffmpeg_path, fps=25):
    """合成视频"""
    # 获取所有幻灯片图片
    slide_files = sorted(glob.glob(os.path.join(slides_dir, "slide_*.png")))
    
    if not slide_files:
        raise FileNotFoundError(f"在 {slides_dir} 中未找到幻灯片图片")
    
    num_slides = len(slide_files)
    
    # 获取音频时长
    probe_cmd = [ffmpeg_path, "-i", audio_file, "-hide_banner"]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    
    # 解析时长（从stderr中提取）
    import re
    duration_match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe_result.stderr)
    if duration_match:
        h, m, s = map(float, duration_match.groups())
        audio_duration = h * 3600 + m * 60 + s
    else:
        audio_duration = num_slides * 17  # 默认每页17秒
    
    # 计算每页显示时长
    slide_duration = audio_duration / num_slides
    
    print(f"音频时长: {audio_duration:.1f}秒")
    print(f"幻灯片数量: {num_slides}")
    print(f"每页显示: {slide_duration:.1f}秒")
    
    # 构建ffmpeg命令
    cmd_parts = [ffmpeg_path, "-y"]
    
    # 添加每张幻灯片（loop模式，指定时长）
    for slide_file in slide_files:
        cmd_parts.extend([
            "-loop", "1",
            "-t", str(slide_duration),
            "-i", slide_file
        ])
    
    # 添加音频
    cmd_parts.extend(["-i", audio_file])
    
    # 构建filter_complex
    filter_parts = []
    for i in range(num_slides):
        filter_parts.append(f"[{i}:v]format=yuv420p,scale=1920:1080,setsar=1[t{i}];")
    
    concat_inputs = "".join([f"[t{i}]" for i in range(num_slides)])
    filter_complex = "".join(filter_parts) + f"{concat_inputs}concat=n={num_slides}:v=1:a=0[outv]"
    
    cmd_parts.extend([
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", f"{num_slides}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        output_file
    ])
    
    print("\n正在合成视频...")
    result = subprocess.run(cmd_parts, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n视频已生成: {output_file}")
        
        # 显示视频信息
        probe_cmd = [ffmpeg_path, "-i", output_file, "-hide_banner"]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        print("\n视频信息:")
        info_lines = probe_result.stderr.split('\n')
        for line in info_lines[:10]:
            if line.strip():
                print(f"  {line.strip()}")
    else:
        print(f"\n错误: {result.stderr[-500:]}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='合成演示视频')
    parser.add_argument('--slides', required=True, help='幻灯片图片目录')
    parser.add_argument('--audio', required=True, help='配音音频文件')
    parser.add_argument('--output', default='output.mp4', help='输出视频文件')
    parser.add_argument('--ffmpeg', help='ffmpeg路径（可选）')
    parser.add_argument('--fps', type=int, default=25, help='帧率')
    
    args = parser.parse_args()
    
    # 查找ffmpeg
    ffmpeg_path = args.ffmpeg or find_ffmpeg()
    print(f"使用ffmpeg: {ffmpeg_path}")
    
    # 合成视频
    synthesize_video(
        args.slides,
        args.audio,
        args.output,
        ffmpeg_path,
        args.fps
    )

if __name__ == "__main__":
    main()