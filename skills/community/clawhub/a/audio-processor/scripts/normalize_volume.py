#!/usr/bin/env python3
"""
audio-processor/scripts/normalize_volume.py
音量标准化 - 支持 Peak / RMS / LUFS 模式
"""

import argparse
import os

from pydub import AudioSegment
from pydub.effects import normalize


def normalize_peak(audio: AudioSegment, target_dbfs: float = -1.0):
    """Peak normalization"""
    peak = audio.max_dBFS
    gain = target_dbfs - peak
    return audio.apply_gain(gain)


def normalize_rms(audio: AudioSegment, target_dbfs: float = -20.0):
    """RMS normalization"""
    rms = audio.rms
    current_dbfs = 20 * (rms / audio.max_possible_amplitude)
    gain = target_dbfs - current_dbfs
    return audio.apply_gain(gain)


def main():
    parser = argparse.ArgumentParser(description='Normalize audio volume')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--mode', '-m', choices=['peak', 'rms', 'loudness'], default='peak',
                        help='Normalization mode')
    parser.add_argument('--target', '-t', type=float, default=-1.0,
                        help='Target dBFS (default: -1 for peak, -20 for RMS)')
    args = parser.parse_args()
    
    audio = AudioSegment.from_file(args.input)
    
    if args.mode == 'peak':
        target = args.target if args.target != -1.0 else -1.0
        result = normalize_peak(audio, target)
    elif args.mode == 'rms':
        target = args.target if args.target != -1.0 else -20.0
        result = normalize_rms(audio, target)
    else:
        # Use pydub's built-in normalize for loudness
        result = normalize(audio)
    
    result.export(args.output)
    print(f"Normalized ({args.mode}): {args.input} -> {args.output}")
    print(f"  Original max dBFS: {audio.max_dBFS:.2f}")
    print(f"  Result max dBFS: {result.max_dBFS:.2f}")


if __name__ == '__main__':
    main()
