#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.coinfound_rwa.fetch import fetch_endpoint


def parse_json_argument(raw: str | None) -> dict[str, object]:
    if not raw:
        return {}
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("JSON argument must decode to an object.")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch CoinFound RWA GET data using the shared endpoint catalog.")
    parser.add_argument("--endpoint-key", help="Catalog endpoint key such as stable-coin.market-cap.timeseries")
    parser.add_argument("--asset-class", help="Asset class such as stable-coin")
    parser.add_argument("--family", help="Endpoint family such as timeseries, aggregates, list, pie, dataset")
    parser.add_argument("--metric", help="Optional metric such as market-cap or network")
    parser.add_argument("--path-params", help="JSON object for path params")
    parser.add_argument("--query", help="JSON object for query params")
    parser.add_argument("--raw", action="store_true", help="Return the raw response envelope without normalization")
    args = parser.parse_args()

    try:
        result = fetch_endpoint(
            endpoint_key=args.endpoint_key,
            asset_class=args.asset_class,
            family=args.family,
            metric=args.metric,
            path_params=parse_json_argument(args.path_params),
            query=parse_json_argument(args.query),
            raw=args.raw,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - CLI guard
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
