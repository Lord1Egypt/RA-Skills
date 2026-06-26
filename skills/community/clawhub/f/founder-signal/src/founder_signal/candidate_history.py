"""Local candidate history for repeat-run deduplication."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_STATE_DIRNAME = "state"
_HISTORY_FILENAME = "past-candidates.json"
_HISTORY_VERSION = 2


def load_excluded_source_ids(
    *,
    root_dir: Path,
    profile_id: str,
    profile_excluded_urls_by_platform: dict[str, list[str]],
    ttl_days: int = 45,
) -> tuple[set[str], dict[str, int]]:
    """Return platform-aware source IDs that discovery should skip."""
    profile_ids: set[str] = set()
    for platform, urls in profile_excluded_urls_by_platform.items():
        normalized_platform = str(platform).strip().lower() or "reddit"
        for url in _normalize_urls(urls):
            profile_ids.add(url)
            profile_ids.add(_canonical_source_id(platform=normalized_platform, source_url=url))
    history_ids, expired_count, retained_count = _history_source_ids(
        root_dir=root_dir,
        profile_id=profile_id,
        ttl_days=ttl_days,
    )
    return profile_ids | history_ids, {
        "profile_excluded_source_ids": len(profile_ids),
        "history_excluded_source_ids": len(history_ids),
        "history_expired_source_ids": expired_count,
        "history_retained_source_ids": retained_count,
        "total_excluded_source_ids": len(profile_ids | history_ids),
        # Backward-compatible report fields.
        "profile_excluded_reddit_urls": len(
            [item for item in profile_ids if item.startswith("reddit:")]
        ),
        "history_excluded_reddit_urls": len(
            [item for item in history_ids if item.startswith("reddit:")]
        ),
        "history_expired_reddit_urls": expired_count,
        "history_retained_reddit_urls": len(
            [item for item in history_ids if item.startswith("reddit:")]
        ),
        "total_excluded_reddit_urls": len(
            [item for item in (profile_ids | history_ids) if item.startswith("reddit:")]
        ),
    }


def load_excluded_reddit_urls(
    *,
    root_dir: Path,
    profile_id: str,
    profile_excluded_reddit_urls: list[str],
    ttl_days: int,
) -> tuple[set[str], dict[str, int]]:
    """Return legacy Reddit URL exclusions."""
    source_ids, counts = load_excluded_source_ids(
        root_dir=root_dir,
        profile_id=profile_id,
        profile_excluded_urls_by_platform={"reddit": profile_excluded_reddit_urls},
        ttl_days=ttl_days,
    )
    reddit_urls = {item.removeprefix("reddit:") for item in source_ids if item.startswith("reddit:")}
    reddit_urls.update(item for item in source_ids if item.startswith("http"))
    return reddit_urls, counts


def record_discovered_candidates(
    *,
    root_dir: Path,
    profile_id: str,
    run_id: str,
    candidates: list[dict[str, Any]],
) -> Path:
    """Persist platform-aware source IDs so later runs can skip repeats."""
    history_path = _history_path(root_dir)
    payload = _load_history_payload(history_path)
    payload["version"] = _HISTORY_VERSION
    profiles = payload.setdefault("profiles", {})
    profile_payload = profiles.setdefault(profile_id, {"candidates": {}})
    candidate_map = profile_payload.setdefault("candidates", {})
    now = datetime.now(timezone.utc).isoformat()

    for candidate in candidates:
        source_url = str(candidate.get("source_url") or candidate.get("reddit_url") or "").strip()
        platform = str(candidate.get("platform") or candidate.get("source_platform") or "reddit").strip().lower() or "reddit"
        source_id = str(candidate.get("source_id") or f"{platform}:{source_url}").strip()
        if not source_url or not source_id:
            continue
        existing = candidate_map.get(source_id)
        if not isinstance(existing, dict):
            existing = {
                "platform": platform,
                "source_url": source_url,
                "first_seen_run_id": run_id,
                "first_seen_at": now,
            }
        existing.update(
            {
                "platform": platform,
                "source_url": source_url,
                "last_seen_run_id": run_id,
                "last_seen_at": now,
                "source_type": str(candidate.get("source_type") or ""),
                "discovery_method": str(candidate.get("discovery_method") or ""),
                "last_decision": str(
                    candidate.get("selection_gate_reason")
                    or candidate.get("read_status")
                    or candidate.get("status")
                    or "discovered"
                ),
            }
        )
        if platform == "reddit":
            existing["reddit_url"] = source_url
        candidate_map[source_id] = existing

    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return history_path


def _history_source_ids(
    *,
    root_dir: Path,
    profile_id: str,
    ttl_days: int,
) -> tuple[set[str], int, int]:
    history_path = _history_path(root_dir)
    payload = _load_history_payload(history_path)
    profile_payload = payload.get("profiles", {}).get(profile_id, {})
    candidate_map = profile_payload.get("candidates", {})
    if not isinstance(candidate_map, dict):
        return set(), 0, 0

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=ttl_days)
    source_ids: set[str] = set()
    expired_count = 0
    retained_count = 0
    changed = False
    for key, value in list(candidate_map.items()):
        timestamp = None
        if isinstance(value, dict):
            timestamp = _parse_history_timestamp(
                value.get("last_seen_at") or value.get("first_seen_at") or ""
            )
        if timestamp is not None and timestamp < cutoff:
            candidate_map.pop(key, None)
            expired_count += 1
            changed = True
            continue
        key_text = str(key).strip()
        if not key_text:
            continue
        retained_count += 1
        # Version 1 URL-only history is Reddit history.
        if key_text.startswith("http"):
            source_ids.add(f"reddit:{key_text}")
            continue
        if ":" in key_text.split("//", 1)[0]:
            source_ids.add(key_text)
            continue
        if isinstance(value, dict):
            platform = str(value.get("platform") or "reddit").strip().lower() or "reddit"
            source_url = str(value.get("source_url") or value.get("reddit_url") or "").strip()
            if source_url:
                source_ids.add(f"{platform}:{source_url}")
    if changed:
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return source_ids, expired_count, retained_count


def _canonical_source_id(*, platform: str, source_url: str) -> str:
    try:
        from .platforms import get_adapter

        adapter = get_adapter(platform)
    except Exception:
        return f"{platform}:{source_url}"
    canonicalizer = getattr(adapter, "canonical_source_id", None)
    if callable(canonicalizer):
        return str(canonicalizer(source_url))
    return f"{platform}:{source_url}"


def _history_path(root_dir: Path) -> Path:
    return root_dir / _STATE_DIRNAME / _HISTORY_FILENAME


def _load_history_payload(history_path: Path) -> dict[str, Any]:
    if not history_path.exists():
        return {"version": _HISTORY_VERSION, "profiles": {}}
    try:
        payload = json.loads(history_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": _HISTORY_VERSION, "profiles": {}}
    if not isinstance(payload, dict):
        return {"version": _HISTORY_VERSION, "profiles": {}}
    payload.setdefault("version", 1)
    payload.setdefault("profiles", {})
    return payload


def _normalize_urls(urls: list[str]) -> set[str]:
    return {str(url).strip() for url in urls if str(url).strip()}


def _parse_history_timestamp(value: str) -> datetime | None:
    normalized = str(value).strip()
    if not normalized:
        return None
    try:
        return datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return None
