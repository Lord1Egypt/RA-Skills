#!/usr/bin/env python3
"""Collect and print one read-only BTC or ETH strategy input bundle."""

from __future__ import annotations

import json
import sys

from mcp_server import get_crypto_strategy_inputs


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1].upper() not in {"BTC", "ETH"}:
        print("usage: cli_analyze.py BTC|ETH", file=sys.stderr)
        return 2
    result = get_crypto_strategy_inputs(sys.argv[1].upper())
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
