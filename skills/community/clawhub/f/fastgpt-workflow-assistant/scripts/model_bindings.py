"""Preserve legacy names and stable model IDs without guessing cross-version mappings."""

from typing import Any


MODEL_INPUT_KEYS = frozenset({
    "model", "modelId", "rerankModel", "rerankModelId",
    "datasetSearchExtensionModel", "datasetSearchExtensionModelId",
})


def model_bindings(node: dict[str, Any]) -> dict[str, list[Any]]:
    """Keep keys, empty values, references, and duplicate bindings for drift checks."""
    result: dict[str, list[Any]] = {}
    for item in node.get("inputs", []):
        if isinstance(item, dict) and item.get("key") in MODEL_INPUT_KEYS:
            result.setdefault(item["key"], []).append(item.get("value"))
    return result


def collect_model_bindings(nodes: list[dict[str, Any]]) -> dict[str, dict[str, list[Any]]]:
    result = {}
    for node in nodes:
        bindings = model_bindings(node)
        if bindings:
            result[str(node.get("nodeId", node.get("id", "")))] = bindings
    return result
