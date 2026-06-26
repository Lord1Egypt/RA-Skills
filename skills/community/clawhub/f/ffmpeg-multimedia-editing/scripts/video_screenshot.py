# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    emit_multi_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从视频中提取截图")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--time", help="指定时间截图（格式：HH:MM:SS 或秒数）")
    parser.add_argument("--interval", type=float, help="按间隔（秒）截图")
    parser.add_argument("--count", type=int, help="均匀提取 N 张截图")
    parser.add_argument("--format", choices=["png", "jpg", "jpeg"], default="png", help="输出图片格式")
    parser.add_argument("--output-dir", type=Path, help="输出目录（不指定则自动生成）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    duration = probe.duration

    suffix = f".{args.format}"

    with timer() as t:
        if args.time:
            # Single frame at specific time
            output_path = build_output_path("screenshot", input_path, suffix=suffix)
            seconds = float(args.time) if args.time.replace(".", "").isdigit() else None
            if seconds is None:
                from common import parse_time_to_seconds
                seconds = parse_time_to_seconds(args.time)

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(seconds),
                "-i", str(input_path),
                "-frames:v", "1",
                "-q:v", "2",
                str(output_path),
            ]
            run_ffmpeg(cmd)

            emit_result(
                type="image",
                operation="screenshot",
                local_path=output_path,
                input_path=input_path,
                time=args.time,
                elapsed=t(),
            )

        elif args.interval and args.interval > 0:
            # Periodic screenshots
            out_dir = args.output_dir or build_output_path("screenshot", input_path).parent
            out_dir.mkdir(parents=True, exist_ok=True)
            output_pattern = str(out_dir / f"screenshot_%04d{suffix}")

            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-vf", f"fps=1/{args.interval}",
                "-q:v", "2",
                output_pattern,
            ]
            run_ffmpeg(cmd)

            # Collect output files
            outputs = sorted(out_dir.glob(f"screenshot_*{suffix}"))
            emit_multi_result(
                type="image",
                operation="screenshot",
                local_paths=outputs,
                input_path=input_path,
                mode="interval",
                interval=args.interval,
                elapsed=t(),
            )

        elif args.count and args.count > 0:
            # N evenly-spaced frames
            out_dir = args.output_dir or build_output_path("screenshot", input_path).parent
            out_dir.mkdir(parents=True, exist_ok=True)
            outputs = []
            for i in range(args.count):
                ts = (duration / (args.count + 1)) * (i + 1)
                out_path = out_dir / f"screenshot_{i + 1:04d}{suffix}"
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(ts),
                    "-i", str(input_path),
                    "-frames:v", "1",
                    "-q:v", "2",
                    str(out_path),
                ]
                run_ffmpeg(cmd)
                outputs.append(out_path)

            emit_multi_result(
                type="image",
                operation="screenshot",
                local_paths=outputs,
                input_path=input_path,
                mode="count",
                count=args.count,
                elapsed=t(),
            )

        else:
            from common import emit_error
            print("错误: 请指定 --time、--interval 或 --count 中的一个", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
