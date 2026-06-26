#!/usr/bin/env python3
"""Save a dream record to ~/.openclaw/memory/dreams/"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DREAMS_DIR = Path.home() / ".openclaw" / "memory" / "dreams"
DREAMS_DIR.mkdir(parents=True, exist_ok=True)


def next_filename(date_str: str) -> Path:
    existing = sorted(DREAMS_DIR.glob(f"{date_str}-*.md"))
    idx = len(existing) + 1
    return DREAMS_DIR / f"{date_str}-{idx:03d}.md"


def save_dream(title: str, raw: str, structured: str, tags: list[str]) -> str:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    filepath = next_filename(date_str)

    tags_str = ", ".join(tags) if tags else ""
    content = f"""---
date: {now.strftime("%Y-%m-%d %H:%M")}
title: {title}
tags: [{tags_str}]
---

## 原始描述

{raw}

## 整理版本

{structured}
"""
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


if __name__ == "__main__":
    raw_bytes = sys.stdin.buffer.read()
    data = json.loads(raw_bytes.decode("utf-8"))
    path = save_dream(
        title=data.get("title", "无题梦境"),
        raw=data.get("raw", ""),
        structured=data.get("structured", ""),
        tags=data.get("tags", []),
    )
    sys.stdout.buffer.write(json.dumps({"saved": path}, ensure_ascii=False).encode("utf-8"))
