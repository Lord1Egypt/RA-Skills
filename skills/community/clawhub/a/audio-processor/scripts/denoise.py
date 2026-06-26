#!/usr/bin/env python3
"""
audio-processor/scripts/denoise.py
音频降噪处理 - 使用 spectral gating
"""

import argparse
import os
import sys

import noisereduce as nr
import numpy as np
import soundfile as sf


def denoise(input_path: str, output_path: str, noise_sample_start: float = 0.0,
            noise_sample_duration: float = 0.5, prop_decrease: float = 1.0,
            stationary: bool = False):
    print(f"Loading: {input_path}")
    
    data, sr = sf.read(input_path)
    
    # Handle stereo
    if len(data.shape) > 1:
        print("Processing stereo channels separately...")
        result_channels = []
        for ch in range(data.shape[1]):
            ch_data = data[:, ch]
            noise_sample = ch_data[int(noise_sample_start * sr):int((noise_sample_start + noise_sample_duration) * sr)]
            reduced = nr.reduce_noise(
                y=ch_data,
                y_noise=noise_sample,
                sr=sr,
                prop_decrease=prop_decrease,
                stationary=stationary,
            )
            result_channels.append(reduced)
        result = np.stack(result_channels, axis=1)
    else:
        noise_sample = data[int(noise_sample_start * sr):int((noise_sample_start + noise_sample_duration) * sr)]
        result = nr.reduce_noise(
            y=data,
            y_noise=noise_sample,
            sr=sr,
            prop_decrease=prop_decrease,
            stationary=stationary,
        )
    
    sf.write(output_path, result, sr)
    print(f"Denoised: {input_path} -> {output_path}")
    print(f"  Noise sample: {noise_sample_start}s to {noise_sample_start + noise_sample_duration}s")
    print(f"  Prop decrease: {prop_decrease}")
    print(f"  Stationary: {stationary}")


def main():
    parser = argparse.ArgumentParser(description='Denoise audio using spectral gating')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('output', help='Output audio file')
    parser.add_argument('--noise-start', type=float, default=0.0,
                        help='Start time of noise sample (seconds)')
    parser.add_argument('--noise-duration', type=float, default=0.5,
                        help='Duration of noise sample (seconds)')
    parser.add_argument('--prop-decrease', type=float, default=1.0,
                        help='Proportion of noise to reduce (0.0-1.0)')
    parser.add_argument('--stationary', action='store_true',
                        help='Use stationary noise reduction')
    args = parser.parse_args()
    
    denoise(args.input, args.output, args.noise_start, args.noise_duration,
            args.prop_decrease, args.stationary)


if __name__ == '__main__':
    main()
