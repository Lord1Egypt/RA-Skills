# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    timer,
    validate_input_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从图片序列合成视频（可选背景音乐）")
    parser.add_argument("--images", required=True, type=Path, help="图片文件或目录（支持通配符，需要 shell 展开）")
    parser.add_argument("--image-pattern", help="图片序列模式（如 img_%04d.png）")
    parser.add_argument("--duration", type=float, default=5.0, help="每张图片显示时长（秒，默认 5）")
    parser.add_argument("--framerate", type=float, help="输出帧率（不指定则由 duration 推算）")
    parser.add_argument("--audio", type=Path, help="背景音乐文件路径")
    parser.add_argument("--resolution", help="输出分辨率（如 1920x1080）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.images)

    output_path = args.output or build_output_path("image_compose", input_path, suffix=".mp4")

    # Determine input mode
    if args.image_pattern:
        # Sequence mode: img_%04d.png
        input_mode = "sequence"
        input_source = args.image_pattern
    elif input_path.is_dir():
        # Directory mode: collect images sorted
        image_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
        images = sorted(
            p for p in input_path.iterdir()
            if p.is_file() and p.suffix.lower() in image_exts
        )
        if not images:
            print(f"错误: 目录中未找到图片文件: {input_path}", file=sys.stderr)
            sys.exit(1)
        input_mode = "directory"
        input_source = str(input_path)
    else:
        # Single file as pattern
        input_mode = "single"
        input_source = str(input_path)

    fps = args.framerate or (1.0 / args.duration)

    with timer() as t:
        cmd = ["ffmpeg", "-y"]

        if input_mode == "sequence":
            cmd.extend(["-framerate", str(fps), "-i", input_source])
        elif input_mode == "directory":
            cmd.extend(["-framerate", str(fps), "-i", str(input_path)])
        else:
            # Single image, loop it
            cmd.extend(["-loop", "1", "-framerate", str(fps), "-i", str(input_path)])

        if args.audio:
            audio_path = validate_input_file(args.audio)
            cmd.extend(["-i", str(audio_path)])
            cmd.extend(["-shortest"])

        if args.resolution:
            cmd.extend(["-vf", f"scale={args.resolution}"])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
        ])

        if args.audio:
            cmd.extend(["-c:a", "aac", "-b:a", "192k"])

        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="image_compose",
        local_path=output_path,
        input_path=input_source,
        image_duration=args.duration,
        fps=fps,
        has_audio=bool(args.audio),
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
