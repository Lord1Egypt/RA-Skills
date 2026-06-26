#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient, get_standard_path

def main():
    parser = argparse.ArgumentParser(description="Generate speech using MiniMax speech-2.8-hd")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--voice", default="male-qn-qingse", help="Voice ID")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5-2.0)")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Print budget report
    print(client.get_budget_report("speech-2.8-hd", text_len=len(args.text)))
    if args.estimate:
        sys.exit(0)

    data = {
        "model": "speech-2.8-hd",
        "text": args.text,
        "stream": False,
        "voice_setting": {
            "voice_id": args.voice,
            "speed": args.speed,
            "vol": 1.0,
            "pitch": 0
        },
        "output_format": "url"
    }

    print(f"Synthesizing speech...")
    resp = client.post("t2a_v2", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["audio"]
        
        target_dir, filename_base = get_standard_path("TTS", project=args.project, prompt_slug=args.text[:20])
        filepath = os.path.join(target_dir, f"{filename_base}.mp3")
        
        audio_data = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        print(f"Success! Audio saved to: {filepath}")
        print(f"MEDIA:{filepath}")
    else:
        print(f"Error: {resp}")

if __name__ == "__main__":
    main()
