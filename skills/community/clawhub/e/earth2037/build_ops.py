#!/usr/bin/env python3
"""
Building queue: GETBUILDCOST + ADDBUILDQUEUE only (same as game /getbuildcost and /addbuildqueue).

Examples:
  python3 build_ops.py getbuildcost "8:3,2"
  python3 build_ops.py getbuildcost "8 3"
  python3 build_ops.py addbuildqueue '{"buildAction":1,...}'
  python3 build_ops.py compose --tile 273897 --point 27 --build 8 --level 3
  python3 build_ops.py cancel-queue 273897 27

Some HTTP gateways may alias UPGRADE_* to ADDBUILDQUEUE; raw game protocol uses the two commands above.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time


def _import_game():
    base = os.path.dirname(os.path.abspath(__file__))
    if base not in sys.path:
        sys.path.insert(0, base)
    from cache import _game_command, _get_token, _load_config, humanize_command_output
    return _game_command, _get_token, _load_config, humanize_command_output


def _parse_svr_payload(data: str, cmd: str):
    if not data or not isinstance(data, str):
        return None
    pat = re.compile(r"^/svr\s+" + re.escape(cmd) + r"\s+(.+)$", re.IGNORECASE | re.DOTALL)
    m = pat.match(data.strip())
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def _net_date_ms(ms: int, tz: str = "+0800") -> str:
    return f"/Date({int(ms)}{tz})/"


def main():
    gc, get_token, load_cfg, humanize = _import_game()
    ap = argparse.ArgumentParser(description="GETBUILDCOST + ADDBUILDQUEUE")
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_cost = sub.add_parser("getbuildcost")
    p_cost.add_argument("parms")

    p_add = sub.add_parser("addbuildqueue")
    p_add.add_argument("json")

    p_comp = sub.add_parser("compose")
    p_comp.add_argument("--tile", type=int, required=True, dest="tile_id")
    p_comp.add_argument("--point", type=int, required=True, dest="point_id")
    p_comp.add_argument("--build", type=int, required=True, dest="build_id")
    p_comp.add_argument("--level", type=int, required=True)
    p_comp.add_argument("--tz", default="+0800")

    p_ca = sub.add_parser("cancel-queue")
    p_ca.add_argument("tile_id", type=int)
    p_ca.add_argument("point_id", type=int)

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("Need EARTH2037_TOKEN", file=sys.stderr)
        sys.exit(1)

    try:
        if args.cmd == "getbuildcost":
            out = gc(api, token, "GETBUILDCOST", args.parms.strip())
        elif args.cmd == "cancel-queue":
            out = gc(api, token, "CANCELBUILDQUEUE", f"{args.tile_id} {args.point_id}")
        elif args.cmd == "addbuildqueue":
            js = args.json
            if js.startswith("@"):
                with open(js[1:].strip(), "r", encoding="utf-8") as f:
                    js = f.read().strip()
            elif js == "-":
                js = sys.stdin.read().strip()
            out = gc(api, token, "ADDBUILDQUEUE", js)
        else:
            bid, lv = args.build_id, args.level
            cost_raw = gc(api, token, "GETBUILDCOST", f"{bid}:{lv}")
            data = _parse_svr_payload(cost_raw, "getbuildcost")
            if data is None:
                print(f"Bad getbuildcost response: {cost_raw!r}", file=sys.stderr)
                sys.exit(1)
            training = None
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("Level") == lv:
                        training = item.get("TrainingTime")
                        break
                if training is None and data and isinstance(data[0], dict):
                    training = data[0].get("TrainingTime")
            elif isinstance(data, dict):
                training = data.get("TrainingTime")
            if training is None:
                print(f"No TrainingTime in {data!r}", file=sys.stderr)
                sys.exit(1)
            sec = int(training)
            due_ms = int(time.time() * 1000) + sec * 1000
            body = {
                "buildAction": 1,
                "buildID": bid,
                "completed": False,
                "dueSecond": sec,
                "dueTime": _net_date_ms(due_ms, args.tz),
                "id": 0,
                "level": lv,
                "pointID": args.point_id,
                "tileID": args.tile_id,
            }
            line = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
            out = gc(api, token, "ADDBUILDQUEUE", line)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(humanize(out))


if __name__ == "__main__":
    main()
