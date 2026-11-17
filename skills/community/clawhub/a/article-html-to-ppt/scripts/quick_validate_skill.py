#!/usr/bin/env python3
"""Validate the public Skill entrypoint without requiring a YAML dependency."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def frontmatter(text: str) -> str:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    return match.group(1)


def scalar(block: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+)", block)
    if not match:
        raise ValueError(f"SKILL.md frontmatter is missing {key}")
    return match.group(1).strip()


def main() -> int:
    skill_path = ROOT / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    block = frontmatter(text)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    assert scalar(block, "name") == "article-html-to-ppt"
    assert scalar(block, "description")
    assert scalar(block, "version") == version
    assert "public_slug: \"meowclaw-pptsmith\"" in block
    assert "MODEL_AUTHORING_REQUIRED" in text
    assert "Bespoke" in text and "Template" in text and "Standard / Engineering" in text
    assert not re.search(r"(?i)TODO|TBD|replace me|placeholder description", block)
    print(f"skill validation passed: article-html-to-ppt {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
