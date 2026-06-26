from __future__ import annotations

import hashlib
from typing import Optional


def md5_text(text: Optional[str]) -> str:
    """
    对文本生成 MD5 哈希。
    """
    value = (text or "").strip()
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def build_content_hash(
    title: Optional[str],
    summary: Optional[str] = None,
    content: Optional[str] = None,
) -> str:
    """
    组合标题/摘要/正文生成稳定内容哈希。
    """
    combined = " || ".join([
        (title or "").strip().lower(),
        (summary or "").strip().lower(),
        (content or "").strip().lower(),
    ])
    return md5_text(combined)