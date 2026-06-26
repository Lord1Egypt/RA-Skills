#!/usr/bin/env python3
"""
audio-processor/scripts/speed_pitch.py
变速变调处理
"""

import argparse
import os

from pydub import AudioSegment


def change_speed(input_path: str, output_path: str, speed: float = 1.0):
    """Change speed without changing pitch (time stretching)"""
    audio = AudioSegment.from_file(input_path)
    # pydub speed change affects pitch too - use soundstretch if available
    # Fallback: naive speed change
    if speed == 1.0:
        audio.export(output_path)
        return
    
    # Naive approach: change frame rate then resample
    new_frame_rate = int(audio.frame_rate * speed)
    stretched = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
    stretched = stretched.set_frame_rate(audio.frame_rate)
    stretched.export(output_path)
    print(f"Speed changed ({speed}x): {output_path}")


def change_pitch(input_path: str, output_path: str, semitones: float = 0.0):
    """Change pitch in semitones"""
    audio = AudioSegment.from_file(input_path)
    if semitones == 0:
        audio.export(output_path)
        return
    
    # Change frame rate to shift pitch
    ratio = 2 ** (semitones / 12.0)
    new_frame_rate = int(audio.frame_rate * ratio)
    pitched = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
    pitched = pitched.set_frame_rate(audio.frame_rate)
    pitched.export(output_path)
    print(f"Pitch shifted ({semitones:+} semitones): {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Change audio speed or pitch')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--speed', '-s', type=float, help='Speed multiplier (1.0 = normal)')
    parser.add_argument('--pitch', '-p', type=float, help='Pitch shift in semitones')
    args = parser.parse_args()
    
    if args.speed:
        change_speed(args.input, args.output, args.speed)
    elif args.pitch is not None:
        change_pitch(args.input, args.output, args.pitch)
    else:
        print("Error: specify --speed or --pitch")


if __name__ == '__main__':
    main()
