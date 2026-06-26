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
    format_size,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)

FILE_SIZE_WARNING = 500 * 1024 * 1024  # 500MB


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频倒放")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    parser.add_argument("--force", action="store_true", help="跳过大文件警告")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    output_path = args.output or build_output_path("reverse", input_path)

    file_size = input_path.stat().st_size
    if file_size > FILE_SIZE_WARNING and not args.force:
        print(
            f"警告: 文件较大 ({format_size(file_size)})，倒放需要全量缓冲到内存。\n"
            f"使用 --force 跳过此警告。",
            file=sys.stderr,
        )
        sys.exit(1)

    with timer() as t:
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        vf = "reverse"
        af = "areverse" if probe.has_audio else None

        cmd.extend(["-vf", vf])
        if af:
            cmd.extend(["-af", af])

        cmd.extend(["-c:v", "libx264", "-c:a", "aac"])
        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="reverse",
        local_path=output_path,
        input_path=input_path,
        duration=probe.duration,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
