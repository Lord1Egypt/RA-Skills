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

POSITIONS = {
    "top-left": "10:10",
    "top-right": "main_w-overlay_w-10:10",
    "bottom-left": "10:main_h-overlay_h-10",
    "bottom-right": "main_w-overlay_w-10:main_h-overlay_h-10",
    "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="画中画（将一个视频叠加到另一个视频上）")
    parser.add_argument("--main", required=True, type=Path, help="主视频路径")
    parser.add_argument("--overlay", required=True, type=Path, help="叠加视频路径")
    parser.add_argument("--position", default="bottom-right", choices=list(POSITIONS.keys()), help="叠加位置")
    parser.add_argument("--overlay-scale", type=float, default=0.25, help="叠加视频缩放比例（相对于主视频宽度，默认 0.25）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    main_path = validate_video_file(args.main)
    overlay_path = validate_video_file(args.overlay)
    main_probe = run_ffprobe(main_path)
    output_path = args.output or build_output_path("pip", main_path)

    pos = POSITIONS[args.position]
    overlay_w = int(main_probe.width * args.overlay_scale) if main_probe.width else 320

    filter_complex = (
        f"[1:v]scale={overlay_w}:-2[ov];"
        f"[0:v][ov]overlay={pos}"
    )

    with timer() as t:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(main_path), "-i", str(overlay_path),
            "-filter_complex", filter_complex,
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest",
            str(output_path),
        ]
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="pip",
        local_path=output_path,
        input_paths=[str(main_path), str(overlay_path)],
        position=args.position,
        overlay_scale=args.overlay_scale,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
