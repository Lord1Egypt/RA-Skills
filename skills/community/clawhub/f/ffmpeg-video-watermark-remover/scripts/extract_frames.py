#!/usr/bin/env python3
"""
Video Watermark Remover - Helper Script
Extracts frames from video at regular intervals for watermark analysis.
"""
import subprocess
import json
import sys
from pathlib import Path

def get_video_info(input_path):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_path]
    data = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    vid = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
    if not vid:
        raise ValueError(f"No video stream found in {input_path}")
    
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', input_path]
    data = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    duration = float(data['format']['duration'])
    
    return vid['width'], vid['height'], duration

def extract_sample_frames(input_path, output_dir, interval=1.0):
    """Extract frames at regular intervals for watermark detection."""
    _, _, duration = get_video_info(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frames = []
    num_samples = int(duration / interval)
    for i in range(num_samples + 1):
        t = i * interval
        if t > duration:
            break
        frame_path = output_dir / f"frame_{i:03d}.jpg"
        cmd = [
            'ffmpeg', '-y', '-ss', f'{t:.2f}',
            '-i', input_path,
            '-frames:v', '1', '-q:v', '2',
            str(frame_path)
        ]
        subprocess.run(cmd, capture_output=True)
        if frame_path.exists():
            frames.append((t, frame_path))
            print(f"  t={t:.2f}s: {frame_path}")
    
    return frames

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: extract_frames.py <input_video> <output_dir> [interval_seconds]")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_dir = sys.argv[2]
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    print(f"Extracting frames from: {input_video}")
    w, h, dur = get_video_info(input_video)
    print(f"Video: {w}x{h}, duration: {dur:.2f}s")
    
    frames = extract_sample_frames(input_video, output_dir, interval)
    print(f"\nExtracted {len(frames)} frames to {output_dir}/")
