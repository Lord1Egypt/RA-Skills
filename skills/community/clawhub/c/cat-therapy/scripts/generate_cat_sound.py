#!/usr/bin/env python3
"""
Generate a simple meow sound effect using sine waves.
Creates a .wav file that can be used for cat-therapy skill.
"""

import wave
import struct
import math
import os

def generate_meow(output_path, duration=1.0, sample_rate=44100):
    """Generate a simple meow-like sound."""
    
    num_samples = int(sample_rate * duration)
    
    # Create a frequency sweep (meow goes from high to low)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Frequency sweep from 800Hz to 400Hz (meow-like)
        freq = 800 - 400 * (t / duration)
        # Amplitude envelope (fade in and out)
        amplitude = math.sin(math.pi * t / duration) * 0.5
        # Generate sample
        sample = amplitude * math.sin(2 * math.pi * freq * t)
        samples.append(sample)
    
    # Write to WAV file
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        for sample in samples:
            # Convert to 16-bit integer
            packed = struct.pack('<h', int(sample * 32767))
            wav_file.writeframes(packed)
    
    return output_path

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    output_path = os.path.join(output_dir, "meow.wav")
    
    generate_meow(output_path)
    print(f"Generated: {output_path}")
    
    # Also generate purr sound
    purr_path = os.path.join(output_dir, "purr.wav")
    
    # Purr is a low rumble (around 25Hz)
    num_samples = 44100 * 2  # 2 seconds
    samples = []
    for i in range(num_samples):
        t = i / 44100
        # Low frequency purr
        freq = 25
        # Add some variation
        sample = 0.3 * math.sin(2 * math.pi * freq * t)
        sample += 0.1 * math.sin(2 * math.pi * (freq * 2) * t)
        sample += 0.05 * math.sin(2 * math.pi * 60 * t)  # 60Hz hum
        samples.append(sample)
    
    with wave.open(purr_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        for sample in samples:
            packed = struct.pack('<h', int(sample * 32767))
            wav_file.writeframes(packed)
    
    print(f"Generated: {purr_path}")
