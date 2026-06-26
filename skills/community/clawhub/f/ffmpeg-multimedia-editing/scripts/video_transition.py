# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import (
    XFADER_TRANSITIONS,
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="在两段视频之间添加过渡特效")
    parser.add_argument("--inputs", required=True, nargs=2, type=Path, help="两个输入视频文件")
    parser.add_argument("--type", default="fade",
                        choices=XFADER_TRANSITIONS,
                        help="过渡类型（默认 fade）")
    parser.add_argument("--duration", type=float, default=1.0, help="过渡时长（秒，默认 1）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_a = validate_video_file(args.inputs[0])
    input_b = validate_video_file(args.inputs[1])

    probe_a = run_ffprobe(input_a)
    probe_b = run_ffprobe(input_b)

    if probe_a.duration <= args.duration:
        print(f"错误: 第一个视频时长 ({probe_a.duration:.1f}s) 必须大于过渡时长 ({args.duration}s)", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or build_output_path("transition", input_a)

    offset = probe_a.duration - args.duration

    with timer() as t:
        filter_parts = []
        if probe_a.has_audio and probe_b.has_audio:
            filter_complex = (
                f"[0:v][1:v]xfade=transition={args.type}:duration={args.duration}:offset={offset}[v];"
                f"[0:a][1:a]acrossfade=d={args.duration}:c1=tri:c2=tri[a]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_a), "-i", str(input_b),
                "-filter_complex", filter_complex,
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-c:a", "aac",
                str(output_path),
            ]
        else:
            filter_complex = (
                f"[0:v][1:v]xfade=transition={args.type}:duration={args.duration}:offset={offset}[v]"
            )
            audio_map = []
            if probe_a.has_audio or probe_b.has_audio:
                audio_map = ["-map", "0:a?", "-map", "1:a?", "-c:a", "aac"]
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_a), "-i", str(input_b),
                "-filter_complex", filter_complex,
                "-map", "[v]",
                *audio_map,
                "-c:v", "libx264",
                str(output_path),
            ]

        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="transition",
        local_path=output_path,
        input_paths=[str(input_a), str(input_b)],
        transition_type=args.type,
        transition_duration=args.duration,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
