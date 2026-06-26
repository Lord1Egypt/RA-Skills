from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from model import load_json, write_json


def _safe_json_for_script(value: Any) -> str:
    return json.dumps(json.dumps(value, ensure_ascii=False)).replace("</", "<\\/")


def _load_patch_records(
    patch_path: Path,
    revision_id: str | None,
    field_locks: dict[str, Any],
) -> list[dict[str, Any]]:
    if patch_path.exists():
        raw_patch = patch_path.read_text(encoding="utf-8").strip()
        if raw_patch:
            return [json.loads(line) for line in raw_patch.splitlines() if line.strip()]

    seed_entry = {
        "op": "seed_patch_log",
        "revisionId": revision_id,
        "fieldLocks": field_locks,
    }
    patch_path.write_text(json.dumps(seed_entry, ensure_ascii=False) + "\n", encoding="utf-8")
    return [seed_entry]


def write_viewer_package(
    blueprint_path: Path,
    viewer_path: Path,
    handoff_path: Path,
    patch_path: Path,
) -> None:
    blueprint = load_json(blueprint_path)
    asset_path = Path(__file__).parent / "assets" / "viewer.html"
    viewer_template = asset_path.read_text(encoding="utf-8")
    viewer_path.parent.mkdir(parents=True, exist_ok=True)
    patch_path.parent.mkdir(parents=True, exist_ok=True)
    meta = blueprint.get("meta", {})
    patch_log = _load_patch_records(
        patch_path,
        meta.get("revisionId"),
        blueprint.get("editor", {}).get("fieldLocks", {}),
    )
    rendered = viewer_template.replace(
        "__BLUEPRINT_JSON__",
        _safe_json_for_script(blueprint),
    ).replace(
        "__PATCH_LOG_JSON__",
        _safe_json_for_script(patch_log),
    )
    viewer_path.write_text(rendered, encoding="utf-8")

    handoff = {
        "revisionId": meta.get("revisionId"),
        "parentRevisionId": meta.get("parentRevisionId"),
        "lastModifiedBy": meta.get("lastModifiedBy"),
        "blueprintPath": str(blueprint_path),
        "viewerPath": str(viewer_path),
        "patchPath": str(patch_path),
    }
    write_json(handoff_path, handoff)
