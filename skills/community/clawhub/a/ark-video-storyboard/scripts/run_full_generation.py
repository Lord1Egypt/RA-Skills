#!/usr/bin/env python3
"""Run the full multi-segment generation flow from storyboard JSON."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from submit_segment import submit, load_api_key
from poll_task_until_done import poll
from download_video import download

DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"
DEFAULT_RATIO = "16:9"
DEFAULT_WATERMARK = False
DEFAULT_POLL_INTERVAL = 10
DEFAULT_POLL_TIMEOUT = 1800
SUPPORTED_DURATION_MIN = 4
SUPPORTED_DURATION_MAX = 12
DEFAULT_TOTAL_DURATION = 60
DEFAULT_SEGMENT_COUNT = 6


def compute_duration(total_duration_seconds: int, segment_count: int) -> int:
    if segment_count <= 0:
        raise ValueError("segment_count must be > 0")
    if total_duration_seconds % segment_count != 0:
        raise ValueError(f"total_duration_seconds={total_duration_seconds} 不能被 segment_count={segment_count} 整除")
    duration = total_duration_seconds // segment_count
    if not (SUPPORTED_DURATION_MIN <= duration <= SUPPORTED_DURATION_MAX):
        raise ValueError(
            f"当前模型要求单段 duration 为 {SUPPORTED_DURATION_MIN}~{SUPPORTED_DURATION_MAX} 的整数秒；当前计算值为 {duration}"
        )
    return duration


def build_payload(segment: dict, image_refs: list[str] | None = None, duration_override: int | None = None) -> dict:
    duration = duration_override if duration_override is not None else segment.get("duration_seconds", 10)
    content = [{"type": "text", "text": segment["ai_prompt"]}]
    for ref in image_refs or []:
        content.append({
            "type": "image_url",
            "image_url": {"url": ref},
            "role": "reference_image",
        })
    return {
        "model": DEFAULT_MODEL,
        "content": content,
        "ratio": DEFAULT_RATIO,
        "duration": duration,
        "watermark": DEFAULT_WATERMARK,
        "metadata": {
            "segment_index": segment["segment_index"],
            "requested_duration_seconds": segment.get("duration_seconds", duration),
            "visual_description": segment.get("visual_description", ""),
            "lighting_state": segment.get("lighting_state", ""),
            "continuity_notes": segment.get("continuity_notes", ""),
        },
    }


def maybe_download(video_url: str | None, output_dir: str | None, title: str, segment_index: int) -> str | None:
    if not video_url or not output_dir:
        return None
    safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in (title or "storyboard"))
    filename = f"{safe_title}_segment_{segment_index}.mp4"
    return download(video_url, str(Path(output_dir) / filename))


def run(storyboard_path: str, image_refs: list[str] | None = None, poll_interval: int = DEFAULT_POLL_INTERVAL, poll_timeout: int = DEFAULT_POLL_TIMEOUT, download_dir: str | None = None) -> dict:
    storyboard = json.loads(Path(storyboard_path).read_text(encoding="utf-8"))
    total_duration = storyboard.get("total_duration_seconds", DEFAULT_TOTAL_DURATION)
    segments = storyboard.get("segments", [])
    segment_count = storyboard.get("segment_count") or len(segments) or DEFAULT_SEGMENT_COUNT
    duration_per_segment = compute_duration(total_duration, segment_count)

    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("ARK_VIDEO_STORYBOARD_API_KEY") or load_api_key()
    results = []

    for segment in segments:
        payload = build_payload(segment, image_refs=image_refs, duration_override=duration_per_segment)
        submit_resp = submit(payload, api_key=api_key)
        task_id = submit_resp.get("id")
        item = {
            "segment_index": segment["segment_index"],
            "prompt": segment["ai_prompt"],
            "payload": payload,
            "submit_response": submit_resp,
            "task_id": task_id,
            "status": None,
            "video_url": None,
            "downloaded_path": None,
            "poll_response": None,
        }
        if task_id:
            poll_resp = poll(task_id, interval_seconds=poll_interval, timeout_seconds=poll_timeout)
            item["status"] = poll_resp.get("status")
            item["video_url"] = poll_resp.get("video_url")
            item["poll_response"] = poll_resp
            item["downloaded_path"] = maybe_download(item["video_url"], download_dir, storyboard.get("title", "storyboard"), segment["segment_index"])
        results.append(item)

    return {
        "storyboard_title": storyboard.get("title"),
        "total_duration_seconds": total_duration,
        "segment_count": segment_count,
        "duration_per_segment": duration_per_segment,
        "download_dir": download_dir,
        "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("storyboard_json")
    parser.add_argument("image_refs", nargs="*")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--poll-timeout", type=int, default=DEFAULT_POLL_TIMEOUT)
    parser.add_argument("--download-dir")
    args = parser.parse_args()
    print(json.dumps(run(args.storyboard_json, image_refs=args.image_refs, poll_interval=args.poll_interval, poll_timeout=args.poll_timeout, download_dir=args.download_dir), ensure_ascii=False, indent=2))
