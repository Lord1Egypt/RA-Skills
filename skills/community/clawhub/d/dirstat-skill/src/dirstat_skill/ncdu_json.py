from __future__ import annotations

import json
from pathlib import Path

from dirstat_skill.models import NormalizedNode, ParsedExport


def parse_ncdu_export(export_path: Path) -> ParsedExport:
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    return parse_ncdu_payload(payload)


def parse_ncdu_payload(payload: list[object]) -> ParsedExport:
    directory = payload[3]
    root_info = directory[0]
    root_path = root_info["name"]
    nodes: list[NormalizedNode] = []
    _walk_directory(directory, root_path, nodes)
    return ParsedExport(root_path=root_path, nodes=nodes)


def _walk_directory(entry: list[object], current_path: str, nodes: list[NormalizedNode]) -> int:
    info = entry[0]
    own_dsize = int(info.get("dsize", 0))
    total_dsize = own_dsize
    child_nodes: list[NormalizedNode] = []
    nodes.append(
        NormalizedNode(
            path=current_path,
            name=info["name"].split("/")[-1] or current_path,
            is_dir=True,
            asize=int(info.get("asize", 0)),
            dsize=0,
        )
    )
    for child in entry[1:]:
        if isinstance(child, list):
            child_info = child[0]
            child_path = f"{current_path.rstrip('/')}/{child_info['name']}"
            total_dsize += _walk_directory(child, child_path, child_nodes)
            continue

        child_path = f"{current_path.rstrip('/')}/{child['name']}"
        file_dsize = int(child.get("dsize", 0))
        child_nodes.append(
            NormalizedNode(
                path=child_path,
                name=child["name"],
                is_dir=False,
                asize=int(child.get("asize", 0)),
                dsize=file_dsize,
            )
        )
        total_dsize += file_dsize
    nodes[-1] = NormalizedNode(
        path=current_path,
        name=info["name"].split("/")[-1] or current_path,
        is_dir=True,
        asize=int(info.get("asize", 0)),
        dsize=total_dsize,
    )
    nodes.extend(child_nodes)
    return total_dsize

