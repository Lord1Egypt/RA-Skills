# -*- coding: utf-8 -*-
"""使用HTML模板制作演示视频（完整版）

用法:
    python make_video_html.py <脚本文件> <输出视频名>
    
示例:
    python make_video_html.py my_script.txt demo.mp4
"""

import argparse
import os
import subprocess
import asyncio
import edge_tts
import glob
import re
import json

# 模板映射
TEMPLATE_MAP = {
    'cover': '01_cover.html',
    'content': '02_content.html',
    'dual': '03_dual_column.html',
    'timeline': '04_timeline.html',
    'ending': '05_ending.html',
}

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
DEFAULT_RATE = "+5%"
WIDTH = 1920
HEIGHT = 1080

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

def find_playwright():
    """查找Playwright"""
    try:
        # 检查是否安装了playwright
        result = subprocess.run(["python", "-m", "playwright", "--version"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass
    return False

def install_playwright():
    """安装Playwright"""
    print("安装Playwright...")
    subprocess.run(["pip", "install", "playwright"], check=True)
    subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)

def render_html(html_content, output_path):
    """使用Playwright渲染HTML为图片"""
    # 创建临时HTML文件
    tmp_html = "temp_slide.html"
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Playwright脚本
    script = f'''
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setViewportSize({{ width: {WIDTH}, height: {HEIGHT} }});
    await page.goto('file://{os.path.abspath(tmp_html)}');
    await page.waitForTimeout(500);  // 等待渲染
    await page.screenshot({{ path: '{output_path}', fullPage: false }});
    await browser.close();
    console.log('Done');
}})();
'''
    
    tmp_js = "temp_render.js"
    with open(tmp_js, 'w') as f:
        f.write(script)
    
    result = subprocess.run(["node", tmp_js], capture_output=True, text=True)
    
    # 清理临时文件
    os.remove(tmp_html)
    os.remove(tmp_js)
    
    if result.returncode != 0:
        print(f"渲染错误: {result.stderr}")
        return False
    return True

def generate_template(template_name, data):
    """生成HTML模板内容"""
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    template_file = TEMPLATE_MAP.get(template_name, '02_content.html')
    template_path = os.path.join(template_dir, template_file)
    
    if not os.path.exists(template_path):
        # 使用默认内容页模板
        template_path = os.path.join(template_dir, '02_content.html')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 替换占位符
    html = html.replace('{{TITLE}}', data.get('title', ''))
    html = html.replace('{{CONTENT}}', '\n'.join(data.get('content', [])))
    
    return html

def parse_script(filepath):
    """解析脚本文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    slides = []
    current = {"title": "", "content": [], "type": "content"}
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            if current["title"] or current["content"]:
                slides.append(current)
            current = {"title": line[2:], "content": [], "type": "content"}
        elif line.startswith('type:'):
            current["type"] = line.split(':')[1].strip()
        elif line:
            current["content"].append(line)
    
    if current["title"] or current["content"]:
        slides.append(current)
    
    return slides

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
    parser = argparse.ArgumentParser(description='使用HTML模板制作演示视频')
    parser.add_argument('script', help='脚本文件')
    parser.add_argument('output', help='输出视频')
    parser.add_argument('--voice', default=DEFAULT_VOICE)
    parser.add_argument('--rate', default=DEFAULT_RATE)
    parser.add_argument('--ffmpeg', help='ffmpeg路径')
    parser.add_argument('--install-playwright', action='store_true', 
                        help='安装Playwright')
    
    args = parser.parse_args()
    
    # 检查/安装Playwright
    if args.install_playwright or not find_playwright():
        install_playwright()
    
    # 创建临时目录
    tmp_dir = "temp_video_html_" + str(os.getpid())
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, "slides"), exist_ok=True)
    
    try:
        # 1. 解析脚本
        print("解析脚本...")
        slides = parse_script(args.script)
        print(f"共 {len(slides)} 页")
        
        # 2. 生成HTML幻灯片并渲染为图片
        print("生成HTML幻灯片...")
        for i, slide in enumerate(slides):
            html = generate_template(slide.get('type', 'content'), slide)
            output_png = os.path.join(tmp_dir, "slides", f"slide_{i+1:02d}.png")
            
            print(f"  渲染第 {i+1} 页...")
            render_html(html, output_png)
        
        # 3. 生成音频
        print("生成配音...")
        audio_text = ""
        for slide in slides:
            audio_text += slide["title"] + "\n"
            audio_text += "\n".join(slide["content"]) + "\n\n"
        
        asyncio.run(generate_audio(audio_text, os.path.join(tmp_dir, "audio.mp3"),
                                   args.voice, args.rate))
        
        # 4. 合成视频
        ffmpeg = args.ffmpeg or find_ffmpeg()
        synthesize_video(
            os.path.join(tmp_dir, "slides"),
            os.path.join(tmp_dir, "audio.mp3"),
            args.output,
            ffmpeg
        )
        
    finally:
        # 清理临时文件
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()