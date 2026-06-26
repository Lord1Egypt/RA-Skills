#!/usr/bin/env python3
"""
audio-processor/scripts/convert_format.py
音频格式转换工具
支持 MP3 / WAV / FLAC / OGG / AAC / M4A / OPUS
"""

import argparse
import os
import subprocess
import sys

SUPPORTED_FORMATS = {'mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a', 'opus', 'wma'}

FFMPEG_CODECS = {
    'mp3': 'libmp3lame',
    'ogg': 'libvorbis',
    'aac': 'aac',
    'm4a': 'aac',
    'opus': 'libopus',
    'flac': 'flac',
    'wav': 'pcm_s16le',
}


def convert(input_path: str, output_path: str, bitrate: str = None, sample_rate: int = None, channels: int = None):
    ext = os.path.splitext(output_path)[1].lstrip('.').lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"Error: unsupported format '{ext}'. Supported: {SUPPORTED_FORMATS}")
        sys.exit(1)
    
    cmd = ['ffmpeg', '-y', '-i', input_path]
    
    codec = FFMPEG_CODECS.get(ext)
    if codec:
        cmd.extend(['-c:a', codec])
    
    if bitrate:
        cmd.extend(['-b:a', bitrate])
    if sample_rate:
        cmd.extend(['-ar', str(sample_rate)])
    if channels:
        cmd.extend(['-ac', str(channels)])
    
    cmd.append(output_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        sys.exit(1)
    print(f"Converted: {input_path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Convert audio format')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--bitrate', '-b', help='Target bitrate (e.g. 320k, 128k)')
    parser.add_argument('--sample-rate', '-ar', type=int, help='Target sample rate (Hz)')
    parser.add_argument('--channels', '-ac', type=int, help='Target channel count')
    args = parser.parse_args()
    
    convert(args.input, args.output, args.bitrate, args.sample_rate, args.channels)


if __name__ == '__main__':
    main()
