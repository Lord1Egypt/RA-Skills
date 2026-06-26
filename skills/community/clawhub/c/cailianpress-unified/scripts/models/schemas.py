from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


@dataclass
class ClsItem:
    id: int | None
    title: str
    brief: str
    content: str
    level: str
    is_red: bool
    reading_num: int
    ctime: int | None
    published_at: str
    shareurl: str
    stock_list: list[dict[str, Any]] = field(default_factory=list)
    subjects: list[dict[str, Any]] = field(default_factory=list)
    plate_list: list[dict[str, Any]] = field(default_factory=list)
    raw_source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClsQueryResult:
    query_type: str
    count: int
    items: list[ClsItem]
    source_used: str
    fallback_used: bool
    generated_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_type": self.query_type,
            "count": self.count,
            "items": [item.to_dict() for item in self.items],
            "source_used": self.source_used,
            "fallback_used": self.fallback_used,
            "generated_at": self.generated_at,
        }


def normalize_published_at(ctime: int | None) -> str:
    if not ctime:
        return ""
    return datetime.fromtimestamp(int(ctime), SHANGHAI_TZ).strftime("%Y-%m-%d %H:%M:%S")


def is_red_level(level: str | None) -> bool:
    return str(level or "").upper() in {"A", "B"}
