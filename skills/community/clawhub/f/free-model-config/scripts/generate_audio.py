#!/usr/bin/env python3
"""
音频生成工具（简单合成音频）。

当没有 TTS 工具时，可使用此脚本生成简单的合成音频。
适用于生成喊叫声、背景音效等。

用法:
  python generate_audio.py --output shout.wav --duration 5.0
  python generate_audio.py --output shout.wav --duration 5.0 --frequencies 200,400,600,800
"""

import argparse
import wave
import struct
import math
import random

def generate_shout_audio(filename, duration=5.0, sample_rate=44100, frequencies=None, amplitudes=None):
    """生成一个简单的喊叫音频文件"""
    if frequencies is None:
        frequencies = [200, 400, 600, 800]  # 基频和谐波
    if amplitudes is None:
        amplitudes = [0.3, 0.2, 0.15, 0.1]
    
    num_samples = int(duration * sample_rate)
    
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        sample = 0
        
        # 添加多个频率成分
        for freq, amp in zip(frequencies, amplitudes):
            sample += amp * math.sin(2 * math.pi * freq * t)
        
        # 添加一些随机噪声模拟喊叫
        sample += random.uniform(-0.1, 0.1)
        
        # 添加包络（淡入淡出）
        envelope = 1.0
        if t < 0.1:  # 淡入
            envelope = t / 0.1
        elif t > duration - 0.1:  # 淡出
            envelope = (duration - t) / 0.1
        
        sample *= envelope
        
        # 限制在[-1, 1]范围内
        sample = max(-1.0, min(1.0, sample))
        
        # 转换为16位整数
        sample_int = int(sample * 32767)
        samples.append(sample_int)
    
    # 写入WAV文件
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        
        # 打包样本数据
        sample_data = struct.pack(f'<{len(samples)}h', *samples)
        wav_file.writeframes(sample_data)
    
    print(f"音频文件已生成: {filename}")
    print(f"时长: {duration}秒, 采样率: {sample_rate}Hz")
    print(f"频率成分: {frequencies}")
    print(f"振幅: {amplitudes}")

def main():
    parser = argparse.ArgumentParser(description="简单音频生成工具")
    parser.add_argument("--output", "-o", required=True, help="输出音频文件路径")
    parser.add_argument("--duration", "-d", type=float, default=5.0, help="音频时长（秒）")
    parser.add_argument("--sample-rate", "-s", type=int, default=44100, help="采样率（Hz）")
    parser.add_argument("--frequencies", "-f", help="频率成分（逗号分隔，如 200,400,600,800）")
    parser.add_argument("--amplitudes", "-a", help="振幅成分（逗号分隔，如 0.3,0.2,0.15,0.1）")
    
    args = parser.parse_args()
    
    frequencies = None
    amplitudes = None
    
    if args.frequencies:
        frequencies = [float(f) for f in args.frequencies.split(",")]
    if args.amplitudes:
        amplitudes = [float(a) for a in args.amplitudes.split(",")]
    
    generate_shout_audio(
        filename=args.output,
        duration=args.duration,
        sample_rate=args.sample_rate,
        frequencies=frequencies,
        amplitudes=amplitudes
    )

if __name__ == "__main__":
    main()