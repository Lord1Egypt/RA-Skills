#!/usr/bin/env python3
"""Text-to-speech voiceover generation using Microsoft Edge TTS (free).

Usage:
  python text_to_speech.py --text "萤火虫空压机，专注节能十五年" -o narration.mp3
  python text_to_speech.py --file script.txt -o voiceover.mp3 --voice zh-CN-YunxiNeural
  python text_to_speech.py --text "Firefly Air Compressor" --lang en -o output.mp3

Requires: pip install edge-tts
"""

import argparse
import io
import os
import subprocess
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LANG = {
    "zh": {
        "missing_edge_tts": "edge-tts 未安装。请执行: pip install edge-tts",
        "generating": "生成语音中",
        "done": "完成",
        "error": "错误",
        "output": "输出文件",
        "voice": "语音",
        "rate": "语速",
        "duration": "时长",
    },
    "en": {
        "missing_edge_tts": "edge-tts not installed. Run: pip install edge-tts",
        "generating": "Generating voiceover",
        "done": "Done",
        "error": "Error",
        "output": "Output",
        "voice": "Voice",
        "rate": "Rate",
        "duration": "Duration",
    },
}

VOICE_MAP = {
    "zh": {
        "female_natural": "zh-CN-XiaoxiaoNeural",
        "male_professional": "zh-CN-YunxiNeural",
        "female_lively": "zh-CN-XiaoyiNeural",
        "male_mature": "zh-CN-YunjianNeural",
        "news_style": "zh-CN-YunyangNeural",
        "customer_service": "zh-CN-XiaochenNeural",
    },
    "en": {
        "female_natural": "en-US-JennyNeural",
        "male_professional": "en-US-GuyNeural",
        "female_lively": "en-US-AriaNeural",
    },
}

DEFAULT_VOICE = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-JennyNeural",
}


def check_edge_tts_cli():
    """Check if edge-tts CLI is available."""
    try:
        r = subprocess.run(
            ["edge-tts", "--version"], capture_output=True, text=True, timeout=10,
            shell=(sys.platform == "win32")
        )
        if r.returncode == 0:
            return True
    except Exception:
        pass
    # Try python -m edge_tts
    try:
        r = subprocess.run(
            [sys.executable, "-m", "edge_tts", "--help"], capture_output=True, text=True, timeout=10,
            shell=(sys.platform == "win32")
        )
        if r.returncode == 0:
            return True
    except Exception:
        pass
    return False


def generate_tts(text, output_path, voice, rate):
    """Generate TTS audio using edge-tts CLI."""
    rate_str = f"{rate:+d}%" if rate != 0 else "+0%"

    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--rate", rate_str,
        "--text", text,
        "--write-media", output_path,
    ]

    subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)


def main():
    parser = argparse.ArgumentParser(description="TTS voiceover generation via edge-tts")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Text to speak (inline)")
    src.add_argument("--file", help="Text file to read")
    parser.add_argument("--output", "-o", default="output_tts.mp3", help="Output MP3 file path")
    parser.add_argument("--voice", help="Edge TTS voice name (uses default for --lang if not specified)")
    parser.add_argument("--rate", type=int, default=0,
                        help="Speed adjustment: -50 to +50 (default: 0)")
    parser.add_argument("--lang", default="zh", choices=["zh", "en"],
                        help="Language for default voice selection")
    args = parser.parse_args()

    msg = LANG[args.lang]

    if not check_edge_tts_cli():
        print(f"[✗] {msg['missing_edge_tts']}")
        sys.exit(1)

    # Determine voice
    if args.voice:
        voice = args.voice
    else:
        voice = DEFAULT_VOICE[args.lang]

    # Load text
    if args.file:
        if not os.path.isfile(args.file):
            print(f"[✗] {msg['error']}: file not found - {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text

    if not text:
        print(f"[✗] {msg['error']}: no text provided")
        sys.exit(1)

    print(f"  {msg['voice']}: {voice}")
    print(f"  {msg['rate']}: {args.rate:+d}%")
    print(f"[{msg['generating']}] \"{text[:60]}{'...' if len(text) > 60 else ''}\" ...", end=" ", flush=True)

    try:
        generate_tts(text, args.output, voice, args.rate)
        size_kb = os.path.getsize(args.output) / 1024
        print(f"{msg['done']} ({size_kb:.1f} KB)")
        print(f"  {msg['output']}: {args.output}")
    except subprocess.CalledProcessError as e:
        print(f"[✗] {msg['error']}: {e.stderr.decode() if e.stderr else str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
