# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import (
    FORMAT_TO_EXT,
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_input_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从视频中提取音频或替换音频")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--extract-audio", action="store_true", help="提取音频")
    group.add_argument("--replace-audio", type=Path, help="替换音频的新音频文件路径")
    parser.add_argument("--format", help="提取音频时的目标格式（如 mp3, wav, aac）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)

    with timer() as t:
        if args.extract_audio:
            probe = run_ffprobe(input_path)
            if not probe.has_audio:
                print("错误: 视频中不包含音频流", file=sys.stderr)
                sys.exit(1)

            suffix = f".{args.format}" if args.format else f".{probe.audio_codec}" if probe.audio_codec else ".aac"
            output_path = args.output or build_output_path("audio_extract", input_path, suffix=suffix)

            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-vn",
                "-c:a", "copy",
                str(output_path),
            ]
            run_ffmpeg(cmd)

            emit_result(
                type="audio",
                operation="extract",
                local_path=output_path,
                input_path=input_path,
                codec=probe.audio_codec,
                duration=probe.duration,
                elapsed=t(),
            )

        elif args.replace_audio:
            new_audio_path = validate_input_file(args.replace_audio)
            output_path = args.output or build_output_path("audio_replace", input_path)

            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-i", str(new_audio_path),
                "-c:v", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:a", "aac",
                "-shortest",
                str(output_path),
            ]
            run_ffmpeg(cmd)

            emit_result(
                type="video",
                operation="replace_audio",
                local_path=output_path,
                input_path=input_path,
                new_audio=str(new_audio_path),
                elapsed=t(),
            )


if __name__ == "__main__":
    main()
