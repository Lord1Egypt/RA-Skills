"""Persistent watch/mission definitions for recurring DataPulse workflows."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .utils import generate_slug, watchlist_path_from_env


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _dedup_lower(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = str(raw).strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def _dedup_text(values: list[Any]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = str(raw or "").strip()
        if not value:
            continue
        key = value.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


@dataclass
class MissionRun:
    mission_id: str
    status: str = "success"
    item_count: int = 0
    trigger: str = "manual"
    error: str = ""
    started_at: str = ""
    finished_at: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        if not self.started_at:
            self.started_at = _utcnow()
        if not self.finished_at:
            self.finished_at = self.started_at
        if not self.id:
            self.id = f"{self.mission_id}:{self.started_at}"
        self.status = (self.status or "success").strip().lower()
        self.trigger = (self.trigger or "manual").strip().lower()
        self.error = str(self.error or "").strip()
        try:
            self.item_count = max(0, int(self.item_count))
        except Exception:
            self.item_count = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MissionRun":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class MissionIntent:
    demand_intent: str = ""
    key_questions: list[str] = field(default_factory=list)
    scope_entities: list[str] = field(default_factory=list)
    scope_topics: list[str] = field(default_factory=list)
    scope_regions: list[str] = field(default_factory=list)
    scope_window: str = ""
    freshness_expectation: str = ""
    freshness_max_age_hours: int = 0
    coverage_targets: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.demand_intent = str(self.demand_intent or "").strip()
        self.key_questions = _dedup_text(self.key_questions)
        self.scope_entities = _dedup_text(self.scope_entities)
        self.scope_topics = _dedup_text(self.scope_topics)
        self.scope_regions = _dedup_text(self.scope_regions)
        self.scope_window = str(self.scope_window or "").strip()
        self.freshness_expectation = str(self.freshness_expectation or "").strip()
        try:
            self.freshness_max_age_hours = max(0, int(self.freshness_max_age_hours))
        except Exception:
            self.freshness_max_age_hours = 0
        self.coverage_targets = _dedup_text(self.coverage_targets)

    def has_content(self) -> bool:
        return any(
            (
                self.demand_intent,
                self.key_questions,
                self.scope_entities,
                self.scope_topics,
                self.scope_regions,
                self.scope_window,
                self.freshness_expectation,
                self.freshness_max_age_hours > 0,
                self.coverage_targets,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MissionIntent":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class TrendFeedInput:
    provider: str = ""
    label: str = ""
    location: str = ""
    topics: list[str] = field(default_factory=list)
    feed_url: str = ""
    snapshot_time: str = ""
    input_kind: str = "trend_feed"
    usage_mode: str = "watch_seed_only"
    notes: str = ""

    def __post_init__(self) -> None:
        self.provider = str(self.provider or "").strip().lower()
        self.label = str(self.label or "").strip()
        self.location = str(self.location or "").strip()
        self.topics = _dedup_text(self.topics)
        self.feed_url = str(self.feed_url or "").strip()
        self.snapshot_time = str(self.snapshot_time or "").strip()
        self.input_kind = "trend_feed"
        self.usage_mode = "watch_seed_only"
        self.notes = str(self.notes or "").strip()

    def has_content(self) -> bool:
        return any(
            (
                self.label,
                self.location,
                self.topics,
                self.feed_url,
                self.snapshot_time,
                self.notes,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrendFeedInput":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


@dataclass
class WatchMission:
    name: str
    query: str
    mission_intent: MissionIntent = field(default_factory=MissionIntent)
    trend_inputs: list[TrendFeedInput] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    sites: list[str] = field(default_factory=list)
    schedule: str = "manual"
    min_confidence: float = 0.0
    top_n: int = 5
    alert_rules: list[dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""
    last_run_at: str = ""
    last_run_count: int = 0
    last_run_status: str = ""
    last_run_error: str = ""
    runs: list[MissionRun] = field(default_factory=list)
    id: str = ""

    def __post_init__(self) -> None:
        self.name = str(self.name or "").strip()
        self.query = str(self.query or "").strip()
        if not self.name:
            raise ValueError("Watch mission name is required")
        if not self.query:
            raise ValueError("Watch mission query is required")
        if not self.id:
            self.id = generate_slug(self.name, max_length=48)
        now = _utcnow()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = self.created_at
        if isinstance(self.mission_intent, MissionIntent):
            normalized_intent = self.mission_intent
        elif isinstance(self.mission_intent, dict):
            normalized_intent = MissionIntent.from_dict(self.mission_intent)
        else:
            normalized_intent = MissionIntent()
        self.mission_intent = normalized_intent
        normalized_trend_inputs: list[TrendFeedInput] = []
        seen_trend_inputs: set[tuple[str, str, str, tuple[str, ...], str, str]] = set()
        for trend_raw in self.trend_inputs:
            if isinstance(trend_raw, TrendFeedInput):
                trend_input = trend_raw
            elif isinstance(trend_raw, dict):
                try:
                    trend_input = TrendFeedInput.from_dict(trend_raw)
                except (TypeError, ValueError):
                    continue
            else:
                continue
            if not trend_input.has_content():
                continue
            signature = (
                trend_input.provider.casefold(),
                trend_input.label.casefold(),
                trend_input.location.casefold(),
                tuple(topic.casefold() for topic in trend_input.topics),
                trend_input.feed_url.casefold(),
                trend_input.snapshot_time,
            )
            if signature in seen_trend_inputs:
                continue
            seen_trend_inputs.add(signature)
            normalized_trend_inputs.append(trend_input)
        self.trend_inputs = normalized_trend_inputs
        self.platforms = _dedup_lower(self.platforms)
        self.sites = _dedup_lower(self.sites)
        self.schedule = str(self.schedule or "manual").strip().lower() or "manual"
        try:
            self.min_confidence = max(0.0, min(1.0, float(self.min_confidence)))
        except Exception:
            self.min_confidence = 0.0
        try:
            self.top_n = max(1, int(self.top_n))
        except Exception:
            self.top_n = 5
        self.alert_rules = [
            rule for rule in self.alert_rules
            if isinstance(rule, dict)
        ]
        self.enabled = bool(self.enabled)
        normalized_runs: list[MissionRun] = []
        for run_raw in self.runs:
            if isinstance(run_raw, MissionRun):
                normalized_runs.append(run_raw)
            elif isinstance(run_raw, dict):
                try:
                    normalized_runs.append(MissionRun.from_dict(run_raw))
                except (TypeError, ValueError):
                    continue
        self.runs = normalized_runs[:10]
        try:
            self.last_run_count = max(0, int(self.last_run_count))
        except Exception:
            self.last_run_count = 0
        self.last_run_status = str(self.last_run_status or "").strip().lower()
        self.last_run_error = str(self.last_run_error or "").strip()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["runs"] = [run.to_dict() for run in self.runs]
        payload["mission_intent"] = (
            self.mission_intent.to_dict()
            if self.mission_intent.has_content()
            else {}
        )
        payload["trend_inputs"] = [trend_input.to_dict() for trend_input in self.trend_inputs]
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WatchMission":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        payload = {k: v for k, v in data.items() if k in valid}
        payload["trend_inputs"] = [
            TrendFeedInput.from_dict(row)
            for row in payload.get("trend_inputs", [])
            if isinstance(row, dict)
        ]
        payload["runs"] = [
            MissionRun.from_dict(run)
            for run in payload.get("runs", [])
            if isinstance(run, dict)
        ]
        return cls(**payload)


class WatchlistStore:
    """File-backed storage for recurring watch missions."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or watchlist_path_from_env()).expanduser()
        self.version = 1
        self.missions: dict[str, WatchMission] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.missions = {}
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.missions = {}
            return
        mission_rows: list[dict[str, Any]]
        if isinstance(raw, dict):
            self.version = int(raw.get("version", 1) or 1)
            source_rows = raw.get("missions", [])
            mission_rows = source_rows if isinstance(source_rows, list) else []
        elif isinstance(raw, list):
            mission_rows = raw
        else:
            self.missions = {}
            return

        loaded: dict[str, WatchMission] = {}
        for row in mission_rows:
            if not isinstance(row, dict):
                continue
            try:
                mission = WatchMission.from_dict(row)
            except (TypeError, ValueError):
                continue
            loaded[mission.id] = mission
        self.missions = loaded

    def save(self) -> None:
        payload = {
            "version": self.version,
            "missions": [mission.to_dict() for mission in self.list_missions(include_disabled=True)],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_missions(self, *, include_disabled: bool = False) -> list[WatchMission]:
        missions = list(self.missions.values())
        if not include_disabled:
            missions = [mission for mission in missions if mission.enabled]
        return sorted(
            missions,
            key=lambda mission: (mission.updated_at, mission.created_at, mission.id),
            reverse=True,
        )

    def _next_id(self, base_id: str) -> str:
        candidate = (base_id or "watch").strip() or "watch"
        if candidate not in self.missions:
            return candidate
        suffix = 2
        while f"{candidate}-{suffix}" in self.missions:
            suffix += 1
        return f"{candidate}-{suffix}"

    def create_mission(
        self,
        *,
        name: str,
        query: str,
        mission_intent: dict[str, Any] | MissionIntent | None = None,
        trend_inputs: list[dict[str, Any] | TrendFeedInput] | None = None,
        platforms: list[str] | None = None,
        sites: list[str] | None = None,
        schedule: str = "manual",
        min_confidence: float = 0.0,
        top_n: int = 5,
        alert_rules: list[dict[str, Any]] | None = None,
        enabled: bool = True,
    ) -> WatchMission:
        normalized_mission_intent = (
            mission_intent
            if isinstance(mission_intent, MissionIntent)
            else MissionIntent.from_dict(mission_intent)
            if isinstance(mission_intent, dict)
            else MissionIntent()
        )
        normalized_trend_inputs: list[TrendFeedInput] = []
        for trend_raw in trend_inputs or []:
            if isinstance(trend_raw, TrendFeedInput):
                trend_input = trend_raw
            elif isinstance(trend_raw, dict):
                try:
                    trend_input = TrendFeedInput.from_dict(trend_raw)
                except (TypeError, ValueError):
                    continue
            else:
                continue
            if trend_input.has_content():
                normalized_trend_inputs.append(trend_input)
        mission = WatchMission(
            name=name,
            query=query,
            mission_intent=normalized_mission_intent,
            trend_inputs=normalized_trend_inputs,
            platforms=list(platforms or []),
            sites=list(sites or []),
            schedule=schedule,
            min_confidence=min_confidence,
            top_n=top_n,
            alert_rules=list(alert_rules or []),
            enabled=enabled,
        )
        mission.id = self._next_id(mission.id)
        mission.updated_at = mission.created_at
        self.missions[mission.id] = mission
        self.save()
        return mission

    def update_mission(
        self,
        identifier: str,
        *,
        name: str | None = None,
        query: str | None = None,
        mission_intent: dict[str, Any] | MissionIntent | None = None,
        trend_inputs: list[dict[str, Any] | TrendFeedInput] | None = None,
        platforms: list[str] | None = None,
        sites: list[str] | None = None,
        schedule: str | None = None,
        min_confidence: float | None = None,
        top_n: int | None = None,
        alert_rules: list[dict[str, Any]] | None = None,
        enabled: bool | None = None,
    ) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        updated = WatchMission(
            id=mission.id,
            name=mission.name if name is None else name,
            query=mission.query if query is None else query,
            mission_intent=mission.mission_intent if mission_intent is None else mission_intent,
            trend_inputs=mission.trend_inputs if trend_inputs is None else trend_inputs,
            platforms=mission.platforms if platforms is None else list(platforms),
            sites=mission.sites if sites is None else list(sites),
            schedule=mission.schedule if schedule is None else schedule,
            min_confidence=mission.min_confidence if min_confidence is None else min_confidence,
            top_n=mission.top_n if top_n is None else top_n,
            alert_rules=mission.alert_rules if alert_rules is None else list(alert_rules),
            enabled=mission.enabled if enabled is None else enabled,
            created_at=mission.created_at,
            updated_at=_utcnow(),
            last_run_at=mission.last_run_at,
            last_run_count=mission.last_run_count,
            last_run_status=mission.last_run_status,
            last_run_error=mission.last_run_error,
            runs=list(mission.runs),
        )
        self.missions[mission.id] = updated
        self.save()
        return updated

    def get(self, identifier: str) -> WatchMission | None:
        key = str(identifier or "").strip()
        if not key:
            return None
        if key in self.missions:
            return self.missions[key]
        normalized = key.casefold()
        for mission in self.missions.values():
            if mission.name.casefold() == normalized:
                return mission
        return None

    def disable(self, identifier: str) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        mission.enabled = False
        mission.updated_at = _utcnow()
        self.save()
        return mission

    def enable(self, identifier: str) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        mission.enabled = True
        mission.updated_at = _utcnow()
        self.save()
        return mission

    def delete(self, identifier: str) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        removed = self.missions.pop(mission.id, None)
        if removed is None:
            return None
        self.save()
        return removed

    def replace_alert_rules(self, identifier: str, alert_rules: list[dict[str, Any]] | None) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        mission.alert_rules = [
            dict(rule)
            for rule in list(alert_rules or [])
            if isinstance(rule, dict)
        ]
        mission.updated_at = _utcnow()
        self.save()
        return mission

    def record_run(self, identifier: str, run: MissionRun) -> WatchMission | None:
        mission = self.get(identifier)
        if mission is None:
            return None
        mission.last_run_at = run.finished_at or run.started_at
        mission.last_run_count = run.item_count
        mission.last_run_status = run.status
        mission.last_run_error = run.error
        mission.updated_at = mission.last_run_at or _utcnow()
        mission.runs.insert(0, run)
        mission.runs = mission.runs[:10]
        self.save()
        return mission
