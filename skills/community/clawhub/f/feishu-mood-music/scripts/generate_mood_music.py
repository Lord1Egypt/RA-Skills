#!/usr/bin/env python3
"""
generate_mood_music.py - Generate mood-matching music via MiniMax Music API
Usage: python3 generate_mood_music.py --prompt "..." --output /tmp/mood.mp3 [--instrumental]
Env: MINIMAX_API_KEY (required)
"""

import argparse
import requests
import os
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, help="Music generation prompt")
    parser.add_argument("--output", required=True, help="Output MP3 path")
    parser.add_argument("--instrumental", action="store_true", help="Generate instrumental only")
    parser.add_argument("--bitrate", type=int, default=256000)
    parser.add_argument("--sample-rate", type=int, default=44100)
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        print("❌ MINIMAX_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    url = "https://api.minimaxi.com/v1/music_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "music-2.5+",
        "prompt": args.prompt,
        "is_instrumental": args.instrumental,
        "lyrics_optimizer": not args.instrumental,
        "output_format": "url",
        "aigc_watermark": False,
        "audio_setting": {
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "format": "mp3"
        }
    }

    emoji = "🎹" if args.instrumental else "🎤"
    print(f"{emoji} Generating mood music...", flush=True)
    start = time.time()

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=300)
        data = resp.json()
    except Exception as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    status_code = data.get("base_resp", {}).get("status_code", -1)
    if status_code != 0:
        msg = data.get("base_resp", {}).get("status_msg", "unknown error")
        print(f"❌ API error: {msg}", file=sys.stderr)
        sys.exit(1)

    audio_url = data.get("data", {}).get("audio", "")
    if not audio_url or not audio_url.startswith("http"):
        print("❌ No audio URL returned", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    r = requests.get(audio_url, timeout=60)
    with open(args.output, "wb") as f:
        f.write(r.content)

    elapsed = time.time() - start
    duration_ms = data.get("extra_info", {}).get("music_duration", 0)
    size_kb = os.path.getsize(args.output) / 1024

    print(f"✅ Done! {duration_ms/1000:.1f}s audio, {size_kb:.0f}KB, took {elapsed:.0f}s")
    print(f"PATH:{args.output}")

if __name__ == "__main__":
    main()
