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
    forward_slash,
    run_ffmpeg,
    validate_input_file,
    timer,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="拼接多个音频文件")
    parser.add_argument("--inputs", required=True, nargs="+", type=Path, help="输入音频文件（可多个）")
    parser.add_argument("--crossfade", type=float, default=0, help="交叉淡入淡出时长（秒，0 表示不交叉）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    parser.add_argument("--format", help="输出格式（如 mp3, wav, flac）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if len(args.inputs) < 2:
        print("错误: 至少需要 2 个输入文件", file=sys.stderr)
        sys.exit(1)

    input_paths = [validate_input_file(p) for p in args.inputs]
    suffix = f".{args.format}" if args.format else input_paths[0].suffix
    output_path = args.output or build_output_path("audio_concat", input_paths[0], suffix=suffix)

    with timer() as t:
        if args.crossfade > 0:
            # Crossfade mode: use filter_complex with acrossfade for pairs
            # Build chain of acrossfade filters
            inputs = []
            for p in input_paths:
                inputs.extend(["-i", str(p)])

            filter_parts = []
            n = len(input_paths)
            for i in range(n - 1):
                if i == 0:
                    filter_parts.append(f"[0:a][1:a]acrossfade=d={args.crossfade}:c1=tri:c2=tri[af{i}]")
                else:
                    filter_parts.append(f"[af{i-1}][{i+1}:a]acrossfade=d={args.crossfade}:c1=tri:c2=tri[af{i}]")

            filter_complex = ";".join(filter_parts)
            last_label = f"[af{n-2}]"

            cmd = [
                "ffmpeg", "-y",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", last_label,
                "-c:a", "aac" if suffix == ".mp3" or suffix == ".m4a" else "copy",
                str(output_path),
            ]
            run_ffmpeg(cmd)
        else:
            # Simple concat using demuxer
            list_file = None
            try:
                list_file = tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False, encoding="utf-8",
                )
                for p in input_paths:
                    list_file.write(f"file '{forward_slash(p)}'\n")
                list_file.close()

                cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0", "-i", list_file.name,
                    "-c:a", "copy" if not args.format else "aac" if args.format == "mp3" else "copy",
                    str(output_path),
                ]
                run_ffmpeg(cmd)
            finally:
                if list_file:
                    Path(list_file.name).unlink(missing_ok=True)

    emit_result(
        type="audio",
        operation="concat",
        local_path=output_path,
        input_path=[str(p) for p in input_paths],
        input_count=len(input_paths),
        crossfade=args.crossfade,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
