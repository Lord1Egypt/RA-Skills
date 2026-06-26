"""Story aggregation models, clustering, and storage for intelligence workspaces."""

from __future__ import annotations

import importlib
import json
import os
import re
import shlex
import subprocess
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .entities import normalize_entity_name
from .entity_store import EntityStore
from .models import DataPulseItem
from .semantic import build_semantic_review
from .triage import GROUNDING_BACKEND_KIND, build_item_governance, evidence_grade_priority
from .utils import content_fingerprint, generate_slug, get_domain, stories_path_from_env

FACTUALITY_BACKEND_REQUEST_SCHEMA_VERSION = "evidence_backend_request.v1"
FACTUALITY_BACKEND_RESULT_SCHEMA_VERSION = "evidence_backend_result.v1"
FACTUALITY_BACKEND_KIND = "openfactverification_class"
FACTUALITY_BACKEND_CMD_ENV = "DATAPULSE_FACTUALITY_BACKEND_CMD"
FACTUALITY_BACKEND_CALLABLE_ENV = "DATAPULSE_FACTUALITY_BACKEND_CALLABLE"
FACTUALITY_BACKEND_WORKDIR_ENV = "DATAPULSE_FACTUALITY_BACKEND_WORKDIR"
FACTUALITY_BACKEND_TIMEOUT_ENV = "DATAPULSE_FACTUALITY_BACKEND_TIMEOUT_SECONDS"
DEFAULT_FACTUALITY_BACKEND_TIMEOUT_SECONDS = 30
FACTUALITY_BACKEND_STATUSES = {
    "applied",
    "skipped",
    "fallback_used",
    "unavailable",
    "invalid",
}
FACTUALITY_GATE_STATUSES = {"empty", "ready", "review_required", "blocked"}
FACTUALITY_GATE_STATUS_PRIORITY = {
    "empty": 0,
    "ready": 1,
    "review_required": 2,
    "blocked": 3,
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_dt(value: str) -> datetime:
    text = str(value or "").strip()
    if not text:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[\w\-]{2,}", str(text or "").lower())
        if token
    }


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _entity_labels_for_item(item: DataPulseItem, *, entity_store: EntityStore | None = None) -> list[str]:
    rows: list[str] = []
    raw_entities = item.extra.get("entities")
    if isinstance(raw_entities, list):
        for raw in raw_entities:
            if isinstance(raw, dict):
                value = str(raw.get("display_name") or raw.get("name") or "").strip()
            elif isinstance(raw, str):
                value = raw.strip()
            else:
                continue
            if value:
                rows.append(value)

    if not rows and entity_store is not None:
        for entity in entity_store.query_by_source_item(item.id):
            value = str(entity.display_name or entity.name).strip()
            if value:
                rows.append(value)

    out: list[str] = []
    seen: set[str] = set()
    for raw in rows:
        normalized = normalize_entity_name(raw)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(raw)
    return out


@dataclass
class StoryEvidence:
    item_id: str
    title: str
    url: str
    source_name: str
    source_type: str
    score: int = 0
    confidence: float = 0.0
    fetched_at: str = ""
    review_state: str = "new"
    role: str = "secondary"
    entities: list[str] = field(default_factory=list)
    governance: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.item_id = str(self.item_id or "").strip()
        self.title = str(self.title or "").strip()
        self.url = str(self.url or "").strip()
        self.source_name = str(self.source_name or "").strip()
        self.source_type = str(self.source_type or "").strip()
        self.role = str(self.role or "secondary").strip().lower() or "secondary"
        self.review_state = str(self.review_state or "new").strip().lower() or "new"
        try:
            self.score = int(self.score)
        except Exception:
            self.score = 0
        try:
            self.confidence = max(0.0, min(1.0, float(self.confidence)))
        except Exception:
            self.confidence = 0.0
        self.entities = [str(entity).strip() for entity in self.entities if str(entity).strip()]
        self.governance = dict(self.governance or {})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StoryEvidence":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class StoryTimelineEvent:
    time: str
    item_id: str
    title: str
    source_name: str
    url: str
    role: str = "secondary"
    score: int = 0

    def __post_init__(self) -> None:
        self.time = str(self.time or "").strip()
        self.item_id = str(self.item_id or "").strip()
        self.title = str(self.title or "").strip()
        self.source_name = str(self.source_name or "").strip()
        self.url = str(self.url or "").strip()
        self.role = str(self.role or "secondary").strip().lower() or "secondary"
        try:
            self.score = int(self.score)
        except Exception:
            self.score = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StoryTimelineEvent":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class StoryConflict:
    topic: str
    positive: int = 0
    negative: int = 0
    neutral: int = 0
    note: str = ""

    def __post_init__(self) -> None:
        self.topic = str(self.topic or "").strip()
        self.note = str(self.note or "").strip()
        for field_name in ("positive", "negative", "neutral"):
            try:
                setattr(self, field_name, max(0, int(getattr(self, field_name))))
            except Exception:
                setattr(self, field_name, 0)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StoryConflict":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class Story:
    title: str
    summary: str = ""
    status: str = "active"
    score: float = 0.0
    confidence: float = 0.0
    item_count: int = 0
    source_count: int = 0
    primary_item_id: str = ""
    entities: list[str] = field(default_factory=list)
    source_names: list[str] = field(default_factory=list)
    primary_evidence: list[StoryEvidence] = field(default_factory=list)
    secondary_evidence: list[StoryEvidence] = field(default_factory=list)
    timeline: list[StoryTimelineEvent] = field(default_factory=list)
    contradictions: list[StoryConflict] = field(default_factory=list)
    semantic_review: dict[str, Any] = field(default_factory=dict)
    governance: dict[str, Any] = field(default_factory=dict)
    generated_at: str = ""
    updated_at: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        self.title = str(self.title or "").strip()
        if not self.title:
            raise ValueError("Story title is required")
        self.summary = str(self.summary or "").strip()
        self.status = str(self.status or "active").strip().lower() or "active"
        if not self.id:
            self.id = generate_slug(self.title, max_length=48)
        now = _utcnow()
        if not self.generated_at:
            self.generated_at = now
        if not self.updated_at:
            self.updated_at = self.generated_at
        try:
            self.score = round(float(self.score), 2)
        except Exception:
            self.score = 0.0
        try:
            self.confidence = round(max(0.0, min(1.0, float(self.confidence))), 4)
        except Exception:
            self.confidence = 0.0
        for field_name in ("item_count", "source_count"):
            try:
                setattr(self, field_name, max(0, int(getattr(self, field_name))))
            except Exception:
                setattr(self, field_name, 0)
        self.primary_item_id = str(self.primary_item_id or "").strip()
        self.entities = [str(entity).strip() for entity in self.entities if str(entity).strip()]
        self.source_names = [str(source).strip() for source in self.source_names if str(source).strip()]
        self.primary_evidence = [
            evidence if isinstance(evidence, StoryEvidence) else StoryEvidence.from_dict(evidence)
            for evidence in self.primary_evidence
            if isinstance(evidence, (StoryEvidence, dict))
        ]
        self.secondary_evidence = [
            evidence if isinstance(evidence, StoryEvidence) else StoryEvidence.from_dict(evidence)
            for evidence in self.secondary_evidence
            if isinstance(evidence, (StoryEvidence, dict))
        ]
        self.timeline = [
            event if isinstance(event, StoryTimelineEvent) else StoryTimelineEvent.from_dict(event)
            for event in self.timeline
            if isinstance(event, (StoryTimelineEvent, dict))
        ]
        self.contradictions = [
            conflict if isinstance(conflict, StoryConflict) else StoryConflict.from_dict(conflict)
            for conflict in self.contradictions
            if isinstance(conflict, (StoryConflict, dict))
        ]
        self.semantic_review = dict(self.semantic_review or {})
        self.governance = dict(self.governance or {})

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["primary_evidence"] = [evidence.to_dict() for evidence in self.primary_evidence]
        payload["secondary_evidence"] = [evidence.to_dict() for evidence in self.secondary_evidence]
        payload["timeline"] = [event.to_dict() for event in self.timeline]
        payload["contradictions"] = [conflict.to_dict() for conflict in self.contradictions]
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Story":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        payload = {k: v for k, v in data.items() if k in valid}
        payload["primary_evidence"] = [
            StoryEvidence.from_dict(row)
            for row in payload.get("primary_evidence", [])
            if isinstance(row, dict)
        ]
        payload["secondary_evidence"] = [
            StoryEvidence.from_dict(row)
            for row in payload.get("secondary_evidence", [])
            if isinstance(row, dict)
        ]
        payload["timeline"] = [
            StoryTimelineEvent.from_dict(row)
            for row in payload.get("timeline", [])
            if isinstance(row, dict)
        ]
        payload["contradictions"] = [
            StoryConflict.from_dict(row)
            for row in payload.get("contradictions", [])
            if isinstance(row, dict)
        ]
        return cls(**payload)


class StoryStore:
    """File-backed storage for persisted story aggregation snapshots."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or stories_path_from_env()).expanduser()
        self.version = 1
        self.stories: dict[str, Story] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.stories = {}
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.stories = {}
            return
        if isinstance(raw, dict):
            self.version = int(raw.get("version", 1) or 1)
            rows = raw.get("stories", [])
        elif isinstance(raw, list):
            rows = raw
        else:
            rows = []
        loaded: dict[str, Story] = {}
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, dict):
                continue
            try:
                story = Story.from_dict(row)
            except (TypeError, ValueError):
                continue
            loaded[story.id] = story
        self.stories = loaded

    def save(self) -> None:
        payload = {
            "version": self.version,
            "stories": [story.to_dict() for story in self.list_stories(limit=5000)],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _unique_id(base_id: str, existing: set[str]) -> str:
        candidate = (base_id or "story").strip() or "story"
        if candidate not in existing:
            return candidate
        suffix = 2
        while f"{candidate}-{suffix}" in existing:
            suffix += 1
        return f"{candidate}-{suffix}"

    def replace_stories(self, stories: list[Story]) -> list[Story]:
        normalized: dict[str, Story] = {}
        for story in stories:
            candidate = story if isinstance(story, Story) else Story.from_dict(story)
            candidate.id = self._unique_id(candidate.id, set(normalized))
            provenance = (
                candidate.governance.get("provenance", {})
                if isinstance(candidate.governance, dict)
                else {}
            )
            if isinstance(provenance, dict):
                provenance["story_id"] = candidate.id
            normalized[candidate.id] = candidate
        self.stories = normalized
        self.save()
        return self.list_stories(limit=len(normalized) or 20)

    def list_stories(self, *, limit: int = 20, min_items: int = 1) -> list[Story]:
        rows = [
            story for story in self.stories.values()
            if story.item_count >= max(0, int(min_items))
        ]
        rows.sort(
            key=lambda story: (
                story.score,
                story.confidence,
                story.source_count,
                story.updated_at,
                story.id,
            ),
            reverse=True,
        )
        return rows[: max(0, limit)]

    def get_story(self, identifier: str) -> Story | None:
        key = str(identifier or "").strip()
        if not key:
            return None
        story = self.stories.get(key)
        if story is not None:
            return story
        lowered = key.casefold()
        for candidate in self.stories.values():
            if candidate.title.casefold() == lowered:
                return candidate
        return None

    def create_story(self, payload: Story | dict[str, Any]) -> Story:
        candidate = payload if isinstance(payload, Story) else Story.from_dict(payload)
        candidate.id = self._unique_id(candidate.id, set(self.stories))
        provenance = (
            candidate.governance.get("provenance", {})
            if isinstance(candidate.governance, dict)
            else {}
        )
        if isinstance(provenance, dict):
            provenance["story_id"] = candidate.id
        self.stories[candidate.id] = candidate
        self.save()
        return candidate

    def update_story(
        self,
        identifier: str,
        *,
        title: str | None = None,
        summary: str | None = None,
        status: str | None = None,
    ) -> Story | None:
        story = self.get_story(identifier)
        if story is None:
            return None
        if title is not None:
            next_title = str(title or "").strip()
            if not next_title:
                raise ValueError("Story title cannot be empty")
            story.title = next_title
        if summary is not None:
            story.summary = str(summary or "").strip()
        if status is not None:
            next_status = str(status or "").strip().lower()
            if not next_status:
                raise ValueError("Story status cannot be empty")
            story.status = next_status
        story.updated_at = _utcnow()
        self.save()
        return story

    def delete_story(self, identifier: str) -> Story | None:
        story = self.get_story(identifier)
        if story is None:
            return None
        del self.stories[story.id]
        self.save()
        return story


def _descriptor_for_item(item: DataPulseItem, *, entity_store: EntityStore | None = None) -> dict[str, Any]:
    entity_labels = _entity_labels_for_item(item, entity_store=entity_store)
    return {
        "item": item,
        "fingerprint": content_fingerprint(item.content) if len(item.content) >= 50 else "",
        "title_tokens": _tokenize(item.title),
        "content_tokens": _tokenize(item.content[:1500]),
        "domain": get_domain(item.url),
        "entity_labels": entity_labels,
        "entity_keys": {normalize_entity_name(label) for label in entity_labels if normalize_entity_name(label)},
    }


def _cluster_similarity(descriptor: dict[str, Any], cluster: dict[str, Any]) -> float:
    if descriptor["fingerprint"] and descriptor["fingerprint"] in cluster["fingerprints"]:
        return 1.0
    title_overlap = _jaccard(descriptor["title_tokens"], cluster["title_tokens"])
    content_overlap = _jaccard(descriptor["content_tokens"], cluster["content_tokens"])
    entity_overlap = _jaccard(descriptor["entity_keys"], cluster["entity_keys"])
    same_domain = descriptor["domain"] == cluster["domain"] and descriptor["domain"] != "unknown"
    score = (0.45 * title_overlap) + (0.20 * content_overlap) + (0.25 * entity_overlap)
    if same_domain:
        score += 0.10
    if title_overlap >= 0.25 and entity_overlap >= 0.25:
        score += 0.08
    return round(min(score, 1.0), 4)


def _select_primary_count(item_count: int, evidence_limit: int) -> int:
    if evidence_limit <= 1:
        return 1
    if item_count >= 4:
        return min(2, evidence_limit)
    return 1


def _story_summary(title: str, *, item_count: int, source_count: int, entities: list[str], contradictions: int) -> str:
    lead = f"{item_count} signals across {source_count} sources around {title!r}"
    if entities:
        lead += f"; key entities: {', '.join(entities[:3])}"
    if contradictions:
        lead += f"; contradictions: {contradictions}"
    return lead


def _story_seed_summary(
    items: list[DataPulseItem],
    *,
    title: str,
    entities: list[str],
    contradictions: int,
) -> str:
    if not items:
        return _story_summary(title, item_count=0, source_count=0, entities=entities, contradictions=contradictions)
    if len(items) > 1:
        return _story_summary(
            title,
            item_count=len(items),
            source_count=len({item.source_name for item in items}),
            entities=entities,
            contradictions=contradictions,
        )
    first = items[0]
    review_notes = [
        str(note.get("note", "") or "").strip()
        for note in first.review_notes
        if isinstance(note, dict) and str(note.get("note", "") or "").strip()
    ]
    if review_notes:
        return review_notes[0]
    excerpt = re.sub(r"\s+", " ", str(first.content or "")).strip()
    if excerpt:
        return excerpt[:217].rstrip() + "..." if len(excerpt) > 220 else excerpt
    return _story_summary(
        title,
        item_count=1,
        source_count=1,
        entities=entities,
        contradictions=contradictions,
    )


def _max_risk_level(left: str, right: str) -> str:
    priority = {"none": 0, "low": 1, "medium": 2, "high": 3}
    return left if priority.get(left, 0) >= priority.get(right, 0) else right


def _normalize_string_list(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, list):
        return []
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = str(raw or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return normalized


def _coerce_nonnegative_int(value: Any, *, default: int = 0) -> int:
    try:
        return max(0, int(round(float(value))))
    except Exception:
        return default


def _normalize_factuality_backend_status(value: Any, *, default: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in FACTUALITY_BACKEND_STATUSES:
        return normalized
    return default


def _normalize_factuality_gate_status(value: Any, *, default: str = "review_required") -> str:
    normalized = str(value or "").strip().lower()
    if normalized in FACTUALITY_GATE_STATUSES:
        return normalized
    aliases = {
        "ok": "ready",
        "pass": "ready",
        "passed": "ready",
        "clear": "ready",
        "supported": "ready",
        "verified": "ready",
        "review": "review_required",
        "warning": "review_required",
        "warn": "review_required",
        "needs_review": "review_required",
        "needs-review": "review_required",
        "uncertain": "review_required",
        "caution": "review_required",
        "fail": "blocked",
        "failed": "blocked",
        "reject": "blocked",
        "rejected": "blocked",
    }
    normalized_default = str(default or "review_required").strip().lower() or "review_required"
    if normalized_default not in FACTUALITY_GATE_STATUSES:
        normalized_default = "review_required"
    return aliases.get(normalized, normalized_default)


def _normalize_backend_factuality_signal(raw: Any, *, index: int) -> dict[str, Any] | None:
    if isinstance(raw, str):
        detail = str(raw).strip()
        if not detail:
            return None
        return {
            "kind": f"backend_signal_{index}",
            "status": "noted",
            "detail": detail,
        }
    if not isinstance(raw, dict):
        return None
    kind = str(raw.get("kind", f"backend_signal_{index}") or f"backend_signal_{index}").strip()
    status = str(raw.get("status", "unknown") or "unknown").strip()
    detail = str(raw.get("detail", "") or raw.get("message", "") or raw.get("summary", "")).strip()
    if not detail:
        detail = json.dumps(raw, ensure_ascii=True, sort_keys=True)
    return {
        "kind": kind,
        "status": status,
        "detail": detail,
    }


def _normalize_backend_factuality_signals(values: Any) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    signals: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(values, start=1):
        signal = _normalize_backend_factuality_signal(raw, index=index)
        if signal is None:
            continue
        signature = (
            str(signal.get("kind", "")).strip(),
            str(signal.get("status", "")).strip(),
            str(signal.get("detail", "")).strip(),
        )
        if signature in seen:
            continue
        seen.add(signature)
        signals.append(signal)
    return signals


def _factuality_backend_callable_path() -> str:
    return str(os.getenv(FACTUALITY_BACKEND_CALLABLE_ENV, "") or "").strip()


def _factuality_backend_command() -> list[str]:
    raw = str(os.getenv(FACTUALITY_BACKEND_CMD_ENV, "") or "").strip()
    if not raw:
        return []
    return shlex.split(raw)


def _factuality_backend_workdir() -> str | None:
    raw = str(os.getenv(FACTUALITY_BACKEND_WORKDIR_ENV, "") or "").strip()
    if not raw:
        return None
    return str(Path(raw).expanduser())


def _factuality_backend_timeout_seconds() -> int:
    raw = str(os.getenv(FACTUALITY_BACKEND_TIMEOUT_ENV, "") or "").strip()
    if not raw:
        return DEFAULT_FACTUALITY_BACKEND_TIMEOUT_SECONDS
    try:
        return max(1, int(float(raw)))
    except ValueError:
        return DEFAULT_FACTUALITY_BACKEND_TIMEOUT_SECONDS


def _has_factuality_backend_configured() -> bool:
    return bool(_factuality_backend_callable_path() or _factuality_backend_command())


def _default_factuality_backend_name() -> str:
    callable_path = _factuality_backend_callable_path()
    if callable_path:
        target = callable_path.rsplit(":", 1)[-1]
        return target.rsplit(".", 1)[-1].strip()
    command = _factuality_backend_command()
    if not command:
        return ""
    for token in reversed(command):
        if str(token).startswith("-"):
            continue
        candidate = Path(str(token)).stem.strip()
        if candidate and candidate.lower() not in {"python", "python3", "uv"}:
            return candidate
    return Path(command[0]).stem.strip()


def _build_factuality_backend_review(
    *,
    status: str,
    deterministic_status: str,
    backend_status: str = "",
    transport: str = "",
    backend_name: str = "",
    backend_version: str = "",
    fallback_mode: str = "deterministic_gate",
    request_id: str = "",
    latency_ms: int = 0,
    used_output: bool = False,
    summary: str = "",
    reasons: list[str] | None = None,
    signals: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    error_code: str = "",
    error: str = "",
) -> dict[str, Any]:
    payload = {
        "status": _normalize_factuality_backend_status(status, default="skipped"),
        "backend_kind": FACTUALITY_BACKEND_KIND,
        "backend_name": str(backend_name or "").strip(),
        "transport": str(transport or "").strip(),
        "fallback_mode": str(fallback_mode or "").strip() or "deterministic_gate",
        "deterministic_status": _normalize_factuality_gate_status(deterministic_status, default="review_required"),
        "backend_status": _normalize_factuality_gate_status(
            backend_status or deterministic_status,
            default=_normalize_factuality_gate_status(deterministic_status, default="review_required"),
        ),
        "used_output": bool(used_output),
        "warnings": _normalize_string_list(warnings or []),
    }
    if backend_version:
        payload["backend_version"] = str(backend_version).strip()
    if request_id:
        payload["request_id"] = str(request_id).strip()
    if latency_ms > 0:
        payload["latency_ms"] = _coerce_nonnegative_int(latency_ms)
    if summary:
        payload["summary"] = str(summary).strip()
    normalized_reasons = _normalize_string_list(reasons or [])
    if normalized_reasons:
        payload["reasons"] = normalized_reasons
    normalized_signals = _normalize_backend_factuality_signals(signals or [])
    if normalized_signals:
        payload["signals"] = normalized_signals
    if error_code:
        payload["error_code"] = str(error_code).strip()
    if error:
        payload["error"] = str(error).strip()
    return payload


def _build_factuality_backend_request(
    *,
    subject: str,
    surface: str,
    evidence_rows: list[dict[str, Any]],
    source_names: list[str],
    deterministic_gate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": FACTUALITY_BACKEND_REQUEST_SCHEMA_VERSION,
        "surface": "factuality",
        "subject": subject,
        "backend_kind": FACTUALITY_BACKEND_KIND,
        "input": {
            "surface": surface,
            "source_names": list(source_names),
            "evidence_rows": evidence_rows,
        },
        "deterministic": {
            "status": deterministic_gate.get("status", "review_required"),
            "score": float(deterministic_gate.get("score", 0.0) or 0.0),
            "operator_action": deterministic_gate.get("operator_action", "review_before_delivery"),
            "summary": deterministic_gate.get("summary", ""),
            "counts": deterministic_gate.get("counts", {}),
            "reasons": deterministic_gate.get("reasons", []),
            "signals": deterministic_gate.get("signals", []),
        },
        "metadata": {
            "allow_fallback": True,
            "repo_surface": surface,
        },
    }


def _resolve_factuality_backend_callable(path: str) -> Any:
    module_name: str
    attr_name: str
    if ":" in path:
        module_name, attr_name = path.split(":", 1)
    else:
        module_name, _, attr_name = path.rpartition(".")
    module_name = module_name.strip()
    attr_name = attr_name.strip()
    if not module_name or not attr_name:
        raise ValueError(f"Invalid factuality backend callable path: {path}")
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def _call_factuality_backend(
    request_payload: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    deterministic_status = _normalize_factuality_gate_status(
        request_payload.get("deterministic", {}).get("status", "review_required")
        if isinstance(request_payload.get("deterministic"), dict)
        else "review_required",
        default="review_required",
    )
    callable_path = _factuality_backend_callable_path()
    if callable_path:
        backend_name = _default_factuality_backend_name()
        started = time.perf_counter()
        try:
            backend_callable = _resolve_factuality_backend_callable(callable_path)
            raw_result = backend_callable(request_payload)
        except Exception as exc:
            return None, _build_factuality_backend_review(
                status="unavailable",
                deterministic_status=deterministic_status,
                transport="in_process",
                backend_name=backend_name,
                latency_ms=_coerce_nonnegative_int((time.perf_counter() - started) * 1000.0),
                error_code="backend_unavailable",
                error=str(exc),
            )
        return (
            raw_result if isinstance(raw_result, dict) else None,
            _build_factuality_backend_review(
                status="invalid" if not isinstance(raw_result, dict) else "fallback_used",
                deterministic_status=deterministic_status,
                transport="in_process",
                backend_name=backend_name,
                latency_ms=_coerce_nonnegative_int((time.perf_counter() - started) * 1000.0),
                error_code="invalid_result" if not isinstance(raw_result, dict) else "",
                error=(
                    "factuality backend returned a non-JSON-object result"
                    if not isinstance(raw_result, dict)
                    else ""
                ),
            ),
        )

    command = _factuality_backend_command()
    backend_name = _default_factuality_backend_name()
    timeout_seconds = _factuality_backend_timeout_seconds()
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            input=json.dumps(request_payload, ensure_ascii=True),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            cwd=_factuality_backend_workdir(),
            env=dict(os.environ),
        )
    except subprocess.TimeoutExpired:
        return None, _build_factuality_backend_review(
            status="unavailable",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=_coerce_nonnegative_int((time.perf_counter() - started) * 1000.0),
            error_code="backend_timeout",
            error=f"factuality backend timed out after {timeout_seconds}s",
        )
    except OSError as exc:
        return None, _build_factuality_backend_review(
            status="unavailable",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=_coerce_nonnegative_int((time.perf_counter() - started) * 1000.0),
            error_code="backend_unavailable",
            error=str(exc),
        )

    latency_ms = _coerce_nonnegative_int((time.perf_counter() - started) * 1000.0)
    stderr = str(completed.stderr or "").strip()
    if completed.returncode != 0:
        tail = stderr.splitlines()[-1] if stderr else ""
        detail = f" ({tail})" if tail else ""
        return None, _build_factuality_backend_review(
            status="unavailable",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=latency_ms,
            error_code="backend_exited_nonzero",
            error=f"factuality backend exited with code {completed.returncode}{detail}",
        )

    stdout = str(completed.stdout or "").strip()
    if not stdout:
        return None, _build_factuality_backend_review(
            status="unavailable",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=latency_ms,
            error_code="backend_empty_stdout",
            error="factuality backend returned empty stdout",
        )
    try:
        raw_result = json.loads(stdout)
    except json.JSONDecodeError:
        return None, _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=latency_ms,
            error_code="invalid_json",
            error="factuality backend returned invalid JSON",
        )
    if not isinstance(raw_result, dict):
        return None, _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport="subprocess_json",
            backend_name=backend_name,
            latency_ms=latency_ms,
            error_code="invalid_result",
            error="factuality backend result must be a JSON object",
        )
    return raw_result, _build_factuality_backend_review(
        status="fallback_used",
        deterministic_status=deterministic_status,
        transport="subprocess_json",
        backend_name=backend_name,
        latency_ms=latency_ms,
    )


def _apply_factuality_backend(
    *,
    subject: str,
    surface: str,
    evidence_rows: list[dict[str, Any]],
    source_names: list[str],
    deterministic_gate: dict[str, Any],
) -> dict[str, Any]:
    request_payload = _build_factuality_backend_request(
        subject=subject,
        surface=surface,
        evidence_rows=evidence_rows,
        source_names=source_names,
        deterministic_gate=deterministic_gate,
    )
    raw_result, backend_review = _call_factuality_backend(request_payload)
    if raw_result is None:
        return backend_review

    deterministic_status = _normalize_factuality_gate_status(
        deterministic_gate.get("status", "review_required"),
        default="review_required",
    )
    schema_version = str(raw_result.get("schema_version", "") or "").strip()
    if schema_version != FACTUALITY_BACKEND_RESULT_SCHEMA_VERSION:
        return _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport=backend_review.get("transport", ""),
            backend_name=backend_review.get("backend_name", ""),
            latency_ms=backend_review.get("latency_ms", 0),
            error_code="invalid_schema",
            error=f"unexpected factuality backend schema {schema_version or 'missing'}",
        )

    if str(raw_result.get("surface", "") or "").strip().lower() != "factuality":
        return _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport=backend_review.get("transport", ""),
            backend_name=backend_review.get("backend_name", ""),
            latency_ms=backend_review.get("latency_ms", 0),
            error_code="invalid_surface",
            error="factuality backend returned a non-factuality payload",
        )

    if str(raw_result.get("backend_kind", FACTUALITY_BACKEND_KIND) or "").strip() != FACTUALITY_BACKEND_KIND:
        return _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport=backend_review.get("transport", ""),
            backend_name=backend_review.get("backend_name", ""),
            latency_ms=backend_review.get("latency_ms", 0),
            error_code="invalid_backend_kind",
            error="factuality backend returned an unexpected backend_kind",
        )

    provenance_payload = raw_result.get("provenance", {})
    if not isinstance(provenance_payload, dict):
        provenance_payload = {}
    fallback_payload = raw_result.get("fallback", {})
    if not isinstance(fallback_payload, dict):
        fallback_payload = {}
    fallback_mode = str(
        fallback_payload.get("baseline")
        or backend_review.get("fallback_mode")
        or "deterministic_gate"
    ).strip() or "deterministic_gate"

    warnings: list[str] = []
    for warning in backend_review.get("warnings", []) if isinstance(backend_review.get("warnings"), list) else []:
        text = str(warning or "").strip()
        if text and text not in warnings:
            warnings.append(text)
    for warning in provenance_payload.get("warnings", []) if isinstance(provenance_payload.get("warnings"), list) else []:
        text = str(warning or "").strip()
        if text and text not in warnings:
            warnings.append(text)

    if not bool(raw_result.get("ok")):
        return _build_factuality_backend_review(
            status=_normalize_factuality_backend_status(
                provenance_payload.get("status"),
                default=backend_review.get("status", "fallback_used"),
            ),
            deterministic_status=deterministic_status,
            transport=str(raw_result.get("transport") or backend_review.get("transport") or "").strip(),
            backend_name=str(provenance_payload.get("backend_name") or backend_review.get("backend_name") or "").strip(),
            backend_version=str(provenance_payload.get("backend_version") or "").strip(),
            fallback_mode=fallback_mode,
            request_id=str(provenance_payload.get("request_id") or "").strip(),
            latency_ms=_coerce_nonnegative_int(
                provenance_payload.get("latency_ms", backend_review.get("latency_ms", 0)),
            ),
            used_output=False,
            warnings=warnings,
            error_code=str(raw_result.get("error_code") or backend_review.get("error_code") or "").strip(),
            error=str(raw_result.get("error") or backend_review.get("error") or "").strip(),
        )

    result_payload = raw_result.get("result", {})
    if not isinstance(result_payload, dict):
        return _build_factuality_backend_review(
            status="invalid",
            deterministic_status=deterministic_status,
            transport=str(raw_result.get("transport") or backend_review.get("transport") or "").strip(),
            backend_name=str(provenance_payload.get("backend_name") or backend_review.get("backend_name") or "").strip(),
            fallback_mode=fallback_mode,
            latency_ms=_coerce_nonnegative_int(
                provenance_payload.get("latency_ms", backend_review.get("latency_ms", 0)),
            ),
            warnings=warnings,
            error_code="invalid_result",
            error="factuality backend result payload must be an object",
        )

    has_backend_status = any(key in result_payload for key in ("status", "backend_status", "review_status", "verdict"))
    backend_status = _normalize_factuality_gate_status(
        result_payload.get("status")
        or result_payload.get("backend_status")
        or result_payload.get("review_status")
        or result_payload.get("verdict")
        or deterministic_status,
        default=deterministic_status,
    )
    summary = str(
        result_payload.get("summary")
        or result_payload.get("detail")
        or result_payload.get("message")
        or provenance_payload.get("summary")
        or ""
    ).strip()
    reasons = _normalize_string_list(result_payload.get("reasons") or result_payload.get("notes"))
    signals = _normalize_backend_factuality_signals(result_payload.get("signals"))
    used_output = bool(has_backend_status or summary or reasons or signals)
    if not used_output:
        warnings = list(warnings)
        if "empty_backend_review" not in warnings:
            warnings.append("empty_backend_review")
        return _build_factuality_backend_review(
            status="fallback_used",
            deterministic_status=deterministic_status,
            transport=str(raw_result.get("transport") or backend_review.get("transport") or "").strip(),
            backend_name=str(provenance_payload.get("backend_name") or backend_review.get("backend_name") or "").strip(),
            backend_version=str(provenance_payload.get("backend_version") or "").strip(),
            fallback_mode=fallback_mode,
            request_id=str(provenance_payload.get("request_id") or "").strip(),
            latency_ms=_coerce_nonnegative_int(
                provenance_payload.get("latency_ms", backend_review.get("latency_ms", 0)),
            ),
            used_output=False,
            warnings=warnings,
            error_code=str(raw_result.get("error_code") or backend_review.get("error_code") or "").strip(),
            error=str(raw_result.get("error") or backend_review.get("error") or "").strip(),
        )

    return _build_factuality_backend_review(
        status=_normalize_factuality_backend_status(provenance_payload.get("status"), default="applied"),
        deterministic_status=deterministic_status,
        backend_status=backend_status,
        transport=str(raw_result.get("transport") or backend_review.get("transport") or "").strip(),
        backend_name=str(provenance_payload.get("backend_name") or backend_review.get("backend_name") or "").strip(),
        backend_version=str(provenance_payload.get("backend_version") or "").strip(),
        fallback_mode=fallback_mode,
        request_id=str(provenance_payload.get("request_id") or "").strip(),
        latency_ms=_coerce_nonnegative_int(
            provenance_payload.get("latency_ms", backend_review.get("latency_ms", 0)),
        ),
        used_output=True,
        summary=summary,
        reasons=reasons,
        signals=signals,
        warnings=warnings,
        error_code=str(raw_result.get("error_code") or backend_review.get("error_code") or "").strip(),
        error=str(raw_result.get("error") or backend_review.get("error") or "").strip(),
    )


def _build_deterministic_factuality_gate(
    *,
    subject: str,
    surface: str,
    evidence_rows: list[dict[str, Any]],
    source_names: list[str] | None = None,
    grounded_claim_count: int = 0,
    contradiction_count: int = 0,
) -> dict[str, Any]:
    normalized_rows: list[dict[str, Any]] = []
    for raw in evidence_rows:
        if not isinstance(raw, dict):
            continue
        normalized_rows.append(raw)

    resolved_sources = {
        str(name or "").strip()
        for name in source_names or []
        if str(name or "").strip()
    }
    if not resolved_sources:
        resolved_sources = {
            str(row.get("source_name", "") or "").strip()
            for row in normalized_rows
            if str(row.get("source_name", "") or "").strip()
        }

    signals: list[dict[str, Any]] = []
    reasons: list[str] = []
    if not normalized_rows:
        return {
            "subject": subject,
            "surface": surface,
            "status": "empty",
            "score": 0.0,
            "operator_action": "review_before_delivery",
            "summary": "No evidence rows were selected for factuality review.",
            "counts": {
                "evidence_count": 0,
                "source_count": 0,
                "grounded_claim_count": 0,
                "grounded_item_count": 0,
                "verified_evidence_count": 0,
                "working_evidence_count": 0,
                "low_confidence_count": 0,
                "contradiction_count": max(0, int(contradiction_count)),
            },
            "signals": [
                {
                    "kind": "selection",
                    "status": "empty",
                    "detail": "No evidence rows reached the factuality gate.",
                }
            ],
            "reasons": ["No evidence rows reached the factuality gate."],
        }

    evidence_scores = [
        max(0.0, min(1.0, float(row.get("evidence_score", 0.0) or 0.0)))
        for row in normalized_rows
    ]
    avg_evidence_score = sum(evidence_scores) / max(1, len(evidence_scores))
    verified_count = sum(
        1
        for row in normalized_rows
        if str(row.get("evidence_grade", "working")).strip().lower() == "verified"
    )
    working_count = sum(
        1
        for row in normalized_rows
        if str(row.get("evidence_grade", "working")).strip().lower() in {"working", "discarded"}
    )
    low_confidence_count = sum(
        1
        for row in normalized_rows
        if float(row.get("confidence", 0.0) or 0.0) < 0.55
    )
    grounded_item_count = sum(
        1
        for row in normalized_rows
        if int(row.get("grounded_claim_count", 0) or 0) > 0
    )
    resolved_grounded_claim_count = max(
        0,
        int(grounded_claim_count or 0)
        or sum(int(row.get("grounded_claim_count", 0) or 0) for row in normalized_rows),
    )
    resolved_contradiction_count = max(0, int(contradiction_count or 0))
    source_count = len(resolved_sources)

    signals.append(
        {
            "kind": "source_support",
            "status": "strong" if source_count >= 2 else "limited",
            "detail": (
                f"{source_count} independent source(s) back this delivery surface."
                if source_count
                else "No source names were resolved for this delivery surface."
            ),
        }
    )
    signals.append(
        {
            "kind": "claim_grounding",
            "status": "grounded" if resolved_grounded_claim_count > 0 else "missing",
            "detail": (
                f"{resolved_grounded_claim_count} grounded claim(s) across {grounded_item_count} evidence row(s)."
                if resolved_grounded_claim_count > 0
                else "No grounded claims are attached to the selected evidence rows."
            ),
        }
    )
    signals.append(
        {
            "kind": "evidence_maturity",
            "status": (
                "verified"
                if verified_count == len(normalized_rows)
                else "mixed"
                if working_count > 0
                else "reviewed"
            ),
            "detail": (
                f"{verified_count}/{len(normalized_rows)} evidence row(s) are verified;"
                f" {working_count} remain working-grade."
            ),
        }
    )
    signals.append(
        {
            "kind": "contradiction_scan",
            "status": "detected" if resolved_contradiction_count > 0 else "clear",
            "detail": (
                f"{resolved_contradiction_count} contradiction signal(s) remain unresolved."
                if resolved_contradiction_count > 0
                else "No contradiction signals were detected in the selected evidence."
            ),
        }
    )
    signals.append(
        {
            "kind": "confidence_floor",
            "status": "low" if low_confidence_count > 0 else "ok",
            "detail": (
                f"{low_confidence_count} evidence row(s) fall below the 0.55 confidence floor."
                if low_confidence_count > 0
                else "All selected evidence rows meet the default confidence floor."
            ),
        }
    )

    status = "ready"
    operator_action = "allow_delivery"
    if resolved_contradiction_count > 0:
        status = "blocked"
        operator_action = "review_before_delivery"
        reasons.append("Contradiction signals remain unresolved across the selected evidence.")
    if source_count <= 1:
        if status != "blocked":
            status = "review_required"
            operator_action = "review_before_delivery"
        reasons.append("Only one source currently backs this delivery surface.")
    if resolved_grounded_claim_count <= 0:
        if status != "blocked":
            status = "review_required"
            operator_action = "review_before_delivery"
        reasons.append("Grounded claims are missing from the selected delivery evidence.")
    if working_count > 0:
        if status != "blocked":
            status = "review_required"
            operator_action = "review_before_delivery"
        reasons.append("Working-grade evidence is still present in the selected delivery evidence.")
    if low_confidence_count > 0:
        if status != "blocked":
            status = "review_required"
            operator_action = "review_before_delivery"
        reasons.append("At least one selected evidence row is below the default confidence floor.")

    score = avg_evidence_score
    if source_count >= 2:
        score += 0.12
    elif source_count == 1:
        score -= 0.08
    if resolved_grounded_claim_count > 0:
        score += min(0.12, 0.03 * min(4, resolved_grounded_claim_count))
    else:
        score -= 0.08
    if working_count > 0:
        score -= min(0.18, 0.06 * working_count)
    if low_confidence_count > 0:
        score -= min(0.12, 0.04 * low_confidence_count)
    if resolved_contradiction_count > 0:
        score -= 0.3
    score = round(max(0.0, min(1.0, score)), 4)

    return {
        "subject": subject,
        "surface": surface,
        "status": status,
        "score": score,
        "operator_action": operator_action,
        "summary": (
            f"{len(normalized_rows)} evidence row(s), {source_count} source(s), "
            f"{resolved_grounded_claim_count} grounded claim(s), {resolved_contradiction_count} contradiction signal(s)."
        ),
        "counts": {
            "evidence_count": len(normalized_rows),
            "source_count": source_count,
            "grounded_claim_count": resolved_grounded_claim_count,
            "grounded_item_count": grounded_item_count,
            "verified_evidence_count": verified_count,
            "working_evidence_count": working_count,
            "low_confidence_count": low_confidence_count,
            "contradiction_count": resolved_contradiction_count,
        },
        "signals": signals,
        "reasons": reasons,
    }


def resolve_factuality_gate_status(factuality: dict[str, Any] | None) -> str:
    if not isinstance(factuality, dict):
        return "review_required"
    deterministic_status = _normalize_factuality_gate_status(
        factuality.get("status", "review_required"),
        default="review_required",
    )
    backend_review = factuality.get("backend_review", {})
    if not isinstance(backend_review, dict) or not bool(backend_review.get("used_output")):
        return deterministic_status
    backend_status = _normalize_factuality_gate_status(
        backend_review.get("backend_status", deterministic_status),
        default=deterministic_status,
    )
    if FACTUALITY_GATE_STATUS_PRIORITY.get(backend_status, 0) > FACTUALITY_GATE_STATUS_PRIORITY.get(deterministic_status, 0):
        return backend_status
    return deterministic_status


def resolve_factuality_operator_action(factuality: dict[str, Any] | None) -> str:
    return "allow_delivery" if resolve_factuality_gate_status(factuality) == "ready" else "review_before_delivery"


def _visible_factuality_backend_review(review: dict[str, Any]) -> bool:
    if not isinstance(review, dict) or not review:
        return False
    if str(review.get("status", "skipped") or "skipped").strip().lower() != "skipped":
        return True
    return bool(
        review.get("used_output")
        or review.get("summary")
        or review.get("reasons")
        or review.get("signals")
        or review.get("warnings")
        or review.get("error")
    )


def build_factuality_gate(
    *,
    subject: str,
    surface: str,
    evidence_rows: list[dict[str, Any]],
    source_names: list[str] | None = None,
    grounded_claim_count: int = 0,
    contradiction_count: int = 0,
) -> dict[str, Any]:
    deterministic_gate = _build_deterministic_factuality_gate(
        subject=subject,
        surface=surface,
        evidence_rows=evidence_rows,
        source_names=source_names,
        grounded_claim_count=grounded_claim_count,
        contradiction_count=contradiction_count,
    )
    payload = dict(deterministic_gate)
    if (
        _has_factuality_backend_configured()
        and str(deterministic_gate.get("status", "empty") or "empty").strip().lower() != "empty"
    ):
        normalized_rows = [row for row in evidence_rows if isinstance(row, dict)]
        resolved_sources = {
            str(name or "").strip()
            for name in source_names or []
            if str(name or "").strip()
        }
        if not resolved_sources:
            resolved_sources = {
                str(row.get("source_name", "") or "").strip()
                for row in normalized_rows
                if str(row.get("source_name", "") or "").strip()
            }
        payload["backend_review"] = _apply_factuality_backend(
            subject=subject,
            surface=surface,
            evidence_rows=normalized_rows,
            source_names=sorted(resolved_sources),
            deterministic_gate=deterministic_gate,
        )
    payload["effective_status"] = resolve_factuality_gate_status(payload)
    payload["effective_operator_action"] = resolve_factuality_operator_action(payload)
    return payload


def _aggregate_story_evidence_grade(governances: list[dict[str, Any]]) -> str:
    if not governances:
        return "working"
    ranks = [evidence_grade_priority(row.get("evidence_grade")) for row in governances]
    if ranks and min(ranks) >= evidence_grade_priority("verified"):
        return "verified"
    if ranks and min(ranks) >= evidence_grade_priority("reviewed"):
        return "reviewed"
    return "working"


def _build_story_grounding_backend(evidence_rows: list[StoryEvidence]) -> dict[str, Any]:
    backend_rows: list[dict[str, Any]] = []
    statuses: list[str] = []
    warnings: list[str] = []
    applied_claim_count = 0

    for evidence in evidence_rows:
        governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
        backend = grounding.get("backend", {}) if isinstance(grounding.get("backend"), dict) else {}
        if not backend:
            continue
        entry = dict(backend)
        entry["item_id"] = evidence.item_id
        entry["role"] = evidence.role
        entry["source_name"] = evidence.source_name
        entry["title"] = evidence.title
        status = str(entry.get("status", "skipped") or "skipped").strip().lower() or "skipped"
        statuses.append(status)
        try:
            applied_claim_count += max(0, int(entry.get("applied_claim_count", 0) or 0))
        except Exception:
            applied_claim_count += 0
        for warning in entry.get("warnings", []) if isinstance(entry.get("warnings"), list) else []:
            text = str(warning or "").strip()
            if text and text not in warnings:
                warnings.append(text)
        backend_rows.append(entry)

    if not backend_rows:
        return {}

    summary_status = "skipped"
    if any(status == "applied" for status in statuses):
        summary_status = "applied"
    elif any(status == "invalid" for status in statuses):
        summary_status = "invalid"
    elif any(status == "unavailable" for status in statuses):
        summary_status = "unavailable"
    elif any(status == "fallback_used" for status in statuses):
        summary_status = "fallback_used"

    return {
        "status": summary_status,
        "backend_kind": next(
            (
                str(row.get("backend_kind", "") or "").strip()
                for row in backend_rows
                if str(row.get("backend_kind", "") or "").strip()
            ),
            GROUNDING_BACKEND_KIND,
        ),
        "attempted_item_count": len(
            {
                str(row.get("item_id", "") or "").strip()
                for row in backend_rows
                if row.get("item_id")
                and str(row.get("status", "skipped") or "skipped").strip().lower() != "skipped"
            }
        ),
        "applied_item_count": sum(
            1
            for row in backend_rows
            if str(row.get("status", "skipped") or "skipped").strip().lower() == "applied"
        ),
        "applied_claim_count": applied_claim_count,
        "warnings": warnings,
        "items": backend_rows,
    }


def _build_story_grounding(story_id: str, evidence_rows: list[StoryEvidence]) -> dict[str, Any]:
    claims: list[dict[str, Any]] = []
    grounded_items: set[str] = set()
    seen_claims: set[tuple[str, str]] = set()
    primary_claim_count = 0
    evidence_span_count = 0
    backend_summary = _build_story_grounding_backend(evidence_rows)

    for evidence in evidence_rows:
        governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
        raw_claims = grounding.get("claims", []) if isinstance(grounding.get("claims"), list) else []
        if not raw_claims:
            continue
        evidence_claim_added = False
        for raw_claim in raw_claims:
            if not isinstance(raw_claim, dict):
                continue
            text = str(raw_claim.get("text", "") or "").strip()
            if not text:
                continue
            claim_key = (evidence.item_id, text.casefold())
            if claim_key in seen_claims:
                continue
            seen_claims.add(claim_key)

            claim_id = f"{story_id}:{evidence.item_id}:claim:{len(claims) + 1}"
            source_link = dict(raw_claim.get("source_link", {})) if isinstance(raw_claim.get("source_link"), dict) else {}
            source_link.setdefault("item_id", evidence.item_id)
            source_link.setdefault("title", evidence.title)
            source_link.setdefault("url", evidence.url)
            source_link.setdefault("source_name", evidence.source_name)
            source_link.setdefault("source_type", evidence.source_type)
            source_link["story_id"] = story_id

            spans: list[dict[str, Any]] = []
            for span_index, raw_span in enumerate(raw_claim.get("evidence_spans", []), start=1):
                if not isinstance(raw_span, dict):
                    continue
                span = dict(raw_span)
                span.setdefault("span_id", f"{claim_id}:span:{span_index}")
                span.setdefault("item_id", evidence.item_id)
                span.setdefault("url", evidence.url)
                spans.append(span)
            evidence_span_count += len(spans)

            claims.append(
                {
                    "claim_id": claim_id,
                    "origin_claim_id": str(raw_claim.get("claim_id", "") or "").strip(),
                    "text": text,
                    "role": evidence.role,
                    "source_link": source_link,
                    "evidence_spans": spans,
                }
            )
            evidence_claim_added = True
            if evidence.role == "primary":
                primary_claim_count += 1
        if evidence_claim_added:
            grounded_items.add(evidence.item_id)

    payload: dict[str, Any] = {
        "mode": "projected" if claims else "empty",
        "grounded_item_count": len(grounded_items),
        "claim_count": len(claims),
        "primary_claim_count": primary_claim_count,
        "evidence_span_count": evidence_span_count,
        "claims": claims,
    }
    if backend_summary:
        payload["backend"] = backend_summary
    return payload


def _build_story_governance(
    *,
    story_id: str,
    primary_item_id: str,
    source_names: list[str],
    evidence_rows: list[StoryEvidence],
    contradictions: list[StoryConflict],
    generated_at: str,
) -> dict[str, Any]:
    primary_governances = [
        dict(evidence.governance)
        for evidence in evidence_rows
        if evidence.role == "primary" and isinstance(evidence.governance, dict)
    ]
    all_governances = [
        dict(evidence.governance)
        for evidence in evidence_rows
        if isinstance(evidence.governance, dict)
    ]
    aggregated = primary_governances or all_governances
    evidence_grade = _aggregate_story_evidence_grade(aggregated)
    evidence_score = round(
        sum(float(row.get("evidence_score", 0.0) or 0.0) for row in aggregated) / max(1, len(aggregated)),
        4,
    )
    story_grounding = _build_story_grounding(story_id, evidence_rows)
    factuality_rows: list[dict[str, Any]] = []
    for evidence in evidence_rows:
        governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        factuality_rows.append(
            {
                "item_id": evidence.item_id,
                "title": evidence.title,
                "source_name": evidence.source_name,
                "evidence_grade": str(governance.get("evidence_grade", "working")).strip().lower() or "working",
                "evidence_score": float(governance.get("evidence_score", 0.0) or 0.0),
                "review_state": str(governance.get("review_state") or evidence.review_state).strip().lower() or "new",
                "confidence": evidence.confidence,
                "grounded_claim_count": int(
                    (
                        governance.get("grounding", {})
                        if isinstance(governance.get("grounding"), dict)
                        else {}
                    ).get("claim_count", 0) or 0
                ),
            }
        )
    factuality = build_factuality_gate(
        subject="story",
        surface="story_export",
        evidence_rows=factuality_rows,
        source_names=source_names,
        grounded_claim_count=int(story_grounding.get("claim_count", 0) or 0),
        contradiction_count=len(contradictions),
    )

    delivery_status = "ready"
    delivery_level = "low"
    delivery_reasons: list[str] = []
    effective_factuality_status = resolve_factuality_gate_status(factuality)

    if contradictions:
        delivery_status = "review_required"
        delivery_level = "high"
        delivery_reasons.append("Story contains unresolved contradiction signals.")
    if any(str(row.get("evidence_grade", "working")).strip().lower() == "working" for row in aggregated):
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("Primary story evidence still includes working-grade signals.")
    if len(source_names) <= 1:
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("Story is currently backed by a single source.")
    if effective_factuality_status == "blocked":
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "high")
        delivery_reasons.append("Factuality gate blocked outward-facing story delivery pending analyst review.")
    elif effective_factuality_status != "ready":
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("Factuality gate requires analyst review before outward-facing story delivery.")

    provenance_chain: list[dict[str, Any]] = []
    review_states: dict[str, int] = {}
    for evidence in evidence_rows:
        governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        provenance = governance.get("provenance", {}) if isinstance(governance.get("provenance"), dict) else {}
        grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
        review_state = str(governance.get("review_state") or evidence.review_state).strip().lower() or "new"
        review_states[review_state] = review_states.get(review_state, 0) + 1
        provenance_chain.append(
            {
                "item_id": evidence.item_id,
                "role": evidence.role,
                "title": evidence.title,
                "source_name": evidence.source_name,
                "source_type": evidence.source_type,
                "review_state": review_state,
                "evidence_grade": str(governance.get("evidence_grade", "working")).strip().lower() or "working",
                "url": evidence.url,
                "fetched_at": provenance.get("fetched_at", evidence.fetched_at),
                "grounded_claim_count": int(grounding.get("claim_count", 0) or 0),
                "grounded_evidence_span_count": int(grounding.get("evidence_span_count", 0) or 0),
            }
        )

    return {
        "subject": "story",
        "evidence_grade": evidence_grade,
        "evidence_score": evidence_score,
        "grounding": story_grounding,
        "factuality": factuality,
        "provenance": {
            "kind": "story",
            "story_id": story_id,
            "primary_item_id": primary_item_id,
            "item_ids": [row["item_id"] for row in provenance_chain if row.get("item_id")],
            "source_names": list(source_names),
            "review_states": review_states,
            "evidence_chain": provenance_chain,
            "grounded_claim_count": int(story_grounding.get("claim_count", 0) or 0),
            "grounded_evidence_span_count": int(story_grounding.get("evidence_span_count", 0) or 0),
            "generated_at": generated_at,
        },
        "delivery_risk": {
            "surface": "story_package",
            "status": delivery_status,
            "level": delivery_level,
            "reasons": delivery_reasons,
            "route_observations": [],
        },
    }


def render_story_markdown(story: Story) -> str:
    governance = story.governance if isinstance(story.governance, dict) else {}
    delivery_risk = governance.get("delivery_risk", {}) if isinstance(governance.get("delivery_risk"), dict) else {}
    provenance = governance.get("provenance", {}) if isinstance(governance.get("provenance"), dict) else {}
    grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
    grounding_backend = grounding.get("backend", {}) if isinstance(grounding.get("backend"), dict) else {}
    factuality = governance.get("factuality", {}) if isinstance(governance.get("factuality"), dict) else {}
    factuality_backend = (
        factuality.get("backend_review", {})
        if isinstance(factuality.get("backend_review"), dict)
        else {}
    )
    effective_factuality_status = resolve_factuality_gate_status(factuality)
    effective_factuality_action = resolve_factuality_operator_action(factuality)
    lines = [
        f"# {story.title}",
        "",
        f"- story_id: {story.id}",
        f"- status: {story.status}",
        f"- item_count: {story.item_count}",
        f"- source_count: {story.source_count}",
        f"- score: {story.score}",
        f"- confidence: {story.confidence:.3f}",
        f"- evidence_grade: {governance.get('evidence_grade', 'working')}",
        f"- factuality_status: {factuality.get('status', 'review_required')}",
        f"- factuality_score: {float(factuality.get('score', 0.0) or 0.0):.3f}",
        f"- delivery_status: {delivery_risk.get('status', 'review_required')}",
        f"- delivery_risk: {delivery_risk.get('level', 'medium')}",
        f"- generated_at: {story.generated_at}",
        "",
        story.summary,
        "",
        "## Governance",
        f"- primary_item_id: {provenance.get('primary_item_id', story.primary_item_id)}",
        f"- evidence_items: {len(provenance.get('item_ids', [])) if isinstance(provenance.get('item_ids'), list) else 0}",
        f"- sources: {', '.join(provenance.get('source_names', story.source_names)) if isinstance(provenance.get('source_names'), list) else ', '.join(story.source_names)}",
        f"- grounded_claims: {int(grounding.get('claim_count', 0) or 0)}",
        f"- grounded_evidence_spans: {int(grounding.get('evidence_span_count', 0) or 0)}",
    ]
    show_grounding_backend = bool(grounding_backend) and (
        str(grounding_backend.get("status", "skipped") or "skipped").strip().lower() != "skipped"
        or int(grounding_backend.get("applied_item_count", 0) or 0) > 0
        or bool(grounding_backend.get("warnings", []))
    )
    if show_grounding_backend:
        lines.append(f"- grounding_backend_status: {grounding_backend.get('status', 'skipped')}")
        lines.append(f"- grounding_backend_applied_items: {int(grounding_backend.get('applied_item_count', 0) or 0)}")
    if effective_factuality_status != str(factuality.get("status", "review_required") or "review_required").strip().lower():
        lines.append(f"- factuality_effective_status: {effective_factuality_status}")
    if _visible_factuality_backend_review(factuality_backend):
        lines.append(f"- factuality_backend_status: {factuality_backend.get('status', 'skipped')}")
        lines.append(f"- factuality_backend_verdict: {factuality_backend.get('backend_status', effective_factuality_status)}")
    for reason in delivery_risk.get("reasons", []) if isinstance(delivery_risk.get("reasons"), list) else []:
        lines.append(f"- delivery_note: {reason}")

    lines.extend(["", "## Factuality Gate"])
    lines.append(f"- action: {factuality.get('operator_action', 'review_before_delivery')}")
    lines.append(f"- summary: {factuality.get('summary', 'No factuality summary recorded.')}")
    if effective_factuality_action != str(factuality.get("operator_action", "review_before_delivery") or "review_before_delivery").strip():
        lines.append(f"- effective_action: {effective_factuality_action}")
    for reason in factuality.get("reasons", []) if isinstance(factuality.get("reasons"), list) else []:
        lines.append(f"- factuality_note: {reason}")
    for signal in factuality.get("signals", []) if isinstance(factuality.get("signals"), list) else []:
        if not isinstance(signal, dict):
            continue
        lines.append(
            f"- factuality_signal: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}"
        )
    if _visible_factuality_backend_review(factuality_backend):
        lines.append(
            f"- factuality_backend_review: {factuality_backend.get('status', 'skipped')} | "
            f"verdict={factuality_backend.get('backend_status', effective_factuality_status)}"
        )
        if factuality_backend.get("summary"):
            lines.append(f"- factuality_backend_summary: {factuality_backend.get('summary', '')}")
        for reason in factuality_backend.get("reasons", []) if isinstance(factuality_backend.get("reasons"), list) else []:
            lines.append(f"- factuality_backend_note: {reason}")
        for signal in factuality_backend.get("signals", []) if isinstance(factuality_backend.get("signals"), list) else []:
            if not isinstance(signal, dict):
                continue
            lines.append(
                f"- factuality_backend_signal: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}"
            )
        for warning in factuality_backend.get("warnings", []) if isinstance(factuality_backend.get("warnings"), list) else []:
            lines.append(f"- factuality_backend_warning: {warning}")
        if factuality_backend.get("error"):
            lines.append(f"- factuality_backend_error: {factuality_backend.get('error', '')}")

    lines.extend([
        "",
        "## Entities",
    ])
    for entity in story.entities:
        lines.append(f"- {entity}")
    if not story.entities:
        lines.append("- none")

    lines.extend(["", "## Grounded Claims"])
    claim_rows = grounding.get("claims", []) if isinstance(grounding.get("claims"), list) else []
    for claim in claim_rows:
        if not isinstance(claim, dict):
            continue
        source_link = claim.get("source_link", {}) if isinstance(claim.get("source_link"), dict) else {}
        span_bits: list[str] = []
        for span in claim.get("evidence_spans", []) if isinstance(claim.get("evidence_spans"), list) else []:
            if not isinstance(span, dict):
                continue
            field = str(span.get("field", "content") or "content").strip()
            start = span.get("start")
            end = span.get("end")
            locator = f"{field}[{start}:{end}]" if isinstance(start, int) and isinstance(end, int) else field
            excerpt = str(span.get("text", "") or "").strip()
            span_bits.append(f"{locator} {excerpt!r}".strip())
        lines.append(
            f"- {str(claim.get('text', '') or '').strip()} | "
            f"source={source_link.get('source_name', '')}:{source_link.get('item_id', '')} | "
            f"evidence={'; '.join(span_bits) if span_bits else 'none'}"
        )
    if not claim_rows:
        lines.append("- none")

    lines.extend(["", "## Primary Evidence"])
    for evidence in story.primary_evidence:
        evidence_governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        evidence_grounding = (
            evidence_governance.get("grounding", {})
            if isinstance(evidence_governance.get("grounding"), dict)
            else {}
        )
        lines.append(
            f"- [{evidence.title}]({evidence.url}) | {evidence.source_name} | "
            f"score={evidence.score} confidence={evidence.confidence:.3f} state={evidence.review_state} "
            f"grade={evidence_governance.get('evidence_grade', 'working')} "
            f"grounded_claims={int(evidence_grounding.get('claim_count', 0) or 0)} "
            f"spans={int(evidence_grounding.get('evidence_span_count', 0) or 0)}"
        )
    if not story.primary_evidence:
        lines.append("- none")

    lines.extend(["", "## Secondary Evidence"])
    for evidence in story.secondary_evidence:
        evidence_governance = evidence.governance if isinstance(evidence.governance, dict) else {}
        evidence_grounding = (
            evidence_governance.get("grounding", {})
            if isinstance(evidence_governance.get("grounding"), dict)
            else {}
        )
        lines.append(
            f"- [{evidence.title}]({evidence.url}) | {evidence.source_name} | "
            f"score={evidence.score} confidence={evidence.confidence:.3f} state={evidence.review_state} "
            f"grade={evidence_governance.get('evidence_grade', 'working')} "
            f"grounded_claims={int(evidence_grounding.get('claim_count', 0) or 0)} "
            f"spans={int(evidence_grounding.get('evidence_span_count', 0) or 0)}"
        )
    if not story.secondary_evidence:
        lines.append("- none")

    lines.extend(["", "## Contradictions"])
    for conflict in story.contradictions:
        lines.append(
            f"- {conflict.topic}: positive={conflict.positive} negative={conflict.negative} neutral={conflict.neutral}"
        )
    if not story.contradictions:
        lines.append("- none")

    lines.extend(["", "## Timeline"])
    for event in story.timeline:
        lines.append(f"- {event.time} | [{event.title}]({event.url}) | {event.source_name} | role={event.role}")
    if not story.timeline:
        lines.append("- none")

    return "\n".join(lines)


def _story_item_ids(story: Story) -> list[str]:
    rows: list[str] = []
    if story.primary_item_id:
        rows.append(story.primary_item_id)
    for evidence in [*story.primary_evidence, *story.secondary_evidence]:
        if evidence.item_id:
            rows.append(evidence.item_id)
    for event in story.timeline:
        if event.item_id:
            rows.append(event.item_id)
    return list(dict.fromkeys(rows))


def build_story_graph(
    story: Story,
    *,
    entity_store: EntityStore | None = None,
    entity_limit: int = 12,
    relation_limit: int = 24,
) -> dict[str, Any]:
    entity_limit = max(0, int(entity_limit))
    relation_limit = max(0, int(relation_limit))
    story_item_ids = set(_story_item_ids(story))

    entity_rows: list[dict[str, Any]] = []
    seen_entities: set[str] = set()
    for raw_label in story.entities:
        normalized = normalize_entity_name(raw_label)
        if not normalized or normalized in seen_entities:
            continue
        seen_entities.add(normalized)
        entity = entity_store.get_entity(raw_label) if entity_store is not None else None
        source_item_ids = set(entity.source_item_ids) if entity is not None else set()
        in_story_source_ids = sorted(story_item_ids & source_item_ids)
        entity_rows.append(
            {
                "id": f"entity:{normalized.lower()}",
                "entity_key": normalized,
                "label": entity.display_name if entity is not None else raw_label,
                "kind": "entity",
                "entity_type": entity.entity_type.value if entity is not None else "UNKNOWN",
                "source_count": len(source_item_ids),
                "mention_count": entity.mention_count if entity is not None else 0,
                "in_story_source_count": len(in_story_source_ids),
                "in_story_source_ids": in_story_source_ids,
            }
        )

    entity_rows.sort(
        key=lambda row: (
            row["in_story_source_count"],
            row["source_count"],
            row["mention_count"],
            row["label"],
        ),
        reverse=True,
    )
    selected_entities = entity_rows[:entity_limit]
    selected_keys = {row["entity_key"] for row in selected_entities}

    nodes: list[dict[str, Any]] = [
        {
            "id": story.id,
            "label": story.title,
            "kind": "story",
            "status": story.status,
            "item_count": story.item_count,
            "source_count": story.source_count,
            "focus": True,
        }
    ]
    for row in selected_entities:
        nodes.append({key: value for key, value in row.items() if key != "entity_key"})

    mention_edges: list[dict[str, Any]] = []
    for row in selected_entities:
        mention_edges.append(
            {
                "id": f"{story.id}->{row['id']}",
                "source": story.id,
                "target": row["id"],
                "kind": "story_entity",
                "relation_type": "MENTIONED_IN_STORY",
                "weight": max(1.0, float(row["in_story_source_count"] or row["source_count"] or 1)),
                "source_item_count": row["in_story_source_count"] or row["source_count"] or 1,
                "keywords": [],
            }
        )

    relation_edges: list[dict[str, Any]] = []
    if entity_store is not None and selected_keys:
        seen_relations: set[tuple[str, str, str]] = set()
        for relation in entity_store.relations:
            if relation.source_entity not in selected_keys or relation.target_entity not in selected_keys:
                continue
            relation_source_ids = {item_id for item_id in relation.source_item_ids if item_id}
            if relation_source_ids and story_item_ids and not (relation_source_ids & story_item_ids):
                continue
            relation_key = (relation.source_entity, relation.target_entity, relation.relation_type)
            if relation_key in seen_relations:
                continue
            seen_relations.add(relation_key)
            overlap_ids = sorted(story_item_ids & relation_source_ids) if relation_source_ids else []
            relation_edges.append(
                {
                    "id": f"rel:{relation.source_entity}:{relation.target_entity}:{relation.relation_type}",
                    "source": f"entity:{relation.source_entity.lower()}",
                    "target": f"entity:{relation.target_entity.lower()}",
                    "kind": "entity_relation",
                    "relation_type": relation.relation_type,
                    "weight": float(relation.weight or 1.0),
                    "source_item_count": len(overlap_ids) or len(relation_source_ids),
                    "source_item_ids": overlap_ids or sorted(relation_source_ids),
                    "keywords": list(relation.keywords),
                }
            )

    relation_edges.sort(
        key=lambda edge: (
            edge["source_item_count"],
            edge["weight"],
            edge["relation_type"],
            edge["id"],
        ),
        reverse=True,
    )
    relation_edges = relation_edges[:relation_limit]
    edges = [*mention_edges, *relation_edges]

    return {
        "story": {
            "id": story.id,
            "title": story.title,
            "status": story.status,
            "item_count": story.item_count,
            "source_count": story.source_count,
        },
        "nodes": nodes,
        "edges": edges,
        "entity_count": len(selected_entities),
        "edge_count": len(edges),
        "relation_count": len(relation_edges),
    }


def build_story_from_items(
    items: list[DataPulseItem],
    *,
    title: str | None = None,
    summary: str | None = None,
    status: str | None = None,
    entity_store: EntityStore | None = None,
    evidence_limit: int = 4,
) -> Story:
    normalized_items = [item for item in items if isinstance(item, DataPulseItem)]
    if not normalized_items:
        raise ValueError("At least one item is required to build a story")

    descriptors = [_descriptor_for_item(item, entity_store=entity_store) for item in normalized_items]
    evidence_limit_safe = max(1, int(evidence_limit))
    primary_count = _select_primary_count(len(normalized_items), evidence_limit_safe)

    entity_counter: Counter[str] = Counter()
    entity_display: dict[str, str] = {}
    for row in descriptors:
        for label in row["entity_labels"]:
            normalized = normalize_entity_name(label)
            if not normalized:
                continue
            entity_counter[normalized] += 1
            entity_display[normalized] = label
    entities = [entity_display[key] for key, _ in entity_counter.most_common(6)]

    evidence_rows: list[StoryEvidence] = []
    for index, row in enumerate(descriptors[:evidence_limit_safe]):
        item = row["item"]
        role = "primary" if index < primary_count else "secondary"
        evidence_rows.append(
            StoryEvidence(
                item_id=item.id,
                title=item.title,
                url=item.url,
                source_name=item.source_name,
                source_type=item.source_type.value,
                score=item.score,
                confidence=item.confidence,
                fetched_at=item.fetched_at,
                review_state=item.review_state,
                role=role,
                entities=row["entity_labels"],
                governance=build_item_governance(item),
            )
        )

    primary_evidence = [row for row in evidence_rows if row.role == "primary"]
    secondary_evidence = [row for row in evidence_rows if row.role == "secondary"]
    primary_item_id = primary_evidence[0].item_id if primary_evidence else normalized_items[0].id
    timeline_rows = sorted(
        descriptors,
        key=lambda row: (_parse_dt(row["item"].extra.get("date_published", row["item"].fetched_at)), row["item"].id),
    )
    timeline = [
        StoryTimelineEvent(
            time=str(item.extra.get("date_published") or item.fetched_at),
            item_id=item.id,
            title=item.title,
            source_name=item.source_name,
            url=item.url,
            role="primary" if item.id == primary_item_id else "secondary",
            score=item.score,
        )
        for item in [row["item"] for row in timeline_rows]
    ]

    semantic_review = build_semantic_review(normalized_items)
    contradictions = [
        StoryConflict(
            topic=str(row.get("topic", "")),
            positive=int(row.get("positive", 0) or 0),
            negative=int(row.get("negative", 0) or 0),
            neutral=int(row.get("neutral", 0) or 0),
            note="semantic contradiction hint",
        )
        for row in semantic_review.get("contradictions", [])
        if isinstance(row, dict)
    ]
    source_names = sorted({item.source_name for item in normalized_items})
    top_slice = normalized_items[: min(3, len(normalized_items))]
    avg_score = round(sum(item.score for item in top_slice) / max(1, len(top_slice)), 2)
    avg_confidence = round(sum(item.confidence for item in top_slice) / max(1, len(top_slice)), 4)
    story_title = str(title or "").strip() or normalized_items[0].title
    story_id = generate_slug(story_title, max_length=48)
    generated_at = _utcnow()
    story_summary_text = str(summary or "").strip() or _story_seed_summary(
        normalized_items,
        title=story_title,
        entities=entities,
        contradictions=len(contradictions),
    )
    story_status = str(status or "").strip().lower() or ("conflicted" if contradictions else "active")

    return Story(
        title=story_title,
        summary=story_summary_text,
        status=story_status,
        score=avg_score,
        confidence=avg_confidence,
        item_count=len(normalized_items),
        source_count=len(source_names),
        primary_item_id=primary_item_id,
        entities=entities,
        source_names=source_names,
        primary_evidence=primary_evidence,
        secondary_evidence=secondary_evidence,
        timeline=timeline,
        contradictions=contradictions,
        semantic_review=semantic_review,
        generated_at=generated_at,
        governance=_build_story_governance(
            story_id=story_id,
            primary_item_id=primary_item_id,
            source_names=source_names,
            evidence_rows=evidence_rows,
            contradictions=contradictions,
            generated_at=generated_at,
        ),
        id=story_id,
    )


def build_story_clusters(
    items: list[DataPulseItem],
    *,
    entity_store: EntityStore | None = None,
    max_stories: int = 10,
    evidence_limit: int = 6,
) -> list[Story]:
    if not items:
        return []

    ranked = sorted(
        items,
        key=lambda item: (item.score, item.confidence, _parse_dt(item.fetched_at).timestamp(), item.id),
        reverse=True,
    )
    clusters: list[dict[str, Any]] = []

    for item in ranked:
        descriptor = _descriptor_for_item(item, entity_store=entity_store)
        best_cluster: dict[str, Any] | None = None
        best_similarity = 0.0
        for cluster in clusters:
            similarity = _cluster_similarity(descriptor, cluster)
            if similarity > best_similarity:
                best_similarity = similarity
                best_cluster = cluster
        if best_cluster is None or best_similarity < 0.34:
            clusters.append(
                {
                    "descriptors": [descriptor],
                    "fingerprints": {descriptor["fingerprint"]} if descriptor["fingerprint"] else set(),
                    "title_tokens": set(descriptor["title_tokens"]),
                    "content_tokens": set(descriptor["content_tokens"]),
                    "entity_keys": set(descriptor["entity_keys"]),
                    "domain": descriptor["domain"],
                }
            )
            continue

        best_cluster["descriptors"].append(descriptor)
        if descriptor["fingerprint"]:
            best_cluster["fingerprints"].add(descriptor["fingerprint"])
        best_cluster["title_tokens"].update(descriptor["title_tokens"])
        best_cluster["content_tokens"].update(descriptor["content_tokens"])
        best_cluster["entity_keys"].update(descriptor["entity_keys"])

    stories: list[Story] = []
    for cluster in clusters:
        descriptors: list[dict[str, Any]] = sorted(
            cluster["descriptors"],
            key=lambda row: (
                row["item"].score,
                row["item"].confidence,
                _parse_dt(row["item"].fetched_at).timestamp(),
                row["item"].id,
            ),
            reverse=True,
        )
        cluster_items = [row["item"] for row in descriptors]
        exemplar = descriptors[0]
        evidence_limit_safe = max(1, int(evidence_limit))
        primary_count = _select_primary_count(len(cluster_items), evidence_limit_safe)

        entity_counter: Counter[str] = Counter()
        entity_display: dict[str, str] = {}
        for row in descriptors:
            for label in row["entity_labels"]:
                normalized = normalize_entity_name(label)
                if not normalized:
                    continue
                entity_counter[normalized] += 1
                entity_display[normalized] = label
        entities = [entity_display[key] for key, _ in entity_counter.most_common(6)]

        evidence_rows: list[StoryEvidence] = []
        for index, row in enumerate(descriptors[:evidence_limit_safe]):
            item = row["item"]
            role = "primary" if index < primary_count else "secondary"
            evidence_rows.append(
                StoryEvidence(
                    item_id=item.id,
                    title=item.title,
                    url=item.url,
                    source_name=item.source_name,
                    source_type=item.source_type.value,
                    score=item.score,
                    confidence=item.confidence,
                    fetched_at=item.fetched_at,
                    review_state=item.review_state,
                    role=role,
                    entities=row["entity_labels"],
                    governance=build_item_governance(item),
                )
            )

        primary_evidence = [row for row in evidence_rows if row.role == "primary"]
        secondary_evidence = [row for row in evidence_rows if row.role == "secondary"]
        timeline_rows = sorted(
            descriptors,
            key=lambda row: (_parse_dt(row["item"].extra.get("date_published", row["item"].fetched_at)), row["item"].id),
        )
        timeline = [
            StoryTimelineEvent(
                time=str(item.extra.get("date_published") or item.fetched_at),
                item_id=item.id,
                title=item.title,
                source_name=item.source_name,
                url=item.url,
                role="primary" if item.id == primary_evidence[0].item_id else "secondary",
                score=item.score,
            )
            for item in [row["item"] for row in timeline_rows]
        ]

        semantic_review = build_semantic_review(cluster_items)
        contradictions = [
            StoryConflict(
                topic=str(row.get("topic", "")),
                positive=int(row.get("positive", 0) or 0),
                negative=int(row.get("negative", 0) or 0),
                neutral=int(row.get("neutral", 0) or 0),
                note="semantic contradiction hint",
            )
            for row in semantic_review.get("contradictions", [])
            if isinstance(row, dict)
        ]
        status = "conflicted" if contradictions else "active"
        source_names = sorted({item.source_name for item in cluster_items})
        top_slice = cluster_items[: min(3, len(cluster_items))]
        avg_score = round(sum(item.score for item in top_slice) / max(1, len(top_slice)), 2)
        avg_confidence = round(sum(item.confidence for item in top_slice) / max(1, len(top_slice)), 4)
        title = exemplar["item"].title
        story_id = generate_slug(title, max_length=48)
        primary_item_id = primary_evidence[0].item_id if primary_evidence else ""
        generated_at = _utcnow()
        story = Story(
            title=title,
            summary=_story_summary(
                title,
                item_count=len(cluster_items),
                source_count=len(source_names),
                entities=entities,
                contradictions=len(contradictions),
            ),
            status=status,
            score=avg_score,
            confidence=avg_confidence,
            item_count=len(cluster_items),
            source_count=len(source_names),
            primary_item_id=primary_item_id,
            entities=entities,
            source_names=source_names,
            primary_evidence=primary_evidence,
            secondary_evidence=secondary_evidence,
            timeline=timeline,
            contradictions=contradictions,
            semantic_review=semantic_review,
            generated_at=generated_at,
            governance=_build_story_governance(
                story_id=story_id,
                primary_item_id=primary_item_id,
                source_names=source_names,
                evidence_rows=evidence_rows,
                contradictions=contradictions,
                generated_at=generated_at,
            ),
            id=story_id,
        )
        stories.append(story)

    stories.sort(
        key=lambda story: (
            story.score,
            story.confidence,
            story.item_count,
            story.source_count,
            story.id,
        ),
        reverse=True,
    )
    return stories[: max(0, max_stories)]
