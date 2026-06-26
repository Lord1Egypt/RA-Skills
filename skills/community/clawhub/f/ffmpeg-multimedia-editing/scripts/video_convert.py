# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    FORMAT_TO_EXT,
    build_output_path,
    emit_result,
    run_ffmpeg,
    timer,
    validate_input_file,
)

PRESETS = {
    "web-optimized": {"vcodec": "libx264", "acodec": "aac", "pix_fmt": "yuv420p"},
    "h265": {"vcodec": "libx265", "acodec": "aac"},
    "lossless": {"vcodec": "libx264", "acodec": "flac", "crf": "0"},
    "webm-vp9": {"vcodec": "libvpx-vp9", "acodec": "libopus"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频格式转换")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--format", help="目标格式（如 webm, mkv, avi）")
    parser.add_argument("--video-codec", help="视频编码器（如 libx264, libx265, libvpx-vp9）")
    parser.add_argument("--audio-codec", help="音频编码器（如 aac, libopus, flac）")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="使用预设配置")
    parser.add_argument("--crf", type=int, help="视频质量（0-51，越小质量越高）")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)
    output_path = args.output

    preset = PRESETS.get(args.preset, {}) if args.preset else {}

    target_format = args.format or (None if not args.preset else None)
    vcodec = args.video_codec or preset.get("vcodec")
    acodec = args.audio_codec or preset.get("acodec")
    crf = args.crf or preset.get("crf")

    # Auto-override codec when it's incompatible with the target container
    if target_format == "webm":
        if not args.video_codec and vcodec not in ("libvpx", "libvpx-vp9", "libaom-av1"):
            vcodec = "libvpx-vp9"
        if not args.audio_codec and acodec not in ("libopus", "libvorbis"):
            acodec = "libopus"
    elif target_format == "avi":
        if not vcodec:
            vcodec = "libx264"
        if not acodec:
            acodec = "mp3lame"

    if not output_path:
        suffix = FORMAT_TO_EXT.get(target_format, ".mp4") if target_format else ".mp4"
        output_path = build_output_path("convert", input_path, suffix=suffix)

    with timer() as t:
        cmd = ["ffmpeg", "-y", "-i", str(input_path)]

        if vcodec:
            cmd.extend(["-c:v", vcodec])
            if crf is not None and vcodec in ("libx264", "libx265", "libvpx-vp9"):
                cmd.extend(["-crf", str(crf)])
        else:
            cmd.extend(["-c:v", "copy"])

        if acodec:
            cmd.extend(["-c:a", acodec])
        else:
            cmd.extend(["-c:a", "copy"])

        if preset.get("pix_fmt"):
            cmd.extend(["-pix_fmt", preset["pix_fmt"]])

        cmd.append(str(output_path))
        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="convert",
        local_path=output_path,
        input_path=input_path,
        format=target_format,
        video_codec=vcodec,
        audio_codec=acodec,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
