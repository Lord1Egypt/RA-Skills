#!/usr/bin/env python3
"""
世界频道 / 联盟频道 — GETWMSGS、GETALLYCHAT、SENDWMSG、SENDALLYMSG。
发送消息时从 userinfo.json（需先 sync/bootstrap）读取 userID、username、allianceID；可用参数覆盖。
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


def _net_date_ms_now(offset: str = "+0800") -> str:
    ms = int(time.time() * 1000)
    return f"/Date({ms}{offset})/"


def _load_userinfo(skill_dir: dict) -> dict:
    path = os.path.join(skill_dir, "userinfo.json")
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def main():
    gc, get_token, load_cfg, humanize = _import_game()
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Earth2037 聊天（HTTP game/command）")
    ap.add_argument("--api-base", dest="api_base", default=os.environ.get("EARTH2037_API_BASE", "").strip() or None)

    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("world-msgs", help="世界聊天拉取 /getwmsgs；参数为起始消息 ID（新消息从 0 拉）")
    p1.add_argument("from_id", nargs="?", type=int, default=0)

    p2 = sub.add_parser("ally-chat", help="联盟聊天；参数为游标（示例 0）")
    p2.add_argument("cursor", nargs="?", type=int, default=0)

    p3 = sub.add_parser("send-world", help="发世界消息（type=2）")
    p3.add_argument("text")
    p3.add_argument("--user-id", type=int, default=0)
    p3.add_argument("--username", default="")
    p3.add_argument("--layout-id", type=int, default=2131558440)

    p4 = sub.add_parser("send-ally", help="发联盟消息（type=1）")
    p4.add_argument("text")
    p4.add_argument("--alliance-id", type=int, default=0)
    p4.add_argument("--user-id", type=int, default=0)
    p4.add_argument("--username", default="")
    p4.add_argument("--layout-id", type=int, default=2131558439)

    args = ap.parse_args()
    api = (args.api_base or load_cfg()).rstrip("/")
    token = get_token()
    if not token:
        print("❌ 需要 EARTH2037_TOKEN 或 config.json token", file=sys.stderr)
        sys.exit(1)

    ui = _load_userinfo(skill_dir)
    uid = ui.get("UserID") or ui.get("userID") or 0
    uname = (ui.get("Username") or ui.get("username") or "").strip()
    ally = ui.get("AllianceID") or ui.get("allyID") or ui.get("AllianceId") or 0

    try:
        if args.cmd == "world-msgs":
            out = gc(api, token, "GETWMSGS", str(args.from_id))
        elif args.cmd == "ally-chat":
            out = gc(api, token, "GETALLYCHAT", str(args.cursor))
        elif args.cmd == "send-world":
            u = args.user_id or int(uid) if uid else 0
            n = args.username or uname
            msg = {
                "content": args.text,
                "contentFormat": 0,
                "contentMetadata": None,
                "id": 0,
                "layoutID": args.layout_id,
                "payloads": [],
                "received": _net_date_ms_now(),
                "type": 2,
                "userID": u,
                "username": n,
            }
            out = gc(api, token, "SENDWMSG", json.dumps(msg, ensure_ascii=False, separators=(",", ":")))
        else:
            aid = args.alliance_id or int(ally) if ally else 0
            if aid <= 0:
                print("❌ 缺少联盟 ID：先 sync 写入 userinfo.json，或传 --alliance-id", file=sys.stderr)
                sys.exit(1)
            u = args.user_id or int(uid) if uid else 0
            n = args.username or uname
            msg = {
                "allianceID": aid,
                "content": args.text,
                "contentFormat": 0,
                "contentMetadata": None,
                "id": 0,
                "layoutID": args.layout_id,
                "payloads": [],
                "received": _net_date_ms_now(),
                "type": 1,
                "userID": u,
                "username": n,
            }
            out = gc(api, token, "SENDALLYMSG", json.dumps(msg, ensure_ascii=False, separators=(",", ":")))
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    print(humanize(out))


if __name__ == "__main__":
    main()
