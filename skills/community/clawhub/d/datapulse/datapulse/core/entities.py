"""Entity extraction primitives and lightweight LLM/heuristic extractor."""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import logging
import os
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

import requests

from datapulse.core.retry import CircuitBreaker, CircuitBreakerOpen, RateLimitError, retry
from datapulse.core.security import get_secret

logger = logging.getLogger("datapulse.entities")


class EntityType(str, Enum):
    PERSON = "PERSON"
    ORG = "ORG"
    LOCATION = "LOCATION"
    CONCEPT = "CONCEPT"
    EVENT = "EVENT"
    TECHNOLOGY = "TECHNOLOGY"
    PRODUCT = "PRODUCT"
    UNKNOWN = "UNKNOWN"


_RAW_EVENT_TOKENS = {
    "CES",
    "WWDC",
    "NeurIPS",
    "ICML",
    "ICLR",
    "ACL",
    "NAACL",
    "SIGGRAPH",
}

_TECH_TERMS = {
    "PYTHON",
    "AWS",
    "KUBERNETES",
    "DOCKER",
    "LLM",
    "CHATGPT",
    "CLAUDE",
    "GEMINI",
    "CLAUDE",
    "RUST",
    "GO",
    "JAVASCRIPT",
    "TYPESCRIPT",
    "PYTORCH",
    "TENSORFLOW",
    "KUBERNETES",
    "CUDA",
    "OLLAMA",
    "OPENAI",
    "ANTHROPIC",
    "MICROSOFT",
    "GOOGLE",
    "TESLA",
    "OPENAI",
}


_ORGANIZATION_HINTS = (
    "Inc",
    "Corp",
    "Corporation",
    "LLC",
    "Ltd",
    "Limited",
    "Company",
    "Group",
    "Foundation",
    "Agency",
    "Institute",
    "University",
)


@dataclass(frozen=True)
class Entity:
    name: str
    entity_type: EntityType
    display_name: str
    source_item_ids: list[str] = field(default_factory=list)
    mention_count: int = 1
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return hashlib.md5(f"{self.entity_type}:{self.name}".encode("utf-8")).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["entity_type"] = self.entity_type.value
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Entity":
        return cls(
            name=str(data.get("name", "")).strip(),
            entity_type=EntityType(data.get("entity_type", EntityType.UNKNOWN.value)),
            display_name=str(data.get("display_name", "")).strip() or str(data.get("name", "")).strip(),
            source_item_ids=[str(item) for item in data.get("source_item_ids", []) if str(item)],
            mention_count=max(int(data.get("mention_count", 1)), 1),
            extra=dict(data.get("extra", {})),
        )


@dataclass(frozen=True)
class Relation:
    source_entity: str
    target_entity: str
    relation_type: str
    keywords: list[str] = field(default_factory=list)
    weight: float = 1.0
    source_item_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_entity": self.source_entity,
            "target_entity": self.target_entity,
            "relation_type": self.relation_type,
            "keywords": self.keywords,
            "weight": self.weight,
            "source_item_ids": self.source_item_ids,
        }


_ENTITY_BREAKER = CircuitBreaker(
    failure_threshold=int(os.getenv("DATAPULSE_ENTITY_BREAKER_THRESHOLD", "5")),
    recovery_timeout=float(os.getenv("DATAPULSE_ENTITY_RECOVERY_TIMEOUT", "60")),
    name="entity_llm",
    rate_limit_weight=2,
)


def normalize_entity_name(name: str) -> str:
    """Normalize to UPPER_UNDERSCORE style."""
    clean = name.strip()
    if not clean:
        return ""
    # Collapse non alnum characters and keep Unicode words.
    cleaned = re.sub(r"[\s\-.\/]+", "_", clean.upper())
    cleaned = re.sub(r"[^0-9A-Z_]+", "", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def _normalize_type(raw: str | EntityType) -> EntityType:
    if isinstance(raw, EntityType):
        return raw
    key = (raw or "").strip().upper()
    if not key:
        return EntityType.UNKNOWN
    for value in EntityType:
        if key == value.value:
            return value
    # Common aliases.
    alias_map = {
        "PERSONS": EntityType.PERSON,
        "PEOPLE": EntityType.PERSON,
        "ORGANIZATION": EntityType.ORG,
        "COMPANY": EntityType.ORG,
        "LOCATION": EntityType.LOCATION,
        "PLACE": EntityType.LOCATION,
        "PLACEHOLDER": EntityType.LOCATION,
        "EVENTS": EntityType.EVENT,
        "TECH": EntityType.TECHNOLOGY,
        "TECHNOLOGIES": EntityType.TECHNOLOGY,
        "TOOL": EntityType.TECHNOLOGY,
        "TOOLS": EntityType.TECHNOLOGY,
        "PRODUCTS": EntityType.PRODUCT,
        "TOPIC": EntityType.CONCEPT,
        "TOPICS": EntityType.CONCEPT,
    }
    return alias_map.get(key, EntityType.UNKNOWN)


def _make_entity(display_name: str, entity_type: EntityType, source_item_ids: list[str] | None = None) -> Entity:
    normalized = normalize_entity_name(display_name)
    if not normalized:
        raise ValueError("entity name cannot be empty")
    return Entity(
        name=normalized,
        entity_type=entity_type,
        display_name=display_name.strip(),
        source_item_ids=list(dict.fromkeys([item for item in (source_item_ids or []) if item])),
    )


def _add_entity(
    bucket: dict[str, Entity],
    display_name: str,
    entity_type: EntityType,
    source_item_ids: list[str] | None = None,
) -> None:
    candidate = _make_entity(display_name, entity_type, source_item_ids=source_item_ids)
    existing = bucket.get(candidate.id)
    if existing is None:
        bucket[candidate.id] = candidate
        return

    merged = Entity(
        name=existing.name,
        entity_type=existing.entity_type,
        display_name=existing.display_name,
        source_item_ids=sorted(set(existing.source_item_ids) | set(candidate.source_item_ids)),
        mention_count=existing.mention_count + max(1, candidate.mention_count),
        extra={**existing.extra, **candidate.extra},
    )
    bucket[candidate.id] = merged


def extract_entities_fast(text: str, source_item_id: str = "") -> tuple[list[Entity], list[Relation]]:
    """Heuristic extraction without external dependency."""
    content = (text or "").strip()
    entities: dict[str, Entity] = {}
    relations: list[Relation] = []
    if not content:
        return [], []

    lower = content.lower()
    for token in _TECH_TERMS:
        if token.lower() in lower:
            _add_entity(entities, token.title(), EntityType.TECHNOLOGY, [source_item_id])

    for token in _RAW_EVENT_TOKENS:
        if token.lower() in lower:
            _add_entity(entities, token, EntityType.EVENT, [source_item_id])

    # Organization pattern: "Acme Corp", "Open Source Foundation"
    org_re = re.compile(
        r"([A-Z][A-Za-z0-9&'\.\-]*(?:\s+[A-Z][A-Za-z0-9&'\.\-]*)*\s+(?:" + "|".join(_ORGANIZATION_HINTS) + r"))\b"
    )
    for match in org_re.findall(content):
        _add_entity(entities, str(match).strip(), EntityType.ORG, [source_item_id])

    # Person pattern with role cues
    person_pattern = re.compile(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b\s*(?:said|says|said that|announced|launched|founded|founds|appointed|reported)\b",
        re.IGNORECASE,
    )
    for match in person_pattern.findall(content):
        _add_entity(entities, str(match), EntityType.PERSON, [source_item_id])

    # Location cues (best-effort).
    loc_pattern = re.compile(r"\b(?:in|at|from)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})\b")
    for match in loc_pattern.findall(content):
        token = str(match).strip()
        if len(token) >= 3:
            _add_entity(entities, token, EntityType.LOCATION, [source_item_id])

    return list(entities.values()), relations


def _parse_tuple_line(line: str) -> tuple[str, str, str, str] | None:
    if not line:
        return None
    cleaned = line.strip()
    # Keep tuple format strict first.
    if not (cleaned.startswith("(") or cleaned.startswith("['") or cleaned.startswith('"entity"')):
        return None
    try:
        value = ast.literal_eval(cleaned)
    except Exception:
        return None

    if isinstance(value, (tuple, list)) and len(value) >= 4:
        raw_type = str(value[0]).strip().strip('"\'')
        if raw_type.lower() != "entity":
            return None
        return str(value[0]), str(value[1]), str(value[2]), str(value[3])
    return None


def parse_llm_output(raw: str) -> tuple[list[Entity], list[Relation]]:
    """Parse mixed tuple-like and JSON outputs from LLM."""
    entities: dict[str, Entity] = {}
    relations: list[Relation] = []

    if not raw:
        return [], []

    parsed_from_llm = False
    for line in raw.splitlines():
        parsed = _parse_tuple_line(line)
        if not parsed:
            continue
        _, name, raw_type, desc = parsed
        source_item = ""
        if desc:
            pass
        _add_entity(entities, name, _normalize_type(raw_type), [source_item])
        parsed_from_llm = True

    if parsed_from_llm:
        return list(entities.values()), relations

    try:
        payload = json.loads(raw)
    except Exception:
        return list(entities.values()), relations

    if isinstance(payload, dict):
        raw_entities = payload.get("entities")
        raw_relations = payload.get("relations")
    else:
        raw_entities = payload if isinstance(payload, list) else []
        raw_relations = []

    if isinstance(raw_entities, list):
        for raw_entity in raw_entities:
            if not isinstance(raw_entity, dict):
                continue
            name = str(raw_entity.get("name", "")).strip()
            if not name:
                continue
            entity_type = _normalize_type(str(raw_entity.get("type", "")) or str(raw_entity.get("entity_type", "")))
            source_ids = [str(s) for s in raw_entity.get("source_item_ids", []) if str(s)]
            _add_entity(entities, name, entity_type, source_ids)

    if isinstance(raw_relations, list):
        for raw_relation in raw_relations:
            if not isinstance(raw_relation, dict):
                continue
            source = str(raw_relation.get("source_entity", "")).strip()
            target = str(raw_relation.get("target_entity", "")).strip()
            relation_type = str(raw_relation.get("relation_type", "RELATED_TO")).strip() or "RELATED_TO"
            if source and target:
                relations.append(
                    Relation(
                        source_entity=normalize_entity_name(source),
                        target_entity=normalize_entity_name(target),
                        relation_type=relation_type.upper(),
                        keywords=[
                            str(item) for item in (raw_relation.get("keywords", []) or []) if str(item).strip()
                        ],
                        weight=float(raw_relation.get("weight", 1.0) or 1.0),
                        source_item_ids=[str(item) for item in (raw_relation.get("source_item_ids", []) or []) if str(item)],
                    )
                )

    return list(entities.values()), relations


def _decode_prompt(payload: str | bytes) -> str:
    if isinstance(payload, bytes):
        return base64.b64decode(payload).decode("utf-8")
    return payload


def _call_llm_api(prompt: str, api_key: str, model: str, api_base: str) -> str:
    endpoint = f"{api_base.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You extract named entities from text."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 2048,
    }
    response = requests.post(
        endpoint,
        json=body,
        headers=headers,
        timeout=15,
    )
    if response.status_code == 429:
        retry_after = float(response.headers.get("Retry-After", "0") or 0)
        raise RateLimitError(
            f"LLM rate limit: {response.status_code}",
            retry_after=retry_after if retry_after > 0 else 0,
        )
    if response.status_code >= 400:
        raise RuntimeError(f"LLM request failed: {response.status_code} {response.text[:200]}")
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content", "")).strip()


@retry(max_attempts=2, base_delay=1.0, retryable=(RateLimitError, requests.RequestException, RuntimeError))
def _llm_text(prompt: str, *, api_key: str, model: str, api_base: str) -> str:
    return _call_llm_api(prompt, api_key=api_key, model=model, api_base=api_base)


def extract_entities_llm(
    text: str,
    source_item_id: str = "",
    *,
    api_key: str | None = None,
    model: str = "gpt-4o-mini",
    api_base: str = "https://api.openai.com/v1",
) -> tuple[list[Entity], list[Relation]]:
    """LLM extraction path (opt-in)."""
    resolved_api_key = api_key or get_secret("DATAPULSE_LLM_API_KEY")
    if not resolved_api_key:
        return [], []

    if not text:
        return [], []

    if source_item_id:
        trace = source_item_id
    else:
        trace = "<unknown>"
    prompt = (
        "Extract entities in tuple format: (\"entity\", \"NAME\", \"TYPE\", \"DESC\").\n"
        "Allowed TYPE values: PERSON, ORG, LOCATION, CONCEPT, EVENT, TECHNOLOGY, PRODUCT.\n"
        "Return only valid entities and relations in JSON if tuple is infeasible.\n"
        "Input:\n"
        f"{text[:8000]}\n"
        f"item={trace}"
    )

    try:
        raw = _ENTITY_BREAKER.call(
            _llm_text,
            prompt,
            api_key=resolved_api_key,
            model=model,
            api_base=api_base,
        )
    except CircuitBreakerOpen as exc:
        logger.warning("LLM entity extraction rejected by circuit breaker: %s", exc)
        return [], []
    except Exception as exc:
        logger.warning("LLM entity extraction failed, fallback to fast mode: %s", exc)
        return [], []

    return parse_llm_output(raw)


def extract_entities(
    text: str,
    mode: str = "fast",
    source_item_id: str = "",
    *,
    llm_api_key: str | None = None,
    llm_model: str = "gpt-4o-mini",
    llm_api_base: str = "https://api.openai.com/v1",
) -> tuple[list[Entity], list[Relation]]:
    normalized_mode = (mode or "fast").strip().lower()
    if normalized_mode == "llm":
        entities, relations = extract_entities_llm(
            text[:8000],
            source_item_id=source_item_id,
            api_key=llm_api_key,
            model=llm_model,
            api_base=llm_api_base,
        )
        if entities or relations:
            return entities, relations
    return extract_entities_fast(text[:8000], source_item_id=source_item_id)
