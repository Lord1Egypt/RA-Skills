#!/usr/bin/env python3
"""Parse timed lyrics and generate TTS audio segments for karaoke-style sync."""

import argparse
import re
import sys
import os
from pathlib import Path

def parse_timestamp(ts: str) -> int:
    """Convert MM:SS to milliseconds."""
    parts = ts.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid timestamp {ts}")
    mins, secs = int(parts[0]), int(parts[1])
    return mins * 60 * 1000 + secs * 1000

def parse_lyrics_file(filepath: str) -> list[tuple[int, str]]:
    """Parse timed lyrics file, return list of (timestamp_ms, text)."""
    entries = []
    pattern = re.compile(r"\[(\d+:\d+)\]\s*(.+)")
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.rstrip("\n")
            match = pattern.match(line)
            if match:
                ts = parse_timestamp(match.group(1))
                text = match.group(2).strip()
                entries.append((ts, text))
            elif line.strip() and not line.strip().startswith("#"):
                print(f"Skipping line {i+1}: {line[:50]}", file=sys.stderr)
    return entries

def build_playback_txt(entries: list[tuple[int, str]], output_dir: str) -> str:
    """Generate playback.txt content."""
    lines = ["# discord-music-sync playback guide", "# Format: timestamp_ms|filename|text", ""]
    for i, (ts, text) in enumerate(entries):
        filename = f"lyric_{i+1:03d}_{ts//60000:02d}-{ts%60000//1000:02d}.mp3"
        lines.append(f"{ts}|{filename}|{text}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Parse timed lyrics for TTS generation")
    parser.add_argument("--lyrics", required=True, help="Path to lyrics file")
    parser.add_argument("--output", required=True, help="Output directory for audio files")
    parser.add_argument("--voice", default="Charming_Lady", help="TTS voice ID")
    args = parser.parse_args()

    entries = parse_lyrics_file(args.lyrics)
    if not entries:
        print("No timed lyrics found. Use format [MM:SS] <text> per line.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    # Write playback guide
    playback_path = Path(args.output) / "playback.txt"
    with open(playback_path, "w", encoding="utf-8") as f:
        f.write(build_playback_txt(entries, args.output))

    print(f"Parsed {len(entries)} lyric lines")
    print(f"Playback guide: {playback_path}")
    print(f"\nNext step: Call minimax__text_to_audio for each line,")
    print(f"using output_directory='{args.output}' and filenames from playback.txt")
    print(f"\nVoice: {args.voice}")

if __name__ == "__main__":
    main()