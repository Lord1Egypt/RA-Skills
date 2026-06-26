#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Announcement Player - PyGame Version
使用 pygame.mixer 播放，高质量、低延迟
需要: pip install pygame
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import shutil
import time
import threading

# 配置
CACHE_DIR = os.path.expanduser("~/.cache/audio-announcement")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "audio-announcement")
MAX_RETRIES = 3
KEEP_TEMP_FILES = True
VOLUME = 1.0  # 0.0 - 1.0

def ensure_dirs():
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

def get_cache_key(text, voice):
    key_str = f"{text}-{voice}"
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()

def generate_audio(text, voice, output_file):
    """生成 MP3"""
    print(f"[INFO] 生成语音: {text[:30]}...", file=sys.stderr)
    
    cache_key = get_cache_key(text, voice)
    cached_file = os.path.join(CACHE_DIR, f"{cache_key}.mp3")
    
    if os.path.exists(cached_file):
        print(f"[INFO] 使用缓存", file=sys.stderr)
        shutil.copy2(cached_file, output_file)
        return True
    
    for i in range(1, MAX_RETRIES + 1):
        try:
            # 使用 python -m edge_tts 避免依赖 PATH，更稳定
            result = subprocess.run(
                [sys.executable, "-m", "edge_tts", "--text", text, "--voice", voice, "--write-media", output_file],
                capture_output=True, timeout=30
            )
            if result.returncode == 0 and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                shutil.copy2(output_file, cached_file)
                print(f"[INFO] 生成成功", file=sys.stderr)
                return True
        except Exception as e:
            print(f"[WARN] 第{i}次失败: {e}", file=sys.stderr)
        if i < MAX_RETRIES:
            time.sleep(1)
    
    print(f"[ERROR] 生成失败", file=sys.stderr)
    return False

def play_pygame(audio_file):
    """使用 pygame 播放（高质量、低延迟）"""
    try:
        import pygame
        
        # 初始化 pygame mixer，使用更大缓冲区减少卡顿
        # frequency=44100, size=-16 (16bit), channels=2, buffer=4096 (更大缓冲)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # 设置音量 (0.0 - 1.0)
        pygame.mixer.music.set_volume(VOLUME)
        
        # 加载并播放
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        print(f"[INFO] pygame 播放 (音量: {VOLUME*100:.0f}%)", file=sys.stderr)
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)  # 更短的间隔，更流畅
        
        print(f"[INFO] 播放完成", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"[ERROR] pygame 播放失败: {e}", file=sys.stderr)
        return False

def announce(type_, message, lang="zh"):
    voices = {
        "zh": "zh-CN-XiaoxiaoNeural",
        "en": "en-US-JennyNeural",
        "ja": "ja-JP-NanamiNeural",
        "ko": "ko-KR-SunHiNeural",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
    }
    
    voice = voices.get(lang, voices["zh"])
    
    prefixes = {
        "task": "任务: ",
        "complete": "完成: ",
        "error": "警告: ",
        "custom": ""
    }
    
    full_message = prefixes.get(type_, "") + message
    timestamp = int(time.time() * 1000)
    temp_mp3 = os.path.join(TEMP_DIR, f"announce_{os.getpid()}_{timestamp}.mp3")
    
    try:
        if not generate_audio(full_message, voice, temp_mp3):
            return False
        
        if not play_pygame(temp_mp3):
            print("[ERROR] 播放失败", file=sys.stderr)
            return False
        
        print(f"[INFO] 播报成功", file=sys.stderr)
        
        if KEEP_TEMP_FILES:
            print(f"[DEBUG] 文件保留: {temp_mp3}", file=sys.stderr)
        else:
            def cleanup():
                time.sleep(10)
                try:
                    os.remove(temp_mp3)
                except:
                    pass
            threading.Thread(target=cleanup, daemon=True).start()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 异常: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    ensure_dirs()
    
    if len(sys.argv) < 3:
        print("用法: python announce_pygame.py <type> <message> [lang]", file=sys.stderr)
        print("示例: python announce_pygame.py complete '任务完成' zh", file=sys.stderr)
        sys.exit(1)
    
    type_ = sys.argv[1]
    message = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "zh"
    
    success = announce(type_, message, lang)
    sys.exit(0 if success else 1)
