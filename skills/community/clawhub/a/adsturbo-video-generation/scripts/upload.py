#!/usr/bin/env python3
"""Turn a local file into a public URL.

Every other endpoint takes media as a URL, never as an upload. This module is
the bridge: hand it a local path, get back a URL to pass along.
"""

from __future__ import annotations

import argparse

from shared.client import run_cli

UPLOAD_FILE = "/openapi/v1/storage/upload/once"
UPLOAD_IMAGE = "/openapi/v1/storage/upload/once/pic"
UPLOAD_AUDIO = "/openapi/v1/storage/upload/onceaudio/notrans"


def cmd_file(client, args) -> dict:
    return client.upload(UPLOAD_FILE, args.path)


def cmd_image(client, args) -> dict:
    return client.upload(UPLOAD_IMAGE, args.path)


def cmd_audio(client, args) -> dict:
    """Audio is stored as-is, no transcoding."""
    return client.upload(UPLOAD_AUDIO, args.path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo media upload")
    sub = parser.add_subparsers(dest="command")

    for name, help_text in (
        ("file", "upload any file (video, document, ...)"),
        ("image", "upload an image"),
        ("audio", "upload audio without transcoding"),
    ):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("path", help="local file path")

    return parser


HANDLERS = {
    "file": cmd_file,
    "image": cmd_image,
    "audio": cmd_audio,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
