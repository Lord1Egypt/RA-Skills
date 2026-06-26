from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RecallResult:
    text: str
    path: str
    line_no: int
    score: float = 0.0
    tier: str = "cold"
    category: str | None = None
    refs: list[str] = field(default_factory=list)
    provenance: str | None = None
    status: str = "active"
    extra: dict[str, Any] = field(default_factory=dict)
