#!/usr/bin/env python3
"""
Decode the base64-encoded LoRA adapter shipped with this Clawhub skill.
Produces assets/adapters/adapters.safetensors from the .json wrapper.
Idempotent: skips if the binary already exists.

Usage:  python scripts/decode_adapters.py
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ADAPTER_DIR = SKILL_ROOT / "assets" / "adapters"
BINARY = ADAPTER_DIR / "adapters.safetensors"
ENCODED = ADAPTER_DIR / "adapters.safetensors.json"


def decode() -> bool:
    if BINARY.exists():
        print(f"Already decoded: {BINARY}")
        return True
    if not ENCODED.exists():
        print(f"Encoded file not found: {ENCODED}", file=sys.stderr)
        return False
    with open(ENCODED, "r", encoding="utf-8") as f:
        obj = json.load(f)
    raw = base64.b64decode(obj["data"])
    BINARY.write_bytes(raw)
    print(f"Decoded {ENCODED.name} -> {BINARY.name} ({len(raw):,} bytes)")
    return True


if __name__ == "__main__":
    if not decode():
        sys.exit(1)
