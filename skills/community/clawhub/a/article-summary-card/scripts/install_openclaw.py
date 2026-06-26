#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def ignore_filter(directory, names):
    ignored = set()
    for name in names:
        if name in {"__pycache__", ".DS_Store"}:
            ignored.add(name)
    return ignored


def main():
    parser = argparse.ArgumentParser(description="Install the article-summary-card skill into an OpenClaw workspace.")
    parser.add_argument(
        "--dest",
        default="~/.openclaw/workspace/skills/article-summary-card",
        help="Destination skill directory in the OpenClaw workspace.",
    )
    args = parser.parse_args()

    source = Path(__file__).resolve().parent.parent
    dest = Path(args.dest).expanduser().resolve()

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(source, dest, ignore=ignore_filter)
    print(dest)


if __name__ == "__main__":
    main()
