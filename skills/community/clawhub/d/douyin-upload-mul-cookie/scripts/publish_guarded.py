#!/usr/bin/env python3
import argparse
import subprocess
import sys


from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLISH_SCRIPT = SCRIPT_DIR / "publish.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guarded local Douyin publish entry.")
    parser.add_argument("-v", "--video", required=True, help="Path to the video file.")
    parser.add_argument("-t", "--title", required=True, help="Douyin title.")
    parser.add_argument("-g", "--tags", default="", help="Comma-separated tags.")
    parser.add_argument("-c", "--cover", default=None, help="Optional cover image path.")
    parser.add_argument("-s", "--schedule", default=None, help="Optional schedule time, format: YYYY-MM-DD HH:MM")
    parser.add_argument("--cookie-name", default="", help="Optional cookie profile name.")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode.")
    return parser.parse_args()


def build_publish_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(PUBLISH_SCRIPT),
        "--video",
        args.video,
        "--title",
        args.title,
    ]
    if args.tags:
        command.extend(["--tags", args.tags])
    if args.cover:
        command.extend(["--cover", args.cover])
    if args.schedule:
        command.extend(["--schedule", args.schedule])
    if args.cookie_name:
        command.extend(["--cookie-name", args.cookie_name])
    if args.headless:
        command.append("--headless")
    return command


def main() -> int:
    args = parse_args()

    command = build_publish_command(args)
    try:
        result = subprocess.run(command, check=False)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to start local publish: {exc}", file=sys.stderr)
        return 1
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
