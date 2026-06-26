#!/usr/bin/env python3
"""使用 faster-whisper 进行语音识别 - 离线模式"""

from faster_whisper import WhisperModel
import os

audio_path = "/tmp/openclaw/bot-resource-1773578952536-cb087391-d1d5-4064-bd35-f40018176ec4"

print(f"📥 识别文件：{audio_path}")
print("="*50)

# 检查模型是否已下载
model_cache = os.path.expanduser("~/.cache/huggingface/hub")
if not os.path.exists(model_cache):
    print("❌ 错误：faster-whisper 模型未下载")
    print("\n请先配置网络代理或使用阿里云方案\n")
    exit(1)

try:
    print(f"🔍 加载 faster-whisper 模型... (缓存目录：{model_cache})")
    
    # 使用 base 模型（约 73MB，比 whisper 的 140MB 小很多）
    model = WhisperModel("base", device="auto")
    
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
