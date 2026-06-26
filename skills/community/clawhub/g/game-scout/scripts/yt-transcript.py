#!/usr/bin/env python3
"""Fetch YouTube video transcript using yt-dlp. Outputs clean plain text."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def clean_vtt(content: str) -> str:
    """Clean WebVTT content to plain text, removing timestamps and duplicates."""
    lines = content.splitlines()
    text_lines = []
    timestamp_pattern = re.compile(
        r"\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s\d{2}:\d{2}:\d{2}\.\d{3}"
    )

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT" or line.isdigit():
            continue
        if timestamp_pattern.match(line):
            continue
        if line.startswith("NOTE") or line.startswith("STYLE"):
            continue
        if text_lines and text_lines[-1] == line:
            continue
        line = re.sub(r"<[^>]+>", "", line)
        text_lines.append(line)

    return "\n".join(text_lines)


def get_metadata(url: str) -> dict:
    """Get video title, channel, and description."""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--skip-download",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        import json

        data = json.loads(result.stdout)
        return {
            "title": data.get("title", ""),
            "channel": data.get("channel", data.get("uploader", "")),
            "upload_date": data.get("upload_date", ""),
            "view_count": data.get("view_count", 0),
            "description": data.get("description", ""),
            "duration": data.get("duration_string", ""),
        }
    except (subprocess.CalledProcessError, Exception):
        return {}


def get_transcript(url: str, include_meta: bool = True):
    """Fetch and print the transcript."""
    if include_meta:
        meta = get_metadata(url)
        if meta:
            print(f"## {meta.get('title', 'Unknown')}")
            print(f"**Channel**: {meta.get('channel', 'Unknown')}")
            date = meta.get("upload_date", "")
            if date and len(date) == 8:
                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            print(f"**Date**: {date}")
            print(f"**Views**: {meta.get('view_count', 'N/A')}")
            print(f"**Duration**: {meta.get('duration', 'N/A')}")
            desc = meta.get("description", "")
            if desc:
                # Truncate long descriptions
                if len(desc) > 1000:
                    desc = desc[:1000] + "..."
                print(f"\n### Description\n{desc}")
            print("\n### Transcript\n")

    with tempfile.TemporaryDirectory() as temp_dir:
        cmd = [
            "yt-dlp",
            "--write-subs",
            "--write-auto-subs",
            "--skip-download",
            "--sub-lang",
            "en",
            "--output",
            "subs",
            url,
        ]

        try:
            subprocess.run(cmd, cwd=temp_dir, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(
                f"Error running yt-dlp: {e.stderr.decode()}", file=sys.stderr
            )
            sys.exit(1)
        except FileNotFoundError:
            print(
                "Error: yt-dlp not found. Install with: brew install yt-dlp",
                file=sys.stderr,
            )
            sys.exit(1)

        temp_path = Path(temp_dir)
        vtt_files = list(temp_path.glob("*.vtt"))

        if not vtt_files:
            print("No subtitles found for this video.", file=sys.stderr)
            sys.exit(1)

        content = vtt_files[0].read_text(encoding="utf-8")
        print(clean_vtt(content))


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube transcript with metadata."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--no-meta",
        action="store_true",
        help="Skip metadata (title, channel, etc.)",
    )
    args = parser.parse_args()
    get_transcript(args.url, include_meta=not args.no_meta)


if __name__ == "__main__":
    main()
