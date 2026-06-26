#!/usr/bin/env python3
import argparse
import base64
import os
import sys
from pathlib import Path

import requests


DEFAULT_VOICE_ID = "2001286865130360832"
TTS_URL = "https://studio.mosi.cn/v1/audio/tts"


def fail(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def main():
    parser = argparse.ArgumentParser(description="Call MOSS-TTS and save wav file")
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice_id", default=DEFAULT_VOICE_ID)
    parser.add_argument("--output", default="output.wav")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    if not args.text.strip():
        fail("--text cannot be empty")

    api_key = os.getenv("MOSS_API_KEY")
    if not api_key:
        fail("MOSS_API_KEY is not set")

    out_path = Path(args.output)
    if out_path.parent and not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "moss-tts",
        "text": args.text,
        "voice_id": args.voice_id,
        "sampling_params": {"temperature": 1.7, "top_p": 0.8, "top_k": 25},
    }

    try:
        resp = requests.post(TTS_URL, json=payload, headers=headers, timeout=args.timeout)
    except requests.RequestException as e:
        fail(f"request failed: {e}")

    if resp.status_code != 200:
        fail(f"HTTP {resp.status_code}: {resp.text[:300]}")

    try:
        data = resp.json()
    except ValueError:
        fail(f"non-JSON response: {resp.text[:300]}")

    audio_data = data.get("audio_data")
    if not audio_data:
        fail(f"missing audio_data in response: {data}")

    try:
        audio_bytes = base64.b64decode(audio_data)
    except Exception as e:
        fail(f"invalid base64 audio_data: {e}")

    out_path.write_bytes(audio_bytes)
    print(f"Successfully saved to {out_path}")


if __name__ == "__main__":
    main()
