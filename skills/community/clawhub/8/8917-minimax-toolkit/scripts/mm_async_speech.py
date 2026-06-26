#!/usr/bin/env python3
import sys
import argparse
from minimax_client import MinimaxClient
from executor_common import execute_async_speech


def main():
    parser = argparse.ArgumentParser(description="Asynchronous long-text speech synthesis")
    parser.add_argument("text_or_file", help="Text to synthesize, or path to a .txt file")
    parser.add_argument("--voice", default="male-qn-qingse", help="Voice ID")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--format", default="mp3", choices=["mp3", "pcm", "flac", "wav"], help="Audio format")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    client = MinimaxClient()
    result = execute_async_speech(client, args.text_or_file, "speech-2.8-hd", args.project, args.output_dir, args.estimate, {
        "voice": args.voice,
        "speed": args.speed,
        "format": args.format,
    })
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("filepath"):
        print(f"MEDIA:{result['filepath']}")


if __name__ == "__main__":
    main()
