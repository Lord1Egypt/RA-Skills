"""
A2A Gateway v2.2 — Agent Registry (simplified)

Keeps only what router needs: load, save, find.
No CLI. Migration completed, v1 file is legacy.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE = Path(__file__).parent.parent
REGISTRY_FILE = WORKSPACE / "registry" / "agent_cards_v2.json"
REGISTRY_V1 = WORKSPACE / "registry" / "agent_cards.json"  # legacy fallback


def load() -> Dict[str, Any]:
    """Load agent registry, preferring v2, falling back to v1."""
    for path in (REGISTRY_FILE, REGISTRY_V1):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}


def save(data: Dict[str, Any]):
    """Persist registry to v2 file."""
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find(keyword: str) -> List[Dict[str, Any]]:
    """Find agents by keyword match in name/skills/description."""
    registry = load()
    keyword_lower = keyword.lower()
    matches = []
    for agent_id, card in registry.items():
        search_text = " ".join([
            card.get("name", ""),
            card.get("description", ""),
            " ".join(card.get("skills", [])),
            " ".join(card.get("capabilities", [])),
        ]).lower()
        if keyword_lower in search_text:
            matches.append({"agent_id": agent_id, "card": card})
    return matches
