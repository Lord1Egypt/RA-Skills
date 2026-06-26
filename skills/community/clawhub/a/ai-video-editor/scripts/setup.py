#!/usr/bin/env python3
"""Cross-platform setup helper for the Sparki Business API skill."""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path

from sparki_video_editor import (
    DEFAULT_API_URL,
    DEFAULT_CONFIG_FILE,
    DEFAULT_OUTPUT_DIR,
    SUPPORT_EMAIL,
    SparkiError,
    ensure_output_dir,
    load_config,
    verify_api_connectivity,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create or validate sparki.env.")
    parser.add_argument(
        "--config-file",
        default=str(DEFAULT_CONFIG_FILE),
        help="Path to the sparki.env file to create or validate.",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Write SPARKI_API_KEY into the config file before validation.",
    )
    return parser


def write_default_config(config_path: Path, api_key: str) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(
        [
            "# Sparki Business API configuration",
            f"SPARKI_API_KEY={api_key}",
            f"SPARKI_API_URL={DEFAULT_API_URL}",
            f"SPARKI_OUTPUT_DIR={DEFAULT_OUTPUT_DIR}",
            "",
        ]
    )
    config_path.write_text(content, encoding="utf-8")
    if os.name != "nt":
        config_path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def main() -> int:
    args = build_parser().parse_args()
    config_path = Path(args.config_file).expanduser()

    try:
        if not config_path.exists():
            write_default_config(config_path, args.api_key)
            print(f"Created {config_path}")
            if not args.api_key:
                print("Fill in SPARKI_API_KEY, then run python scripts/health.py")
                return 0

        config = load_config(str(config_path))
        verify_api_connectivity(config)
        ensure_output_dir(config.output_dir)
        print(f"API key verification passed against {config.api_url}")
        print(f"Output directory ready: {config.output_dir}")
        return 0
    except SparkiError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            f"If the issue persists, send details to {SUPPORT_EMAIL}.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
