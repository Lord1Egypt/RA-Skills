"""Main DataPulse reader API."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, cast
from urllib.parse import urlparse

from datapulse.collectors.trending import TrendingCollector, build_trending_url
from datapulse.core.alerts import AlertRouteStore, AlertStore, dispatch_alert_event, evaluate_watch_alerts
from datapulse.core.confidence import compute_confidence
from datapulse.core.entities import Entity, Relation
from datapulse.core.entities import extract_entities as extract_entities_text
from datapulse.core.entity_store import EntityStore
from datapulse.core.jina_client import JinaSearchOptions
from datapulse.core.models import DataPulseItem, SourceType
from datapulse.core.ops import WatchStatusStore
from datapulse.core.router import ParsePipeline
from datapulse.core.scheduler import WatchDaemon, WatchScheduler, describe_schedule, is_watch_due, next_run_at
from datapulse.core.scoring import rank_items
from datapulse.core.search_gateway import SearchGateway, SearchHit
from datapulse.core.source_catalog import SourceCatalog
from datapulse.core.storage import UnifiedInbox, output_record_md, project_markdown
from datapulse.core.story import (
    StoryStore,
    build_factuality_gate,
    build_story_from_items,
    build_story_clusters,
    build_story_graph,
    render_story_markdown,
    resolve_factuality_gate_status,
)
from datapulse.core.triage import (
    TriageQueue,
    is_digest_candidate,
    normalize_review_state,
    serialize_item_with_governance,
)
from datapulse.core.utils import content_fingerprint, inbox_path_from_env, normalize_language
from datapulse.core.watchlist import MissionIntent, MissionRun, TrendFeedInput, WatchlistStore, WatchMission

logger = logging.getLogger("datapulse.reader")


def _utcnow_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _parse_timestamp(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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
        value = str(raw or "").strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return normalized


def _normalize_route_names(rule: dict[str, Any]) -> list[str]:
    names = _normalize_string_list(rule.get("routes"))
    if names:
        return names
    return _normalize_string_list(rule.get("route"))


PLATFORM_SEARCH_SITES: dict[str, list[str]] = {
    "xhs": ["xiaohongshu.com", "xhslink.com"],
    "twitter": ["x.com", "twitter.com"],
    "reddit": ["reddit.com"],
    "hackernews": ["news.ycombinator.com"],
    "arxiv": ["arxiv.org"],
    "bilibili": ["bilibili.com"],
}

TREND_SEED_BOUNDARY_TEXT = (
    "Trend inputs seed watches and feed surfaces only; item-level evidence still comes from collected URLs and search hits."
)


class DataPulseReader:
    """End-to-end URL reader used by CLI/MCP/Skill/Agent."""

    def __init__(self, inbox_path: str | None = None):
        self.router = ParsePipeline()
        self.inbox = UnifiedInbox(inbox_path or inbox_path_from_env())
        self.catalog = SourceCatalog()
        self.watchlist = WatchlistStore()
        self.watch_scheduler = WatchScheduler(self.watchlist)
        self.triage = TriageQueue(self.inbox)
        self.story_store = StoryStore()
        self.alert_store = AlertStore()
        self.alert_routes = AlertRouteStore()
        self.watch_status = WatchStatusStore()
        self._search_gateway = SearchGateway()
        self._jina_client = self._search_gateway._jina_client
        self._entity_store: EntityStore | None = None

    @property
    def entity_store(self) -> EntityStore:
        if self._entity_store is None:
            self._entity_store = EntityStore()
        return self._entity_store

    def _serialize_watch_mission(self, mission: WatchMission) -> dict[str, Any]:
        payload = mission.to_dict()
        payload["intent_summary"] = self._build_watch_intent_summary(mission.mission_intent)
        payload["trend_inputs"] = [
            self._serialize_trend_input(trend_input)
            for trend_input in mission.trend_inputs
        ]
        payload["trend_seed_summary"] = self._build_watch_trend_summary(mission.trend_inputs)
        payload["schedule_label"] = describe_schedule(mission.schedule)
        payload["is_due"] = is_watch_due(mission)
        payload["next_run_at"] = next_run_at(mission)
        payload["alert_rule_count"] = len(mission.alert_rules)
        success_runs = sum(1 for run in mission.runs if run.status == "success")
        error_runs = sum(1 for run in mission.runs if run.status != "success")
        average_items = 0.0
        if mission.runs:
            average_items = round(
                sum(run.item_count for run in mission.runs) / len(mission.runs),
                2,
            )
        payload["run_stats"] = {
            "total": len(mission.runs),
            "success": success_runs,
            "error": error_runs,
            "average_items": average_items,
            "last_status": mission.last_run_status or "",
            "last_error": mission.last_run_error or "",
        }
        return payload

    @staticmethod
    def _build_watch_intent_summary(intent: MissionIntent) -> dict[str, Any]:
        def _preview(values: list[str], *, limit: int = 3) -> str:
            if not values:
                return ""
            visible = values[:limit]
            preview = ", ".join(visible)
            if len(values) > limit:
                preview = f"{preview}, +{len(values) - limit} more"
            return preview

        scope_parts: list[str] = []
        if intent.scope_entities:
            scope_parts.append(f"entities={_preview(intent.scope_entities)}")
        if intent.scope_topics:
            scope_parts.append(f"topics={_preview(intent.scope_topics)}")
        if intent.scope_regions:
            scope_parts.append(f"regions={_preview(intent.scope_regions)}")
        if intent.scope_window:
            scope_parts.append(f"window={intent.scope_window}")

        freshness_parts: list[str] = []
        if intent.freshness_expectation:
            freshness_parts.append(intent.freshness_expectation)
        if intent.freshness_max_age_hours > 0:
            freshness_parts.append(f"max_age<={intent.freshness_max_age_hours}h")

        coverage_preview = _preview(intent.coverage_targets)
        return {
            "has_intent": intent.has_content(),
            "demand_intent": intent.demand_intent,
            "key_questions": list(intent.key_questions),
            "scope": " | ".join(scope_parts),
            "freshness": " | ".join(freshness_parts),
            "coverage": coverage_preview,
            "coverage_target_count": len(intent.coverage_targets),
        }

    @staticmethod
    def _serialize_trend_input(trend_input: TrendFeedInput) -> dict[str, Any]:
        payload = trend_input.to_dict()
        payload["topic_count"] = len(trend_input.topics)
        payload["topics_preview"] = list(trend_input.topics[:5])
        return payload

    def _build_watch_trend_summary(self, trend_inputs: list[TrendFeedInput]) -> dict[str, Any]:
        providers: list[str] = []
        provider_seen: set[str] = set()
        locations: list[str] = []
        location_seen: set[str] = set()
        topics: list[str] = []
        topic_seen: set[str] = set()
        latest_snapshot = ""

        for trend_input in trend_inputs:
            provider = str(trend_input.provider or "").strip().lower()
            if provider and provider not in provider_seen:
                provider_seen.add(provider)
                providers.append(provider)
            location = str(trend_input.location or "").strip()
            location_key = location.casefold()
            if location and location_key not in location_seen:
                location_seen.add(location_key)
                locations.append(location)
            snapshot_time = str(trend_input.snapshot_time or "").strip()
            if snapshot_time and snapshot_time > latest_snapshot:
                latest_snapshot = snapshot_time
            for topic in trend_input.topics:
                normalized = str(topic or "").strip()
                if not normalized:
                    continue
                key = normalized.casefold()
                if key in topic_seen:
                    continue
                topic_seen.add(key)
                topics.append(normalized)

        return {
            "has_trend_inputs": bool(trend_inputs),
            "input_count": len(trend_inputs),
            "provider_count": len(providers),
            "providers": providers,
            "locations": locations,
            "topic_count": len(topics),
            "topics_preview": topics[:5],
            "latest_snapshot_time": latest_snapshot,
            "seed_boundary": TREND_SEED_BOUNDARY_TEXT if trend_inputs else "",
        }

    @staticmethod
    def _latest_failed_run(mission: WatchMission) -> MissionRun | None:
        return next((run for run in mission.runs if run.status != "success"), None)

    @staticmethod
    def _classify_watch_failure(error: str) -> tuple[str, str, list[str]]:
        message = str(error or "").strip()
        text = message.lower()
        if not text:
            return "", "", []
        if (
            "api key" in text
            or "apikey" in text
            or "api-key" in text
            or "unauthorized" in text
            or "authentication" in text
            or "credentials" in text
            or "login" in text
            or "session" in text
        ):
            return (
                "credentials",
                "The last failed run looks blocked by missing credentials or an expired session.",
                ["Validate upstream API keys or platform login state before rerunning."],
            )
        if "429" in text or "rate limit" in text or "too many requests" in text:
            return (
                "rate_limit",
                "The last failed run looks rate-limited by an upstream provider.",
                ["Wait for the upstream cooldown window, then rerun the mission once."],
            )
        if (
            "timeout" in text
            or "timed out" in text
            or "temporary" in text
            or "connection" in text
            or "network" in text
            or "reset by peer" in text
        ):
            return (
                "transient",
                "The last failed run looks like a transient upstream or network failure.",
                ["A manual rerun is usually safe once the upstream recovers."],
            )
        return (
            "unknown",
            "The last failed run needs manual inspection before retry.",
            ["Review the recorded error and collector health below before rerunning."],
        )

    def _doctor_lookup(self) -> dict[str, dict[str, Any]]:
        lookup: dict[str, dict[str, Any]] = {}
        try:
            report = self.doctor()
        except Exception:
            return lookup
        for tier_name, entries in report.items():
            for raw in entries:
                if not isinstance(raw, dict):
                    continue
                name = str(raw.get("name", "")).strip().lower()
                if not name:
                    continue
                entry = dict(raw)
                entry["tier"] = tier_name
                lookup[name] = entry
        return lookup

    def _watch_retry_advice(
        self,
        mission: WatchMission,
        failed_run: MissionRun | None,
    ) -> dict[str, Any] | None:
        if failed_run is None:
            return None

        failure_class, summary, notes = self._classify_watch_failure(failed_run.error)
        doctor_lookup = self._doctor_lookup()
        error_text = str(failed_run.error or "").lower()
        candidate_names = set(_normalize_string_list(mission.platforms))
        candidate_names.update(
            name
            for name in doctor_lookup
            if name and name in error_text
        )
        if not candidate_names and ("jina" in error_text or "search" in error_text):
            candidate_names.add("jina")

        suspected_collectors: list[dict[str, Any]] = []
        for name in sorted(candidate_names):
            entry = doctor_lookup.get(name)
            if not entry:
                continue
            status_name = str(entry.get("status", "ok")).strip().lower() or "ok"
            available = bool(entry.get("available", True))
            if status_name == "ok" and available:
                continue
            suspected_collectors.append(
                {
                    "name": name,
                    "tier": entry.get("tier", ""),
                    "status": status_name,
                    "available": available,
                    "message": str(entry.get("message", "") or "").strip(),
                    "setup_hint": str(entry.get("setup_hint", "") or "").strip(),
                }
            )

        if suspected_collectors:
            notes.append("Fix the degraded collector setup below before rerunning the mission.")
        elif failure_class == "unknown":
            notes.append("Retry manually after confirming collector health and query scope.")

        advice = {
            "failure_class": failure_class,
            "summary": summary,
            "retry_command": f"datapulse --watch-run {mission.id}",
            "daemon_retry_command": "datapulse --watch-daemon --watch-daemon-once" if mission.schedule != "manual" else "",
            "suspected_collectors": suspected_collectors,
            "notes": notes,
        }
        return advice

    def _watch_health_snapshot(
        self,
        *,
        limit: int | None = None,
    ) -> tuple[dict[str, int], list[dict[str, Any]]]:
        summary = {
            "total": 0,
            "enabled": 0,
            "disabled": 0,
            "healthy": 0,
            "degraded": 0,
            "idle": 0,
            "due": 0,
        }
        rows: list[dict[str, Any]] = []

        for mission in self.watchlist.list_missions(include_disabled=True):
            payload = self._serialize_watch_mission(mission)
            run_stats = payload.get("run_stats", {})
            run_total = int(run_stats.get("total", 0) or 0)
            success_total = int(run_stats.get("success", 0) or 0)
            error_total = int(run_stats.get("error", 0) or 0)
            success_rate = round(success_total / run_total, 3) if run_total > 0 else None
            is_due = bool(payload.get("is_due", False))

            if not mission.enabled:
                health_status = "disabled"
            elif run_total <= 0:
                health_status = "idle"
            elif str(mission.last_run_status or "").strip().lower() == "success":
                health_status = "healthy"
            else:
                health_status = "degraded"

            summary["total"] += 1
            if mission.enabled:
                summary["enabled"] += 1
                if is_due:
                    summary["due"] += 1
            else:
                summary["disabled"] += 1
            if health_status in {"healthy", "degraded", "idle"}:
                summary[health_status] += 1

            rows.append(
                {
                    "id": mission.id,
                    "name": mission.name,
                    "enabled": mission.enabled,
                    "status": health_status,
                    "is_due": is_due,
                    "schedule_label": payload.get("schedule_label", "manual"),
                    "next_run_at": payload.get("next_run_at", ""),
                    "last_run_at": mission.last_run_at,
                    "last_run_status": mission.last_run_status or "",
                    "last_run_error": mission.last_run_error or "",
                    "alert_rule_count": len(mission.alert_rules),
                    "run_total": run_total,
                    "success_total": success_total,
                    "error_total": error_total,
                    "success_rate": success_rate,
                    "average_items": run_stats.get("average_items", 0.0),
                }
            )

        severity = {"degraded": 0, "healthy": 1, "idle": 2, "disabled": 3}
        rows.sort(
            key=lambda row: (
                severity.get(str(row.get("status", "idle")), 99),
                0 if row.get("is_due", False) else 1,
                -(_parse_timestamp(row.get("last_run_at")) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
                str(row.get("id", "")),
            )
        )
        if limit is not None:
            rows = rows[: max(0, int(limit))]
        return summary, rows

    @staticmethod
    def _scorecard_signal(
        *,
        signal_id: str,
        label: str,
        status: str,
        value: float | None,
        unit: str,
        display: str,
        detail: str,
        **extra: Any,
    ) -> dict[str, Any]:
        payload = {
            "id": signal_id,
            "label": label,
            "status": status,
            "value": round(value, 4) if isinstance(value, (int, float)) else None,
            "unit": unit,
            "display": display,
            "detail": detail,
        }
        payload.update(extra)
        return payload

    @staticmethod
    def _normalize_scorecard_label(value: Any) -> str:
        text = str(value or "").strip().casefold()
        if text.startswith("www."):
            text = text[4:]
        return text

    @classmethod
    def _coverage_expectations(cls, mission: WatchMission) -> list[dict[str, str]]:
        expected: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()

        def add(kind: str, raw: Any) -> None:
            label = str(raw or "").strip()
            key = cls._normalize_scorecard_label(label)
            if not key:
                return
            marker = (kind, key)
            if marker in seen:
                return
            seen.add(marker)
            expected.append({"kind": kind, "label": label, "key": key})

        for platform in mission.platforms:
            add("platform", platform)
        for site in mission.sites:
            add("site", site)
        for target in mission.mission_intent.coverage_targets:
            add("coverage_target", target)
        return expected

    @classmethod
    def _coverage_observation_labels(cls, item: DataPulseItem) -> set[str]:
        labels: set[str] = set()
        for raw in [item.source_name, item.source_type.value, item.parser, *item.tags]:
            key = cls._normalize_scorecard_label(raw)
            if key:
                labels.add(key)
        try:
            domain = str(urlparse(str(item.url or "")).netloc or "").strip().lower()
        except ValueError:
            domain = ""
        if domain.startswith("www."):
            domain = domain[4:]
        if domain:
            labels.add(domain)
        for raw in _normalize_string_list(item.extra.get("search_sources")):
            key = cls._normalize_scorecard_label(raw)
            if key:
                labels.add(key)
            try:
                source_domain = str(urlparse(raw).netloc or "").strip().lower()
            except ValueError:
                source_domain = ""
            if source_domain.startswith("www."):
                source_domain = source_domain[4:]
            if source_domain:
                labels.add(source_domain)
        return labels

    @classmethod
    def _coverage_target_hit(cls, target: str, observed_labels: set[str]) -> bool:
        if not target:
            return False
        if target in observed_labels:
            return True
        if len(target) < 4:
            return False
        return any(target in candidate or candidate in target for candidate in observed_labels)

    def governance_scorecard_snapshot(self) -> dict[str, Any]:
        enabled_missions = self.watchlist.list_missions(include_disabled=False)
        all_missions = self.watchlist.list_missions(include_disabled=True)
        all_items = list(self.inbox.items)
        all_stories = self.story_store.list_stories(limit=5000, min_items=1)
        triage_stats = self.triage.stats()
        enabled_mission_ids = {mission.id for mission in enabled_missions}
        now = datetime.now(timezone.utc)

        mission_items: dict[str, list[DataPulseItem]] = {}
        for item in all_items:
            mission_id = str(item.extra.get("watch_mission_id", "") or "").strip()
            if not mission_id:
                continue
            mission_items.setdefault(mission_id, []).append(item)

        coverage_expected_total = 0
        coverage_hit_total = 0
        missions_with_targets = 0
        missions_without_targets = 0
        uncovered_targets: list[dict[str, Any]] = []
        for mission in enabled_missions:
            expected = self._coverage_expectations(mission)
            if not expected:
                missions_without_targets += 1
                continue
            missions_with_targets += 1
            observed_labels: set[str] = set()
            for item in mission_items.get(mission.id, []):
                observed_labels.update(self._coverage_observation_labels(item))
            for row in expected:
                coverage_expected_total += 1
                if self._coverage_target_hit(row["key"], observed_labels):
                    coverage_hit_total += 1
                    continue
                uncovered_targets.append(
                    {
                        "mission_id": mission.id,
                        "mission_name": mission.name,
                        "kind": row["kind"],
                        "target": row["label"],
                    }
                )
        coverage_rate = (
            round(coverage_hit_total / coverage_expected_total, 4)
            if coverage_expected_total > 0
            else None
        )
        coverage_signal = self._scorecard_signal(
            signal_id="coverage",
            label="Coverage",
            status=(
                "missing"
                if coverage_expected_total <= 0
                else "ok"
                if (coverage_rate or 0.0) >= 0.7
                else "watch"
            ),
            value=coverage_rate,
            unit="ratio",
            display=(
                "No coverage touchpoint declared on enabled missions."
                if coverage_expected_total <= 0
                else f"{coverage_hit_total}/{coverage_expected_total} declared touchpoints observed"
            ),
            detail="Matches enabled mission platforms, sites, and coverage_targets against persisted watch results.",
            expected_targets_total=coverage_expected_total,
            covered_targets_total=coverage_hit_total,
            missions_with_targets=missions_with_targets,
            missions_without_targets=missions_without_targets,
            uncovered_targets=uncovered_targets[:8],
        )

        freshness_sla_missions = 0
        freshness_text_only_missions = 0
        fresh_missions = 0
        stale_missions: list[dict[str, Any]] = []
        missing_freshness_results = 0
        for mission in enabled_missions:
            max_age_hours = max(0, int(mission.mission_intent.freshness_max_age_hours or 0))
            if max_age_hours <= 0:
                if mission.mission_intent.freshness_expectation:
                    freshness_text_only_missions += 1
                continue
            freshness_sla_missions += 1
            latest_result = max(
                mission_items.get(mission.id, []),
                key=lambda item: (_parse_timestamp(item.fetched_at) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
                default=None,
            )
            latest_ts = _parse_timestamp(getattr(latest_result, "fetched_at", "")) if latest_result is not None else None
            if latest_ts is None:
                missing_freshness_results += 1
                stale_missions.append(
                    {
                        "mission_id": mission.id,
                        "mission_name": mission.name,
                        "freshness_max_age_hours": max_age_hours,
                        "latest_result_at": "",
                        "age_hours": None,
                    }
                )
                continue
            assert latest_result is not None
            age_hours = round(max(0.0, (now - latest_ts).total_seconds() / 3600), 2)
            if age_hours <= max_age_hours:
                fresh_missions += 1
                continue
            stale_missions.append(
                {
                    "mission_id": mission.id,
                    "mission_name": mission.name,
                    "freshness_max_age_hours": max_age_hours,
                    "latest_result_at": latest_result.fetched_at,
                    "age_hours": age_hours,
                }
            )
        freshness_rate = (
            round(fresh_missions / freshness_sla_missions, 4)
            if freshness_sla_missions > 0
            else None
        )
        freshness_signal = self._scorecard_signal(
            signal_id="freshness",
            label="Freshness",
            status=(
                "missing"
                if freshness_sla_missions <= 0
                else "ok"
                if (freshness_rate or 0.0) >= 0.7
                else "watch"
            ),
            value=freshness_rate,
            unit="ratio",
            display=(
                "No mission defines a numeric freshness SLA yet."
                if freshness_sla_missions <= 0
                else f"{fresh_missions}/{freshness_sla_missions} SLA-backed missions are fresh"
            ),
            detail="Uses mission_intent.freshness_max_age_hours and each mission's latest persisted result timestamp.",
            missions_with_sla=freshness_sla_missions,
            missions_with_text_only_expectation=freshness_text_only_missions,
            fresh_missions=fresh_missions,
            stale_missions=max(0, freshness_sla_missions - fresh_missions),
            missing_results=missing_freshness_results,
            stale_mission_detail=stale_missions[:8],
        )

        successful_runs = sum(
            1
            for mission in enabled_missions
            for run in mission.runs
            if str(run.status or "").strip().lower() == "success"
        )
        alert_events = [
            event
            for event in self.alert_store.events
            if event.mission_id in enabled_mission_ids
        ]
        alert_count = len(alert_events)
        alerting_missions = len({event.mission_id for event in alert_events if str(event.mission_id or "").strip()})
        alert_yield_rate = round(alert_count / successful_runs, 4) if successful_runs > 0 else None
        alert_yield_signal = self._scorecard_signal(
            signal_id="alert_yield",
            label="Alert Yield",
            status=(
                "missing"
                if successful_runs <= 0
                else "watch"
                if alert_count <= 0 or (alert_yield_rate or 0.0) > 1.5
                else "ok"
            ),
            value=alert_yield_rate,
            unit="alerts_per_successful_run",
            display=(
                "No successful mission run recorded yet."
                if successful_runs <= 0
                else f"{alert_count} alerts across {successful_runs} successful runs"
            ),
            detail="Compares persisted AlertEvent rows against successful MissionRun records for enabled missions.",
            alert_count=alert_count,
            successful_runs=successful_runs,
            alerting_missions=alerting_missions,
        )

        triage_total = int(triage_stats.get("total", 0) or 0)
        triage_states = triage_stats.get("states", {}) if isinstance(triage_stats.get("states"), dict) else {}
        new_items = int(triage_states.get("new", 0) or 0)
        triage_acted_on = max(0, triage_total - new_items)
        triage_closed = int(triage_stats.get("closed_count", 0) or 0)
        triage_rate = round(triage_acted_on / triage_total, 4) if triage_total > 0 else None
        closed_rate = round(triage_closed / triage_total, 4) if triage_total > 0 else None
        triage_signal = self._scorecard_signal(
            signal_id="triage_throughput",
            label="Triage Throughput",
            status=(
                "missing"
                if triage_total <= 0
                else "ok"
                if (triage_rate or 0.0) >= 0.6 or (closed_rate or 0.0) >= 0.35
                else "watch"
            ),
            value=triage_rate,
            unit="acted_item_ratio",
            display=(
                "No inbox item has entered triage yet."
                if triage_total <= 0
                else f"{triage_acted_on}/{triage_total} items moved beyond new"
            ),
            detail="Measures how much of the persisted inbox has received analyst triage state changes or notes.",
            total_items=triage_total,
            acted_on_items=triage_acted_on,
            closed_items=triage_closed,
            open_items=int(triage_stats.get("open_count", 0) or 0),
            note_count=int(triage_stats.get("note_count", 0) or 0),
            closed_rate=closed_rate,
        )

        story_item_ids = {
            str(evidence.item_id or "").strip()
            for story in all_stories
            for evidence in [*story.primary_evidence, *story.secondary_evidence]
            if str(evidence.item_id or "").strip()
        }
        delivery_ready_stories = 0
        for story in all_stories:
            governance = story.governance if isinstance(story.governance, dict) else {}
            delivery_risk = governance.get("delivery_risk", {}) if isinstance(governance.get("delivery_risk"), dict) else {}
            if str(delivery_risk.get("status", "") or "").strip().lower() == "ready":
                delivery_ready_stories += 1
        eligible_story_items = [
            item
            for item in all_items
            if normalize_review_state(item.review_state, processed=item.processed) in {"triaged", "verified", "escalated"}
        ]
        eligible_story_item_ids = {
            str(item.id or "").strip()
            for item in eligible_story_items
            if str(item.id or "").strip()
        }
        converted_story_items = len(eligible_story_item_ids & story_item_ids)
        story_conversion_rate = (
            round(converted_story_items / len(eligible_story_item_ids), 4)
            if eligible_story_item_ids
            else None
        )
        story_signal = self._scorecard_signal(
            signal_id="story_conversion",
            label="Story Conversion",
            status=(
                "missing"
                if not eligible_story_item_ids
                else "ok"
                if (story_conversion_rate or 0.0) >= 0.4
                else "watch"
            ),
            value=story_conversion_rate,
            unit="conversion_ratio",
            display=(
                "No triaged item is ready for story conversion yet."
                if not eligible_story_item_ids
                else f"{converted_story_items}/{len(eligible_story_item_ids)} triaged items referenced by stories"
            ),
            detail="Tracks how much reviewed evidence is already represented in persisted story objects.",
            story_count=len(all_stories),
            ready_story_count=delivery_ready_stories,
            eligible_item_count=len(eligible_story_item_ids),
            converted_item_count=converted_story_items,
        )

        signals = {
            signal["id"]: signal
            for signal in (
                coverage_signal,
                freshness_signal,
                alert_yield_signal,
                triage_signal,
                story_signal,
            )
        }
        status_counts = {"ok": 0, "watch": 0, "missing": 0}
        for signal in signals.values():
            status_name = str(signal.get("status", "missing") or "missing").strip().lower()
            status_counts[status_name] = status_counts.get(status_name, 0) + 1

        return {
            "generated_at": _utcnow_z(),
            "mission_scope": {
                "total": len(all_missions),
                "enabled": len(enabled_missions),
                "disabled": max(0, len(all_missions) - len(enabled_missions)),
                "items": len(all_items),
                "stories": len(all_stories),
            },
            "signals": signals,
            "summary": {
                "signal_count": len(signals),
                "ok": status_counts.get("ok", 0),
                "watch": status_counts.get("watch", 0),
                "missing": status_counts.get("missing", 0),
            },
        }

    def _run_jina_search(
        self,
        query: str,
        *,
        sites: list[str] | None,
        limit: int = 5,
    ) -> tuple[list[SearchHit], dict[str, Any]]:
        """Run Jina search through the reader's injected client for testable behavior."""
        opts = JinaSearchOptions(sites=sites or [], limit=max(1, int(limit)))
        raw_hits = self._jina_client.search(query, options=opts)

        hits: list[SearchHit] = []
        for r in raw_hits:
            url = (r.url or "").strip()
            if not url:
                continue
            snippet = str(r.description or r.content or "").strip()
            hit = SearchHit(
                title=str(r.title or "").strip()[:300] or "Untitled",
                url=self._search_gateway._sanitize_url(url),
                snippet=snippet,
                provider="jina",
                source="jina",
                score=0.45,
                raw={"title": r.title, "description": r.description, "content": r.content},
                extra={"sources": ["jina"]},
            )
            hits.append(hit)

        search_audit = {
            "query": query,
            "mode": "single",
            "requested_provider": "jina",
            "provider_chain": ["jina"],
            "attempts": [
                {
                    "provider": "jina",
                    "status": "ok",
                    "count": len(hits),
                    "latency_ms": 0.0,
                    "retry_count": 0,
                    "attempts": 0,
                    "circuit_state_before": None,
                    "circuit_state_after": None,
                }
            ],
            "providers_selected": 1,
            "providers_with_hit": 1 if hits else 0,
            "source_count": 1 if hits else 0,
            "provider_count": 1,
            "sampled_at": _utcnow_z(),
        }
        return hits, search_audit

    @staticmethod
    def _is_api_key_error(exc: BaseException) -> bool:
        message = (str(exc) or "").lower()
        if not message:
            return False
        return (
            "api key" in message
            or "apikey" in message
            or "api-key" in message
            or "unauthorized" in message
            or "authentication" in message
        )

    async def read(
        self,
        url: str,
        *,
        min_confidence: float = 0.0,
        extract_entities: bool = False,
        entity_mode: str = "fast",
        store_entities: bool = True,
        entity_api_key: str | None = None,
        entity_model: str = "gpt-4o-mini",
        entity_api_base: str = "https://api.openai.com/v1",
    ) -> DataPulseItem:
        return await asyncio.to_thread(
            self._read_sync,
            url,
            min_confidence,
            extract_entities,
            entity_mode,
            store_entities,
            entity_api_key,
            entity_model,
            entity_api_base,
        )

    def _read_sync(
        self,
        url: str,
        min_confidence: float = 0.0,
        extract_entities: bool = False,
        entity_mode: str = "fast",
        store_entities: bool = True,
        entity_api_key: str | None = None,
        entity_model: str = "gpt-4o-mini",
        entity_api_base: str = "https://api.openai.com/v1",
    ) -> DataPulseItem:
        result, parser = self.router.route(url)
        if not result.success:
            raise RuntimeError(result.error)

        item = self._to_item(result, parser.name)
        if parser.name == "twitter" and "thin_content" in item.confidence_factors:
            fallback_content = ""
            fallback_parser = ""
            original_timeout = getattr(self._jina_client, "timeout", 8)
            try:
                for timeout in (int(original_timeout), max(20, int(original_timeout))):
                    try:
                        self._jina_client.timeout = timeout
                        fallback = self._jina_client.read(url)
                        candidate = (fallback.content or "").strip()
                        if candidate:
                            fallback_content = candidate
                            fallback_parser = f"jina_reader_t{timeout}"
                            break
                    except Exception as exc:  # noqa: BLE001
                        logger.info(
                            "Twitter thin_content jina fallback failed for %s (timeout=%s): %s",
                            url,
                            timeout,
                            exc,
                        )
            finally:
                self._jina_client.timeout = original_timeout

            if not fallback_content:
                try:
                    import requests

                    resp = requests.get(
                        f"https://r.jina.ai/{url}",
                        headers={"Accept": "text/plain"},
                        timeout=max(20, int(original_timeout)),
                    )
                    resp.raise_for_status()
                    fallback_content = (resp.text or "").strip()
                    if fallback_content:
                        fallback_parser = "jina_http_direct"
                except Exception as exc:  # noqa: BLE001
                    logger.info("Twitter thin_content direct fallback skipped for %s: %s", url, exc)

            if len(fallback_content) >= max(160, len(item.content) * 2):
                item.content = fallback_content
                item.parser = "twitter+jina_fallback"
                item.confidence = max(item.confidence, 0.92)
                item.confidence_factors = [
                    factor for factor in item.confidence_factors
                    if factor != "thin_content"
                ]
                if "long_content" not in item.confidence_factors:
                    item.confidence_factors.append("long_content")
                if "jina_fallback" not in item.tags:
                    item.tags.append("jina_fallback")
                item.extra["fallback_parser"] = fallback_parser or "jina_reader"
        if item.confidence < min_confidence:
            raise RuntimeError(f"Confidence too low: {item.confidence:.3f}")

        if extract_entities:
            self._attach_entities(
                item,
                *self._extract_entities(
                    item,
                    mode=entity_mode,
                    store=store_entities,
                    llm_api_key=entity_api_key,
                    llm_model=entity_model,
                    llm_api_base=entity_api_base,
                )
            )

        if self.inbox.add(item):
            projection = project_markdown(item)
            item.extra["markdown_projection"] = projection.to_dict()
            self.inbox.save()
            if projection.primary_path:
                logger.info("Projected markdown: %s", projection.primary_path)
            if projection.status == "degraded":
                logger.warning(
                    "Markdown projection degraded for %s: %s",
                    item.id,
                    projection.reason,
                )
        else:
            logger.info("Item already exists in inbox: %s", item.id)
        return item

    async def read_batch(
        self,
        urls: list[str],
        *,
        min_confidence: float = 0.0,
        return_all: bool = True,
        store: bool | None = None,
        extract_entities: bool = False,
        entity_mode: str = "fast",
        store_entities: bool = True,
        entity_api_key: str | None = None,
        entity_model: str = "gpt-4o-mini",
        entity_api_base: str = "https://api.openai.com/v1",
    ) -> list[DataPulseItem]:
        # Normalize and deduplicate URLs
        seen: set[str] = set()
        unique_urls: list[str] = []
        for url in urls:
            normalized = url.strip().rstrip("/")
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_urls.append(url.strip())
        max_concurrency = int(os.getenv("DATAPULSE_BATCH_CONCURRENCY", "5"))
        semaphore = asyncio.Semaphore(max_concurrency)
        if store is not None:
            logger.debug(
                "read_batch(store=%s) is deprecated; storage remains automatic.",
                store,
            )

        async def _bounded_read(url: str) -> DataPulseItem:
            async with semaphore:
                kwargs: dict[str, Any] = {"min_confidence": min_confidence}
                if extract_entities:
                    kwargs["extract_entities"] = True
                    kwargs["entity_mode"] = entity_mode
                    kwargs["store_entities"] = store_entities
                if entity_api_key:
                    kwargs["entity_api_key"] = entity_api_key
                if entity_model != "gpt-4o-mini":
                    kwargs["entity_model"] = entity_model
                if entity_api_base != "https://api.openai.com/v1":
                    kwargs["entity_api_base"] = entity_api_base
                return await self.read(url, **kwargs)

        tasks = [_bounded_read(url) for url in unique_urls]
        outputs: list[DataPulseItem] = []
        for item in await asyncio.gather(*tasks, return_exceptions=True):
            if isinstance(item, BaseException):
                logger.warning("Batch entry failed: %s", item)
                if return_all:
                    continue
                raise item
            outputs.append(item)  # type: ignore[arg-type]

        # Highest confidence first
        outputs.sort(key=lambda it: it.confidence, reverse=True)
        return outputs

    def _extract_entities(
        self,
        item: DataPulseItem,
        *,
        mode: str = "fast",
        store: bool = True,
        llm_api_key: str | None = None,
        llm_model: str = "gpt-4o-mini",
        llm_api_base: str = "https://api.openai.com/v1",
    ) -> tuple[list[Entity], list[Relation]]:
        source_id = item.id
        entities, relations = extract_entities_text(
            item.content,
            mode=mode,
            source_item_id=source_id,
            llm_api_key=llm_api_key,
            llm_model=llm_model,
            llm_api_base=llm_api_base,
        )
        if store and (entities or relations):
            self.entity_store.add_entities(entities)
            self.entity_store.add_relations(relations)
        return entities, relations

    @staticmethod
    def _extract_entities_from_dict(payload: Any) -> list[str]:
        if isinstance(payload, list):
            names: list[str] = []
            for raw in payload:
                if isinstance(raw, dict):
                    name = str(raw.get("name", "")).strip().upper()
                elif isinstance(raw, str):
                    name = raw.strip().upper()
                else:
                    continue
                if name:
                    names.append(name)
            return names
        if isinstance(payload, str):
            return [payload.strip().upper()]
        return []

    @staticmethod
    def _collect_entity_source_counts(items: list[DataPulseItem]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in items:
            if not item.extra.get("entities"):
                continue
            names = set(DataPulseReader._extract_entities_from_dict(item.extra.get("entities")))
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts

    def _attach_entities(
        self,
        item: DataPulseItem,
        entities: list[Entity],
        relations: list[Relation],
    ) -> None:
        if entities:
            item.extra["entities"] = [entity.to_dict() for entity in entities]
        elif "entities" in item.extra:
            item.extra.pop("entities")

        if relations:
            item.extra["relations"] = [relation.to_dict() for relation in relations]
        elif "relations" in item.extra:
            item.extra.pop("relations")

    async def search(
        self,
        query: str,
        *,
        sites: list[str] | None = None,
        platform: str | None = None,
        limit: int = 5,
        top_n: int | None = None,
        fetch_content: bool = True,
        min_confidence: float = 0.0,
        extract_entities: bool = False,
        entity_mode: str = "fast",
        store_entities: bool = True,
        entity_api_key: str | None = None,
        entity_model: str = "gpt-4o-mini",
        entity_api_base: str = "https://api.openai.com/v1",
        provider: str = "auto",
        mode: str = "single",
        deep: bool = False,
        news: bool = False,
        time_range: str | None = None,
        freshness: str | None = None,
    ) -> list[DataPulseItem]:
        """Search the web via Jina/Tavily and return scored DataPulseItems."""
        if top_n is not None and top_n > 0:
            limit = top_n
        effective_mode = "multi" if provider == "multi" else mode
        merged_sites = list(sites or [])
        if platform and platform in PLATFORM_SEARCH_SITES:
            for domain in PLATFORM_SEARCH_SITES[platform]:
                if domain not in merged_sites:
                    merged_sites.append(domain)

        # Keep gateway Jina client reference aligned for external test/mocking.
        self._search_gateway._jina_client = self._jina_client

        # Provider-level orchestration (single provider + fallback, or multi-source fusion).
        requested_time_range = time_range or freshness

        requested_query = query
        effective_query = self._search_gateway._with_sites(query, merged_sites)

        if provider == "jina":
            try:
                search_hits, search_audit = self._run_jina_search(
                    query,
                    sites=merged_sites,
                    limit=limit,
                )
            except Exception as exc:
                logger.warning(
                    "Jina search failed: provider=jina query=%r sites=%s error=%s",
                    query,
                    merged_sites,
                    exc,
                )
                return []
        elif provider == "auto":
            fallback_applied = False
            fallback_reason = ""
            primary_attempt: dict[str, Any] | None = None
            try:
                search_hits, search_audit = self._run_jina_search(
                    query,
                    sites=merged_sites,
                    limit=limit,
                )
                if not search_hits:
                    fallback_applied = True
                    fallback_reason = "jina_empty_result"
                    primary_attempt = {
                        "provider": "jina",
                        "status": "ok",
                        "count": 0,
                        "latency_ms": 0.0,
                        "retry_count": 0,
                        "attempts": 0,
                        "error": "",
                        "fallback_trigger": "empty_result",
                        "circuit_state_before": None,
                        "circuit_state_after": None,
                    }
                    raise RuntimeError(fallback_reason)
                search_audit["requested_provider"] = "auto"
                search_audit["effective_provider"] = "jina"
                search_audit["fallback_applied"] = False
            except Exception as exc:
                fallback_applied = True
                fallback_reason = fallback_reason or str(exc)
                if primary_attempt is None:
                    primary_attempt = {
                        "provider": "jina",
                        "status": "error",
                        "count": 0,
                        "latency_ms": 0.0,
                        "retry_count": 0,
                        "attempts": 0,
                        "error": str(exc),
                        "fallback_trigger": "exception",
                        "circuit_state_before": None,
                        "circuit_state_after": None,
                    }
                logger.warning("Auto search fallback triggered: %s", exc)
                try:
                    search_hits, search_audit = self._search_gateway.search(
                        query,
                        sites=merged_sites,
                        limit=limit,
                        provider="auto",
                        mode=effective_mode,
                        deep=deep,
                        news=news,
                        time_range=requested_time_range,
                    )
                except Exception as fallback_exc:
                    if self._is_api_key_error(exc) or self._is_api_key_error(fallback_exc):
                        logger.warning("Search unavailable due to missing API key(s): %s", fallback_exc)
                        return []
                    raise

                attempts = list(search_audit.get("attempts", [])) if isinstance(search_audit, dict) else []
                attempts.insert(0, primary_attempt)
                if not isinstance(search_audit, dict):
                    search_audit = {}
                search_audit["attempts"] = attempts
                search_audit["fallback_applied"] = fallback_applied
                search_audit["fallback_reason"] = fallback_reason
                search_audit["initial_provider"] = "jina"
                effective_provider = search_hits[0].provider if search_hits else ""
                search_audit["fallback_provider"] = effective_provider
                search_audit["effective_provider"] = effective_provider
        else:
            search_hits, search_audit = self._search_gateway.search(
                query,
                sites=merged_sites,
                limit=limit,
                provider=provider,
                mode=effective_mode,
                deep=deep,
                news=news,
                time_range=requested_time_range,
            )
        if not isinstance(search_audit, dict):
            search_audit = {}
        search_audit.setdefault("requested_provider", provider)
        search_audit.setdefault("requested_query", requested_query)
        search_audit.setdefault("effective_query", effective_query)
        if merged_sites:
            search_audit.setdefault("constraints_preserved", True)
        search_audit.setdefault("fallback_applied", False)
        search_audit.setdefault("effective_provider", "")

        if not search_hits:
            return []
        if not search_audit.get("effective_provider"):
            search_audit["effective_provider"] = search_hits[0].provider if search_hits else ""

        items: list[DataPulseItem] = []
        for sr in search_hits:
            item: DataPulseItem | None = None
            hit_sources = sr.extra.get("sources", [sr.provider])
            hit_sources = list(dict.fromkeys(hit_sources)) if hit_sources else [sr.provider]
            hit_source_count = len(hit_sources)
            cross_validation = sr.extra.get("cross_validation", {})
            cross_validated = bool(
                isinstance(cross_validation, dict)
                and cross_validation.get("is_cross_validated")
            )

            # Tag and confidence bias for multi-source supported snippets.
            parser_name = "jina_search" if sr.provider == "jina" else "tavily_search" if sr.provider == "tavily" else "search_result"
            extra_flags = ["search_result", parser_name]
            if hit_source_count >= 2:
                extra_flags.append("multi_source")
            if cross_validated:
                extra_flags.append("cross_validated")

            if fetch_content and sr.url:
                try:
                    result, parser = self.router.route(sr.url)
                    if result.success:
                        item = self._to_item(result, parser.name)
                except Exception:
                    logger.info("Full fetch failed for search result %s, using snippet", sr.url)

            if item is None:
                # Build item directly from search snippet
                content = sr.snippet
                lang = normalize_language(f"{sr.title} {content}")
                confidence, reasons = compute_confidence(
                    parser_name,
                    has_title=bool(sr.title),
                    content_length=len(content),
                    has_source=True,
                    has_author=False,
                    extra_flags=extra_flags,
                )
                snippet_source_type = SourceType.XHS if platform == "xhs" else SourceType.GENERIC
                snippet_tags = [parser_name, snippet_source_type.value]
                if platform == "xhs":
                    snippet_tags.append("xhs_search")
                snippet_tags.append(sr.provider)
                if hit_source_count >= 2:
                    snippet_tags.append("multi_source")
                if cross_validated:
                    snippet_tags.append("cross_validated")
                item = DataPulseItem(
                    source_type=snippet_source_type,
                    source_name=sr.source,
                    title=(sr.title or "Untitled").strip()[:300],
                    content=content,
                    url=sr.url,
                    parser=parser_name,
                    confidence=confidence,
                    confidence_factors=reasons,
                    language=lang,
                    tags=snippet_tags,
                    extra={
                        "search_query": query,
                        "search_provider": provider,
                        "search_mode": effective_mode,
                        "search_audit": search_audit,
                        "search_sources": hit_sources,
                        "search_source_count": hit_source_count,
                        "search_raw": sr.raw,
                        "search_consistency": cross_validation,
                        "search_cross_validation": cross_validation,
                        "search_description": "",
                    },
                    score=0,
                )

            # Ensure search metadata is present
            item.extra["search_query"] = query
            item.extra["search_provider"] = provider
            item.extra["search_mode"] = effective_mode
            item.extra["search_audit"] = search_audit
            item.extra["search_sources"] = hit_sources
            item.extra["search_source_count"] = hit_source_count
            item.extra["search_consistency"] = cross_validation
            item.extra["search_cross_validation"] = cross_validation
            item.extra["search_source_diversity"] = sr.extra.get("source_diversity", 0.0)
            if "jina_search" not in item.tags:
                item.tags.append("jina_search")
            if parser_name not in item.tags:
                item.tags.append(parser_name)
            if "search" not in item.tags:
                item.tags.append("search")
            if effective_mode == "multi" or hit_source_count >= 2:
                if "multi_source" not in item.tags:
                    item.tags.append("multi_source")
            if cross_validated and "cross_validated" not in item.tags:
                item.tags.append("cross_validated")

            if extract_entities:
                entities, relations = self._extract_entities(
                    item,
                    mode=entity_mode,
                    store=store_entities,
                    llm_api_key=entity_api_key,
                    llm_model=entity_model,
                    llm_api_base=entity_api_base,
                )
                self._attach_entities(item, entities, relations)

            if min_confidence and item.confidence < min_confidence:
                continue

            items.append(item)

        # Batch add to inbox + single save
        added_any = False
        for item in items:
            if self.inbox.add(item):
                added_any = True
        if added_any:
            self.inbox.save()

        # Score and rank
        authority_map = self.catalog.build_authority_map()
        entity_source_counts = self._collect_entity_source_counts(items)
        ranked = rank_items(items, authority_map=authority_map, entity_source_counts=entity_source_counts)
        return ranked

    async def trending(
        self,
        location: str = "",
        top_n: int = 20,
        store: bool = False,
        validate: bool | None = None,
        validate_mode: str = "strict",
    ) -> dict[str, Any]:
        """Fetch trending topics from trends24.in.

        Returns structured data with the latest snapshot.
        store=True saves the snapshot as a DataPulseItem to inbox (opt-in).
        """
        collector = TrendingCollector()
        requested_location = location.strip().lower() if location else "worldwide"
        resolved_location = requested_location
        fallback_reason = ""
        try:
            snapshots = await asyncio.to_thread(
                collector.fetch_snapshots, location, top_n
            )
        except Exception as exc:  # noqa: BLE001
            if requested_location not in {"", "worldwide", "global"}:
                logger.warning(
                    "Trending fetch failed for %s, fallback to worldwide: %s",
                    requested_location,
                    exc,
                )
                snapshots = await asyncio.to_thread(
                    collector.fetch_snapshots, "worldwide", top_n
                )
                resolved_location = "worldwide"
                fallback_reason = str(exc)
            else:
                raise
        if not snapshots:
            return {
                "location": resolved_location or "worldwide",
                "requested_location": requested_location or "worldwide",
                "snapshot_time": "",
                "trend_count": 0,
                "trends": [],
                "fallback_reason": fallback_reason,
                "degraded": bool(fallback_reason),
            }

        latest = snapshots[0]
        if collector._is_low_signal_snapshot(latest):
            low_signal_reason = "Low-signal trending snapshot (placeholder topics)"
            combined_reason = fallback_reason or low_signal_reason
            if fallback_reason and low_signal_reason not in fallback_reason:
                combined_reason = f"{fallback_reason}; {low_signal_reason}"
            return {
                "location": resolved_location or "worldwide",
                "requested_location": requested_location or "worldwide",
                "snapshot_time": latest.timestamp_utc or latest.timestamp,
                "trend_count": 0,
                "trends": [],
                "fallback_reason": combined_reason,
                "degraded": True,
            }

        loc_slug = resolved_location or "worldwide"
        from urllib.parse import quote
        trends_out = [
            {
                "rank": t.rank,
                "name": t.name,
                "volume": t.volume,
                "volume_raw": t.volume_raw,
                "twitter_search_url": f"https://x.com/search?q={quote(t.name)}",
            }
            for t in latest.trends
        ]

        result: dict[str, Any] = {
            "location": loc_slug,
            "requested_location": requested_location or "worldwide",
            "snapshot_time": latest.timestamp_utc or latest.timestamp,
            "trend_count": len(latest.trends),
            "trends": trends_out,
            "degraded": bool(fallback_reason),
        }
        if fallback_reason:
            result["fallback_reason"] = fallback_reason

        if validate is None:
            validate = os.getenv("DATAPULSE_TRENDING_CROSS_VALIDATE", "0").strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }
        if validate and result["trends"]:
            result["trends"] = await self._validate_trending_topics(
                result["trends"],
                query_mode=validate_mode,
            )
            result["trend_count"] = len(result["trends"])

        if store:
            url = build_trending_url(location)
            parse_result = collector.parse(url)
            if parse_result.success:
                item = self._to_item(parse_result, collector.name)
                if self.inbox.add(item):
                    self.inbox.save()
                result["stored_item_id"] = item.id

        return result

    @staticmethod
    def _build_trend_input_from_trending_result(
        payload: dict[str, Any],
        *,
        label: str = "",
    ) -> TrendFeedInput | None:
        if not isinstance(payload, dict):
            return None
        trends = payload.get("trends", [])
        topics: list[str] = []
        if isinstance(trends, list):
            for row in trends:
                if not isinstance(row, dict):
                    continue
                topic = str(row.get("name", "") or "").strip()
                if topic:
                    topics.append(topic)
        location = str(payload.get("location") or payload.get("requested_location") or "worldwide").strip() or "worldwide"
        snapshot_time = str(payload.get("snapshot_time", "") or "").strip()
        notes = str(payload.get("fallback_reason", "") or "").strip()
        if not label:
            label = f"Trending seeds ({location})"
        trend_input = TrendFeedInput(
            provider="trends24",
            label=label,
            location=location,
            topics=topics,
            feed_url=build_trending_url(location),
            snapshot_time=snapshot_time,
            notes=notes,
        )
        if not trend_input.has_content():
            return None
        return trend_input

    async def create_watch_from_trends(
        self,
        *,
        name: str,
        query: str,
        location: str = "",
        trend_limit: int = 5,
        label: str = "",
        mission_intent: dict[str, Any] | None = None,
        platforms: list[str] | None = None,
        sites: list[str] | None = None,
        schedule: str = "manual",
        min_confidence: float = 0.0,
        top_n: int = 5,
        alert_rules: list[dict[str, Any]] | None = None,
        enabled: bool = True,
        validate: bool | None = None,
        validate_mode: str = "strict",
    ) -> dict[str, Any]:
        trend_result = await self.trending(
            location=location,
            top_n=trend_limit,
            store=False,
            validate=validate,
            validate_mode=validate_mode,
        )
        trend_input = self._build_trend_input_from_trending_result(trend_result, label=label)
        payload = self.create_watch(
            name=name,
            query=query,
            mission_intent=mission_intent,
            trend_inputs=[trend_input.to_dict()] if trend_input is not None else None,
            platforms=platforms,
            sites=sites,
            schedule=schedule,
            min_confidence=min_confidence,
            top_n=top_n,
            alert_rules=alert_rules,
            enabled=enabled,
        )
        payload["trend_seed_result"] = trend_result
        return payload

    async def _validate_trending_topics(
        self,
        trends: list[dict[str, Any]],
        *,
        query_mode: str = "strict",
    ) -> list[dict[str, Any]]:
        concurrency = max(1, int(os.getenv("DATAPULSE_TRENDING_VALIDATE_CONCURRENCY", "4")))
        sem = asyncio.Semaphore(concurrency)

        async def _check(topic: str) -> dict[str, Any]:
            async with sem:
                def _sync_search() -> tuple[list[Any], dict[str, Any]]:
                    return self._search_gateway.search(
                        topic,
                        limit=3,
                        provider="tavily",
                        mode="single",
                        news=query_mode == "news",
                        time_range="day" if query_mode == "news" else None,
                    )

                hits, audit = await asyncio.to_thread(_sync_search)
                is_validated = False
                source_count = 0
                consistency: dict[str, Any] = {}
                search_provider = "tavily"
                validation_level = "unvalidated"

                if hits:
                    top_hit = hits[0]
                    providers = top_hit.extra.get("providers", [])
                    if not providers and isinstance(top_hit.extra.get("cross_validation"), dict):
                        providers = top_hit.extra["cross_validation"].get("providers", [])
                    source_count = len(set(providers or [top_hit.provider]))
                    consistency = top_hit.extra.get("cross_validation", {})
                    is_cross_validated = bool(
                        isinstance(consistency, dict)
                        and consistency.get("is_cross_validated", False)
                    )
                    if is_cross_validated:
                        search_provider = "multi"
                    if query_mode == "strict":
                        is_validated = is_cross_validated
                        validation_level = "strict_validated" if is_validated else "strict_rejected"
                    elif query_mode == "news":
                        is_validated = source_count >= 1
                        validation_level = "news_validated" if is_validated else "news_rejected"
                    else:
                        is_validated = source_count >= 1
                        validation_level = "lenient_validated" if is_validated else "lenient_rejected"
                return {
                    "search_consistency": consistency,
                    "search_source_count": source_count,
                    "is_validated": is_validated,
                    "validation_mode": query_mode,
                    "validation_level": validation_level,
                    "search_provider": search_provider,
                    "search_audit": audit,
                }

        check_tasks = [(_check(item["name"]), item) for item in trends if item.get("name")]
        if not check_tasks:
            return []

        check_results = await asyncio.gather(*[t[0] for t in check_tasks])

        validated_topics: list[dict[str, Any]] = []
        for report, (_, topic) in zip(check_results, check_tasks):
            merged = dict(topic)
            merged.update(report)
            if report.get("is_validated"):
                validated_topics.append(merged)
        return validated_topics

    def emit_digest_package(
        self,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        top_n: int = 3,
        secondary_n: int = 7,
        min_confidence: float = 0.0,
        since: str | None = None,
        output_format: str = "json",
    ) -> str:
        """Build read-only digest package for downstream automation (no side effects)."""
        payload = cast(dict[str, Any], self.build_digest(
            profile=profile,
            source_ids=source_ids,
            top_n=top_n,
            secondary_n=secondary_n,
            min_confidence=min_confidence,
            since=since,
        ))

        primary_payload = payload.get("primary")
        secondary_payload = payload.get("secondary")
        primary = primary_payload if isinstance(primary_payload, list) else []
        secondary = secondary_payload if isinstance(secondary_payload, list) else []
        all_items = [item for item in primary + secondary if isinstance(item, dict)]
        sources: dict[str, int] = {}
        timeline: list[dict[str, Any]] = []
        recommendations: list[str] = []
        todos: list[str] = []
        high_confidence_hits = 0

        for item in all_items:
            source_name = item.get("source_name") or "unknown"
            sources[source_name] = sources.get(source_name, 0) + 1
            timeline.append(
                {
                    "time": item.get("date_published", item.get("fetched_at", "")),
                    "title": item.get("title", ""),
                    "source": source_name,
                    "url": item.get("url", ""),
                }
            )
            if (item.get("score", 0) or 0) >= 60:
                recommendations.append(
                    f"优先复核高置信内容: {item.get('title', '')} ({source_name})"
                )
                high_confidence_hits += 1
            else:
                todos.append(f"需补充来源/验证: {item.get('title', '')} ({source_name})")

        package: dict[str, Any] = {
            "summary": {
                "title": f"DataPulse Digest Package | {profile}",
                "generated_at": _utcnow_z(),
                "high_confidence_count": high_confidence_hits,
                "item_count": len(all_items),
                "stats": payload.get("stats", {}),
                "factuality_status": (
                    payload.get("factuality", {}).get("status", "review_required")
                    if isinstance(payload.get("factuality"), dict)
                    else "review_required"
                ),
                "factuality_score": (
                    float(payload.get("factuality", {}).get("score", 0.0) or 0.0)
                    if isinstance(payload.get("factuality"), dict)
                    else 0.0
                ),
            },
            "sources": [
                {"source_name": name, "count": count}
                for name, count in sorted(sources.items(), key=lambda kv: kv[0])
            ],
            "recommendations": recommendations,
            "timeline": sorted(timeline, key=lambda x: x.get("time", ""), reverse=True),
            "todos": todos,
            "factuality": payload.get("factuality", {}),
            "digest_payload": payload,
        }
        factuality = package["factuality"] if isinstance(package["factuality"], dict) else {}
        factuality_backend = (
            factuality.get("backend_review", {})
            if isinstance(factuality.get("backend_review"), dict)
            else {}
        )
        effective_factuality_status = resolve_factuality_gate_status(factuality)
        if effective_factuality_status != str(
            factuality.get("status", package["summary"]["factuality_status"]) or package["summary"]["factuality_status"]
        ).strip().lower():
            package["summary"]["factuality_effective_status"] = effective_factuality_status
        for reason in factuality.get("reasons", []) if isinstance(factuality.get("reasons"), list) else []:
            todos.append(f"事实性复核: {reason}")
        for reason in factuality_backend.get("reasons", []) if isinstance(factuality_backend.get("reasons"), list) else []:
            todos.append(f"事实性后端复核: {reason}")

        if output_format.lower() == "md" or output_format.lower() == "markdown":
            lines = [
                "# DataPulse Digest Package",
                f"- **生成时间**: {package['summary']['generated_at']}",
                f"- **高置信条目**: {package['summary']['high_confidence_count']}",
                f"- **总条目**: {package['summary']['item_count']}",
                f"- **事实性状态**: {package['summary']['factuality_status']}",
                f"- **事实性分数**: {package['summary']['factuality_score']:.3f}",
            ]
            if package["summary"].get("factuality_effective_status"):
                lines.append(f"- **事实性生效状态**: {package['summary']['factuality_effective_status']}")
            lines.extend([
                "",
                "## 摘要",
                package["summary"]["title"],
                "",
                "## Factuality Gate",
                f"- 状态: {factuality.get('status', 'review_required')}",
                f"- 动作: {factuality.get('operator_action', 'review_before_delivery')}",
                f"- 摘要: {factuality.get('summary', 'No factuality summary recorded.')}",
            ])
            for reason in factuality.get("reasons", []) if isinstance(factuality.get("reasons"), list) else []:
                lines.append(f"- 复核提示: {reason}")
            for signal in factuality.get("signals", []) if isinstance(factuality.get("signals"), list) else []:
                if not isinstance(signal, dict):
                    continue
                lines.append(
                    f"- 信号: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}"
                )
            show_backend_review = bool(factuality_backend) and (
                str(factuality_backend.get("status", "skipped") or "skipped").strip().lower() != "skipped"
                or bool(factuality_backend.get("used_output"))
                or bool(factuality_backend.get("summary"))
                or bool(factuality_backend.get("reasons"))
                or bool(factuality_backend.get("signals"))
                or bool(factuality_backend.get("warnings"))
                or bool(factuality_backend.get("error"))
            )
            if show_backend_review:
                lines.append(
                    f"- 后端复核: {factuality_backend.get('status', 'skipped')} | "
                    f"verdict={factuality_backend.get('backend_status', effective_factuality_status)}"
                )
                if factuality_backend.get("summary"):
                    lines.append(f"- 后端摘要: {factuality_backend.get('summary', '')}")
                for reason in factuality_backend.get("reasons", []) if isinstance(factuality_backend.get("reasons"), list) else []:
                    lines.append(f"- 后端提示: {reason}")
                for signal in factuality_backend.get("signals", []) if isinstance(factuality_backend.get("signals"), list) else []:
                    if not isinstance(signal, dict):
                        continue
                    lines.append(
                        f"- 后端信号: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}"
                    )
                for warning in factuality_backend.get("warnings", []) if isinstance(factuality_backend.get("warnings"), list) else []:
                    lines.append(f"- 后端警告: {warning}")
                if factuality_backend.get("error"):
                    lines.append(f"- 后端错误: {factuality_backend.get('error', '')}")
            lines.extend([
                "",
                "## 来源",
            ])
            for source in package["sources"]:
                lines.append(f"- {source['source_name']}: {source['count']}")
            lines.extend([
                "",
                "## 建议行动",
            ])
            for item in package["recommendations"]:
                lines.append(f"- {item}")
            lines.extend([
                "",
                "## 待办",
            ])
            for item in package["todos"]:
                lines.append(f"- {item}")
            lines.extend([
                "",
                "## 时序",
            ])
            for event in package["timeline"]:
                lines.append(f"- [{event.get('time','')}]{event.get('title','')}")
            return "\n".join(lines)

        return json.dumps(package, ensure_ascii=False, indent=2)

    def story_build(
        self,
        *,
        items: list[DataPulseItem] | None = None,
        profile: str = "default",
        source_ids: list[str] | None = None,
        max_stories: int = 10,
        evidence_limit: int = 6,
        min_confidence: float = 0.0,
        since: str | None = None,
        save: bool = True,
    ) -> dict[str, Any]:
        if items is None:
            candidates = self.query_feed(
                profile=profile,
                source_ids=source_ids,
                limit=500,
                min_confidence=min_confidence,
                since=since,
            )
        else:
            candidates = [
                item for item in items
                if item.confidence >= min_confidence
            ]
        candidates = [item for item in candidates if is_digest_candidate(item)]
        authority_map = self.catalog.build_authority_map()
        entity_source_counts = self._collect_entity_source_counts(candidates)
        ranked = rank_items(
            candidates,
            authority_map=authority_map,
            entity_source_counts=entity_source_counts,
        )
        stories = build_story_clusters(
            ranked,
            entity_store=self.entity_store,
            max_stories=max_stories,
            evidence_limit=evidence_limit,
        )
        persisted = self.story_store.replace_stories(stories) if save else stories
        contradicted = sum(1 for story in persisted if story.contradictions)
        grounded_story_count = 0
        grounded_claim_count = 0
        grounded_evidence_span_count = 0
        for story in persisted:
            governance = story.governance if isinstance(story.governance, dict) else {}
            grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
            claim_count = int(grounding.get("claim_count", 0) or 0)
            span_count = int(grounding.get("evidence_span_count", 0) or 0)
            if claim_count > 0:
                grounded_story_count += 1
            grounded_claim_count += claim_count
            grounded_evidence_span_count += span_count
        return {
            "version": "1.0",
            "generated_at": _utcnow_z(),
            "stats": {
                "items_considered": len(candidates),
                "stories_built": len(stories),
                "stories_saved": len(persisted),
                "contradicted_stories": contradicted,
                "grounded_story_count": grounded_story_count,
                "grounded_claim_count": grounded_claim_count,
                "grounded_evidence_span_count": grounded_evidence_span_count,
            },
            "stories": [story.to_dict() for story in persisted],
        }

    def list_stories(self, *, limit: int = 20, min_items: int = 1) -> list[dict[str, Any]]:
        return [story.to_dict() for story in self.story_store.list_stories(limit=limit, min_items=min_items)]

    def create_story(self, **payload: Any) -> dict[str, Any]:
        story = self.story_store.create_story(payload)
        return story.to_dict()

    def create_story_from_triage(
        self,
        item_ids: list[str],
        *,
        title: str | None = None,
        summary: str | None = None,
        status: str = "monitoring",
    ) -> dict[str, Any]:
        normalized_ids: list[str] = []
        seen: set[str] = set()
        for raw in item_ids if isinstance(item_ids, list) else []:
            item_id = str(raw or "").strip()
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            normalized_ids.append(item_id)
        if not normalized_ids:
            raise ValueError("At least one triage item id is required")

        item_map = {item.id: item for item in self.inbox.items}
        missing = [item_id for item_id in normalized_ids if item_id not in item_map]
        if missing:
            raise ValueError(f"Triage item not found: {missing[0]}")

        selected_items = [item_map[item_id] for item_id in normalized_ids]
        story = build_story_from_items(
            selected_items,
            title=title,
            summary=summary,
            status=status,
            entity_store=self.entity_store,
        )
        return self.story_store.create_story(story).to_dict()

    def show_story(self, identifier: str) -> dict[str, Any] | None:
        story = self.story_store.get_story(identifier)
        if story is None:
            return None
        return story.to_dict()

    def update_story(
        self,
        identifier: str,
        *,
        title: str | None = None,
        summary: str | None = None,
        status: str | None = None,
    ) -> dict[str, Any] | None:
        story = self.story_store.update_story(
            identifier,
            title=title,
            summary=summary,
            status=status,
        )
        if story is None:
            return None
        return story.to_dict()

    def delete_story(self, identifier: str) -> dict[str, Any] | None:
        story = self.story_store.delete_story(identifier)
        if story is None:
            return None
        return story.to_dict()

    def export_story(self, identifier: str, *, output_format: str = "json") -> str | None:
        story = self.story_store.get_story(identifier)
        if story is None:
            return None
        if output_format.lower() in {"md", "markdown"}:
            return render_story_markdown(story)
        return json.dumps(story.to_dict(), ensure_ascii=False, indent=2)

    def story_graph(
        self,
        identifier: str,
        *,
        entity_limit: int = 12,
        relation_limit: int = 24,
    ) -> dict[str, Any] | None:
        story = self.story_store.get_story(identifier)
        if story is None:
            return None
        return build_story_graph(
            story,
            entity_store=self.entity_store,
            entity_limit=entity_limit,
            relation_limit=relation_limit,
        )

    def _to_item(self, parse_result, parser_name: str) -> DataPulseItem:
        source_type = parse_result.source_type or SourceType.GENERIC
        lang = normalize_language(f"{parse_result.title} {parse_result.content}")
        conf_flags: list[str] = list(getattr(parse_result, "confidence_flags", []))
        source_name = parse_result.author or source_type.value
        source_name = source_name or parser_name

        confidence, reasons = compute_confidence(
            parser_name,
            has_title=bool(parse_result.title.strip()),
            content_length=len(parse_result.content or ""),
            has_source=bool(source_name),
            has_author=bool(parse_result.author),
            media_hint=getattr(parse_result, "media_type", "text") or "text",
            extra_flags=conf_flags,
        )
        merged_factors = list(dict.fromkeys([
            *reasons,
            *[str(flag).strip() for flag in conf_flags if str(flag).strip()],
        ]))

        return DataPulseItem(
            source_type=source_type,
            source_name=source_name,
            title=(parse_result.title or "Untitled").strip()[:300],
            content=parse_result.content or "",
            url=parse_result.url,
            parser=parser_name,
            confidence=confidence,
            confidence_factors=merged_factors,
            quality_rank=0,
            language=lang,
            tags=list(dict.fromkeys([
                source_type.value,
                parser_name,
                *getattr(parse_result, "tags", []),
            ])),
            extra={
                "raw_excerpt": parse_result.excerpt,
                **getattr(parse_result, "extra", {}),
            },
            score=0,
        )

    def doctor(self) -> dict[str, list[dict[str, str | bool]]]:
        """Run health checks on all collectors, grouped by tier."""
        return self.router.doctor()

    async def doctor_async(self) -> dict[str, list[dict[str, str | bool]]]:
        """Async wrapper for doctor() in coroutine contexts."""
        return await asyncio.to_thread(self.doctor)

    def mark_processed(self, item_id: str, processed: bool = True) -> bool:
        ok = self.inbox.mark_processed(item_id, processed=processed)
        if ok:
            self.inbox.save()
        return ok

    def query_unprocessed(self, limit: int = 20, min_confidence: float = 0.0) -> list[DataPulseItem]:
        return self.inbox.query_unprocessed(limit=limit, min_confidence=min_confidence)

    def triage_list(
        self,
        *,
        limit: int = 20,
        min_confidence: float = 0.0,
        states: list[str] | None = None,
        include_closed: bool = False,
    ) -> list[dict[str, Any]]:
        items = self.triage.list_items(
            limit=limit,
            min_confidence=min_confidence,
            states=states,
            include_closed=include_closed,
        )
        return [serialize_item_with_governance(item) for item in items]

    def triage_update(
        self,
        item_id: str,
        *,
        state: str,
        note: str = "",
        actor: str = "system",
        duplicate_of: str | None = None,
    ) -> dict[str, Any] | None:
        item = self.triage.update_state(
            item_id,
            state=state,
            note=note,
            actor=actor,
            duplicate_of=duplicate_of,
        )
        if item is None:
            return None
        return serialize_item_with_governance(item)

    def triage_note(
        self,
        item_id: str,
        *,
        note: str,
        author: str = "system",
    ) -> dict[str, Any] | None:
        item = self.triage.add_note(item_id, note=note, author=author)
        if item is None:
            return None
        return serialize_item_with_governance(item)

    def triage_delete(self, item_id: str) -> dict[str, Any] | None:
        item = self.triage.delete_item(item_id)
        if item is None:
            return None
        return serialize_item_with_governance(item)

    def triage_stats(self, *, min_confidence: float = 0.0) -> dict[str, Any]:
        return self.triage.stats(min_confidence=min_confidence)

    def triage_explain(self, item_id: str, *, limit: int = 5) -> dict[str, Any] | None:
        return self.triage.explain_duplicate(item_id, limit=limit)

    def detect_platform(self, url: str) -> str:
        result, parser = self.router.route(url)
        if result.success:
            return parser.name
        return "generic"

    def list_memory(self, limit: int = 20, min_confidence: float = 0.0) -> list[DataPulseItem]:
        return self.inbox.query(limit=limit, min_confidence=min_confidence)

    def create_watch(
        self,
        *,
        name: str,
        query: str,
        mission_intent: dict[str, Any] | None = None,
        trend_inputs: list[dict[str, Any] | TrendFeedInput] | None = None,
        platforms: list[str] | None = None,
        sites: list[str] | None = None,
        schedule: str = "manual",
        min_confidence: float = 0.0,
        top_n: int = 5,
        alert_rules: list[dict[str, Any]] | None = None,
        enabled: bool = True,
    ) -> dict[str, Any]:
        mission = self.watchlist.create_mission(
            name=name,
            query=query,
            mission_intent=mission_intent,
            trend_inputs=trend_inputs,
            platforms=platforms,
            sites=sites,
            schedule=schedule,
            min_confidence=min_confidence,
            top_n=top_n,
            alert_rules=alert_rules,
            enabled=enabled,
        )
        return self._serialize_watch_mission(mission)

    def update_watch(
        self,
        identifier: str,
        *,
        name: str | None = None,
        query: str | None = None,
        mission_intent: dict[str, Any] | None = None,
        trend_inputs: list[dict[str, Any] | TrendFeedInput] | None = None,
        platforms: list[str] | None = None,
        sites: list[str] | None = None,
        schedule: str | None = None,
        min_confidence: float | None = None,
        top_n: int | None = None,
        alert_rules: list[dict[str, Any]] | None = None,
        enabled: bool | None = None,
    ) -> dict[str, Any] | None:
        mission = self.watchlist.update_mission(
            identifier,
            name=name,
            query=query,
            mission_intent=mission_intent,
            trend_inputs=trend_inputs,
            platforms=platforms,
            sites=sites,
            schedule=schedule,
            min_confidence=min_confidence,
            top_n=top_n,
            alert_rules=alert_rules,
            enabled=enabled,
        )
        if mission is None:
            return None
        return self.show_watch(mission.id)

    def set_watch_alert_rules(
        self,
        identifier: str,
        *,
        alert_rules: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        mission = self.watchlist.replace_alert_rules(identifier, alert_rules)
        if mission is None:
            return None
        return self.show_watch(mission.id)

    def list_watches(self, *, include_disabled: bool = False) -> list[dict[str, Any]]:
        return [
            self._serialize_watch_mission(mission)
            for mission in self.watchlist.list_missions(include_disabled=include_disabled)
        ]

    def _watch_result_items(
        self,
        mission: WatchMission,
        *,
        min_confidence: float = 0.0,
    ) -> list[DataPulseItem]:
        matched = [
            item
            for item in self.inbox.all_items(min_confidence=min_confidence)
            if str(item.extra.get("watch_mission_id", "")).strip() == mission.id
        ]
        return sorted(
            matched,
            key=lambda item: (
                (_parse_timestamp(item.fetched_at) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
                item.score,
                item.confidence,
            ),
            reverse=True,
        )

    @staticmethod
    def _watch_result_filter_tags(item: DataPulseItem) -> dict[str, str]:
        state = str(getattr(item, "review_state", "") or "new").strip().lower() or "new"
        source_label = str(item.source_name or getattr(item.source_type, "value", "") or "unknown").strip() or "unknown"
        source_key = source_label.casefold() or "unknown"
        try:
            domain = str(urlparse(str(item.url or "")).netloc or "").strip().lower()
        except ValueError:
            domain = ""
        if domain.startswith("www."):
            domain = domain[4:]
        return {
            "state": state,
            "source": source_key,
            "domain": domain or "unknown",
        }

    def _serialize_watch_result(self, item: DataPulseItem) -> dict[str, Any]:
        payload = item.to_dict()
        payload["watch_filters"] = self._watch_result_filter_tags(item)
        return payload

    @staticmethod
    def _build_watch_result_filters(items: list[dict[str, Any]]) -> dict[str, Any]:
        buckets: dict[str, dict[str, dict[str, Any]]] = {
            "states": {},
            "sources": {},
            "domains": {},
        }

        def add(bucket_name: str, key: str, label: str) -> None:
            bucket = buckets[bucket_name]
            row = bucket.setdefault(key, {"key": key, "label": label, "count": 0})
            row["count"] += 1

        for item in items:
            filters = item.get("watch_filters", {}) if isinstance(item, dict) else {}
            if not isinstance(filters, dict):
                filters = {}
            state_key = str(filters.get("state", "new") or "new").strip().lower() or "new"
            source_key = str(filters.get("source", "unknown") or "unknown").strip().casefold() or "unknown"
            domain_key = str(filters.get("domain", "unknown") or "unknown").strip().lower() or "unknown"
            add("states", state_key, state_key.replace("_", " "))
            add(
                "sources",
                source_key,
                str(item.get("source_name") or item.get("source_type") or "unknown").strip() or "unknown",
            )
            add("domains", domain_key, domain_key)

        state_order = {
            "new": 0,
            "triaged": 1,
            "verified": 2,
            "escalated": 3,
            "duplicate": 4,
            "ignored": 5,
            "unknown": 99,
        }
        return {
            "window_count": len(items),
            "states": sorted(
                buckets["states"].values(),
                key=lambda row: (state_order.get(str(row.get("key", "unknown")), 98), str(row.get("label", ""))),
            ),
            "sources": sorted(
                buckets["sources"].values(),
                key=lambda row: (-int(row.get("count", 0) or 0), str(row.get("label", ""))),
            ),
            "domains": sorted(
                buckets["domains"].values(),
                key=lambda row: (-int(row.get("count", 0) or 0), str(row.get("label", ""))),
            ),
        }

    @staticmethod
    def _build_watch_timeline_strip(
        mission: WatchMission,
        recent_results: list[dict[str, Any]],
        recent_alerts: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for run in mission.runs[:6]:
            event_time = run.finished_at or run.started_at
            if not event_time:
                continue
            events.append(
                {
                    "kind": "run",
                    "time": event_time,
                    "tone": "ok" if run.status == "success" else "hot",
                    "label": f"run: {run.status or 'unknown'}",
                    "detail": f"trigger={run.trigger or 'manual'} | items={run.item_count}",
                }
            )

        for item in recent_results[:6]:
            event_time = str(item.get("fetched_at", "") or "").strip()
            if not event_time:
                continue
            filters = item.get("watch_filters", {}) if isinstance(item.get("watch_filters"), dict) else {}
            source_label = str(item.get("source_name") or item.get("source_type") or "unknown").strip() or "unknown"
            review_state = str(filters.get("state", item.get("review_state", "new")) or "new").strip().lower() or "new"
            events.append(
                {
                    "kind": "result",
                    "time": event_time,
                    "tone": "ok" if review_state in {"verified", "escalated"} else "",
                    "label": f"result: {str(item.get('title', '') or 'untitled').strip() or 'untitled'}",
                    "detail": f"{source_label} | score={item.get('score', 0)} | state={review_state}",
                }
            )

        for alert in recent_alerts[:6]:
            event_time = str(alert.get("created_at", "") or "").strip()
            if not event_time:
                continue
            extra = alert.get("extra", {}) if isinstance(alert, dict) else {}
            delivery_errors = extra.get("delivery_errors", {}) if isinstance(extra, dict) else {}
            delivered = ",".join(alert.get("delivered_channels", []) or ["json"])
            events.append(
                {
                    "kind": "alert",
                    "time": event_time,
                    "tone": "hot" if delivery_errors else "ok",
                    "label": f"alert: {str(alert.get('rule_name', 'threshold') or 'threshold').strip()}",
                    "detail": f"{delivered or 'json'} | {str(alert.get('summary', '') or '').strip() or 'no summary'}",
                }
            )

        return sorted(
            events,
            key=lambda row: (_parse_timestamp(row.get("time")) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
            reverse=True,
        )[:10]

    def list_watch_results(
        self,
        identifier: str,
        *,
        limit: int = 10,
        min_confidence: float = 0.0,
    ) -> list[dict[str, Any]] | None:
        mission = self.watchlist.get(identifier)
        if mission is None:
            return None
        items = self._watch_result_items(mission, min_confidence=min_confidence)
        return [self._serialize_watch_result(item) for item in items[: max(0, int(limit))]]

    def show_watch(self, identifier: str) -> dict[str, Any] | None:
        mission = self.watchlist.get(identifier)
        if mission is None:
            return None
        payload = self._serialize_watch_mission(mission)
        last_failure = self._latest_failed_run(mission)
        payload["last_failure"] = last_failure.to_dict() if last_failure is not None else None
        payload["retry_advice"] = self._watch_retry_advice(mission, last_failure)
        result_items = self._watch_result_items(mission, min_confidence=0.0)
        payload["recent_results"] = [self._serialize_watch_result(item) for item in result_items[:8]]
        payload["result_stats"] = {
            "stored_result_count": len(result_items),
            "returned_result_count": min(8, len(result_items)),
            "latest_result_at": result_items[0].fetched_at if result_items else "",
        }
        payload["result_filters"] = self._build_watch_result_filters(payload["recent_results"])
        recent_alerts = self.list_alerts(limit=6, mission_id=mission.id)
        payload["recent_alerts"] = recent_alerts
        payload["delivery_stats"] = {
            "recent_alert_count": len(recent_alerts),
            "recent_error_count": sum(
                1
                for event in recent_alerts
                if isinstance(event.get("extra"), dict)
                and isinstance(event["extra"].get("delivery_errors"), dict)
                and event["extra"]["delivery_errors"]
            ),
            "last_alert_at": recent_alerts[0].get("created_at", "") if recent_alerts else "",
        }
        payload["timeline_strip"] = self._build_watch_timeline_strip(mission, payload["recent_results"], recent_alerts)
        return payload

    def disable_watch(self, identifier: str) -> dict[str, Any] | None:
        mission = self.watchlist.disable(identifier)
        if mission is None:
            return None
        return mission.to_dict()

    def enable_watch(self, identifier: str) -> dict[str, Any] | None:
        mission = self.watchlist.enable(identifier)
        if mission is None:
            return None
        return mission.to_dict()

    def delete_watch(self, identifier: str) -> dict[str, Any] | None:
        mission = self.watchlist.delete(identifier)
        if mission is None:
            return None
        return mission.to_dict()

    def _tag_items_with_watch(self, mission: WatchMission, items: list[DataPulseItem]) -> None:
        if not items:
            return
        intent_payload = mission.mission_intent.to_dict() if mission.mission_intent.has_content() else {}
        trend_payload = [self._serialize_trend_input(trend_input) for trend_input in mission.trend_inputs]
        changed = False
        for item in items:
            item.extra["watch_mission_id"] = mission.id
            item.extra["watch_mission_name"] = mission.name
            item.extra["watch_query"] = mission.query
            if intent_payload:
                item.extra["watch_mission_intent"] = dict(intent_payload)
            if trend_payload:
                item.extra["watch_seed_inputs"] = [dict(row) for row in trend_payload]
                item.extra["watch_seed_boundary"] = TREND_SEED_BOUNDARY_TEXT
            if "watch" not in item.tags:
                item.tags.append("watch")

            for stored in self.inbox.items:
                if stored.id != item.id:
                    continue
                stored.extra["watch_mission_id"] = mission.id
                stored.extra["watch_mission_name"] = mission.name
                stored.extra["watch_query"] = mission.query
                if intent_payload:
                    stored.extra["watch_mission_intent"] = dict(intent_payload)
                if trend_payload:
                    stored.extra["watch_seed_inputs"] = [dict(row) for row in trend_payload]
                    stored.extra["watch_seed_boundary"] = TREND_SEED_BOUNDARY_TEXT
                if "watch" not in stored.tags:
                    stored.tags.append("watch")
                changed = True
                break
        if changed:
            self.inbox.save()

    def _item_trend_seed_context(self, item: DataPulseItem) -> dict[str, Any] | None:
        mission_id = str(item.extra.get("watch_mission_id", "") or "").strip()
        mission_name = str(item.extra.get("watch_mission_name", "") or "").strip()
        trend_inputs: list[dict[str, Any]] = []

        mission = self.watchlist.get(mission_id) if mission_id else None
        if mission is not None and mission.trend_inputs:
            mission_name = mission.name
            trend_inputs = [
                self._serialize_trend_input(trend_input)
                for trend_input in mission.trend_inputs
            ]
        else:
            raw_inputs = item.extra.get("watch_seed_inputs", [])
            if isinstance(raw_inputs, list):
                for raw in raw_inputs:
                    if not isinstance(raw, dict):
                        continue
                    normalized = dict(raw)
                    normalized["input_kind"] = "trend_feed"
                    normalized["usage_mode"] = "watch_seed_only"
                    trend_inputs.append(normalized)

        if not trend_inputs:
            return None
        return {
            "watch_mission_id": mission_id,
            "watch_mission_name": mission_name,
            "trend_seeded": True,
            "seed_boundary": TREND_SEED_BOUNDARY_TEXT,
            "seed_inputs": trend_inputs,
        }

    def _build_feed_context(self, items: list[DataPulseItem]) -> dict[str, Any] | None:
        seeded_watches: list[dict[str, Any]] = []
        seen_watch_ids: set[str] = set()
        seeded_item_count = 0

        for item in items:
            context = self._item_trend_seed_context(item)
            if context is None:
                continue
            seeded_item_count += 1
            watch_id = str(context.get("watch_mission_id", "") or "").strip() or str(item.id or "").strip()
            if watch_id in seen_watch_ids:
                continue
            seen_watch_ids.add(watch_id)
            seed_inputs = context.get("seed_inputs", [])
            topic_count = 0
            providers: list[str] = []
            provider_seen: set[str] = set()
            for seed_input in seed_inputs if isinstance(seed_inputs, list) else []:
                if not isinstance(seed_input, dict):
                    continue
                topic_count += len(seed_input.get("topics", []) or [])
                provider = str(seed_input.get("provider", "") or "").strip().lower()
                if provider and provider not in provider_seen:
                    provider_seen.add(provider)
                    providers.append(provider)
            seeded_watches.append(
                {
                    "watch_mission_id": context.get("watch_mission_id", ""),
                    "watch_mission_name": context.get("watch_mission_name", ""),
                    "seed_input_count": len(seed_inputs) if isinstance(seed_inputs, list) else 0,
                    "topic_count": topic_count,
                    "providers": providers,
                }
            )

        if not seeded_watches:
            return None
        return {
            "trend_seeded_item_count": seeded_item_count,
            "trend_seeded_watch_count": len(seeded_watches),
            "trend_seeded_watches": seeded_watches,
            "seed_boundary": TREND_SEED_BOUNDARY_TEXT,
        }

    def list_alerts(self, *, limit: int = 20, mission_id: str | None = None) -> list[dict[str, Any]]:
        return [
            event.to_dict()
            for event in self.alert_store.list_events(limit=limit, mission_id=mission_id)
        ]

    def list_alert_routes(self) -> list[dict[str, Any]]:
        return self.alert_routes.list_routes()

    def create_alert_route(self, **payload: Any) -> dict[str, Any]:
        route_name = str(payload.pop("name", "") or "").strip()
        return self.alert_routes.create(route_name, payload)

    def update_alert_route(self, name: str, **payload: Any) -> dict[str, Any] | None:
        return self.alert_routes.update(name, payload)

    def delete_alert_route(self, name: str) -> dict[str, Any] | None:
        return self.alert_routes.delete(name)

    def alert_route_health(self, *, limit: int = 100) -> list[dict[str, Any]]:
        route_rows: dict[str, dict[str, Any]] = {}
        for route in self.list_alert_routes():
            name = str(route.get("name", "")).strip().lower()
            if not name:
                continue
            route_rows[name] = {
                "name": name,
                "channel": str(route.get("channel", "")).strip().lower() or "unknown",
                "configured": True,
                "status": "idle",
                "event_count": 0,
                "delivered_count": 0,
                "failure_count": 0,
                "success_rate": None,
                "last_event_at": "",
                "last_delivered_at": "",
                "last_failed_at": "",
                "last_error": "",
                "last_summary": "",
                "mission_ids": set(),
                "rule_names": set(),
            }

        for event in self.alert_store.list_events(limit=max(0, int(limit))):
            rule = event.extra.get("rule", {}) if isinstance(event.extra, dict) else {}
            if not isinstance(rule, dict):
                continue
            route_names = _normalize_route_names(rule)
            if not route_names:
                continue
            delivered_channels = {
                str(label or "").strip().lower()
                for label in event.delivered_channels
                if str(label or "").strip()
            }
            delivery_errors = event.extra.get("delivery_errors", {}) if isinstance(event.extra, dict) else {}
            if not isinstance(delivery_errors, dict):
                delivery_errors = {}
            for route_name in route_names:
                route_payload = self.alert_routes.get(route_name)
                route_dict: dict[str, Any] | None = route_payload if isinstance(route_payload, dict) else None
                channel = str(route_dict.get("channel", "")).strip().lower() if route_dict is not None else ""
                route_row = route_rows.setdefault(
                    route_name,
                    {
                        "name": route_name,
                        "channel": channel or "unknown",
                        "configured": route_dict is not None,
                        "status": "missing" if route_dict is None else "idle",
                        "event_count": 0,
                        "delivered_count": 0,
                        "failure_count": 0,
                        "success_rate": None,
                        "last_event_at": "",
                        "last_delivered_at": "",
                        "last_failed_at": "",
                        "last_error": "",
                        "last_summary": "",
                        "mission_ids": set(),
                        "rule_names": set(),
                    },
                )
                if channel and route_row["channel"] == "unknown":
                    route_row["channel"] = channel
                route_row["configured"] = route_row["configured"] or isinstance(route, dict)
                route_row["event_count"] += 1
                route_row["mission_ids"].add(event.mission_id)
                route_row["rule_names"].add(event.rule_name)
                if not route_row["last_event_at"]:
                    route_row["last_event_at"] = event.created_at
                    route_row["last_summary"] = event.summary

                route_label = f"{channel}:{route_name}" if channel else route_name
                if route_label in delivered_channels:
                    route_row["delivered_count"] += 1
                    if not route_row["last_delivered_at"]:
                        route_row["last_delivered_at"] = event.created_at

                error_message = str(
                    delivery_errors.get(route_label)
                    or delivery_errors.get(f"route:{route_name}")
                    or ""
                ).strip()
                if error_message:
                    route_row["failure_count"] += 1
                    if not route_row["last_failed_at"]:
                        route_row["last_failed_at"] = event.created_at
                    if not route_row["last_error"]:
                        route_row["last_error"] = error_message

        severity = {"missing": 0, "degraded": 1, "healthy": 2, "idle": 3}
        payloads: list[dict[str, Any]] = []
        for route_row in route_rows.values():
            attempts = route_row["delivered_count"] + route_row["failure_count"]
            if not route_row["configured"]:
                route_row["status"] = "missing"
            elif route_row["failure_count"] > 0:
                route_row["status"] = "degraded"
            elif route_row["delivered_count"] > 0:
                route_row["status"] = "healthy"
            else:
                route_row["status"] = "idle"
            if attempts > 0:
                route_row["success_rate"] = round(route_row["delivered_count"] / attempts, 3)
            route_row["mission_ids"] = sorted(route_row["mission_ids"])
            route_row["rule_names"] = sorted(route_row["rule_names"])
            payloads.append(route_row)

        return sorted(
            payloads,
            key=lambda row: (
                severity.get(str(row.get("status", "idle")), 99),
                -(_parse_timestamp(row.get("last_event_at")) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
                str(row.get("name", "")),
            ),
        )

    def watch_status_snapshot(self) -> dict[str, Any]:
        return self.watch_status.snapshot()

    def ops_snapshot(
        self,
        *,
        alert_limit: int = 8,
        route_limit: int = 100,
        recent_failure_limit: int = 5,
    ) -> dict[str, Any]:
        doctor_report = self.doctor()
        status = self.watch_status_snapshot()
        route_health = self.alert_route_health(limit=route_limit)
        recent_alerts = self.list_alerts(limit=alert_limit)
        watch_summary, watch_health = self._watch_health_snapshot()
        governance_scorecard = self.governance_scorecard_snapshot()

        collector_summary = {
            "total": 0,
            "ok": 0,
            "warn": 0,
            "error": 0,
            "available": 0,
            "unavailable": 0,
        }
        collector_tiers: dict[str, dict[str, Any]] = {}
        degraded_collectors: list[dict[str, Any]] = []

        for tier_name, entries in doctor_report.items():
            tier_summary = {
                "total": 0,
                "ok": 0,
                "warn": 0,
                "error": 0,
                "available": 0,
                "unavailable": 0,
            }
            for raw_entry in entries:
                entry = dict(raw_entry)
                status_name = str(entry.get("status", "ok")).strip().lower() or "ok"
                available = bool(entry.get("available", True))
                collector_summary["total"] += 1
                tier_summary["total"] += 1
                if status_name not in {"ok", "warn", "error"}:
                    status_name = "error"
                collector_summary[status_name] += 1
                tier_summary[status_name] += 1
                if available:
                    collector_summary["available"] += 1
                    tier_summary["available"] += 1
                else:
                    collector_summary["unavailable"] += 1
                    tier_summary["unavailable"] += 1
                if status_name != "ok" or not available:
                    degraded_collectors.append(
                        {
                            "tier": tier_name,
                            "name": entry.get("name", ""),
                            "status": status_name,
                            "available": available,
                            "message": entry.get("message", ""),
                            "setup_hint": entry.get("setup_hint", ""),
                        }
                    )
            collector_tiers[tier_name] = tier_summary

        collector_drilldown = sorted(
            [
                {
                    "tier": tier_name,
                    "name": str(entry.get("name", "") or "").strip(),
                    "status": str(entry.get("status", "ok") or "ok").strip().lower(),
                    "available": bool(entry.get("available", True)),
                    "message": str(entry.get("message", "") or "").strip(),
                    "setup_hint": str(entry.get("setup_hint", "") or "").strip(),
                }
                for tier_name, entries in doctor_report.items()
                for entry in entries
            ],
            key=lambda row: (
                {"error": 0, "warn": 1, "ok": 2}.get(str(row.get("status", "ok")), 99),
                0 if not bool(row.get("available", True)) else 1,
                str(row.get("tier", "")),
                str(row.get("name", "")),
            ),
        )

        metrics = status.get("metrics", {}) if isinstance(status, dict) else {}
        runs_total = int(metrics.get("runs_total", 0) or 0)
        success_total = int(metrics.get("success_total", 0) or 0)
        error_total = int(metrics.get("error_total", 0) or 0)
        watch_metrics = {
            "state": status.get("state", "idle") if isinstance(status, dict) else "idle",
            "heartbeat_at": status.get("heartbeat_at", "") if isinstance(status, dict) else "",
            "last_error": status.get("last_error", "") if isinstance(status, dict) else "",
            "cycles_total": int(metrics.get("cycles_total", 0) or 0),
            "runs_total": runs_total,
            "success_total": success_total,
            "error_total": error_total,
            "alerts_total": int(metrics.get("alerts_total", 0) or 0),
            "success_rate": round(success_total / runs_total, 3) if runs_total > 0 else None,
        }

        route_summary = {
            "total": len(route_health),
            "healthy": sum(1 for route in route_health if route.get("status") == "healthy"),
            "degraded": sum(1 for route in route_health if route.get("status") == "degraded"),
            "missing": sum(1 for route in route_health if route.get("status") == "missing"),
            "idle": sum(1 for route in route_health if route.get("status") == "idle"),
        }
        route_drilldown = [
            {
                "name": str(route.get("name", "") or "").strip(),
                "channel": str(route.get("channel", "unknown") or "unknown").strip().lower(),
                "status": str(route.get("status", "idle") or "idle").strip().lower(),
                "configured": bool(route.get("configured", False)),
                "event_count": int(route.get("event_count", 0) or 0),
                "delivered_count": int(route.get("delivered_count", 0) or 0),
                "failure_count": int(route.get("failure_count", 0) or 0),
                "success_rate": route.get("success_rate"),
                "last_event_at": str(route.get("last_event_at", "") or "").strip(),
                "last_delivered_at": str(route.get("last_delivered_at", "") or "").strip(),
                "last_failed_at": str(route.get("last_failed_at", "") or "").strip(),
                "last_error": str(route.get("last_error", "") or "").strip(),
                "last_summary": str(route.get("last_summary", "") or "").strip(),
                "mission_count": len(route.get("mission_ids", []) or []),
                "rule_count": len(route.get("rule_names", []) or []),
                "mission_ids": list(route.get("mission_ids", []) or []),
                "rule_names": list(route.get("rule_names", []) or []),
            }
            for route in route_health
        ]
        route_timeline: list[dict[str, Any]] = []
        for event in self.alert_store.list_events(limit=max(0, int(route_limit))):
            rule = event.extra.get("rule", {}) if isinstance(event.extra, dict) else {}
            if not isinstance(rule, dict):
                continue
            route_names = _normalize_route_names(rule)
            if not route_names:
                continue
            delivery_errors = event.extra.get("delivery_errors", {}) if isinstance(event.extra, dict) else {}
            if not isinstance(delivery_errors, dict):
                delivery_errors = {}
            delivered_channels = {
                str(label or "").strip().lower()
                for label in event.delivered_channels
                if str(label or "").strip()
            }
            for route_name in route_names:
                route = self.alert_routes.get(route_name)
                channel = str(route.get("channel", "")).strip().lower() if isinstance(route, dict) else ""
                route_label = f"{channel}:{route_name}" if channel else route_name
                error_message = str(
                    delivery_errors.get(route_label)
                    or delivery_errors.get(f"route:{route_name}")
                    or ""
                ).strip()
                delivered = route_label in delivered_channels
                route_timeline.append(
                    {
                        "route": route_name,
                        "channel": channel or "unknown",
                        "mission_id": event.mission_id,
                        "mission_name": event.mission_name,
                        "rule_name": event.rule_name,
                        "created_at": event.created_at,
                        "status": "failed" if error_message else "delivered" if delivered else "pending",
                        "summary": str(event.summary or "").strip(),
                        "error": error_message,
                        "delivered_channels": sorted(delivered_channels),
                    }
                )
        route_timeline = sorted(
            route_timeline,
            key=lambda row: (_parse_timestamp(row.get("created_at")) or datetime.fromtimestamp(0, tz=timezone.utc)).timestamp(),
            reverse=True,
        )[:12]

        recent_failures: list[dict[str, Any]] = []
        last_result = status.get("last_result", {}) if isinstance(status, dict) else {}
        results = last_result.get("results", []) if isinstance(last_result, dict) else []
        for row in results if isinstance(results, list) else []:
            if str(row.get("status", "")).strip().lower() == "success":
                continue
            recent_failures.append(
                {
                    "kind": "watch_run",
                    "mission_id": row.get("mission_id", ""),
                    "mission_name": row.get("mission_name", ""),
                    "status": row.get("status", "error"),
                    "error": row.get("error", ""),
                    "attempts": row.get("attempts", 0),
                }
            )
        for route in route_health:
            if route.get("failure_count", 0) and route.get("last_error"):
                recent_failures.append(
                    {
                        "kind": "route_delivery",
                        "name": route.get("name", ""),
                        "channel": route.get("channel", ""),
                        "status": route.get("status", "degraded"),
                        "error": route.get("last_error", ""),
                        "last_event_at": route.get("last_event_at", ""),
                    }
                )
        recent_failures = recent_failures[: max(0, int(recent_failure_limit))]

        return {
            "collector_summary": collector_summary,
            "collector_tiers": collector_tiers,
            "degraded_collectors": degraded_collectors[:8],
            "collector_drilldown": collector_drilldown[:12],
            "watch_metrics": watch_metrics,
            "watch_summary": watch_summary,
            "watch_health": watch_health[:8],
            "route_summary": route_summary,
            "route_health": route_health[:8],
            "route_drilldown": route_drilldown[:12],
            "route_timeline": route_timeline,
            "recent_failures": recent_failures,
            "recent_alerts": recent_alerts,
            "governance_scorecard": governance_scorecard,
            "daemon": status,
        }

    def _evaluate_and_dispatch_watch_alerts(
        self,
        mission: WatchMission,
        items: list[DataPulseItem],
    ) -> list[dict[str, Any]]:
        outputs: list[dict[str, Any]] = []
        for event, matches, cooldown_seconds in evaluate_watch_alerts(mission, items):
            if not self.alert_store.add(event, cooldown_seconds=cooldown_seconds):
                continue
            delivered, errors = dispatch_alert_event(event, matches)
            event.delivered_channels = delivered
            if errors:
                event.extra["delivery_errors"] = errors
            self.alert_store.save()
            outputs.append(event.to_dict())
        return outputs

    async def run_watch(self, identifier: str, *, trigger: str = "manual") -> dict[str, Any]:
        mission = self.watchlist.get(identifier)
        if mission is None:
            raise ValueError(f"Watch mission not found: {identifier}")
        if not mission.enabled:
            raise ValueError(f"Watch mission is disabled: {identifier}")

        started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        try:
            if mission.platforms:
                batches = await asyncio.gather(*[
                    self.search(
                        mission.query,
                        sites=mission.sites or None,
                        platform=platform,
                        limit=mission.top_n,
                        min_confidence=mission.min_confidence,
                    )
                    for platform in mission.platforms
                ])
                merged: dict[str, DataPulseItem] = {}
                for batch in batches:
                    for item in batch:
                        merged[item.id] = item
                items = sorted(
                    merged.values(),
                    key=lambda item: (item.score, item.confidence, item.fetched_at),
                    reverse=True,
                )[: mission.top_n]
            else:
                items = await self.search(
                    mission.query,
                    sites=mission.sites or None,
                    limit=mission.top_n,
                    min_confidence=mission.min_confidence,
                )

            self._tag_items_with_watch(mission, items)
            alert_events = self._evaluate_and_dispatch_watch_alerts(mission, items)
            run = MissionRun(
                mission_id=mission.id,
                status="success",
                item_count=len(items),
                trigger=trigger,
                started_at=started_at,
                finished_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            )
            updated = self.watchlist.record_run(mission.id, run) or mission
            return {
                "mission": self._serialize_watch_mission(updated),
                "run": run.to_dict(),
                "items": [item.to_dict() for item in items],
                "alert_events": alert_events,
            }
        except Exception as exc:
            run = MissionRun(
                mission_id=mission.id,
                status="error",
                item_count=0,
                trigger=trigger,
                error=str(exc),
                started_at=started_at,
                finished_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            )
            self.watchlist.record_run(mission.id, run)
            raise

    async def run_due_watches(
        self,
        limit: int | None = None,
        *,
        retry_attempts: int = 1,
        retry_base_delay: float = 1.0,
        retry_max_delay: float = 30.0,
        retry_backoff_factor: float = 2.0,
    ) -> dict[str, Any]:
        scheduled_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        due_missions = self.watch_scheduler.due_missions(limit=limit)
        results: list[dict[str, Any]] = []

        for mission in due_missions:
            attempt = 1
            delay = max(0.1, float(retry_base_delay))
            while True:
                try:
                    payload = await self.run_watch(mission.id, trigger="scheduled")
                    run_payload = payload.get("run", {})
                    alert_events = payload.get("alert_events", [])
                    results.append(
                        {
                            "mission_id": mission.id,
                            "mission_name": mission.name,
                            "status": run_payload.get("status", "success"),
                            "item_count": run_payload.get("item_count", 0),
                            "attempts": attempt,
                            "retry_count": max(0, attempt - 1),
                            "alert_count": len(alert_events) if isinstance(alert_events, list) else 0,
                        }
                    )
                    break
                except Exception as exc:
                    if attempt >= max(1, int(retry_attempts)):
                        results.append(
                            {
                                "mission_id": mission.id,
                                "mission_name": mission.name,
                                "status": "error",
                                "item_count": 0,
                                "attempts": attempt,
                                "retry_count": max(0, attempt - 1),
                                "error": str(exc),
                            }
                        )
                        break
                    await asyncio.sleep(min(delay, retry_max_delay))
                    delay = min(delay * retry_backoff_factor, retry_max_delay)
                    attempt += 1

        return {
            "scheduled_at": scheduled_at,
            "due_count": len(due_missions),
            "run_count": len(results),
            "results": results,
        }

    async def run_watch_daemon(
        self,
        *,
        poll_seconds: float = 60.0,
        max_cycles: int | None = None,
        due_limit: int | None = None,
        retry_attempts: int = 1,
        retry_base_delay: float = 1.0,
        retry_max_delay: float = 30.0,
        retry_backoff_factor: float = 2.0,
        lock_path: str | None = None,
    ) -> dict[str, Any]:
        daemon = WatchDaemon(self, lock_path=lock_path, status_store=self.watch_status)
        payload = await daemon.run_forever(
            poll_seconds=poll_seconds,
            max_cycles=max_cycles,
            due_limit=due_limit,
            retry_attempts=retry_attempts,
            retry_base_delay=retry_base_delay,
            retry_max_delay=retry_max_delay,
            retry_backoff_factor=retry_backoff_factor,
        )
        return payload

    def resolve_source(self, url: str) -> dict[str, Any]:
        return self.catalog.resolve_source(url)

    def list_sources(self, *, include_inactive: bool = False, public_only: bool = False) -> list[dict[str, Any]]:
        return [s.to_dict() for s in self.catalog.list_sources(include_inactive=include_inactive, public_only=public_only)]

    def list_packs(self, *, public_only: bool = False) -> list[dict[str, Any]]:
        return [p.to_dict() for p in self.catalog.list_packs(public_only=public_only)]

    def list_subscriptions(self, profile: str = "default") -> list[str]:
        return self.catalog.list_subscriptions(profile=profile)

    def subscribe_source(self, source_id: str, *, profile: str = "default") -> bool:
        return self.catalog.subscribe(profile=profile, source_id=source_id)

    def unsubscribe_source(self, source_id: str, *, profile: str = "default") -> bool:
        return self.catalog.unsubscribe(profile=profile, source_id=source_id)

    def install_pack(self, slug: str, *, profile: str = "default") -> int:
        return self.catalog.install_pack(profile, slug=slug)

    def query_feed(
        self,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        limit: int = 20,
        min_confidence: float = 0.0,
        since: str | None = None,
    ) -> list[DataPulseItem]:
        all_items = self.inbox.all_items(min_confidence=min_confidence)
        filtered = self.catalog.filter_by_subscription(
            all_items,
            profile=profile,
            source_ids=source_ids,
        )
        if since:
            since_dt = None
            try:
                since_dt = datetime.fromisoformat(since)
            except Exception:
                since_dt = None
            if since_dt:
                valid: list[DataPulseItem] = []
                for item in filtered:
                    try:
                        ts = datetime.fromisoformat(item.fetched_at)
                    except Exception:
                        valid.append(item)
                        continue
                    if ts >= since_dt:
                        valid.append(item)
                filtered = valid

        ordered = sorted(filtered, key=lambda it: it.fetched_at, reverse=True)
        return ordered[: max(0, limit)]

    def build_json_feed(
        self,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        limit: int = 20,
        min_confidence: float = 0.0,
        since: str | None = None,
    ) -> dict[str, Any]:
        items = self.query_feed(
            profile=profile,
            source_ids=source_ids,
            limit=limit,
            min_confidence=min_confidence,
            since=since,
        )
        base = "https://datapulse.local"
        now = _utcnow_z()
        payload: dict[str, Any] = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": f"DataPulse Feed ({profile})",
            "home_page_url": base,
            "feed_url": f"{base}/feed/{profile}.json",
            "items": [],
            "generated_at": now,
        }
        for item in items:
            row: dict[str, Any] = {
                "id": item.id,
                "title": item.title,
                "content_text": item.content,
                "date_published": item.fetched_at,
                "url": item.url,
                "source_type": item.source_type.value,
                "source_name": item.source_name,
                "authors": [{"name": item.source_name}] if item.source_name else [],
            }
            trend_context = self._item_trend_seed_context(item)
            if trend_context is not None:
                row["datapulse_context"] = trend_context
            payload["items"].append(row)
        feed_context = self._build_feed_context(items)
        if feed_context is not None:
            payload["datapulse_context"] = feed_context
        return payload

    def build_rss_feed(
        self,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        limit: int = 20,
        min_confidence: float = 0.0,
        since: str | None = None,
    ) -> str:
        items = self.query_feed(
            profile=profile,
            source_ids=source_ids,
            limit=limit,
            min_confidence=min_confidence,
            since=since,
        )
        def _xml_escape(value: str) -> str:
            return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;"))

        feed_context = self._build_feed_context(items)
        description = "Unified content feed"
        if feed_context is not None:
            description = f"{description}. {feed_context['seed_boundary']}"
        rows = []
        for item in items:
            pub = item.fetched_at
            try:
                dt = datetime.fromisoformat(pub).strftime("%a, %d %b %Y %H:%M:%S GMT")
            except Exception:
                dt = pub
            category = "<category>trend-seeded-watch</category>" if self._item_trend_seed_context(item) is not None else ""
            rows.append(
                "<item>"
                f"<title>{_xml_escape(item.title)}</title>"
                f"<link>{_xml_escape(item.url)}</link>"
                f"<guid>{_xml_escape(item.id)}</guid>"
                f"<pubDate>{_xml_escape(dt)}</pubDate>"
                f"<description>{_xml_escape(item.content[:1800])}</description>"
                f"{category}"
                "</item>"
            )

        payload = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<rss version=\"2.0\"><channel>"
            "<title>DataPulse Feed</title>"
            f"<description>{_xml_escape(description)}</description>"
            "<link>https://datapulse.local</link>"
            + "".join(rows)
            + "</channel></rss>"
        )
        return payload


    def build_digest(
        self,
        items: list[DataPulseItem] | None = None,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        top_n: int = 3,
        secondary_n: int = 7,
        min_confidence: float = 0.0,
        since: str | None = None,
        max_per_source: int = 2,
    ) -> dict[str, Any]:
        """Build a curated digest with primary and secondary stories."""
        # 1. Get candidates
        if items is None:
            candidates = self.query_feed(
                profile=profile,
                source_ids=source_ids,
                limit=500,  # grab a large pool
                min_confidence=min_confidence,
                since=since,
            )
        else:
            candidates = [
                item for item in items
                if (not min_confidence or item.confidence >= min_confidence)
                and is_digest_candidate(item)
            ]
        candidates_total = len(candidates)

        if not candidates:
            today = _utc_today()
            factuality = build_factuality_gate(
                subject="digest",
                surface="digest_delivery",
                evidence_rows=[],
                source_names=[],
                grounded_claim_count=0,
                contradiction_count=0,
            )
            return {
                "version": "1.0",
                "generated_at": _utcnow_z(),
                "digest_date": today,
                "stats": {
                    "candidates_total": 0,
                    "candidates_after_dedup": 0,
                    "sources_seen": 0,
                    "selected_primary": 0,
                    "selected_secondary": 0,
                },
                "primary": [],
                "secondary": [],
                "semantic_review": {
                    "status": "empty",
                    "items_analyzed": 0,
                    "stance_counts": {"positive": 0, "negative": 0, "neutral": 0},
                    "contradictions": [],
                    "claim_candidates": [],
                },
                "factuality": factuality,
                "provenance": "No items available",
            }

        # 2. Score and rank
        candidates = [item for item in candidates if is_digest_candidate(item)]
        authority_map = self.catalog.build_authority_map()
        ranked = rank_items(candidates, authority_map=authority_map)

        # 3. Fingerprint dedup (keep first = highest scored per fingerprint)
        seen_fps: set[str] = set()
        deduped: list[DataPulseItem] = []
        for item in ranked:
            fp = content_fingerprint(item.content)
            if fp not in seen_fps:
                seen_fps.add(fp)
                deduped.append(item)

        sources_seen = len({item.source_name for item in deduped})

        # 4. Diverse selection
        total_needed = top_n + secondary_n
        selected = self._select_diverse(
            deduped, total_needed, max_per_source=max_per_source,
        )

        primary = selected[:top_n]
        secondary = selected[top_n:top_n + secondary_n]

        today = _utc_today()
        for item in primary + secondary:
            item.digest_date = today

        semantic_review = self._build_semantic_review(primary + secondary)
        selected_payloads = [serialize_item_with_governance(item) for item in primary + secondary]
        factuality_rows: list[dict[str, Any]] = []
        for payload in selected_payloads:
            governance = payload.get("governance", {}) if isinstance(payload, dict) else {}
            if not isinstance(governance, dict):
                governance = {}
            provenance = governance.get("provenance", {}) if isinstance(governance.get("provenance"), dict) else {}
            grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
            factuality_rows.append(
                {
                    "item_id": provenance.get("item_id", payload.get("id", "")),
                    "title": payload.get("title", ""),
                    "source_name": provenance.get("source_name", payload.get("source_name", "")),
                    "evidence_grade": str(governance.get("evidence_grade", "working")).strip().lower() or "working",
                    "evidence_score": float(governance.get("evidence_score", 0.0) or 0.0),
                    "review_state": str(governance.get("review_state", "new") or "new").strip().lower() or "new",
                    "confidence": float(payload.get("confidence", 0.0) or 0.0),
                    "grounded_claim_count": int(grounding.get("claim_count", 0) or 0),
                }
            )
        factuality = build_factuality_gate(
            subject="digest",
            surface="digest_delivery",
            evidence_rows=factuality_rows,
            source_names=[item.source_name for item in primary + secondary],
            grounded_claim_count=sum(
                int(
                    (
                        payload.get("governance", {}).get("grounding", {})
                        if isinstance(payload.get("governance"), dict)
                        and isinstance(payload.get("governance", {}).get("grounding"), dict)
                        else {}
                    ).get("claim_count", 0)
                    or 0
                )
                for payload in selected_payloads
                if isinstance(payload, dict)
            ),
            contradiction_count=len(
                semantic_review.get("contradictions", [])
                if isinstance(semantic_review.get("contradictions"), list)
                else []
            ),
        )

        return {
            "version": "1.0",
            "generated_at": _utcnow_z(),
            "digest_date": today,
            "stats": {
                "candidates_total": candidates_total,
                "candidates_after_dedup": len(deduped),
                "sources_seen": sources_seen,
                "selected_primary": len(primary),
                "selected_secondary": len(secondary),
            },
            "primary": selected_payloads[: len(primary)],
            "secondary": selected_payloads[len(primary):],
            "semantic_review": semantic_review,
            "factuality": factuality,
            "provenance": f"Curated from {candidates_total} items across {sources_seen} sources",
        }

    async def build_digest_async(
        self,
        items: list[DataPulseItem] | None = None,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        top_n: int = 3,
        secondary_n: int = 7,
        min_confidence: float = 0.0,
        since: str | None = None,
        max_per_source: int = 2,
    ) -> dict[str, Any]:
        """Async wrapper for build_digest() in coroutine contexts."""
        return await asyncio.to_thread(
            self.build_digest,
            items,
            profile=profile,
            source_ids=source_ids,
            top_n=top_n,
            secondary_n=secondary_n,
            min_confidence=min_confidence,
            since=since,
            max_per_source=max_per_source,
        )

    @staticmethod
    def _build_semantic_review(items: list[DataPulseItem]) -> dict[str, Any]:
        if not items:
            return {
                "status": "empty",
                "items_analyzed": 0,
                "stance_counts": {"positive": 0, "negative": 0, "neutral": 0},
                "contradictions": [],
                "claim_candidates": [],
            }
        try:
            from datapulse.core.semantic import build_semantic_review

            payload = build_semantic_review(items)
            payload["status"] = "ok"
            return payload
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "degraded",
                "items_analyzed": len(items),
                "stance_counts": {"positive": 0, "negative": 0, "neutral": 0},
                "contradictions": [],
                "claim_candidates": [],
                "error": str(exc),
            }

    @staticmethod
    def _select_diverse(
        items: list[DataPulseItem],
        n: int,
        *,
        max_per_source: int = 2,
    ) -> list[DataPulseItem]:
        """Greedy diverse selection: limits same-source items to max_per_source."""
        if not items:
            return []
        selected: list[DataPulseItem] = []
        source_counts: dict[str, int] = {}

        for item in items:
            if len(selected) >= n:
                break
            source = item.source_name
            count = source_counts.get(source, 0)
            if count >= max_per_source:
                continue
            source_counts[source] = count + 1
            selected.append(item)

        return selected

    def build_atom_feed(
        self,
        *,
        profile: str = "default",
        source_ids: list[str] | None = None,
        limit: int = 20,
        min_confidence: float = 0.0,
        since: str | None = None,
    ) -> str:
        items = self.query_feed(
            profile=profile,
            source_ids=source_ids,
            limit=limit,
            min_confidence=min_confidence,
            since=since,
        )

        def _xml_escape(value: str) -> str:
            return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;"))

        now = _utcnow_z()
        base = "https://datapulse.local"
        feed_context = self._build_feed_context(items)
        subtitle = (
            f"<subtitle>{_xml_escape(feed_context['seed_boundary'])}</subtitle>"
            if feed_context is not None
            else ""
        )

        entries = []
        for item in items:
            updated = item.fetched_at
            if not updated.endswith("Z"):
                updated += "Z"
            category = '<category term="trend-seeded-watch"/>' if self._item_trend_seed_context(item) is not None else ""
            entries.append(
                "<entry>"
                f"<title>{_xml_escape(item.title)}</title>"
                f'<link href="{_xml_escape(item.url)}" rel="alternate"/>'
                f"<id>urn:datapulse:{_xml_escape(item.id)}</id>"
                f"<updated>{_xml_escape(updated)}</updated>"
                f"<summary>{_xml_escape(item.content[:1800])}</summary>"
                f"<author><name>{_xml_escape(item.source_name)}</name></author>"
                f"{category}"
                "</entry>"
            )

        payload = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<feed xmlns="http://www.w3.org/2005/Atom">'
            f"<title>DataPulse Feed ({_xml_escape(profile)})</title>"
            f"{subtitle}"
            f'<link href="{base}/feed/{profile}.atom" rel="self"/>'
            f"<id>urn:datapulse:feed:{_xml_escape(profile)}</id>"
            f"<updated>{now}</updated>"
            + "".join(entries)
            + "</feed>"
        )
        return payload

    async def extract_entities(
        self,
        source: str | DataPulseItem,
        *,
        mode: str = "fast",
        store: bool = True,
        llm_api_key: str | None = None,
        llm_model: str = "gpt-4o-mini",
        llm_api_base: str = "https://api.openai.com/v1",
    ) -> dict[str, Any]:
        if isinstance(source, DataPulseItem):
            item = source
            entities, relations = self._extract_entities(
                item,
                mode=mode,
                store=store,
                llm_api_key=llm_api_key,
                llm_model=llm_model,
                llm_api_base=llm_api_base,
            )
            self._attach_entities(item, entities, relations)
        elif isinstance(source, str):
            if not source.strip():
                raise ValueError("URL is required")
            item = await self.read(
                source,
                extract_entities=True,
                entity_mode=mode,
                store_entities=store,
                entity_api_key=llm_api_key,
                entity_model=llm_model,
                entity_api_base=llm_api_base,
            )
        else:
            raise TypeError("source must be URL string or DataPulseItem")

        return {
            "item": item.to_dict(),
            "entities": item.extra.get("entities", []),
            "relations": item.extra.get("relations", []),
        }

    def query_entities(
        self,
        *,
        entity_type: str | None = None,
        name: str | None = None,
        min_sources: int = 1,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        if min_sources < 1:
            min_sources = 1
        if limit < 0:
            limit = 0

        candidate_entities: list[Entity] = []
        normalized_name = (name or "").strip()
        if normalized_name:
            raw = self.entity_store.get_entity(normalized_name)
            if raw:
                candidate_entities = [raw]
        elif entity_type:
            candidate_entities = list(self.entity_store.query_by_type(entity_type))
        else:
            candidate_entities = list(self.entity_store.entities.values())

        items: list[dict[str, Any]] = []
        for raw in candidate_entities:
            if entity_type and raw.entity_type.value != entity_type.strip().upper():
                continue
            if len(raw.source_item_ids) < min_sources:
                continue
            payload = raw.to_dict()
            payload["source_count"] = len(raw.source_item_ids)
            items.append(payload)

        ordered = sorted(
            items,
            key=lambda value: (value.get("source_count", 0), value.get("mention_count", 0), value.get("name", "")),
            reverse=True,
        )
        return ordered[:limit]

    def entity_graph(self, entity_name: str, *, limit: int = 50) -> dict[str, Any]:
        if not (entity_name or "").strip():
            return {"entity": None, "related": []}

        source_entity = self.entity_store.get_entity(entity_name)
        if source_entity is None:
            return {"entity": None, "related": []}

        related = self.entity_store.query_related(source_entity.display_name)
        if limit < 0:
            limit = 0
        return {
            "entity": source_entity.to_dict(),
            "related": related[:limit],
            "relation_count": len(related),
        }

    def entity_stats(self) -> dict[str, Any]:
        return self.entity_store.stats()


def _safe_markdown_document(item: DataPulseItem) -> str:
    return output_record_md(item)
