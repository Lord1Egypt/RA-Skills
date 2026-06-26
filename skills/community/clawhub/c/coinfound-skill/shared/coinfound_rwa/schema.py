from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .catalog import SNAPSHOT_DIR


def infer_shape_family(response: dict[str, Any], suggested: str | None = None) -> str:
    if response.get("code") == 0 and "data" not in response:
        return "empty_success"

    data = response.get("data")
    inferred = _infer_shape_from_data(data)

    if suggested in {None, "", "unknown", "unsupported"}:
        return inferred
    if suggested == "dataset_wrapped_list" and inferred == "dataset_nested_networks":
        return inferred
    return suggested


def _infer_shape_from_data(data: Any) -> str:
    if isinstance(data, list):
        sample = data[:3]
        if sample and all(isinstance(item, dict) and "time" in item and "aggregates" in item for item in sample):
            return "timeseries_aggregate"
        if sample and all(isinstance(item, dict) and {"name", "value"}.issubset(item.keys()) for item in sample):
            return "pie_name_value"
        return "envelope_list"

    if isinstance(data, dict):
        wrapped = data.get("list")
        if isinstance(wrapped, list):
            if any(isinstance(item, dict) and "networks" in item for item in wrapped[:3]):
                return "dataset_nested_networks"
            return "dataset_wrapped_list"
        return "envelope_object"

    if data is None:
        return "empty_success"
    return "unknown"


def infer_schema(value: Any) -> dict[str, Any]:
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {"type": "string"}
    if isinstance(value, list):
        if not value:
            return {"type": "array", "items": {"type": "unknown"}}
        item_schemas = [_normalize_schema(infer_schema(item)) for item in value[:5]]
        unique = _unique_schemas(item_schemas)
        if len(unique) == 1:
            items = unique[0]
        else:
            items = {"anyOf": unique}
        return {"type": "array", "items": items}
    if isinstance(value, dict):
        properties = {key: infer_schema(item) for key, item in sorted(value.items())}
        return {
            "type": "object",
            "properties": properties,
            "required": sorted(value.keys()),
        }
    return {"type": type(value).__name__}


def load_snapshot(endpoint_key: str, root: Path | None = None) -> dict[str, Any] | None:
    path = snapshot_path(endpoint_key, root=root)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def snapshot_path(endpoint_key: str, root: Path | None = None) -> Path:
    base = root or SNAPSHOT_DIR
    return base / f"{endpoint_key.replace('.', '__')}.json"


def write_snapshot(snapshot: dict[str, Any], root: Path | None = None) -> Path:
    endpoint_key = snapshot["endpoint_key"]
    output = snapshot_path(endpoint_key, root=root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return output


def _normalize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(schema, sort_keys=True, ensure_ascii=False))


def _unique_schemas(schemas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for schema in schemas:
        signature = json.dumps(schema, sort_keys=True, ensure_ascii=False)
        if signature in seen:
            continue
        unique.append(schema)
        seen.add(signature)
    return unique
