#!/usr/bin/env python3
"""Client helper for the Calibre Converter OpenClaw skill.

This script sends a conversion request to calibre-openclaw-server. The server is
responsible for running ebook-convert, registering the new format in Calibre,
and returning the operation result.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_SERVER_URL = "http://127.0.0.1:6180"
SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_ENV_FILE = SKILL_ROOT / ".env"


def load_skill_env(env_file: Path = SKILL_ENV_FILE) -> None:
    """Load key/value pairs from the skill root .env without overriding env vars."""
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        os.environ[key] = value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Request a Calibre book format conversion through calibre-openclaw-server."
    )
    identifier = parser.add_mutually_exclusive_group(required=True)
    identifier.add_argument("--book-id", type=int, help="Internal OpenClaw/PostgreSQL book ID.")
    identifier.add_argument("--calibre-id", type=int, help="Native Calibre book ID.")
    identifier.add_argument("--title", help="Exact book title when it uniquely identifies one book.")
    parser.add_argument(
        "--target-format",
        required=True,
        help="Requested output format, for example epub, azw3, mobi, pdf, docx, txt.",
    )
    parser.add_argument(
        "--source-format",
        help="Optional preferred source format when the book has multiple formats.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reconvert and replace the target format when it already exists.",
    )
    parser.add_argument(
        "--server-url",
        default=os.environ.get("CALIBRE_OPENCLAW_SERVER_URL", DEFAULT_SERVER_URL),
        help="Base URL for calibre-openclaw-server.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("CALIBRE_OPENCLAW_API_KEY"),
        help="API key for calibre-openclaw-server. Defaults to CALIBRE_OPENCLAW_API_KEY.",
    )
    return parser


def request_conversion(args: argparse.Namespace) -> dict:
    payload = {
        "book_id": args.book_id,
        "calibre_id": args.calibre_id,
        "title": args.title,
        "target_format": args.target_format,
        "source_format": args.source_format,
        "force": args.force,
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    url = args.server_url.rstrip("/") + "/api/books/convert-format"
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    if args.api_key:
        request.add_header("Authorization", f"Bearer {args.api_key}")

    try:
        with urllib.request.urlopen(request, timeout=1200) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Server returned HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach calibre-openclaw-server: {exc}") from exc

    return json.loads(response_body)


def main() -> int:
    load_skill_env()
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = request_conversion(args)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
