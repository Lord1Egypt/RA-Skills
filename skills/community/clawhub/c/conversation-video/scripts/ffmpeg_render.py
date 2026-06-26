#!/usr/bin/env python3
"""
ffmpeg_render.py — Render a conversation video with timed text overlays.

Reads a timing manifest (from generate_audio.py) and produces an MP4
with speaker-labeled text timed to an audio track.

Usage:
    python ffmpeg_render.py timings.json audio.wav output.mp4

Opts:
    --width 1280          video width
    --height 720          video height
    --fps 30              video fps
    --bg 0x0b1021         background color
    --font-size 24        base font size
    --font /path/to.ttf   font file
    --no-audio            skip audio input (silent video)
    --padding 80          horizontal padding in px

The script auto-generates an ffmpeg drawtext filter chain and runs it.
"""

import json
import os
import sys
import subprocess
import argparse


def find_ffmpeg():
    for candidate in ["/usr/lib/jellyfin-ffmpeg/ffmpeg", "ffmpeg"]:
        try:
            subprocess.run([candidate, "-version"], capture_output=True, check=True)
            return candidate
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print("ERROR: ffmpeg not found", file=sys.stderr)
    sys.exit(1)


def find_font():
    """Probe system for a usable sans-serif font."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # Fallback: let ffmpeg use default
    return None


def build_drawtext_filter(timings, width, height, font_file, base_font_size, padding):
    """Build ffmpeg drawtext filter string from timing manifest."""
    # Speaker color map
    colors = {
        "NARRATOR": "#cbd5e1",
        "INTERVIEWER": "#60a5fa",
        "CUSTOMER": "#34d399",
    }
    align_map = {
        "left": "left",
        "right": "right",
        "center": "center",
    }

    filters = []
    intro_end = timings[0]["start"] if timings else 2.5
    # Try to auto-detect intro end from first non-narrator or just use first segment start

    # Title card if first speaker is NARRATOR and starts at 0
    if timings and timings[0]["speaker"].upper() == "NARRATOR" and timings[0]["start"] < 0.1:
        t = timings[0]
        # Centered title
        filters.append(
            f"drawtext=fontfile={font_file}:text='{escape(t['text'])}':"
            f"fontsize={base_font_size + 8}:fontcolor=#f8fafc:x=(w-text_w)/2:y={height//2 - 40}:"
            f"enable='between(t\\,0\\,{t['end']})'"
        )
        intro_end = t["end"]

    for t in timings:
        speaker = t["speaker"].upper()
        text = t["text"]
        start = t["start"]
        end = t["end"]
        align = align_map.get(t.get("align", "center"), "center")
        color = colors.get(speaker, "#f8fafc")

        # Speaker label
        label_cfg = f"drawtext=fontfile={font_file}:text='{speaker}':"
        if align == "left":
            label_cfg += f"fontsize={max(11, base_font_size - 13)}:fontcolor={color}:x={padding}:y={height//2 - 60}:"
        elif align == "right":
            label_cfg += f"fontsize={max(11, base_font_size - 13)}:fontcolor={color}:x=(w-text_w-{padding}):y={height//2 - 60}:"
        else:
            label_cfg += f"fontsize={max(11, base_font_size - 13)}:fontcolor={color}:x=(w-text_w)/2:y={height//2 - 60}:"
        label_cfg += f"enable='between(t\\,{start}\\,{end})'"
        filters.append(label_cfg)

        # Main text — split long lines at ~40 chars
        lines = split_lines(text, 40)
        for li, line in enumerate(lines):
            line_cfg = f"drawtext=fontfile={font_file}:text='{escape(line)}':"
            line_cfg += f"fontsize={base_font_size}:fontcolor=#f8fafc:"
            if align == "left":
                line_cfg += f"x={padding}:y={height//2 - 30 + li * (base_font_size + 10)}:"
            elif align == "right":
                line_cfg += f"x=(w-text_w-{padding}):y={height//2 - 30 + li * (base_font_size + 10)}:"
            else:
                line_cfg += f"x=(w-text_w)/2:y={height//2 - 30 + li * (base_font_size + 10)}:"
            line_cfg += f"enable='between(t\\,{start}\\,{end})'"
            filters.append(line_cfg)

    return ",".join(filters)


def split_lines(text, max_chars):
    """Split text into lines of max_chars width by words."""
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 > max_chars:
            lines.append(current.strip())
            current = w
        else:
            current = (current + " " + w).strip()
    if current:
        lines.append(current.strip())
    return lines if lines else [text]


def escape(s):
    """Escape special chars for ffmpeg drawtext text parameter."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def main():
    parser = argparse.ArgumentParser(description="Render conversation video via ffmpeg")
    parser.add_argument("timings", help="Timing JSON manifest")
    parser.add_argument("audio", help="Audio file (wav/mp3)")
    parser.add_argument("output", help="Output MP4 path")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--bg", default="0x0b1021")
    parser.add_argument("--font-size", type=int, default=24)
    parser.add_argument("--font", default=None, help="Path to TTF font")
    parser.add_argument("--no-audio", action="store_true", help="Skip audio track")
    parser.add_argument("--padding", type=int, default=80)
    parser.add_argument("--crf", type=int, default=23)
    parser.add_argument("--preset", default="fast")
    args = parser.parse_args()

    with open(args.timings) as f:
        timings = json.load(f)

    ffmpeg = find_ffmpeg()
    font_file = args.font or find_font()
    if not font_file:
        print("WARNING: no font found, ffmpeg will use default", file=sys.stderr)
        font_file = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    # Compute total duration
    total_dur = max(t["end"] for t in timings) if timings else 10

    vf = build_drawtext_filter(timings, args.width, args.height, font_file, args.font_size, args.padding)

    cmd = [
        ffmpeg, "-y",
        "-f", "lavfi", "-i", f"color=c={args.bg}:s={args.width}x{args.height}:d={total_dur}:r={args.fps}",
    ]

    if not args.no_audio:
        cmd += ["-i", args.audio]

    cmd += ["-vf", vf]
    cmd += ["-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf)]

    if not args.no_audio:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-shortest"]
    else:
        cmd += ["-an"]

    cmd += ["-movflags", "+faststart", args.output]

    print("Running ffmpeg...")
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-2000:], file=sys.stderr)
        sys.exit(1)

    print(f"Done! {args.output}")


if __name__ == "__main__":
    main()
