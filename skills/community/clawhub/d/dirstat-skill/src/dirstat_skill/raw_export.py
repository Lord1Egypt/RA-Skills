from __future__ import annotations

import json
from pathlib import Path

from dirstat_skill.models import NormalizedNode, ParsedExport
from dirstat_skill.ncdu_json import parse_ncdu_payload


def load_raw_export(export_path: Path) -> dict[str, object]:
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "engine" in payload:
        return payload
    return {"engine": "ncdu", "payload": payload}


def parse_export(export_path: Path) -> ParsedExport:
    payload = load_raw_export(export_path)
    engine_name = payload["engine"]
    if engine_name == "windows-native":
        return _parse_windows_export_payload(payload)
    if engine_name == "ncdu":
        raw_payload = payload.get("payload")
        if not isinstance(raw_payload, list):
            raise ValueError("Unsupported ncdu payload")
        return parse_ncdu_payload(raw_payload)
    raise ValueError(f"Unsupported raw export engine: {engine_name}")


def _parse_windows_export_payload(payload: dict[str, object]) -> ParsedExport:
    roots = payload.get("roots")
    root_values = roots if isinstance(roots, list) else [payload.get("root", "")]
    normalized_roots = [str(item) for item in root_values if item]
    nodes_payload = payload.get("nodes")
    if not isinstance(nodes_payload, list):
        raise ValueError("Unsupported windows-native payload")

    nodes: list[NormalizedNode] = []
    for item in nodes_payload:
        if not isinstance(item, dict):
            continue
        nodes.append(
            NormalizedNode(
                path=str(item["path"]),
                name=str(item["name"]),
                is_dir=bool(item["is_dir"]),
                asize=int(item.get("size", 0)),
                dsize=int(item.get("dsize", item.get("size", 0))),
            )
        )

    root_path = ", ".join(normalized_roots) if normalized_roots else "windows-native"
    return ParsedExport(root_path=root_path, nodes=nodes)

