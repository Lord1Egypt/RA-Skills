#!/usr/bin/env python3
"""
Build a subtitle preview mp4 from audio + srt for quick manual checking.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def escape_subtitles_path(path: str) -> str:
    # Escape characters that are special in ffmpeg filter expressions.
    return (
        path.replace("\\", "\\\\")
        .replace(":", r"\:")
        .replace(",", r"\,")
        .replace("'", r"\'")
        .replace("[", r"\[")
        .replace("]", r"\]")
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate preview mp4 by burning SRT subtitles onto black background."
    )
    parser.add_argument("--audio", required=True, help="Path to source audio.")
    parser.add_argument("--srt", required=True, help="Path to source srt.")
    parser.add_argument(
        "--output",
        default="preview_check.mp4",
        help="Output mp4 path. Default: preview_check.mp4 in current directory.",
    )
    parser.add_argument("--width", type=int, default=1280, help="Video width.")
    parser.add_argument("--height", type=int, default=720, help="Video height.")
    parser.add_argument("--fps", type=int, default=25, help="Video fps.")
    parser.add_argument("--font", default="Arial Unicode MS", help="Subtitle font name.")
    parser.add_argument("--font-size", type=int, default=38, help="Subtitle font size.")
    parser.add_argument("--preset", default="veryfast", help="x264 preset.")
    parser.add_argument("--crf", type=int, default=23, help="x264 crf.")
    parser.add_argument("--audio-bitrate", default="192k", help="AAC bitrate.")
    parser.add_argument("--background", default="black", help="Background color.")
    parser.add_argument(
        "--ffmpeg-bin",
        default="ffmpeg",
        help="ffmpeg binary path or name in PATH.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audio_path = Path(args.audio).expanduser().resolve()
    srt_path = Path(args.srt).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")
    if not srt_path.exists():
        raise SystemExit(f"SRT file not found: {srt_path}")

    ffmpeg_bin = args.ffmpeg_bin
    if not shutil.which(ffmpeg_bin):
        raise SystemExit(
            f"ffmpeg not found: {ffmpeg_bin}. "
            "Use --ffmpeg-bin to provide a full path."
        )

    escaped_srt = escape_subtitles_path(str(srt_path))
    force_style = (
        f"FontName={args.font},"
        f"FontSize={args.font_size},"
        "PrimaryColour=&H00FFFFFF&,"
        "OutlineColour=&H00000000&,"
        "BorderStyle=1,"
        "Outline=2,"
        "Shadow=0,"
        "Alignment=2"
    )
    video_filter = f"subtitles='{escaped_srt}':force_style='{force_style}'"

    cmd = [
        ffmpeg_bin,
        "-y",
        "-v",
        "warning",
        "-f",
        "lavfi",
        "-i",
        f"color=c={args.background}:s={args.width}x{args.height}:r={args.fps}",
        "-i",
        str(audio_path),
        "-vf",
        video_filter,
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        args.audio_bitrate,
        "-shortest",
        str(output_path),
    ]

    subprocess.run(cmd, check=True)
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
