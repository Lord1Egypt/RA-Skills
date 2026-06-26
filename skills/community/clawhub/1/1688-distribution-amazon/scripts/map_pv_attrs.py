"""Step5: map 1688 product PVs to Amazon required attributes."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import ALPHA_PRE_BASE, alpha_headers, dump, post

PV_MAP_URL = f"{ALPHA_PRE_BASE}/global.1688.cbu.pv.mapping.query/1.0"
SUPPORTED_PLATFORM = "amazon"


def normalize_platform(platform: str | None = SUPPORTED_PLATFORM) -> str:
    normalized = (platform or SUPPORTED_PLATFORM).strip().lower()
    if normalized != SUPPORTED_PLATFORM:
        raise ValueError(f"CPV mapping only supports platform={SUPPORTED_PLATFORM}; got {platform!r}")
    return normalized


def query_cpv_mapping(offer_id: int | str, required_attrs: list[dict], platform: str = SUPPORTED_PLATFORM) -> dict:
    platform = normalize_platform(platform)
    payload = {
        "offerId": int(offer_id),
        "requiredPv": json.dumps(required_attrs, ensure_ascii=False),
        "platform": platform,
    }
    response = post(PV_MAP_URL, payload, headers=alpha_headers(), timeout=90)
    if response.get("resultCode") != "SUCCESS" or not response.get("result"):
        raise RuntimeError(f"CPV mapping failed: {response}")
    data = response["result"].get("data") or response["result"]
    return {
        "commonPvList": data.get("commonPvList", []),
        "skuPvList": data.get("skuPvList", []),
        "descriptions": data.get("descriptions", []),
        "pvList": data.get("pvList", []),
    }


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 1:
        print("Usage: python scripts/map_pv_attrs.py <session_dir> OR <offerId> [requiredPvJsonFile] [platform]", file=sys.stderr)
        return 1
    if os.path.isdir(argv[0]):
        from scripts.common import read_session, write_session

        session_dir = argv[0]
        run_input = read_session(session_dir, "input.json", required_keys=["offer_id"])
        attr_data = read_session(session_dir, "map_amazon_attrs.json", required_keys=["requiredAttrs"])
        result = query_cpv_mapping(run_input["offer_id"], attr_data["requiredAttrs"], platform=SUPPORTED_PLATFORM)
        write_session(session_dir, "map_pv_attrs.json", result)
        print(dump(result))
    else:
        if len(argv) >= 2:
            with open(argv[1]) as f:
                required = json.load(f)
        else:
            required = json.load(sys.stdin)
        platform = argv[2] if len(argv) >= 3 else SUPPORTED_PLATFORM
        try:
            print(dump(query_cpv_mapping(argv[0], required, platform=platform)))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            raise SystemExit(2) from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
