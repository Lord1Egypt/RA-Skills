# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    RESOLUTION_MAP,
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频压缩和缩放")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--resolution", help="目标分辨率（如 720p, 1080p, 480p）")
    parser.add_argument("--width", type=int, help="目标宽度（像素，自动保持宽高比）")
    parser.add_argument("--height", type=int, help="目标高度（像素，自动保持宽高比）")
    parser.add_argument("--crf", type=int, default=23, help="视频质量 CRF（0-51，默认 23）")
    parser.add_argument("--max-bitrate", help="最大码率（如 1M, 500K）")
    parser.add_argument("--framerate", type=float, help="目标帧率")
    parser.add_argument("--preset", default="medium", choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], help="编码速度预设（默认 medium）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    output_path = args.output or build_output_path("compress_scale", input_path)

    # Determine target dimensions
    if args.resolution:
        height = RESOLUTION_MAP.get(args.resolution)
        if not height:
            from common import RESOLUTION_MAP as rm
            print(f"错误: 不支持的分辨率 '{args.resolution}'，支持: {list(RESOLUTION_MAP.keys())}", file=sys.stderr)
            sys.exit(1)
        scale_filter = f"scale=-2:{height}"
    elif args.width:
        scale_filter = f"scale={args.width}:-2"
    elif args.height:
        scale_filter = f"scale=-2:{args.height}"
    else:
        scale_filter = None

    with timer() as t:
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        vf_parts = []
        if scale_filter:
            vf_parts.append(scale_filter)

        if vf_parts:
            cmd.extend(["-vf", ",".join(vf_parts)])

        if args.framerate:
            cmd.extend(["-r", str(args.framerate)])

        cmd.extend([
            "-c:v", "libx264",
            "-preset", args.preset,
            "-crf", str(args.crf),
        ])

        if args.max_bitrate:
            cmd.extend(["-maxrate", args.max_bitrate, "-bufsize", "2*"])

        cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    output_probe = run_ffprobe(output_path)

    emit_result(
        type="video",
        operation="compress_scale",
        local_path=output_path,
        input_path=input_path,
        input_size=probe.size,
        output_size=output_probe.size,
        compression_ratio=f"{output_probe.size / probe.size:.2%}" if probe.size > 0 else "N/A",
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
