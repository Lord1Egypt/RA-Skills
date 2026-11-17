"""Content-preservation guard for high-fidelity model-authored PPT pages.

This guard deliberately permits arbitrary geometry, shape composition and
styling. It only rejects a candidate if it adds or removes native business
text relative to the accepted base deck. It is one gate; provenance remains
owned by the base IR verification and visual quality by a separate review.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from pptx import Presentation


def _normalized(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


def text_inventory(pptx_path: str | Path) -> list[str]:
    """Return native, non-empty textual units in document order."""
    prs = Presentation(str(pptx_path))
    inventory: list[str] = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if not getattr(shape, "has_text_frame", False):
                continue
            text = _normalized(shape.text or "")
            if text:
                inventory.append(text)
    return inventory


def content_lock(base_pptx: str | Path, candidate_pptx: str | Path) -> dict:
    """Compare native text multisets; geometry and shape count may differ."""
    base = Counter(text_inventory(base_pptx))
    candidate = Counter(text_inventory(candidate_pptx))
    missing = list((base - candidate).elements())
    added = list((candidate - base).elements())
    return {
        "status": "pass" if not missing and not added else "fail",
        "base_text_count": sum(base.values()),
        "candidate_text_count": sum(candidate.values()),
        "missing_text": missing,
        "added_text": added,
    }
