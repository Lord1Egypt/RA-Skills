#!/usr/bin/env python3
"""Proxy chain resolver for the `down` skill.

Usage:
    python proxy_chain.py --json

Emits a JSON object on stdout describing the ordered proxy chain to try.
Exit code 0 always (except on bad usage) — caller iterates the chain
and retries downloads through each proxy until one succeeds.

Design notes:
  * Read-only. Never probes proxies, never modifies environment.
  * Zero third-party deps — stdlib only, Python 3.9+.
  * No network calls — pure configuration resolution.
    Why no probing? Because a proxy can be "up" but not reach the target;
    the only reliable way to verify is by attempting the actual download.
  * Priority order (first hit wins, auto-deduped):
      1. direct            (always first, unless NO_PROXY matches)
      2. env               (HTTPS_PROXY / HTTP_PROXY env vars)
      3. config file       (~/.downrc, JSON)
      4. builtin defaults  (hardcoded in this script)
  * Honors NO_PROXY — caller must skip proxies when target domain matches.
  * Never installs, never modifies environment. Caller decides retry logic.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional


# --- Builtin default proxy chain --------------------------------------------

# Order matters: Hermes-verified first, then Clash default, then LAN fallback.
BUILTIN_PROXY_CHAIN: list[str] = [
    "http://127.0.0.1:7897",        # Hermes runtime verified proxy (from user memory)
    "http://127.0.0.1:7890",        # Clash default port
    "http://192.168.31.135:7890",   # LAN fallback (NAS/Pi-hole Clash)
]


# --- Config file handling ---------------------------------------------------

CONFIG_FILE = "~/.downrc"
CONFIG_FILE_DESC = "~/.downrc (JSON)"


def _resolve_config_path() -> Path:
    """Return absolute path to ~/.downrc."""
    return Path(os.path.expanduser(CONFIG_FILE))


def _load_config(config_path: Path) -> Optional[dict]:
    """Load JSON config from disk. Returns None on any error."""
    if not config_path.is_file():
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


# --- Chain resolution -------------------------------------------------------

def resolve_chain() -> dict:
    """Build the ordered proxy chain with deduplication.

    Returns dict with keys: chain, noproxy, env_honored, config_file, config_exists.
    """
    seen: set[str] = set()
    chain: list[dict] = []

    # 1. Direct (always first)
    chain.append({"type": "direct", "label": "直连"})

    # 2. Environment variables
    for var_name in ("HTTPS_PROXY", "HTTP_PROXY"):
        val = os.environ.get(var_name)
        if val and val not in seen:
            chain.append({
                "type": "env",
                "proxy": val,
                "source": f"{var_name} env",
            })
            seen.add(val)

    # 3. Config file (~/.downrc)
    config_path = _resolve_config_path()
    config_exists = config_path.is_file()
    config_data = _load_config(config_path) if config_exists else None

    if config_data and isinstance(config_data.get("proxy_chain"), list):
        for p in config_data["proxy_chain"]:
            if isinstance(p, str) and p not in seen:
                chain.append({
                    "type": "file",
                    "proxy": p,
                    "source": CONFIG_FILE_DESC,
                })
                seen.add(p)

    # 4. Builtin defaults
    for p in BUILTIN_PROXY_CHAIN:
        if p not in seen:
            chain.append({
                "type": "builtin",
                "proxy": p,
                "source": "SKILL.md default",
            })
            seen.add(p)

    return {
        "chain": chain,
        "noproxy": os.environ.get("NO_PROXY", ""),
        "env_honored": ["HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY"],
        "config_file": CONFIG_FILE_DESC,
        "config_exists": config_exists,
    }


# --- CLI --------------------------------------------------------------------

def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="Resolve the proxy chain for the `down` skill."
    )
    p.add_argument("--json", action="store_true",
                   help="Emit JSON (default; kept for clarity)")
    args = p.parse_args(argv)

    output = resolve_chain()
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
