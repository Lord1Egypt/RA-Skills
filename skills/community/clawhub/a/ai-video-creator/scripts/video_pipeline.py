#!/usr/bin/env python3
"""
Video Pipeline - Generate multi-clip videos, stitch with ffmpeg, add BGM.

Usage:
    python video_pipeline.py create --prompts prompts.json --output ./output/ --text "line1|line2" --bgm-dir ./bgm --mood healing
    python video_pipeline.py generate --prompts prompts.json --output ./output/
    python video_pipeline.py stitch --input ./output/ --bgm-dir ./bgm --mood healing --text "line1|line2"

Environment variables:
    VOLCENGINE_ACCESS_KEY  - Volcengine Access Key ID
    VOLCENGINE_SECRET_KEY  - Volcengine Secret Access Key
"""

import argparse
import glob
import json
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.request

from volcengine.visual.VisualService import VisualService


# Jimeng 3.0 720P text-to-video (cheaper, faster)
REQ_KEY = "jimeng_t2v_v30"
FRAMES = 121  # ~5s at 24fps
FONT = os.environ.get("VIDEO_FONT", "/System/Library/Fonts/STHeiti Medium.ttc")

# BGM tags for AI to select mood
# Each mood maps to a directory under bgm/
# AI should pick the mood that best matches the video content
BGM_MOODS = {
    "healing": {
        "description": "治愈温暖，适合：咖啡馆、阳光、花开、微笑、拥抱、温馨日常",
        "keywords": ["温暖", "治愈", "阳光", "咖啡", "花", "日常", "幸福", "陪伴"],
    },
    "quiet": {
        "description": "安静平和，适合：深夜、雨天、独处、冥想、读书、窗边发呆",
        "keywords": ["安静", "深夜", "雨", "独处", "冥想", "宁静", "月光", "星空"],
    },
    "warm": {
        "description": "温馨感动，适合：重逢、家、童年回忆、老照片、牵手、陪伴",
        "keywords": ["感动", "家", "童年", "回忆", "重逢", "牵手", "温馨", "守护"],
    },
    "melancholy": {
        "description": "淡淡忧伤，适合：离别、秋天、独行、黄昏、空荡街道、思念",
        "keywords": ["离别", "秋天", "忧伤", "思念", "孤独", "黄昏", "远方", "告别"],
    },
    "dreamy": {
        "description": "梦幻飘渺，适合：云海、极光、水下、星河、魔法、仙境",
        "keywords": ["梦幻", "星河", "极光", "云海", "水下", "仙境", "飘渺", "奇幻"],
    },
    "citynight": {
        "description": "都市夜景，适合：霓虹灯、深夜街头、便利店、出租车、天桥、城市天际线",
        "keywords": ["城市", "夜", "霓虹", "街头", "便利店", "天桥", "都市", "灯光"],
    },
    "nature": {
        "description": "自然之声，适合：森林、溪流、海浪、鸟鸣、田野、山谷",
        "keywords": ["自然", "森林", "海", "溪流", "山", "田野", "鸟", "风"],
    },
}


def _create_service() -> VisualService:
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
    sk = os.environ.get("VOLCENGINE_SECRET_KEY", "")
    if not ak or not sk:
        print("Error: VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY must be set")
        sys.exit(1)
    service = VisualService()
    service.set_ak(ak)
    service.set_sk(sk)
    return service


def _get_video_duration(path: str) -> float:
    """Get video duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())
    except (ValueError, AttributeError):
        # Fallback: estimate from file size and typical bitrate
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-count_frames",
                 "-select_streams", "v:0",
                 "-show_entries", "stream=nb_read_frames,r_frame_rate",
                 "-of", "csv=p=0", path],
                capture_output=True, text=True,
            )
            parts = result.stdout.strip().split(",")
            if len(parts) >= 2:
                fps_str = parts[0]
                frames = int(parts[1])
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = float(num) / float(den)
                else:
                    fps = float(fps_str)
                return frames / fps
        except Exception:
            pass
        # Last resort: assume 5 seconds per clip * number of clips
        print("Warning: Could not determine video duration, assuming 20s")
        return 20.0


def generate_clips(prompts: list[str], output_dir: str) -> list[str]:
    """Generate multiple video clips from prompts. Returns list of file paths."""
    service = _create_service()
    os.makedirs(output_dir, exist_ok=True)
    saved = []

    for i, prompt in enumerate(prompts):
        print(f"\n=== Clip {i+1}/{len(prompts)} ===")
        form = {
            "req_key": REQ_KEY,
            "prompt": prompt,
            "seed": -1,
            "frames": FRAMES,
            "aspect_ratio": "9:16",
        }
        result = service.cv_sync2async_submit_task(form)
        task_id = result["data"]["task_id"]
        print(f"  Task: {task_id}")

        for attempt in range(120):
            try:
                query = {"req_key": REQ_KEY, "task_id": task_id}
                result = service.cv_sync2async_get_result(query)
                data = result.get("data", {})
                status = data.get("status", "")
                if status == "done":
                    video_url = data.get("video_url", "")
                    if video_url:
                        path = os.path.join(output_dir, f"clip_{i+1}.mp4")
                        urllib.request.urlretrieve(video_url, path)
                        size_mb = os.path.getsize(path) / (1024 * 1024)
                        print(f"  Saved: clip_{i+1}.mp4 ({size_mb:.1f} MB)")
                        saved.append(path)
                    break
                if attempt % 6 == 0:
                    print(f"  {status}... ({attempt*5}s)")
            except Exception:
                if attempt % 6 == 0:
                    print(f"  waiting... ({attempt*5}s)")
            time.sleep(5)

    print(f"\n{len(saved)}/{len(prompts)} clips generated.")
    return saved


def stitch_clips(clip_paths: list[str], output_path: str) -> str:
    """Stitch multiple clips into one video, normalize format."""
    output_dir = os.path.dirname(output_path)

    # Normalize each clip to same format
    fixed_paths = []
    for i, clip in enumerate(clip_paths):
        fixed = os.path.join(output_dir, f"_fixed_{i}.mp4")
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", clip,
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-r", "24", "-s", "1080x1920", "-an",
                "-vf", "setsar=1",
                fixed,
            ],
            capture_output=True,
        )
        fixed_paths.append(fixed)

    # Create concat file
    concat_file = os.path.join(output_dir, "_concat.txt")
    with open(concat_file, "w") as f:
        for path in fixed_paths:
            f.write(f"file '{os.path.basename(path)}'\n")

    # Concat
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file, "-c", "copy", output_path,
        ],
        capture_output=True,
    )

    # Cleanup temp files
    for f in fixed_paths:
        os.remove(f)
    os.remove(concat_file)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Stitched: {output_path} ({size_mb:.1f} MB)")
    return output_path


def add_text_overlay(input_path: str, output_path: str, lines: list[str]) -> str:
    """Add centered text overlay to video."""
    if not lines:
        shutil.copy2(input_path, output_path)
        return output_path

    if not os.path.exists(FONT):
        print(f"Warning: Font not found at {FONT}, skipping text overlay")
        shutil.copy2(input_path, output_path)
        return output_path

    filters = []
    for i, line in enumerate(lines):
        escaped = line.replace("'", "\\'").replace(":", "\\:")
        y_pos = f"h/2-{(len(lines)-1)*50}+{i*100}"
        size = 80 if i == 0 else 52
        filters.append(
            f"drawtext=fontfile='{FONT}':text='{escaped}'"
            f":fontsize={size}:fontcolor=white"
            f":x=(w-text_w)/2:y={y_pos}"
            f":shadowcolor=black@0.6:shadowx=3:shadowy=3"
        )

    vf = ",".join(filters)
    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", input_path,
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            output_path,
        ],
        capture_output=True, text=True,
    )

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print(f"Warning: Text overlay failed: {result.stderr[-200:] if result.stderr else 'unknown error'}")
        print("Using video without text overlay")
        shutil.copy2(input_path, output_path)

    return output_path


def select_bgm(bgm_dir: str, mood: str) -> str:
    """Select a BGM file from the mood directory. Falls back to any available BGM."""
    if not bgm_dir:
        return ""

    # Try exact mood directory first
    mood_dir = os.path.join(bgm_dir, mood)
    if os.path.isdir(mood_dir):
        files = glob.glob(os.path.join(mood_dir, "*.mp3")) + glob.glob(os.path.join(mood_dir, "*.m4a"))
        if files:
            chosen = random.choice(files)
            print(f"BGM ({mood}): {os.path.basename(chosen)}")
            return chosen

    # Fallback: try any mood directory with files
    for fallback_mood in BGM_MOODS:
        fallback_dir = os.path.join(bgm_dir, fallback_mood)
        if os.path.isdir(fallback_dir):
            files = glob.glob(os.path.join(fallback_dir, "*.mp3")) + glob.glob(os.path.join(fallback_dir, "*.m4a"))
            if files:
                chosen = random.choice(files)
                print(f"BGM (fallback {fallback_mood}): {os.path.basename(chosen)}")
                return chosen

    return ""


def add_bgm(input_path: str, output_path: str, bgm_dir: str = "", mood: str = "healing") -> str:
    """Add background music to video."""
    bgm_file = select_bgm(bgm_dir, mood)

    if not bgm_file:
        # Generate ambient noise as fallback
        print("No BGM files found, generating ambient sound...")
        bgm_file = input_path + ".ambient.mp3"
        subprocess.run(
            [
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", "anoisesrc=d=120:c=pink:r=44100:a=0.025",
                "-af", "lowpass=f=1800,highpass=f=200",
                "-t", "120", bgm_file,
            ],
            capture_output=True,
        )

    duration = _get_video_duration(input_path)
    fade_out_start = max(0, duration - 2)

    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", input_path, "-i", bgm_file,
            "-filter_complex",
            f"[1:a]afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start:.1f}:d=2,volume=0.5[bgm]",
            "-map", "0:v", "-map", "[bgm]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            output_path,
        ],
        capture_output=True, text=True,
    )

    # Cleanup temp ambient file
    if bgm_file.endswith(".ambient.mp3"):
        os.remove(bgm_file)

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print(f"Warning: BGM merge failed: {result.stderr[-200:] if result.stderr else 'unknown'}")
        print("Using video without BGM")
        shutil.copy2(input_path, output_path)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Final video: {output_path} ({size_mb:.1f} MB, {duration:.0f}s)")
    return output_path


def full_pipeline(
    prompts: list[str],
    output_dir: str,
    text_lines: list[str],
    bgm_dir: str = "",
    mood: str = "healing",
) -> str:
    """Full pipeline: generate clips -> stitch -> add text -> add BGM."""
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Generate clips
    print("=" * 40)
    print("Step 1: Generating video clips...")
    print("=" * 40)
    clips = generate_clips(prompts, output_dir)
    if not clips:
        print("Error: No clips generated")
        sys.exit(1)

    # Step 2: Stitch
    print("\n" + "=" * 40)
    print("Step 2: Stitching clips...")
    print("=" * 40)
    merged = os.path.join(output_dir, "merged.mp4")
    stitch_clips(clips, merged)

    # Step 3: Add text overlay
    print("\n" + "=" * 40)
    print("Step 3: Adding text overlay...")
    print("=" * 40)
    with_text = os.path.join(output_dir, "with_text.mp4")
    add_text_overlay(merged, with_text, text_lines)

    # Step 4: Add BGM
    print("\n" + "=" * 40)
    print("Step 4: Adding BGM...")
    print("=" * 40)
    final = os.path.join(output_dir, "final.mp4")
    add_bgm(with_text, final, bgm_dir, mood)

    return final


def print_mood_tags():
    """Print available BGM mood tags for AI reference."""
    print("\nAvailable BGM moods:")
    for mood, info in BGM_MOODS.items():
        print(f"  {mood}: {info['description']}")
        print(f"    keywords: {', '.join(info['keywords'])}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Video Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # full pipeline
    full_parser = subparsers.add_parser("create", help="Full pipeline")
    full_parser.add_argument("--prompts", required=True, help="JSON file with prompt list")
    full_parser.add_argument("--output", required=True, help="Output directory")
    full_parser.add_argument("--text", required=True, help="Overlay text lines, separated by |")
    full_parser.add_argument("--bgm-dir", default="", help="BGM directory")
    full_parser.add_argument("--mood", default="healing", help="BGM mood: " + ", ".join(BGM_MOODS.keys()))

    # generate only
    gen_parser = subparsers.add_parser("generate", help="Generate clips only")
    gen_parser.add_argument("--prompts", required=True, help="JSON file with prompt list")
    gen_parser.add_argument("--output", required=True, help="Output directory")

    # stitch only
    stitch_parser = subparsers.add_parser("stitch", help="Stitch and finalize")
    stitch_parser.add_argument("--input", required=True, help="Directory with clip_*.mp4 files")
    stitch_parser.add_argument("--text", default="", help="Overlay text lines, separated by |")
    stitch_parser.add_argument("--bgm-dir", default="", help="BGM directory")
    stitch_parser.add_argument("--mood", default="healing", help="BGM mood")

    # list moods
    subparsers.add_parser("moods", help="List available BGM mood tags")

    args = parser.parse_args()

    if args.command == "create":
        with open(args.prompts) as f:
            prompts = json.load(f)
        text_lines = args.text.split("|") if args.text else []
        result = full_pipeline(prompts, args.output, text_lines, args.bgm_dir, args.mood)
        print(f"\nDone! Final video: {result}")

    elif args.command == "generate":
        with open(args.prompts) as f:
            prompts = json.load(f)
        generate_clips(prompts, args.output)

    elif args.command == "stitch":
        clips = sorted(glob.glob(os.path.join(args.input, "clip_*.mp4")))
        if not clips:
            print("No clip_*.mp4 files found")
            sys.exit(1)
        merged = os.path.join(args.input, "merged.mp4")
        stitch_clips(clips, merged)
        if args.text:
            with_text = os.path.join(args.input, "with_text.mp4")
            add_text_overlay(merged, with_text, args.text.split("|"))
            merged = with_text
        final = os.path.join(args.input, "final.mp4")
        add_bgm(merged, final, args.bgm_dir, args.mood)
        print(f"\nDone! Final video: {final}")

    elif args.command == "moods":
        print_mood_tags()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
