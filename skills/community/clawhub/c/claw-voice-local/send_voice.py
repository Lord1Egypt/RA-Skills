#!/usr/bin/env python3
"""
send_voice.py — Send an OGG file as a Telegram voice note.

No dependencies beyond Python stdlib.

Usage:
  python3 send_voice.py /tmp/output.ogg --chat-id 123456789
  python3 send_voice.py /tmp/output.ogg --caption "Agent speaking"

Token resolution order:
  1. TELEGRAM_BOT_TOKEN environment variable
  2. TELEGRAM_CHAT_ID environment variable (for --chat-id)
"""

import argparse
import json
import os
import sys
from pathlib import Path


def send_voice(ogg_path: Path, chat_id: str, bot_token: str, caption: str | None = None) -> dict:
    """Upload OGG file as Telegram voice message. Returns API response dict."""
    import urllib.request

    url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
    boundary = "----ClawVoiceBoundary"

    def _field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    parts: list[bytes] = [_field("chat_id", chat_id)]
    if caption:
        parts.append(_field("caption", caption))

    data = ogg_path.read_bytes()
    parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="voice"; filename="{ogg_path.name}"\r\n'
            f"Content-Type: audio/ogg\r\n\r\n"
        ).encode("utf-8")
        + data
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))

    body = b"".join(parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    parser = argparse.ArgumentParser(description="Send OGG file as Telegram voice note")
    parser.add_argument("ogg", help="Path to .ogg file")
    parser.add_argument("--chat-id", help="Telegram chat ID (or set TELEGRAM_CHAT_ID env var)")
    parser.add_argument("--caption", help="Optional caption text")
    args = parser.parse_args()

    ogg_path = Path(args.ogg)
    if not ogg_path.exists():
        print(f"ERROR: File not found: {ogg_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve chat ID
    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("ERROR: Provide --chat-id or set TELEGRAM_CHAT_ID env var", file=sys.stderr)
        sys.exit(1)

    # Resolve bot token
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print(
            "ERROR: TELEGRAM_BOT_TOKEN not found.\n"
            "  Set it as environment variable: export TELEGRAM_BOT_TOKEN=your_token",
            file=sys.stderr,
        )
        sys.exit(1)

    result = send_voice(ogg_path, chat_id, bot_token, args.caption)
    if result.get("ok"):
        print(f"Sent: message_id={result['result']['message_id']}")
    else:
        print(f"Telegram API error: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
