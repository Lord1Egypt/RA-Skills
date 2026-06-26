#!/usr/bin/env python3
"""
audio-processor/scripts/detect_silence.py
静音检测与自动分割
"""

import argparse
import os

from pydub import AudioSegment
from pydub.silence import detect_nonsilent, detect_nonsilent_ranges


def split_on_silence(input_path: str, output_dir: str, min_length: int = 1000,
                     silence_thresh: int = -40, keep_silence: int = 300):
    audio = AudioSegment.from_file(input_path)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Detect non-silent ranges
    ranges = detect_nonsilent(audio, min_silence_len=min_length, silence_thresh=silence_thresh)
    
    if not ranges:
        print("No non-silent segments found")
        return []
    
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    files = []
    
    for i, (start, end) in enumerate(ranges):
        # Add padding
        start = max(0, start - keep_silence)
        end = min(len(audio), end + keep_silence)
        
        segment = audio[start:end]
        output_path = os.path.join(output_dir, f"{base_name}_segment_{i+1:03d}.wav")
        segment.export(output_path, format='wav')
        files.append(output_path)
        print(f"Segment {i+1}: {start/1000:.2f}s - {end/1000:.2f}s -> {output_path}")
    
    print(f"\nSplit into {len(files)} segments")
    return files


def main():
    parser = argparse.ArgumentParser(description='Detect silence and split audio')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory')
    parser.add_argument('--min-length', '-l', type=int, default=1000,
                        help='Minimum silence length to consider (ms)')
    parser.add_argument('--threshold', '-t', type=int, default=-40,
                        help='Silence threshold in dBFS')
    parser.add_argument('--keep-silence', '-k', type=int, default=300,
                        help='Silence padding around segments (ms)')
    args = parser.parse_args()
    
    split_on_silence(args.input, args.output_dir, args.min_length, args.threshold, args.keep_silence)


if __name__ == '__main__':
    main()
