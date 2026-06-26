#!/usr/bin/env python3
"""Cross-platform Sparki video editing entrypoint."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sparki_video_editor import (
    SUPPORT_EMAIL,
    SparkiError,
    create_render_project,
    download_file,
    ensure_output_dir,
    format_file_size,
    get_asset_status,
    get_project_status,
    get_result_url,
    load_config,
    upload_asset,
    validate_inputs,
    validate_video_path,
    wait_for_terminal_status,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload an MP4, create a render project, poll with exponential backoff, and download the final MP4."
    )
    parser.add_argument("video_path", help="Local MP4 file path")
    parser.add_argument("tips", nargs="?", default="", help="Tip ID or comma-separated tips")
    parser.add_argument("user_prompt", nargs="?", default="", help="Free-text prompt")
    parser.add_argument("aspect_ratio", nargs="?", default="9:16", help="Output aspect ratio")
    parser.add_argument("duration", nargs="?", default="", help="Target output duration in seconds")
    parser.add_argument(
        "--config-file",
        default=None,
        help="Optional path to a sparki.env file. Environment variables take precedence.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        config = load_config(args.config_file)
        video_path = validate_video_path(Path(args.video_path).expanduser())
        validate_inputs(args.tips, args.user_prompt, args.duration)
        ensure_output_dir(config.output_dir)

        print("=== Sparki AI Video Editor ===")
        print(f"Video: {video_path}")
        print(f"Tips: {args.tips or '<empty>'}")
        print(f"Prompt: {args.user_prompt or '<empty>'}")
        print(f"Aspect Ratio: {args.aspect_ratio}")
        print(f"Duration: {args.duration or '<empty>'}")
        print(f"API: {config.api_url}")
        print("")

        print("[1/4] Uploading asset...")
        object_key = upload_asset(config, video_path)
        print(f"  Uploaded object_key: {object_key}")

        print("[2/4] Waiting for asset processing...")
        wait_for_terminal_status(
            lambda: get_asset_status(config, object_key),
            timeout_seconds=config.asset_timeout,
            initial_interval=config.asset_poll_interval,
            max_interval=config.asset_poll_max_interval,
            label="Asset",
        )

        print("[3/4] Creating render project...")
        project_id = create_render_project(
            config,
            object_key,
            args.tips,
            args.user_prompt,
            args.aspect_ratio,
            args.duration,
        )
        print(f"  Project ID: {project_id}")

        print("[4/4] Waiting for render completion...")
        project_response = wait_for_terminal_status(
            lambda: get_project_status(config, project_id),
            timeout_seconds=config.project_timeout,
            initial_interval=config.project_poll_interval,
            max_interval=config.project_poll_max_interval,
            label="Project",
        )

        result_url = get_result_url(project_response)
        output_file = config.output_dir / f"{project_id}.mp4"
        download_file(result_url, output_file)

        print("")
        print("=== Done! ===")
        print(f"Output: {output_file} ({format_file_size(output_file)})")
        return 0
    except SparkiError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            f"If the issue persists, send details to {SUPPORT_EMAIL}.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
