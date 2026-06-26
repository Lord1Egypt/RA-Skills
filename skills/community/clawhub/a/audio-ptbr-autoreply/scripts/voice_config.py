#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace"))
CONFIG_PATH = WORKSPACE / ".audio_pt_voice_config.json"

VOICE_MAP = {
    "jeff": "jeff",
    "cadu": "cadu",
    "faber": "faber",
    "miro": "miro",
    "feminina": "miro",
    "masculina": "jeff",
}

VOICE_LABELS = {
    "jeff": "Jeff",
    "cadu": "Cadu",
    "faber": "Faber",
    "miro": "Miro",
}


def ensure_config() -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps({"voice": "jeff"}), encoding="utf-8")


def get_voice() -> str:
    ensure_config()
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        voice = data.get("voice", "jeff")
        return voice if voice in VOICE_LABELS else "jeff"
    except Exception:
        return "jeff"


def set_voice(name: str) -> str:
    ensure_config()
    normalized = VOICE_MAP.get(name.lower())
    if not normalized:
        raise ValueError(f"Unknown voice: {name}")
    CONFIG_PATH.write_text(json.dumps({"voice": normalized}), encoding="utf-8")
    return normalized


def print_list() -> None:
    print("Vozes disponíveis:")
    print("- jeff")
    print("- cadu")
    print("- faber")
    print("- miro")
    print("- feminina -> miro")
    print("- masculina -> jeff")
    print(f"Atual: {get_voice()}")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(get_voice())
        return 0

    cmd = argv[1].lower()

    if cmd == "get":
        print(get_voice())
        return 0
    if cmd == "list":
        print_list()
        return 0
    if cmd == "set":
        if len(argv) < 3:
            print("Usage: voice_config.py set <voice>", file=sys.stderr)
            return 1
        try:
            voice = set_voice(argv[2])
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Voz definida para: {voice}")
        return 0

    # convenience: direct voice name as subcommand
    if cmd in VOICE_MAP:
        voice = set_voice(cmd)
        print(f"Voz definida para: {voice}")
        return 0

    print("Usage: voice_config.py [get|list|set <voice>]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
