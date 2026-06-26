# -*- coding: utf-8 -*-
"""一键制作演示视频

用法:
    python make_video.py <脚本文件> <输出视频名>
    
示例:
    python make_video.py my_script.txt demo.mp4
"""

import argparse
import os
import subprocess
import asyncio
import edge_tts
import glob
import re
from PIL import Image, ImageDraw, ImageFont

# 默认配置
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
DEFAULT_RATE = "+5%"
DEFAULT_FPS = 25
WIDTH = 1920
HEIGHT = 1080

# 颜色配置
COLORS = {
    'dark_blue': (0, 51, 102),
    'primary_blue': (0, 102, 255),
    'white': (255, 255, 255),
    'light_gray': (245, 245, 245),
    'accent_green': (0, 204, 102),
    'accent_orange': (255, 153, 0),
    'dark_text': (51, 51, 51),
    'gray_text': (102, 102, 102),
}

def find_ffmpeg():
    """查找ffmpeg"""
    paths = [
        r"C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe",
        "ffmpeg",
    ]
    for path in paths:
        try:
            result = subprocess.run([path, "-version"], capture_output=True)
            if result.returncode == 0:
                return path
        except:
            pass
    raise FileNotFoundError("未找到ffmpeg")

def get_fonts():
    """获取字体"""
    fonts = {}
    sizes = {'title': 72, 'subtitle': 40, 'body': 32, 'small': 24}
    try:
        font_path = "C:\\Windows\\Fonts\\msyh.ttc"
        for name, size in sizes.items():
            fonts[name] = ImageFont.truetype(font_path, size)
    except:
        for name in sizes:
            fonts[name] = ImageFont.load_default()
    return fonts

def parse_script(filepath):
    """解析脚本文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    slides = []
    current = {"title": "", "content": []}
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            if current["title"] or current["content"]:
                slides.append(current)
            current = {"title": line[2:], "content": []}
        elif line:
            current["content"].append(line)
    
    if current["title"] or current["content"]:
        slides.append(current)
    
    return slides

def create_slide(slide, fonts, idx, total):
    """创建幻灯片图片"""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['white'])
    draw = ImageDraw.Draw(img)
    
    # 顶部条
    draw.rectangle([0, 0, WIDTH, 120], fill=COLORS['dark_blue'])
    draw.text((60, 40), slide["title"], font=fonts['title'], fill=COLORS['white'])
    
    # 内容
    y = 180
    for item in slide["content"]:
        if item:
            draw.text((80, y), item, font=fonts['body'], fill=COLORS['dark_text'])
        y += 55
    
    return img

async def generate_audio(text, output, voice, rate):
    """生成音频"""
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(output)

def synthesize_video(slides_dir, audio_file, output_file, ffmpeg_path):
    """合成视频"""
    slide_files = sorted(glob.glob(os.path.join(slides_dir, "slide_*.png")))
    num = len(slide_files)
    
    # 获取音频时长
    probe = subprocess.run([ffmpeg_path, "-i", audio_file, "-hide_banner"],
                           capture_output=True, text=True)
    match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe.stderr)
    if match:
        h, m, s = map(float, match.groups())
        duration = h * 3600 + m * 60 + s
    else:
        duration = num * 17
    
    slide_dur = duration / num
    print(f"音频: {duration:.1f}s, 幻灯片: {num}张, 每页: {slide_dur:.1f}s")
    
    # ffmpeg命令
    cmd = [ffmpeg_path, "-y"]
    for sf in slide_files:
        cmd.extend(["-loop", "1", "-t", str(slide_dur), "-i", sf])
    cmd.extend(["-i", audio_file])
    
    # filter
    filters = [f"[{i}:v]format=yuv420p,scale=1920:1080,setsar=1[t{i}];" for i in range(num)]
    concat = "".join([f"[t{i}]" for i in range(num)])
    filter_complex = "".join(filters) + f"{concat}concat=n={num}:v=1:a=0[outv]"
    
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", f"{num}:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", output_file
    ])
    
    print("合成中...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"完成: {output_file}")
        return True
    else:
        print(f"错误: {result.stderr[-300:]}")
        return False

def main():
    parser = argparse.ArgumentParser(description='一键制作演示视频')
    parser.add_argument('script', help='脚本文件')
    parser.add_argument('output', help='输出视频')
    parser.add_argument('--voice', default=DEFAULT_VOICE)
    parser.add_argument('--rate', default=DEFAULT_RATE)
    parser.add_argument('--ffmpeg', help='ffmpeg路径')
    
    args = parser.parse_args()
    
    # 创建临时目录
    tmp_dir = "temp_video_" + str(os.getpid())
    os.makedirs(tmp_dir, exist_ok=True)
    
    try:
        # 1. 解析脚本
        print("解析脚本...")
        slides = parse_script(args.script)
        print(f"共 {len(slides)} 页")
        
        # 2. 生成幻灯片
        print("生成幻灯片...")
        fonts = get_fonts()
        for i, slide in enumerate(slides):
            img = create_slide(slide, fonts, i, len(slides))
            img.save(os.path.join(tmp_dir, f"slide_{i+1:02d}.png"))
        
        # 3. 生成音频
        print("生成配音...")
        # 从脚本提取音频文本（去掉标题标记）
        audio_text = ""
        for slide in slides:
            audio_text += slide["title"] + "\n"
            audio_text += "\n".join(slide["content"]) + "\n\n"
        
        asyncio.run(generate_audio(audio_text, os.path.join(tmp_dir, "audio.mp3"),
                                   args.voice, args.rate))
        
        # 4. 合成视频
        ffmpeg = args.ffmpeg or find_ffmpeg()
        synthesize_video(tmp_dir, os.path.join(tmp_dir, "audio.mp3"),
                        args.output, ffmpeg)
        
    finally:
        # 清理临时文件
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()