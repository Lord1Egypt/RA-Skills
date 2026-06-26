"""Canonical Founder Signal setup config intake, validation, and import."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import _PROFILE_ID_PATTERN, _validate_profile
from .models import FounderSignalConfig

_DEFAULT_V2EX_PROVIDERS = ["sov2ex", "node_latest", "configured_seed_urls"]
_KNOWN_PLATFORM_NAMES = {"reddit", "v2ex"}
_LEGACY_FIELD_HINTS = {
    "subreddits": "Use platforms.reddit.communities instead of subreddits.",
    "seed_reddit_urls": "Use platforms.reddit.seed_urls instead of seed_reddit_urls.",
    "excluded_reddit_urls": "Use platforms.reddit.excluded_urls instead of excluded_reddit_urls.",
    "draft_publish_command": "Remove draft_publish_command; Draft CLI handoff uses the canonical skill contract.",
}


@dataclass(frozen=True)
class DoctorResult:
    status: str
    profile_id: str
    normalized_config: dict[str, Any]
    internal_profile: dict[str, Any]
    platform_summaries: list[str]
    warnings: list[str]
    next_command: str


@dataclass(frozen=True)
class ImportResult:
    profile_id: str
    profile_path: Path
    normalized_config_path: Path
    doctor_result: DoctorResult


def load_user_config(config_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Config file is not valid JSON: {config_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Config file must contain one JSON object: {config_path}")
    return payload


def doctor_user_config(*, root_dir: Path, config_path: Path) -> DoctorResult:
    raw_payload = load_user_config(config_path)
    normalized = _normalize_user_config(raw_payload)
    internal_profile = _build_internal_profile(normalized)
    config = FounderSignalConfig.from_dict(internal_profile)
    _validate_profile(config=config, profile_path=config_path)

    warnings: list[str] = []
    platform_summaries: list[str] = []
    for platform_name in sorted(config.platforms):
        platform_payload = normalized["platforms"][platform_name]
        summary, platform_warnings = _platform_summary(
            platform_name=platform_name,
            platform_payload=platform_payload,
            snapshots=normalized["verified_evidence_snapshots"],
        )
        platform_summaries.append(summary)
        warnings.extend(platform_warnings)

    status = "ready" if not warnings else "ready_with_warnings"
    next_command = f"python3 -m founder_signal config import {config_path.name}"
    return DoctorResult(
        status=status,
        profile_id=config.profile_id,
        normalized_config=normalized,
        internal_profile=internal_profile,
        platform_summaries=platform_summaries,
        warnings=warnings,
        next_command=next_command,
    )


def import_user_config(*, root_dir: Path, config_path: Path) -> ImportResult:
    doctor = doctor_user_config(root_dir=root_dir, config_path=config_path)
    profiles_dir = root_dir / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    profile_path = profiles_dir / f"{doctor.profile_id}.json"
    profile_path.write_text(json.dumps(doctor.internal_profile, indent=2) + "\n", encoding="utf-8")
    normalized_dir = root_dir / "config-imports"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    normalized_path = normalized_dir / f"{doctor.profile_id}.config.json"
    normalized_path.write_text(json.dumps(doctor.normalized_config, indent=2) + "\n", encoding="utf-8")
    return ImportResult(
        profile_id=doctor.profile_id,
        profile_path=profile_path,
        normalized_config_path=normalized_path,
        doctor_result=doctor,
    )


def render_doctor_report(result: DoctorResult, *, config_path: Path) -> str:
    lines = [
        "Founder Signal Doctor",
        "",
        f"Status: {'Ready' if result.status == 'ready' else 'Ready with warnings'}",
        "",
        "Profile:",
        f"- {result.profile_id}",
        "",
        "Platforms:",
    ]
    lines.extend(f"- {summary}" for summary in result.platform_summaries)
    lines.extend(
        [
            "",
            "Safety:",
            (
                "- Draft publish intent enabled"
                if result.normalized_config["draft"]["generate_publish_intent"]
                else "- Draft publish intent disabled"
            ),
            "- Draft public-page publishing is automatic after every run, including failure reports when possible",
            "- Public web publishing requires explicit confirmation",
        ]
    )
    if result.warnings:
        lines.extend(["", "Warnings:"])
        lines.extend(f"- {warning}" for warning in result.warnings)
    lines.extend(
        [
            "",
            "Validated config:",
            f"- {config_path}",
            "",
            "Next command:",
            result.next_command,
        ]
    )
    return "\n".join(lines) + "\n"


def _normalize_user_config(payload: dict[str, Any]) -> dict[str, Any]:
    legacy_fields = [field for field in _LEGACY_FIELD_HINTS if field in payload]
    if legacy_fields:
        hints = " ".join(_LEGACY_FIELD_HINTS[field] for field in legacy_fields)
        raise ValueError(f"Legacy config fields detected: {', '.join(sorted(legacy_fields))}. {hints}")

    profile_id = _require_string(payload, "profile_id")
    if not _PROFILE_ID_PATTERN.match(profile_id):
        raise ValueError(
            "profile_id must use lowercase letters, digits, '-' or '_'."
        )
    normalized_platforms = _normalize_platforms(payload.get("platforms"))
    enabled_platforms = [
        platform_name
        for platform_name, platform_payload in normalized_platforms.items()
        if platform_payload["enabled"]
    ]
    if not enabled_platforms:
        raise ValueError("At least one platform must be enabled in platforms.")

    draft_payload = payload.get("draft", {})
    if draft_payload is None:
        draft_payload = {}
    if not isinstance(draft_payload, dict):
        raise ValueError("draft must be a JSON object when provided.")
    if "draft_publish_command" in draft_payload:
        raise ValueError(
            "draft.draft_publish_command is not allowed; Draft CLI handoff uses the canonical skill contract."
        )
    if draft_payload.get("generate_publish_intent", True) is not True:
        raise ValueError(
            "draft.generate_publish_intent must stay true because Draft handoff is part of the Founder Signal review flow."
        )
    if draft_payload.get("require_confirmation_before_public_publish", True) is not True:
        raise ValueError(
            "draft.require_confirmation_before_public_publish must stay true to preserve the public Draft confirmation boundary."
        )

    normalized = {
        "profile_id": profile_id,
        "enabled": bool(payload.get("enabled", True)),
        "product_name": _require_string(payload, "product_name"),
        "product_one_liner": _require_string(payload, "product_one_liner"),
        "target_audience": _require_string(payload, "target_audience"),
        "keywords": _require_string_list(payload, "keywords", min_items=1),
        "scoring_terms": _require_string_list(payload, "scoring_terms", min_items=1),
        "negative_scoring_terms": _optional_string_list(payload, "negative_scoring_terms"),
        "discovery_terms": _optional_string_list(payload, "discovery_terms"),
        "live_discovery_terms": _optional_string_list(payload, "live_discovery_terms"),
        "research_terms": _optional_string_list(payload, "research_terms"),
        "platforms": normalized_platforms,
        "verified_evidence_snapshots": _normalize_verified_snapshots(
            payload.get("verified_evidence_snapshots", [])
        ),
        "discovery_mode": _normalized_choice(
            payload.get("discovery_mode", "research"),
            field_name="discovery_mode",
            allowed={"live", "research"},
        ),
        "max_candidates": _require_int(payload, "max_candidates", minimum=1),
        "max_action_cards": 1,
        "max_post_age_days": _optional_int(payload, "max_post_age_days", default=7, minimum=0),
        "preferred_post_age_hours": _optional_int(
            payload, "preferred_post_age_hours", default=72, minimum=0
        ),
        "min_comment_count": _optional_int(payload, "min_comment_count", default=0, minimum=0),
        "max_comment_count": _optional_int(payload, "max_comment_count", default=250, minimum=0),
        "history_ttl_days": _optional_int(payload, "history_ttl_days", default=45, minimum=1),
        "draft": {
            "generate_publish_intent": bool(draft_payload.get("generate_publish_intent", True)),
            "require_confirmation_before_public_publish": True,
        },
    }
    if normalized["min_comment_count"] > normalized["max_comment_count"]:
        raise ValueError("min_comment_count must be less than or equal to max_comment_count.")
    return normalized


def _build_internal_profile(normalized: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "profile_id": normalized["profile_id"],
        "enabled": normalized["enabled"],
        "product_name": normalized["product_name"],
        "product_one_liner": normalized["product_one_liner"],
        "target_audience": normalized["target_audience"],
        "keywords": normalized["keywords"],
        "platforms": normalized["platforms"],
        "verified_evidence_snapshots": normalized["verified_evidence_snapshots"],
        "discovery_mode": normalized["discovery_mode"],
        "max_post_age_days": normalized["max_post_age_days"],
        "preferred_post_age_hours": normalized["preferred_post_age_hours"],
        "min_comment_count": normalized["min_comment_count"],
        "max_comment_count": normalized["max_comment_count"],
        "history_ttl_days": normalized["history_ttl_days"],
        "scoring_terms": normalized["scoring_terms"],
        "negative_scoring_terms": normalized["negative_scoring_terms"],
        "max_candidates": normalized["max_candidates"],
        "max_action_cards": 1,
        "draft": normalized["draft"],
    }
    for optional_key in ("discovery_terms", "live_discovery_terms", "research_terms"):
        if normalized[optional_key]:
            payload[optional_key] = normalized[optional_key]
    return payload


def _normalize_platforms(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict):
        raise ValueError("platforms is required and must be a JSON object.")
    normalized: dict[str, dict[str, Any]] = {}
    for raw_name, raw_payload in value.items():
        platform_name = str(raw_name).strip().lower()
        if platform_name not in _KNOWN_PLATFORM_NAMES:
            raise ValueError(f"Unsupported platform '{raw_name}'. Supported platforms: reddit, v2ex.")
        if not isinstance(raw_payload, dict):
            raise ValueError(f"platforms.{platform_name} must be a JSON object.")
        if any(field in raw_payload for field in _LEGACY_FIELD_HINTS):
            raise ValueError(
                f"Legacy config fields detected under platforms.{platform_name}; use communities, seed_urls, and excluded_urls."
            )
        normalized_payload = {
            "enabled": bool(raw_payload.get("enabled", True)),
            "communities": _optional_string_list(raw_payload, "communities"),
            "seed_urls": _optional_string_list(raw_payload, "seed_urls"),
            "excluded_urls": _optional_string_list(raw_payload, "excluded_urls"),
        }
        if platform_name == "v2ex":
            providers = _optional_string_list(raw_payload, "discovery_providers")
            normalized_payload["discovery_providers"] = providers or list(_DEFAULT_V2EX_PROVIDERS)
        normalized[platform_name] = normalized_payload
    return normalized


def _normalize_verified_snapshots(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("verified_evidence_snapshots must be an array when provided.")
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"verified_evidence_snapshots[{index}] must be a JSON object.")
        platform = _normalized_choice(
            item.get("platform", "reddit"),
            field_name=f"verified_evidence_snapshots[{index}].platform",
            allowed=_KNOWN_PLATFORM_NAMES,
        )
        source_url = str(item.get("source_url") or item.get("reddit_url") or "").strip()
        if not source_url:
            raise ValueError(f"verified_evidence_snapshots[{index}].source_url is required.")
        text_snapshot = str(item.get("text_snapshot") or "").strip()
        if not text_snapshot:
            raise ValueError(
                f"verified_evidence_snapshots[{index}].text_snapshot is required."
            )
        normalized.append(
            {
                "platform": platform,
                "source_url": source_url,
                "verification_method": str(item.get("verification_method", "agent_browser")).strip()
                or "agent_browser",
                "verified_by": str(item.get("verified_by", "")).strip(),
                "text_snapshot": text_snapshot,
            }
        )
    return normalized


def _platform_summary(
    *,
    platform_name: str,
    platform_payload: dict[str, Any],
    snapshots: list[dict[str, str]],
) -> tuple[str, list[str]]:
    communities = platform_payload.get("communities", [])
    seed_urls = platform_payload.get("seed_urls", [])
    snapshot_count = sum(
        1 for snapshot in snapshots if snapshot.get("platform") == platform_name
    )
    warnings: list[str] = []
    if not communities and not seed_urls and snapshot_count == 0:
        warnings.append(
            f"{platform_name} is enabled but has no communities, seed_urls, or verified_evidence_snapshots."
        )
    if platform_name == "reddit":
        return (
            f"Reddit: enabled, {len(communities)} communities, {len(seed_urls)} seed URLs, {snapshot_count} verified snapshots",
            warnings,
        )
    providers = platform_payload.get("discovery_providers", [])
    return (
        "V2EX: enabled, "
        f"{len(communities)} communities, "
        f"{len(providers)} discovery providers, "
        f"{len(seed_urls)} seed URLs, "
        f"{snapshot_count} verified snapshots",
        warnings,
    )


def _require_string(payload: dict[str, Any], field_name: str) -> str:
    value = str(payload.get(field_name) or "").strip()
    if not value:
        raise ValueError(f"{field_name} is required.")
    return value


def _require_string_list(payload: dict[str, Any], field_name: str, *, min_items: int = 0) -> list[str]:
    values = _optional_string_list(payload, field_name)
    if len(values) < min_items:
        raise ValueError(f"{field_name} must contain at least {min_items} item(s).")
    return values


def _optional_string_list(payload: dict[str, Any], field_name: str) -> list[str]:
    value = payload.get(field_name, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be an array when provided.")
    values = [str(item).strip() for item in value]
    return [item for item in values if item]


def _require_int(payload: dict[str, Any], field_name: str, *, minimum: int | None = None) -> int:
    if field_name not in payload:
        raise ValueError(f"{field_name} is required.")
    return _coerce_int(payload[field_name], field_name=field_name, minimum=minimum)


def _optional_int(
    payload: dict[str, Any],
    field_name: str,
    *,
    default: int,
    minimum: int | None = None,
) -> int:
    if field_name not in payload:
        return default
    return _coerce_int(payload[field_name], field_name=field_name, minimum=minimum)


def _coerce_int(value: Any, *, field_name: str, minimum: int | None = None) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an integer.") from exc
    if minimum is not None and result < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}.")
    return result


def _normalized_choice(value: Any, *, field_name: str, allowed: set[str]) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ValueError(f"{field_name} must be one of: {allowed_values}.")
    return normalized
