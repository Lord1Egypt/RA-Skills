from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any


TOP_LEVEL_KEYS = [
    "version",
    "meta",
    "context",
    "library",
    "relations",
    "views",
    "editor",
    "artifacts",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def new_revision_meta(
    parent_revision_id: str | None = None,
    modified_by: str = "ai",
) -> dict[str, str | None]:
    revision_id = f"rev-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    return {
        "revisionId": revision_id,
        "parentRevisionId": parent_revision_id,
        "lastModifiedAt": utc_now(),
        "lastModifiedBy": modified_by,
    }


def ensure_top_level_shape(payload: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in TOP_LEVEL_KEYS:
        default = [] if key in {"relations", "views"} else {}
        result[key] = deepcopy(payload.get(key, default))
    result["library"].setdefault("capabilities", [])
    result["library"].setdefault("actors", [])
    result["library"].setdefault("flowSteps", [])
    result["library"].setdefault("systems", [])
    return result
