#!/usr/bin/env python3
"""
Volcengine Jimeng AI Video Generation Client (using official SDK).

Usage:
    python jimeng_client.py generate --prompt "description" --output ./output/video.mp4
    python jimeng_client.py generate --prompt "description" --aspect-ratio 9:16 --duration 5
    python jimeng_client.py status --task-id <task_id>

Environment variables:
    VOLCENGINE_ACCESS_KEY  - Volcengine Access Key ID
    VOLCENGINE_SECRET_KEY  - Volcengine Secret Access Key
"""

import argparse
import json
import os
import sys
import time
import urllib.request

from volcengine.visual.VisualService import VisualService


# req_key mapping
MODEL_KEYS = {
    "720p": "jimeng_t2v_v30",
    "1080p": "jimeng_t2v_v30_1080p",
    "pro": "jimeng_ti2v_v30_pro",
}

# frames mapping: 3.0 Pro requires frames % 24 == 1
# 24fps: 97(~4s), 121(~5s), 145(~6s), 193(~8s), 241(~10s)
DURATION_TO_FRAMES = {
    4: 97,
    5: 121,
    6: 145,
    8: 193,
    10: 241,
}


def _create_service(access_key: str, secret_key: str) -> VisualService:
    """Create and configure VisualService instance."""
    service = VisualService()
    service.set_ak(access_key)
    service.set_sk(secret_key)
    return service


def submit_task(
    service: VisualService,
    prompt: str,
    aspect_ratio: str = "9:16",
    duration: int = 5,
    model: str = "720p",
) -> str:
    """Submit a video generation task. Returns task_id."""
    req_key = MODEL_KEYS.get(model, MODEL_KEYS["720p"])
    frames = DURATION_TO_FRAMES.get(duration, 151)

    form = {
        "req_key": req_key,
        "prompt": prompt,
        "seed": -1,
        "frames": frames,
        "aspect_ratio": aspect_ratio,
    }

    print(f"Submitting video generation task...")
    print(f"  Model: {model} ({req_key})")
    print(f"  Duration: {duration}s ({frames} frames)")
    print(f"  Aspect ratio: {aspect_ratio}")
    print(f"  Prompt: {prompt[:100]}...")

    result = service.cv_sync2async_submit_task(form)

    if result.get("code") != 10000:
        print(f"Error submitting task: {json.dumps(result, ensure_ascii=False, indent=2)}")
        sys.exit(1)

    task_id = result["data"]["task_id"]
    print(f"Task submitted successfully! task_id: {task_id}")
    return task_id


def poll_task(
    service: VisualService,
    task_id: str,
    req_key: str,
    interval: int = 10,
    max_wait: int = 600,
) -> dict:
    """Poll for task completion. Returns result dict with video_url."""
    form = {
        "req_key": req_key,
        "task_id": task_id,
    }

    elapsed = 0
    while elapsed < max_wait:
        result = service.cv_sync2async_get_result(form)

        code = result.get("code")
        data = result.get("data", {})
        status = data.get("status", "")

        if code == 10000 and status == "done":
            print(f"Video generation complete! ({elapsed}s elapsed)")
            return data

        if status in ("not_start", "running", "processing", "submitted", "in_queue") or code != 10000:
            print(f"  {status or 'waiting'}... ({elapsed}s elapsed)")
            time.sleep(interval)
            elapsed += interval
            continue

        # Unexpected status
        print(f"Unexpected response: {json.dumps(result, ensure_ascii=False, indent=2)}")
        time.sleep(interval)
        elapsed += interval

    print(f"Timeout after {max_wait}s waiting for task {task_id}")
    sys.exit(1)


def download_video(url: str, output_path: str):
    """Download video from URL to local file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"Downloading video to {output_path}...")
    urllib.request.urlretrieve(url, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Downloaded: {size_mb:.1f} MB")


def generate(
    prompt: str,
    output: str,
    aspect_ratio: str = "9:16",
    duration: int = 5,
    model: str = "720p",
):
    """Full pipeline: submit -> poll -> download."""
    access_key = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
    secret_key = os.environ.get("VOLCENGINE_SECRET_KEY", "")

    if not access_key or not secret_key:
        print("Error: VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY must be set")
        print("  export VOLCENGINE_ACCESS_KEY=your_key")
        print("  export VOLCENGINE_SECRET_KEY=your_secret")
        sys.exit(1)

    service = _create_service(access_key, secret_key)
    req_key = MODEL_KEYS.get(model, MODEL_KEYS["720p"])

    task_id = submit_task(service, prompt, aspect_ratio, duration, model)

    print(f"\nWaiting for video generation (may take 1-5 minutes)...")
    result = poll_task(service, task_id, req_key)

    # Extract video URL (try multiple response formats)
    video_url = result.get("video_url", "")
    if not video_url:
        resp_data = result.get("resp_data")
        if isinstance(resp_data, str):
            try:
                resp_data = json.loads(resp_data)
            except json.JSONDecodeError:
                pass
        if isinstance(resp_data, dict):
            video_url = resp_data.get("video_url", "")
    # Also check video_urls array
    if not video_url:
        video_urls = result.get("video_urls", [])
        if video_urls:
            video_url = video_urls[0]

    if not video_url:
        print(f"No video URL in response:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    download_video(video_url, output)
    print(f"\nDone! Video saved to: {output}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Jimeng AI Video Generation Client")
    subparsers = parser.add_subparsers(dest="command")

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a video")
    gen_parser.add_argument("--prompt", required=True, help="Video generation prompt")
    gen_parser.add_argument("--output", required=True, help="Output file path")
    gen_parser.add_argument(
        "--aspect-ratio", default="9:16", help="Aspect ratio (default: 9:16)"
    )
    gen_parser.add_argument(
        "--duration", type=int, default=5, help="Duration in seconds (default: 5)"
    )
    gen_parser.add_argument(
        "--model",
        default="720p",
        choices=["720p", "1080p", "pro"],
        help="Model quality (default: 720p)",
    )

    # status command
    status_parser = subparsers.add_parser("status", help="Check task status")
    status_parser.add_argument("--task-id", required=True, help="Task ID to check")
    status_parser.add_argument(
        "--model", default="720p", choices=["720p", "1080p", "pro"]
    )

    args = parser.parse_args()

    if args.command == "generate":
        generate(args.prompt, args.output, args.aspect_ratio, args.duration, args.model)
    elif args.command == "status":
        access_key = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
        secret_key = os.environ.get("VOLCENGINE_SECRET_KEY", "")
        if not access_key or not secret_key:
            print("Error: VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY must be set")
            sys.exit(1)
        service = _create_service(access_key, secret_key)
        req_key = MODEL_KEYS.get(args.model, MODEL_KEYS["720p"])
        result = poll_task(service, args.task_id, req_key, max_wait=1)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
