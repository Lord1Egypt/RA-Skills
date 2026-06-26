#!/usr/bin/env python3
"""
空投：与客户端 /airinfo、/airdropres 一致。
AIRDROPRES 成功时服务端连续返回两行：/svr getResource {...}、/svr airdropres ok（GameSkillAPI 将整段作为一条 data 字符串返回，见 SKILL.md）。
"""

import json
import sys

from cache import (
    _game_command,
    _load_config,
    _get_token,
    parse_svr_lines,
    extract_getresource_json,
    apply_getresource_from_command_to_session_cache,
    get_current_village_id,
    humanize_command_output,
)


def parse_airinfo_counts(data):
    """
    解析 /svr airinfo 已用,总次数 → (used, total)；失败或 err 行返回 None。
    """
    if not data:
        return None
    for cmd, payload in parse_svr_lines(data):
        if cmd != "airinfo":
            continue
        pl = payload.strip()
        if pl.lower().startswith("err"):
            return None
        parts = pl.split(",")
        if len(parts) >= 2:
            try:
                return int(parts[0].strip()), int(parts[1].strip())
            except ValueError:
                pass
    return None


def airdrop_success(data):
    """是否含 /svr airdropres ok。"""
    for cmd, payload in parse_svr_lines(data):
        if cmd == "airdropres" and payload.strip().lower() == "ok":
            return True
    return False


def airinfo(api_base=None, token=None):
    """POST AIRINFO，返回 (原始 data 字符串, (used,total) 或 None)。"""
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("需要 token：EARTH2037_TOKEN 或 config.json")
    raw = _game_command(api_base, token, "AIRINFO", "")
    return raw, parse_airinfo_counts(raw)


def airdropres(tile_id, api_base=None, token=None, update_cache=True):
    """
    POST AIRDROPRES tileID。成功时合并 getResource 到 session_cache.json（若存在）。
    返回 (原始 data, getResource 对象或 None, 是否成功)。
    """
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("需要 token：EARTH2037_TOKEN 或 config.json")
    tid = int(tile_id)
    raw = _game_command(api_base, token, "AIRDROPRES", str(tid))
    res = extract_getresource_json(raw)
    ok = airdrop_success(raw) and res is not None
    if update_cache and ok:
        apply_getresource_from_command_to_session_cache(raw)
    return raw, res, ok


def main():
    if len(sys.argv) < 2:
        print("用法: python3 airdrop_ops.py airinfo | airdrop [tileID]")
        print("  airinfo: 查询空投已用/总次数（剩余=总-已用）")
        print("  airdrop: 领取空投；省略 tileID 时用 userinfo 当前城/主城")
        sys.exit(1)
    sub = sys.argv[1].lower()
    api_base = _load_config()
    token = _get_token()
    if not token:
        print("❌ 需要 token", file=sys.stderr)
        sys.exit(1)
    if sub == "airinfo":
        raw, counts = airinfo(api_base=api_base, token=token)
        print(humanize_command_output(raw).rstrip())
        if counts:
            u, t = counts
            print(f"remaining={t - u} (used={u}, total={t})")
    elif sub == "airdrop":
        tid = sys.argv[2] if len(sys.argv) > 2 else None
        if tid is None:
            tid = get_current_village_id()
            if tid is None:
                print("❌ 无 tileID 且无法从 userinfo.json 读取当前城/主城", file=sys.stderr)
                sys.exit(1)
            print(f"(tileID={tid} from cache)")
        raw, res, ok = airdropres(tid, api_base=api_base, token=token)
        print(humanize_command_output(raw).rstrip())
        if ok:
            print(json.dumps(res, ensure_ascii=False, indent=2))
            print("✅ 已写入 session_cache.json（getresource_last / resource_by_tile）")
        else:
            sys.exit(1)
    else:
        print("未知子命令", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
