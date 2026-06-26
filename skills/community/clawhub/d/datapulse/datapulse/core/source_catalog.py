"""Source catalog and subscription model for DataPulse."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .models import (
    DataPulseItem,
    SourceAuthorityLevel,
    SourceCollectionMode,
    SourceGovernance,
    SourceGovernanceClass,
    SourceSensitivity,
    SourceType,
)
from .utils import generate_slug, resolve_platform_hint

JSONSource = dict[str, Any]


def _normalize_source_type(value: str) -> str:
    if not value:
        return SourceType.GENERIC.value
    normalized = value.strip().lower()
    try:
        return SourceType(normalized).value
    except ValueError:
        return normalized


def _item_id(seed: str) -> str:
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _primary_source_type_value(source_type: str) -> str:
    parts = [part.strip() for part in str(source_type or "").split("|") if part.strip()]
    if not parts:
        return SourceType.GENERIC.value
    return parts[0].lower()


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    seen: list[str] = []
    for item in value:
        text = str(item).strip()
        if text and text not in seen:
            seen.append(text)
    return seen


def _default_source_class(source_type: str) -> SourceGovernanceClass:
    normalized = _primary_source_type_value(source_type)
    if normalized == SourceType.MANUAL.value:
        return SourceGovernanceClass.ANALYST
    if normalized in {
        "github",
        SourceType.TWITTER.value,
        SourceType.REDDIT.value,
        SourceType.YOUTUBE.value,
        SourceType.BILIBILI.value,
        SourceType.TELEGRAM.value,
        SourceType.WECHAT.value,
        SourceType.WEIBO.value,
        SourceType.XHS.value,
        SourceType.HACKERNEWS.value,
    }:
        return SourceGovernanceClass.PLATFORM
    if normalized in {SourceType.RSS.value, SourceType.ARXIV.value}:
        return SourceGovernanceClass.PUBLISHER
    return SourceGovernanceClass.GENERIC


def _default_collection_mode(source_type: str, config: dict[str, Any]) -> SourceCollectionMode:
    normalized = _primary_source_type_value(source_type)
    explicit = str(config.get("collection_mode", "") or config.get("mode", "")).strip().lower()
    if explicit:
        try:
            return SourceCollectionMode(explicit)
        except ValueError:
            pass
    if normalized == SourceType.MANUAL.value:
        return SourceCollectionMode.MANUAL_FACT
    if any(str(config.get(key, "")).strip() for key in ("api_base", "api_url", "api_endpoint")):
        return SourceCollectionMode.API
    return SourceCollectionMode.PUBLIC_WEB


def _default_authority(source_type: str, source_class: SourceGovernanceClass) -> SourceAuthorityLevel:
    normalized = _primary_source_type_value(source_type)
    if normalized in {"github", SourceType.RSS.value, SourceType.ARXIV.value}:
        return SourceAuthorityLevel.PRIMARY
    if source_class == SourceGovernanceClass.ANALYST:
        return SourceAuthorityLevel.SECONDARY
    if source_class == SourceGovernanceClass.PLATFORM:
        return SourceAuthorityLevel.COMMUNITY
    if source_class == SourceGovernanceClass.AGGREGATOR:
        return SourceAuthorityLevel.SECONDARY
    if source_class == SourceGovernanceClass.PUBLISHER:
        return SourceAuthorityLevel.PRIMARY
    return SourceAuthorityLevel.SECONDARY


def _default_sensitivity(
    source_type: str,
    collection_mode: SourceCollectionMode,
) -> SourceSensitivity:
    normalized = _primary_source_type_value(source_type)
    if collection_mode in {SourceCollectionMode.SEARCH_GATEWAY, SourceCollectionMode.MANUAL_FACT}:
        return SourceSensitivity.REVIEW_REQUIRED
    if normalized in {
        SourceType.TELEGRAM.value,
        SourceType.WECHAT.value,
        SourceType.WEIBO.value,
        SourceType.XHS.value,
    }:
        return SourceSensitivity.REVIEW_REQUIRED
    return SourceSensitivity.PUBLIC


def _default_compliance_hints(collection_mode: SourceCollectionMode) -> list[str]:
    if collection_mode == SourceCollectionMode.API:
        return [
            "public_content_only",
            "respect_source_terms",
            "respect_rate_limits",
            "api_terms_apply",
            "no_automated_legal_determination",
        ]
    if collection_mode == SourceCollectionMode.SEARCH_GATEWAY:
        return [
            "search_results_require_verification",
            "respect_source_terms",
            "operator_review_required",
            "no_automated_legal_determination",
        ]
    if collection_mode == SourceCollectionMode.MANUAL_FACT:
        return [
            "manual_entry_requires_attribution",
            "operator_review_required",
            "no_automated_legal_determination",
        ]
    return [
        "public_content_only",
        "respect_source_terms",
        "respect_rate_limits",
        "no_automated_legal_determination",
    ]


def _merge_compliance_hints(explicit_hints: list[str], defaults: list[str]) -> list[str]:
    seen: list[str] = []
    for item in [*explicit_hints, *defaults]:
        text = str(item).strip()
        if text and text not in seen:
            seen.append(text)
    return seen


def _governance_from_raw(raw: JSONSource, source_type: str, config: dict[str, Any]) -> SourceGovernance:
    governance_raw = raw.get("governance", {})
    if not isinstance(governance_raw, dict):
        governance_raw = {}

    source_class_value = governance_raw.get("source_class") or raw.get("source_class") or _default_source_class(source_type)
    try:
        source_class = SourceGovernanceClass(source_class_value)
    except (TypeError, ValueError):
        source_class = _default_source_class(source_type)

    collection_mode_value = governance_raw.get("collection_mode") or raw.get("collection_mode") or _default_collection_mode(source_type, config)
    try:
        collection_mode = SourceCollectionMode(collection_mode_value)
    except (TypeError, ValueError):
        collection_mode = _default_collection_mode(source_type, config)

    authority = governance_raw.get("authority") or raw.get("authority") or _default_authority(source_type, source_class)
    sensitivity = governance_raw.get("sensitivity") or raw.get("sensitivity") or _default_sensitivity(source_type, collection_mode)
    explicit_hints = _normalize_string_list(governance_raw.get("compliance_hints", raw.get("compliance_hints", [])))
    defaults = _default_compliance_hints(collection_mode)

    return SourceGovernance(
        source_class=source_class,
        collection_mode=collection_mode,
        authority=authority,
        sensitivity=sensitivity,
        compliance_hints=_merge_compliance_hints(explicit_hints, defaults),
    )


@dataclass
class SourceRecord:
    name: str
    source_type: str
    config: dict[str, Any] = field(default_factory=dict)
    governance: SourceGovernance = field(default_factory=SourceGovernance)
    is_active: bool = True
    is_public: bool = True
    tags: list[str] = field(default_factory=list)
    match: dict[str, str] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    id: str = ""
    tier: int = 2
    authority_weight: float = 0.5

    @classmethod
    def from_dict(cls, raw: JSONSource) -> "SourceRecord":
        if not isinstance(raw, dict):
            raise TypeError("source must be object")

        source_type = _normalize_source_type(str(raw.get("source_type", "")) or str(raw.get("type", "")))
        name = str(raw.get("name", "source")).strip() or source_type
        source_id = str(raw.get("id", "")).strip() or _item_id(f"{name}:{source_type}:{raw.get('config', {}).get('url', '')}")
        config = raw.get("config", {})
        if not isinstance(config, dict):
            config = {}
        governance = _governance_from_raw(raw, source_type, config)
        tags = [str(t).strip() for t in raw.get("tags", []) if str(t).strip()]
        match = raw.get("match", {})
        if not isinstance(match, dict):
            match = {}
        tier = _safe_int(raw.get("tier"), default=2)
        tier = max(1, min(3, tier))
        authority_weight = raw.get("authority_weight", 0.5)
        try:
            authority_weight = float(authority_weight)
        except (TypeError, ValueError):
            authority_weight = 0.5
        authority_weight = max(0.0, min(1.0, authority_weight))

        return cls(
            id=source_id,
            name=name,
            source_type=source_type,
            config=config,
            governance=governance,
            is_active=bool(raw.get("is_active", True)),
            is_public=bool(raw.get("is_public", True)),
            tags=tags,
            match={str(k): str(v) for k, v in match.items() if str(k) and str(v)},
            created_at=str(raw.get("created_at", "")),
            updated_at=str(raw.get("updated_at", "")),
            tier=tier,
            authority_weight=authority_weight,
        )

    def to_dict(self) -> JSONSource:
        payload: JSONSource = {
            "id": self.id,
            "name": self.name,
            "source_type": self.source_type,
            "config": self.config,
            "governance": self.governance.to_dict(),
            "is_active": self.is_active,
            "is_public": self.is_public,
            "tags": self.tags,
            "match": self.match,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tier": self.tier,
            "authority_weight": self.authority_weight,
        }
        return payload

    def _matches_host(self, value: str, host: str) -> bool:
        if not value or not host:
            return False
        return host == value or host.endswith(f".{value}")

    def _matches_pattern(self, pattern: str, url: str) -> bool:
        if not pattern:
            return False
        try:
            return bool(re.search(pattern, url))
        except re.error:
            return pattern in url

    def matches(self, item: DataPulseItem) -> bool:
        if item.source_type.value != self.source_type and item.source_type.value not in self.source_type.split("|"):
            return False

        parsed = urlparse(item.url)
        host = (parsed.hostname or "").lower()

        # explicit domain filter
        domain = self.match.get("domain", "").lower()
        if domain and self._matches_host(domain, host):
            return True

        # explicit url prefix match
        prefix = self.match.get("url_prefix", "")
        if prefix and item.url.startswith(prefix):
            return True

        # regex / text pattern
        pattern = self.match.get("pattern", "")
        if pattern and self._matches_pattern(pattern, item.url):
            return True

        # fallback to configured source url/domain
        source_url = str(self.config.get("url", "")).lower()
        if source_url and item.url.startswith(source_url):
            return True
        source_host = urlparse(source_url).hostname or ""
        if source_host and self._matches_host(source_host.lower(), host):
            return True

        return False


@dataclass
class SourcePack:
    name: str
    source_ids: list[str]
    slug: str = ""
    description: str = ""
    is_public: bool = True
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_dict(cls, raw: JSONSource) -> "SourcePack":
        if not isinstance(raw, dict):
            raise TypeError("pack must be object")
        raw_name = str(raw.get("name", "pack")).strip()
        source_ids = [str(sid) for sid in raw.get("source_ids", []) if str(sid).strip()]
        slug = str(raw.get("slug", "")).strip() or generate_slug(raw_name, max_length=80)
        return cls(
            name=raw_name,
            source_ids=source_ids,
            slug=slug,
            description=str(raw.get("description", "")),
            is_public=bool(raw.get("is_public", True)),
            created_at=str(raw.get("created_at", "")),
            updated_at=str(raw.get("updated_at", "")),
        )

    def to_dict(self) -> JSONSource:
        return {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "source_ids": self.source_ids,
            "is_public": self.is_public,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


_SUPPORTED_CATALOG_VERSIONS = {1, 2}
_BUILTIN_SOURCE_SEEDS: tuple[JSONSource, ...] = (
    {
        "id": "builtin_github",
        "name": "GitHub Open Source",
        "source_type": "github|generic",
        "config": {"url": "https://github.com"},
        "governance": {
            "source_class": "platform",
            "collection_mode": "public_web",
            "authority": "primary",
            "sensitivity": "public",
        },
        "is_active": True,
        "is_public": True,
        "tags": ["github", "code", "opensource"],
        "match": {"domain": "github.com"},
        "tier": 1,
        "authority_weight": 0.92,
    },
    {
        "id": "builtin_reddit",
        "name": "Reddit Communities",
        "source_type": "reddit",
        "config": {"url": "https://www.reddit.com"},
        "governance": {
            "source_class": "platform",
            "collection_mode": "public_web",
            "authority": "community",
            "sensitivity": "public",
        },
        "is_active": True,
        "is_public": True,
        "tags": ["reddit", "community"],
        "match": {"domain": "reddit.com"},
        "tier": 1,
        "authority_weight": 0.75,
    },
    {
        "id": "builtin_x",
        "name": "X Network",
        "source_type": "twitter",
        "config": {"url": "https://x.com"},
        "governance": {
            "source_class": "platform",
            "collection_mode": "public_web",
            "authority": "community",
            "sensitivity": "public",
        },
        "is_active": True,
        "is_public": True,
        "tags": ["x", "twitter"],
        "match": {"domain": "x.com"},
        "tier": 1,
        "authority_weight": 0.72,
    },
    {
        "id": "builtin_hn",
        "name": "Hacker News",
        "source_type": "hackernews",
        "config": {"url": "https://news.ycombinator.com"},
        "governance": {
            "source_class": "platform",
            "collection_mode": "public_web",
            "authority": "community",
            "sensitivity": "public",
        },
        "is_active": True,
        "is_public": True,
        "tags": ["hackernews", "tech"],
        "match": {"domain": "news.ycombinator.com"},
        "tier": 1,
        "authority_weight": 0.78,
    },
)


class SourceCatalog:
    def __init__(self, catalog_path: str | None = None):
        default_path = os.getenv("DATAPULSE_SOURCE_CATALOG", "").strip() or "datapulse_source_catalog.json"
        self._explicit_catalog_path = catalog_path is not None
        self.path = Path(catalog_path or default_path).expanduser()
        self.version = 1
        self.sources: dict[str, SourceRecord] = {}
        self.subscriptions: dict[str, list[str]] = {}
        self.packs: dict[str, SourcePack] = {}
        self._bootstrapped_defaults = False
        self._load()

    def _bootstrap_builtin_sources(self) -> None:
        added = False
        for raw in _BUILTIN_SOURCE_SEEDS:
            try:
                source = SourceRecord.from_dict(raw)
            except (KeyError, TypeError, ValueError):
                continue
            if source.id in self.sources:
                continue
            self.sources[source.id] = source
            added = True
        if added:
            self._bootstrapped_defaults = True

    def _load(self) -> None:
        if not self.path.exists():
            if not self._explicit_catalog_path:
                self._bootstrap_builtin_sources()
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            if not self._explicit_catalog_path:
                self._bootstrap_builtin_sources()
            return
        if not isinstance(raw, dict):
            if not self._explicit_catalog_path:
                self._bootstrap_builtin_sources()
            return

        self.version = _safe_int(raw.get("version"), default=1)
        if self.version not in _SUPPORTED_CATALOG_VERSIONS:
            import logging
            logging.getLogger("datapulse.source_catalog").warning(
                "Source catalog version %d is not supported (supported: %s). "
                "Some features may not work correctly.",
                self.version, _SUPPORTED_CATALOG_VERSIONS,
            )
        self.sources = {}
        for source_obj in raw.get("sources", []) if isinstance(raw.get("sources"), list) else []:
            try:
                source = SourceRecord.from_dict(source_obj)
            except (KeyError, TypeError, ValueError):
                continue
            self.sources[source.id] = source

        self.subscriptions = {}
        raw_sub = raw.get("subscriptions", {})
        if isinstance(raw_sub, dict):
            for profile, ids in raw_sub.items():
                if not isinstance(ids, list):
                    continue
                normalized: list[str] = []
                for source_id in ids:
                    sid = str(source_id).strip()
                    if sid and sid in self.sources:
                        normalized.append(sid)
                self.subscriptions[str(profile).strip() or "default"] = normalized

        self.packs = {}
        for pack_obj in raw.get("packs", []) if isinstance(raw.get("packs"), list) else []:
            try:
                pack = SourcePack.from_dict(pack_obj)
                key = pack.slug.lower()
                pack.slug = key
            except (KeyError, TypeError, ValueError):
                continue
            self.packs[key] = pack
        if not self.sources and not self._explicit_catalog_path:
            self._bootstrap_builtin_sources()

    def _ensure_file(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _touch_timestamps(self, source: SourceRecord, create: bool = False) -> None:
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        if create:
            source.created_at = source.created_at or now
        source.updated_at = now

    def _save(self) -> None:
        self._ensure_file()
        payload = {
            "version": self.version,
            "sources": [source.to_dict() for source in self.sources.values()],
            "subscriptions": self.subscriptions,
            "packs": [pack.to_dict() for pack in self.packs.values()],
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_sources(self, *, include_inactive: bool = False, public_only: bool = False) -> list[SourceRecord]:
        items = list(self.sources.values())
        if not include_inactive:
            items = [s for s in items if s.is_active]
        if public_only:
            items = [s for s in items if s.is_public]
        return sorted(items, key=lambda s: s.name.lower())

    def build_authority_map(self) -> dict[str, float]:
        """Build a name/domain → authority_weight mapping from active sources."""
        authority: dict[str, float] = {}
        for source in self.sources.values():
            if not source.is_active:
                continue
            weight = source.authority_weight
            authority[source.name.lower()] = weight
            # Also map by domain if available
            domain = source.match.get("domain", "").lower().strip()
            if domain:
                authority[domain] = weight
            source_url = str(source.config.get("url", "")).strip()
            if source_url:
                source_host = (urlparse(source_url).hostname or "").lower()
                if source_host and source_host not in authority:
                    authority[source_host] = weight
        return authority

    def list_packs(self, *, public_only: bool = False) -> list[SourcePack]:
        items = list(self.packs.values())
        if public_only:
            items = [p for p in items if p.is_public]
        return sorted(items, key=lambda p: p.name.lower())

    def get_pack(self, slug: str) -> SourcePack | None:
        return self.packs.get(str(slug or "").lower())

    def get_source(self, source_id: str) -> SourceRecord | None:
        return self.sources.get(str(source_id))

    @staticmethod
    def _primary_source_type(source_type: str) -> str:
        return _primary_source_type_value(source_type)

    def _to_source_payload(self, source: SourceRecord) -> dict[str, Any]:
        return {
            "source_id": source.id,
            "source_type": self._primary_source_type(source.source_type),
            "name": source.name,
            "config": dict(source.config),
            "governance": source.governance.to_dict(),
            "tags": source.tags,
            "match": source.match,
            "is_public": source.is_public,
            "is_active": source.is_active,
            "tier": source.tier,
            "authority_weight": source.authority_weight,
        }

    def resolve_source(self, url: str) -> dict[str, Any]:
        parsed = urlparse(url)
        source_type = resolve_platform_hint(url)
        host = (parsed.hostname or "").lower()
        seed = parsed.geturl() or url

        normalized_source_type = _normalize_source_type(source_type)
        ranked: list[tuple[int, SourceRecord]] = []

        for source in self.sources.values():
            if not source.is_active:
                continue

            score = 0

            domain = str(source.match.get("domain", "")).lower().strip()
            if domain and source._matches_host(domain, host):
                score = max(score, 90)

            url_prefix = str(source.match.get("url_prefix", "")).strip()
            if url_prefix and seed.startswith(url_prefix):
                score = max(score, 100)

            pattern = str(source.match.get("pattern", "")).strip()
            if pattern and source._matches_pattern(pattern, seed):
                score = max(score, 80)

            source_url = str(source.config.get("url", "")).strip().lower()
            if source_url and seed.startswith(source_url):
                score = max(score, 70)

            source_host = (urlparse(source_url).hostname or "").lower()
            if source_host and source._matches_host(source_host, host):
                score = max(score, 50)

            source_types = [part.strip() for part in source.source_type.split("|") if part.strip()]
            source_type_match = normalized_source_type in source_types
            if source_type_match and score < 20:
                score = max(score, 20)

            if score > 0:
                ranked.append((score, source))

        if ranked:
            ranked.sort(key=lambda item: (-item[0], item[1].name.lower(), item[1].id))
            _, chosen = ranked[0]
            return self._to_source_payload(chosen)

        fallback_host = host or (parsed.path[:30] if parsed.path else "")
        fallback_governance = _governance_from_raw({}, source_type, {"url": seed})
        return {
            "source_type": source_type,
            "name": (host or source_type) or "source",
            "config": {"url": seed, "seed_host": fallback_host},
            "governance": fallback_governance.to_dict(),
            "tags": [source_type],
            "match": {},
            "is_public": True,
            "tier": 2,
            "authority_weight": 0.5,
        }

    def _default_profile(self) -> str:
        return "default"

    def get_subscription(self, profile: str | None = None) -> list[str]:
        key = str(profile or self._default_profile())
        if key in self.subscriptions:
            return list(self.subscriptions[key])
        return []

    def list_subscriptions(self, profile: str | None = None) -> list[str]:
        return self.get_subscription(profile)

    def set_subscription(self, profile: str, source_ids: list[str]) -> list[str]:
        key = str(profile or self._default_profile())
        existing: list[str] = []
        for source_id in source_ids:
            sid = str(source_id).strip()
            if sid in self.sources:
                existing.append(sid)
        self.subscriptions[key] = existing
        self._save()
        return existing

    def subscribe(self, profile: str, source_id: str) -> bool:
        key = str(profile or self._default_profile())
        if source_id not in self.sources:
            return False
        items = self.subscriptions.setdefault(key, [])
        if source_id in items:
            return False
        items.append(source_id)
        self._save()
        return True

    def unsubscribe(self, profile: str, source_id: str) -> bool:
        key = str(profile or self._default_profile())
        items = self.subscriptions.get(key, [])
        if source_id not in items:
            return False
        self.subscriptions[key] = [x for x in items if x != source_id]
        self._save()
        return True

    def install_pack(self, profile: str, slug: str) -> int:
        pack = self.get_pack(slug)
        if not pack:
            return 0
        profile_key = str(profile or self._default_profile())
        ids = set(self.subscriptions.get(profile_key, []))
        added = 0
        for sid in pack.source_ids:
            if sid in self.sources and sid not in ids:
                ids.add(sid)
                added += 1
        self.subscriptions[profile_key] = sorted(ids)
        self._save()
        return added

    def register_auto_source(self, name: str, source_type: str, source_url: str) -> SourceRecord:
        sid = _item_id(f"{name}:{source_type}:{source_url}")
        if sid in self.sources:
            return self.sources[sid]

        source_type = _normalize_source_type(source_type)
        record = SourceRecord(
            id=sid,
            name=name,
            source_type=source_type,
            config={"url": source_url},
            governance=_governance_from_raw({}, source_type, {"url": source_url}),
            is_active=True,
            is_public=True,
            match={"url_prefix": source_url},
            tags=[source_type],
        )
        self._touch_timestamps(record, create=True)
        self.sources[sid] = record
        self._save()
        return record

    def filter_by_subscription(
        self,
        items: list[DataPulseItem],
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
    ) -> list[DataPulseItem]:
        if not items:
            return []

        if source_ids is None:
            source_ids = self.get_subscription(profile)
            if not source_ids:
                if self._bootstrapped_defaults and not self.subscriptions:
                    return items
                # fallback: all public active sources
                source_ids = [s.id for s in self.list_sources(include_inactive=False, public_only=True)]
            if not source_ids:
                return items

        target = set(source_ids)
        selected: list[DataPulseItem] = []
        for item in items:
            matched = False
            for source in self.sources.values():
                if source.id not in target or not source.is_active:
                    continue
                if source.matches(item):
                    matched = True
                    break
            if matched:
                selected.append(item)

        return selected
