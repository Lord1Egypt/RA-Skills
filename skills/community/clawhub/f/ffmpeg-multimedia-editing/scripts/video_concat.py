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
    validate_video_file,
    timer,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="拼接多个视频文件")
    parser.add_argument("--inputs", required=True, nargs="+", type=Path, help="输入视频文件（可多个）")
    parser.add_argument("--reencode", action="store_true", help="强制重新编码（处理不同分辨率/编码格式的情况）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if len(args.inputs) < 2:
        print("错误: 至少需要 2 个输入文件", file=sys.stderr)
        sys.exit(1)

    input_paths = [validate_video_file(p) for p in args.inputs]
    suffix = input_paths[0].suffix
    output_path = args.output or build_output_path("concat", input_paths[0], suffix=suffix)

    # Write concat list to temp file
    list_file = None
    try:
        list_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8",
        )
        for p in input_paths:
            list_file.write(f"file '{forward_slash(p)}'\n")
        list_file.close()

        with timer() as t:
            if args.reencode:
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0", "-i", list_file.name,
                    "-c:v", "libx264", "-c:a", "aac",
                    str(output_path),
                ]
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0", "-i", list_file.name,
                    "-c", "copy",
                    str(output_path),
                ]
            run_ffmpeg(cmd)
    finally:
        if list_file:
            Path(list_file.name).unlink(missing_ok=True)

    emit_result(
        type="video",
        operation="concat",
        local_path=output_path,
        input_paths=[str(p) for p in input_paths],
        input_count=len(input_paths),
        reencoded=args.reencode,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
