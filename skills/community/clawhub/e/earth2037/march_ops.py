#!/usr/bin/env python3
"""March / combat via ADDCOMBATQUEUE (e.g. oasis attack marchType 256)."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time


def _import_game():
    base = os.path.dirname(os.path.abspath(__file__))
    if base not in sys.path:
        sys.path.insert(0, base)
    from cache import _game_command, _get_token, _load_config, humanize_command_output
    return _game_command, _get_token, _load_config, humanize_command_output


def _expand_troops(spec: str) -> str:
    parts = []
    for seg in spec.split("|"):
        seg = seg.strip()
        if not seg:
            continue
        if "_" not in seg:
            arm, qty = seg.split(":", 1)
            parts.append(f"{arm.strip()}:{qty.strip()}_0_0_0")
        else:
            parts.append(seg)
    return "|".join(parts)


def _net_date_ms(ms: int, offset: str = "+0800") -> str:
    return f"/Date({ms}{offset})/"


def main():
    gc, get_token, load_cfg, humanize = _import_game()
    ap = argparse.ArgumentParser(description="Earth2037 ADDCOMBATQUEUE helper")
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)
    sub = ap.add_subparsers(dest="mode", required=True)
    p_w = sub.add_parser("attack-oasis", help="Wilderness attack, default marchType=256")
    p_w.add_argument("--from", dest="from_city", type=int, required=True)
    p_w.add_argument("--to", dest="to_city", type=int, required=True)
    p_w.add_argument("--troops", required=True)
    p_w.add_argument("--march-type", type=int, default=256)
    p_w.add_argument("--hero", type=int, default=0)
    p_w.add_argument("--upkeep", type=int, default=0)
    p_w.add_argument("--in-seconds", type=int, default=120)
    p_w.add_argument("--resources", default="0|0|0|0")
    p_j = sub.add_parser("raw-json")
    p_j.add_argument("json_one_line")

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("Need EARTH2037_TOKEN", file=sys.stderr)
        sys.exit(1)

    if args.mode == "attack-oasis":
        ms = int(time.time() * 1000) + args.in_seconds * 1000
        body = {
            "fromCityID": args.from_city,
            "toCityID": args.to_city,
            "marchType": args.march_type,
            "troops": _expand_troops(args.troops),
            "resources": args.resources,
            "heroID": args.hero,
            "spyIntoType": 0,
            "arrivalTime": _net_date_ms(ms),
            "completed": False,
            "id": 0,
            "upkeep": args.upkeep,
        }
        line = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
    else:
        line = args.json_one_line.strip()

    try:
        out = gc(api, token, "ADDCOMBATQUEUE", line)
        print(humanize(out))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
