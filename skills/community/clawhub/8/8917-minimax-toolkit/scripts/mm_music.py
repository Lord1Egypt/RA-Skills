#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient, get_standard_path


def main():
    parser = argparse.ArgumentParser(description="Generate music using MiniMax music-2.5+")
    parser.add_argument("prompt", help="Text prompt for music generation")
    parser.add_argument("--lyrics", default="", help="Lyrics for the song")
    parser.add_argument("--instrumental", action="store_true", help="Generate instrumental music")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report("Music-2.5+"))
    if args.estimate:
        sys.exit(0)

    data = {
        "model": "music-2.5+",
        "prompt": args.prompt,
        "is_instrumental": args.instrumental,
        "output_format": "url"
    }
    if args.lyrics:
        data["lyrics"] = args.lyrics
    elif not args.instrumental:
        data["lyrics_optimizer"] = True

    print(f"Generating music: {args.prompt}...")
    resp = client.post("music_generation", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["audio"]
        target_dir, filename_base = get_standard_path("MSC", project=args.project, prompt_slug=args.prompt, output_dir=args.output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.mp3")

        music_data = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(music_data)

        client.print_saved_result(filepath, "Music", project=args.project)
        print(f"MEDIA:{filepath}")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
