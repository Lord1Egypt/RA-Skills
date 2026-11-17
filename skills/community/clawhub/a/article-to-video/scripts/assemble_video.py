# -*- coding: utf-8 -*-
"""
Stage 4: Video Assembly
Combines slide images + TTS audio into final video using FFmpeg.

Features:
- Per-scene clip generation with Ken Burns zoom effect
- Scene transitions (fade, dissolve, slide)
- Background music mixing with automatic ducking
- Subtitle burning (SRT → video)
- Windows-safe ASCII temp file naming
- Disk space pre-check
- Progress tracking

Usage:
    python assemble_video.py \
        --slides ./slides --audio ./audio \
        --timing ./audio/timing.json \
        --output final.mp4 \
        --bgm ./assets/bgm.mp3 \
        --resolution 1920x1080
"""

import argparse
import hashlib
import json
import os
import re
import sys
import shutil
import subprocess
import textwrap
import time
import random
from pathlib import Path
from typing import Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import VIDEO_CONFIG, EFFECTS_CONFIG, PATHS_CONFIG, BGM_CONFIG, KEN_BURNS_SPEED_MAP


# ============================================================
# FFmpeg Helper Functions
# ============================================================

def run_ffmpeg(args: list, check: bool = True, timeout: int = 300) -> Tuple[bool, str]:
    """Run FFmpeg command and return (success, stderr_output).

    Args:
        args: FFmpeg command arguments (without the ffmpeg binary path).
        check: If True, treat non-zero return code as failure.
        timeout: Maximum execution time in seconds (default 300).
                Set to 1800+ for long re-encoding tasks like subtitle burning.
    """
    cmd = [PATHS_CONFIG["ffmpeg"], "-y", "-hide_banner", "-loglevel", "warning"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if check and result.returncode != 0:
            return False, result.stderr
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"FFmpeg timed out ({timeout}s)"
    except FileNotFoundError:
        return False, "FFmpeg not found. Install it and add to PATH."


def check_disk_space(path: str, min_mb: int = 500) -> bool:
    """Check if disk has enough free space."""
    try:
        usage = shutil.disk_usage(path)
        free_mb = usage.free / (1024 * 1024)
        if free_mb < min_mb:
            print(f"ERROR: Insufficient disk space. Need {min_mb}MB, have {free_mb:.0f}MB")
            return False
        return True
    except Exception:
        return True  # Skip check if can't determine


# ============================================================
# SRT Subtitle Generation
# ============================================================

def generate_srt(scenes: list, timing_data: list, output_path: str,
                 time_offset: float = 0.0):
    """Generate SRT subtitle file from scenes and timing data.

    Args:
        scenes: List of scene dicts from scenes.json
        timing_data: List of timing info dicts from timing.json
        output_path: Path to write the SRT file
        time_offset: Starting time offset in seconds (e.g. title slide duration).
                      All subtitle timestamps are shifted by this amount.
    """
    current_time = time_offset
    srt_entries = []

    for scene_info in timing_data:
        idx = scene_info["index"]
        duration = scene_info["duration"]

        # Find corresponding scene text
        scene = next((s for s in scenes if s["index"] == idx), None)
        if not scene:
            continue

        text = scene["narration"]

        # Split text into subtitle chunks (max ~40 chars per line, ~2 lines)
        lines = textwrap.wrap(text, width=40)
        # Group into pairs (max 2 lines per subtitle entry)
        chunks = [lines[i:i+2] for i in range(0, len(lines), 2)]

        # Distribute duration across chunks
        chunk_duration = duration / len(chunks) if chunks else duration

        for chunk_idx, chunk in enumerate(chunks):
            start = current_time + chunk_idx * chunk_duration
            end = start + chunk_duration

            # Format timestamps: HH:MM:SS,mmm
            def format_ts(ts: float) -> str:
                h = int(ts // 3600)
                m = int((ts % 3600) // 60)
                s = int(ts % 60)
                ms = int((ts % 1) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

            srt_entries.append({
                "index": len(srt_entries) + 1,
                "start": format_ts(start),
                "end": format_ts(end),
                "text": "\n".join(chunk)
            })

        current_time += duration

    # Write SRT file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in srt_entries:
            f.write(f"{entry['index']}\n")
            f.write(f"{entry['start']} --> {entry['end']}\n")
            f.write(f"{entry['text']}\n\n")

    return output_path


# ============================================================
# Scene Clip Generation
# ============================================================

def create_scene_clip(image_path: str, audio_path: str, output_path: str,
                      duration: float, width: int, height: int,
                      ken_burns: bool = True, ken_burns_speed: str = "normal") -> bool:
    """Create a single video clip from image + audio with Ken Burns effect."""

    fps = VIDEO_CONFIG["fps"]
    total_frames = int(duration * fps)

    if ken_burns and total_frames > 30:
        # Enhanced Ken Burns: zoom + pan for cinematic camera movement
        speed_cfg = KEN_BURNS_SPEED_MAP.get(ken_burns_speed, KEN_BURNS_SPEED_MAP["normal"])
        zoom_start = speed_cfg["zoom_start"]
        zoom_end = speed_cfg["zoom_end"]

        # 'z' formula: linear interpolation from zoom_start to zoom_end
        zoom_expr = f"'{zoom_start}+({zoom_end}-{zoom_start})*on/{total_frames}'"

        # Pan direction: alternate left-right-up-down based on scene index
        # Uses a hash of the image filename to pick a deterministic but varied direction
        fname = os.path.basename(image_path)
        scene_hash = int(hashlib.md5(fname.encode()).hexdigest()[:8], 16)
        pan_mode = scene_hash % 4  # 0=right, 1=left, 2=down, 3=up

        # x/y expressions: start from center, pan towards edge as zoom increases
        # zoom/2 is half the zoomed view width; iw/ih are input dimensions
        # We pan by up to pan_range pixels from center over the clip duration
        pan_range = speed_cfg.get("pan_range", 80)  # from config, fallback 80

        if pan_mode == 0:  # Pan right
            x_expr = f"'iw/2-(iw/zoom/2)+{pan_range}*on/{total_frames}'"
            y_expr = f"'ih/2-(ih/zoom/2)'"
        elif pan_mode == 1:  # Pan left
            x_expr = f"'iw/2-(iw/zoom/2)-{pan_range}*on/{total_frames}'"
            y_expr = f"'ih/2-(ih/zoom/2)'"
        elif pan_mode == 2:  # Pan down
            x_expr = f"'iw/2-(iw/zoom/2)'"
            y_expr = f"'ih/2-(ih/zoom/2)+{pan_range}*on/{total_frames}'"
        else:  # Pan up
            x_expr = f"'iw/2-(iw/zoom/2)'"
            y_expr = f"'ih/2-(ih/zoom/2)-{pan_range}*on/{total_frames}'"

        vf = (
            f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase,"
            f"crop={width*2}:{height*2},"
            f"zoompan=z={zoom_expr}"
            f":x={x_expr}:y={y_expr}"
            f":d={total_frames}:s={width}x{height}:fps={fps}"
        )
    else:
        # Static image, just scale to target resolution
        vf = f"scale={width}:{height}:force_original_aspect_ratio=increase," \
             f"crop={width}:{height}"

    args = [
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-c:v", VIDEO_CONFIG["video_codec"],
        "-preset", VIDEO_CONFIG["video_preset"],
        "-crf", str(VIDEO_CONFIG["video_crf"]),
        "-pix_fmt", VIDEO_CONFIG["pixel_format"],
        "-c:a", VIDEO_CONFIG["audio_codec"],
        "-b:a", VIDEO_CONFIG["audio_bitrate"],
        "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
        "-ac", "2",  # Force stereo for consistency across all clips
        "-shortest",
        output_path
    ]

    success, err = run_ffmpeg(args)
    if not success:
        print(f"    FFmpeg error: {err[:200]}")
    return success


def add_bgm_to_clip(video_path: str, bgm_path: str, output_path: str,
                    narration_vol: str, bgm_vol: str) -> bool:
    """Mix background music into a video clip."""
    clip_duration = _get_duration(video_path)
    fade_in = EFFECTS_CONFIG["bgm_fade_in"]
    fade_out = EFFECTS_CONFIG["bgm_fade_out"]

    # Clamp fade-out start time to avoid negative values for short clips
    fade_out_start = max(0, clip_duration - fade_out)
    # If clip is shorter than fade_in, reduce fade_in to clip duration
    actual_fade_in = min(fade_in, clip_duration)

    # Log BGM mixing parameters for troubleshooting
    print(f"    [bgm-mix] {os.path.basename(video_path)}: "
          f"duration={clip_duration:.3f}s, "
          f"narration_vol={narration_vol}, bgm_vol={bgm_vol}, "
          f"fade_in={actual_fade_in:.1f}s, fade_out_start={fade_out_start:.1f}s")
    if fade_out_start == 0 and clip_duration < fade_out:
        print(f"    [bgm-mix] NOTE: clip shorter than fade_out "
              f"({clip_duration:.1f}s < {fade_out}s), clamped fade_out_start to 0")

    args = [
        "-i", video_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[0:a]volume={narration_vol}[a0];"
        f"[1:a]volume={bgm_vol},afade=t=in:st=0:d={actual_fade_in},afade=t=out:"
        f"st={fade_out_start}:d={min(fade_out, clip_duration)}[a1];"
        f"[a0][a1]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", VIDEO_CONFIG["audio_codec"],
        "-b:a", VIDEO_CONFIG["audio_bitrate"],
        "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
        "-ac", "2",
        "-shortest",
        output_path
    ]
    success, err = run_ffmpeg(args)
    if not success:
        # If BGM mixing fails, just copy the original
        print(f"    [bgm-mix] WARNING: BGM mix failed, using original audio: {err[:150]}")
        shutil.copy2(video_path, output_path)
    else:
        print(f"    [bgm-mix] Success: {os.path.basename(output_path)}")
    return True


def _get_duration(video_path: str) -> float:
    """Get video duration in seconds.
    Tries ffprobe first, falls back to ffmpeg -i parsing.
    """
    # Try ffprobe first
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffprobe"], "-v", "error",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1",
             video_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except Exception:
        pass

    # Fallback: parse ffmpeg -i stderr output
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffmpeg"], "-i", video_path],
            capture_output=True, text=True, timeout=10
        )
        # Look for "Duration: 00:00:13.34" pattern
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)', result.stderr)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
    except Exception:
        pass

    return 10.0  # Ultimate fallback


def _has_audio_stream(video_path: str) -> bool:
    """Check if a video file has an audio stream.

    Uses ffprobe first, falls back to ffmpeg -i stderr parsing
    (consistent with _get_duration and measure_audio_duration patterns).
    """
    fname = os.path.basename(video_path)

    # Try ffprobe first
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffprobe"], "-v", "error",
             "-select_streams", "a",
             "-show_entries", "stream=codec_name",
             "-of", "default=noprint_wrappers=1:nokey=1",
             video_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            has_audio = bool(result.stdout.strip())
            codec = result.stdout.strip() or "none"
            print(f"    [audio] {fname}: ffprobe detected "
                  f"{'audio' if has_audio else 'NO audio'} (codec={codec})")
            return has_audio
        else:
            print(f"    [audio] {fname}: ffprobe returned rc={result.returncode}, "
                  f"falling back to ffmpeg -i")
    except Exception as e:
        print(f"    [audio] {fname}: ffprobe exception ({type(e).__name__}), "
              f"falling back to ffmpeg -i")

    # Fallback: check ffmpeg -i stderr for "Audio:" indicator
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffmpeg"], "-i", video_path],
            capture_output=True, text=True, timeout=10
        )
        has_audio = "Audio:" in result.stderr
        print(f"    [audio] {fname}: ffmpeg -i detected "
              f"{'audio' if has_audio else 'NO audio'}")
        return has_audio
    except Exception as e:
        # If we can't check, assume audio exists (better than failing)
        print(f"    [audio] {fname}: both ffprobe and ffmpeg failed "
              f"({type(e).__name__}), assuming audio exists")
        return True


# ============================================================
# Scene Concatenation with Transitions
# ============================================================

def _ensure_all_clips_have_audio(clip_paths: list, output_path: str) -> list:
    """Ensure all clips have audio streams. Add silent audio if missing.

    For clips without audio, creates a temp file with silent audio added.
    This normalizes all clips so both xfade and concat demuxer work reliably.

    Returns a new list of clip paths (some may be temp files with added audio).
    """
    temp_dir = os.path.dirname(output_path)
    result = []
    clips_needing_audio = 0
    clips_with_audio = 0
    clips_failed = 0

    print(f"    [audio-check] Checking {len(clip_paths)} clips for audio streams...")

    for i, clip in enumerate(clip_paths):
        if _has_audio_stream(clip):
            result.append(clip)
            clips_with_audio += 1
        else:
            clips_needing_audio += 1
            fname = os.path.basename(clip)
            # Add silent audio to the clip
            temp_clip = os.path.join(temp_dir, f"clip_silent_{i:03d}.mp4")
            duration = _get_duration(clip)
            print(f"    [audio-fix] Clip {i} ({fname}): no audio stream, "
                  f"adding silent audio (duration={duration:.3f}s)")

            success, err = run_ffmpeg([
                "-i", clip,
                "-f", "lavfi", "-i",
                f"anullsrc=channel_layout=stereo:sample_rate="
                f"{VIDEO_CONFIG['audio_sample_rate']}",
                "-t", f"{duration:.3f}",
                "-c:v", "copy",
                "-c:a", VIDEO_CONFIG["audio_codec"],
                "-b:a", VIDEO_CONFIG["audio_bitrate"],
                "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
                "-ac", "2",
                "-shortest",
                temp_clip
            ], check=False)
            if success:
                result.append(temp_clip)
                print(f"    [audio-fix] Clip {i}: silent audio added -> {os.path.basename(temp_clip)}")
            else:
                clips_failed += 1
                print(f"    [audio-fix] Clip {i}: FAILED to add silent audio "
                      f"({err[:150]}), using original")
                # If we can't add audio, use original (concat may still work)
                result.append(clip)

    print(f"    [audio-check] Summary: {clips_with_audio} with audio, "
          f"{clips_needing_audio} needed fix, {clips_failed} failed")

    return result


def concatenate_scenes(clip_paths: list, output_path: str,
                       transition: str, transition_duration: float) -> bool:
    """Concatenate scene clips with crossfade transitions."""

    print(f"  [concat] Starting: {len(clip_paths)} clips, "
          f"transition='{transition}', duration={transition_duration}s")

    if len(clip_paths) == 1:
        print(f"  [concat] Only 1 clip, copying directly (no transitions needed)")
        shutil.copy2(clip_paths[0], output_path)
        return True

    # Ensure all clips have audio streams (P1 fix: audio error tolerance)
    print(f"  [concat] Pre-check: ensuring all clips have audio streams...")
    clip_paths = _ensure_all_clips_have_audio(clip_paths, output_path)
    print(f"  [concat] Audio normalization complete, proceeding with {len(clip_paths)} clips")

    if transition == "none" or transition_duration <= 0:
        # Simple concatenation without transitions
        print(f"  [concat] Mode: simple concat (no transitions)")
        # Use concat filter (not concat demuxer with -c copy) to re-encode audio
        # This prevents stream corruption when clips have different audio params
        list_file = output_path + ".txt"
        with open(list_file, 'w') as f:
            for clip in clip_paths:
                # Use absolute paths with forward slashes for FFmpeg compatibility
                # (concat demuxer resolves relative paths relative to the list file)
                abs_path = os.path.abspath(clip).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")

        print(f"  [concat] Concat list written to {os.path.basename(list_file)} "
              f"({len(clip_paths)} entries)")

        # Re-encode both video and audio to ensure consistent format
        # (different clips may have different bitrates/sample rates)
        # Use fast preset for concat to avoid timeout on long videos (20+ min)
        args = ["-f", "concat", "-safe", "0", "-i", list_file,
                "-r", str(VIDEO_CONFIG["fps"]),  # Force consistent FPS
                "-c:v", VIDEO_CONFIG["video_codec"],
                "-preset", "fast",
                "-crf", "24",
                "-pix_fmt", VIDEO_CONFIG["pixel_format"],
                "-c:a", VIDEO_CONFIG["audio_codec"],
                "-b:a", VIDEO_CONFIG["audio_bitrate"],
                "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
                "-ac", "2",  # Force stereo
                output_path]
        success, err = run_ffmpeg(args, timeout=1800)
        if not success:
            print(f"  [concat] ERROR: simple concat failed: {err[:500]}")
        else:
            # Log output file size for verification
            out_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  [concat] Success: output={os.path.basename(output_path)} "
                  f"({out_size:.1f}MB)")
        os.remove(list_file)
        return success

    # Build xfade filter chain
    # This requires all clips to be re-encoded, but gives smooth transitions
    print(f"  [concat] Mode: xfade transitions ('{transition}', {transition_duration}s)")
    filter_parts = []
    inputs = []

    for i, clip in enumerate(clip_paths):
        inputs.extend(["-i", clip])

    # Build the filter complex
    # Format: [0:v][1:v]xfade=transition=fade:duration=0.5:offset=D0[v01];
    #          [v01][2:v]xfade=transition=fade:duration=0.5:offset=D1[v012]; ...
    filter_str = ""
    prev_label = "0:v"
    accumulated_offset = 0.0

    # Get durations of each clip
    durations = []
    for clip in clip_paths:
        d = _get_duration(clip)
        durations.append(d)

    print(f"  [concat] Clip durations: " +
          ", ".join(f"[{i}]={d:.2f}s" for i, d in enumerate(durations)))

    for i in range(1, len(clip_paths)):
        # Offset = accumulated duration - transition overlap
        accumulated_offset += durations[i-1] - transition_duration

        current_label = f"v{i}" if i < len(clip_paths) - 1 else "vout"
        filter_str += (
            f"[{prev_label}][{i}:v]xfade="
            f"transition={transition}:"
            f"duration={transition_duration}:"
            f"offset={accumulated_offset:.3f}"
            f"[{current_label}];"
        )
        print(f"  [concat] xfade step {i}: {prev_label} + [{i}:v] -> {current_label} "
              f"(offset={accumulated_offset:.3f}s)")
        prev_label = current_label

    # Remove trailing semicolon
    filter_str = filter_str.rstrip(';')

    # Also concatenate audio
    audio_inputs = "".join(f"[{i}:a]" for i in range(len(clip_paths)))
    filter_str += f";{audio_inputs}concat=n={len(clip_paths)}:v=0:a=1[aout]"

    print(f"  [concat] Audio concat: {len(clip_paths)} streams -> [aout]")

    args = inputs + [
        "-filter_complex", filter_str,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", VIDEO_CONFIG["video_codec"],
        "-preset", "fast",
        "-crf", "24",
        "-pix_fmt", VIDEO_CONFIG["pixel_format"],
        "-c:a", VIDEO_CONFIG["audio_codec"],
        "-b:a", VIDEO_CONFIG["audio_bitrate"],
        "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
        "-ac", "2",
        output_path
    ]

    print(f"  [concat] Executing xfade ffmpeg command ({len(clip_paths)} inputs, timeout=1800s)...")
    success, err = run_ffmpeg(args, check=False, timeout=1800)
    if not success:
        # Fallback: simple concat without transitions
        print(f"  [concat] WARNING: xfade concat failed, falling back to simple concat")
        print(f"  [concat] Error details: {err[:300]}")
        return concatenate_scenes(clip_paths, output_path, "none", 0)

    out_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  [concat] Success: xfade output={os.path.basename(output_path)} "
          f"({out_size:.1f}MB)")
    return True


# ============================================================
# Subtitle Burning
# ============================================================

def burn_subtitles(video_path: str, srt_path: str, output_path: str) -> bool:
    """Burn SRT subtitles into video.

    Uses faster encoding settings (preset=fast, crf=24) and extended timeout
    (1800s) to handle long videos (20+ minutes) that the default 300s timeout
    cannot accommodate.
    """
    font = EFFECTS_CONFIG["subtitle_font"]
    font_size = EFFECTS_CONFIG["subtitle_font_size"]
    font_color = EFFECTS_CONFIG["subtitle_color"]
    border_color = EFFECTS_CONFIG["subtitle_border_color"]
    border_width = EFFECTS_CONFIG["subtitle_border_width"]

    # Escape SRT path for FFmpeg subtitles filter on Windows
    # Need to escape backslashes and colons in the file path
    srt_escaped = srt_path.replace('\\', '/').replace(':', '\\:')

    # Build force_style string (ASS format)
    # Color format: &H00BBGGRR& (already includes &H prefix in config)
    force_style = (
        f"FontName={font},"
        f"FontSize={font_size},"
        f"PrimaryColour={font_color},"
        f"OutlineColour={border_color},"
        f"BorderStyle=1,"
        f"Outline={border_width},"
        f"Alignment=2,"
        f"MarginV=20"
    )

    vf = f"subtitles='{srt_escaped}':force_style='{force_style}'"

    # Use faster preset and slightly higher CRF for subtitle burning
    # to reduce re-encoding time on long videos (20+ min)
    sub_preset = "fast"
    sub_crf = 24

    args = [
        "-i", video_path,
        "-vf", vf,
        "-c:v", VIDEO_CONFIG["video_codec"],
        "-preset", sub_preset,
        "-crf", str(sub_crf),
        "-pix_fmt", VIDEO_CONFIG["pixel_format"],
        "-c:a", VIDEO_CONFIG["audio_codec"],
        "-b:a", VIDEO_CONFIG["audio_bitrate"],
        "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
        "-ac", "2",
        output_path
    ]

    print(f"    [subtitle] Burning subtitles (preset={sub_preset}, crf={sub_crf}, timeout=1800s)...")
    success, err = run_ffmpeg(args, timeout=1800)
    if not success:
        print(f"    [subtitle] FAILED: {err[:200]}")
        print(f"    Copying video without subtitles")
        shutil.copy2(video_path, output_path)
    else:
        print(f"    [subtitle] Success: {os.path.basename(output_path)}")
    return True


# ============================================================
# Thumbnail Extraction
# ============================================================

def extract_thumbnail(video_path: str, output_path: str) -> bool:
    """Extract first frame as thumbnail."""
    args = ["-i", video_path, "-ss", "00:00:01", "-frames:v", "1",
            "-q:v", "2", output_path]
    success, _ = run_ffmpeg(args, check=False)
    return success


# ============================================================
# Main Assembly Pipeline
# ============================================================

def _find_bgm_for_type(content_type: str, style_override: str = None) -> str:
    """Auto-select BGM file based on content type.

    If multiple audio files exist in the style directory, one is randomly selected.
    Args:
        content_type: Content type for auto-mapping (ignored if style_override is set)
        style_override: Force a specific BGM style (e.g. "cinematic")
    Returns: Path to BGM file, or empty string if none found.
    """
    if not BGM_CONFIG.get("auto_select", False) and not style_override:
        return ""

    # Determine BGM style: explicit override > content type mapping > default
    if style_override:
        bgm_style = style_override
    else:
        bgm_style = BGM_CONFIG["type_bgm_map"].get(content_type,
                                                    BGM_CONFIG["default_style"])

    style_info = BGM_CONFIG["styles"].get(bgm_style)
    if not style_info:
        return ""

    bgm_dir = os.path.join(PATHS_CONFIG["assets_dir"], "bgm", style_info["dir"])
    if not os.path.exists(bgm_dir):
        return ""

    # Collect all audio files and randomly select one
    audio_files = [f for f in os.listdir(bgm_dir)
                   if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
    if not audio_files:
        return ""

    selected = random.choice(audio_files)
    return os.path.join(bgm_dir, selected)


def _get_bgm_volume(bgm_path: str) -> str:
    """Get BGM volume based on the style directory of the BGM file.

    Matches the BGM file's parent directory against BGM_CONFIG styles
    to find the style-specific volume. Falls back to the default bgm_volume.
    """
    if not bgm_path:
        return EFFECTS_CONFIG["bgm_volume"]

    bgm_dir = os.path.basename(os.path.dirname(bgm_path))
    for style_name, style_info in BGM_CONFIG["styles"].items():
        if style_info["dir"] == bgm_dir:
            return style_info.get("volume", EFFECTS_CONFIG["bgm_volume"])
    return EFFECTS_CONFIG["bgm_volume"]


def run_assembly(slides_dir: str, audio_dir: str, timing_path: str,
                output_path: str, bgm_path: str, srt_path: str,
                resolution: str, transition: str, ken_burns: bool,
                burn_subs: bool, bgm_style: str = None,
                narration_vol: str = None):
    """Run the complete video assembly pipeline.

    Args:
        bgm_style: Optional BGM style override (e.g. "cinematic", "corporate").
                   When provided, forces this BGM style regardless of content type.
        narration_vol: Optional narration volume override (e.g. "-3dB").
                       When provided, overrides EFFECTS_CONFIG["narration_volume"].
    """

    # Parse resolution
    try:
        width, height = map(int, resolution.split('x'))
    except ValueError:
        width = VIDEO_CONFIG["width"]
        height = VIDEO_CONFIG["height"]

    # Load timing data
    with open(timing_path, 'r', encoding='utf-8') as f:
        timing = json.load(f)
    timing_scenes = timing["scenes"]

    # Read voice profile params from timing.json if present
    if narration_vol is None:
        narration_vol = timing.get("narration_volume", EFFECTS_CONFIG["narration_volume"])
    if bgm_style is None:
        bgm_style = timing.get("bgm_style")

    # Load scenes (for subtitle text)
    scenes_json = None
    scenes_path = os.path.join(slides_dir, "..", "scenes.json")
    if not os.path.exists(scenes_path):
        # Try audio dir parent
        scenes_path = os.path.join(os.path.dirname(audio_dir), "scenes.json")
    if os.path.exists(scenes_path):
        with open(scenes_path, 'r', encoding='utf-8') as f:
            scenes_json = json.load(f)

    total = len(timing_scenes)

    # Disk space check
    temp_dir = os.path.join(os.path.dirname(output_path), "_tmp_video")
    if not check_disk_space(temp_dir, min_mb=500):
        return False
    os.makedirs(temp_dir, exist_ok=True)

    # Load slides manifest
    manifest_path = os.path.join(slides_dir, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = None

    # Extract content type and Ken Burns speed from manifest
    content_type = "default"
    ken_burns_speed = "normal"
    if manifest:
        content_type = manifest.get("content_type", "default")
        ken_burns_speed = manifest.get("ken_burns_speed", "normal")
    elif scenes_json:
        content_type = scenes_json.get("content_type", "default")

    # Auto-select BGM based on content type if not explicitly provided
    # bgm_style override takes priority over content_type mapping
    if not bgm_path or not os.path.exists(bgm_path):
        auto_bgm = _find_bgm_for_type(content_type, style_override=bgm_style)
        if auto_bgm:
            bgm_path = auto_bgm
            print(f"  Auto-selected BGM for '{content_type}': {bgm_path}")

    print(f"Video Assembly: {total} scenes")
    print(f"  Content type: {content_type}")
    print(f"  Ken Burns speed: {ken_burns_speed}")
    print(f"  Resolution: {width}x{height}")
    print(f"  Transition: {transition}")
    print(f"  Ken Burns: {'on' if ken_burns else 'off'}")
    print(f"  BGM: {bgm_path or 'none'}")
    if bgm_style:
        print(f"  BGM style override: {bgm_style}")
    print(f"  Narration volume: {narration_vol}")
    print(f"  Subtitles: {'on' if burn_subs else 'off'}")
    print()

    # Step 1: Create individual scene clips
    print("--- Step 1: Creating scene clips ---")
    clip_paths = []
    title_duration = 0.0

    # Add title slide if available
    title_image = os.path.join(slides_dir, "title.png")
    if os.path.exists(title_image) and manifest:
        title_clip = os.path.join(temp_dir, "clip_title.mp4")
        title_duration = 3.0  # Title slide is 3 seconds
        # Use a 3-second title card with silence + subtle Ken Burns zoom
        fps = VIDEO_CONFIG["fps"]
        title_frames = int(title_duration * fps)
        # Subtle zoom: 1.0 → 1.05 over the title duration
        title_vf = (
            f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase,"
            f"crop={width*2}:{height*2},"
            f"zoompan=z='1.0+0.05*on/{title_frames}':d={title_frames}:s={width}x{height}:fps={fps}"
        )
        success, _ = run_ffmpeg([
            "-loop", "1", "-i", title_image,
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-t", str(title_duration),
            "-vf", title_vf,
            "-r", str(VIDEO_CONFIG["fps"]),  # Force consistent FPS
            "-c:v", VIDEO_CONFIG["video_codec"], "-preset", "fast",
            "-crf", str(VIDEO_CONFIG["video_crf"]),
            "-pix_fmt", VIDEO_CONFIG["pixel_format"],
            "-c:a", VIDEO_CONFIG["audio_codec"],
            "-b:a", VIDEO_CONFIG["audio_bitrate"],
            "-ar", str(VIDEO_CONFIG["audio_sample_rate"]),
            "-ac", "2",
            "-shortest", title_clip
        ])
        if success:
            clip_paths.append(title_clip)
            print(f"  Title clip created")

    for i, scene_info in enumerate(timing_scenes):
        idx = scene_info["index"]
        duration = scene_info["duration"]
        audio_file = scene_info["audio_file"]

        if not audio_file or duration <= 0:
            print(f"  [{i+1}/{total}] Scene {idx}: SKIP (no audio)")
            continue

        # Find corresponding image
        image_file = os.path.join(slides_dir, f"scene_{idx:03d}.png")
        if not os.path.exists(image_file):
            print(f"  [{i+1}/{total}] Scene {idx}: SKIP (no image)")
            continue

        # Create clip (ASCII-safe temp name)
        clip_path = os.path.join(temp_dir, f"clip_{idx:03d}.mp4")
        print(f"  [{i+1}/{total}] Scene {idx}: {duration:.1f}s clip...")

        success = create_scene_clip(
            image_file, audio_file, clip_path, duration,
            width, height, ken_burns, ken_burns_speed
        )

        if not success:
            print(f"    FAILED, skipping")
            continue

        # Mix BGM if provided (use style-specific volume from BGM_CONFIG)
        if bgm_path and os.path.exists(bgm_path):
            bgm_clip = os.path.join(temp_dir, f"clip_{idx:03d}_bgm.mp4")
            add_bgm_to_clip(
                clip_path, bgm_path, bgm_clip,
                narration_vol,
                _get_bgm_volume(bgm_path)
            )
            clip_paths.append(bgm_clip)
        else:
            clip_paths.append(clip_path)

    print(f"\n  Created {len(clip_paths)} clips total")

    # Step 2: Concatenate with transitions
    print("\n--- Step 2: Concatenating with transitions ---")
    print(f"  [assembly] Clips to concatenate:")
    for i, cp in enumerate(clip_paths):
        print(f"    [{i}] {os.path.basename(cp)} "
              f"({os.path.getsize(cp)/1024:.0f}KB)")
    concat_path = os.path.join(temp_dir, "concat.mp4")
    success = concatenate_scenes(
        clip_paths, concat_path,
        transition, EFFECTS_CONFIG["transition_duration"]
    )

    if not success:
        print("ERROR: Concatenation failed!")
        return False

    # Step 3: Burn subtitles
    final_path = concat_path
    if burn_subs:
        print("\n--- Step 3: Burning subtitles ---")

        # Generate SRT if not provided
        if not srt_path or not os.path.exists(srt_path):
            if scenes_json:
                srt_path = os.path.join(temp_dir, "subtitle.srt")
                generate_srt(scenes_json["scenes"], timing_scenes, srt_path,
                            time_offset=title_duration)
                print(f"  Generated SRT: {srt_path}")
            else:
                print("  No scenes data for subtitles, skipping")

        if srt_path and os.path.exists(srt_path):
            sub_path = os.path.join(temp_dir, "subtitled.mp4")
            burn_subtitles(concat_path, srt_path, sub_path)
            final_path = sub_path
            # Copy SRT to output location
            srt_output = os.path.splitext(output_path)[0] + ".srt"
            shutil.copy2(srt_path, srt_output)

    # Step 4: Copy to final output
    print(f"\n--- Step 4: Saving final video ---")
    shutil.copy2(final_path, output_path)

    # Step 5: Extract thumbnail
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    extract_thumbnail(output_path, thumb_path)

    # Cleanup temp
    try:
        shutil.rmtree(temp_dir)
        print(f"  Cleaned up temp files")
    except Exception:
        print(f"  Warning: could not clean temp dir: {temp_dir}")

    # Summary
    total_duration = title_duration + sum(s["duration"] for s in timing_scenes)
    file_size = os.path.getsize(output_path) / (1024 * 1024)

    print(f"\n{'='*50}")
    print(f"Video assembled successfully!")
    print(f"  File: {output_path}")
    print(f"  Size: {file_size:.1f} MB")
    print(f"  Duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")
    print(f"  Resolution: {width}x{height}")
    if burn_subs and srt_path:
        print(f"  Subtitles: {os.path.splitext(output_path)[0]}.srt")
    print(f"  Thumbnail: {thumb_path}")
    print(f"{'='*50}")

    return True


# ============================================================
# Main Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Assemble video from slides and audio")
    parser.add_argument("--slides", "-s", required=True, help="Slides directory")
    parser.add_argument("--audio", "-a", required=True, help="Audio directory")
    parser.add_argument("--timing", "-t", required=True, help="timing.json path")
    parser.add_argument("--output", "-o", required=True, help="Output video path")
    parser.add_argument("--bgm", "-b", default=None, help="Background music MP3")
    parser.add_argument("--srt", default=None, help="SRT subtitle file")
    parser.add_argument("--resolution", "-r", default="1920x1080",
                       help="Output resolution (WxH)")
    parser.add_argument("--transition", default=EFFECTS_CONFIG["transition"],
                       choices=["fade", "dissolve", "slideleft", "slideright",
                                "wipeup", "wipedown", "circleopen", "none"],
                       help="Transition type")
    parser.add_argument("--no-ken-burns", action="store_true",
                       help="Disable Ken Burns effect")
    parser.add_argument("--no-subtitle", action="store_true",
                       help="Disable subtitle burning")
    parser.add_argument("--bgm-style", default=None,
                       choices=list(BGM_CONFIG["styles"].keys()),
                       help="Override BGM style (e.g. corporate, cinematic, electronic)")
    parser.add_argument("--narration-volume", default=None,
                       help="Narration volume override (e.g. -3dB, 0dB). "
                            "Auto-read from timing.json if not specified.")
    args = parser.parse_args()

    try:
        success = run_assembly(
            slides_dir=args.slides,
            audio_dir=args.audio,
            timing_path=args.timing,
            output_path=args.output,
            bgm_path=args.bgm,
            srt_path=args.srt,
            resolution=args.resolution,
            transition=args.transition,
            ken_burns=not args.no_ken_burns,
            burn_subs=not args.no_subtitle,
            bgm_style=args.bgm_style,
            narration_vol=args.narration_volume
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
