#!/usr/bin/env python3
"""Compute stable fingerprints for packaged source and validation artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_relative_file(root: Path, value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label} must stay beneath {root}")
    path = root / relative
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"{label} must not escape through a symbolic link")
    return path


def fingerprint_files(entries: list[tuple[str, Path]]) -> str:
    digest = hashlib.sha256()
    for label, path in entries:
        digest.update(label.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def package_fingerprint(package: Path) -> str:
    source = package / "source"
    motion_path = source / "motion.json"
    if not motion_path.is_file():
        raise FileNotFoundError(f"packaged motion not found: {motion_path}")
    motion = json.loads(motion_path.read_text(encoding="utf-8"))
    frames = motion.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("packaged motion must contain a non-empty frames array")
    entries = [("source/motion.json", motion_path)]
    reference_path = source / "reference.json"
    if reference_path.is_file():
        entries.append(("source/reference.json", reference_path))
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        included_path = reference.get("included_path")
        if included_path is not None:
            included = safe_relative_file(
                source,
                included_path,
                "reference.included_path",
            )
            entries.append((f"reference:{included_path}", included))
    for index, frame in enumerate(frames):
        if not isinstance(frame, dict):
            raise ValueError(f"frames[{index}] must be an object")
        path = safe_relative_file(
            source,
            frame.get("file"),
            f"frames[{index}].file",
        )
        entries.append((f"frame:{frame['file']}", path))
    sticker = package / "sticker.webp"
    if sticker.is_file():
        entries.append(
            (
                "sticker.webp",
                safe_relative_file(package, "sticker.webp", "sticker.webp"),
            )
        )
    return fingerprint_files(entries)


def render_track_fingerprint(package: Path) -> str:
    source = package / "source"
    motion_path = source / "motion.json"
    motion = json.loads(motion_path.read_text(encoding="utf-8"))
    render = motion.get("render")
    if not isinstance(render, dict):
        raise ValueError("packaged motion has no render track metadata")
    frame_dir_value = render.get("frame_dir")
    if not isinstance(frame_dir_value, str) or not frame_dir_value:
        raise ValueError("render.frame_dir must be a non-empty relative path")
    relative = Path(frame_dir_value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("render.frame_dir must stay beneath package source")
    frame_dir = source / relative
    if not frame_dir.is_dir() or not frame_dir.resolve().is_relative_to(source.resolve()):
        raise ValueError("render.frame_dir is missing or escapes package source")
    frame_paths = sorted(frame_dir.glob("*.png"))
    if not frame_paths:
        raise ValueError("render track contains no PNG frames")
    metadata = json.dumps(render, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256()
    digest.update(b"render-metadata\0")
    digest.update(metadata)
    digest.update(b"\0")
    for path in frame_paths:
        digest.update(f"render-frame:{path.name}".encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def report_artifact_fingerprint(report_path: Path, report: dict[str, object]) -> str:
    scope = report.get("artifact_scope")
    if scope == "package_source":
        return package_fingerprint(report_path.parent.parent)
    if scope == "render_track":
        return render_track_fingerprint(report_path.parent.parent)
    if scope == "export_files":
        artifacts = report.get("validation_artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError("export validation report must list validation_artifacts")
        entries: list[tuple[str, Path]] = []
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                raise ValueError(f"validation_artifacts[{index}] must be an object")
            path = safe_relative_file(
                report_path.parent,
                artifact.get("path"),
                f"validation_artifacts[{index}].path",
            )
            entries.append((f"artifact:{artifact['path']}", path))
        return fingerprint_files(entries)
    raise ValueError(
        "report artifact_scope must be 'package_source', 'render_track', or 'export_files'"
    )
