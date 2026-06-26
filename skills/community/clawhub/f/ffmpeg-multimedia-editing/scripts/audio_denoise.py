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
    validate_input_file,
)

STRENGTH_MAP = {
    "light": {"noise_reduction": 15, "noise_floor": -35},
    "medium": {"noise_reduction": 25, "noise_floor": -45},
    "heavy": {"noise_reduction": 40, "noise_floor": -55},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="音频降噪")
    parser.add_argument("--input", required=True, type=Path, help="输入文件路径（音频或视频）")
    parser.add_argument("--strength", choices=["light", "medium", "heavy"], default="medium", help="降噪强度（默认 medium）")
    parser.add_argument("--noise-profile", type=Path, help="自定义噪声样本文件")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)
    probe = run_ffprobe(input_path)

    if not probe.has_audio:
        print("错误: 文件不包含音频流", file=sys.stderr)
        import sys
        sys.exit(1)

    output_path = args.output or build_output_path("audio_denoise", input_path, suffix=input_path.suffix)

    strength = STRENGTH_MAP[args.strength]

    with timer() as t:
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        if args.noise_profile:
            # Use custom noise profile with anlmdn (non-linear median denoiser)
            profile_path = validate_input_file(args.noise_profile)
            af = f"anlmdn=s={strength['noise_reduction']}"
        else:
            # Use afftdn (FFT denoiser) with default noise profile
            af = (
                f"afftdn=nr={strength['noise_reduction']}:nf={strength['noise_floor']}"
            )

        cmd.extend(["-af", af])

        if probe.has_video:
            cmd.extend(["-c:v", "copy", "-c:a", "aac"])
        else:
            cmd.extend(["-c:a", "aac"])

        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    emit_result(
        type="audio" if not probe.has_video else "video",
        operation="denoise",
        local_path=output_path,
        input_path=input_path,
        strength=args.strength,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
