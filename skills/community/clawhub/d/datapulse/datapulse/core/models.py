"""Core data models for DataPulse."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, TypeVar

from .triage import normalize_review_state

EnumT = TypeVar("EnumT", bound=Enum)


class SourceType(str, Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    YOUTUBE = "youtube"
    BILIBILI = "bilibili"
    TELEGRAM = "telegram"
    WECHAT = "wechat"
    WEIBO = "weibo"
    XHS = "xhs"
    RSS = "rss"
    ARXIV = "arxiv"
    HACKERNEWS = "hackernews"
    TRENDING = "trending"
    GENERIC = "generic"
    MANUAL = "manual"


class SourceGovernanceClass(str, Enum):
    PUBLISHER = "publisher"
    PLATFORM = "platform"
    AGGREGATOR = "aggregator"
    ANALYST = "analyst"
    GENERIC = "generic"


class SourceCollectionMode(str, Enum):
    PUBLIC_WEB = "public_web"
    API = "api"
    SEARCH_GATEWAY = "search_gateway"
    MANUAL_FACT = "manual_fact"
    HYBRID = "hybrid"


class SourceAuthorityLevel(str, Enum):
    OFFICIAL = "official"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    COMMUNITY = "community"
    UNVERIFIED = "unverified"


class SourceSensitivity(str, Enum):
    PUBLIC = "public"
    REVIEW_REQUIRED = "review_required"
    ELEVATED = "elevated"


def _coerce_enum(enum_cls: type[EnumT], value: Any, default: EnumT) -> EnumT:
    if isinstance(value, enum_cls):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        try:
            return enum_cls(normalized)
        except ValueError:
            return default
    return default


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    seen: list[str] = []
    for item in value:
        text = str(item).strip()
        if text and text not in seen:
            seen.append(text)
    return seen


@dataclass
class SourceGovernance:
    source_class: SourceGovernanceClass = SourceGovernanceClass.GENERIC
    collection_mode: SourceCollectionMode = SourceCollectionMode.PUBLIC_WEB
    authority: SourceAuthorityLevel = SourceAuthorityLevel.SECONDARY
    sensitivity: SourceSensitivity = SourceSensitivity.PUBLIC
    compliance_hints: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.source_class = _coerce_enum(
            SourceGovernanceClass,
            self.source_class,
            SourceGovernanceClass.GENERIC,
        )
        self.collection_mode = _coerce_enum(
            SourceCollectionMode,
            self.collection_mode,
            SourceCollectionMode.PUBLIC_WEB,
        )
        self.authority = _coerce_enum(
            SourceAuthorityLevel,
            self.authority,
            SourceAuthorityLevel.SECONDARY,
        )
        self.sensitivity = _coerce_enum(
            SourceSensitivity,
            self.sensitivity,
            SourceSensitivity.PUBLIC,
        )
        self.compliance_hints = _normalize_string_list(self.compliance_hints)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_class": self.source_class.value,
            "collection_mode": self.collection_mode.value,
            "authority": self.authority.value,
            "sensitivity": self.sensitivity.value,
            "compliance_hints": list(self.compliance_hints),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "SourceGovernance":
        payload = data if isinstance(data, dict) else {}
        return cls(
            source_class=payload.get("source_class", SourceGovernanceClass.GENERIC.value),
            collection_mode=payload.get("collection_mode", SourceCollectionMode.PUBLIC_WEB.value),
            authority=payload.get("authority", SourceAuthorityLevel.SECONDARY.value),
            sensitivity=payload.get("sensitivity", SourceSensitivity.PUBLIC.value),
            compliance_hints=payload.get("compliance_hints", []),
        )


class MediaType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


@dataclass
class DataPulseItem:
    source_type: SourceType
    source_name: str
    title: str
    content: str
    url: str

    parser: str = ""
    id: str = ""
    fetched_at: str = ""
    media_type: MediaType = MediaType.TEXT

    score: int = 0
    confidence: float = 0.0
    confidence_factors: list[str] = field(default_factory=list)
    quality_rank: int = 0

    tags: list[str] = field(default_factory=list)
    language: str = "unknown"

    category: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    processed: bool = False
    review_state: str = "new"
    review_notes: list[dict[str, str]] = field(default_factory=list)
    review_actions: list[dict[str, str]] = field(default_factory=list)
    duplicate_of: Optional[str] = None
    digest_date: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.id:
            self.id = hashlib.md5(f"{self.url}:{self.title}".encode("utf-8")).hexdigest()[:12]
        if not self.fetched_at:
            self.fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        self.review_state = normalize_review_state(self.review_state, processed=self.processed)
        self.review_notes = [
            {str(k): str(v) for k, v in note.items()}
            for note in self.review_notes
            if isinstance(note, dict)
        ]
        self.review_actions = [
            {str(k): str(v) for k, v in action.items()}
            for action in self.review_actions
            if isinstance(action, dict)
        ]
        self.duplicate_of = str(self.duplicate_of or "").strip() or None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_type"] = self.source_type.value
        payload["media_type"] = self.media_type.value
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DataPulseItem":
        if isinstance(data.get("source_type"), str):
            data["source_type"] = SourceType(data["source_type"])
        if isinstance(data.get("media_type"), str):
            data["media_type"] = MediaType(data["media_type"])

        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})
