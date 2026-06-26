#!/usr/bin/env python3
import sys
import argparse
from minimax_client import MinimaxClient
from executor_common import execute_voice_design


def main():
    parser = argparse.ArgumentParser(description="Design a new voice using text description via MiniMax Voice Design API")
    parser.add_argument("description", help="Text description of the desired voice")
    parser.add_argument("--preview-text", required=True, help="试听文本，官方要求必填")
    parser.add_argument("--voice-id", help="Optional custom voice ID")
    parser.add_argument("--estimate", action="store_true", help="Only show info, don't execute")
    args = parser.parse_args()

    client = MinimaxClient()
    result = execute_voice_design(client, args.description, None, None, None, args.estimate, {
        "voice_id": args.voice_id,
        "preview_text": args.preview_text,
    })
    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)
    if result.get("voice_id"):
        print(f"Voice ID: {result['voice_id']}")


if __name__ == "__main__":
    main()
