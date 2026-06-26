#!/usr/bin/env python3
"""使用 Whisper tiny 模型快速转写"""
import os
import sys
import subprocess

output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"
audio_file = os.path.join(output_dir, "raspberry_zero.mp3")

print(f"🎤 使用 Whisper tiny 模型转写：{audio_file}")
print("=" * 60)

try:
    # 使用 whisper 命令行，tiny 模型更快
    cmd = [
        "whisper",
        audio_file,
        "--model", "tiny",  # 最小最快的模型
        "--language", "zh",
        "--output_dir", output_dir,
        "--output_format", "txt",
        "--task", "transcribe"
    ]
    
    print(f"⏳ 开始转写（约需 5-10 分钟）...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    
    if result.returncode == 0:
        print(f"✅ 转写完成！")
        
        # 查找输出文件
        for f in os.listdir(output_dir):
            if f.startswith("raspberry_zero") and f.endswith(".txt"):
                transcript_file = os.path.join(output_dir, f)
                with open(transcript_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                print(f"\n📄 转写文件：{transcript_file}")
                print(f"📝 完整内容:\n")
                print(content)
                break
    else:
        print(f"❌ 转写失败:\n{result.stderr[:1000]}")
        sys.exit(1)
        
except subprocess.TimeoutExpired:
    print(f"❌ 转写超时（超过 15 分钟）")
    sys.exit(1)
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
