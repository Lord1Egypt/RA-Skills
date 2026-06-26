"""CLI entrypoint for subprocess usage: python -m free_search."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import configure_logging, get_quota_status, reset_quota, search, task_search, get_real_quota
from .discovery import SourceDiscovery
from .health import HealthTracker
from .router import SearchRouter, SearchRouterError
from .storage import persist_search_payload, run_gc


def _normalize_compat_tokens(argv: list[str]) -> list[str]:
    if len(argv) >= 3 and argv[0].lower() == "brave" and argv[1].lower() == "search":
        return argv[2:]
    if len(argv) >= 2 and argv[0].lower() == "search":
        return argv[1:]
    return argv


_ENV_KEY_MAP = {
    "brave": ["BRAVE_API_KEY"],
    "exa": ["EXA_API_KEY"],
    "tavily": ["TAVILY_API_KEY"],
    "serper": ["SERPER_API_KEY"],
    "searchapi": ["SEARCHAPI_API_KEY"],
    "google_cse": ["GOOGLE_API_KEY", "GOOGLE_CX"],
    "baidu": ["BAIDU_API_KEY"],
    "mojeek": ["MOJEEK_API_KEY"],
}

_FREE_PROVIDERS = {"duckduckgo", "bing_html", "wikipedia", "duckduckgo_instant"}


def _run_doctor(*, config_path: str | None = None) -> dict[str, Any]:
    """Run system diagnostics: config, providers, storage, health."""
    import os
    from .storage import _memory_root

    checks: list[dict[str, Any]] = []

    # 1. Config file check
    try:
        router = SearchRouter(config_path=config_path)
        checks.append({"check": "config_load", "status": "ok", "providers_configured": len(router.order)})
    except Exception as exc:
        checks.append({"check": "config_load", "status": "error", "detail": str(exc)})
        return {"checks": checks, "overall": "error"}

    # 2. Provider credential check
    provider_status: list[dict[str, Any]] = []
    for name in router.order:
        provider = router.providers.get(name)
        if not provider:
            provider_status.append({"provider": name, "status": "not_loaded"})
            continue
        if not provider.is_enabled():
            provider_status.append({"provider": name, "status": "disabled"})
            continue

        # Check if API key is set for key-required providers
        if name in _ENV_KEY_MAP:
            missing = [k for k in _ENV_KEY_MAP[name] if not os.environ.get(k)]
            if missing:
                provider_status.append({"provider": name, "status": "missing_keys", "keys": missing})
                continue

        provider_status.append({"provider": name, "status": "ready"})

    checks.append({"check": "providers", "status": "ok", "providers": provider_status})

    # 3. Storage directory check
    try:
        mem_root = _memory_root()
        mem_root.mkdir(parents=True, exist_ok=True)
        writable = os.access(str(mem_root), os.W_OK)
        checks.append({"check": "storage", "status": "ok" if writable else "warning",
                       "path": str(mem_root), "writable": writable})
    except Exception as exc:
        checks.append({"check": "storage", "status": "error", "detail": str(exc)})

    # 4. Health data check
    try:
        tracker = HealthTracker()
        summary = tracker.get_summary(window_hours=24)
        checks.append({"check": "health_data", "status": "ok",
                       "records_24h": summary.get("total_records", 0)})
    except Exception as exc:
        checks.append({"check": "health_data", "status": "error", "detail": str(exc)})

    # 5. Quota check
    try:
        quota = get_quota_status(config_path=config_path)
        high_usage = [
            p["provider"] for p in quota.get("providers", [])
            if isinstance(p.get("percentage_used"), (int, float)) and p["percentage_used"] >= 80
        ]
        checks.append({"check": "quota", "status": "warning" if high_usage else "ok",
                       "high_usage_providers": high_usage})
    except Exception as exc:
        checks.append({"check": "quota", "status": "error", "detail": str(exc)})

    # Overall status
    statuses = [c["status"] for c in checks]
    if "error" in statuses:
        overall = "error"
    elif "warning" in statuses:
        overall = "warning"
    else:
        overall = "ok"

    ready_count = sum(1 for p in provider_status if p["status"] == "ready")

    return {
        "overall": overall,
        "ready_providers": ready_count,
        "total_providers": len(provider_status),
        "checks": checks,
    }


def _run_setup(*, config_path: str | None = None) -> dict[str, Any]:
    """Show setup status and configuration recommendations."""
    import os

    providers_info: list[dict[str, Any]] = []

    # Free providers (always available)
    for name in sorted(_FREE_PROVIDERS):
        providers_info.append({
            "provider": name,
            "type": "free",
            "status": "ready",
            "action": "No setup required",
        })

    # API-key providers
    for name, keys in sorted(_ENV_KEY_MAP.items()):
        set_keys = [k for k in keys if os.environ.get(k)]
        missing_keys = [k for k in keys if not os.environ.get(k)]

        if not missing_keys:
            providers_info.append({
                "provider": name,
                "type": "api_key",
                "status": "ready",
                "action": "Configured and ready",
            })
        else:
            providers_info.append({
                "provider": name,
                "type": "api_key",
                "status": "needs_setup",
                "missing_keys": missing_keys,
                "action": f"Set environment variable(s): {', '.join(missing_keys)}",
            })

    ready = sum(1 for p in providers_info if p["status"] == "ready")
    needs_setup = sum(1 for p in providers_info if p["status"] == "needs_setup")

    recommendations: list[str] = []
    if needs_setup > 0:
        recommendations.append(f"{needs_setup} providers need API keys — set the environment variables to enable them")
    if ready < 4:
        recommendations.append("Consider setting up more API-key providers for better failover coverage")
    recommendations.append("Run 'python -m free_search doctor' for a full system diagnostic")
    recommendations.append("Run 'python -m free_search discover' to find additional search sources")

    return {
        "ready_providers": ready,
        "needs_setup": needs_setup,
        "providers": providers_info,
        "recommendations": recommendations,
    }


def main(argv: list[str] | None = None) -> int:
    raw_args = list(argv) if argv is not None else sys.argv[1:]
    normalized_args = _normalize_compat_tokens(raw_args)

    if normalized_args and normalized_args[0].lower() in ("status", "remaining", "quota"):
        parser = argparse.ArgumentParser(description="Show or reset provider quota usage")
        parser.add_argument("--config", default=None, help="Path to providers.yaml")
        parser.add_argument("--log-level", default="INFO")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        parser.add_argument("--reset", action="store_true", help="Reset quota counters before showing status")
        parser.add_argument("--real", action="store_true", help="Fetch real provider quota when supported")
        parser.add_argument("--probe", action="store_true", help="Allow probe requests for providers without quota endpoints (may consume quota)")
        args = parser.parse_args(normalized_args[1:])

        configure_logging(args.log_level)
        try:
            payload = (
                reset_quota(config_path=args.config)
                if args.reset
                else get_quota_status(config_path=args.config)
            )
        except Exception as exc:  # pragma: no cover - defensive for CLI consumers
            print(json.dumps({"error": f"unexpected_error: {exc}"}, ensure_ascii=False), file=sys.stderr)
            return 1

        # Add convenience totals for quick inspection
        totals = {"total_remaining": 0, "total_daily_quota": 0}
        for p in payload.get("providers", []):
            dq = p.get("daily_quota")
            rem = p.get("remaining")
            if isinstance(dq, int):
                totals["total_daily_quota"] += dq
            if isinstance(rem, int):
                totals["total_remaining"] += rem
        payload["totals"] = totals

        if args.real:
            real = get_real_quota(config_path=args.config, probe_brave=bool(args.probe))
            payload["real_quota"] = real

        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    if normalized_args and normalized_args[0].lower() == "gc":
        parser = argparse.ArgumentParser(description="Clean old search cache/report files")
        parser.add_argument("--cache-days", type=int, default=14)
        parser.add_argument("--report-days", type=int, default=None)
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        args = parser.parse_args(normalized_args[1:])

        payload = run_gc(cache_days=args.cache_days, report_days=args.report_days)
        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    if normalized_args and normalized_args[0].lower() == "task":
        parser = argparse.ArgumentParser(description="Run task-level multi-query search")
        parser.add_argument("task", nargs="+", help="Task or goal statement")
        parser.add_argument("--max-results", type=int, default=5)
        parser.add_argument("--max-queries", type=int, default=6)
        parser.add_argument("--max-merged-results", type=int, default=None)
        parser.add_argument("--workers", type=int, default=1)
        parser.add_argument("--config", default=None, help="Path to providers.yaml")
        parser.add_argument("--log-level", default="INFO")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        args = parser.parse_args(normalized_args[1:])
        task = " ".join(args.task).strip()

        # Preset prefixes for interaction convenience:
        # - @dual: workers=2
        # - @deep: workers=3 and max_queries>=8 (depth first, not brute force concurrency)
        effective_workers = args.workers
        effective_max_queries = args.max_queries
        if task.startswith("@dual"):
            task = task[len("@dual"):].strip()
            effective_workers = 2
        elif task.startswith("@deep"):
            task = task[len("@deep"):].strip()
            effective_workers = 3
            effective_max_queries = max(effective_max_queries, 8)

        # Quota-aware degradation: when quota usage is high, reduce concurrency.
        try:
            status = get_quota_status(config_path=args.config)
            max_pct = 0.0
            for p in status.get("providers", []):
                pct = p.get("percentage_used")
                if isinstance(pct, (int, float)):
                    max_pct = max(max_pct, float(pct))
            if max_pct >= 80.0 and effective_workers > 2:
                effective_workers = 2
        except Exception:
            pass

        configure_logging(args.log_level)
        try:
            payload = task_search(
                task,
                max_results_per_query=args.max_results,
                max_queries=effective_max_queries,
                max_merged_results=args.max_merged_results,
                max_workers=effective_workers,
                config_path=args.config,
            )
        except SearchRouterError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
            return 2
        except Exception as exc:  # pragma: no cover - defensive for CLI consumers
            print(json.dumps({"error": f"unexpected_error: {exc}"}, ensure_ascii=False), file=sys.stderr)
            return 1

        storage_info = persist_search_payload(query=task, payload=payload, mode="task")
        payload.setdefault("meta", {})["storage"] = storage_info

        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    # ── health command ──────────────────────────────────────────────────────
    if normalized_args and normalized_args[0].lower() == "health":
        parser = argparse.ArgumentParser(description="Show provider health dashboard")
        parser.add_argument("--window", type=int, default=72, help="Analysis window in hours")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        parser.add_argument("--compact-health", action="store_true", help="Compact old health records")
        args = parser.parse_args(normalized_args[1:])

        tracker = HealthTracker()

        if args.compact_health:
            removed = tracker.compact(keep_hours=args.window)
            print(json.dumps({"compacted": True, "records_removed": removed}, indent=2))
            return 0

        payload = tracker.get_summary(window_hours=args.window)
        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    # ── discover command ─────────────────────────────────────────────────────
    if normalized_args and normalized_args[0].lower() == "discover":
        parser = argparse.ArgumentParser(description="Discover and probe search sources")
        parser.add_argument("--config", default=None, help="Path to providers.yaml")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        parser.add_argument("--log-level", default="INFO")
        args = parser.parse_args(normalized_args[1:])

        configure_logging(args.log_level)
        discovery = SourceDiscovery(config_path=args.config)
        payload = discovery.run_discovery()

        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    # ── doctor command ───────────────────────────────────────────────────────
    if normalized_args and normalized_args[0].lower() == "doctor":
        parser = argparse.ArgumentParser(description="Run system diagnostics")
        parser.add_argument("--config", default=None, help="Path to providers.yaml")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        parser.add_argument("--log-level", default="WARNING")
        args = parser.parse_args(normalized_args[1:])

        configure_logging(args.log_level)
        diagnostics = _run_doctor(config_path=args.config)

        indent = None if args.compact else 2
        print(json.dumps(diagnostics, ensure_ascii=False, indent=indent))
        return 0

    # ── setup command ────────────────────────────────────────────────────────
    if normalized_args and normalized_args[0].lower() == "setup":
        parser = argparse.ArgumentParser(description="Show setup status and recommendations")
        parser.add_argument("--config", default=None, help="Path to providers.yaml")
        parser.add_argument("--compact", action="store_true", help="Print compact JSON")
        args = parser.parse_args(normalized_args[1:])

        payload = _run_setup(config_path=args.config)

        indent = None if args.compact else 2
        print(json.dumps(payload, ensure_ascii=False, indent=indent))
        return 0

    # ── default: search ──────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="Run failover web search")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--config", default=None, help="Path to providers.yaml")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args(normalized_args)
    query = " ".join(args.query).strip()

    configure_logging(args.log_level)
    try:
        payload = search(query, max_results=args.max_results, config_path=args.config)
    except SearchRouterError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive for CLI consumers
        print(json.dumps({"error": f"unexpected_error: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1

    storage_info = persist_search_payload(query=query, payload=payload, mode="search")
    payload.setdefault("meta", {})["storage"] = storage_info

    indent = None if args.compact else 2
    print(json.dumps(payload, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
