# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)

ROTATION_MAP = {
    "90": "transpose=1",    # 90° clockwise
    "180": "transpose=1,transpose=1",
    "270": "transpose=2",  # 90° counter-clockwise
}


def parse_crop(crop_str: str) -> list[str]:
    """Parse crop string like '1280:720:0:0' or '1280x720+0+0' into filter parts."""
    if "x" in crop_str and "+" in crop_str:
        size, offset = crop_str.split("+")
        w, h = size.split("x")
        x, y = offset.split("+")
        return [f"crop={w}:{h}:{x}:{y}"]
    return [f"crop={crop_str}"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频裁剪、旋转、翻转")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--crop", help="裁剪区域（WxH+X+Y 或 W:H:X:Y）")
    parser.add_argument("--rotate", choices=["90", "180", "270"], help="旋转角度")
    parser.add_argument("--flip", choices=["h", "v"], help="翻转方向：h=水平, v=垂直")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.crop and not args.rotate and not args.flip:
        print("错误: 必须指定 --crop、--rotate 或 --flip 中的至少一个", file=sys.stderr)
        sys.exit(1)

    input_path = validate_video_file(args.input)
    output_path = args.output or build_output_path("crop_rotate", input_path)

    filters = []

    if args.crop:
        filters.extend(parse_crop(args.crop))
    if args.rotate:
        filters.append(ROTATION_MAP[args.rotate])
    if args.flip == "h":
        filters.append("hflip")
    elif args.flip == "v":
        filters.append("vflip")

    vf = ",".join(filters)

    with timer() as t:
        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-vf", vf,
            "-c:v", "libx264", "-c:a", "copy",
            str(output_path),
        ]
        run_ffmpeg(cmd)

    operations = []
    if args.crop:
        operations.append(f"crop({args.crop})")
    if args.rotate:
        operations.append(f"rotate({args.rotate}°)")
    if args.flip:
        operations.append(f"flip({args.flip})")

    emit_result(
        type="video",
        operation="crop_rotate",
        local_path=output_path,
        input_path=input_path,
        operations=operations,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
