#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书单爆款短视频生成器 v2.0
精准字幕语音对齐版
"""

import asyncio
import json
import subprocess
import random
import time
import argparse
import os
import re
import sys
import platform
from pathlib import Path
from datetime import datetime

# 自动安装依赖
try:
    import edge_tts
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts", "requests", "-q"])
    import edge_tts
    import requests

# 配置
OUTPUT_DIR = Path("output")
ARK_API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
ARK_MODEL = "doubao-seedream-4-0-250828"
DEFAULT_VOICE = "zh-CN-YunxiNeural"


def get_font_path(font_name: str) -> str:
    system = platform.system()
    if system == "Windows":
        return f"/Windows/Fonts/{font_name}"
    elif system == "Darwin":
        return f"/System/Library/Fonts/{font_name}"
    else:
        return font_name


def load_api_key() -> str:
    # 环境变量
    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("DOUBAO_API_KEY")
    if api_key:
        return api_key
    
    # 配置文件
    possible_paths = [
        Path.home() / ".qclaw" / "workspace" / "kdjojodsi.md",
        Path.home() / ".qclaw" / "workspace" / "api_keys.md",
        Path.cwd() / "kdjojodsi.md",
        Path(__file__).parent.parent / "kdjojodsi.md",
    ]
    
    for keys_file in possible_paths:
        if keys_file.exists():
            content = keys_file.read_text(encoding="utf-8")
            match = re.search(r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})", content, re.IGNORECASE)
            if match:
                return match.group(1)
    
    print("\n" + "="*50)
    print("未找到豆包API Key，请配置：")
    print("\n方式1 - 配置文件:")
    print("  创建 ~/.qclaw/workspace/kdjojodsi.md")
    print("  内容: 豆包 API Key: `你的Key`")
    print("\n方式2 - 环境变量:")
    print("  export ARK_API_KEY='你的Key'")
    print("="*50 + "\n")
    raise ValueError("未找到API Key")


def generate_ai_image(prompt: str, output_path: str) -> bool:
    api_key = load_api_key()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"model": ARK_MODEL, "prompt": prompt, "size": "1080x1920", "response_format": "url", "watermark": False}
    
    try:
        r = requests.post(ARK_API_URL, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            img_url = r.json()["data"][0]["url"]
            img_r = requests.get(img_url, timeout=30)
            if img_r.status_code == 200 and len(img_r.content) > 10000:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_r.content)
                return True
    except Exception as e:
        print(f"    错误: {e}")
    return False


def download_ai_images(output_dir: Path, segments: list):
    print(f"\n[1/4] 生成{len(segments)}张AI配图...")
    paths = []
    for i, seg in enumerate(segments):
        output = output_dir / f"bg_{i:02d}.jpg"
        prompt = seg.get("prompt", "book illustration, cinematic")
        print(f"  [{i+1}/{len(segments)}] {prompt[:50]}...")
        
        if generate_ai_image(prompt, str(output)):
            paths.append(output)
            print(f"    [OK]")
        else:
            print(f"    [FAIL] 占位图")
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=1080x1920:d=1", "-frames:v", "1", str(output)], capture_output=True)
            paths.append(output)
        time.sleep(1)
    return paths


async def generate_voice(run_dir: Path, segments: list, voice: str = DEFAULT_VOICE, rate: str = "+0%"):
    print(f"\n[2/4] 生成语音...")
    voice_dir = run_dir / "voices"
    voice_dir.mkdir(exist_ok=True)
    
    timestamps = []
    all_files = []
    current_time = 0.0
    
    for i, seg in enumerate(segments):
        vf = voice_dir / f"seg_{i:02d}.mp3"
        comm = edge_tts.Communicate(seg["cn"], voice, rate=rate)
        chunks = []
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        with open(vf, "wb") as f:
            for c in chunks:
                f.write(c)
        
        probe = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(vf)], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        try:
            dur = float(json.loads(probe.stdout)["format"]["duration"])
        except:
            dur = len(seg["cn"]) * 0.15
        
        timestamps.append({"start": current_time, "end": current_time + dur, "duration": dur, "index": i})
        all_files.append(vf)
        current_time += dur
        print(f"  [{i+1}/{len(segments)}] {dur:.2f}s")
    
    # 合并
    merged = run_dir / "voice_merged.mp3"
    concat = run_dir / "voice_concat.txt"
    with open(concat, "w", encoding="utf-8") as f:
        for vf in all_files:
            f.write(f"file '{str(vf.absolute()).replace(chr(92), '/')}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(merged)], capture_output=True)
    
    print(f"  总时长: {timestamps[-1]['end']:.2f}s")
    return merged, timestamps


def escape_text(text: str) -> str:
    return text.replace("'", "").replace(":", "").replace("\\", "")


def create_video(run_dir: Path, bg_paths: list, voice_path: Path, timestamps: list, segments: list, book_title: str, book_author: str):
    print(f"\n[3/4] 生成视频片段...")
    
    cn_font = get_font_path("msyhbd.ttc")
    en_font = get_font_path("arial.ttf")
    videos = []
    
    random.seed(42)
    directions = []
    for i in range(len(segments)):
        if i == 0:
            directions.append(random.randint(0, 3))
        else:
            d = random.randint(0, 3)
            while d == directions[-1]:
                d = random.randint(0, 3)
            directions.append(d)
    
    for i, seg in enumerate(segments):
        dur = timestamps[i]["duration"]
        cn_c = escape_text(seg["cn"])
        en_c = escape_text(seg.get("en", ""))
        out = run_dir / f"seg_{i}.mp4"
        bg = bg_paths[i % len(bg_paths)]
        
        cn_f = f"drawtext=text='{cn_c}':fontfile={cn_font}:fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h*7/10):shadowx=4:shadowy=4:shadowcolor=black@0.7"
        en_f = f"drawtext=text='{en_c}':fontfile={en_font}:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h*7/10)+65:shadowx=3:shadowy=3:shadowcolor=black@0.6"
        title_f = f"drawtext=text='《{book_title}》':fontfile={cn_font}:fontsize=84:fontcolor=0x87CEEB:x=(w-text_w)/2:y=(h*3/10):shadowx=4:shadowy=4:shadowcolor=black@0.7,drawtext=text='作者：{book_author}':fontfile={cn_font}:fontsize=48:fontcolor=0xFFA500:x=(w-text_w)/2:y=(h*3/10)+80:shadowx=3:shadowy=3:shadowcolor=black@0.6"
        
        d = directions[i]
        if d == 0:
            vf = f"scale=1188:2112,crop=1080:1920:t*60:100,{title_f},{cn_f},{en_f}"
        elif d == 1:
            vf = f"scale=1188:2112,crop=1080:1920:108-t*60:100,{title_f},{cn_f},{en_f}"
        elif d == 2:
            vf = f"scale=1188:2112,crop=1080:1920:50:t*60,{title_f},{cn_f},{en_f}"
        else:
            vf = f"scale=1188:2112,crop=1080:1920:50:192-t*60,{title_f},{cn_f},{en_f}"
        
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(bg), "-t", str(dur), "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out)], capture_output=True)
        if out.exists() and out.stat().st_size > 1000:
            videos.append(out)
        print(f"  [{i+1}/{len(segments)}] {dur:.2f}s")
    
    print(f"\n[4/4] 合并...")
    concat = run_dir / "concat.txt"
    with open(concat, "w", encoding="utf-8") as f:
        for v in videos:
            f.write(f"file '{str(v.absolute()).replace(chr(92), '/')}'\n")
    
    merged = run_dir / "merged.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(merged)], capture_output=True)
    
    output = run_dir / "final.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(merged), "-i", str(voice_path), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(output)], capture_output=True)
    return output


async def main():
    parser = argparse.ArgumentParser(description="书单爆款短视频生成器 v2.0")
    parser.add_argument("--book", "-b", required=True, help="书名")
    parser.add_argument("--author", "-a", required=True, help="作者")
    parser.add_argument("--quotes", "-q", help="金句JSON")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    args = parser.parse_args()
    
    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.output)
    run_dir = OUTPUT_DIR / f"{args.book}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*50)
    print(f"《{args.book}》爆款视频生成 v2.0")
    print("="*50)
    
    if args.quotes:
        with open(args.quotes, "r", encoding="utf-8") as f:
            segments = json.load(f)
    else:
        template = Path(__file__).parent.parent / "templates" / "rich_dad_poor_dad.json"
        if template.exists():
            with open(template, "r", encoding="utf-8") as f:
                segments = json.load(f)
        else:
            print("[ERROR] 请用 -q 指定金句文件")
            return
    
    segments[0]["cn"] = f"今天分享的是：《{args.book}》。"
    
    bg_paths = download_ai_images(run_dir, segments)
    if not bg_paths:
        print("[ERROR] 没有图片")
        return
    
    voice_path, timestamps = await generate_voice(run_dir, segments)
    output = create_video(run_dir, bg_paths, voice_path, timestamps, segments, args.book, args.author)
    
    if output and output.exists():
        size = output.stat().st_size / 1024 / 1024
        print(f"\n[SUCCESS] {size:.1f}MB")
        print(f"路径: {output}")


if __name__ == "__main__":
    asyncio.run(main())
