#!/usr/bin/env python3
"""简单的 B 站音频下载和转写脚本"""
import requests
import subprocess
import sys
import os

bvid = "BV1QWd8BCEH7"
cid = 37542367030
output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"

print(f"🎬 处理视频：{bvid}")
print("=" * 60)

# 尝试获取音频 URL（无需登录的接口）
try:
    # 使用 playurl 接口
    url = f"https://api.bilibili.com/x/player/playurl?cid={cid}&bvid={bvid}&qn=0&type=&otype=json&fnver=0&fnval=4048"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    data = resp.json()
    
    if data.get('code') == 0:
        audio_url = data['data']['dash']['audio'][0]['baseUrl']
        print(f"✅ 获取到音频 URL")
        
        # 下载音频
        audio_file = os.path.join(output_dir, "raspberry_zero.mp3")
        print(f"⬇️  下载音频中...")
        subprocess.run([
            "yt-dlp", 
            "-x", "--audio-format", "mp3",
            "-o", audio_file,
            audio_url
        ], check=True, timeout=180)
        
        print(f"✅ 音频下载完成：{audio_file}")
        
        # 使用 whisper 转写
        print(f"🎤 开始语音转写...")
        transcript_file = os.path.join(output_dir, "raspberry_zero_transcript.txt")
        subprocess.run([
            "whisper",
            audio_file,
            "--model", "base",
            "--language", "zh",
            "--output_dir", output_dir,
            "--output_format", "txt"
        ], check=True, timeout=600)
        
        print(f"✅ 转写完成！")
        print(f"📄 输出文件：{transcript_file}")
        
    else:
        print(f"❌ 获取音频 URL 失败：{data.get('message', 'Unknown error')}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ 错误：{e}")
    sys.exit(1)
