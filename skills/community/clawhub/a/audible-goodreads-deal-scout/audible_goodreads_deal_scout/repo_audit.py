from __future__ import annotations

from pathlib import Path
from typing import Any


FORBIDDEN_LEAK_MARKERS = {
    "horst",
    "tailscale",
    "openclawchaperone",
    "/home/openclaw",
    "d068138",
    "bot - books",
    "books & blogs",
}


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


def scan_repo_for_leaks(root: Path) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    for path in iter_repo_files(root):
        rel = path.relative_to(root).as_posix()
        lowered_rel = rel.casefold()
        for marker in FORBIDDEN_LEAK_MARKERS:
            if marker in lowered_rel:
                findings.append({"type": "path", "marker": marker, "path": rel})
        if rel == "audible_goodreads_deal_scout/repo_audit.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        lowered_text = text.casefold()
        for marker in FORBIDDEN_LEAK_MARKERS:
            if marker in lowered_text:
                findings.append({"type": "content", "marker": marker, "path": rel})
    return {"ok": not findings, "findings": findings}
