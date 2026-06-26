#!/usr/bin/env python3
"""Generate a 6-digit TOTP code for a stored alias."""

from __future__ import annotations

import argparse
import json
import sys

from totp_common import generate_totp, normalize_seed
from secret_store import backend_name, fetch_seed


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a TOTP code from a Keychain alias.")
    parser.add_argument("--alias", required=True, help="Stored alias.")
    parser.add_argument("--json", action="store_true", help="Return JSON output.")
    args = parser.parse_args()

    try:
        seed = normalize_seed(fetch_seed(args.alias))
        code, expires_in = generate_totp(seed)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"alias": args.alias, "code": code, "expires_in": expires_in, "backend": backend_name()}))
    else:
        print(code)
        print(f"expires_in={expires_in}")
        print(f"backend={backend_name()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
