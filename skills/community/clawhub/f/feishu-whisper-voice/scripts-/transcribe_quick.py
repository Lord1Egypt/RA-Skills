#!/usr/bin/env python3
"""快速语音识别 - 简单版"""

import subprocess
import sys

audio_path = "/tmp/openclaw/bot-resource-1773578262747-a7da1d11-604d-4f80-ae2a-5ff39981f1c8"

print(f"📥 开始识别：{audio_path}")
print("="*50)

try:
    # 安装依赖（如果未安装）
    subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper", "--quiet"], check=True)
    
    from faster_whisper import WhisperModel
    
    print("🔍 加载模型 base (约 140MB，首次需要下载)...")
    model = WhisperModel("base", device="cpu")
    
    print("⏳ 正在识别语音...")
    segments, info = model.transcribe(audio_path, language="zh")
    
    text = " ".join([segment.text for segment in segments])
    
    print("="*50)
    print(f"✅ 识别成功！\n\n📝 内容：{text}\n")
    print("="*50)
    
except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback
    traceback.print_exc()
