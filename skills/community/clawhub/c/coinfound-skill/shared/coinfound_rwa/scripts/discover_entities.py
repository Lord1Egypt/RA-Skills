#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.coinfound_rwa.probe import discover_sample_entities


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover sample CoinFound RWA entity identifiers.")
    parser.add_argument("--asset-class", required=True, help="Asset class such as platforms or market-overview")
    parser.add_argument("--limit", type=int, default=5, help="Maximum candidates per field")
    args = parser.parse_args()

    try:
        result = discover_sample_entities(args.asset_class, limit=args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - CLI guard
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
