from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from canvas_claw.download import download_url, infer_extension


def write_metadata(*, output_dir: Path, payload: dict[str, Any]) -> Path:
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return metadata_path


def _save_images(output_dir: Path, result_urls: list[str]) -> list[str]:
    saved_files: list[str] = []
    for index, url in enumerate(result_urls, start=1):
        file_path = output_dir / f"image_{index}{infer_extension(url, '.jpg')}"
        download_url(url, file_path)
        saved_files.append(file_path.name)
    return saved_files


def _save_videos(output_dir: Path, result_urls: list[str]) -> list[str]:
    saved_files: list[str] = []
    multiple = len(result_urls) > 1
    for index, url in enumerate(result_urls, start=1):
        filename = f"video_{index}.mp4" if multiple else "video.mp4"
        file_path = output_dir / filename
        download_url(url, file_path)
        saved_files.append(file_path.name)
    return saved_files


def save_result_bundle(
    *,
    output_dir: Path,
    result: dict[str, Any],
    kind: str,
    metadata: dict[str, Any],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    result_urls = [str(url) for url in result.get("result_urls", []) if str(url).strip()]
    if kind == "image":
        downloaded_files = _save_images(output_dir, result_urls)
    else:
        downloaded_files = _save_videos(output_dir, result_urls)
    merged_metadata = dict(metadata)
    merged_metadata["result_urls"] = result_urls
    merged_metadata["downloaded_files"] = downloaded_files
    if result.get("task_id") is not None:
        merged_metadata["task_id"] = result["task_id"]
    if result.get("status") is not None:
        merged_metadata["status"] = result["status"]
    if result.get("updated_at") is not None:
        merged_metadata["updated_at"] = result["updated_at"]
    return write_metadata(output_dir=output_dir, payload=merged_metadata)
