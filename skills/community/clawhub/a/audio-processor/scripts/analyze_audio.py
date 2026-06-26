#!/usr/bin/env python3
"""
audio-processor/scripts/analyze_audio.py
音频特征分析工具 - 波形/频谱/BPM/音量
"""

import argparse
import json
import os
import sys

import librosa
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def analyze(input_path: str, output_dir: str = None, plot: bool = True):
    print(f"Analyzing: {input_path}")
    
    # Load audio
    y, sr = librosa.load(input_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # Basic info
    info = {
        'file': input_path,
        'duration_sec': round(duration, 3),
        'duration_formatted': f"{int(duration // 60)}:{duration % 60:05.2f}",
        'sample_rate': sr,
        'channels': 1 if len(y.shape) == 1 else y.shape[0],
        'samples': len(y),
        'bit_depth': 'unknown (via librosa)',
    }
    
    # Volume analysis
    rms = np.sqrt(np.mean(y**2))
    dbfs = 20 * np.log10(rms) if rms > 0 else -float('inf')
    peak = np.max(np.abs(y))
    
    info['volume'] = {
        'rms': round(float(rms), 6),
        'dbfs': round(float(dbfs), 2),
        'peak': round(float(peak), 6),
        'peak_dbfs': round(20 * np.log10(peak) if peak > 0 else -float('inf'), 2),
    }
    
    # BPM detection
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        info['bpm'] = round(float(tempo), 1)
    except Exception as e:
        info['bpm'] = None
        info['bpm_error'] = str(e)
    
    # Spectral features
    try:
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        info['spectral'] = {
            'centroid_mean_hz': round(float(np.mean(spectral_centroids)), 1),
            'rolloff_mean_hz': round(float(np.mean(spectral_rolloff)), 1),
        }
    except Exception as e:
        info['spectral_error'] = str(e)
    
    # Zero crossing rate (noisiness indicator)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    info['zero_crossing_rate'] = round(float(np.mean(zcr)), 6)
    
    # Silence detection
    hop_length = 512
    frame_length = 2048
    rms_frames = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    silence_threshold = 0.01
    silent_frames = np.sum(rms_frames < silence_threshold)
    total_frames = len(rms_frames)
    
    info['silence'] = {
        'threshold': silence_threshold,
        'silent_frames': int(silent_frames),
        'total_frames': int(total_frames),
        'silence_ratio': round(float(silent_frames / total_frames), 4),
        'estimated_silence_sec': round(float(silent_frames * hop_length / sr), 2),
    }
    
    # Output report
    print("\n--- Analysis Report ---")
    print(json.dumps(info, indent=2, ensure_ascii=False))
    
    # Save JSON
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, 'analysis_report.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"\nReport saved: {json_path}")
    
    # Plot visualizations
    if plot and output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # Waveform
        ax1 = axes[0]
        times = np.linspace(0, duration, len(y))
        ax1.plot(times, y, linewidth=0.5)
        ax1.set_title('Waveform')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.set_xlim(0, duration)
        
        # Spectrogram
        ax2 = axes[1]
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=ax2)
        ax2.set_title('Spectrogram')
        fig.colorbar(img, ax=ax2, format='%+2.0f dB')
        
        # RMS over time
        ax3 = axes[2]
        rms_times = librosa.times_like(rms_frames, sr=sr, hop_length=hop_length)
        ax3.plot(rms_times, rms_frames)
        ax3.axhline(y=silence_threshold, color='r', linestyle='--', label='silence threshold')
        ax3.set_title('RMS Volume Over Time')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('RMS')
        ax3.legend()
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'analysis_plots.png')
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Plots saved: {plot_path}")
    
    return info


def main():
    parser = argparse.ArgumentParser(description='Analyze audio features')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('--output', '-o', help='Output directory for report and plots')
    parser.add_argument('--no-plot', action='store_true', help='Skip generating plots')
    args = parser.parse_args()
    
    analyze(args.input, args.output, plot=not args.no_plot)


if __name__ == '__main__':
    main()
