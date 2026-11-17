#!/usr/bin/env python3
"""
APIMart Image Generation Backend

Handles APIMart's async task-based image generation (gpt-image-2).
APIMart returns a task_id on submission; this backend polls for completion.

API endpoint: POST https://api.apimart.ai/v1/images/generations
Poll endpoint: GET  https://api.apimart.ai/v1/tasks/{task_id}

Configuration keys:
  OPENAI_API_KEY        (required) APIMart API key
  OPENAI_BASE_URL       (optional) Default: https://api.apimart.ai/v1/
  APIMART_POLL_INTERVAL (optional) Seconds between poll attempts (default: 5)
  APIMART_MAX_POLLS     (optional) Maximum poll attempts (default: 120 = 10 min)

Dependencies:
  pip install requests Pillow
"""

import json
import os
import sys
import time

import requests

from image_backends.backend_common import (
    MAX_RETRIES,
    download_image,
    is_rate_limit_error,
    normalize_image_size,
    resolve_output_path,
    retry_delay,
    save_image_bytes,
)

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_BASE_URL = "https://api.apimart.ai/v1/"

# APIMart GPT-Image-2 supported aspect ratios (from official docs)
VALID_ASPECT_RATIOS = [
    "1:1", "3:2", "2:3", "4:3", "3:4", "5:4", "4:5",
    "16:9", "9:16", "2:1", "1:2", "3:1", "1:3", "21:9", "9:21",
]

# Map image_size param to API resolution field
IMAGE_SIZE_TO_RESOLUTION = {
    "512px": "1k",
    "1K": "1k",
    "2K": "2k",
    "4K": "4k",
}


def _resolution_from_image_size(image_size: str) -> str:
    """Convert image_size (e.g. '2K') to API resolution (e.g. '2k')."""
    image_size = normalize_image_size(image_size)
    return IMAGE_SIZE_TO_RESOLUTION.get(image_size, "1k")


def _submit_task(api_key: str, base_url: str, prompt: str,
                 aspect_ratio: str, resolution: str, model: str) -> str:
    """Submit an image generation task and return the task_id."""
    url = f"{base_url.rstrip('/')}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "size": aspect_ratio,
        "resolution": resolution,
        "n": 1,
    }

    print(f"  [..] Submitting task...", end="", flush=True)
    resp = requests.post(url, headers=headers, json=payload, timeout=60,
                         proxies={"http": None, "https": None})

    if resp.status_code != 200:
        raise RuntimeError(
            f"Task submission failed ({resp.status_code}): {resp.text[:500]}"
        )

    body = resp.json()

    # Check API-level error code
    code = body.get("code", 200)
    if code != 200:
        error_info = body.get("error", {})
        raise RuntimeError(
            f"API error (code={code}): {error_info.get('message', str(body)[:300])}"
        )

    task_id = body.get("data", [{}])[0].get("task_id")
    if not task_id:
        raise RuntimeError(
            f"Unexpected submission response: {json.dumps(body, ensure_ascii=False)[:500]}"
        )
    print(f" task_id={task_id}")
    return task_id


def _poll_task(api_key: str, base_url: str, task_id: str,
               poll_interval: int = 5, max_polls: int = 120) -> dict:
    """Poll for task completion and return the result data."""
    url = f"{base_url.rstrip('/')}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"  [..] Polling task...", end="", flush=True)
    start = time.time()

    for attempt in range(max_polls):
        resp = requests.get(url, headers=headers, timeout=30,
                            proxies={"http": None, "https": None})

        if resp.status_code != 200:
            print(f"\n  [WARN] Poll failed ({resp.status_code}), retrying...")
            time.sleep(poll_interval)
            continue

        body = resp.json()

        # Check API-level error code
        code = body.get("code", 200)
        if code != 200:
            print(f"\n  [WARN] API error code={code}, retrying...")
            time.sleep(poll_interval)
            continue

        data = body.get("data", {})
        status = data.get("status", "unknown")

        elapsed = time.time() - start

        if status in ("completed", "succeed"):
            print(f" done ({elapsed:.0f}s)")
            return data.get("result", {})

        if status == "failed":
            error_msg = data.get("error", "Unknown error")
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", str(error_msg))
            raise RuntimeError(f"Task failed: {error_msg}")

        if attempt > 0 and attempt % 6 == 0:
            print(f" {elapsed:.0f}s...", end="", flush=True)

        time.sleep(poll_interval)

    raise RuntimeError(f"Task did not complete within {max_polls * poll_interval}s")


def _download_result(result: dict, output_dir: str, filename: str) -> str:
    """Download image(s) from the task result and save to disk."""
    images = result.get("images", [])
    if not images:
        raise RuntimeError("Task result contains no images")

    image_data = images[0]
    urls = image_data.get("url", [])
    if not urls:
        raise RuntimeError("Task result image has no URL")

    image_url = urls[0]
    ext = ".png"

    path = resolve_output_path("apimart_image", output_dir, filename, ext)
    return download_image(image_url, path)


def generate(prompt: str,
             aspect_ratio: str = "1:1", image_size: str = "1K",
             output_dir: str = None, filename: str = None,
             model: str = None, max_retries: int = MAX_RETRIES) -> str:
    """
    APIMart image generation with async task support.

    Reads credentials from environment or .env:
      OPENAI_API_KEY  (required)
      OPENAI_BASE_URL (optional, default: https://api.apimart.ai/v1/)

    Args:
        prompt: Prompt text
        aspect_ratio: Aspect ratio (e.g. "16:9")
        image_size: Image size ("512px", "1K", "2K", "4K")
        output_dir: Output directory
        filename: Output filename (without extension)
        model: Model name (default: gpt-image-2)
        max_retries: Maximum retries

    Returns:
        Path of the saved image file
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL)

    if not api_key:
        raise ValueError(
            "No API key found. Set OPENAI_API_KEY in the current environment or a .env file."
        )

    if model is None:
        model = os.environ.get("OPENAI_MODEL") or DEFAULT_MODEL

    if aspect_ratio not in VALID_ASPECT_RATIOS:
        raise ValueError(
            f"Unsupported aspect ratio '{aspect_ratio}' for APIMart backend. "
            f"Supported: {', '.join(VALID_ASPECT_RATIOS)}"
        )

    resolution = _resolution_from_image_size(image_size)

    print(f"[APIMart - {base_url}]")
    print(f"  Model:        {model}")
    print(f"  Prompt:       {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print(f"  Size:         {aspect_ratio}")
    print(f"  Resolution:   {resolution} (from image_size={image_size})")
    print()

    poll_interval = int(os.environ.get("APIMART_POLL_INTERVAL", "5"))
    max_polls = int(os.environ.get("APIMART_MAX_POLLS", "120"))

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            task_id = _submit_task(
                api_key, base_url, prompt, aspect_ratio, resolution, model
            )
            result = _poll_task(api_key, base_url, task_id, poll_interval, max_polls)
            saved_path = _download_result(result, output_dir, filename)
            print(f"  [SAVED] {saved_path}")
            return saved_path
        except Exception as e:
            last_error = e
            if attempt < max_retries and is_rate_limit_error(e):
                delay = retry_delay(attempt, rate_limited=True)
                print(f"\n  [WARN] Rate limit hit (attempt {attempt + 1}/{max_retries + 1}). "
                      f"Waiting {delay}s before retry...")
                time.sleep(delay)
            elif attempt < max_retries:
                delay = retry_delay(attempt, rate_limited=False)
                print(f"\n  [WARN] Error (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                      f"Retrying in {delay}s...")
                time.sleep(delay)
            else:
                break

    raise RuntimeError(f"Failed after {max_retries + 1} attempts. Last error: {last_error}")
