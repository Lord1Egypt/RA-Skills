"""Merge logic scaffold."""

import re


def split_character_sections(content: str):
    """Extract character sections from merged SOUL markdown (best-effort)."""
    pattern = r'## ([^\n]+)\n(.*?)(?=\n## [^\n]+\n|\Z)'
    return re.findall(pattern, content, re.DOTALL)


def merge_soul_content(existing: str, new: str) -> str:
    """Idempotent merge by section title + body content string equality."""
    if not existing.strip():
        return new
    if new.strip() in existing:
        return existing
    return existing.rstrip() + "\n\n" + new.lstrip()
