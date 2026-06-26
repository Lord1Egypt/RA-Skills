#!/usr/bin/env python3
"""
Video Watermark Remover - Main Processor
Handles single-segment and multi-segment watermark removal.
"""
import subprocess
import json
import sys
from pathlib import Path

def process_single_segment(input_video, output_video, x, y, w, h):
    """Process video with a single delogo region."""
    cmd = [
        'ffmpeg', '-y', '-i', input_video,
        '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}',
        '-c:a', 'copy', output_video
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr[-500:]}", file=sys.stderr)
        return False
    return True

def process_multi_segment(input_video, output_video, segments, temp_dir):
    """
    Process video with multiple delogo regions across different time segments.
    
    segments: list of (start_time, end_time, x, y, w, h)
    """
    temp_dir = Path(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each segment
    seg_files = []
    for i, (s, e, x, y, w, h) in enumerate(segments):
        seg_file = temp_dir / f'seg_{i+1}.mp4'
        t_len = e - s
        
        # For first segment, decode from 0; for others, use -ss with input seeking
        if i == 0:
            cmd = [
                'ffmpeg', '-y', '-i', input_video,
                '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}',
                '-t', str(t_len), '-c:a', 'copy', str(seg_file)
            ]
        else:
            cmd = [
                'ffmpeg', '-y', '-ss', str(s), '-i', input_video,
                '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}',
                '-t', str(t_len), '-c:a', 'aac', str(seg_file)
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Segment {i+1} error: {result.stderr[-300:]}", file=sys.stderr)
            return False
        seg_files.append(seg_file)
        print(f"  Segment {i+1}: {s:.2f}s-{e:.2f}s delogo ({x},{y},{w},{h}) → OK")
    
    # Concatenate segments
    concat_file = temp_dir / 'concat.txt'
    concat_file.write_text('\n'.join(f"file '{f}'" for f in seg_files))
    
    result = subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_file), '-c', 'copy', output_video
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Concat error: {result.stderr[-300:]}", file=sys.stderr)
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process_video.py <input> <output> <segments_json>")
        print("  segments_json: JSON array of [start, end, x, y, w, h]")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2]
    segments = json.loads(sys.argv[3])
    
    temp_dir = f"/tmp/watermark_proc_{Path(input_video).stem}"
    
    if len(segments) == 1:
        s = segments[0]
        print(f"Processing single segment: delogo ({s[2]},{s[3]},{s[4]},{s[5]})")
        ok = process_single_segment(input_video, output_video, s[2], s[3], s[4], s[5])
    else:
        print(f"Processing {len(segments)} segments...")
        ok = process_multi_segment(input_video, output_video, segments, temp_dir)
    
    if ok:
        sz = Path(output_video).stat().st_size
        print(f"Done: {output_video} ({sz/1024/1024:.2f}MB)")
    else:
        sys.exit(1)
