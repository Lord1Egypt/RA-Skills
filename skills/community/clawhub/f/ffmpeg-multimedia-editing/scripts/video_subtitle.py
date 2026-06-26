# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from common import (
    build_output_path,
    emit_result,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_input_file,
)


def _relative_path(p: Path) -> str:
    """Return a relative path from CWD to avoid Windows drive-letter issues in FFmpeg filters."""
    try:
        rel = os.path.relpath(p)
    except ValueError:
        # Different drives on Windows — fall back to absolute with forward slashes
        rel = str(p).replace("\\", "/")
    # Replace backslashes (just in case)
    return rel.replace("\\", "/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="嵌入字幕到视频（支持软字幕和硬字幕）")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--subtitle", required=True, type=Path, help="字幕文件路径（SRT/ASS/SSA/VTT）")
    parser.add_argument("--mode", choices=["soft", "hard"], default="soft", help="字幕模式：soft=软字幕（可关闭），hard=硬字幕（烧录到画面）")
    parser.add_argument("--output", type=Path, help="输出文件路径（不指定则自动生成）")
    parser.add_argument("--style", help="硬字幕样式（如 FontSize=24,PrimaryColour=&H00FFFFFF）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)
    subtitle_path = validate_input_file(args.subtitle)
    probe = run_ffprobe(input_path)

    suffix = input_path.suffix
    output_path = args.output or build_output_path("subtitle", input_path, suffix=suffix)

    with timer() as t:
        if args.mode == "soft":
            # 软字幕：mux 字幕流到容器中
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-i", str(subtitle_path),
                "-c:v", "copy",
                "-c:a", "copy",
                "-c:s", "mov_text",
                "-map", "0:v:0", "-map", "0:a?", "-map", "1:s:0",
                str(output_path),
            ]
        else:
            # 硬字幕：烧录到画面
            sub_ext = subtitle_path.suffix.lower()
            if sub_ext == ".ass":
                filter_name = "ass"
            else:
                filter_name = "subtitles"

            filter_str = f"{filter_name}={_relative_path(subtitle_path)}"
            if args.style:
                if sub_ext == ".ass":
                    # ASS 文件的 style 由文件自身控制
                    pass
                else:
                    filter_str += f":force_style='{args.style}'"

            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-vf", filter_str,
                "-c:v", "libx264",
                "-c:a", "copy",
                str(output_path),
            ]

        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="subtitle",
        local_path=output_path,
        input_path=input_path,
        mode=args.mode,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
