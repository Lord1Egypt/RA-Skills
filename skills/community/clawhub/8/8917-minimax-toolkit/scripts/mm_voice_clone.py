#!/usr/bin/env python3
import sys
import argparse
from minimax_client import MinimaxClient
from executor_common import execute_voice_clone


def main():
    parser = argparse.ArgumentParser(description="Clone a voice using MiniMax Voice Clone")
    parser.add_argument("audio", help="Path to audio file to clone (mp3/m4a/wav)")
    parser.add_argument("--prompt-audio", help="Optional: Path to sample audio for quality enhancement")
    parser.add_argument("--prompt-text", help="Text corresponding to --prompt-audio")
    parser.add_argument("--preview-text", help="Optional试听文本；提供后会返回试听音频")
    parser.add_argument("--voice-id", required=True, help="Custom voice ID to assign")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    client = MinimaxClient()
    result = execute_voice_clone(client, args.audio, "speech-2.8-hd", None, None, args.estimate, {
        "voice_id": args.voice_id,
        "prompt_audio": args.prompt_audio,
        "prompt_text": args.prompt_text,
        "preview_text": args.preview_text,
    })
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("voice_id"):
        print(f"Voice ID: {result['voice_id']}")


if __name__ == "__main__":
    main()
