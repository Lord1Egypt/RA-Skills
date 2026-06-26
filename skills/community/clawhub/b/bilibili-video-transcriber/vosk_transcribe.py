#!/usr/bin/env python3
"""使用 Vosk 进行快速语音转写"""
import os
import sys
import json
import wave

output_dir = "/root/.openclaw/workspace/skills/bilibili-video-transcriber/bilibili_transcripts"
audio_file = os.path.join(output_dir, "raspberry_zero.mp3")
output_file = os.path.join(output_dir, "raspberry_zero_transcript.txt")

try:
    from vosk import Model, KaldiRecognizer
    
    print(f"🎤 使用 Vosk 转写：{audio_file}")
    print("=" * 60)
    
    # 检查模型
    model_path = os.path.expanduser("~/.cache/vosk-models/vosk-model-small-cn-0.22")
    if not os.path.exists(model_path):
        print(f"⬇️  下载 Vosk 中文模型...")
        model_path = os.path.expanduser("~/.cache/vosk-models/vosk-model-cn-0.22")
    
    if not os.path.exists(model_path):
        # 尝试自动下载
        from vosk import SetLogLevel
        SetLogLevel(-1)  # 静默下载
        print(f"📦 首次运行会自动下载模型...")
    
    print(f"📦 加载模型：{model_path}")
    model = Model(model_path)
    
    # 转换音频为 wav 格式（如果需要）
    import subprocess
    wav_file = audio_file.replace('.mp3', '.wav')
    if not os.path.exists(wav_file):
        print(f"🔄 转换音频为 WAV 格式...")
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_file,
            "-ar", "16000", "-ac", "1",
            "-f", "s16le", "-bitexact",
            wav_file + ".raw"
        ], check=True, capture_output=True)
        wav_file = wav_file + ".raw"
    
    # 转写
    print(f"🎤 开始转写...")
    recognizer = KaldiRecognizer(model, 16000)
    
    text_parts = []
    with open(wav_file, "rb") as f:
        while True:
            data = f.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if 'text' in result and result['text']:
                    text_parts.append(result['text'])
    
    # 获取最后的结果
    final_result = json.loads(recognizer.FinalResult())
    if 'text' in final_result and final_result['text']:
        text_parts.append(final_result['text'])
    
    # 合并文本
    full_text = " ".join(text_parts)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"✅ 转写完成！")
    print(f"📄 输出文件：{output_file}")
    print(f"\n📝 内容预览:\n{full_text[:500]}...")
    
except ImportError as e:
    print(f"❌ Vosk 未安装：{e}")
    print(f"💡 尝试使用 whisper 转写...")
    
    # 回退到 whisper
    import subprocess
    try:
        cmd = [
            "whisper",
            audio_file,
            "--model", "tiny",  # 使用更小的模型
            "--language", "zh",
            "--output_dir", output_dir,
            "--output_format", "txt"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if result.returncode == 0:
            print(f"✅ Whisper 转写完成！")
        else:
            print(f"❌ Whisper 转写失败：{result.stderr[:500]}")
    except Exception as we:
        print(f"❌ Whisper 也失败了：{we}")
        sys.exit(1)
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
