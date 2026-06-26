from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .catalog import BASE_URL, DEFAULT_CATALOG_PATH, load_catalog
from .formatter import format_display_data
from .schema import infer_shape_family, load_snapshot


def resolve_entry(
    *,
    endpoint_key: str | None = None,
    asset_class: str | None = None,
    family: str | None = None,
    metric: str | None = None,
    catalog_path=None,
    path_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    catalog = load_catalog(catalog_path or DEFAULT_CATALOG_PATH)
    if endpoint_key:
        for entry in catalog:
            if entry["key"] == endpoint_key:
                return entry
        raise LookupError(f"Unknown endpoint key: {endpoint_key}")

    if not asset_class or not family:
        raise LookupError("asset_class and family are required when endpoint_key is not provided.")

    candidates = [entry for entry in catalog if entry["asset_class"] == asset_class and entry["family"] == family]
    if metric is not None:
        candidates = [entry for entry in candidates if entry["metric"] == metric]

    if not candidates:
        raise LookupError(f"No endpoint matched asset_class={asset_class}, family={family}, metric={metric}.")

    if len(candidates) == 1:
        return candidates[0]

    required_path_params = len(path_params or {})
    same_arity = [entry for entry in candidates if len(entry["path_params"]) == required_path_params]
    if len(same_arity) == 1:
        return same_arity[0]
    if same_arity:
        candidates = same_arity

    candidates.sort(key=lambda item: (item["key"].count("detail"), len(item["path_params"]), item["key"]))
    return candidates[0]


def ensure_supported(entry: dict[str, Any]) -> None:
    if entry.get("unsupported_by_design"):
        raise ValueError(
            f"Endpoint {entry['key']} is excluded by design from the read skill. "
            "Use non-report data endpoints instead."
        )


def build_request_context(
    entry: dict[str, Any],
    *,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    base_url: str = BASE_URL,
) -> dict[str, Any]:
    ensure_supported(entry)
    resolved_path = fill_path_template(entry["path_template"], path_params or {})
    query_string = encode_query(query or {})
    url = f"{base_url}{resolved_path}"
    if query_string:
        url = f"{url}?{query_string}"
    return {
        "method": entry["method"],
        "path": resolved_path,
        "path_params": path_params or {},
        "query": query or {},
        "url": url,
    }


def execute_request(
    entry: dict[str, Any],
    *,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    timeout: int = 30,
    base_url: str = BASE_URL,
) -> tuple[dict[str, Any], dict[str, Any]]:
    request_context = build_request_context(entry, path_params=path_params, query=query, base_url=base_url)
    request = Request(request_context["url"], method=entry["method"])
    request.add_header("Accept", "application/json")
    with urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return request_context, json.loads(payload)


def fetch_endpoint(
    *,
    endpoint_key: str | None = None,
    asset_class: str | None = None,
    family: str | None = None,
    metric: str | None = None,
    path_params: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    raw: bool = False,
    catalog_path=None,
    timeout: int = 30,
    base_url: str = BASE_URL,
) -> dict[str, Any]:
    entry = resolve_entry(
        endpoint_key=endpoint_key,
        asset_class=asset_class,
        family=family,
        metric=metric,
        catalog_path=catalog_path,
        path_params=path_params,
    )
    request_context, response = execute_request(
        entry,
        path_params=path_params,
        query=query,
        timeout=timeout,
        base_url=base_url,
    )
    shape_family = infer_shape_family(response, entry.get("shape_family"))
    snapshot = load_snapshot(entry["key"])
    result = {
        "endpoint_key": entry["key"],
        "request": request_context,
        "response_envelope": response,
        "shape_family": shape_family,
        "schema_source": "snapshot" if snapshot else entry["doc_status"],
        "schema_snapshot": snapshot["snapshot_path"] if snapshot and "snapshot_path" in snapshot else None,
    }
    if not raw:
        result["normalized_data"] = normalize_data(response, shape_family)
        result["display_data"] = format_display_data(result["normalized_data"])
    return result


def fill_path_template(path_template: str, path_params: dict[str, Any]) -> str:
    resolved = path_template
    for key in extract_required_params(path_template):
        if key not in path_params:
            raise ValueError(f"Missing path parameter: {key}")
        resolved = resolved.replace(f"{{{key}}}", str(path_params[key]))
    return resolved


def extract_required_params(path_template: str) -> list[str]:
    required: list[str] = []
    start = 0
    while True:
        left = path_template.find("{", start)
        if left == -1:
            return required
        right = path_template.find("}", left)
        if right == -1:
            return required
        required.append(path_template[left + 1 : right])
        start = right + 1


def normalize_data(response: dict[str, Any], shape_family: str) -> Any:
    if shape_family == "empty_success":
        return None

    data = response.get("data")
    if shape_family == "timeseries_aggregate" and isinstance(data, list):
        return [{"time": item.get("time"), "aggregates": item.get("aggregates", [])} for item in data]
    if shape_family == "pie_name_value" and isinstance(data, list):
        return [{"name": item.get("name"), "value": item.get("value")} for item in data]
    if shape_family in {"dataset_wrapped_list", "dataset_nested_networks"} and isinstance(data, dict):
        return data.get("list", [])
    return data


def encode_query(query: dict[str, Any]) -> str:
    normalized: list[tuple[str, Any]] = []
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, list):
            for item in value:
                normalized.append((key, item))
        else:
            normalized.append((key, value))
    return urlencode(normalized, doseq=True)
