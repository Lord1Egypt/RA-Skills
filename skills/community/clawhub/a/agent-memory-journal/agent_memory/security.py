from __future__ import annotations

import re
from pathlib import Path

ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\ufeff]")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
BLOCKLIST = [
    re.compile(r"ignore\s+previous\s+instructions", re.IGNORECASE),
    re.compile(r"^system:\s*", re.IGNORECASE),
    re.compile(r"^developer:\s*", re.IGNORECASE),
    re.compile(r"^assistant:\s*", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"reset\s+all\s+previous\s+instructions", re.IGNORECASE),
    re.compile(r"<\|system\|>", re.IGNORECASE),
    re.compile(r"```(?:bash|sh|shell)?", re.IGNORECASE),
]


def sanitize_text(text: str) -> str:
    cleaned = ZERO_WIDTH_RE.sub('', text)
    cleaned = CONTROL_RE.sub('', cleaned)
    return cleaned.strip()


def is_safe_memory_text(text: str) -> bool:
    cleaned = sanitize_text(text)
    if not cleaned:
        return False
    return not any(pattern.search(cleaned) for pattern in BLOCKLIST)


def require_safe_memory_text(text: str) -> str:
    cleaned = sanitize_text(text)
    if not cleaned:
        raise ValueError('empty memory text')
    for pattern in BLOCKLIST:
        if pattern.search(cleaned):
            raise ValueError(f"unsafe memory text: blocked by pattern {pattern.pattern}")
    return cleaned


def validate_hot_path(memory_root: str | Path, hot_path: str) -> Path:
    memory_root_path = Path(memory_root).expanduser().resolve()
    candidate = Path(hot_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (memory_root_path / candidate).resolve()

    allowed_roots = {
        memory_root_path,
        memory_root_path.parent,
    }
    if not any(root == resolved or root in resolved.parents for root in allowed_roots):
        raise ValueError(f"invalid hot_path outside allowed roots: {hot_path}")
    return resolved


def sanitize_evidence_text(text: str) -> str:
    # Episodic/session log, preserves prompt-injection text as evidence.
    # Only invisible/control characters are stripped here.
    cleaned = sanitize_text(text)
    if not cleaned:
        raise ValueError('empty memory text')
    return cleaned
