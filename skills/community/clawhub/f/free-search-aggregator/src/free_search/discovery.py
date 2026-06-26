"""Source discovery: probe providers, scan candidate sources, find new search engines."""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from .health import HealthTracker
from .router import SearchRouter
from .storage import _memory_root

logger = logging.getLogger(__name__)

_PROBE_QUERY = "test"
_PROBE_TIMEOUT = 8
_PROBE_MAX_RESULTS = 3
_MAX_ACCEPTABLE_LATENCY_MS = 5000

# ── Candidate Search Sources ────────────────────────────────────────────────
# Free search engines / APIs that are not yet integrated as full providers
# but can be probed for availability and quality.

CANDIDATE_SOURCES: list[dict[str, Any]] = [
    {
        "name": "marginalia",
        "probe_url": "https://api.marginalia.nu/{subpath}",
        "search_url": "https://search.marginalia.nu/search?query={query}&count={count}&format=json",
        "type": "json_api",
        "description": "Independent index focused on non-commercial/small websites",
        "result_path": "results",
        "title_key": "title",
        "url_key": "url",
        "snippet_key": "description",
    },
    {
        "name": "wiby",
        "search_url": "https://wiby.me/json/?q={query}",
        "type": "json_api",
        "description": "Minimalist search engine for classic/Web 1.0 content",
        "result_path": None,  # root is array
        "title_key": "Title",
        "url_key": "URL",
        "snippet_key": "Snippet",
    },
    {
        "name": "curlie",
        "search_url": "https://curlie.org/search?q={query}&format=json",
        "type": "json_api",
        "description": "DMOZ successor, human-curated web directory",
        "result_path": "results",
        "title_key": "title",
        "url_key": "url",
        "snippet_key": "description",
    },
    # ── SearXNG Public Instances ──────────────────────────────────────────
    {
        "name": "searxng_paulgo",
        "search_url": "https://paulgo.io/search?q={query}&format=json",
        "type": "searxng",
        "description": "SearXNG public instance (paulgo.io)",
    },
    {
        "name": "searxng_priv",
        "search_url": "https://priv.au/search?q={query}&format=json",
        "type": "searxng",
        "description": "SearXNG public instance (priv.au)",
    },
    {
        "name": "searxng_northboot",
        "search_url": "https://search.bus-hit.me/search?q={query}&format=json",
        "type": "searxng",
        "description": "SearXNG public instance (bus-hit.me)",
    },
    {
        "name": "searxng_ononoki",
        "search_url": "https://search.ononoki.org/search?q={query}&format=json",
        "type": "searxng",
        "description": "SearXNG public instance (ononoki.org)",
    },
]


def _discovery_storage_path() -> Path:
    return _memory_root() / "provider-discovery" / "discovery.jsonl"


def _probe_existing_provider(
    router: SearchRouter,
    name: str,
) -> dict[str, Any]:
    """Probe a single configured provider with a test query."""
    provider = router.providers.get(name)
    if not provider:
        return {
            "provider": name,
            "status": "not_configured",
            "latency_ms": 0,
            "result_count": 0,
        }
    if not provider.is_enabled():
        return {
            "provider": name,
            "status": "disabled",
            "latency_ms": 0,
            "result_count": 0,
        }

    started = time.perf_counter()
    try:
        items = provider.search(_PROBE_QUERY, max_results=_PROBE_MAX_RESULTS)
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "provider": name,
            "status": "ok" if items else "empty",
            "latency_ms": elapsed_ms,
            "result_count": len(items) if items else 0,
        }
    except Exception as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "provider": name,
            "status": "error",
            "latency_ms": elapsed_ms,
            "result_count": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _probe_candidate_source(candidate: dict[str, Any]) -> dict[str, Any]:
    """Probe a candidate search source for availability and quality."""
    name = candidate["name"]
    search_url = candidate.get("search_url", "")
    source_type = candidate.get("type", "json_api")

    if not search_url:
        return {
            "name": name,
            "status": "no_url",
            "latency_ms": 0,
            "result_count": 0,
            "quality_score": 0.0,
        }

    url = search_url.replace("{query}", _PROBE_QUERY).replace("{count}", "3")

    started = time.perf_counter()
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; FreeSearchAggregator/1.0)",
            "Accept": "application/json",
        }
        resp = requests.get(url, headers=headers, timeout=_PROBE_TIMEOUT)
        elapsed_ms = int((time.perf_counter() - started) * 1000)

        if resp.status_code != 200:
            return {
                "name": name,
                "status": "http_error",
                "http_status": resp.status_code,
                "latency_ms": elapsed_ms,
                "result_count": 0,
                "quality_score": 0.0,
            }

        # Try to parse response
        result_count = 0
        quality_score = 0.0

        try:
            data = resp.json()

            if source_type == "searxng":
                results = data.get("results", []) if isinstance(data, dict) else []
                result_count = len(results)
            elif source_type == "json_api":
                result_path = candidate.get("result_path")
                if result_path is None:
                    # Root is array
                    results = data if isinstance(data, list) else []
                else:
                    results = data.get(result_path, []) if isinstance(data, dict) else []
                result_count = len(results) if isinstance(results, list) else 0
            else:
                result_count = 0

            # Quality scoring: result count + reasonable latency
            if result_count > 0:
                count_score = min(1.0, result_count / 5.0)
                latency_score = max(0.0, 1.0 - elapsed_ms / _MAX_ACCEPTABLE_LATENCY_MS)
                quality_score = round(count_score * 0.6 + latency_score * 0.4, 4)

        except (ValueError, KeyError):
            return {
                "name": name,
                "status": "parse_error",
                "latency_ms": elapsed_ms,
                "result_count": 0,
                "quality_score": 0.0,
            }

        status = "available" if result_count > 0 else "empty"
        return {
            "name": name,
            "type": source_type,
            "status": status,
            "latency_ms": elapsed_ms,
            "result_count": result_count,
            "quality_score": quality_score,
            "description": candidate.get("description", ""),
        }

    except requests.exceptions.Timeout:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "name": name,
            "status": "timeout",
            "latency_ms": elapsed_ms,
            "result_count": 0,
            "quality_score": 0.0,
        }
    except requests.exceptions.RequestException as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "name": name,
            "status": "network_error",
            "latency_ms": elapsed_ms,
            "result_count": 0,
            "quality_score": 0.0,
            "error": str(exc),
        }


class SourceDiscovery:
    """Discovers and probes search sources — both configured and candidate."""

    def __init__(self, config_path: str | None = None) -> None:
        self.config_path = config_path
        self.storage_path = _discovery_storage_path()
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def probe_all(self) -> dict[str, Any]:
        """Probe all configured providers in parallel."""
        router = SearchRouter(config_path=self.config_path)
        results: list[dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=3) as pool:
            futs = {
                pool.submit(_probe_existing_provider, router, name): name
                for name in router.order
            }
            for fut in as_completed(futs):
                results.append(fut.result())

        # Sort by status: ok first, then by latency
        results.sort(key=lambda x: (0 if x["status"] == "ok" else 1, x.get("latency_ms", 9999)))
        return {
            "configured_providers": results,
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }

    def scan_candidate_sources(self) -> list[dict[str, Any]]:
        """Probe all candidate sources in parallel."""
        results: list[dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=4) as pool:
            futs = {
                pool.submit(_probe_candidate_source, src): src["name"]
                for src in CANDIDATE_SOURCES
            }
            for fut in as_completed(futs):
                results.append(fut.result())

        # Sort: available first, then by quality score descending
        results.sort(key=lambda x: (
            0 if x["status"] == "available" else 1,
            -x.get("quality_score", 0),
        ))
        return results

    def run_discovery(self) -> dict[str, Any]:
        """Full discovery cycle: probe existing + scan candidates + generate recommendations."""
        logger.info("Starting source discovery...")

        # Phase 1: Probe existing providers
        existing = self.probe_all()

        # Phase 2: Scan candidate sources
        candidates = self.scan_candidate_sources()

        # Phase 3: Sync to health tracker
        health = HealthTracker()
        for p in existing.get("configured_providers", []):
            name = p.get("provider", "")
            if not name:
                continue
            health.record(
                name,
                success=p["status"] == "ok",
                latency_ms=p.get("latency_ms", 0),
                error_type=p.get("error", None) if p["status"] not in ("ok", "disabled", "not_configured") else None,
            )

        # Phase 4: Generate recommendations
        recommendations: list[str] = []
        for c in candidates:
            if c["status"] == "available" and c.get("quality_score", 0) >= 0.3:
                desc = c.get("description", c["name"])
                recommendations.append(
                    f"{c['name']} (quality={c['quality_score']:.2f}, latency={c['latency_ms']}ms): {desc}"
                )

        # Identify degraded existing providers
        degraded: list[str] = []
        for p in existing.get("configured_providers", []):
            if p["status"] in ("error", "empty") and p["provider"] not in ("searxng", "yacy"):
                degraded.append(f"{p['provider']}: {p.get('error', p['status'])}")

        result = {
            "existing_providers": existing.get("configured_providers", []),
            "candidate_results": candidates,
            "recommendations": recommendations,
            "degraded_providers": degraded,
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }

        # Persist discovery result
        self._persist(result)

        return result

    def _persist(self, result: dict[str, Any]) -> None:
        """Append discovery result to storage."""
        try:
            with self.storage_path.open("a", encoding="utf-8") as f:
                entry = {
                    "ts": result.get("timestamp_utc", datetime.now(UTC).isoformat()),
                    "existing_ok": sum(
                        1 for p in result.get("existing_providers", [])
                        if p.get("status") == "ok"
                    ),
                    "existing_total": len(result.get("existing_providers", [])),
                    "candidates_available": sum(
                        1 for c in result.get("candidate_results", [])
                        if c.get("status") == "available"
                    ),
                    "candidates_total": len(result.get("candidate_results", [])),
                    "recommendations_count": len(result.get("recommendations", [])),
                    "degraded_count": len(result.get("degraded_providers", [])),
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            logger.warning("Failed to persist discovery results", exc_info=True)
