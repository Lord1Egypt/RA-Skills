#!/usr/bin/env python3
"""Video editing wrapper around FFmpeg for common product video operations.

Usage:
  python video_edit.py trim input.mp4 --start 0:30 --end 2:45 -o trimmed.mp4
  python video_edit.py concat part1.mp4 part2.mp4 part3.mp4 -o combined.mp4
  python video_edit.py add-audio video.mp4 --audio narration.mp3 -o final.mp4
  python video_edit.py resize input.mp4 --width 1920 --height 1080 -o hd.mp4
  python video_edit.py info input.mp4
  python video_edit.py screenshot input.mp4 --at 0:05 -o thumb.jpg

Requires: FFmpeg (system install)
"""

import argparse
import io
import json
import os
import subprocess
import sys
import tempfile

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LANG = {
    "zh": {
        "missing_ffmpeg": "FFmpeg 未安装。请从 https://ffmpeg.org/download.html 下载安装。",
        "missing_ffprobe": "ffprobe 未找到（通常与 FFmpeg 一起安装）。",
        "processing": "处理中",
        "done": "完成",
        "error": "错误",
        "output": "输出",
        "input": "输入",
        "duration": "时长",
        "resolution": "分辨率",
        "codec": "编码",
        "bitrate": "码率",
        "not_found": "文件不存在",
    },
    "en": {
        "missing_ffmpeg": "FFmpeg not installed. Download from https://ffmpeg.org/download.html",
        "missing_ffprobe": "ffprobe not found (usually installed with FFmpeg).",
        "processing": "Processing",
        "done": "Done",
        "error": "Error",
        "output": "Output",
        "input": "Input",
        "duration": "Duration",
        "resolution": "Resolution",
        "codec": "Codec",
        "bitrate": "Bitrate",
        "not_found": "File not found",
    },
}


def run_ffmpeg(cmd, msg):
    """Run an FFmpeg command and handle errors."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            stderr = result.stderr.split("\n")[-5:] if result.stderr else ["Unknown error"]
            print(f"[✗] {msg['error']}:")
            for line in stderr:
                if line.strip():
                    print(f"    {line.strip()}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"[✗] {msg['error']}: timeout (10 min)")
        return False
    except Exception as e:
        print(f"[✗] {msg['error']}: {e}")
        return False


def cmd_trim(args, msg):
    """Trim a video segment (lossless cut)."""
    if not os.path.isfile(args.input):
        print(f"[✗] {msg['not_found']}: {args.input}")
        return 1

    output = args.output or f"{os.path.splitext(args.input)[0]}_trimmed.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-ss", args.start,
        "-i", args.input,
        "-to", args.end,
        "-c", "copy",
        output,
    ]

    print(f"[{msg['processing']}] {args.input} [{args.start} -> {args.end}] ...", end=" ", flush=True)
    if run_ffmpeg(cmd, msg):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"{msg['done']} ({size_mb:.1f} MB)")
        print(f"  {msg['output']}: {output}")
        return 0
    return 1


def cmd_concat(args, msg):
    """Concatenate multiple video files."""
    for f in args.inputs:
        if not os.path.isfile(f):
            print(f"[✗] {msg['not_found']}: {f}")
            return 1

    output = args.output or "combined.mp4"

    # Write file list for concat demuxer
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for input_file in args.inputs:
            f.write(f"file '{os.path.abspath(input_file)}'\n")
        list_path = f.name

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output,
    ]

    print(f"[{msg['processing']}] {len(args.inputs)} files -> {output} ...", end=" ", flush=True)
    success = run_ffmpeg(cmd, msg)
    os.unlink(list_path)

    if success:
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"{msg['done']} ({size_mb:.1f} MB)")
        print(f"  {msg['output']}: {output}")
        return 0
    return 1


def cmd_add_audio(args, msg):
    """Add or replace audio track in a video."""
    if not os.path.isfile(args.video):
        print(f"[✗] {msg['not_found']}: {args.video}")
        return 1
    if not os.path.isfile(args.audio):
        print(f"[✗] {msg['not_found']}: {args.audio}")
        return 1

    output = args.output or f"{os.path.splitext(args.video)[0]}_with_audio.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", args.video,
        "-i", args.audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output,
    ]

    print(f"[{msg['processing']}] {args.video} + {args.audio} ...", end=" ", flush=True)
    if run_ffmpeg(cmd, msg):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"{msg['done']} ({size_mb:.1f} MB)")
        print(f"  {msg['output']}: {output}")
        return 0
    return 1


def cmd_resize(args, msg):
    """Resize video to specified dimensions."""
    if not os.path.isfile(args.input):
        print(f"[✗] {msg['not_found']}: {args.input}")
        return 1

    output = args.output or f"{os.path.splitext(args.input)[0]}_{args.width}x{args.height}.mp4"

    vf = f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2"

    cmd = [
        "ffmpeg", "-y",
        "-i", args.input,
        "-vf", vf,
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "128k",
        output,
    ]

    print(f"[{msg['processing']}] {args.input} -> {args.width}x{args.height} ...", end=" ", flush=True)
    if run_ffmpeg(cmd, msg):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"{msg['done']} ({size_mb:.1f} MB)")
        print(f"  {msg['output']}: {output}")
        return 0
    return 1


def cmd_info(args, msg):
    """Print video metadata as JSON."""
    if not os.path.isfile(args.input):
        print(f"[✗] {msg['not_found']}: {args.input}")
        return 1

    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        args.input,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"[✗] {msg['missing_ffprobe']}")
            return 1

        data = json.loads(result.stdout)
        format_info = data.get("format", {})
        video_stream = None
        audio_stream = None
        for stream in data.get("streams", []):
            if stream["codec_type"] == "video" and not video_stream:
                video_stream = stream
            elif stream["codec_type"] == "audio" and not audio_stream:
                audio_stream = stream

        print(f"=== {args.input} ===")
        print(f"  {msg['duration']}: {float(format_info.get('duration', 0)):.1f}s")
        print(f"  {msg['bitrate']}: {int(format_info.get('bit_rate', 0)) // 1000} kbps")
        if video_stream:
            print(f"  {msg['resolution']}: {video_stream.get('width')}x{video_stream.get('height')}")
            print(f"  Video {msg['codec']}: {video_stream.get('codec_name')}")
        if audio_stream:
            print(f"  Audio {msg['codec']}: {audio_stream.get('codec_name')}")

        return 0
    except json.JSONDecodeError:
        print(f"[✗] {msg['error']}: failed to parse ffprobe output")
        return 1


def cmd_screenshot(args, msg):
    """Extract a frame as an image."""
    if not os.path.isfile(args.input):
        print(f"[✗] {msg['not_found']}: {args.input}")
        return 1

    output = args.output or f"{os.path.splitext(args.input)[0]}_thumb.jpg"

    cmd = [
        "ffmpeg", "-y",
        "-ss", args.at,
        "-i", args.input,
        "-vframes", "1",
        "-q:v", "2",
        output,
    ]

    print(f"[{msg['processing']}] {args.input} @ {args.at} ...", end=" ", flush=True)
    if run_ffmpeg(cmd, msg):
        print(f"{msg['done']}")
        print(f"  {msg['output']}: {output}")
        return 0
    return 1


def check_ffmpeg(msg):
    """Check if ffmpeg and ffprobe are available."""
    for tool in ["ffmpeg", "ffprobe"]:
        try:
            r = subprocess.run(
                [tool, "-version"], capture_output=True, text=True, timeout=10,
                shell=(sys.platform == "win32")
            )
            if r.returncode != 0:
                print(f"[✗] {msg['missing_' + tool]}")
                return False
        except Exception:
            print(f"[✗] {msg['missing_' + tool]}")
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Video editing via FFmpeg")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    # trim
    p_trim = subparsers.add_parser("trim", help="Trim video segment")
    p_trim.add_argument("input", help="Input video file")
    p_trim.add_argument("--start", "-s", required=True, help="Start time (HH:MM:SS or seconds)")
    p_trim.add_argument("--end", "-e", required=True, help="End time (HH:MM:SS or seconds)")
    p_trim.add_argument("--output", "-o", help="Output file path")
    p_trim.add_argument("--lang", default="zh", choices=["zh", "en"])

    # concat
    p_concat = subparsers.add_parser("concat", help="Concatenate multiple videos")
    p_concat.add_argument("inputs", nargs="+", help="Input video files (in order)")
    p_concat.add_argument("--output", "-o", help="Output file path")
    p_concat.add_argument("--lang", default="zh", choices=["zh", "en"])

    # add-audio
    p_audio = subparsers.add_parser("add-audio", help="Add/replace audio track")
    p_audio.add_argument("video", help="Video file")
    p_audio.add_argument("--audio", "-a", required=True, help="Audio file (mp3, aac, etc.)")
    p_audio.add_argument("--output", "-o", help="Output file path")
    p_audio.add_argument("--lang", default="zh", choices=["zh", "en"])

    # resize
    p_resize = subparsers.add_parser("resize", help="Resize video")
    p_resize.add_argument("input", help="Input video file")
    p_resize.add_argument("--width", type=int, required=True, help="Target width")
    p_resize.add_argument("--height", type=int, required=True, help="Target height")
    p_resize.add_argument("--output", "-o", help="Output file path")
    p_resize.add_argument("--lang", default="zh", choices=["zh", "en"])

    # info
    p_info = subparsers.add_parser("info", help="Show video metadata")
    p_info.add_argument("input", help="Input video file")
    p_info.add_argument("--lang", default="zh", choices=["zh", "en"])

    # screenshot
    p_shot = subparsers.add_parser("screenshot", help="Extract frame as image")
    p_shot.add_argument("input", help="Input video file")
    p_shot.add_argument("--at", required=True, help="Time position (HH:MM:SS or seconds)")
    p_shot.add_argument("--output", "-o", help="Output image path")
    p_shot.add_argument("--lang", default="zh", choices=["zh", "en"])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    msg = LANG[args.lang]

    if not check_ffmpeg(msg):
        return 1

    if args.command == "trim":
        return cmd_trim(args, msg)
    elif args.command == "concat":
        return cmd_concat(args, msg)
    elif args.command == "add-audio":
        return cmd_add_audio(args, msg)
    elif args.command == "resize":
        return cmd_resize(args, msg)
    elif args.command == "info":
        return cmd_info(args, msg)
    elif args.command == "screenshot":
        return cmd_screenshot(args, msg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
