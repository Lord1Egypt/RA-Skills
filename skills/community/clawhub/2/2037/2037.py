#!/usr/bin/env python3
"""
Earth2037 Game Skill - 命令行入口
调用 GameSkillAPI 完成 key、注册、登录、apply 等操作。
使用标准库 urllib，无需 pip install。
"""

import json
import os
import sys
import urllib.error
import urllib.request


def load_config(api_base_override=None, lang=None):
    """从 env、config.json 或 apiBaseByLang 读取 apiBase。优先级：api_base_override > EARTH2037_API_BASE > apiBaseByLang[lang] > apiBase"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    api_base = "https://2037cn1.9235.net"
    api_base_by_lang = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                api_base = cfg.get("apiBase", api_base)
                api_base_by_lang = cfg.get("apiBaseByLang") or {}
        except (json.JSONDecodeError, IOError):
            pass

    if api_base_override:
        return api_base_override.rstrip("/")
    env_base = os.environ.get("EARTH2037_API_BASE", "").strip()
    if env_base:
        return env_base.rstrip("/")
    if lang and api_base_by_lang.get(lang):
        return api_base_by_lang[lang].rstrip("/")
    return api_base.rstrip("/")


def http_get(url):
    """GET 请求"""
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post(url, data):
    """POST JSON 请求"""
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_key(api_base):
    """GET /auth/key?skill_id=2037"""
    url = f"{api_base}/auth/key?skill_id=2037"
    try:
        r = http_get(url)
        if r.get("ok") and r.get("key"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print(f"\n✅ key 已获取，长期有效。请保存后用于注册/绑定。")
        else:
            print(json.dumps(r, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def _resolve_tribe_id(t):
    """解析种族；无法识别时返回 None。"""
    if t is None:
        return None
    s = str(t).strip()
    if not s:
        return None
    m = {
        "1": 1,
        "2": 2,
        "3": 3,
        "人类联邦": 1,
        "人类联盟": 1,
        "旭日帝国": 2,
        "鹰之神界": 3,
    }
    if s in m:
        return m[s]
    if s.isdigit():
        v = int(s)
        return v if v in (1, 2, 3) else None
    return None


def _parse_tribe_id(t):
    """解析 tribe_id：1|2|3 或中文种族名；缺省或无法识别时默认 1（兼容旧用法）。"""
    if t is None or str(t).strip() == "":
        return 1
    r = _resolve_tribe_id(t)
    return r if r is not None else 1


def _prompt_tribe_interactive():
    """终端交互选择种族；非 TTY 时退出并提示带参调用。"""
    if not sys.stdin.isatty():
        print("❌ 当前为非交互环境，请一次性指定种族，例如：")
        print("   python3 skills/earth2037-game/2037.py register <用户名> <密码> 1")
        print("   1=人类联盟  2=旭日帝国  3=鹰之神界")
        sys.exit(1)
    print("")
    print("请选择种族（输入 1 / 2 / 3，或完整名称）：")
    print("  1 — 人类联盟")
    print("  2 — 旭日帝国")
    print("  3 — 鹰之神界")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            sys.exit(1)
        tid = _resolve_tribe_id(line)
        if tid is not None:
            return tid
        print("无效输入，请输入 1、2、3 或「人类联盟」「旭日帝国」「鹰之神界」。")


def cmd_register(api_base, username, password, tribe_id=None):
    """POST /auth/register"""
    url = f"{api_base}/auth/register"
    tid = _parse_tribe_id(tribe_id)
    try:
        r = http_post(url, {"username": username, "password": password, "tribe_id": tid})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print(f"\n✅ 注册成功。请将 token 填入 OpenClaw 的 2037 API Key 配置。")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def cmd_recover(api_base, username, password):
    """POST /auth/recover-key — 有账号密码但无 SK-key 时，凭密码找回 API key（skill token）"""
    url = f"{api_base}/auth/recover-key"
    try:
        r = http_post(url, {"username": username, "password": password, "skill_id": "2037"})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print(f"\n✅ 已凭密码找回 key（即 token）。请填入 OpenClaw 的 2037 API Key 配置。")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def cmd_login(api_base, username, password):
    """POST /auth/token"""
    url = f"{api_base}/auth/token"
    try:
        r = http_post(url, {"username": username, "password": password})
        if r.get("ok") and r.get("token"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            print(f"\n✅ 登录成功。请将 token 填入 OpenClaw 的 2037 API Key 配置。")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def cmd_apply(api_base, username, password, key, action="register", tribe_id=None):
    """POST /auth/apply"""
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
            print(f"\n✅ 成功。请将 token 填入 OpenClaw 的 2037 API Key 配置。")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def _get_token():
    """从环境变量或 config.json 读取 token"""
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
    """POST /auth/newkey - 需 Bearer token，生成新 token 并作废旧 token"""
    token = _get_token()
    if not token:
        print("❌ 未找到 token，请先设置 EARTH2037_TOKEN 或 config.json 中的 token/apiKey")
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
            print(f"\n✅ 新 key 已生成，旧 key 已作废。请将新 token 更新到 OpenClaw 的 2037 API Key 配置。")
        else:
            print(json.dumps(r, ensure_ascii=False))
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def cmd_setcity(api_base, tile_id):
    """SETCURCITY 切换当前城并同步 userinfo.json / citys.json"""
    try:
        from cache import humanize_command_output, set_current_city

        ui, cs, raw = set_current_city(tile_id, api_base=api_base)
        cv = ui.get("CurrentVillageID") or ui.get("currentVillageID")
        print("✅ SETCURCITY 已执行，本地缓存已更新")
        print(f"  CurrentVillageID={cv}, CapitalID={ui.get('CapitalID')}")
        print(f"  citys.json: {len(cs)} 座城市")
        if raw.strip():
            print(f"  服端: {humanize_command_output(raw).strip()[:500]}")
    except Exception as e:
        print(f"❌ setcity 失败: {e}")
        sys.exit(1)


def cmd_sync(api_base):
    """同步 userinfo、citys 到本地缓存"""
    try:
        from cache import sync as cache_sync
        ui, cs = cache_sync(api_base=api_base)
        print("✅ 缓存已更新")
        cv = ui.get("CurrentVillageID") or ui.get("currentVillageID")
        print(f"  userinfo.json: userID={ui.get('UserID')}, CapitalID={ui.get('CapitalID')}, CurrentVillageID={cv}")
        print(f"  citys.json: {len(cs)} 座城市")
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        sys.exit(1)


def cmd_bootstrap(api_base):
    """一次请求拉取多路游戏数据，写入 session_cache.json（等价 TCP 登录后连续多条命令）"""
    try:
        from cache import bootstrap as cache_bootstrap
        data = cache_bootstrap(api_base=api_base)
        keys = list(data.keys()) if isinstance(data, dict) else []
        print("✅ 已写入 session_cache.json（整包会话缓存）")
        print(f"  数据键: {', '.join(keys[:15])}{'...' if len(keys) > 15 else ''}")
    except Exception as e:
        print(f"❌ bootstrap 失败: {e}")
        sys.exit(1)


def cmd_show(focus=None):
    """按块打印本地 session_cache.json（不连网）"""
    from cache import show_cache

    sys.exit(show_cache(focus))


def main():
    args = sys.argv[1:]
    api_base_override = None
    lang = None
    while args and args[0].startswith("--"):
        if args[0] == "--api-base" and len(args) > 1:
            api_base_override = args[1]
            args = args[2:]
        elif args[0] == "--lang" and len(args) > 1:
            lang = args[1].lower()
            args = args[2:]
        else:
            args = args[1:]

    if len(args) < 1:
        print("用法: 2037.py [--api-base URL] [--lang zh|en] key | ... | setcity | sync | bootstrap | show [分类]")
        print("  --api-base: 指定 API 地址，覆盖 config.json")
        print("  --lang zh|en: 按语言选默认服务器（需 config.json 中 apiBaseByLang）")
        print("  register: 可先只输入用户名、密码，再在终端选择种族；或一行写完：register 用户 密码 [1|2|3|种族名]")
        print("  种族: 1=人类联盟 2=旭日帝国 3=鹰之神界（OpenClaw 上应先问用户选族再执行 register）")
        print("  recover: 有用户名密码但无 SK-key 时，凭密码找回 API key（skill token）")
        print("  newkey: 换新 key（需 token，旧 key 作废）")
        print("  setcity <tileID>: SETCURCITY 切换当前城并刷新 userinfo.json / citys.json（需 token）")
        print("  sync: 仅 USERINFO+CITYLIST → userinfo.json / citys.json（需 token）")
        print("  bootstrap: 服务端一次合并多路命令 → session_cache.json（需 token，推荐）")
        print("  show: 读本地缓存，打印城市/建筑/军队等（不连网）；分类: city build troops task queue hero goods")
        print("  airinfo: 空投次数（已用/总次数，剩余=总-已用）；airdrop [tileID]: 领取空投（省略则用当前城/主城），需 token")
        print("  另见: build_ops.py（GETBUILDCOST/ADDBUILDQUEUE/取消队列） recruit_ops.py（征兵） march_ops.py chat_ops.py airdrop_ops.py，需 token")
        sys.exit(1)

    api_base = load_config(api_base_override=api_base_override, lang=lang)
    cmd = args[0].lower()

    if cmd == "setcity":
        if len(args) < 2:
            print("用法: 2037.py setcity <tileID>")
            sys.exit(1)
        try:
            tid = int(args[1])
        except ValueError:
            print("❌ tileID 须为整数")
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
            print(f"❌ {e}")
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
                    print("❌ 请指定 tileID：2037.py airdrop <tileID>，或先 sync 写入 userinfo.json")
                    sys.exit(1)
                print(f"(tileID={tid} from userinfo cache)")
            raw, res, ok = airdropres(tid, api_base=api_base)
            print(humanize_command_output(raw).rstrip())
            if res:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            if ok:
                print("✅ getResource 已合并到 session_cache.json（若存在）")
            else:
                sys.exit(1)
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)
    elif cmd == "newkey":
        cmd_newkey(api_base)
    elif cmd == "key":
        cmd_key(api_base)
    elif cmd == "register":
        if len(args) < 3:
            print("用法: 2037.py register <用户名> <密码> [种族]")
            print("  种族: 1 / 2 / 3 或 人类联盟 / 旭日帝国 / 鹰之神界；省略时在终端交互选择（OpenClaw 应先问族别再带参执行）")
            sys.exit(1)
        u, pw = args[1], args[2]
        if len(args) >= 4:
            tribe_token = args[3]
        else:
            tribe_token = _prompt_tribe_interactive()
        cmd_register(api_base, u, pw, tribe_token)
    elif cmd == "recover":
        if len(args) < 3:
            print("用法: 2037.py recover <用户名> <密码>")
            sys.exit(1)
        cmd_recover(api_base, args[1], args[2])
    elif cmd == "login":
        if len(args) < 3:
            print("用法: 2037.py login <用户名> <密码>")
            sys.exit(1)
        cmd_login(api_base, args[1], args[2])
    elif cmd == "apply":
        if len(args) < 4:
            print("用法: 2037.py apply <用户名> <密码> <key> [种族]")
            sys.exit(1)
        tribe_id = args[4] if len(args) > 4 else None
        cmd_apply(api_base, args[1], args[2], args[3], tribe_id=tribe_id)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
