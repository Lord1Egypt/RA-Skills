"""Platform adapter registry for Founder Signal."""

from __future__ import annotations

from collections import deque
from typing import Any

from . import reddit, v2ex

_ADAPTERS = {
    "reddit": reddit,
    "v2ex": v2ex,
}


def get_adapter(platform: str):
    normalized = platform.strip().lower()
    if normalized not in _ADAPTERS:
        raise ValueError(f"Unsupported platform: {platform}")
    return _ADAPTERS[normalized]


def discover_all_candidates(
    config,
    *,
    excluded_source_ids: set[str] | None = None,
    opener=None,
    timeout_seconds: float = 20.0,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_source_ids = {item for item in (excluded_source_ids or set()) if item.strip()}
    platform_queues: list[tuple[str, deque[dict[str, Any]]]] = []
    for platform in sorted(config.platforms):
        adapter = get_adapter(platform)
        discovery_kwargs = {
            "excluded_source_ids": seen_source_ids,
            "timeout_seconds": timeout_seconds,
        }
        if opener is not None:
            discovery_kwargs["opener"] = opener
        platform_candidates = deque(adapter.discover_candidates(config, **discovery_kwargs))
        if platform_candidates:
            platform_queues.append((platform, platform_candidates))

    while platform_queues and len(candidates) < config.max_candidates:
        next_round: list[tuple[str, deque[dict[str, Any]]]] = []
        for platform, queue in platform_queues:
            if len(candidates) >= config.max_candidates:
                break
            if not queue:
                continue
            candidate = queue.popleft()
            source_id = str(candidate.get("source_id") or "").strip()
            if source_id and source_id in seen_source_ids:
                if queue:
                    next_round.append((platform, queue))
                continue
            if source_id:
                seen_source_ids.add(source_id)
            candidate = dict(candidate)
            candidate["candidate_id"] = f"cand-{len(candidates) + 1:03d}"
            candidates.append(candidate)
            if queue:
                next_round.append((platform, queue))
        platform_queues = next_round
    return candidates
