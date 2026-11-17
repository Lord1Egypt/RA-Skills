#!/usr/bin/env python3
"""Shared helpers for the adaptive image handoff skill."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
BACKENDS = {
    "auto",
    "chatgpt_computer_use",
    "built_in_imagegen",
    "manual_chatgpt_handoff",
    "mixed",
    "deterministic",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temporary, path)


def parse_dimensions(value: str) -> tuple[int, int]:
    normalized = value.lower().replace(" ", "")
    parts = normalized.split("x", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid dimensions '{value}', expected WIDTHxHEIGHT")
    width, height = int(parts[0]), int(parts[1])
    if width <= 0 or height <= 0:
        raise ValueError(f"Dimensions must be positive: {value}")
    return width, height


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_info(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        width, height = image.size
        return {
            "width": width,
            "height": height,
            "format": image.format or path.suffix.lstrip(".").upper(),
            "mode": image.mode,
            "ratio": round(width / height, 6),
        }


def find_job(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    for job in state.get("jobs", []):
        if job.get("job_id") == job_id:
            return job
    raise ValueError(f"Unknown job_id: {job_id}")


def refresh_run_status(state: dict[str, Any]) -> None:
    jobs = state.get("jobs", [])
    statuses = [job.get("status") for job in jobs]
    confirmations = [job.get("human_confirmation") for job in jobs]
    selected_backend = state.get("generation_runtime", {}).get("selected_backend")

    if jobs and all(status == "qa_passed" for status in statuses):
        if all(status == "approved" for status in confirmations):
            state["run_status"] = "ready_for_downstream"
        else:
            state["run_status"] = "awaiting_human_confirmation"
    elif any(status == "needs_revision" for status in statuses):
        state["run_status"] = "needs_revision"
    elif any(status in {"prompt_submitted", "generating", "downloaded", "imported"} for status in statuses):
        state["run_status"] = "in_progress"
    elif any(status == "failed" for status in statuses):
        state["run_status"] = "retryable_failures"
    elif selected_backend:
        state["run_status"] = "ready_for_generation"
    else:
        state["run_status"] = "awaiting_backend_selection"
    state["updated_at"] = utc_now()


def render_contact_sheet(handoff: Path, state: dict[str, Any]) -> Path | None:
    imported: list[tuple[str, Path]] = []
    for job in state.get("jobs", []):
        relative = job.get("import", {}).get("output_path")
        if relative:
            candidate = handoff / relative
            if candidate.exists():
                imported.append((job["job_id"], candidate))

    if not imported:
        return None

    columns = min(4, len(imported))
    rows = (len(imported) + columns - 1) // columns
    cell_width, cell_height = 300, 440
    margin, header = 32, 64
    sheet = Image.new(
        "RGB",
        (margin * 2 + columns * cell_width, header + margin + rows * cell_height),
        "#111820",
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 22), f"IMAGE HANDOFF / {state.get('run_id', 'RUN')}", fill="#F2E7D1")

    for index, (job_id, path) in enumerate(imported):
        row, column = divmod(index, columns)
        x = margin + column * cell_width
        y = header + row * cell_height
        with Image.open(path) as image:
            thumb = ImageOps.contain(image.convert("RGB"), (260, 360))
        frame = Image.new("RGB", (270, 370), "#F2E7D1")
        frame.paste(thumb, ((270 - thumb.width) // 2, (370 - thumb.height) // 2))
        sheet.paste(frame, (x, y))
        draw.text((x, y + 382), job_id, fill="#D7A72F")
        draw.text((x, y + 404), path.name, fill="#F2E7D1")

    output = handoff / "reports" / "contact-sheet.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)
    return output
