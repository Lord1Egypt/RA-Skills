#!/usr/bin/env python3
"""
audio-processor/scripts/merge_audio.py
多段音频合并拼接，支持淡入淡出
"""

import argparse
import os
import sys

from pydub import AudioSegment


def merge(files: list, output_path: str, fade_in: int = 0, fade_out: int = 0,
          crossfade: int = 0, padding: int = 0):
    print(f"Merging {len(files)} files...")
    
    segments = []
    for f in files:
        if not os.path.exists(f):
            print(f"Error: file not found: {f}")
            sys.exit(1)
        seg = AudioSegment.from_file(f)
        segments.append(seg)
    
    # Apply fade and crossfade
    result = segments[0]
    if fade_in > 0:
        result = result.fade_in(fade_in)
    
    for i, seg in enumerate(segments[1:], 1):
        if crossfade > 0:
            result = result.append(seg, crossfade=crossfade)
        else:
            if padding > 0:
                result += AudioSegment.silent(duration=padding)
            result += seg
    
    if fade_out > 0:
        result = result.fade_out(fade_out)
    
    # Export
    fmt = os.path.splitext(output_path)[1].lstrip('.') or 'mp3'
    result.export(output_path, format=fmt)
    
    total_duration = len(result) / 1000
    print(f"Merged: {output_path} ({total_duration:.2f}s)")


def main():
    parser = argparse.ArgumentParser(description='Merge multiple audio files')
    parser.add_argument('files', nargs='+', help='Input audio files (in order)')
    parser.add_argument('--output', '-o', required=True, help='Output file')
    parser.add_argument('--fade-in', type=int, default=0, help='Fade in duration (ms)')
    parser.add_argument('--fade-out', type=int, default=0, help='Fade out duration (ms)')
    parser.add_argument('--crossfade', type=int, default=0, help='Crossfade duration (ms)')
    parser.add_argument('--padding', type=int, default=0, help='Silent padding between files (ms)')
    args = parser.parse_args()
    
    merge(args.files, args.output, args.fade_in, args.fade_out, args.crossfade, args.padding)


if __name__ == '__main__':
    main()
