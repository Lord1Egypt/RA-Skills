#!/usr/bin/env python3
"""
Content Slide Renderer — Pillow frame-by-frame + FFmpeg pipe.

Renders animated content slides with progressive text reveal in a terminal/IDE
aesthetic. Each slide shows lines of text appearing one at a time.

Usage:
    python3 render_slides.py \
        --lines "line1|line2|line3" \
        --duration 30 \
        --fps 24 \
        --resolution 1280x720 \
        --output content_1.mp4

The --lines parameter accepts pipe-separated lines. Whitespace lines are rendered
as blank spacing.
"""

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


def render_slides(lines, duration, fps, resolution, output_path, bg_color="#1a1a2e",
                  text_color="#00ff41", accent_color="#ffffff", font_size=32,
                  title_size=48, font_path=None):
    """
    Render animated content slides.

    Parameters:
        lines: list of text lines to display
        duration: total video duration in seconds
        fps: frames per second
        resolution: (width, height) tuple
        output_path: output .mp4 file
        bg_color: background color (hex)
        text_color: primary text color (hex)
        accent_color: accent/highlight color (hex)
        font_size: body text font size
        title_size: title font size
        font_path: path to font file (auto-detect if None)
    """
    width, height = resolution
    total_frames = int(duration * fps)

    # Font setup
    if font_path is None:
        # Try common macOS Chinese font locations
        candidates = [
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
        for fp in candidates:
            if Path(fp).exists():
                font_path = fp
                break
        if font_path is None:
            font_path = "/System/Library/Fonts/STHeiti Medium.ttc"

    try:
        font_body = ImageFont.truetype(font_path, font_size)
        font_title = ImageFont.truetype(font_path, title_size)
    except Exception as e:
        print(f"Warning: Could not load font {font_path}: {e}")
        font_body = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Start FFmpeg process
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        output_path,
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Calculate reveal timing
    non_empty_lines = [l for l in lines if l.strip()]
    if not non_empty_lines:
        non_empty_lines = [" "]

    frames_per_line = total_frames // (len(non_empty_lines) + 1)
    if frames_per_line < 10:
        frames_per_line = 10

    margin_left = 60
    line_height = font_size + 12
    start_y = (height - len(lines) * line_height) // 2

    for frame_idx in range(total_frames):
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Which lines are revealed so far
        revealed_count = min(frame_idx // frames_per_line, len(non_empty_lines))

        # Track non-empty line index for reveal
        displayed_lines = 0
        for i, line in enumerate(lines):
            y = start_y + i * line_height

            if line.strip():
                displayed_lines += 1
                if displayed_lines <= revealed_count:
                    color = text_color if not line.startswith("#") else accent_color
                    draw.text((margin_left, y), line, fill=color, font=font_body)
            else:
                # Blank line: always render as spacing (no text)
                pass

        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        print(f"Error: FFmpeg exited with code {proc.returncode}", file=sys.stderr)
        sys.exit(1)

    print(f"Rendered {total_frames} frames → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Render content slides as video")
    parser.add_argument("--lines", type=str, required=True,
                        help="Pipe-separated text lines, e.g. 'line1|line2|line3'")
    parser.add_argument("--duration", type=float, required=True,
                        help="Video duration in seconds")
    parser.add_argument("--fps", type=int, default=24, help="Frame rate (default: 24)")
    parser.add_argument("--resolution", type=str, default="1280x720",
                        help="Resolution WxH (default: 1280x720)")
    parser.add_argument("--output", type=str, required=True, help="Output .mp4 file")
    parser.add_argument("--bg-color", type=str, default="#1a1a2e",
                        help="Background color hex (default: #1a1a2e)")
    parser.add_argument("--text-color", type=str, default="#00ff41",
                        help="Text color hex (default: #00ff41)")
    parser.add_argument("--accent-color", type=str, default="#ffffff",
                        help="Accent color hex (default: #ffffff)")
    parser.add_argument("--font-size", type=int, default=32, help="Font size")
    parser.add_argument("--title-size", type=int, default=48, help="Title font size")
    parser.add_argument("--font", type=str, default=None, help="Font file path")

    args = parser.parse_args()

    lines = args.lines.split("|")
    w, h = map(int, args.resolution.split("x"))
    resolution = (w, h)

    render_slides(
        lines=lines,
        duration=args.duration,
        fps=args.fps,
        resolution=resolution,
        output_path=args.output,
        bg_color=args.bg_color,
        text_color=args.text_color,
        accent_color=args.accent_color,
        font_size=args.font_size,
        title_size=args.title_size,
        font_path=args.font,
    )


if __name__ == "__main__":
    main()
