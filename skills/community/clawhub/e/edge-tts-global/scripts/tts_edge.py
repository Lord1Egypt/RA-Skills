#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_VOICE = os.environ.get("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural")


def default_output_path() -> Path:
    cwd = Path.cwd()
    temp_dir = cwd / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / f"edge_tts_{time.strftime('%Y%m%d_%H%M%S')}.mp3"


def generate(text: str, out: str | None, voice: str, subs: str | None) -> int:
    out_path = Path(out) if out else default_output_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", str(out_path),
    ]
    if subs:
        subs_path = Path(subs)
        subs_path.parent.mkdir(parents=True, exist_ok=True)
        cmd += ["--write-subtitles", str(subs_path)]

    subprocess.run(cmd, check=True)
    print(str(out_path))
    return 0


def cleanup(paths: list[str]) -> int:
    for p in paths:
        if not p:
            continue
        try:
            Path(p).unlink(missing_ok=True)
        except TypeError:
            path = Path(p)
            if path.exists():
                path.unlink()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or cleanup Edge TTS temporary files")
    subparsers = parser.add_subparsers(dest="command")

    cleanup_parser = subparsers.add_parser("cleanup", help="Delete generated temporary files")
    cleanup_parser.add_argument("paths", nargs="+", help="Files to delete")

    parser.add_argument("-t", "--text", help="Text to synthesize")
    parser.add_argument("-o", "--out", help="Output audio path; default is <current workspace>/temp/edge_tts_<timestamp>.mp3")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE, help=f"Voice name (default: {DEFAULT_VOICE})")
    parser.add_argument("--subs", help="Optional subtitle output path")

    args = parser.parse_args()

    if args.command == "cleanup":
        return cleanup(args.paths)

    if not args.text:
        parser.error("the following arguments are required: -t/--text")

    return generate(args.text, args.out, args.voice, args.subs)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as e:
        print(f"edge-tts command failed: {e}", file=sys.stderr)
        raise
