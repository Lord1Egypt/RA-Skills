#!/usr/bin/env python3
"""使用 faster-whisper 进行语音识别 - 自动检测模型位置"""

from faster_whisper import WhisperModel
import os
import sys

audio_path = "/tmp/openclaw/bot-resource-1773585421031-d57701a2-6fbd-405b-915f-9d46d7ad2ee3"

print(f"📥 识别文件：{audio_path}")
print("="*50)

# 检查模型位置
model_paths = [
    os.path.expanduser("~/.cache/modelscope/hub/models/pengzhendong/faster-whisper-base"),
    os.path.expanduser("~/.cache/huggingface/hub/models--SYSTRAN-faster-whisper-base"),
]

model_path = None
for path in model_paths:
    if os.path.exists(path):
        print(f"✅ 找到模型：{path}")
        model_path = path
        break

if not model_path:
    print("❌ 错误：faster-whisper 模型未下载")
    print("\n请运行以下命令安装:")
    print("  pip install faster-whisper")
    print("  # 首次运行时会自动下载 base 模型 (~73MB)")
    sys.exit(1)

try:
    print(f"\n🔍 加载 faster-whisper 模型...")
    
    # 使用本地模型路径
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
    
    import traceback
    traceback.print_exc()
