"""Alert evaluation, storage, and simple distribution for watch missions."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from .models import DataPulseItem
from .story import build_factuality_gate, resolve_factuality_gate_status
from .triage import build_item_governance, evidence_grade_priority, serialize_item_with_governance
from .utils import alert_routing_path_from_env, alerts_markdown_path_from_env, alerts_path_from_env
from .watchlist import WatchMission


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_dt(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass
class AlertEvent:
    mission_id: str
    mission_name: str
    rule_name: str
    channels: list[str] = field(default_factory=lambda: ["json"])
    item_ids: list[str] = field(default_factory=list)
    summary: str = ""
    created_at: str = ""
    delivered_channels: list[str] = field(default_factory=list)
    id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
    governance: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = _utcnow()
        self.channels = [str(channel).strip().lower() for channel in self.channels if str(channel).strip()]
        if not self.channels:
            self.channels = ["json"]
        if not self.id:
            seed = f"{self.mission_id}:{self.rule_name}:{self.created_at}:{','.join(self.item_ids[:3])}"
            self.id = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
        self.governance = dict(self.governance or {})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AlertEvent":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in valid})


class AlertStore:
    """File-backed store for watch alert events."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or alerts_path_from_env()).expanduser()
        self.events: list[AlertEvent] = []
        self.max_items = int(os.getenv("DATAPULSE_MAX_ALERTS", "500"))
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.events = []
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.events = []
            return
        rows = raw if isinstance(raw, list) else raw.get("events", []) if isinstance(raw, dict) else []
        loaded: list[AlertEvent] = []
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, dict):
                continue
            try:
                loaded.append(AlertEvent.from_dict(row))
            except (TypeError, ValueError):
                continue
        self.events = sorted(loaded, key=lambda event: event.created_at, reverse=True)[: self.max_items]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [event.to_dict() for event in self.events[: self.max_items]]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_events(self, *, limit: int = 20, mission_id: str | None = None) -> list[AlertEvent]:
        events = self.events
        if mission_id:
            events = [event for event in events if event.mission_id == mission_id]
        return events[: max(0, limit)]

    def should_emit(self, event: AlertEvent, *, cooldown_seconds: int = 0) -> bool:
        if cooldown_seconds <= 0:
            return True
        current = _parse_dt(event.created_at)
        if current is None:
            return True
        for existing in self.events:
            if existing.mission_id != event.mission_id:
                continue
            if existing.rule_name != event.rule_name:
                continue
            seen_at = _parse_dt(existing.created_at)
            if seen_at is None:
                continue
            if current - seen_at < timedelta(seconds=cooldown_seconds):
                return False
        return True

    def add(self, event: AlertEvent, *, cooldown_seconds: int = 0) -> bool:
        if not self.should_emit(event, cooldown_seconds=cooldown_seconds):
            return False
        self.events.insert(0, event)
        self.events = sorted(self.events, key=lambda row: row.created_at, reverse=True)[: self.max_items]
        self.save()
        return True


class AlertRouteStore:
    """File-backed named delivery routes for alert sinks."""

    SUPPORTED_CHANNELS = {"webhook", "feishu", "telegram", "markdown"}

    def __init__(self, path: str | None = None):
        self.path = Path(path or alert_routing_path_from_env()).expanduser()
        self.routes: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.routes = {}
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.routes = {}
            return
        rows = raw.get("routes", raw) if isinstance(raw, dict) else {}
        if not isinstance(rows, dict):
            self.routes = {}
            return
        normalized: dict[str, dict[str, Any]] = {}
        for name, value in rows.items():
            if not isinstance(value, dict):
                continue
            route_name = str(name or "").strip().lower()
            channel = str(value.get("channel", "")).strip().lower()
            if not route_name or not channel:
                continue
            payload = dict(value)
            payload["channel"] = channel
            normalized[route_name] = payload
        self.routes = normalized

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"routes": self.routes}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _normalize_name(name: str) -> str:
        return str(name or "").strip().lower()

    @staticmethod
    def _normalize_headers(headers: Any) -> dict[str, str]:
        if not isinstance(headers, dict):
            return {}
        normalized: dict[str, str] = {}
        for key, value in headers.items():
            header_key = str(key or "").strip()
            if not header_key:
                continue
            normalized[header_key] = str(value or "").strip()
        return normalized

    @classmethod
    def _normalize_route_payload(
        cls,
        payload: dict[str, Any],
        *,
        existing: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("alert route payload must be an object")
        previous = dict(existing or {})
        channel_raw = payload.get("channel", previous.get("channel", ""))
        channel = str(channel_raw or "").strip().lower()
        if not channel:
            raise ValueError("channel is required")
        if channel not in cls.SUPPORTED_CHANNELS:
            supported = ", ".join(sorted(cls.SUPPORTED_CHANNELS))
            raise ValueError(f"unsupported alert channel: {channel}; supported: {supported}")

        normalized: dict[str, Any] = {"channel": channel}
        description = str(payload.get("description", previous.get("description", "")) or "").strip()
        if description:
            normalized["description"] = description

        timeout_value = payload.get("timeout_seconds", previous.get("timeout_seconds"))
        if timeout_value not in (None, ""):
            try:
                timeout_seconds = float(timeout_value)
            except (TypeError, ValueError) as exc:
                raise ValueError("timeout_seconds must be numeric") from exc
            if timeout_seconds <= 0:
                raise ValueError("timeout_seconds must be greater than 0")
            normalized["timeout_seconds"] = timeout_seconds

        if channel == "webhook":
            webhook_url = str(payload.get("webhook_url", previous.get("webhook_url", "")) or "").strip()
            if webhook_url:
                normalized["webhook_url"] = webhook_url
            authorization = str(payload.get("authorization", previous.get("authorization", "")) or "").strip()
            if authorization == "***" and str(previous.get("authorization", "")).strip():
                authorization = str(previous.get("authorization", "")).strip()
            if authorization:
                normalized["authorization"] = authorization
            headers = cls._normalize_headers(payload.get("headers", previous.get("headers", {})))
            if headers:
                normalized["headers"] = headers
        elif channel == "feishu":
            feishu_webhook = str(payload.get("feishu_webhook", previous.get("feishu_webhook", "")) or "").strip()
            if feishu_webhook:
                normalized["feishu_webhook"] = feishu_webhook
        elif channel == "telegram":
            telegram_bot_token = str(
                payload.get("telegram_bot_token", previous.get("telegram_bot_token", "")) or ""
            ).strip()
            if telegram_bot_token == "***" and str(previous.get("telegram_bot_token", "")).strip():
                telegram_bot_token = str(previous.get("telegram_bot_token", "")).strip()
            if telegram_bot_token:
                normalized["telegram_bot_token"] = telegram_bot_token
            telegram_chat_id = str(payload.get("telegram_chat_id", previous.get("telegram_chat_id", "")) or "").strip()
            if telegram_chat_id:
                normalized["telegram_chat_id"] = telegram_chat_id

        return normalized

    @staticmethod
    def _redact_route(route: dict[str, Any]) -> dict[str, Any]:
        redacted: dict[str, Any] = {}
        for key, value in route.items():
            lowered = str(key).strip().lower()
            if any(token in lowered for token in ("token", "secret", "authorization", "password")):
                redacted[key] = "***"
            elif lowered == "headers" and isinstance(value, dict):
                header_map: dict[str, Any] = {}
                for header_key, header_value in value.items():
                    header_lowered = str(header_key).strip().lower()
                    if any(token in header_lowered for token in ("authorization", "token", "secret", "password")):
                        header_map[header_key] = "***"
                    else:
                        header_map[header_key] = header_value
                redacted[key] = header_map
            else:
                redacted[key] = value
        return redacted

    def get(self, name: str) -> dict[str, Any] | None:
        route_name = self._normalize_name(name)
        if not route_name:
            return None
        payload = self.routes.get(route_name)
        if payload is None:
            return None
        return dict(payload)

    def show(self, name: str) -> dict[str, Any] | None:
        route_name = self._normalize_name(name)
        if not route_name:
            return None
        payload = self.get(route_name)
        if payload is None:
            return None
        redacted = self._redact_route(payload)
        redacted["name"] = route_name
        return redacted

    def list_routes(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for name, route in sorted(self.routes.items()):
            payload = self.show(name)
            if payload is not None:
                rows.append(payload)
        return rows

    def create(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        route_name = self._normalize_name(name)
        if not route_name:
            raise ValueError("route name is required")
        if route_name in self.routes:
            raise ValueError(f"alert route already exists: {route_name}")
        self.routes[route_name] = self._normalize_route_payload(payload)
        self.save()
        created = self.show(route_name)
        if created is None:
            raise ValueError(f"failed to create alert route: {route_name}")
        return created

    def update(self, name: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        route_name = self._normalize_name(name)
        if not route_name:
            return None
        existing = self.routes.get(route_name)
        if existing is None:
            return None
        self.routes[route_name] = self._normalize_route_payload(payload, existing=existing)
        self.save()
        return self.show(route_name)

    def delete(self, name: str) -> dict[str, Any] | None:
        route_name = self._normalize_name(name)
        if not route_name:
            return None
        existing = self.show(route_name)
        if existing is None:
            return None
        del self.routes[route_name]
        self.save()
        return existing


def append_alert_markdown(event: AlertEvent, items: list[DataPulseItem], *, path: str | None = None) -> str:
    target = Path(path or alerts_markdown_path_from_env()).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    governance = event.governance if isinstance(event.governance, dict) else {}
    delivery_risk = governance.get("delivery_risk", {}) if isinstance(governance.get("delivery_risk"), dict) else {}
    factuality = governance.get("factuality", {}) if isinstance(governance.get("factuality"), dict) else {}
    factuality_backend = (
        factuality.get("backend_review", {})
        if isinstance(factuality.get("backend_review"), dict)
        else {}
    )
    effective_factuality_status = resolve_factuality_gate_status(factuality)
    show_backend_review = bool(factuality_backend) and (
        str(factuality_backend.get("status", "skipped") or "skipped").strip().lower() != "skipped"
        or bool(factuality_backend.get("used_output"))
        or bool(factuality_backend.get("summary"))
        or bool(factuality_backend.get("reasons"))
        or bool(factuality_backend.get("signals"))
        or bool(factuality_backend.get("warnings"))
        or bool(factuality_backend.get("error"))
    )
    with target.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {event.mission_name} | {event.rule_name}\n")
        handle.write(f"- created_at: {event.created_at}\n")
        handle.write(f"- mission_id: {event.mission_id}\n")
        handle.write(f"- alert_id: {event.id}\n")
        handle.write(f"- summary: {event.summary}\n")
        handle.write(f"- evidence_grade: {governance.get('evidence_grade', 'working')}\n")
        handle.write(f"- factuality_status: {factuality.get('status', 'review_required')}\n")
        handle.write(f"- factuality_score: {float(factuality.get('score', 0.0) or 0.0):.3f}\n")
        if effective_factuality_status != str(factuality.get("status", "review_required") or "review_required").strip().lower():
            handle.write(f"- factuality_effective_status: {effective_factuality_status}\n")
        if show_backend_review:
            handle.write(f"- factuality_backend_status: {factuality_backend.get('status', 'skipped')}\n")
            handle.write(
                f"- factuality_backend_verdict: {factuality_backend.get('backend_status', effective_factuality_status)}\n"
            )
        handle.write(f"- delivery_status: {delivery_risk.get('status', 'recorded')}\n")
        handle.write(f"- delivery_risk: {delivery_risk.get('level', 'medium')}\n")
        for reason in factuality.get("reasons", []) if isinstance(factuality.get("reasons"), list) else []:
            handle.write(f"- factuality_note: {reason}\n")
        for signal in factuality.get("signals", []) if isinstance(factuality.get("signals"), list) else []:
            if not isinstance(signal, dict):
                continue
            handle.write(
                f"- factuality_signal: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}\n"
            )
        if show_backend_review:
            if factuality_backend.get("summary"):
                handle.write(f"- factuality_backend_summary: {factuality_backend.get('summary', '')}\n")
            for reason in factuality_backend.get("reasons", []) if isinstance(factuality_backend.get("reasons"), list) else []:
                handle.write(f"- factuality_backend_note: {reason}\n")
            for signal in factuality_backend.get("signals", []) if isinstance(factuality_backend.get("signals"), list) else []:
                if not isinstance(signal, dict):
                    continue
                handle.write(
                    f"- factuality_backend_signal: {signal.get('kind', 'signal')}={signal.get('status', 'unknown')} | {signal.get('detail', '')}\n"
                )
            for warning in factuality_backend.get("warnings", []) if isinstance(factuality_backend.get("warnings"), list) else []:
                handle.write(f"- factuality_backend_warning: {warning}\n")
            if factuality_backend.get("error"):
                handle.write(f"- factuality_backend_error: {factuality_backend.get('error', '')}\n")
        for reason in delivery_risk.get("reasons", []) if isinstance(delivery_risk.get("reasons"), list) else []:
            handle.write(f"- delivery_note: {reason}\n")
        for item in items[:5]:
            item_governance = build_item_governance(item)
            handle.write(
                f"- [{item.title}]({item.url}) | score={item.score} confidence={item.confidence:.3f} "
                f"grade={item_governance.get('evidence_grade', 'working')}\n"
            )
        handle.write("\n---\n")
    return str(target)


def _alert_text(event: AlertEvent, items: list[DataPulseItem]) -> str:
    governance = event.governance if isinstance(event.governance, dict) else {}
    delivery_risk = governance.get("delivery_risk", {}) if isinstance(governance.get("delivery_risk"), dict) else {}
    factuality = governance.get("factuality", {}) if isinstance(governance.get("factuality"), dict) else {}
    effective_factuality_status = resolve_factuality_gate_status(factuality)
    lines = [
        f"[DataPulse] {event.mission_name} / {event.rule_name}",
        event.summary,
        f"factuality={effective_factuality_status}/{float(factuality.get('score', 0.0) or 0.0):.3f}",
        f"evidence_grade={governance.get('evidence_grade', 'working')} delivery={delivery_risk.get('status', 'recorded')}/{delivery_risk.get('level', 'medium')}",
    ]
    for reason in factuality.get("reasons", [])[:2] if isinstance(factuality.get("reasons"), list) else []:
        lines.append(f"- factuality_note: {reason}")
    for item in items[:5]:
        item_governance = build_item_governance(item)
        lines.append(
            f"- {item.title} | score={item.score} confidence={item.confidence:.3f} "
            f"| grade={item_governance.get('evidence_grade', 'working')} | {item.url}"
        )
    return "\n".join(lines)


def _post_json(url: str, payload: dict[str, Any], *, timeout: float = 10.0, headers: dict[str, str] | None = None) -> None:
    response = requests.post(url, json=payload, headers=headers or {}, timeout=timeout)
    response.raise_for_status()


def _resolve_webhook_url(rule: dict[str, Any]) -> str:
    return str(
        rule.get("webhook_url")
        or os.getenv("DATAPULSE_ALERT_WEBHOOK_URL", "")
    ).strip()


def _resolve_feishu_url(rule: dict[str, Any]) -> str:
    return str(
        rule.get("feishu_webhook")
        or os.getenv("DATAPULSE_FEISHU_WEBHOOK_URL", "")
    ).strip()


def _resolve_telegram_bot_token(rule: dict[str, Any]) -> str:
    return str(
        rule.get("telegram_bot_token")
        or os.getenv("DATAPULSE_TELEGRAM_BOT_TOKEN", "")
    ).strip()


def _resolve_telegram_chat_id(rule: dict[str, Any]) -> str:
    return str(
        rule.get("telegram_chat_id")
        or os.getenv("DATAPULSE_TELEGRAM_CHAT_ID", "")
    ).strip()


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


def _max_risk_level(left: str, right: str) -> str:
    priority = {"none": 0, "low": 1, "medium": 2, "high": 3}
    return left if priority.get(left, 0) >= priority.get(right, 0) else right


def _aggregate_alert_evidence_grade(governances: list[dict[str, Any]]) -> str:
    if not governances:
        return "working"
    ranks = [evidence_grade_priority(row.get("evidence_grade")) for row in governances]
    if ranks and min(ranks) >= evidence_grade_priority("verified"):
        return "verified"
    if ranks and min(ranks) >= evidence_grade_priority("reviewed"):
        return "reviewed"
    return "working"


def _build_route_observations(
    rule: dict[str, Any],
    *,
    delivered_channels: list[str] | None = None,
    delivery_errors: dict[str, str] | None = None,
    held_channels: list[str] | None = None,
) -> list[dict[str, Any]]:
    delivered = {str(label or "").strip().lower() for label in delivered_channels or [] if str(label or "").strip()}
    errors = delivery_errors if isinstance(delivery_errors, dict) else {}
    held = {str(label or "").strip().lower() for label in held_channels or [] if str(label or "").strip()}
    observations: list[dict[str, Any]] = [
        {
            "kind": "record",
            "label": "json",
            "channel": "json",
            "route_name": "",
            "status": "recorded",
            "error": "",
        }
    ]

    for channel in _normalize_rule_channels(rule):
        if channel == "json":
            continue
        error_message = str(errors.get(channel, "") or "").strip()
        if channel in held:
            status = "held"
        elif channel in delivered:
            status = "delivered"
        elif error_message:
            status = "failed"
        else:
            status = "pending"
        observations.append(
            {
                "kind": "direct_channel",
                "label": channel,
                "channel": channel,
                "route_name": "",
                "status": status,
                "error": error_message,
            }
        )

    routing = AlertRouteStore()
    for route_name in _normalize_route_names(rule):
        route = routing.get(route_name)
        channel = str(route.get("channel", "")).strip().lower() if isinstance(route, dict) else ""
        label = f"{channel}:{route_name}" if channel else f"route:{route_name}"
        error_message = str(errors.get(label) or errors.get(f"route:{route_name}") or "").strip()
        if route is None:
            status = "missing"
        elif label in held:
            status = "held"
        elif label in delivered:
            status = "delivered"
        elif error_message:
            status = "failed"
        else:
            status = "pending"
        observations.append(
            {
                "kind": "named_route",
                "label": label,
                "channel": channel or "unknown",
                "route_name": route_name,
                "status": status,
                "error": error_message,
            }
        )
    return observations


def _build_alert_governance(
    event: AlertEvent,
    items: list[DataPulseItem],
    *,
    delivered_channels: list[str] | None = None,
    delivery_errors: dict[str, str] | None = None,
    held_channels: list[str] | None = None,
) -> dict[str, Any]:
    rule = event.extra.get("rule", {}) if isinstance(event.extra, dict) else {}
    if not isinstance(rule, dict):
        rule = {}
    item_governances = [build_item_governance(item) for item in items]
    aggregated = item_governances[:3] or item_governances
    evidence_grade = _aggregate_alert_evidence_grade(aggregated)
    evidence_score = round(
        sum(float(row.get("evidence_score", 0.0) or 0.0) for row in aggregated) / max(1, len(aggregated)),
        4,
    )
    route_observations = _build_route_observations(
        rule,
        delivered_channels=delivered_channels or event.delivered_channels,
        delivery_errors=delivery_errors,
        held_channels=held_channels,
    )
    factuality_rows: list[dict[str, Any]] = []
    for item, governance in zip(items, item_governances):
        grounding = governance.get("grounding", {}) if isinstance(governance.get("grounding"), dict) else {}
        provenance = governance.get("provenance", {}) if isinstance(governance.get("provenance"), dict) else {}
        factuality_rows.append(
            {
                "item_id": provenance.get("item_id", item.id),
                "title": item.title,
                "source_name": provenance.get("source_name", item.source_name),
                "evidence_grade": str(governance.get("evidence_grade", "working")).strip().lower() or "working",
                "evidence_score": float(governance.get("evidence_score", 0.0) or 0.0),
                "review_state": str(governance.get("review_state", "new") or "new").strip().lower() or "new",
                "confidence": item.confidence,
                "grounded_claim_count": int(grounding.get("claim_count", 0) or 0),
            }
        )
    factuality = build_factuality_gate(
        subject="alert",
        surface="alert_escalation",
        evidence_rows=factuality_rows,
        source_names=[item.source_name for item in items],
        grounded_claim_count=sum(
            int(
                (
                    governance.get("grounding", {})
                    if isinstance(governance.get("grounding"), dict)
                    else {}
                ).get("claim_count", 0)
                or 0
            )
            for governance in item_governances
        ),
        contradiction_count=0,
    )

    delivery_status = "recorded"
    delivery_level = "low"
    delivery_reasons: list[str] = []
    push_observations = [row for row in route_observations if row.get("kind") != "record"]
    effective_factuality_status = resolve_factuality_gate_status(factuality)

    if evidence_grade != "verified":
        delivery_status = "review_required"
        delivery_level = "medium"
        delivery_reasons.append("Alert is backed by evidence that is still actionable but not fully verified.")
    if effective_factuality_status == "blocked":
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "high")
        delivery_reasons.append("Factuality gate blocked outward-facing alert escalation pending analyst review.")
    elif effective_factuality_status != "ready":
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("Factuality gate requires analyst review before outward-facing alert escalation.")
    if any(row.get("status") in {"failed", "missing"} for row in push_observations):
        delivery_status = "degraded"
        delivery_level = "high"
        delivery_reasons.append("One or more delivery targets failed or are missing route configuration.")
    elif any(row.get("status") == "held" for row in push_observations):
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("One or more external escalation targets were held by the factuality gate.")
    elif any(row.get("status") == "pending" for row in push_observations):
        delivery_status = "review_required"
        delivery_level = _max_risk_level(delivery_level, "medium")
        delivery_reasons.append("Some delivery targets are configured but not yet observed as delivered.")
    elif push_observations and evidence_grade == "verified" and effective_factuality_status == "ready":
        delivery_status = "delivered"

    provenance_chain: list[dict[str, Any]] = []
    for item, governance in zip(items, item_governances):
        provenance = governance.get("provenance", {}) if isinstance(governance.get("provenance"), dict) else {}
        provenance_chain.append(
            {
                "item_id": provenance.get("item_id", item.id),
                "source_name": provenance.get("source_name", item.source_name),
                "source_type": provenance.get("source_type", item.source_type.value),
                "review_state": governance.get("review_state", "new"),
                "evidence_grade": governance.get("evidence_grade", "working"),
                "url": provenance.get("url", item.url),
            }
        )

    return {
        "subject": "alert",
        "evidence_grade": evidence_grade,
        "evidence_score": evidence_score,
        "factuality": factuality,
        "provenance": {
            "kind": "alert",
            "alert_id": event.id,
            "mission_id": event.mission_id,
            "mission_name": event.mission_name,
            "rule_name": event.rule_name,
            "item_ids": list(event.item_ids),
            "source_names": sorted({item.source_name for item in items}),
            "route_names": _normalize_route_names(rule),
            "channels": list(event.channels),
            "evidence_chain": provenance_chain,
            "created_at": event.created_at,
        },
        "delivery_risk": {
            "surface": "alert_delivery",
            "status": delivery_status,
            "level": delivery_level,
            "reasons": delivery_reasons,
            "route_observations": route_observations,
        },
    }


def _resolve_delivery_targets(rule: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    targets: list[dict[str, Any]] = []
    errors: dict[str, str] = {}

    for channel in _normalize_rule_channels(rule):
        if channel == "json":
            continue
        targets.append(
            {
                "label": channel,
                "channel": channel,
                "config": dict(rule),
            }
        )

    route_names = _normalize_route_names(rule)
    if route_names:
        routing = AlertRouteStore()
        for route_name in route_names:
            route = routing.get(route_name)
            label = f"route:{route_name}"
            if route is None:
                errors[label] = "alert route not found"
                continue
            channel = str(route.get("channel", "")).strip().lower()
            if not channel:
                errors[label] = "route channel is required"
                continue
            merged = dict(route)
            if "timeout_seconds" in rule:
                merged["timeout_seconds"] = rule["timeout_seconds"]
            targets.append(
                {
                    "label": f"{channel}:{route_name}",
                    "channel": channel,
                    "config": merged,
                }
            )
    return targets, errors


def dispatch_alert_event(
    event: AlertEvent,
    items: list[DataPulseItem],
    *,
    markdown_path: str | None = None,
) -> tuple[list[str], dict[str, str]]:
    rule = event.extra.get("rule", {}) if isinstance(event.extra, dict) else {}
    targets, errors = _resolve_delivery_targets(rule)
    if not event.governance:
        event.governance = _build_alert_governance(event, items, delivery_errors=errors)
    factuality = event.governance.get("factuality", {}) if isinstance(event.governance, dict) else {}
    factuality_status = resolve_factuality_gate_status(factuality)
    delivered = ["json"]
    held: list[str] = []
    text = _alert_text(event, items)
    timeout = float(rule.get("timeout_seconds", 10.0) or 10.0)

    for target in targets:
        label = str(target.get("label", "")).strip() or str(target.get("channel", "")).strip().lower()
        channel = str(target.get("channel", "")).strip().lower()
        config = target.get("config", rule)
        if not isinstance(config, dict):
            config = rule
        try:
            if channel == "markdown":
                append_alert_markdown(event, items, path=markdown_path)
            elif channel == "webhook":
                url = _resolve_webhook_url(config)
                if not url:
                    raise ValueError("webhook_url is required")
                if factuality_status != "ready":
                    held.append(label or channel)
                    continue
                headers = dict(config.get("headers")) if isinstance(config.get("headers"), dict) else {}
                authorization = str(config.get("authorization", "") or "").strip()
                if authorization and "Authorization" not in headers:
                    headers["Authorization"] = authorization
                _post_json(
                    url,
                    {
                        "alert": event.to_dict(),
                        "items": [serialize_item_with_governance(item) for item in items[:10]],
                    },
                    timeout=float(config.get("timeout_seconds", timeout) or timeout),
                    headers=headers or None,
                )
            elif channel == "feishu":
                url = _resolve_feishu_url(config)
                if not url:
                    raise ValueError("feishu_webhook is required")
                if factuality_status != "ready":
                    held.append(label or channel)
                    continue
                _post_json(
                    url,
                    {"msg_type": "text", "content": {"text": text}},
                    timeout=float(config.get("timeout_seconds", timeout) or timeout),
                )
            elif channel == "telegram":
                bot_token = _resolve_telegram_bot_token(config)
                chat_id = _resolve_telegram_chat_id(config)
                if not bot_token or not chat_id:
                    raise ValueError("telegram_bot_token and telegram_chat_id are required")
                if factuality_status != "ready":
                    held.append(label or channel)
                    continue
                _post_json(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    {"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
                    timeout=float(config.get("timeout_seconds", timeout) or timeout),
                )
            else:
                raise ValueError(f"unsupported alert channel: {channel}")
        except Exception as exc:  # noqa: BLE001
            errors[label or channel] = str(exc)
            continue
        delivered.append(label or channel)
    event.governance = _build_alert_governance(
        event,
        items,
        delivered_channels=delivered,
        delivery_errors=errors,
        held_channels=held,
    )
    return delivered, errors


def _normalize_rule_channels(rule: dict[str, Any]) -> list[str]:
    raw = rule.get("channels", ["json"])
    if isinstance(raw, str):
        raw = [raw]
    channels = [str(channel).strip().lower() for channel in raw if str(channel).strip()]
    return channels or ["json"]


def _normalize_rule_source_types(rule: dict[str, Any]) -> list[str]:
    source_types = _normalize_string_list(rule.get("source_types"))
    if source_types:
        return source_types
    return _normalize_string_list(rule.get("source_type"))


def _normalize_rule_required_tags(rule: dict[str, Any]) -> list[str]:
    tags = _normalize_string_list(rule.get("required_tags"))
    single = str(rule.get("required_tag", "")).strip().lower()
    if single and single not in tags:
        tags.append(single)
    return tags


def _item_domain(item: DataPulseItem) -> str:
    parsed = urlparse(item.url or "")
    return str(parsed.netloc or "").strip().lower()


def _item_search_text(item: DataPulseItem) -> str:
    tags = " ".join(item.tags)
    return " ".join(
        part for part in (
            item.title,
            item.content,
            item.url,
            item.source_name,
            tags,
        )
        if str(part or "").strip()
    ).lower()


def _item_age_minutes(item: DataPulseItem) -> float | None:
    fetched_at = _parse_dt(item.fetched_at)
    if fetched_at is None:
        return None
    return max(0.0, (datetime.now(timezone.utc) - fetched_at).total_seconds() / 60.0)


def _matches_alert_rule(item: DataPulseItem, rule: dict[str, Any]) -> bool:
    if item.score < int(rule.get("min_score", 0) or 0):
        return False
    if item.confidence < float(rule.get("min_confidence", 0.0) or 0.0):
        return False

    item_tags = {str(tag).strip().lower() for tag in item.tags if str(tag).strip()}
    required_tags = _normalize_rule_required_tags(rule)
    if required_tags and not set(required_tags).issubset(item_tags):
        return False

    excluded_tags = set(_normalize_string_list(rule.get("excluded_tags")))
    if excluded_tags and item_tags.intersection(excluded_tags):
        return False

    source_types = set(_normalize_rule_source_types(rule))
    if source_types and item.source_type.value not in source_types:
        return False

    domains = _normalize_string_list(rule.get("domains"))
    if domains:
        domain = _item_domain(item)
        if not any(domain == candidate or domain.endswith(f".{candidate}") for candidate in domains):
            return False

    search_text = _item_search_text(item)
    keyword_any = _normalize_string_list(rule.get("keyword_any"))
    if keyword_any and not any(token in search_text for token in keyword_any):
        return False

    keyword_all = _normalize_string_list(rule.get("keyword_all"))
    if keyword_all and not all(token in search_text for token in keyword_all):
        return False

    exclude_keywords = _normalize_string_list(rule.get("exclude_keywords"))
    if exclude_keywords and any(token in search_text for token in exclude_keywords):
        return False

    max_age_minutes = int(rule.get("max_age_minutes", 0) or 0)
    if max_age_minutes > 0:
        age_minutes = _item_age_minutes(item)
        if age_minutes is None or age_minutes > max_age_minutes:
            return False

    return True


def _rule_summary(mission: WatchMission, rule_name: str, rule: dict[str, Any], match_count: int) -> str:
    criteria: list[str] = []
    if int(rule.get("min_score", 0) or 0) > 0:
        criteria.append(f"score>={int(rule.get('min_score', 0) or 0)}")
    if float(rule.get("min_confidence", 0.0) or 0.0) > 0:
        criteria.append(f"confidence>={float(rule.get('min_confidence', 0.0) or 0.0):.2f}")
    required_tags = _normalize_rule_required_tags(rule)
    if required_tags:
        criteria.append(f"tags={','.join(required_tags[:3])}")
    domains = _normalize_string_list(rule.get("domains"))
    if domains:
        criteria.append(f"domains={','.join(domains[:3])}")
    keyword_any = _normalize_string_list(rule.get("keyword_any"))
    if keyword_any:
        criteria.append(f"keywords(any)={','.join(keyword_any[:3])}")
    keyword_all = _normalize_string_list(rule.get("keyword_all"))
    if keyword_all:
        criteria.append(f"keywords(all)={','.join(keyword_all[:3])}")
    source_types = _normalize_rule_source_types(rule)
    if source_types:
        criteria.append(f"source_types={','.join(source_types[:3])}")
    max_age_minutes = int(rule.get("max_age_minutes", 0) or 0)
    if max_age_minutes > 0:
        criteria.append(f"age<={max_age_minutes}m")
    suffix = ", ".join(criteria[:4]) if criteria else "configured filters"
    return f"{mission.name} triggered {rule_name}: {match_count} item(s) matched {suffix}"


def evaluate_watch_alerts(
    mission: WatchMission,
    items: list[DataPulseItem],
) -> list[tuple[AlertEvent, list[DataPulseItem], int]]:
    """Evaluate alert rules for one mission run."""
    events: list[tuple[AlertEvent, list[DataPulseItem], int]] = []
    for index, raw_rule in enumerate(mission.alert_rules, start=1):
        if not isinstance(raw_rule, dict) or raw_rule.get("enabled", True) is False:
            continue
        min_results = max(1, int(raw_rule.get("min_results", 1) or 1))
        matches: list[DataPulseItem] = []
        for item in items:
            if _matches_alert_rule(item, raw_rule):
                matches.append(item)
        if len(matches) < min_results:
            continue
        rule_name = str(raw_rule.get("name", "")).strip() or f"rule-{index}"
        summary = _rule_summary(mission, rule_name, raw_rule, len(matches))
        event = AlertEvent(
            mission_id=mission.id,
            mission_name=mission.name,
            rule_name=rule_name,
            channels=_normalize_rule_channels(raw_rule),
            item_ids=[item.id for item in matches],
            summary=summary,
            extra={
                "rule": raw_rule,
                "match_count": len(matches),
                "top_item_title": matches[0].title if matches else "",
            },
        )
        event.governance = _build_alert_governance(event, matches)
        cooldown_seconds = int(raw_rule.get("cooldown_seconds", 0) or 0)
        events.append((event, matches, cooldown_seconds))
    return events
