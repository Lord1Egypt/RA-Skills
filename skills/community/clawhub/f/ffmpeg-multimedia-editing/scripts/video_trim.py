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
    parse_time_to_seconds,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="剪辑视频片段")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--start", required=True, help="起始时间（HH:MM:SS 或秒数）")
    parser.add_argument("--end", help="结束时间（HH:MM:SS 或秒数）")
    parser.add_argument("--duration", type=float, help="持续时长（秒），与 --end 互斥")
    parser.add_argument("--reencode", action="store_true", help="重新编码（更精确但更慢）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.end and args.duration:
        print("错误: --end 和 --duration 不能同时使用", file=sys.stderr)
        sys.exit(1)

    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    output_path = args.output or build_output_path("trim", input_path)

    start = parse_time_to_seconds(args.start)
    if args.end:
        end = parse_time_to_seconds(args.end)
        if end <= start:
            print("错误: 结束时间必须大于起始时间", file=sys.stderr)
            sys.exit(1)
    elif args.duration:
        end = start + args.duration
    else:
        end = probe.duration

    if end > probe.duration:
        print(f"警告: 结束时间 ({end}s) 超过视频时长 ({probe.duration}s)，已调整", file=sys.stderr)
        end = probe.duration

    with timer() as t:
        if args.reencode:
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-to", str(end),
                "-i", str(input_path),
                "-c:v", "libx264", "-c:a", "aac",
                str(output_path),
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start),
                "-to", str(end),
                "-i", str(input_path),
                "-c", "copy",
                str(output_path),
            ]
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="trim",
        local_path=output_path,
        input_path=input_path,
        start=start,
        end=end,
        duration=end - start,
        reencoded=args.reencode,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
