from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path


_PROVIDER_CACHE_VERSION = 3
_PRICE_SENSITIVE_MAX_CACHE_AGE_HOURS = 24.0
_STATEMENT_MAX_CACHE_AGE_HOURS = 168.0


def _has_core_inputs(payload: dict) -> bool:
    fundamentals = payload.get("fundamentals") or {}
    assumptions = payload.get("assumptions") or {}
    has_anchor = ("fcff_anchor" in fundamentals) or ("ebit" in fundamentals)
    has_wacc_inputs = any(
        key in assumptions
        for key in (
            "risk_free_rate",
            "equity_risk_premium",
            "beta",
            "pre_tax_cost_of_debt",
        )
    )
    return bool(has_anchor and has_wacc_inputs)


def _normalize_bool(value, *, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return bool(value)


def _default_cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME")
    if base:
        return Path(base).expanduser() / "fp-dcf"
    return Path.home() / ".cache" / "fp-dcf"


def _resolve_cache_dir(cache_dir: str | os.PathLike[str] | None) -> Path:
    if cache_dir is None:
        return _default_cache_dir()
    return Path(cache_dir).expanduser()


def _provider_cache_key(provider_name: str, payload: dict) -> dict[str, str | int]:
    return {
        "cache_version": _PROVIDER_CACHE_VERSION,
        "provider": provider_name,
        "ticker": str(payload.get("ticker") or "").strip().upper(),
        "market": str(payload.get("market") or "US").strip().upper(),
        "statement_frequency": str(payload.get("statement_frequency") or "A").strip().upper(),
    }


def _provider_cache_path(
    provider_name: str,
    payload: dict,
    cache_dir: str | os.PathLike[str] | None,
) -> Path:
    cache_root = _resolve_cache_dir(cache_dir)
    cache_key = _provider_cache_key(provider_name, payload)
    digest = hashlib.sha256(
        json.dumps(cache_key, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return cache_root / "providers" / provider_name / f"{digest}.json"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds")


def _parse_datetime(value) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _load_provider_cache(cache_path: Path) -> dict | None:
    if not cache_path.exists():
        return None
    try:
        raw = cache_path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except (OSError, ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    snapshot = payload.get("snapshot")
    if not isinstance(snapshot, dict):
        return None
    return {
        "snapshot": snapshot,
        "cache_created_at": payload.get("cache_created_at"),
    }


def _load_provider_snapshot(cache_path: Path) -> dict | None:
    cache = _load_provider_cache(cache_path)
    return cache["snapshot"] if cache is not None else None


def _write_provider_snapshot(cache_path: Path, snapshot: dict) -> str:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_created_at = _to_utc_iso(_utc_now())
    envelope = {
        "cache_version": _PROVIDER_CACHE_VERSION,
        "cache_created_at": cache_created_at,
        "snapshot": snapshot,
    }
    text = json.dumps(envelope, sort_keys=True, ensure_ascii=False)
    tmp_path = cache_path.with_suffix(f"{cache_path.suffix}.tmp")
    tmp_path.write_text(text + "\n", encoding="utf-8")
    tmp_path.replace(cache_path)
    return cache_created_at


def _snapshot_as_of(snapshot: dict, cache_created_at: str | None) -> str | None:
    if snapshot.get("snapshot_as_of"):
        return str(snapshot["snapshot_as_of"])
    fundamentals = snapshot.get("fundamentals") or {}
    if isinstance(fundamentals, dict) and fundamentals.get("last_report_period"):
        return str(fundamentals["last_report_period"])
    parsed_created_at = _parse_datetime(cache_created_at)
    if parsed_created_at is not None:
        return parsed_created_at.date().isoformat()
    return None


def _freshness_max_cache_age_hours(payload: dict, snapshot: dict) -> float:
    normalization = payload.get("normalization") or {}
    if not isinstance(normalization, dict):
        normalization = {}
    raw_override = normalization.get("max_cache_age_hours")
    if raw_override is None:
        raw_override = normalization.get("freshness_max_cache_age_hours")
    try:
        override = float(raw_override)
    except (TypeError, ValueError):
        override = None
    if override is not None and override > 0:
        return override

    fundamentals = snapshot.get("fundamentals") or {}
    assumptions = snapshot.get("assumptions") or {}
    if not isinstance(fundamentals, dict):
        fundamentals = {}
    if not isinstance(assumptions, dict):
        assumptions = {}

    has_price_sensitive_inputs = any(
        fundamentals.get(key) not in (None, "")
        for key in ("market_price", "market_cap", "shares_out")
    )
    capital_structure_source = str(assumptions.get("capital_structure_source") or "")
    if has_price_sensitive_inputs or "market_value" in capital_structure_source:
        return _PRICE_SENSITIVE_MAX_CACHE_AGE_HOURS
    return _STATEMENT_MAX_CACHE_AGE_HOURS


def _provider_data_freshness(
    provider_name: str,
    snapshot: dict | None,
    *,
    cache_created_at: str | None,
    now: datetime | None = None,
    max_cache_age_hours: float | None = None,
) -> dict:
    now = (now or _utc_now()).astimezone(timezone.utc)
    if not isinstance(snapshot, dict):
        return {
            "provider": provider_name,
            "snapshot_as_of": None,
            "cache_created_at": cache_created_at,
            "cache_age_hours": None,
            "freshness_class": "missing",
            "requires_refresh": True,
        }

    parsed_created_at = _parse_datetime(cache_created_at)
    if parsed_created_at is None:
        return {
            "provider": provider_name,
            "snapshot_as_of": _snapshot_as_of(snapshot, cache_created_at),
            "cache_created_at": cache_created_at,
            "cache_age_hours": None,
            "freshness_class": "unknown",
            "requires_refresh": True,
        }

    age_hours = max((now - parsed_created_at).total_seconds() / 3600.0, 0.0)
    freshness_class = "fresh"
    if max_cache_age_hours is not None and age_hours > max_cache_age_hours:
        freshness_class = "stale"
    return {
        "provider": provider_name,
        "snapshot_as_of": _snapshot_as_of(snapshot, cache_created_at),
        "cache_created_at": _to_utc_iso(parsed_created_at),
        "cache_age_hours": round(age_hours, 3),
        "freshness_class": freshness_class,
        "requires_refresh": freshness_class != "fresh",
    }


def _attach_data_freshness(
    payload: dict,
    provider_name: str,
    snapshot: dict | None,
    *,
    cache_created_at: str | None,
) -> None:
    max_cache_age_hours = (
        _freshness_max_cache_age_hours(payload, snapshot) if isinstance(snapshot, dict) else None
    )
    freshness = _provider_data_freshness(
        provider_name,
        snapshot,
        cache_created_at=cache_created_at,
        max_cache_age_hours=max_cache_age_hours,
    )
    payload["_data_freshness"] = freshness
    freshness_class = freshness["freshness_class"]
    _append_prefill_diagnostic(payload, f"provider_data_freshness:{freshness_class}")
    if freshness_class == "stale":
        _append_prefill_warning(payload, "provider_data_stale")
    elif freshness_class == "unknown":
        _append_prefill_warning(payload, "provider_data_freshness_unknown")
    elif freshness_class == "missing":
        _append_prefill_warning(payload, "provider_data_missing")


def _append_prefill_diagnostic(payload: dict, diagnostic: str) -> None:
    diagnostics = list(payload.get("_prefill_diagnostics", []))
    if diagnostic not in diagnostics:
        diagnostics.append(diagnostic)
    payload["_prefill_diagnostics"] = diagnostics


def _append_prefill_warning(payload: dict, warning: str) -> None:
    warnings = list(payload.get("_prefill_warnings", []))
    if warning not in warnings:
        warnings.append(warning)
    payload["_prefill_warnings"] = warnings


def _is_cn_fallback_candidate(payload: dict) -> bool:
    market = str(payload.get("market") or "").strip().upper()
    ticker = str(payload.get("ticker") or "").strip().upper()
    if market == "CN":
        return True
    return ticker.endswith((".SS", ".SH", ".SZ", ".BJ"))


def _provider_handlers(provider_name: str):
    if provider_name == "yahoo":
        from .providers.yahoo import enrich_payload_from_yahoo, fetch_yahoo_snapshot

        return fetch_yahoo_snapshot, enrich_payload_from_yahoo

    if provider_name == "akshare_baostock":
        from .providers.akshare_baostock import (
            enrich_payload_from_akshare_baostock,
            fetch_akshare_baostock_snapshot,
        )

        return fetch_akshare_baostock_snapshot, enrich_payload_from_akshare_baostock

    raise ValueError(f"Unsupported provider: {provider_name}")


def _normalize_with_provider(
    provider_name: str,
    payload: dict,
    *,
    cache_dir: str | os.PathLike[str] | None = None,
    force_refresh: bool | None = None,
) -> dict:
    normalization = payload.get("normalization") or {}
    if not isinstance(normalization, dict):
        normalization = {}

    fetch_snapshot, enrich_payload = _provider_handlers(provider_name)

    use_cache = _normalize_bool(normalization.get("use_cache"), default=True)
    effective_cache_dir = cache_dir or normalization.get("cache_dir")
    should_refresh = (
        force_refresh
        if force_refresh is not None
        else _normalize_bool(normalization.get("refresh"), default=False)
    )

    snapshot = None
    cache_created_at = None
    cache_status = "bypass"
    cache_path = _provider_cache_path(provider_name, payload, effective_cache_dir)
    if use_cache and not should_refresh:
        cached = _load_provider_cache(cache_path)
        if cached is not None:
            snapshot = cached["snapshot"]
            cache_created_at = cached.get("cache_created_at")
            cache_status = "hit"

    if snapshot is None:
        snapshot = fetch_snapshot(
            payload.get("ticker"),
            market=payload.get("market", "US"),
            statement_frequency=payload.get("statement_frequency") or "A",
        )
        cache_created_at = _to_utc_iso(_utc_now())
        if use_cache:
            cache_created_at = _write_provider_snapshot(cache_path, snapshot)
            cache_status = "refresh" if should_refresh else "miss"

    normalized = enrich_payload(payload, snapshot=snapshot)
    _attach_data_freshness(
        normalized,
        provider_name,
        snapshot,
        cache_created_at=cache_created_at,
    )
    if use_cache:
        _append_prefill_diagnostic(normalized, f"provider_cache_{cache_status}:{provider_name}")
    elif should_refresh:
        _append_prefill_diagnostic(
            normalized,
            f"provider_cache_disabled_explicit_refresh:{provider_name}",
        )
    return normalized


def normalize_payload(
    payload: dict,
    provider_override: str | None = None,
    *,
    cache_dir: str | os.PathLike[str] | None = None,
    force_refresh: bool | None = None,
) -> dict:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    out = deepcopy(payload)
    normalization = out.get("normalization") or {}
    if not isinstance(normalization, dict):
        normalization = {}
    provider = provider_override
    if provider is None:
        provider = out.get("provider")
    if provider is None:
        provider = normalization.get("provider")

    if provider is None and not _has_core_inputs(out):
        provider = "yahoo"

    if provider is None:
        return out

    provider_name = str(provider).strip().lower()
    try:
        return _normalize_with_provider(
            provider_name,
            out,
            cache_dir=cache_dir,
            force_refresh=force_refresh,
        )
    except Exception as exc:
        if provider_name != "yahoo" or not _is_cn_fallback_candidate(out):
            raise

        try:
            normalized = _normalize_with_provider(
                "akshare_baostock",
                out,
                cache_dir=cache_dir,
                force_refresh=force_refresh,
            )
        except Exception as fallback_exc:
            raise RuntimeError(
                f"Yahoo normalization failed ({exc}) and akshare_baostock fallback failed ({fallback_exc})"
            ) from fallback_exc

        _append_prefill_diagnostic(normalized, "provider_fallback:yahoo->akshare_baostock")
        _append_prefill_warning(normalized, "yahoo_unavailable_used_akshare_baostock_fallback")
        return normalized
