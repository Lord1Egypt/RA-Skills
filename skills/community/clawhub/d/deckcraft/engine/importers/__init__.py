"""
DeckCraft v5.3 — Source Importers

Convert various document formats (PDF, DOCX) into DeckCraft outline JSON,
which can then be rendered into PPTX via `scripts/generate_ppt.py`.

This module is part of the v5.3 source-import feature.
"""
from .pdf import pdf_to_outline
from .docx import docx_to_outline
from .text import text_to_outline
from .base import detect_and_import

import os
import re
import json


def extract_image_manifest(content_path: str) -> list[dict]:
    """
    从源文档(MD)提取图片引用,生成 PPT Master 风格的资源清单。

    返回 list of dict,每个 dict:
    {
        "filename": "cover_bg.png",
        "size": "1920x1080",
        "aspect_ratio": 1.78,
        "layout_hint": "wide",
        "usage": "封面背景",
        "type": "background",
        "status": "pending",
    }
    """
    if not os.path.isfile(content_path):
        return []

    ext = os.path.splitext(content_path)[1].lower()
    if ext != ".md" and ext != ".txt":
        return []

    with open(content_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Match ![alt](path) and ![](path)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)

    if not matches:
        return []

    manifest = []
    for idx, (alt_text, img_path) in enumerate(matches):
        filename = os.path.basename(img_path.split("?")[0])
        if not filename:
            filename = f"image_{idx + 1}.png"

        # Infer size from alt text or defaults
        size_str = "1920x1080"
        aspect = 1.78
        hint = "wide"
        img_type = "photo"
        usage = f"幻灯片图片 {idx + 1}"

        alt_lower = alt_text.lower()
        if any(k in alt_lower for k in ["bg", "background", "背景"]):
            img_type = "background"
            usage = "背景图"
        elif any(k in alt_lower for k in ["icon", "图标"]):
            img_type = "icon"
            usage = "图标"
        elif any(k in alt_lower for k in ["chart", "图表", "chart"]):
            img_type = "chart"
            usage = "图表"
        elif any(k in alt_lower for k in ["cover", "封面"]):
            img_type = "background"
            usage = "封面背景"
        elif any(k in alt_lower for k in ["logo"]):
            img_type = "decoration"
            usage = "Logo"

        if alt_text:
            usage = alt_text

        manifest.append({
            "filename": filename,
            "size": size_str,
            "aspect_ratio": aspect,
            "layout_hint": hint,
            "usage": usage,
            "type": img_type,
            "status": "pending",
        })

    return manifest


__all__ = [
    "pdf_to_outline",
    "docx_to_outline",
    "text_to_outline",
    "detect_and_import",
    "extract_image_manifest",
]
