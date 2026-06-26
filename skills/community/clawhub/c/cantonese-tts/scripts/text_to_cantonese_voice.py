#!/usr/bin/env python3
"""
文字转粤语语音
Usage: python text_to_cantonese_voice.py <text> [tone] [--voice VOICE]
  tone:  normal (default), slow, fast, angry
  voice: hiuMaan (默认,女声), hiuGaai (女声), wanLung (男声)
"""

import sys
import os
import asyncio
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TONE_CONFIG = {
    "normal": {"rate": "+18%", "pitch": "+8Hz"},
    "slow": {"rate": "+0%", "pitch": "+8Hz"},
    "fast": {"rate": "+24%", "pitch": "+8Hz"},
    "angry": {"rate": "+36%", "pitch": "+12Hz"},
}

VOICE_MAP = {
    "hiuMaan": "zh-HK-HiuMaanNeural",
    "hiuGaai": "zh-HK-HiuGaaiNeural",
    "wanLung": "zh-HK-WanLungNeural",
}

VOICE_LABELS = {
    "hiuMaan": "女声·胡曼 (HiuMaan)",
    "hiuGaai": "女声·曉佳 (HiuGaai)",
    "wanLung": "男声·雲龍 (WanLung)",
}


def parse_args():
    voice = "hiuMaan"
    tone = "normal"
    positional = []
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--voice":
            i += 1
            if i >= len(args):
                print("错误：--voice 后面需要指定语音名称", file=sys.stderr)
                sys.exit(1)
            voice = args[i]
        else:
            positional.append(args[i])
        i += 1

    if len(positional) < 1:
        print("用法: python text_to_cantonese_voice.py <文字> [语气] [--voice 语音]", file=sys.stderr)
        print("  语气: normal (默认), slow, fast, angry", file=sys.stderr)
        print("  语音: hiuMaan (默认,女声), hiuGaai (女声), wanLung (男声)", file=sys.stderr)
        sys.exit(1)

    text = positional[0]
    if len(positional) > 1:
        tone = positional[1]

    return text, tone, voice


async def main():
    text, tone, voice = parse_args()

    if tone not in TONE_CONFIG:
        print(f"错误：不支持的语气 '{tone}'，可选：normal, slow, fast, angry", file=sys.stderr)
        sys.exit(1)

    if voice not in VOICE_MAP:
        print(f"错误：不支持的语音 '{voice}'，可选：hiuMaan, hiuGaai, wanLung", file=sys.stderr)
        sys.exit(1)

    tone_cfg = TONE_CONFIG[tone]
    voice_id = VOICE_MAP[voice]
    voice_label = VOICE_LABELS[voice]

    # 输出目录
    output_dir = Path.cwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 清理文件名
    safe_text = "".join(c if c.isalnum() or c in " _-" else "_" for c in text)[:30]
    output_file = output_dir / f"{timestamp}_{safe_text}.mp3"

    print(f"正在生成粤语语音...", file=sys.stderr)
    print(f"  文字: {text}", file=sys.stderr)
    print(f"  语气: {tone} (rate={tone_cfg['rate']}, pitch={tone_cfg['pitch']})", file=sys.stderr)
    print(f"  语音: {voice_label}", file=sys.stderr)
    print(f"  输出: {output_file}", file=sys.stderr)

    try:
        import edge_tts
    except ImportError:
        print("错误：请先安装 edge-tts: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    communicate = edge_tts.Communicate(
        text,
        voice=voice_id,
        rate=tone_cfg["rate"],
        pitch=tone_cfg["pitch"],
    )
    await communicate.save(str(output_file))

    file_size = output_file.stat().st_size
    print(f"[OK] 生成成功: {output_file} ({file_size / 1024:.1f} KB)")


if __name__ == "__main__":
    asyncio.run(main())
