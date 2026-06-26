#!/usr/bin/env python3
"""使用 faster-whisper 进行语音识别 - 当前文件"""

from faster_whisper import WhisperModel
import os
import sys

# 最新的音频文件路径
audio_path = "/tmp/openclaw/bot-resource-1773586190608-8b5a8811-11d8-42a0-aee4-c17ea2aea956"

print(f"📥 识别文件：{audio_path}")
print("="*50)

# faster-whisper 模型路径（已缓存）
model_path = os.path.expanduser("~/.cache/modelscope/hub/models/pengzhendong/faster-whisper-base")

if not os.path.exists(model_path):
    print(f"❌ 错误：faster-whisper 模型未找到")
    sys.exit(1)

try:
    print(f"\n🔍 加载 faster-whisper 模型...")
    model = WhisperModel(model_path, device="auto")
    
    print("✅ 模型加载成功！")
    print("\n⏳ 正在识别语音...")
    
    # 识别中文语音
    segments, info = model.transcribe(audio_path, language="zh")
    
    text = ""
    for segment in segments:
        text += segment.text + " "
    
    print("="*50)
    print(f"✅ 识别成功！\n\n📝 内容：{text.strip()}\n")
    print("="*50)
    
except Exception as e:
    print(f"\n❌ 错误类型：{type(e).__name__}")
    print(f"❌ 错误信息：{e}")
