#!/usr/bin/env python3
"""
Earth2037 Game Skill - CLI entry (English)
Calls GameSkillAPI for key, register, login, apply. Uses stdlib urllib, no pip install.
"""

import json
import os
import sys
import urllib.error
import urllib.request


def load_config(api_base_override=None):
    """Read apiBase from env, config.json. Priority: api_base_override > EARTH2037_API_BASE > apiBase"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    api_base = "https://2037en1.9235.net"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                api_base = cfg.get("apiBase", api_base)
        except (json.JSONDecodeError, IOError):
            pass

    if api_base_override:
        return api_base_override.rstrip("/")
    env_base = os.environ.get("EARTH2037_API_BASE", "").strip()
    if env_base:
        return env_base.rstrip("/")
    return api_base.rstrip("/")


def http_get(url):
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post(url, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_key(api_base):
    url = f"{api_base}/auth/key?skill_id=2037"
    try:
        r = http_get(url)
        if r.get("ok") and r.get("key"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nKey obtained. Long-term valid. Save for register/bind.")
        else:
            print(json.dumps(r, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def _resolve_tribe_id(t):
    if t is None:
        return None
    s = str(t).strip()
    if not s:
        return None
    m = {
        "1": 1,
        "2": 2,
        "3": 3,
        "human": 1,
        "empire": 2,
        "eagle": 3,
        "人类联邦": 1,
        "人类联盟": 1,
        "旭日帝国": 2,
        "鹰之神界": 3,
    }
    low = s.lower()
    if low in m:
        return m[low]
    if s in m:
        return m[s]
    if s.isdigit():
        v = int(s)
        return v if v in (1, 2, 3) else None
    return None


def _parse_tribe_id(t):
    if t is None or str(t).strip() == "":
        return 1
    r = _resolve_tribe_id(t)
    return r if r is not None else 1


def _prompt_tribe_interactive():
    if not sys.stdin.isatty():
        print("Non-interactive: pass tribe as last arg, e.g. register <user> <pass> 1")
        print("  1=Human Federation  2=Empire  3=Eagle")
        sys.exit(1)
    print("")
    print("Choose tribe (1 / 2 / 3 or name):")
    print("  1 — Human Federation")
    print("  2 — Empire of the Rising Sun")
    print("  3 — Eagle's Realm")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            sys.exit(1)
        tid = _resolve_tribe_id(line)
        if tid is not None:
            return tid
        print("Invalid. Enter 1, 2, 3 or full tribe name.")


def cmd_register(api_base, username, password, tribe_id=None):
    url = f"{api_base}/auth/register"
    tid = _parse_tribe_id(tribe_id)
    try:
        r = http_post(url, {"username": username, "password": password, "tribe_id": tid})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nRegistered. Put token in OpenClaw 2037 API Key config.")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def cmd_recover(api_base, username, password):
    """POST /auth/recover-key — recover API key (skill token) with username/password when no SK-key"""
    url = f"{api_base}/auth/recover-key"
    try:
        r = http_post(url, {"username": username, "password": password, "skill_id": "2037"})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nKey recovered. Put token in OpenClaw 2037 API Key config.")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def cmd_login(api_base, username, password):
    url = f"{api_base}/auth/token"
    try:
        r = http_post(url, {"username": username, "password": password})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nLogged in. Put token in OpenClaw 2037 API Key config.")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def cmd_apply(api_base, username, password, key, action="register", tribe_id=None):
    url = f"{api_base}/auth/apply"
    tid = _parse_tribe_id(tribe_id)
    try:
        r = http_post(
            url,
            {
                "username": username,
                "password": password,
                "action": action,
                "key": key,
                "skill_id": "2037",
                "tribe_id": tid,
            },
        )
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nDone. Put token in OpenClaw 2037 API Key config.")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def _get_token():
    token = os.environ.get("EARTH2037_TOKEN", "").strip()
    if token:
        return token
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return (cfg.get("token") or cfg.get("apiKey") or "").strip()
        except (json.JSONDecodeError, IOError):
            pass
    return ""


def cmd_newkey(api_base):
    token = _get_token()
    if not token:
        print("No token. Set EARTH2037_TOKEN or token/apiKey in config.json")
        sys.exit(1)
    url = f"{api_base}/auth/newkey"
    body = json.dumps({"skill_id": "2037"}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            r = json.loads(resp.read().decode("utf-8"))
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print("\nNew key generated. Old key invalid. Update OpenClaw 2037 API Key config.")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def cmd_setcity(api_base, tile_id):
    try:
        from cache import humanize_command_output, set_current_city

        ui, cs, raw = set_current_city(tile_id, api_base=api_base)
        cv = ui.get("CurrentVillageID") or ui.get("currentVillageID")
        print("SETCURCITY ok, cache updated")
        print(f"  CurrentVillageID={cv}, CapitalID={ui.get('CapitalID')}")
        print(f"  citys.json: {len(cs)} cities")
        if raw.strip():
            print(f"  server: {humanize_command_output(raw).strip()[:500]}")
    except Exception as e:
        print(f"setcity failed: {e}")
        sys.exit(1)


def cmd_sync(api_base):
    try:
        from cache import sync as cache_sync
        ui, cs = cache_sync(api_base=api_base)
        print("Cache updated")
        cv = ui.get("CurrentVillageID") or ui.get("currentVillageID")
        print(f"  userinfo.json: userID={ui.get('UserID')}, CapitalID={ui.get('CapitalID')}, CurrentVillageID={cv}")
        print(f"  citys.json: {len(cs)} cities")
    except Exception as e:
        print(f"Sync failed: {e}")
        sys.exit(1)


def cmd_bootstrap(api_base):
    try:
        from cache import bootstrap as cache_bootstrap
        data = cache_bootstrap(api_base=api_base)
        keys = list(data.keys()) if isinstance(data, dict) else []
        print("Wrote session_cache.json")
        print(f"  keys: {', '.join(keys[:15])}{'...' if len(keys) > 15 else ''}")
    except Exception as e:
        print(f"Bootstrap failed: {e}")
        sys.exit(1)


def cmd_show(focus=None):
    from cache import show_cache

    sys.exit(show_cache(focus))


def main():
    args = sys.argv[1:]
    api_base_override = None
    while args and args[0].startswith("--"):
        if args[0] == "--api-base" and len(args) > 1:
            api_base_override = args[1]
            args = args[2:]
        else:
            args = args[1:]

    if len(args) < 1:
        print("Usage: 2037.py [--api-base URL] key | ... | setcity | sync | bootstrap | show [focus]")
        print("  recover: username+password to recover API key (skill token) without SK-key")
        print("  setcity <tileID>: SETCURCITY then refresh userinfo.json / citys.json (needs token)")
        print("  sync: USERINFO+CITYLIST only; bootstrap: full session JSON → session_cache.json")
        print("  show: print local session_cache (no HTTP); focus: city build troops task queue hero goods")
        print("  airinfo: air supply quota (used,total); airdrop [tileID]: claim (omit tileID = current/capital from cache)")
        print("  Also: build_ops.py, recruit_ops.py, march_ops.py, chat_ops.py, airdrop_ops.py (require token)")
        print("  register: optional tribe on same line, or interactive prompt if omitted (TTY only)")
        sys.exit(1)

    api_base = load_config(api_base_override=api_base_override)
    cmd = args[0].lower()

    if cmd == "setcity":
        if len(args) < 2:
            print("Usage: 2037.py setcity <tileID>")
            sys.exit(1)
        try:
            tid = int(args[1])
        except ValueError:
            print("tileID must be an integer")
            sys.exit(1)
        cmd_setcity(api_base, tid)
    elif cmd == "sync":
        cmd_sync(api_base)
    elif cmd == "show":
        focus = args[1] if len(args) > 1 else None
        cmd_show(focus)
    elif cmd == "bootstrap":
        cmd_bootstrap(api_base)
    elif cmd == "airinfo":
        try:
            from cache import humanize_command_output
            from airdrop_ops import airinfo as do_airinfo

            raw, counts = do_airinfo(api_base=api_base)
            print(humanize_command_output(raw).rstrip())
            if counts:
                u, t = counts
                print(f"remaining={t - u} (used={u}, total={t})")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif cmd == "airdrop":
        try:
            from cache import humanize_command_output
            from airdrop_ops import airdropres, get_current_village_id

            tid = None
            if len(args) > 1:
                tid = int(args[1])
            else:
                tid = get_current_village_id()
                if tid is None:
                    print("Specify tileID: 2037.py airdrop <tileID> or run sync for userinfo.json")
                    sys.exit(1)
                print(f"(tileID={tid} from userinfo cache)")
            raw, res, ok = airdropres(tid, api_base=api_base)
            print(humanize_command_output(raw).rstrip())
            if res:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            if ok:
                print("Merged getResource into session_cache.json if present")
            else:
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif cmd == "newkey":
        cmd_newkey(api_base)
    elif cmd == "key":
        cmd_key(api_base)
    elif cmd == "register":
        if len(args) < 3:
            print("Usage: 2037.py register <username> <password> [tribe]")
            sys.exit(1)
        u, pw = args[1], args[2]
        if len(args) >= 4:
            tribe_token = args[3]
        else:
            tribe_token = _prompt_tribe_interactive()
        cmd_register(api_base, u, pw, tribe_token)
    elif cmd == "recover":
        if len(args) < 3:
            print("Usage: 2037.py recover <username> <password>")
            sys.exit(1)
        cmd_recover(api_base, args[1], args[2])
    elif cmd == "login":
        if len(args) < 3:
            print("Usage: 2037.py login <username> <password>")
            sys.exit(1)
        cmd_login(api_base, args[1], args[2])
    elif cmd == "apply":
        if len(args) < 4:
            print("Usage: 2037.py apply <username> <password> <key> [tribe]")
            sys.exit(1)
        tribe_id = args[4] if len(args) > 4 else None
        cmd_apply(api_base, args[1], args[2], args[3], tribe_id=tribe_id)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
