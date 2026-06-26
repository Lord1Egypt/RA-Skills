#!/usr/bin/env python3
"""
Validate an AgentCard JSON file against A2A schema requirements.

Usage:
    python3 validate_agent_card.py <agent-card.json>

Exit codes:
    0 — valid
    1 — invalid (missing required fields)
    2 — file not found or not readable
"""

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = ["name", "description", "version", "capabilities", "authentication"]
REQUIRED_CAPABILITIES = ["streaming", "pushNotifications"]
REQUIRED_AUTH = ["schemes", "credentials"]


def validate_file(path: str) -> bool:
    p = Path(path)
    if not p.exists():
        print(f"ERROR: file not found: {path}")
        return False

    try:
        with open(p) as f:
            card = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}")
        return False

    # Top-level required fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in card:
            print(f"ERROR: missing required top-level field: {field}")
            return False

    # capabilities.* required fields
    caps = card.get("capabilities", {})
    for field in REQUIRED_CAPABILITIES:
        if field not in caps:
            print(f"ERROR: missing capabilities.{field}")
            return False

    # Validate streaming value
    valid_streaming = {"SUPPORTED", "NOT_SUPPORTED", "STREAMABLE"}
    if caps.get("streaming") not in valid_streaming:
        print(f"ERROR: capabilities.streaming must be one of {valid_streaming}")
        return False

    # Validate pushNotifications value
    valid_push = {"SUPPORTED", "NOT_SUPPORTED"}
    if caps.get("pushNotifications") not in valid_push:
        print(f"ERROR: capabilities.pushNotifications must be one of {valid_push}")
        return False

    # authentication.* required fields
    auth = card.get("authentication", {})
    for field in REQUIRED_AUTH:
        if field not in auth:
            print(f"ERROR: missing authentication.{field}")
            return False

    # credentials must be "required" or "optional"
    valid_creds = {"required", "optional"}
    if auth.get("credentials") not in valid_creds:
        print(f"ERROR: authentication.credentials must be one of {valid_creds}")
        return False

    # skills[] — each skill needs id, name, description
    for i, skill in enumerate(card.get("skills", [])):
        for field in ["id", "name", "description"]:
            if field not in skill:
                print(f"ERROR: skills[{i}] missing required field: {field}")
                return False

    # skills[].id uniqueness
    ids = [s["id"] for s in card.get("skills", [])]
    if len(ids) != len(set(ids)):
        print("ERROR: skills[].id values must be unique")
        return False

    print(f"✅ AgentCard is valid — {p}")
    print(f"   name:         {card['name']}")
    print(f"   version:      {card['version']}")
    print(f"   streaming:    {caps['streaming']}")
    print(f"   pushNotif:    {caps['pushNotifications']}")
    print(f"   auth.schemes: {auth['schemes']}")
    print(f"   skills count: {len(card.get('skills', []))}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_agent_card.py <agent-card.json>")
        sys.exit(2)
    sys.exit(0 if validate_file(sys.argv[1]) else 1)


if __name__ == "__main__":
    main()