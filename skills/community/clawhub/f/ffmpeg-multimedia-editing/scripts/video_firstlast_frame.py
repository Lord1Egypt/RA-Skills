# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="提取视频的首帧和尾帧")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--format", choices=["png", "jpg", "jpeg"], default="png", help="输出图片格式")
    parser.add_argument("--output-dir", type=Path, help="输出目录（不指定则自动生成）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    suffix = f".{args.format}"

    out_dir = args.output_dir or build_output_path("firstlast_frame", input_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem
    first_path = out_dir / f"{stem}_first_frame{suffix}"
    last_path = out_dir / f"{stem}_last_frame{suffix}"

    with timer() as t:
        # First frame
        cmd_first = [
            "ffmpeg", "-y",
            "-ss", "0",
            "-i", str(input_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(first_path),
        ]
        run_ffmpeg(cmd_first)

        # Last frame: use -sseof to seek near the end
        cmd_last = [
            "ffmpeg", "-y",
            "-sseof", "-0.1",
            "-i", str(input_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(last_path),
        ]
        run_ffmpeg(cmd_last)

    emit_result(
        type="image",
        operation="firstlast_frame",
        local_path=first_path,
        input_path=input_path,
        first_frame=str(first_path),
        last_frame=str(last_path),
        duration=probe.duration,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
