#!/usr/bin/env python3
"""
parse_subtitle.py - Parse SRT/VTT subtitles to plain text
Usage: python3 parse.py <subtitle_file.srt> [output.txt]

Removes:
  - Sequence numbers
  - Timestamps
  - HTML-like tags
  - Duplicate consecutive lines
"""
import re
import sys

def parse_subtitle(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    result = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+$', line):  # sequence numbers
            continue
        if re.match(r'^\d{2}:\d{2}:\d{2}', line):  # timestamps
            continue
        if '-->' in line:  # timestamp lines
            continue
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            result.append(clean)

    # Deduplicate consecutive identical lines
    deduped = []
    prev = None
    for r in result:
        if r != prev:
            deduped.append(r)
            prev = r

    return ' '.join(deduped)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse.py <subtitle_file.srt> [output.txt]", file=sys.stderr)
        sys.exit(1)

    subtitle_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    text = parse_subtitle(subtitle_path)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Parsed {len(text)} chars to: {output_path}")
    else:
        print(text)
