"""视觉检查的渲染：把该看的页变成图片，并记下每张图的哈希。

渲染只是给人（或审查代理）准备材料，它不产生任何"通过"结论。
图片哈希记进计划，事后可以核对评审看的到底是不是这一版候选。
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from academic_pdf_translation.verify.visual_plan import (
    REVIEW_DPI,
    VisualReviewError,
    VisualReviewPlan,
)


def render_review_pages(
    candidate_document: Any,
    plan: VisualReviewPlan,
    output_dir: Path,
    *,
    dpi: int = REVIEW_DPI,
) -> list[Path]:
    """把选中的页渲染成图片，供人逐页看。"""

    import fitz

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for item in plan.selected:
        index = item.candidate_page - 1
        if not 0 <= index < candidate_document.page_count:
            raise VisualReviewError(
                f"候选第 {item.candidate_page} 页超出范围，无法渲染"
            )
        pixmap = candidate_document[index].get_pixmap(
            matrix=fitz.Matrix(dpi / 72.0, dpi / 72.0)
        )
        target = output_dir / f"page-{item.candidate_page:04d}.png"
        pixmap.save(target)
        written.append(target)
    plan.rendered = [str(path) for path in written]
    return written


def rendered_image_hashes(paths: list[Path]) -> dict[str, str]:
    """每张渲染图的 SHA-256，供结果与材料对账。"""

    hashes: dict[str, str] = {}
    for path in paths:
        hashes[str(path)] = hashlib.sha256(
            Path(path).read_bytes()
        ).hexdigest()
    return hashes
