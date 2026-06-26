# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import math
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_video_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频变速（慢动作/加速）")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--speed", required=True, type=float, help="变速倍率（<1 慢放，>1 加速，如 0.5=半速, 2.0=两倍速）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def build_atempo_chain(speed: float) -> str:
    """Build chained atempo filters for speed adjustments outside 0.5-2.0 range."""
    if speed == 1.0:
        return ""
    # atempo range is 0.5 to 2.0, chain multiple for larger ranges
    filters = []
    remaining = speed
    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    filters.append(f"atempo={remaining:.4f}")
    return ",".join(filters)


def main() -> None:
    args = parse_args()
    input_path = validate_video_file(args.input)
    probe = run_ffprobe(input_path)
    output_path = args.output or build_output_path("speed", input_path)

    speed = args.speed
    if speed <= 0:
        print("错误: 变速倍率必须大于 0", file=sys.stderr)
        from common import sys
        sys.exit(1)

    # Video: setpts=1/speed * PTS (but setpts uses factor as multiplier on PTS)
    # For 2x speed: setpts=0.5*PTS, for 0.5x speed: setpts=2.0*PTS
    video_factor = 1.0 / speed
    video_filter = f"setpts={video_factor:.4f}*PTS"

    cmd = ["ffmpeg", "-y", "-i", str(input_path), "-vf", video_filter]

    if probe.has_audio:
        audio_filter = build_atempo_chain(speed)
        cmd.extend(["-af", audio_filter])

    cmd.extend(["-c:v", "libx264", "-c:a", "aac"])
    cmd.append(str(output_path))

    with timer() as t:
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="speed",
        local_path=output_path,
        input_path=input_path,
        speed=speed,
        original_duration=probe.duration,
        new_duration=probe.duration / speed,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
