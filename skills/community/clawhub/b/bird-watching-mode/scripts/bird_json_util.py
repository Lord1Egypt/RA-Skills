#!/usr/bin/env python3
"""Shared load/save for workspace/bird.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


SCHEMA_VERSION = 1


def default_doc() -> Dict[str, Any]:
    return {
        "version": SCHEMA_VERSION,
        "location_query": "",
        "region": None,
        "country_code": "",
        "observations": [],
    }


def workspace_bird_path(workspace: Path) -> Path:
    return workspace.resolve() / "workspace" / "bird.json"


def load_doc(workspace: Path) -> Dict[str, Any]:
    p = workspace_bird_path(workspace)
    if not p.is_file():
        return default_doc()
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("bird.json root must be an object")
    out = default_doc()
    out.update(data)
    if not isinstance(out.get("observations"), list):
        out["observations"] = []
    return out


def save_doc(workspace: Path, doc: Dict[str, Any]) -> None:
    p = workspace_bird_path(workspace)
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    p.write_text(text, encoding="utf-8")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def infer_country_code(region: Dict[str, Any]) -> str:
    kind = (region.get("kind") or "").strip()
    code = (region.get("code") or "").strip()
    parent = (region.get("parent") or "").strip()
    if kind == "country":
        return code
    if parent:
        return parent
    if "-" in code:
        return code.split("-", 1)[0]
    return code
