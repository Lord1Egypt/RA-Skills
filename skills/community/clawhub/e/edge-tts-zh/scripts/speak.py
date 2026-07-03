#!/usr/bin/env python3
"""
中文语音合成 (edge-tts) - 小禾专用版
使用 Microsoft Edge TTS 引擎，完全免费，无需 API key
默认声音：xiaoxiao（温暖活泼的女声）
"""

import argparse
import asyncio
import sys
import os
import time

# 中文声音列表（女声优先）
VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",    # 温暖活泼 ⭐ 小禾默认
    "xiaoyi": "zh-CN-XiaoyiNeural",        # 知性优雅
    "xiaomeng": "zh-CN-XiaomengNeural",    # 可爱甜美
    "xiaochen": "zh-CN-XiaochenNeural",    # 温柔
    "xiaohan": "zh-CN-XiaohanNeural",      # 知性
    # 男声备选
    "yunxi": "zh-CN-YunxiNeural",
    "yunyang": "zh-CN-YunyangNeural",
}

DEFAULT_VOICE = "xiaoxiao"  # 小禾的女声
DEFAULT_RATE = "+10%"

def resolve_voice(name):
    if not name:
        return VOICES[DEFAULT_VOICE]
    lower = name.lower()
    if lower in VOICES:
        return VOICES[lower]
    if "Neural" in name:
        return name
    return VOICES[DEFAULT_VOICE]

async def synthesize(text, voice, rate, output_path):
    try:
        import edge_tts
    except ImportError:
        print("❌ edge-tts 未安装，运行：pip install edge-tts", file=sys.stderr)
        return False
    
    voice_name = resolve_voice(voice)
    print(f"Voice: {voice_name}", file=sys.stderr)
    
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice_name, rate=rate)
        await communicate.save(output_path)
        
        size = os.path.getsize(output_path)
        print(f"Generated: {output_path} ({size/1024:.1f}KB)", file=sys.stderr)
        
        # 自动播放（使用 pygame，完全后台无窗口）
        play_audio(output_path)
        
        return True
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def play_audio(file_path):
    """使用 pygame 播放音频，完全隐藏窗口"""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        
        print("Playing completed!", file=sys.stderr)
        pygame.mixer.quit()
    except ImportError:
        print("⚠️ pygame not found, skipping auto-play", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ Play failed: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="中文语音合成 (edge-tts) - 小禾版")
    parser.add_argument("text", nargs="?", help="要转换的文字")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, help=f"声音名称 (默认：{DEFAULT_VOICE})")
    parser.add_argument("--rate", "-r", default=DEFAULT_RATE, help="语速")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    text = args.text
    if not text:
        print("❌ 请提供文本内容", file=sys.stderr)
        return 1
    
    output = args.output or f"C:/Users/Administrator/AppData/Local/Temp/tts-output.mp3"
    
    success = asyncio.run(synthesize(text, args.voice, args.rate, output))
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
