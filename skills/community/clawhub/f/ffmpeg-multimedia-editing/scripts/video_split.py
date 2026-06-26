# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from common import (
    build_segment_path,
    emit_multi_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按时长分段拆分视频")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--segment-duration", type=float, help="每段时长（秒）")
    parser.add_argument("--segments", type=int, help="拆分为 N 段")
    parser.add_argument("--output-dir", type=Path, help="输出目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.segment_duration and not args.segments:
        print("错误: 必须指定 --segment-duration 或 --segments", file=sys.stderr)
        sys.exit(1)

    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    suffix = input_path.suffix

    if args.segments:
        segment_duration = probe.duration / args.segments
    else:
        segment_duration = args.segment_duration

    output_dir = args.output_dir or build_segment_path("split", 0).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = str(output_dir / f"segment_%03d{suffix}")

    with timer() as t:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c", "copy",
            "-f", "segment",
            "-segment_time", str(segment_duration),
            "-reset_timestamps", "1",
            output_pattern,
        ]
        run_ffmpeg(cmd)

    # Collect output files
    outputs = sorted(output_dir.glob(f"segment_*{suffix}"))

    emit_multi_result(
        type="video",
        operation="split",
        local_paths=outputs,
        input_path=input_path,
        segment_duration=segment_duration,
        original_duration=probe.duration,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
