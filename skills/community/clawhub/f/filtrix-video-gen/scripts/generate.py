#!/usr/bin/env python3
"""
Filtrix MCP video generator.

Supports both:
- text-to-video (`generate_video_text`)
- image-to-video (`generate_video_image`)

Optionally polls `get_video_status` until completion and downloads output.
"""

import argparse
import base64
import json
import mimetypes
import sys
import time
import uuid
from pathlib import Path

from mcp_client import (
    McpClient,
    build_output_path,
    download_binary,
    extract_error_message,
    extract_request_id,
    extract_status,
    extract_video_url,
    get_mcp_env,
    is_failure_status,
    is_success_status,
)

VIDEO_MODES = ("text-to-video", "grok-imagine", "seedance-1-5-pro")


def file_to_base64(path: Path) -> tuple[str, str]:
    if not path.exists() or not path.is_file():
        raise RuntimeError(f"Image file not found: {path}")

    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    if not mime.startswith("image/"):
        raise RuntimeError(f"Unsupported mime type for image file: {mime}")

    data = path.read_bytes()
    if not data:
        raise RuntimeError(f"Image file is empty: {path}")

    encoded = base64.b64encode(data).decode("ascii")
    return encoded, mime


def validate_mode_args(args: argparse.Namespace) -> None:
    if args.mode == "text-to-video":
        if args.image_url or args.image_path:
            raise RuntimeError("--image-url/--image-path only apply to image-to-video modes")
        if args.duration_seconds is not None:
            raise RuntimeError("--duration-seconds only applies to image-to-video modes")
        return

    has_url = bool(args.image_url)
    has_path = bool(args.image_path)
    if has_url == has_path:
        raise RuntimeError("image-to-video mode requires exactly one of --image-url or --image-path")

    if args.mode == "grok-imagine":
        if args.duration_seconds is None:
            raise RuntimeError("grok-imagine requires --duration-seconds (6 or 15)")
        if args.duration_seconds not in (6, 15):
            raise RuntimeError("grok-imagine --duration-seconds must be 6 or 15")
    else:
        if args.duration_seconds is None:
            raise RuntimeError("seedance-1-5-pro requires --duration-seconds (5/8/10/12)")
        if args.duration_seconds not in (5, 8, 10, 12):
            raise RuntimeError("seedance-1-5-pro --duration-seconds must be 5, 8, 10, or 12")


def build_submit_args(args: argparse.Namespace, request_key: str) -> tuple[str, dict]:
    if args.mode == "text-to-video":
        return "generate_video_text", {
            "prompt": args.prompt,
            "aspect_ratio": args.aspect_ratio,
            "idempotency_key": request_key,
        }

    payload = {
        "prompt": args.prompt,
        "mode": args.mode,
        "aspect_ratio": args.aspect_ratio,
        "duration_seconds": args.duration_seconds,
        "idempotency_key": request_key,
    }

    if args.image_url:
        payload["image_url"] = args.image_url
    else:
        image_base64, image_mime_type = file_to_base64(Path(args.image_path))
        payload["image_base64"] = image_base64
        payload["image_mime_type"] = image_mime_type

    return "generate_video_image", payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate videos via Filtrix MCP")
    parser.add_argument("--prompt", required=True, help="Video generation prompt")
    parser.add_argument(
        "--mode",
        default="text-to-video",
        choices=VIDEO_MODES,
        help="Video mode: text-to-video | grok-imagine | seedance-1-5-pro",
    )
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio, e.g. 16:9, 9:16, 1:1")
    parser.add_argument("--image-url", default=None, help="Input image URL (for image-to-video)")
    parser.add_argument("--image-path", default=None, help="Input local image path (for image-to-video)")
    parser.add_argument("--duration-seconds", type=int, default=None, help="Duration for image-to-video modes")
    parser.add_argument("--idempotency-key", default=None, help="Optional idempotency key")
    parser.add_argument("--wait", action="store_true", help="Poll until a terminal status and download output")
    parser.add_argument("--poll-interval", type=int, default=8, help="Polling interval in seconds")
    parser.add_argument("--timeout", type=int, default=600, help="Polling timeout in seconds")
    parser.add_argument("--output", default=None, help="Output video path used when downloading")
    parser.add_argument("--print-json", action="store_true", help="Print raw tool payloads")
    args = parser.parse_args()

    request_key = args.idempotency_key or f"vid-{uuid.uuid4().hex}"

    try:
        validate_mode_args(args)
        endpoint, api_key = get_mcp_env()
        tool_name, tool_args = build_submit_args(args, request_key)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    client = McpClient(endpoint=endpoint, api_key=api_key)

    try:
        client.initialize()
        submit_payload = client.call_tool(tool_name, tool_args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.print_json:
        print(json.dumps(submit_payload, ensure_ascii=False, indent=2))

    if submit_payload.get("ok") is not True:
        print(f"ERROR: generation failed: {json.dumps(submit_payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    request_id = extract_request_id(submit_payload)
    if not request_id:
        print(f"ERROR: missing request_id in response: {json.dumps(submit_payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(
        f"ACCEPTED: request_id={request_id} "
        f"idempotency_key={request_key} mode={args.mode} aspect_ratio={args.aspect_ratio}"
    )

    if args.mode != "text-to-video":
        print(f"duration_seconds={args.duration_seconds}")

    if not args.wait:
        print(f"Use: python scripts/status.py --request-id {request_id}")
        return

    poll_interval = max(1, args.poll_interval)
    timeout = max(1, args.timeout)
    started = time.monotonic()
    last_status: str | None = None

    while True:
        try:
            status_payload = client.call_tool("get_video_status", {"request_id": request_id})
        except RuntimeError as exc:
            print(f"ERROR: status polling failed: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.print_json:
            print(json.dumps(status_payload, ensure_ascii=False, indent=2))

        status_text = extract_status(status_payload) or "unknown"
        if status_text != last_status:
            print(f"STATUS: {status_text}")
            last_status = status_text

        if is_success_status(status_text):
            video_url = extract_video_url(status_payload) or extract_video_url(submit_payload)
            if not video_url:
                print("OK: completed but no video_url was returned yet.")
                if not args.print_json:
                    print(json.dumps(status_payload, ensure_ascii=False))
                return

            try:
                video_bytes = download_binary(video_url)
            except RuntimeError as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                sys.exit(1)

            out_path = build_output_path(video_url, args.output, request_id=request_id)
            out_path.write_bytes(video_bytes)
            print(f"OK: {out_path} ({len(video_bytes)} bytes)")
            print(f"request_id={request_id} video_url={video_url}")
            return

        if is_failure_status(status_text):
            message = extract_error_message(status_payload) or "Video generation failed."
            print(
                f"ERROR: request_id={request_id} status={status_text} message={message}",
                file=sys.stderr,
            )
            if not args.print_json:
                print(json.dumps(status_payload, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        if time.monotonic() - started >= timeout:
            print(f"ERROR: timed out after {timeout}s waiting for request_id={request_id}", file=sys.stderr)
            sys.exit(1)

        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
