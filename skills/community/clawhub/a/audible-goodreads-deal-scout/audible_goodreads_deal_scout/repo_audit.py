from __future__ import annotations

import os
import re
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


PRIVATE_MARKERS_ENV = "AUDIBLE_SCOUT_PRIVATE_MARKERS"
GENERIC_LEAK_PATTERNS = (
    (
        "absolute_home_path",
        re.compile(r"(?<![<\w])/(?:Users|home)/[A-Za-z0-9._-]+(?:/[^\s\"'`)>]*)?", re.I),
    ),
    (
        "ssh_overlay_alias",
        re.compile(r"\bssh\s+[A-Za-z0-9._-]*tailscale[A-Za-z0-9._-]*\b", re.I),
    ),
    (
        "credential_assignment",
        re.compile(
            r"(?i)\b(?:access[_-]?token|refresh[_-]?token|api[_-]?key|password|secret)\b\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{12,}"
        ),
    ),
)


def configured_private_markers() -> tuple[str, ...]:
    raw = os.environ.get(PRIVATE_MARKERS_ENV, "")
    return tuple(marker.strip().casefold() for marker in raw.split(",") if marker.strip())


def iter_repo_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".audible-goodreads-deal-scout/"):
            continue
        files.append(path)
    return files


def is_publish_ignored(relative_path: str, patterns: set[str]) -> bool:
    rel = relative_path.lstrip("./")
    for pattern in patterns:
        normalized = pattern.lstrip("./")
        if normalized.endswith("/") and rel.startswith(normalized):
            return True
        if fnmatch(rel, normalized) or fnmatch(Path(rel).name, normalized):
            return True
    return False


def publish_file_paths(root: Path, patterns: set[str]) -> list[Path]:
    return [
        path
        for path in iter_repo_files(root)
        if not is_publish_ignored(path.relative_to(root).as_posix(), patterns)
    ]


def scan_repo_for_leaks(root: Path, *, paths: list[Path] | None = None) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    private_markers = configured_private_markers()
    for path in paths if paths is not None else iter_repo_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        combined = f"{rel}\n{text}"
        for label, pattern in GENERIC_LEAK_PATTERNS:
            if pattern.search(combined):
                findings.append({"type": "pattern", "marker": label, "path": rel})
        lowered_text = text.casefold()
        lowered_rel = rel.casefold()
        for marker in private_markers:
            if marker in lowered_rel:
                findings.append({"type": "path", "marker": "configured_private_marker", "path": rel})
            if marker in lowered_text:
                findings.append({"type": "content", "marker": "configured_private_marker", "path": rel})
    return {"ok": not findings, "findings": findings}
