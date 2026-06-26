from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT / "data"
DEFAULT_CATALOG_PATH = DATA_DIR / "endpoint_catalog.json"
SNAPSHOT_DIR = DATA_DIR / "schema_snapshots"
BASE_URL = "https://api.coinfound.org/api/kakyoin"


def load_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    catalog_path = path or DEFAULT_CATALOG_PATH
    with catalog_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_catalog(entries: list[dict[str, Any]], path: Path | None = None) -> Path:
    catalog_path = path or DEFAULT_CATALOG_PATH
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with catalog_path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return catalog_path
