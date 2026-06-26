from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .fetch import execute_request, normalize_data, resolve_entry
from .schema import infer_schema, infer_shape_family, write_snapshot

SEED_CANDIDATES: dict[str, dict[str, list[str]]] = {
    "stable-coin": {"ticker": ["USDT", "USDC"]},
    "commodity": {"ticker": ["XAUT", "PAXG"]},
    "platforms": {"platform": ["tether-holdings", "ondo"]},
    "x-stock": {"ticker": ["NVDA", "TSLA"]},
}

DISCOVERY_KEYS: dict[str, list[str]] = {
    "market-overview": [
        "market-overview.asset-classes.list",
        "market-overview.network.list",
        "market-overview.platform.list",
    ],
    "platforms": [
        "platforms.dataset",
    ],
    "x-stock": [
        "x-stock.platform.list",
        "x-stock.underlying-stock.list",
    ],
}

FIELD_ALIASES = {
    "slug": "platform",
    "ticker": "ticker",
    "protocol": "platform",
    "name": "name",
}


def discover_sample_entities(asset_class: str, *, limit: int = 5, catalog_path=None) -> dict[str, Any]:
    candidates: dict[str, list[str]] = {key: values[:] for key, values in SEED_CANDIDATES.get(asset_class, {}).items()}
    sources: list[dict[str, Any]] = []

    for endpoint_key in DISCOVERY_KEYS.get(asset_class, []):
        entry = resolve_entry(endpoint_key=endpoint_key, catalog_path=catalog_path)
        request_context, response = execute_request(entry)
        normalized = normalize_data(response, infer_shape_family(response, entry.get("shape_family")))
        source = {"endpoint_key": endpoint_key, "request": request_context}
        sources.append(source)
        if isinstance(normalized, list):
            collect_candidates_from_list(candidates, normalized, limit)

    for name, values in list(candidates.items()):
        deduped: list[str] = []
        for value in values:
            if value in deduped:
                continue
            deduped.append(value)
            if len(deduped) == limit:
                break
        candidates[name] = deduped

    return {
        "asset_class": asset_class,
        "candidates": candidates,
        "sources": sources,
    }


def probe_endpoint_schema(
    *,
    endpoint_key: str | None = None,
    asset_class: str | None = None,
    family: str | None = None,
    metric: str | None = None,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    write_snapshot_file: bool = False,
    catalog_path=None,
) -> dict[str, Any]:
    entry = resolve_entry(
        endpoint_key=endpoint_key,
        asset_class=asset_class,
        family=family,
        metric=metric,
        catalog_path=catalog_path,
        path_params=path_params,
    )
    request_context, response = execute_request(entry, path_params=path_params, query=query)
    shape_family = infer_shape_family(response, entry.get("shape_family"))
    result = {
        "endpoint_key": entry["key"],
        "sample_request": request_context,
        "sample_response": response,
        "shape_family": shape_family,
        "inferred_schema": infer_schema(response.get("data")) if "data" in response else {"type": "absent"},
        "notes": build_probe_notes(entry, response, shape_family),
        "schema_source": "live_probe",
    }
    if write_snapshot_file:
        snapshot = build_snapshot(entry["key"], request_context, response, shape_family, result["inferred_schema"], result["notes"])
        output = write_snapshot(snapshot)
        result["snapshot_path"] = str(output)
    return result


def build_snapshot(
    endpoint_key: str,
    sample_request: dict[str, Any],
    sample_response: dict[str, Any],
    shape_family: str,
    inferred_schema: dict[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "endpoint_key": endpoint_key,
        "inferred_schema": inferred_schema,
        "notes": notes,
        "sample_request": sample_request,
        "sample_response_excerpt": summarize_response(sample_response),
        "shape_family": shape_family,
        "snapshot_path": f"shared/coinfound_rwa/data/schema_snapshots/{endpoint_key.replace('.', '__')}.json",
    }


def summarize_response(response: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "code": response.get("code"),
        "message": response.get("message"),
    }
    if "data" not in response:
        return summary
    data = response["data"]
    if isinstance(data, list):
        summary["data_preview"] = data[:2]
        summary["data_length"] = len(data)
        return summary
    if isinstance(data, dict):
        summary["data_keys"] = sorted(data.keys())
        if "list" in data and isinstance(data["list"], list):
            summary["list_preview"] = data["list"][:1]
            summary["list_length"] = len(data["list"])
        return summary
    summary["data_preview"] = data
    return summary


def build_probe_notes(entry: dict[str, Any], response: dict[str, Any], shape_family: str) -> list[str]:
    notes = list(entry.get("notes", []))
    if shape_family != entry.get("shape_family"):
        notes.append(f"Shape changed from catalog={entry.get('shape_family')} to live={shape_family}.")
    if response.get("code") == 0 and "data" not in response:
        notes.append("Live response returned code=0 without a data field.")
    return notes


def collect_candidates_from_list(candidates: dict[str, list[str]], items: list[Any], limit: int) -> None:
    for item in items:
        if not isinstance(item, dict):
            continue
        for field_name, candidate_key in FIELD_ALIASES.items():
            value = item.get(field_name)
            if not isinstance(value, str) or not value:
                continue
            bucket = candidates.setdefault(candidate_key, [])
            if value not in bucket:
                bucket.append(value)
            if len(bucket) >= limit:
                continue
