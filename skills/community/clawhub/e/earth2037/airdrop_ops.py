#!/usr/bin/env python3
"""Air supply: AIRINFO / AIRDROPRES (same as client /airinfo, /airdropres)."""

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
    for cmd, payload in parse_svr_lines(data):
        if cmd == "airdropres" and payload.strip().lower() == "ok":
            return True
    return False


def airinfo(api_base=None, token=None):
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("Token required: EARTH2037_TOKEN or config.json")
    raw = _game_command(api_base, token, "AIRINFO", "")
    return raw, parse_airinfo_counts(raw)


def airdropres(tile_id, api_base=None, token=None, update_cache=True):
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("Token required: EARTH2037_TOKEN or config.json")
    tid = int(tile_id)
    raw = _game_command(api_base, token, "AIRDROPRES", str(tid))
    res = extract_getresource_json(raw)
    ok = airdrop_success(raw) and res is not None
    if update_cache and ok:
        apply_getresource_from_command_to_session_cache(raw)
    return raw, res, ok


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 airdrop_ops.py airinfo | airdrop [tileID]")
        sys.exit(1)
    sub = sys.argv[1].lower()
    api_base = _load_config()
    token = _get_token()
    if not token:
        print("Token required", file=sys.stderr)
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
                print("No tileID and no userinfo cache", file=sys.stderr)
                sys.exit(1)
            print(f"(tileID={tid} from cache)")
        raw, res, ok = airdropres(tid, api_base=api_base, token=token)
        print(humanize_command_output(raw).rstrip())
        if ok:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
