#!/usr/bin/env python3
"""Cross-platform health check for the Sparki Business API skill."""

from __future__ import annotations

import argparse
import os
import platform
import sys

from sparki_video_editor import (
    SUPPORT_EMAIL,
    SparkiError,
    ensure_output_dir,
    load_config,
    verify_api_connectivity,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate configuration and API connectivity.")
    parser.add_argument(
        "--config-file",
        default=None,
        help="Optional path to a sparki.env file. Environment variables take precedence.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    errors = 0

    print("=== Sparki Business API Health Check ===")
    print("")
    print("[Environment]")
    print(f"  OK  Python {platform.python_version()} ({sys.executable})")
    print(f"  OK  Platform {platform.system()} {platform.release()}")

    print("")
    print("[Configuration]")
    try:
        config = load_config(args.config_file)
        source = "environment"
        if "SPARKI_API_KEY" not in os.environ and config.config_file.exists():
            source = str(config.config_file)
        print(f"  OK  API key configured via {source}")
        print(f"  OK  API URL {config.api_url}")
        ensure_output_dir(config.output_dir)
        print(f"  OK  Output directory ready: {config.output_dir}")
    except SparkiError as exc:
        print(f"  FAIL {exc}")
        print(f"  FAIL If the issue persists, send details to {SUPPORT_EMAIL}.")
        return 1

    print("")
    print("[API Connectivity]")
    try:
        verify_api_connectivity(config)
        print(f"  OK  Business API reachable and key valid ({config.api_url})")
    except SparkiError as exc:
        print(f"  FAIL {exc}")
        errors += 1

    print("")
    if errors == 0:
        print("=== All checks passed ===")
        return 0

    print(f"=== {errors} check(s) failed ===")
    print(f"If the issue persists, send details to {SUPPORT_EMAIL}.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
