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
    forward_slash,
    run_ffmpeg,
    run_ffprobe,
    timer,
    validate_input_file,
)

POSITIONS = {
    "top-left": "x=10:y=10",
    "top-right": "x=W-w-10:y=10",
    "bottom-left": "x=10:y=H-h-10",
    "bottom-right": "x=W-w-10:y=H-h-10",
    "center": "x=(W-w)/2:y=(H-h)/2",
}

POSITIONS_OVERLAY = {
    "top-left": "10:10",
    "top-right": "W-w-10:10",
    "bottom-left": "10:H-h-10",
    "bottom-right": "W-w-10:H-h-10",
    "center": "(W-w)/2:(H-h)/2",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="添加水印（图片或文字）到视频")
    parser.add_argument("--input", required=True, type=Path, help="输入视频路径")
    parser.add_argument("--watermark", type=Path, help="水印图片路径")
    parser.add_argument("--text", help="水印文字")
    parser.add_argument("--position", default="bottom-right", choices=list(POSITIONS.keys()), help="水印位置")
    parser.add_argument("--opacity", type=float, default=1.0, help="水印透明度（0.0-1.0，默认 1.0）")
    parser.add_argument("--font-size", type=int, default=24, help="文字水印字体大小（默认 24）")
    parser.add_argument("--font-color", default="white", help="文字水印颜色（默认 white）")
    parser.add_argument("--tiled", action="store_true", help="平铺水印")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = validate_input_file(args.input)
    output_path = args.output or build_output_path("watermark", input_path)

    if not args.watermark and not args.text:
        print("错误: 必须指定 --watermark 或 --text", file=sys.stderr)
        sys.exit(1)

    pos = POSITIONS[args.position]

    with timer() as t:
        if args.watermark:
            wm_path = validate_input_file(args.watermark)

            if args.tiled:
                # Tiled watermark
                if args.opacity < 1.0:
                    vf = (
                        f"split[s0][s1];[s0]scale=iw:ih,boxblur=20:20[bg];"
                        f"[s1]scale=iw/4:-1[wm];"
                        f"[bg][wm]overlay=0:0,tile=4x4:margin=20:padding=10"
                    )
                else:
                    vf = (
                        f"split[s0][s1];[s1]scale=iw/4:-1[wm];"
                        f"[s0][wm]overlay=0:0,tile=4x4:margin=20:padding=10"
                    )
                # Simplified tiled approach
                vf = f"movie={forward_slash(wm_path)},scale=iw/4:-1[wm];[0:v][wm]overlay=0:0"
            else:
                overlay_pos = POSITIONS_OVERLAY[args.position]
                if args.opacity < 1.0:
                    vf = (
                        f"movie={forward_slash(wm_path)},format=rgba,colorchannelmixer=aa={args.opacity}[wm];"
                        f"[0:v][wm]overlay={overlay_pos}"
                    )
                else:
                    vf = f"movie={forward_slash(wm_path)}[wm];[0:v][wm]overlay={overlay_pos}"

            cmd = [
                "ffmpeg", "-y", "-i", str(input_path),
                "-vf", vf,
                "-c:v", "libx264", "-c:a", "copy",
                str(output_path),
            ]
        else:
            # Text watermark — escape colons in text for FFmpeg filter parser
            escape_text = args.text.replace("'", "'\\''")
            fontfile = "C\\\\:/Windows/Fonts/arial.ttf"
            vf = f"drawtext=fontfile={fontfile}:text='{escape_text}':fontsize={args.font_size}:fontcolor={args.font_color}:{pos}"

            if args.opacity < 1.0:
                vf += f":alpha='{args.opacity}'"

            cmd = [
                "ffmpeg", "-y", "-i", str(input_path),
                "-vf", vf,
                "-c:v", "libx264", "-c:a", "copy",
                str(output_path),
            ]

        run_ffmpeg(cmd)

    emit_result(
        type="video",
        operation="watermark",
        local_path=output_path,
        input_path=input_path,
        watermark_type="image" if args.watermark else "text",
        position=args.position,
        opacity=args.opacity,
        elapsed=t(),
    )


if __name__ == "__main__":
    main()
