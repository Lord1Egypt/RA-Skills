#!/usr/bin/env python3
"""
audio-processor/scripts/batch_process.py
批量处理目录中的音频文件
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def batch_convert(input_dir: str, output_dir: str, target_format: str, bitrate: str = None):
    os.makedirs(output_dir, exist_ok=True)
    supported = {'.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a', '.opus', '.wma'}
    
    files = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in supported]
    print(f"Found {len(files)} audio files to convert")
    
    for f in files:
        output_path = os.path.join(output_dir, f.stem + '.' + target_format)
        cmd = ['python3', os.path.join(os.path.dirname(__file__), 'convert_format.py'),
               str(f), output_path]
        if bitrate:
            cmd.extend(['--bitrate', bitrate])
        subprocess.run(cmd)


def batch_analyze(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    supported = {'.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a'}
    
    files = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in supported]
    print(f"Found {len(files)} audio files to analyze")
    
    for f in files:
        report_dir = os.path.join(output_dir, f.stem)
        cmd = ['python3', os.path.join(os.path.dirname(__file__), 'analyze_audio.py'),
               str(f), '--output', report_dir]
        subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description='Batch process audio files')
    parser.add_argument('input_dir', help='Input directory')
    parser.add_argument('--action', '-a', choices=['convert', 'analyze', 'denoise'],
                        required=True, help='Batch action')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory')
    parser.add_argument('--format', '-f', help='Target format (for convert)')
    parser.add_argument('--bitrate', '-b', help='Target bitrate')
    args = parser.parse_args()
    
    if args.action == 'convert':
        if not args.format:
            print("Error: --format required for convert action")
            sys.exit(1)
        batch_convert(args.input_dir, args.output_dir, args.format, args.bitrate)
    elif args.action == 'analyze':
        batch_analyze(args.input_dir, args.output_dir)
    elif args.action == 'denoise':
        # TODO: implement batch denoise
        print("Batch denoise not yet implemented")


if __name__ == '__main__':
    main()
