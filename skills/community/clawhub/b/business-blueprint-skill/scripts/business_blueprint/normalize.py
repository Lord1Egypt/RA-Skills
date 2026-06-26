from __future__ import annotations

from typing import Any


KNOWN_SYSTEM_ALIASES = {
    "salesforcecrm": "CRM",
    "salesforce": "CRM",
    "crm": "CRM",
    "pos": "POS",
    "enterprisewechat": "企业微信",
    "企微": "企业微信",
}


def _normalized(value: str) -> str:
    return "".join(
        ch.lower() for ch in value if ch.isalnum() or "\u4e00" <= ch <= "\u9fff"
    )


def normalize_system_name(raw_name: str) -> str:
    normalized = _normalized(raw_name.strip())
    return KNOWN_SYSTEM_ALIASES.get(normalized, raw_name.strip())


def _match_keys(name: str) -> set[str]:
    normalized = _normalized(name)
    canonical = _normalized(normalize_system_name(name))
    return {key for key in (normalized, canonical) if key}


def _system_match_keys(system: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for candidate in [system.get("name", ""), system.get("resolution", {}).get("canonicalName", "")]:
        if candidate:
            keys.update(_match_keys(candidate))
    for alias in system.get("aliases", []):
        if alias:
            keys.update(_match_keys(alias))
    return keys


def merge_or_create_system(
    systems: list[dict[str, Any]],
    raw_name: str,
    description: str,
) -> dict[str, Any]:
    canonical_name = normalize_system_name(raw_name)
    normalized_name = _normalized(canonical_name)
    raw_keys = _match_keys(raw_name)
    for system in systems:
        if raw_keys.intersection(_system_match_keys(system)):
            aliases = system.setdefault("aliases", [])
            for alias in {raw_name, canonical_name}:
                if alias and alias != system.get("name") and alias not in aliases:
                    aliases.append(alias)
            if description and not system.get("description"):
                system["description"] = description
            resolution = system.setdefault("resolution", {})
            resolution.setdefault("status", "canonical")
            resolution.setdefault("canonicalName", canonical_name)
            return system

    created = {
        "id": f"sys-{normalized_name or 'unknown'}",
        "kind": "system",
        "name": canonical_name,
        "aliases": [] if canonical_name == raw_name else [raw_name],
        "description": description,
        "resolution": {"status": "canonical", "canonicalName": canonical_name},
        "capabilityIds": [],
    }
    systems.append(created)
    return created


def mark_ambiguous(entity: dict[str, Any], canonical_name: str) -> dict[str, Any]:
    entity["resolution"] = {
        "status": "ambiguous",
        "canonicalName": canonical_name,
    }
    return entity
