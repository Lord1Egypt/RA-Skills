from __future__ import annotations

import time
from typing import Any

from canvas_claw.client import CanvasClawClient
from canvas_claw.errors import CanvasClawError


def build_image_request(
    *,
    prompt: str,
    capability: str,
    task_type: str,
    provider: str,
    model_id: str,
    image_urls: list[str],
    aspect_ratio: str,
    resolution: str,
) -> dict[str, Any]:
    return {
        "type": task_type,
        "provider": provider,
        "model_id": model_id,
        "input": {
            "prompt": prompt,
            "image_urls": image_urls,
            "video_url": None,
        },
        "options": {
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        },
        "meta": {
            "source": "openclaw",
            "capability": capability,
        },
    }


def build_video_request(
    *,
    prompt: str,
    capability: str,
    provider: str,
    model_id: str,
    image_urls: list[str],
    aspect_ratio: str,
    resolution: str,
    duration: int,
    generate_audio: bool,
) -> dict[str, Any]:
    task_type = "image_to_video" if image_urls else "text_to_video"
    return {
        "type": task_type,
        "provider": provider,
        "model_id": model_id,
        "input": {
            "prompt": prompt,
            "image_urls": image_urls,
            "video_url": None,
        },
        "options": {
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": duration,
            "sound": generate_audio,
        },
        "meta": {
            "source": "openclaw",
            "capability": capability,
        },
    }


def normalize_task_result(task_response: dict[str, Any]) -> dict[str, Any]:
    result = task_response.get("result", {})
    return {
        "task_id": task_response.get("task_id"),
        "status": task_response.get("status"),
        "progress": task_response.get("progress"),
        "result_urls": result.get("result_urls", []),
        "primary_url": result.get("primary_url"),
        "text": result.get("text"),
        "updated_at": task_response.get("updated_at"),
    }


def poll_until_terminal(
    client: CanvasClawClient,
    *,
    task_id: str,
    poll_interval: float,
    timeout: float,
) -> dict[str, Any]:
    started_at = time.monotonic()
    while True:
        response = client.get_task(task_id)
        status = str(response.get("status") or "").strip()
        if status == "succeeded":
            return normalize_task_result(response)
        if status == "failed":
            error = response.get("error") or {}
            raise CanvasClawError(
                f"Task failed: {error.get('code') or 'unknown'} {error.get('message') or ''}".strip()
            )
        if time.monotonic() - started_at > timeout:
            raise CanvasClawError(f"Task polling timed out for {task_id}")
        time.sleep(poll_interval)


def submit_and_poll(
    client: CanvasClawClient,
    *,
    payload: dict[str, Any],
    poll_interval: float,
    timeout: float,
) -> dict[str, Any]:
    created = client.create_task(payload)
    task_id = str(created.get("task_id") or "").strip()
    if not task_id:
        raise CanvasClawError("Create task response missing task_id")
    return poll_until_terminal(
        client,
        task_id=task_id,
        poll_interval=poll_interval,
        timeout=timeout,
    )
