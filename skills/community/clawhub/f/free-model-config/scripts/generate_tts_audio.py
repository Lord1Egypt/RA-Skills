#!/usr/bin/env python3
"""
TTS语音合成工具（多人配音）。

使用edge-tts生成多人语音配音，支持中文。
需要安装：pip install edge-tts

用法:
  python generate_tts_audio.py --text "王太平" --output speech.mp3
  python generate_tts_audio.py --text "王太平" --voice zh-CN-YunxiNeural --output speech.mp3
  python generate_tts_audio.py --text "王太平" --voices zh-CN-YunxiNeural,zh-CN-YunyangNeural --output speech.mp3 --mix
"""

import argparse
import asyncio
import os
import sys
import subprocess
import tempfile

# 可用的中文声音列表
CHINESE_VOICES = {
    "男声": [
        "zh-CN-YunxiNeural",      # 年轻男声
        "zh-CN-YunyangNeural",    # 成熟男声
        "zh-CN-YunjianNeural",    # 沉稳男声
    ],
    "女声": [
        "zh-CN-XiaoxiaoNeural",   # 年轻女声
        "zh-CN-XiaoyiNeural",     # 温柔女声
        "zh-CN-XiaochenNeural",   # 活泼女声
    ]
}

async def generate_speech(text, voice, output_file):
    """使用edge-tts生成语音"""
    try:
        import edge_tts
    except ImportError:
        print("错误: 请先安装edge-tts: pip install edge-tts", file=sys.stderr)
        sys.exit(1)
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"语音已生成: {output_file} (声音: {voice})", file=sys.stderr)

async def generate_multiple_speeches(text, voices, output_file, mix=False):
    """生成多人语音"""
    if not mix:
        # 不混合，只生成第一个声音
        await generate_speech(text, voices[0], output_file)
        return
    
    # 混合多个声音
    temp_files = []
    for i, voice in enumerate(voices):
        temp_file = tempfile.mktemp(suffix=".mp3")
        await generate_speech(text, voice, temp_file)
        temp_files.append(temp_file)
    
    # 使用ffmpeg混合音频（如果可用）
    ffmpeg_path = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True).stdout.strip()
    
    if ffmpeg_path and len(temp_files) > 1:
        # 使用ffmpeg混合
        inputs = []
        for f in temp_files:
            inputs.extend(["-i", f])
        
        filter_complex = f"amix=inputs={len(temp_files)}:duration=longest"
        cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_complex, output_file]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"多人语音已混合: {output_file}", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg混合失败: {e}", file=sys.stderr)
            # 回退：只使用第一个声音
            os.rename(temp_files[0], output_file)
    else:
        # 没有ffmpeg，只使用第一个声音
        os.rename(temp_files[0], output_file)
        print(f"警告: 没有ffmpeg，只使用第一个声音", file=sys.stderr)
    
    # 清理临时文件
    for f in temp_files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass

def list_voices():
    """列出可用的声音"""
    print("\n可用的中文声音：", file=sys.stderr)
    for category, voices in CHINESE_VOICES.items():
        print(f"\n{category}:", file=sys.stderr)
        for voice in voices:
            print(f"  - {voice}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="TTS语音合成工具（多人配音）")
    parser.add_argument("--text", "-t", required=True, help="要合成的文本")
    parser.add_argument("--voice", "-v", default="zh-CN-YunxiNeural", help="声音名称（默认: zh-CN-YunxiNeural）")
    parser.add_argument("--voices", help="多个声音名称（逗号分隔）")
    parser.add_argument("--output", "-o", required=True, help="输出音频文件路径")
    parser.add_argument("--mix", "-m", action="store_true", help="混合多个声音")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用的声音")
    
    args = parser.parse_args()
    
    if args.list:
        list_voices()
        return
    
    # 确定使用的声音列表
    if args.voices:
        voices = [v.strip() for v in args.voices.split(",")]
    else:
        voices = [args.voice]
    
    print(f"文本: {args.text}", file=sys.stderr)
    print(f"声音: {voices}", file=sys.stderr)
    print(f"输出: {args.output}", file=sys.stderr)
    
    # 运行异步函数
    asyncio.run(generate_multiple_speeches(args.text, voices, args.output, args.mix))

if __name__ == "__main__":
    main()