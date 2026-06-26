#!/usr/bin/env python3
"""
check-profile.py — Pre-flight lookup for Agent Tollbooth profiles.

Usage:
    python3 scripts/check-profile.py <service-name-or-domain>

Returns the safe pattern for a known service, or a "no profile yet" notice
that seeds the log so promote-profile.py can eventually build one.

Exit codes:
    0 — profile found and printed
    1 — no profile found (observation logged, safe to continue)
"""

from __future__ import annotations

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_DIR = SCRIPT_DIR.parent
PROFILES_PATH = MODULE_DIR / "references" / "profiles.md"

_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
DATA_DIR = _WORKSPACE / "data" / "agent-tollbooth"
LOG_PATH = DATA_DIR / "web-access-log.json"

# Domain → canonical service name aliases
ALIASES: dict[str, str] = {
    "openai.com": "OpenAI API",
    "api.openai.com": "OpenAI API",
    "anthropic.com": "Anthropic API",
    "api.anthropic.com": "Anthropic API",
    "github.com": "GitHub API",
    "api.github.com": "GitHub API",
    "search.brave.com": "Brave Search API",
    "api.search.brave.com": "Brave Search API",
    "google.serper.dev": "Serper (Google Search API)",
    "serper.dev": "Serper (Google Search API)",
    "notion.com": "Notion API",
    "api.notion.com": "Notion API",
    "airtable.com": "Airtable API",
    "api.airtable.com": "Airtable API",
    "stripe.com": "Stripe API",
    "api.stripe.com": "Stripe API",
    "huggingface.co": "HuggingFace Inference API",
    "api-inference.huggingface.co": "HuggingFace Inference API",
    "firecrawl.dev": "Firecrawl",
    "api.firecrawl.dev": "Firecrawl",
    "finance.yahoo.com": "Yahoo Finance",
    "query2.finance.yahoo.com": "Yahoo Finance",
    "coingecko.com": "CoinGecko",
    "api.coingecko.com": "CoinGecko",
    "ghost.io": "Ghost Admin API",
    "clawhub.ai": "ClawHub API",
    "api.telegram.org": "Telegram Bot API",
    "replicate.com": "Replicate (FLUX image gen)",
    "api.replicate.com": "Replicate (FLUX image gen)",
}


def _parse_profiles(path: Path) -> dict[str, list[str]]:
    """Parse profiles.md into {service_name: [bullet lines]}."""
    if not path.exists():
        return {}

    profiles: dict[str, list[str]] = {}
    current: str | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            profiles[current] = []
        elif current is not None and line.startswith("- "):
            profiles[current].append(line)

    return profiles


def _resolve_service(query: str, profiles: dict[str, list[str]]) -> str | None:
    """
    Match query against known profile names and aliases.
    Returns the canonical profile name or None.
    """
    q = query.strip().lower()

    # Exact alias match (domain or shorthand)
    for alias, canonical in ALIASES.items():
        if q == alias.lower():
            return canonical

    # Exact profile name match
    for name in profiles:
        if q == name.lower():
            return name

    # Fuzzy: query is a substring of a profile name or vice versa
    for name in profiles:
        if q in name.lower() or name.lower() in q:
            return name

    # Fuzzy: alias value contains query
    for alias, canonical in ALIASES.items():
        if q in alias.lower():
            return canonical

    return None


def _log_miss(service_raw: str) -> None:
    """Log a cache miss so promote-profile.py can track unknown services."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("[]", encoding="utf-8")

    try:
        events = json.loads(LOG_PATH.read_text(encoding="utf-8") or "[]")
    except json.JSONDecodeError:
        events = []

    events.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": service_raw,
        "event_type": "profile_miss",
        "detail": f"No profile found for '{service_raw}' — observation started",
        "worked": None,
    })
    LOG_PATH.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 check-profile.py <service-name-or-domain>", file=sys.stderr)
        return 2

    query = " ".join(sys.argv[1:])
    profiles = _parse_profiles(PROFILES_PATH)
    match = _resolve_service(query, profiles)

    if match and profiles.get(match):
        print(f"✓ Profile found: {match}")
        print()
        for line in profiles[match]:
            print(line)
        return 0
    else:
        print(f"✗ No profile for '{query}'")
        print("  Logging observation. Use promote-profile.py after a few interactions to build one.")
        _log_miss(query)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
