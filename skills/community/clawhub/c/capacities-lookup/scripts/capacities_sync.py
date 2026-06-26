from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from capacities_cache import load_state, save_spaces_cache, save_state, save_structures_cache
from capacities_client import get_space_info, get_spaces, load_config


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_space_info(raw: dict[str, Any], space_id: str) -> dict[str, Any]:
    structures = raw.get("structures", [])
    normalized_structures: list[dict[str, Any]] = []
    structures_by_id: dict[str, dict[str, Any]] = {}

    for item in structures:
        structure = {
            "id": item.get("id"),
            "title": item.get("title"),
            "pluralName": item.get("pluralName"),
            "labelColor": item.get("labelColor"),
            "propertyDefinitions": item.get("propertyDefinitions", []),
            "collections": item.get("collections", []),
        }
        normalized_structures.append(structure)
        if structure["id"]:
            structures_by_id[structure["id"]] = structure

    return {
        "spaceId": space_id,
        "syncedAt": _now_iso(),
        "structureCount": len(normalized_structures),
        "structures": normalized_structures,
        "structuresById": structures_by_id,
    }


def verify_main_space() -> dict[str, Any]:
    config = load_config()
    target_space_id = config["mainSpaceId"]
    spaces = get_spaces()
    save_spaces_cache(spaces)
    for space in spaces.get("spaces", []):
        if space.get("id") == target_space_id:
            return {"verified": True, "space": space}
    return {"verified": False, "space": None}


def sync_structures() -> dict[str, Any]:
    config = load_config()
    state = load_state()
    target_space_id = config["mainSpaceId"]

    try:
        verification = None
        if config.get("verifySpacesOnSync", True):
            verification = verify_main_space()

        raw = get_space_info(target_space_id)
        normalized = normalize_space_info(raw, target_space_id)
        save_structures_cache(normalized)

        state.update(
            {
                "cacheSchemaVersion": config.get("cacheSchemaVersion", 1),
                "lastStructureSyncAt": normalized["syncedAt"],
                "lastStructureSyncOk": True,
                "lastError": None,
                "spaceVerification": verification,
            }
        )
        save_state(state)
        return {
            "ok": True,
            "spaceId": target_space_id,
            "structureCount": normalized["structureCount"],
            "verification": verification,
        }
    except Exception as exc:
        state.update(
            {
                "lastStructureSyncOk": False,
                "lastError": str(exc),
                "lastStructureSyncAttemptAt": _now_iso(),
            }
        )
        save_state(state)
        raise
