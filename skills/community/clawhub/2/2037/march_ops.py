#!/usr/bin/env python3
"""
出征 / 打野 — 通过 GameSkillAPI 调用 ADDCOMBATQUEUE。
打野目标为绿洲（FieldType=0）时常用 marchType=256（AttackWilderness）。
粮耗 upkeep 可由服务端校验；脚本可先粗略填 0 或由你传入。
"""
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
    """
    spec: "43:35" -> "43:35_0_0_0"；已是 "43:35_0_0_0" 则原样；
    多段用 | 连接: "43:35|44:10"
    """
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
    ap = argparse.ArgumentParser(description="Earth2037 出征（HTTP ADDCOMBATQUEUE）")
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)

    sub = ap.add_subparsers(dest="mode", required=True)
    p_w = sub.add_parser("attack-oasis", help="打野：marchType=256，目标 tile 为绿洲")
    p_w.add_argument("--from", dest="from_city", type=int, required=True)
    p_w.add_argument("--to", dest="to_city", type=int, required=True)
    p_w.add_argument("--troops", required=True, help="如 43:35 或 43:35_0_0_0，多种用 |")
    p_w.add_argument("--march-type", type=int, default=256, help="默认 256=打野")
    p_w.add_argument("--hero", type=int, default=0)
    p_w.add_argument("--upkeep", type=int, default=0)
    p_w.add_argument("--in-seconds", type=int, default=120, help="到达时间=现在+秒数（粗算，仍可能被服端校正）")
    p_w.add_argument("--resources", default="0|0|0|0")

    p_j = sub.add_parser("raw-json", help="args 整段为 CombatQueue JSON")
    p_j.add_argument("json_one_line")

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("❌ 需要 EARTH2037_TOKEN 或 config.json token", file=sys.stderr)
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
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    print(humanize(out))


if __name__ == "__main__":
    main()
