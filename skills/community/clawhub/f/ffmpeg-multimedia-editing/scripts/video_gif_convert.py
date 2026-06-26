# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_input_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频与 GIF 互转")
    parser.add_argument("--input", required=True, type=Path, help="输入文件路径")
    parser.add_argument("--to", required=True, choices=["gif", "mp4"], help="转换目标格式")
    parser.add_argument("--fps", type=int, default=15, help="GIF 帧率（默认 15）")
    parser.add_argument("--width", type=int, default=480, help="GIF 宽度（默认 480，高度自动按比例）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)

    if args.to == "gif":
        probe = run_ffprobe(input_path)
        output_path = args.output or build_output_path("gif", input_path, suffix=".gif")

        palette_path = None
        try:
            with timer() as t:
                # Pass 1: Generate palette
                palette_path = output_path.with_suffix(".palette.png")
                cmd_palette = [
                    "ffmpeg", "-y",
                    "-i", str(input_path),
                    "-vf", f"fps={args.fps},scale={args.width}:-1:flags=lanczos,palettegen",
                    str(palette_path),
                ]
                run_ffmpeg(cmd_palette)

                # Pass 2: Apply palette
                cmd_gif = [
                    "ffmpeg", "-y",
                    "-i", str(input_path),
                    "-i", str(palette_path),
                    "-lavfi", f"fps={args.fps},scale={args.width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                    str(output_path),
                ]
                run_ffmpeg(cmd_gif)

            gif_size = output_path.stat().st_size if output_path.exists() else 0

            emit_result(
                type="image",
                operation="gif_convert",
                local_path=output_path,
                input_path=input_path,
                target_format="gif",
                fps=args.fps,
                width=args.width,
                gif_size=gif_size,
                elapsed=t(),
            )
        finally:
            if palette_path and palette_path.exists():
                palette_path.unlink(missing_ok=True)

    elif args.to == "mp4":
        output_path = args.output or build_output_path("gif_to_mp4", input_path, suffix=".mp4")

        with timer() as t:
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                str(output_path),
            ]
            run_ffmpeg(cmd)

        emit_result(
            type="video",
            operation="gif_convert",
            local_path=output_path,
            input_path=input_path,
            target_format="mp4",
            elapsed=t(),
        )


if __name__ == "__main__":
    main()
