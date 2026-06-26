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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="音频音量调节（音量、标准化、淡入淡出）")
    parser.add_argument("--input", required=True, type=Path, help="输入文件路径（音频或视频）")
    parser.add_argument("--volume", type=float, help="音量倍率（如 1.5=增大50%%，0.5=减小50%%）")
    parser.add_argument("--normalize", action="store_true", help="响度标准化（EBU R128 标准）")
    parser.add_argument("--fade-in", type=float, help="淡入时长（秒）")
    parser.add_argument("--fade-out", type=float, help="淡出时长（秒）")
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

    output_path = args.output or build_output_path("audio_volume", input_path, suffix=input_path.suffix)

    af_parts = []

    if args.normalize:
        # EBU R128 loudness normalization
        af_parts.append("loudnorm=I=-16:TP=-1.5:LRA=11")

    if args.volume is not None and args.volume != 1.0:
        af_parts.append(f"volume={args.volume}")

    if args.fade_in is not None and args.fade_in > 0:
        af_parts.append(f"afade=t=in:st=0:d={args.fade_in}")

    if args.fade_out is not None and args.fade_out > 0:
        st = max(0, probe.duration - args.fade_out)
        af_parts.append(f"afade=t=out:st={st}:d={args.fade_out}")

    with timer() as t:
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        if af_parts:
            cmd.extend(["-af", ",".join(af_parts)])

        if probe.has_video:
            cmd.extend(["-c:v", "copy", "-c:a", "aac"])
        else:
            cmd.extend(["-c:a", "aac"])

        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    emit_result(
        type="audio" if not probe.has_video else "video",
        operation="volume",
        local_path=output_path,
        input_path=input_path,
        volume=args.volume,
        normalized=args.normalize,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
