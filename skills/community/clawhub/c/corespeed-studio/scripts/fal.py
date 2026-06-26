#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fal-client>=0.5.0",
# ]
# ///
"""
Unified fal.ai client for image, video, audio generation and utilities.

Requires FAL_KEY environment variable (get one at https://fal.ai/dashboard/keys).

Usage:
    uv run fal.py ENDPOINT [--json '{"prompt":"..."}'] -f out.png [-i input.png]

Example:
    FAL_KEY=xxx uv run fal.py fal-ai/flux/schnell --json '{"prompt":"a fox"}' -f fox.png
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


# ---------------------------------------------------------------------------
# Input key mapping
# ---------------------------------------------------------------------------
START_IMAGE_ENDPOINTS = {"fal-ai/kling-video"}
VIDEO_INPUT_ENDPOINTS = {"fal-ai/topaz/upscale/video", "fal-ai/sync-lipsync"}


def get_input_key(endpoint: str, count: int) -> str:
    for prefix in VIDEO_INPUT_ENDPOINTS:
        if endpoint.startswith(prefix):
            return "video_url"
    for prefix in START_IMAGE_ENDPOINTS:
        if endpoint.startswith(prefix):
            return "start_image_url"
    if count > 1:
        return "image_urls"
    return "image_url"


def extract_output_url(result: dict) -> str | None:
    """Try common fal output keys: images[], image{}, video{}, audio{}, output{}."""
    images = result.get("images")
    if isinstance(images, list) and images:
        return images[0].get("url")
    for key in ("image", "video", "audio", "output"):
        obj = result.get(key)
        if isinstance(obj, dict) and "url" in obj:
            return obj["url"]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Unified fal.ai client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("endpoint", help="fal.ai endpoint (e.g. fal-ai/nano-banana-2)")
    parser.add_argument("--json", "-j", default="{}", dest="json_args",
                        help='Model parameters as JSON (e.g. \'{"prompt":"..."}\')')
    parser.add_argument("--filename", "-f", required=True, help="Output filename")
    parser.add_argument("--input", "-i", action="append", dest="inputs", metavar="FILE",
                        help="Input file(s) to upload. Repeat for multiple.")
    parser.add_argument("--audio", default="", help="Audio input file (for lipsync)")

    args = parser.parse_args()

    if not os.environ.get("FAL_KEY"):
        print("Error: FAL_KEY environment variable is required. Get one at https://fal.ai/dashboard/keys", file=sys.stderr)
        sys.exit(1)

    import fal_client

    endpoint = args.endpoint
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Parse JSON args
    try:
        request_args: dict = json.loads(args.json_args)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Upload input files
    if args.inputs:
        uploaded = []
        for fpath in args.inputs:
            if fpath.startswith("http"):
                uploaded.append(fpath)
                print(f"Using URL: {fpath}")
            else:
                url = fal_client.upload_file(fpath)
                uploaded.append(url)
                print(f"Uploaded: {fpath} → {url}")

        key = get_input_key(endpoint, len(uploaded))
        if key == "image_urls":
            request_args[key] = uploaded
        else:
            request_args[key] = uploaded[0]

    # Upload audio input
    if args.audio:
        if args.audio.startswith("http"):
            request_args["audio_url"] = args.audio
        else:
            audio_url = fal_client.upload_file(args.audio)
            print(f"Uploaded audio: {args.audio} → {audio_url}")
            request_args["audio_url"] = audio_url

    print(f"Calling {endpoint}...")
    print(f"Args: {json.dumps(request_args, ensure_ascii=False)[:200]}")

    try:
        result = fal_client.subscribe(
            endpoint,
            arguments=request_args,
            with_logs=True,
            on_queue_update=lambda update: (
                print(f"Queue: {update.status}") if hasattr(update, "status") else None
            ),
        )

        # Save output
        output_url = extract_output_url(result)
        if not output_url:
            print(f"Error: Cannot find output URL. Keys: {list(result.keys())}", file=sys.stderr)
            print(f"Response: {json.dumps(result, default=str)[:500]}", file=sys.stderr)
            sys.exit(1)

        urllib.request.urlretrieve(output_url, str(output_path))
        full_path = output_path.resolve()
        print(f"\nSaved: {full_path}")
        print(f"MEDIA: {full_path}")

        # Print extra images if present
        images = result.get("images", [])
        for idx, img in enumerate(images[1:], start=2):
            extra_path = output_path.parent / f"{output_path.stem}-{idx}{output_path.suffix}"
            img_url = img.get("url", "")
            if img_url:
                urllib.request.urlretrieve(img_url, str(extra_path))
                efp = extra_path.resolve()
                print(f"Saved: {efp}")
                print(f"MEDIA: {efp}")

        # Print metadata
        if result.get("description"):
            print(f"\nModel: {result['description']}")
        if result.get("duration_ms"):
            print(f"Duration: {result['duration_ms']}ms")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
