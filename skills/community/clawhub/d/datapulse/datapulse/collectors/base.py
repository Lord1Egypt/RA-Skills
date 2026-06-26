"""Shared parser base abstractions for DataPulse collectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from datapulse.core.models import SourceType
from datapulse.core.utils import generate_excerpt


@dataclass
class ParseResult:
    url: str
    title: str = ""
    content: str = ""
    author: str = ""
    excerpt: str = ""
    tags: list[str] = field(default_factory=list)
    success: bool = True
    error: str = ""
    media_type: str = "text"
    source_type: SourceType | None = None
    extra: dict = field(default_factory=dict)
    confidence_flags: list[str] = field(default_factory=list)

    @classmethod
    def failure(cls, url: str, error: str) -> "ParseResult":
        return cls(url=url, success=False, error=error)


class BaseCollector(ABC):
    name = "base"
    source_type = SourceType.GENERIC
    reliability = 0.62
    timeout = 30
    tier: int = 2  # 0=zero-config, 1=network/free, 2=needs setup
    setup_hint: str = ""

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, url: str) -> ParseResult:
        raise NotImplementedError

    def check(self) -> dict[str, str | bool]:
        """Health self-check. Subclasses override for real checks."""
        return {"status": "ok", "message": "no check implemented", "available": True}

    def _safe_excerpt(self, text: str) -> str:
        return generate_excerpt(text)
