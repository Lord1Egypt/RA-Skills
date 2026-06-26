#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Batch image generation using Gemini Batch API (50% cheaper, 24hr turnaround).

Usage:
    uv run batch.py submit requests.jsonl          # Submit batch job
    uv run batch.py status                         # Check job status
    uv run batch.py download -o ./images/          # Download completed results
    uv run batch.py clear                          # Clear saved state

Request JSONL format (one per line):
    {"key": "image1", "prompt": "a sunset", "aspect_ratio": "16:9", "resolution": "2K"}
    {"key": "image2", "prompt": "a mountain", "input_images": ["/path/to/ref.png"]}
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / ".batch_state.json"
MODEL = "gemini-3-pro-image-preview"


def get_api_key() -> str | None:
    return os.environ.get("GEMINI_API_KEY")


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def build_request(item: dict) -> dict:
    """Build a batch API request from a simplified item."""
    parts = []

    # Add input images first
    if "input_images" in item:
        for img_path in item["input_images"]:
            with open(img_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": img_data
                }
            })

    # Add prompt
    parts.append({"text": item["prompt"]})

    # Build generation config
    gen_config = {"responseModalities": ["TEXT", "IMAGE"]}

    image_config = {}
    if "aspect_ratio" in item:
        image_config["aspectRatio"] = item["aspect_ratio"]
    if "resolution" in item:
        image_config["imageSize"] = item["resolution"]

    if image_config:
        gen_config["imageConfig"] = image_config

    return {
        "key": item["key"],
        "request": {
            "contents": [{"parts": parts}],
            "generationConfig": gen_config
        }
    }


def cmd_submit(args):
    """Submit a new batch job."""
    api_key = get_api_key()
    if not api_key:
        print("Error: Set GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Read and convert requests
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Reading requests from {input_path}...")
    requests = []
    keys = []

    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            requests.append(build_request(item))
            keys.append(item["key"])

    print(f"Built {len(requests)} requests")

    # Write batch JSONL
    batch_jsonl = SCRIPT_DIR / ".batch_requests.jsonl"
    with open(batch_jsonl, "w") as f:
        for req in requests:
            f.write(json.dumps(req) + "\n")

    # Upload to Files API
    print("Uploading to Gemini Files API...")
    uploaded_file = client.files.upload(
        file=batch_jsonl,
        config=types.UploadFileConfig(
            display_name=f"batch-{input_path.stem}",
            mime_type="jsonl"
        )
    )
    print(f"Uploaded: {uploaded_file.name}")

    # Create batch job
    print("Creating batch job...")
    batch_job = client.batches.create(
        model=MODEL,
        src=uploaded_file.name,
        config=types.CreateBatchJobConfig(
            display_name=f"gemini-image-batch-{input_path.stem}"
        )
    )

    print(f"✓ Batch job created: {batch_job.name}")
    print(f"  Status: {batch_job.state}")

    # Save state
    state = {
        "job_name": batch_job.name,
        "status": str(batch_job.state),
        "keys": keys,
        "uploaded_file": uploaded_file.name
    }
    save_state(state)
    print(f"✓ State saved")

    # Cleanup
    batch_jsonl.unlink()

    print("\nBatch submitted! Check status with: uv run batch.py status")
    print("Results typically ready within 24 hours.")


def cmd_status(args):
    """Check batch job status."""
    api_key = get_api_key()
    if not api_key:
        print("Error: Set GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    state = load_state()
    if not state or "job_name" not in state:
        print("No active batch job. Use 'submit' first.")
        return

    from google import genai
    client = genai.Client(api_key=api_key)

    batch_job = client.batches.get(name=state["job_name"])
    status = batch_job.state.name if hasattr(batch_job.state, "name") else str(batch_job.state)

    print(f"Job: {batch_job.name}")
    print(f"Status: {status}")
    print(f"Requests: {len(state.get('keys', []))}")

    state["status"] = status
    save_state(state)

    if status == "JOB_STATE_SUCCEEDED":
        print("\n✓ Ready to download: uv run batch.py download -o ./images/")
    elif status == "JOB_STATE_FAILED":
        print(f"\n✗ Job failed: {batch_job.error}")


def cmd_download(args):
    """Download completed batch results."""
    api_key = get_api_key()
    if not api_key:
        print("Error: Set GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    state = load_state()
    if not state or "job_name" not in state:
        print("No active batch job. Use 'submit' first.")
        return

    from google import genai
    client = genai.Client(api_key=api_key)

    batch_job = client.batches.get(name=state["job_name"])
    status = batch_job.state.name if hasattr(batch_job.state, "name") else str(batch_job.state)

    if status != "JOB_STATE_SUCCEEDED":
        print(f"Job not ready. Status: {status}")
        return

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Download results
    result_file = batch_job.dest.file_name
    print(f"Downloading from: {result_file}")

    content_bytes = client.files.download(file=result_file)
    content = content_bytes.decode("utf-8")

    saved = 0
    failed = 0

    for line in content.splitlines():
        if not line:
            continue

        result = json.loads(line)
        key = result.get("key", f"image_{saved}")
        output_path = output_dir / f"{key}.png"

        if "error" in result:
            print(f"  ✗ {key}: {result['error']}")
            failed += 1
            continue

        # Find image in response
        try:
            response = result.get("response", {})
            candidates = response.get("candidates", [])

            for candidate in candidates:
                parts = candidate.get("content", {}).get("parts", [])
                for part in parts:
                    if part.get("inlineData"):
                        img_data = base64.b64decode(part["inlineData"]["data"])
                        with open(output_path, "wb") as f:
                            f.write(img_data)
                        print(f"  ✓ {key}: {output_path}")
                        saved += 1
                        break
        except Exception as e:
            print(f"  ✗ {key}: {e}")
            failed += 1

    print(f"\n✓ Saved {saved} images to {output_dir}")
    if failed:
        print(f"✗ Failed: {failed}")


def cmd_clear(args):
    """Clear batch state."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        print("✓ Batch state cleared")
    else:
        print("No state to clear")


def main():
    parser = argparse.ArgumentParser(description="Batch image generation (50% cheaper, 24hr)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Submit
    sub = subparsers.add_parser("submit", help="Submit batch job")
    sub.add_argument("input", help="JSONL file with requests")
    sub.set_defaults(func=cmd_submit)

    # Status
    sub = subparsers.add_parser("status", help="Check job status")
    sub.set_defaults(func=cmd_status)

    # Download
    sub = subparsers.add_parser("download", help="Download results")
    sub.add_argument("-o", "--output", default="./batch_images", help="Output directory")
    sub.set_defaults(func=cmd_download)

    # Clear
    sub = subparsers.add_parser("clear", help="Clear batch state")
    sub.set_defaults(func=cmd_clear)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
