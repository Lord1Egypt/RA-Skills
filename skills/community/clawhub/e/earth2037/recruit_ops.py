#!/usr/bin/env python3
"""
Conscription / recruit — prefer GameSkillAPI bridge aliases (no JSON or times in the client):

  LISTRECRUITQUEUE / RECRUITQLIST  → GETCONSCRIPTIONQUEUE (list)
  RECRUITQUEUE / RECRUIT           → ADDCONSCRIPTIONQUEUE (args: troopId total [tileId])

Raw game names and JSON array still work for packet capture; use raw-add / compose if the bridge is not deployed.

Examples (bridge required):
  python3 recruit_ops.py list
  python3 recruit_ops.py list 293135
  python3 recruit_ops.py recruit 43 8
  python3 recruit_ops.py recruit 43 8 293135

Same logic as skills/earth2037-game/recruit_ops.py.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime


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
    raw = m.group(1).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _parse_net_date_ms(s) -> int | None:
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return int(s)
    m = re.search(r"/Date\((\d+)", str(s))
    return int(m.group(1)) if m else None


def _net_date_ms(ms: int, tz: str = "+0800") -> str:
    return f"/Date({int(ms)}{tz})/"


def _city_id(entry: dict) -> int | None:
    for k in ("cityID", "CityID", "villageID", "VillageID", "tileID", "TileID"):
        v = entry.get(k)
        if v is not None:
            try:
                return int(v)
            except (TypeError, ValueError):
                continue
    return None


def _queues_from_payload(data) -> list:
    if data is None:
        return []
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def _infer_unit_training(queues: list, troop_id: int) -> int | None:
    for q in queues:
        tid = q.get("troopID")
        if tid is None:
            tid = q.get("TroopID")
        if tid is not None and int(tid) == troop_id:
            ut = q.get("unitTraining")
            if ut is None:
                ut = q.get("UnitTraining")
            if ut is not None:
                return int(ut)
    return None


def _max_incomplete_due_ms_for_city(queues: list, tile_id: int) -> int | None:
    best = None
    for q in queues:
        if _city_id(q) != tile_id:
            continue
        done = q.get("completed")
        if done is None:
            done = q.get("Completed")
        if done:
            continue
        ms = _parse_net_date_ms(q.get("dueTime") or q.get("DueTime"))
        if ms is None:
            continue
        if best is None or ms > best:
            best = ms
    return best


def _parse_last_conscription_ms(data: str) -> int | None:
    if not data:
        return None
    s = data.strip()
    if s.startswith("/svr"):
        m = re.search(r"getlastconscription\s+(.+)$", s, re.IGNORECASE | re.DOTALL)
        if not m:
            return None
        s = m.group(1).strip()
    if not s:
        return None
    try:
        j = json.loads(s)
        if isinstance(j, str):
            ms = _parse_net_date_ms(j)
            if ms is not None:
                return ms
            if len(j) >= 10 and j[4:5] == "-":
                try:
                    dt = datetime.fromisoformat(j.replace("Z", "+00:00"))
                    return int(dt.timestamp() * 1000)
                except ValueError:
                    pass
    except json.JSONDecodeError:
        pass
    return _parse_net_date_ms(s)


def _build_queue_item(
    tile_id: int,
    troop_id: int,
    total: int,
    unit_training_sec: int,
    start_ms: int,
    tz: str,
) -> dict:
    u_ms = unit_training_sec * 1000
    next_ms = start_ms + u_ms
    due_ms = start_ms + u_ms * total
    return {
        "cityID": tile_id,
        "completed": False,
        "dueTime": _net_date_ms(due_ms, tz),
        "id": None,
        "nextUnit": _net_date_ms(next_ms, tz),
        "total": total,
        "troopID": troop_id,
        "unitTraining": unit_training_sec,
    }


def main():
    gc, get_token, load_cfg, humanize = _import_game()
    ap = argparse.ArgumentParser(
        description="Earth2037 recruit: LISTRECRUITQUEUE / RECRUITQUEUE (bridge); or raw ADDCONSCRIPTIONQUEUE"
    )
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", aliases=["getconscriptionqueue"], help="List recruit queue")
    p_list.add_argument("tile_id", nargs="?", default="", help="City tileID; empty = capital")

    p_rec = sub.add_parser("recruit", help="Enqueue recruit (no JSON)")
    p_rec.add_argument("troop_id", type=int)
    p_rec.add_argument("total", type=int)
    p_rec.add_argument("tile_id", nargs="?", type=int, default=None)

    p_raw = sub.add_parser("raw-add", aliases=["addconscriptionqueue"], help="Raw JSON array for ADDCONSCRIPTIONQUEUE")
    p_raw.add_argument("json")

    p_comp = sub.add_parser("compose", help="Local compose JSON (fallback without bridge)")
    p_comp.add_argument("--tile", type=int, required=True, dest="tile_id")
    p_comp.add_argument("--troop", type=int, required=True, dest="troop_id")
    p_comp.add_argument("--total", type=int, required=True)
    p_comp.add_argument("--unit-training", type=int, dest="unit_training", default=None)
    p_comp.add_argument("--arm-type", type=int, dest="arm_type", default=None)
    p_comp.add_argument("--tz", default="+0800")

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("❌ Need EARTH2037_TOKEN or config.json token", file=sys.stderr)
        sys.exit(1)

    try:
        if args.cmd in ("list", "getconscriptionqueue"):
            parms = (args.tile_id or "").strip()
            out = gc(api, token, "LISTRECRUITQUEUE", parms)
        elif args.cmd == "recruit":
            parts = [str(args.troop_id), str(args.total)]
            if args.tile_id is not None:
                parts.append(str(args.tile_id))
            out = gc(api, token, "RECRUITQUEUE", " ".join(parts))
        elif args.cmd in ("raw-add", "addconscriptionqueue"):
            js = args.json
            if js.startswith("@"):
                path = js[1:].strip()
                with open(path, "r", encoding="utf-8") as f:
                    js = f.read().strip()
            elif js == "-":
                js = sys.stdin.read().strip()
            if not js.lstrip().startswith("["):
                print("❌ ADDCONSCRIPTIONQUEUE expects a JSON array, e.g. [{...}]", file=sys.stderr)
                sys.exit(1)
            out = gc(api, token, "ADDCONSCRIPTIONQUEUE", js)
        elif args.cmd == "compose":
            raw = gc(api, token, "LISTRECRUITQUEUE", "")
            payload = _parse_svr_payload(raw, "getconscriptionqueue")
            queues = _queues_from_payload(payload)

            ut = args.unit_training
            if ut is None:
                ut = _infer_unit_training(queues, args.troop_id)
            if ut is None or ut < 1:
                print("❌ unitTraining missing: use --unit-training or recruit (bridge)", file=sys.stderr)
                sys.exit(1)

            now_ms = int(time.time() * 1000)
            start_ms = now_ms

            if args.arm_type is not None:
                lc_raw = gc(api, token, "GETLASTCONSCRIPTION", f"{args.tile_id} {args.arm_type}")
                lc_ms = _parse_last_conscription_ms(lc_raw)
                if lc_ms is not None:
                    start_ms = max(start_ms, lc_ms)
            else:
                cap = _max_incomplete_due_ms_for_city(queues, args.tile_id)
                if cap is not None:
                    start_ms = max(start_ms, cap)

            item = _build_queue_item(
                args.tile_id,
                args.troop_id,
                args.total,
                ut,
                start_ms,
                args.tz,
            )
            line = json.dumps([item], ensure_ascii=False, separators=(",", ":"))
            out = gc(api, token, "ADDCONSCRIPTIONQUEUE", line)
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    print(humanize(out))


if __name__ == "__main__":
    main()
