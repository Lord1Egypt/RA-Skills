#!/usr/bin/env python3
"""Whisper 语音识别脚本 - Feishu Voice Assistant"""

import sys
from pathlib import Path

def transcribe_audio(audio_path: str) -> str:
    """使用 Whisper 转文字"""
    
    try:
        from faster_whisper import WhisperModel
        
        print("🔍 正在加载 Whisper 模型...")
        
        # 尝试加载 base 模型（CPU 友好）
        model = WhisperModel("base", device="cpu")
        
        print(f"📥 识别音频文件：{audio_path}")
        
        segments, info = model.transcribe(
            audio_path,
            language="zh",  # 中文场景，或自动检测用 None
            word_timestamps=True
        )
        
        text = " ".join([segment.text for segment in segments])
        
        print(f"✅ 识别结果：{text}")
        return text
        
    except ImportError:
        print("❌ faster-whisper 未安装，正在尝试安装...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faster-whisper"])
        
        # 重试
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu")
        segments, info = model.transcribe(audio_path)
        text = " ".join([segment.text for segment in segments])
        
        print(f"✅ 识别结果：{text}")
        return text
        
    except Exception as e:
        print(f"❌ 识别失败：{e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python transcribe.py <audio_file_path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(audio_path).exists():
        print(f"❌ 文件不存在：{audio_path}")
        sys.exit(1)
    
    result = transcribe_audio(audio_path)
    
    if result:
        print("\n=== 识别结果 ===")
        print(result)
        print("===============")
