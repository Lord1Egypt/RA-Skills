#!/usr/bin/env python3
"""Agnes AI - Image and Video Generation CLI.

Usage:
  python generate.py image --prompt "..." [--size 1024x1024] [--image URL1 [URL2 ...]] [--model MODEL] --output path.png
  python generate.py video --prompt "..." [--duration 5] --output path.mp4

Image models:
  agnes-image-2.1-flash  (text-to-image, high info density, DEFAULT for image)
  agnes-image-2.0-flash  (image-to-image, multi-image composition, use --image flag)
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "https://apihub.agnes-ai.com/v1"

DEFAULT_IMAGE_MODEL = "agnes-image-2.1-flash"
I2I_IMAGE_MODEL = "agnes-image-2.0-flash"
VIDEO_MODEL = "agnes-video-v2.0"


def get_api_key():
    """Retrieve API key from environment or config file.

    Checked in order:
      1. Environment variable AGNES_API_KEY
      2. File ~/.agnes-ai/api_key
      3. File api_key in the same directory as this script
    """
    key = os.environ.get("AGNES_API_KEY")
    if key:
        return key

    # User-level config
    key_file = os.path.expanduser("~/.agnes-ai/api_key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            return f.read().strip()

    # Script-adjacent config (self-contained installs)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_key = os.path.join(script_dir, "api_key")
    if os.path.exists(local_key):
        with open(local_key) as f:
            return f.read().strip()

    print("ERROR: AGNES_API_KEY not set.", file=sys.stderr)
    print("Set the environment variable or write it to one of:", file=sys.stderr)
    print("  ~/.agnes-ai/api_key", file=sys.stderr)
    print("  " + local_key, file=sys.stderr)
    sys.exit(1)


def api_request(method, endpoint, body=None, api_key=None):
    """Make an authenticated request to the Agnes AI API."""
    if api_key is None:
        api_key = get_api_key()

    url = API_BASE + endpoint

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print("API Error (" + str(e.code) + "): " + err_body, file=sys.stderr)
        sys.exit(1)


def download_file(url, output_path):
    """Download a file from URL to local path."""
    print("Downloading to " + output_path + " ...")
    urllib.request.urlretrieve(url, output_path)
    print("Saved: " + output_path)


def upload_image_as_data_url(image_path):
    """Read a local image file and return a data URL (base64-encoded)."""
    mime, _ = mimetypes.guess_type(image_path)
    if mime is None:
        # Default to png
        mime = "image/png"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return "data:" + mime + ";base64," + data


def resolve_image_to_url(image_arg, api_key):
    """Resolve an image argument to a URL string.

    - If it already starts with http(s):, treat as URL and return as-is.
    - If it is a local file path, upload as data URL.
    """
    if image_arg.startswith("http://") or image_arg.startswith("https://"):
        return image_arg
    # Local file: read and encode as data URL
    if not os.path.exists(image_arg):
        print("ERROR: Image file not found: " + image_arg, file=sys.stderr)
        sys.exit(1)
    return upload_image_as_data_url(image_arg)


def generate_image(prompt, size, output_path, image_urls=None, model=None):
    """Generate an image using Agnes AI image models.

    If image_urls is provided (non-empty), use image-to-image model (agnes-image-2.0-flash).
    Otherwise use text-to-image model (agnes-image-2.1-flash by default).
    """
    # Determine model
    if image_urls and len(image_urls) > 0:
        selected_model = model if model else I2I_IMAGE_MODEL
        print("Using model (image-to-image): " + selected_model)
    else:
        selected_model = model if model else DEFAULT_IMAGE_MODEL
        print("Using model (text-to-image): " + selected_model)

    print("Generating image: " + prompt[:80] + "...")

    # Build request body
    body = {
        "model": selected_model,
        "prompt": prompt,
        "n": 1,
        "size": size,
    }

    # Image-to-image or multi-image: add extra_body with image URLs
    if image_urls and len(image_urls) > 0:
        resolved_urls = [resolve_image_to_url(u, get_api_key()) for u in image_urls]
        body["tags"] = ["img2img"]
        body["extra_body"] = {
            "image": resolved_urls,
            "response_format": "url",
        }

    resp = api_request("POST", "/images/generations", body)

    data = resp.get("data", [])
    if not data:
        print("ERROR: No image data in response", file=sys.stderr)
        print("Full response: " + json.dumps(resp, indent=2), file=sys.stderr)
        sys.exit(1)

    item = data[0]

    # Prefer b64_json over URL
    if item.get("b64_json"):
        print("Decoding base64 image data...")
        img_bytes = base64.b64decode(item["b64_json"])
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        print("Saved: " + output_path)
        return output_path

    if item.get("url"):
        download_file(item["url"], output_path)
        return output_path

    print("ERROR: No url or b64_json in image response", file=sys.stderr)
    sys.exit(1)


def generate_video(prompt, duration, output_path):
    """Generate a video using agnes-video-v2.0 with polling."""
    print("Generating video (" + str(duration) + "s): " + prompt[:80] + "...")

    # Create generation task
    resp = api_request("POST", "/video/generations", {
        "model": VIDEO_MODEL,
        "prompt": prompt,
        "duration": duration,
    })

    task_id = resp.get("id")
    if not task_id:
        print("ERROR: No task ID in response", file=sys.stderr)
        sys.exit(1)

    print("Task ID: " + task_id)

    # Poll for completion
    max_attempts = 120  # ~10 minutes at 5s intervals
    for attempt in range(max_attempts):
        time.sleep(5)
        status_resp = api_request("GET", "/video/generations/" + task_id)

        # API wraps response in {"code":"success","data":{...}}
        data = status_resp.get("data", status_resp)
        status = data.get("status", "unknown")
        progress = data.get("progress", "")
        print("  [" + str(attempt + 1) + "] Status: " + str(status) + " (" + str(progress) + ")")

        status_lower = status.lower() if isinstance(status, str) else str(status).lower()

        if status_lower in ("completed", "success"):
            # Video URL can be in result_url, data.remixed_from_video_id, or data.url
            url = data.get("result_url")
            if not url:
                inner_data = data.get("data", {})
                url = inner_data.get("remixed_from_video_id") or inner_data.get("url")
            if url:
                download_file(url, output_path)
                return output_path
            else:
                print("ERROR: Completed but no video URL", file=sys.stderr)
                print("Full response: " + json.dumps(status_resp, indent=2), file=sys.stderr)
                sys.exit(1)

        if status_lower in ("failed", "error"):
            err = data.get("fail_reason") or data.get("error", "Unknown error")
            print("ERROR: Generation failed: " + str(err), file=sys.stderr)
            sys.exit(1)

    print("ERROR: Timed out waiting for video generation", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Agnes AI Generator")
    sub = parser.add_subparsers(dest="command", required=True)

    # Image subcommand
    img = sub.add_parser("image", help="Generate an image")
    img.add_argument("--prompt", required=True, help="Image description")
    img.add_argument("--size", default="1024x1024", help="Image size (default: 1024x1024)")
    img.add_argument("--image", nargs="+", default=None,
                     help="Input image URL(s) or local file path(s) for image-to-image / multi-image")
    img.add_argument("--model", default=None,
                     help="Model name (default: agnes-image-2.1-flash for text-to-image, "
                          "agnes-image-2.0-flash for image-to-image)")
    img.add_argument("--output", required=True, help="Output file path")

    # Video subcommand
    vid = sub.add_parser("video", help="Generate a video")
    vid.add_argument("--prompt", required=True, help="Video description")
    vid.add_argument("--duration", type=int, default=5, help="Duration in seconds (default: 5)")
    vid.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(args.prompt, args.size, args.output, args.image, args.model)
    elif args.command == "video":
        generate_video(args.prompt, args.duration, args.output)

    print("Done.")


if __name__ == "__main__":
    main()
