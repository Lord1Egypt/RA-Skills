#!/usr/bin/env python3
"""
audio-processor/scripts/cut_audio.py
按时间码裁剪音频
"""

import argparse
import os
import subprocess
import sys


def time_to_seconds(t: str) -> float:
    """Convert hh:mm:ss or mm:ss or ss to seconds"""
    parts = t.split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    else:
        return float(parts[0])


def cut(input_path: str, output_path: str, start: str = None, end: str = None, duration: str = None):
    cmd = ['ffmpeg', '-y', '-i', input_path]
    
    if start:
        cmd.extend(['-ss', str(time_to_seconds(start))])
    if duration:
        cmd.extend(['-t', str(time_to_seconds(duration))])
    elif end:
        end_sec = time_to_seconds(end)
        start_sec = time_to_seconds(start) if start else 0
        cmd.extend(['-t', str(end_sec - start_sec)])
    
    # Copy codec to avoid re-encoding when possible
    cmd.extend(['-c', 'copy'])
    cmd.append(output_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        sys.exit(1)
    print(f"Cut: {input_path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Cut audio by timecode')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--start', '-s', help='Start time (hh:mm:ss or mm:ss or ss)')
    parser.add_argument('--end', '-e', help='End time (hh:mm:ss or mm:ss or ss)')
    parser.add_argument('--duration', '-d', help='Duration (hh:mm:ss or mm:ss or ss)')
    args = parser.parse_args()
    
    if not args.start and not args.end and not args.duration:
        print("Error: must specify at least one of --start, --end, --duration")
        sys.exit(1)
    
    cut(args.input, args.output, args.start, args.end, args.duration)


if __name__ == '__main__':
    main()
