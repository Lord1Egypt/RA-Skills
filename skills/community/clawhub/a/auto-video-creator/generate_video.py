#!/usr/bin/env python3
"""
XLXAI Video Generation Script
Generates videos from text prompts or images using the XLXAI API.
"""

import sys
import json
import time
import argparse
import requests
import os
import base64
from pathlib import Path
from typing import Optional

API_BASE = "https://api.xlxai.store"
# Load API key from environment variable. Do NOT hardcode API keys in code.
API_KEY = os.environ.get("XLXAI_API_KEY")
if not API_KEY:
    sys.exit("Missing API key: set the XLXAI_API_KEY environment variable (e.g. export XLXAI_API_KEY=sk-... ). See skills/xlxai-video/.env.example for an example and do NOT commit real keys to the repository.")

MODELS = [
    "sora2-portrait-4s",
    "sora2-landscape-4s",
    "sora2-portrait-8s",
    "sora2-landscape-8s",
    "sora2-portrait-12s",
    "sora2-landscape-12s",
]

# Convert local image to data URI
def image_to_data_uri(image_path: str) -> str:
    """Convert local image to data URI."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    print(f"Converting image to data URI: {image_path}", file=sys.stderr)
    
    # Detect mime type
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    data_uri = f"data:{mime_type};base64,{image_data}"
    print(f"Image converted to data URI ({len(data_uri)} chars)", file=sys.stderr)
    return data_uri


def create_video_task(
    prompt: str,
    model: str = "sora2-portrait-4s",
    image_url: Optional[str] = None
) -> dict:
    """Create a video generation task."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt
    }
    
    if image_url:
        payload["image_url"] = image_url
    
    response = requests.post(
        f"{API_BASE}/v1/video/generations",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def check_task_status(task_id: str) -> dict:
    """Check the status of a video generation task."""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.get(
        f"{API_BASE}/v1/videos/{task_id}",
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def wait_for_completion(task_id: str, poll_interval: int = 10, timeout: int = 600) -> dict:
    """Poll task status until completion or timeout."""
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Video generation timed out after {timeout} seconds")
        
        status_data = check_task_status(task_id)
        status = status_data.get("status")
        progress = status_data.get("progress", 0)
        
        print(f"Status: {status} | Progress: {progress}%", file=sys.stderr)
        
        if status == "completed":
            return status_data
        elif status == "failed":
            message = status_data.get("message", "Unknown error")
            raise RuntimeError(f"Video generation failed: {message}")
        
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using XLXAI API"
    )
    parser.add_argument(
        "prompt",
        help="Text prompt describing the video to generate"
    )
    parser.add_argument(
        "--model",
        choices=MODELS,
        default="sora2-portrait-4s",
        help="Model to use for generation (default: sora2-portrait-4s)"
    )
    parser.add_argument(
        "--image",
        help="Image URL or local file path for image-to-video generation"
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for completion, just return task ID"
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between status checks (default: 10)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Maximum seconds to wait for completion (default: 600)"
    )
    
    args = parser.parse_args()
    
    try:
        # Handle image parameter - upload if local file
        image_url = None
        if args.image:
            if args.image.startswith(("http://", "https://")):
                # Already a URL
                image_url = args.image
            else:
                # Local file - convert to data URI
                image_url = image_to_data_uri(args.image)
        
        # Create task
        print("Creating video generation task...", file=sys.stderr)
        task_data = create_video_task(
            prompt=args.prompt,
            model=args.model,
            image_url=image_url
        )
        
        task_id = task_data["task_id"]
        print(f"Task created: {task_id}", file=sys.stderr)
        
        if args.no_wait:
            print(json.dumps(task_data, indent=2))
            return
        
        # Wait for completion
        print("Waiting for video generation...", file=sys.stderr)
        result = wait_for_completion(
            task_id,
            poll_interval=args.poll_interval,
            timeout=args.timeout
        )
        
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
