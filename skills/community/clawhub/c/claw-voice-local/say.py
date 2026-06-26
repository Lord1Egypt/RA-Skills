#!/usr/bin/env python3
"""
say.py — Main entry point: text → Telegram Voice Note.

Combines speak.py (piper TTS) + send_voice.py (Telegram Bot API).

Usage:
  python3 say.py "Hello, how are you?"
  python3 say.py "Hello" --chat-id 123456789
  python3 say.py "Hello" --speed 0.85 --model /path/to/model.onnx
  echo "Hello" | python3 say.py

Environment variables:
  TELEGRAM_BOT_TOKEN   Required: your Telegram bot token
  TELEGRAM_CHAT_ID     Default chat ID (can be overridden with --chat-id)
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).parent
SPEAK = SKILL_DIR / "speak.py"
SEND = SKILL_DIR / "send_voice.py"

DEFAULT_SPEED = "0.85"


def main():
    parser = argparse.ArgumentParser(
        description="Send a text as a Telegram voice note via piper TTS"
    )
    parser.add_argument("text", nargs="?", help="Text to speak (or use stdin)")
    parser.add_argument("--chat-id", help="Telegram chat ID (or set TELEGRAM_CHAT_ID env var)")
    parser.add_argument("--speed", default=DEFAULT_SPEED, help="Speech speed (default: 0.85, lower=slower)")
    parser.add_argument("--model", help="Path to piper .onnx voice model")
    args = parser.parse_args()

    # Text from argument or stdin
    if args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        parser.error("Provide text as argument or via stdin")

    if not text:
        print("ERROR: Empty text", file=sys.stderr)
        sys.exit(1)

    # Chat ID from argument or env
    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("ERROR: Provide --chat-id or set TELEGRAM_CHAT_ID env var", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
        ogg = Path(f.name)

    try:
        # Step 1: text → OGG via piper
        speak_cmd = [sys.executable, str(SPEAK), "--text", text,
                     "--output", str(ogg), "--length-scale", args.speed]
        if args.model:
            speak_cmd += ["--model", args.model]

        subprocess.run(speak_cmd, check=True, capture_output=True, text=True)

        # Step 2: OGG → Telegram Voice Note
        subprocess.run(
            [sys.executable, str(SEND), str(ogg), "--chat-id", chat_id],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    finally:
        if ogg.exists():
            ogg.unlink()


if __name__ == "__main__":
    main()
