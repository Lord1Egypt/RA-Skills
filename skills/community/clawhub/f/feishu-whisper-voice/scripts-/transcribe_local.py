#!/usr/bin/env python3
"""使用本地 faster-whisper 模型进行语音识别"""

import sys
from faster_whisper import WhisperModel

def transcribe_audio(file_path: str):
    """使用本地模型路径进行识别"""
    
    # 指定本地模型路径
    model_path = "/Users/jurry/.cache/modelscope/hub/models/pengzhendong/faster-whisper-base"
    
    print(f"📥 识别文件：{file_path}")
    print("==================================================")
    
    print("\n🔍 加载 faster-whisper 模型...")
    model = WhisperModel(model_path, device="cpu", compute_type="float32")
    print("✅ 模型加载成功！\n")
    
    print("⏳ 正在识别语音...")
    
    # 执行转录
    segments, info = model.transcribe(
        file_path,
        language="zh",
        beam_size=5,
        word_timestamps=False
    )
    
    # 收集结果
    result_text = ""
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        result_text += segment.text + " "
    
    return result_text.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python transcribe_local.py <音频文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        result = transcribe_audio(file_path)
        print("\n==================================================")
        print(f"📝 识别结果:\n{result}")
        # 将结果写入文件供后续使用
        with open("/tmp/voice_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)
