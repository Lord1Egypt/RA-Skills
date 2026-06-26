#!/usr/bin/env python3
"""
Filtrix MCP video status checker.
"""

import argparse
import json
import sys

from mcp_client import (
    McpClient,
    build_output_path,
    download_binary,
    extract_error_message,
    extract_status,
    extract_video_url,
    get_mcp_env,
    is_failure_status,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Filtrix video status via MCP")
    parser.add_argument("--request-id", required=True, help="Video request ID")
    parser.add_argument("--download", action="store_true", help="Download video if URL is available")
    parser.add_argument("--output", default=None, help="Output path (implies download)")
    parser.add_argument("--print-json", action="store_true", help="Print raw tool payload")
    args = parser.parse_args()

    try:
        endpoint, api_key = get_mcp_env()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    client = McpClient(endpoint=endpoint, api_key=api_key)

    try:
        client.initialize()
        payload = client.call_tool("get_video_status", {"request_id": args.request_id})
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.print_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    status_text = extract_status(payload) or "unknown"
    print(f"STATUS: request_id={args.request_id} status={status_text}")

    video_url = extract_video_url(payload)
    if video_url:
        print(f"VIDEO_URL: {video_url}")

    must_download = args.download or bool(args.output)
    if must_download:
        if not video_url:
            print("ERROR: no downloadable video_url in status payload", file=sys.stderr)
            sys.exit(1)

        try:
            data = download_binary(video_url)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        out_path = build_output_path(video_url, args.output, request_id=args.request_id)
        out_path.write_bytes(data)
        print(f"OK: {out_path} ({len(data)} bytes)")

    if is_failure_status(status_text):
        message = extract_error_message(payload) or "Video generation failed."
        print(f"ERROR: status indicates failure: {message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
