#!/usr/bin/env python3
"""
建筑升级 — 与游戏内一致：只有 GETBUILDCOST（查价）与 ADDBUILDQUEUE（入队），无独立「升级」命令。

用法示例：
  python3 build_ops.py getbuildcost "8:3,2"
  python3 build_ops.py getbuildcost "8 3"
  python3 build_ops.py addbuildqueue '{"buildAction":1,"buildID":8,...}'
  python3 build_ops.py compose --tile 273897 --point 27 --build 8 --level 3
  python3 build_ops.py cancel-queue 273897 27

说明：少数 HTTP 网关（如本仓库 GameSkillAPI）会把 UPGRADE_OIL 等简写转成 ADDBUILDQUEUE，那是网关扩展，不是游戏 TCP 原生命令。
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
    """从 /svr <cmd> <json> 中取出 JSON。"""
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


def _net_date_ms(ms: int, tz: str = "+0800") -> str:
    return f"/Date({int(ms)}{tz})/"


def main():
    gc, get_token, load_cfg, humanize = _import_game()
    ap = argparse.ArgumentParser(
        description="Earth2037 建造队列：GETBUILDCOST + ADDBUILDQUEUE（与 /getbuildcost、/addbuildqueue 一致）"
    )
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_cost = sub.add_parser("getbuildcost", help='查建造成本。args 形如 "8:3,2"（多等级）或 "8 3"（buildID + 单等级）')
    p_cost.add_argument("parms", help='例如 8:3,2 或 "8 3"')

    p_add = sub.add_parser("addbuildqueue", help="入队建造/升级，args 为单行 JSON（与客户端 addbuildqueue 一致）")
    p_add.add_argument("json", help="JSON 一行，或 @文件路径 从文件读入")

    p_comp = sub.add_parser(
        "compose",
        help="先 GETBUILDCOST 取 TrainingTime，再组 ADDBUILDQUEUE（buildAction=1）",
    )
    p_comp.add_argument("--tile", type=int, required=True, dest="tile_id")
    p_comp.add_argument("--point", type=int, required=True, dest="point_id")
    p_comp.add_argument("--build", type=int, required=True, dest="build_id")
    p_comp.add_argument("--level", type=int, required=True, help="目标等级（升级后的 level）")
    p_comp.add_argument("--tz", default="+0800", help="dueTime 时区后缀，默认 +0800")

    p_ca = sub.add_parser("cancel-queue", help="取消队列 CANCELBUILDQUEUE")
    p_ca.add_argument("tile_id", type=int)
    p_ca.add_argument("point_id", type=int)

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("❌ 需要 EARTH2037_TOKEN 或 config.json token", file=sys.stderr)
        sys.exit(1)

    try:
        if args.cmd == "getbuildcost":
            out = gc(api, token, "GETBUILDCOST", args.parms.strip())
        elif args.cmd == "cancel-queue":
            out = gc(api, token, "CANCELBUILDQUEUE", f"{args.tile_id} {args.point_id}")
        elif args.cmd == "addbuildqueue":
            js = args.json
            if js.startswith("@"):
                path = js[1:].strip()
                with open(path, "r", encoding="utf-8") as f:
                    js = f.read().strip()
            elif js == "-":
                js = sys.stdin.read().strip()
            out = gc(api, token, "ADDBUILDQUEUE", js)
        else:
            # compose
            bid, lv = args.build_id, args.level
            cost_raw = gc(api, token, "GETBUILDCOST", f"{bid}:{lv}")
            data = _parse_svr_payload(cost_raw, "getbuildcost")
            if data is None:
                print(f"❌ 无法解析 getbuildcost 返回：{cost_raw!r}", file=sys.stderr)
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
                print(f"❌ 未找到 TrainingTime：{data!r}", file=sys.stderr)
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
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    print(humanize(out))


if __name__ == "__main__":
    main()
