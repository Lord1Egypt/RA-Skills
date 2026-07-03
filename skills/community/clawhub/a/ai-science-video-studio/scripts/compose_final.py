#!/usr/bin/env python3
"""
FFmpeg Final Compositing Script — Assemble and encode the final video.

Takes individual segment videos, applies subtitle overlays, concatenates with
xfade/acrossfade transitions, and encodes with unified CRF 20 quality.

Usage:
    # Basic compositing (no transitions, just concat)
    python3 compose_final.py \
        --segments intro.mp4 content_1.mp4 content_2.mp4 content_3.mp4 outro.mp4 \
        --output final.mp4

    # With transitions
    python3 compose_final.py \
        --segments intro.mp4 content_1.mp4 content_2.mp4 content_3.mp4 outro.mp4 \
        --output final.mp4 \
        --xfade 0.5

    # With subtitle overlay and transitions
    python3 compose_final.py \
        --segments intro.mp4 content_1.mp4 content_2.mp4 content_3.mp4 outro.mp4 \
        --subtitles subs_intro/ subs_c1/ subs_c2/ subs_c3/ subs_outro/ \
        --output final.mp4 \
        --xfade 0.5
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def get_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def overlay_subtitles(video_path, subtitle_frame_dir, output_path, fps=24):
    """
    Overlay transparent PNG subtitle frames onto a video.

    The subtitle frame directory should contain frame_00000.png, frame_00001.png, etc.
    """
    width, height = 1280, 720
    total_frames = len(list(Path(subtitle_frame_dir).glob("frame_*.png")))
    if total_frames == 0:
        print(f"Warning: No subtitle frames in {subtitle_frame_dir}, skipping overlay")
        # Just copy
        subprocess.run(["ffmpeg", "-y", "-i", video_path, "-c", "copy", output_path],
                       check=True)
        return

    sub_duration = total_frames / fps
    video_duration = get_duration(video_path)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-framerate", str(fps),
        "-i", f"{subtitle_frame_dir}/frame_%05d.png",
        "-filter_complex",
        f"[0:v][1:v]overlay=0:0:shortest=1[vout]",
        "-map", "[vout]",
        "-map", "0:a",
        "-c:v", "libx264", "-crf", "20",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True)
    print(f"  Subtitled: {video_path} → {output_path}")


def compose_segments(segment_paths, output_path, xfade_duration=0,
                     subtitle_dirs=None, fps=24):
    """
    Composite all segments into a final video.

    Parameters:
        segment_paths: list of input video paths in order
        output_path: final output .mp4
        xfade_duration: crossfade duration in seconds (0 = no transition)
        subtitle_dirs: optional list of subtitle frame directories (one per segment)
        fps: frame rate
    """
    # Step 1: Apply subtitles (if provided)
    if subtitle_dirs and len(subtitle_dirs) == len(segment_paths):
        subtitled_segments = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for i, (seg, sub_dir) in enumerate(zip(segment_paths, subtitle_dirs)):
                tmp_path = os.path.join(tmpdir, f"seg_{i:02d}_subbed.mp4")
                overlay_subtitles(seg, sub_dir, tmp_path, fps)
                subtitled_segments.append(tmp_path)
            segment_paths = subtitled_segments
            _composite_internal(segment_paths, output_path, xfade_duration)
    else:
        _composite_internal(segment_paths, output_path, xfade_duration)


def _composite_internal(segment_paths, output_path, xfade_duration):
    """Internal: run the actual FFmpeg compositing."""
    if xfade_duration <= 0:
        _concat_simple(segment_paths, output_path)
    else:
        _concat_with_xfade(segment_paths, output_path, xfade_duration)


def _concat_simple(segment_paths, output_path):
    """Simple concat without transitions."""
    # First, unify all segments to same format
    unified = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, seg in enumerate(segment_paths):
            tmp_path = os.path.join(tmpdir, f"u_{i:02d}.mp4")
            subprocess.run([
                "ffmpeg", "-y", "-i", seg,
                "-c:v", "libx264", "-crf", "20",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-r", "24",
                tmp_path,
            ], check=True, capture_output=True)
            unified.append(tmp_path)

        # Create concat list
        concat_path = os.path.join(tmpdir, "concat.txt")
        with open(concat_path, "w") as f:
            for u in unified:
                f.write(f"file '{u}'\n")

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_path,
            "-c", "copy",
            output_path,
        ], check=True)

    print(f"Composited {len(segment_paths)} segments → {output_path}")


def _concat_with_xfade(segment_paths, output_path, xfade):
    """Concat with xfade video transitions and acrossfade audio transitions."""
    # Build filter complex
    durations = [get_duration(s) for s in segment_paths]
    total_duration = sum(durations) - xfade * (len(segment_paths) - 1)

    # Video filters: chain xfade
    v_inputs = "".join(f"[{i}:v]settb=AVTB,fps=24,setpts=PTS-STARTPTS[v{i}]" for i in range(len(segment_paths)))
    v_chain = f"[v0]"
    offsets = []
    cumulative = 0
    for i in range(1, len(segment_paths)):
        offset = durations[i - 1] - xfade
        cumulative += offset
        offsets.append(cumulative)
        v_chain += f"[v{i}]xfade=transition=fade:duration={xfade}:offset={cumulative}"

    if len(segment_paths) > 1:
        v_chain += f"[vout]"

    # Audio filters: chain acrossfade
    a_inputs = "".join(f"[{i}:a]asetpts=PTS-STARTPTS[a{i}]" for i in range(len(segment_paths)))
    a_chain = f"[a0]"
    for i in range(1, len(segment_paths)):
        a_chain += f"[a{i}]acrossfade=d={xfade}:curve=tri"

    if len(segment_paths) > 1:
        a_chain += f"[aout]"

    filter_complex = f"{v_inputs};{a_inputs};{v_chain};{a_chain}"

    cmd = [
        "ffmpeg", "-y",
    ]
    for seg in segment_paths:
        cmd.extend(["-i", seg])
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[vout]" if len(segment_paths) > 1 else "[v0]",
        "-map", "[aout]" if len(segment_paths) > 1 else "[a0]",
        "-c:v", "libx264", "-crf", "20",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-af", "alimiter=limit=-0.9dB",
        output_path,
    ])

    subprocess.run(cmd, check=True)
    print(f"Composited {len(segment_paths)} segments with {xfade}s xfade → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="FFmpeg final video compositing")
    parser.add_argument("--segments", type=str, nargs="+", required=True,
                        help="Input segment video files in order")
    parser.add_argument("--output", type=str, required=True, help="Output .mp4 file")
    parser.add_argument("--xfade", type=float, default=0.5,
                        help="Crossfade duration in seconds (default: 0.5)")
    parser.add_argument("--subtitles", type=str, nargs="*", default=None,
                        help="Subtitle frame directories (one per segment)")
    parser.add_argument("--fps", type=int, default=24, help="Frame rate")

    args = parser.parse_args()

    compose_segments(
        segment_paths=args.segments,
        output_path=args.output,
        xfade_duration=args.xfade,
        subtitle_dirs=args.subtitles,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
