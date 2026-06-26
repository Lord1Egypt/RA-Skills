#!/usr/bin/env python3
"""
Earth2037 本地缓存：拉取 userinfo、citys 等数据到本地 JSON，便于映射（主城 tileID、城市名等）。
需 token 认证。执行 2037.py sync 触发同步。
"""

import json
import os
import re
import sys

# 与 2037.py 共用 config
def _load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    api_base = "https://2037cn1.9235.net"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                api_base = cfg.get("apiBase", api_base)
        except (json.JSONDecodeError, IOError):
            pass
    return api_base.rstrip("/")


def _get_token():
    """从环境变量或 config 获取 token"""
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


def _auth_401_hint(token):
    t = (token or "").strip()
    if t.upper().startswith("SK-"):
        return "「SK-」开头的是注册/绑定用 key，不能当 Bearer。请执行 2037.py login 用户名 密码，或 curl POST /auth/token，使用返回的 token。"
    return "请检查 EARTH2037_TOKEN：应用 2037.py login 或 POST /auth/token、/auth/apply 返回的长 token（32 位十六进制），不是 SK- key。"


def _post_bootstrap(api_base, token):
    """POST /game/bootstrap，返回合并后的 data 对象"""
    import urllib.request
    import urllib.error
    url = f"{api_base}/game/bootstrap"
    body = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise RuntimeError("HTTP 401 Unauthorized。 " + _auth_401_hint(token)) from e
        raise
    with resp:
        r = json.loads(resp.read().decode("utf-8"))
    if not r.get("ok"):
        raise RuntimeError(r.get("err", "bootstrap failed"))
    return r.get("data")


def _game_command(api_base, token, cmd, args=""):
    """POST /game/command，返回 data 字符串（如 /svr citylist {...}）"""
    import urllib.request
    import urllib.error
    url = f"{api_base}/game/command"
    body = json.dumps({"cmd": cmd, "args": args or ""}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise RuntimeError("HTTP 401 Unauthorized。 " + _auth_401_hint(token)) from e
        raise
    with resp:
        r = json.loads(resp.read().decode("utf-8"))
    if not r.get("ok"):
        raise RuntimeError(r.get("err", "unknown error"))
    return r.get("data") or ""


def parse_svr_lines(data):
    """
    将 POST /game/command 返回的多行文本拆成 (cmd 小写, payload 字符串)。
    例：/svr getResource {...} 与 /svr airdropres ok 各占一行。
    """
    out = []
    if not data or not isinstance(data, str):
        return out
    for line in data.strip().splitlines():
        line = line.strip()
        if not line.lower().startswith("/svr"):
            continue
        rest = line[4:].lstrip()
        parts = rest.split(None, 1)
        cmd = (parts[0] or "").lower()
        payload = parts[1] if len(parts) > 1 else ""
        out.append((cmd, payload))
    return out


def extract_getresource_json(data):
    """从多行或单行响应中解析第一条 /svr getResource 后的 JSON 对象。"""
    for cmd, payload in parse_svr_lines(data):
        if cmd != "getresource":
            continue
        pl = payload.strip()
        if pl.startswith("{") or pl.startswith("["):
            try:
                return json.loads(pl)
            except json.JSONDecodeError:
                pass
    return _parse_svr_json(data, "getResource")


def extract_all_getresource_jsons(data):
    """解析响应中每一行 /svr getResource 的 JSON（collect_all 可能多行）。"""
    out = []
    for cmd, payload in parse_svr_lines(data):
        if cmd != "getresource":
            continue
        pl = payload.strip()
        if pl.startswith("{") or pl.startswith("["):
            try:
                j = json.loads(pl)
                if isinstance(j, dict):
                    out.append(j)
            except json.JSONDecodeError:
                pass
    if not out:
        one = extract_getresource_json(data)
        if one and isinstance(one, dict):
            out.append(one)
    return out


def apply_getresource_from_command_to_session_cache(data):
    """
    从命令返回文本中提取 getResource（可多行），若存在 session_cache.json 则合并：
    getresource_last（最后一行）、resource_by_tile[tileID]（各行合并）。
    """
    resources = extract_all_getresource_jsons(data)
    if not resources:
        return False
    path = os.path.join(_cache_dir(), "session_cache.json")
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            sc = json.load(f)
    except (IOError, json.JSONDecodeError):
        return False
    if not isinstance(sc, dict):
        return False
    by = sc.get("resource_by_tile")
    if not isinstance(by, dict):
        by = {}
    for res in resources:
        tid = res.get("tileID")
        if tid is not None:
            by[str(tid)] = res
    sc["resource_by_tile"] = by
    sc["getresource_last"] = resources[-1]
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sc, f, ensure_ascii=False, indent=2)
    except IOError:
        return False
    return True


def extract_getaccount_json(data):
    """解析 /svr getaccount {json}（单行）。"""
    for cmd, payload in parse_svr_lines(data):
        if cmd != "getaccount":
            continue
        pl = payload.strip()
        if pl.startswith("{"):
            try:
                return json.loads(pl)
            except json.JSONDecodeError:
                pass
    if not data or not isinstance(data, str):
        return None
    pat = re.compile(r"^/svr\s+getaccount\s+(.+)$", re.IGNORECASE | re.DOTALL)
    m = pat.match(data.strip())
    if not m:
        return None
    raw = m.group(1).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def apply_account_to_userinfo_dict(userinfo, account_obj):
    """将 GETACCOUNT 的 JSON 并入 userinfo 字典：account、goldCoinsTotal = pie + amount。"""
    if not userinfo or not isinstance(userinfo, dict):
        userinfo = {}
    if not account_obj or not isinstance(account_obj, dict):
        return userinfo
    userinfo["account"] = account_obj
    try:
        pie = int(account_obj.get("pie") or 0)
        amt = int(account_obj.get("amount") or 0)
        userinfo["goldCoinsTotal"] = pie + amt
    except (TypeError, ValueError):
        pass
    return userinfo


def _parse_svr_json(data, prefix):
    """从 /svr cmd {json} 或 /svr cmd json 提取 JSON 字符串（单行；多行请用 extract_getresource_json）"""
    if not data or not isinstance(data, str):
        return None
    # 格式: /svr citylist [{...}] 或 /svr userinfo {...}
    pat = re.compile(r"^/svr\s+" + re.escape(prefix) + r"\s+(.+)$", re.IGNORECASE)
    m = pat.match(data.strip())
    if not m:
        return None
    raw = m.group(1).strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _cache_dir():
    """缓存文件所在目录（skill 根目录）"""
    return os.path.dirname(os.path.abspath(__file__))


def sync(api_base=None, token=None):
    """
    拉取 CURRENTUSER、USERINFO、CITYLIST，写入 userinfo.json、citys.json。
    返回 (userinfo, citys) 或抛出异常。
    """
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("需要 token：设置环境变量 EARTH2037_TOKEN 或在 config.json 中配置 token/apiKey")

    # 1. USERINFO（当前用户详情，含 CapitalID）
    raw_user = _game_command(api_base, token, "USERINFO", "")
    userinfo = _parse_svr_json(raw_user, "userinfo")
    if userinfo is None:
        raise RuntimeError("USERINFO 解析失败: " + (raw_user[:200] if raw_user else "无返回"))

    # 1b. GETACCOUNT（充值/系统赠送金币等，并入 userinfo.json）
    try:
        raw_acc = _game_command(api_base, token, "GETACCOUNT", "")
        acc = extract_getaccount_json(raw_acc)
        if acc:
            userinfo = apply_account_to_userinfo_dict(userinfo, acc)
    except Exception:
        pass

    # 2. CITYLIST（城市列表）
    raw_city = _game_command(api_base, token, "CITYLIST", "")
    citys = _parse_svr_json(raw_city, "citylist")
    if citys is None:
        citys = []  # 可能为空数组
    if not isinstance(citys, list):
        citys = [citys] if citys else []

    # 写入本地
    cache_dir = _cache_dir()
    userinfo_path = os.path.join(cache_dir, "userinfo.json")
    citys_path = os.path.join(cache_dir, "citys.json")

    with open(userinfo_path, "w", encoding="utf-8") as f:
        json.dump(userinfo, f, ensure_ascii=False, indent=2)

    with open(citys_path, "w", encoding="utf-8") as f:
        json.dump(citys, f, ensure_ascii=False, indent=2)

    return userinfo, citys


def set_current_city(tile_id, api_base=None, token=None):
    """
    发送 SETCURCITY（与客户端 /setcurcity <tileID> 一致），成功后立即 sync() 更新 userinfo.json / citys.json，
    使本地 CurrentVillageID 与服务器一致。
    返回 (userinfo, citys, raw_line)。
    """
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("需要 token：设置环境变量 EARTH2037_TOKEN 或在 config.json 中配置 token/apiKey")
    tid = int(tile_id)
    raw = _game_command(api_base, token, "SETCURCITY", str(tid))
    ui, cs = sync(api_base=api_base, token=token)
    return ui, cs, raw


def bootstrap(api_base=None, token=None):
    """
    登录后一次性拉取多路数据（等价 TCP 连续多条命令），写入 session_cache.json。
    仍会从 data 中提取 userinfo、citylist 写入 userinfo.json、citys.json（若存在）。
    """
    api_base = api_base or _load_config()
    token = token or _get_token()
    if not token:
        raise ValueError("需要 token：设置环境变量 EARTH2037_TOKEN 或在 config.json 中配置 token/apiKey")

    data = _post_bootstrap(api_base, token)
    cache_dir = _cache_dir()
    path = os.path.join(cache_dir, "session_cache.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    ui = None
    cs = None
    if isinstance(data, dict):
        ui_raw = data.get("userinfo")
        if isinstance(ui_raw, dict):
            ui = ui_raw
        elif isinstance(ui_raw, str):
            try:
                ui = json.loads(ui_raw)
            except (json.JSONDecodeError, TypeError):
                pass
        cl_raw = data.get("citylist")
        if isinstance(cl_raw, list):
            cs = cl_raw
        elif isinstance(cl_raw, str):
            try:
                cs = json.loads(cl_raw)
            except (json.JSONDecodeError, TypeError):
                pass
    if ui:
        with open(os.path.join(cache_dir, "userinfo.json"), "w", encoding="utf-8") as f:
            json.dump(ui, f, ensure_ascii=False, indent=2)
    if cs is not None:
        if not isinstance(cs, list):
            cs = [cs] if cs else []
        with open(os.path.join(cache_dir, "citys.json"), "w", encoding="utf-8") as f:
            json.dump(cs, f, ensure_ascii=False, indent=2)

    return data


def load_session_cache():
    """读取 session_cache.json，无则 None"""
    path = os.path.join(_cache_dir(), "session_cache.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# bootstrap 键顺序与 SessionBootstrapService 一致，供 show 打印
_CACHE_SECTIONS = [
    ("userinfo", "【账号】"),
    ("citylist", "【城市】"),
    ("citybuildlist", "【各城建筑】"),
    ("buildlist", "【建筑类型】"),
    ("getbuildcosts2", "【建造消耗】"),
    ("getuserbuildqueue", "【建造队列】"),
    ("getcitytroops", "【城内驻军】"),
    ("gettasklist", "【任务】"),
    ("getconscriptionqueue", "【征兵队列】"),
    ("usertroopssciencequeue", "【兵种科技队列】"),
    ("armies", "【兵种】"),
    ("usercitymilitarysciences", "【城市军事科技】"),
    ("getoutput", "【产出】"),
    ("userheros", "【英雄】"),
    ("goodslist", "【物品目录】"),
    ("usergoodslist", "【背包】"),
    ("combatqueue", "【出征队列】"),
    ("nm", "【nm】"),
    ("airinfo", "【空袭信息】"),
]

# show 子集：python3 cache.py show city | build | troops | task | queue | hero | goods
_CACHE_FOCUS = {
    "city": {"citylist"},
    "cities": {"citylist"},
    "build": {"citybuildlist", "buildlist", "getbuildcosts2", "getuserbuildqueue"},
    "troops": {"armies", "getcitytroops", "usercitymilitarysciences"},
    "military": {"armies", "getcitytroops", "usercitymilitarysciences"},
    "task": {"gettasklist"},
    "queue": {"getuserbuildqueue", "getconscriptionqueue", "combatqueue", "usertroopssciencequeue"},
    "hero": {"userheros"},
    "goods": {"goodslist", "usergoodslist"},
}


def show_cache(focus=None):
    """
    将 session_cache.json 按块打印到 stdout，便于终端阅读。
    focus: None / all / city / build / troops / task / queue / hero / goods
    返回 0 成功，1 无缓存或未知 focus。
    """
    data = load_session_cache()
    if not data:
        print("无 session_cache.json。请先执行: python3 2037.py bootstrap", file=sys.stderr)
        return 1

    fkey = (focus or "all").strip().lower()
    allowed = None
    if fkey not in ("", "all", "a"):
        allowed = _CACHE_FOCUS.get(fkey)
        if allowed is None:
            print(
                "未知分类。可用: all city build troops task queue hero goods",
                file=sys.stderr,
            )
            return 1

    printed = False
    for key, title in _CACHE_SECTIONS:
        if key not in data:
            continue
        if allowed is not None and key not in allowed:
            continue
        printed = True
        print(title)
        print(json.dumps(data[key], ensure_ascii=False, indent=2))
        print()

    for mk in ("_meta", "_errors"):
        if mk in data and (allowed is None or mk == "_meta"):
            print(f"【{mk}】")
            print(json.dumps(data[mk], ensure_ascii=False, indent=2))
            print()

    if not printed and allowed is not None:
        print("(所选分类在当前缓存中无数据)", file=sys.stderr)
        return 1
    return 0


def load_userinfo():
    """读取本地 userinfo.json"""
    path = os.path.join(_cache_dir(), "userinfo.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_citys():
    """读取本地 citys.json"""
    path = os.path.join(_cache_dir(), "citys.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def get_capital_id():
    """主城 tileID，无缓存时返回 None"""
    u = load_userinfo()
    if not u:
        return None
    return u.get("CapitalID") or u.get("capitalID")


def get_current_village_id():
    """当前城 tileID（服务器 CurrentVillageID；无效则用主城 CapitalID）。"""
    u = load_userinfo()
    if not u:
        return None
    cv = u.get("CurrentVillageID") or u.get("currentVillageID")
    try:
        if cv is not None and int(cv) > 0:
            return int(cv)
    except (TypeError, ValueError):
        pass
    cap = u.get("CapitalID") or u.get("capitalID")
    try:
        return int(cap) if cap is not None else None
    except (TypeError, ValueError):
        return None


def get_tile_by_name(name):
    """按城市名查 tileID，支持「主城」「第一座城」等"""
    citys = load_citys()
    if not citys:
        return get_capital_id() if name in ("主城", "首都", "第一座城") else None
    name = (name or "").strip()
    if name in ("主城", "首都", "第一座城"):
        for c in citys:
            if c.get("IsCapital") or c.get("isCapital"):
                return c.get("TileID") or c.get("tileID")
        return get_capital_id() or (citys[0].get("TileID") if citys else None)
    for c in citys:
        if (c.get("Name") or c.get("name") or "") == name:
            return c.get("TileID") or c.get("tileID")
    return None


_gold_coin_pat = re.compile(r"^(\d+)\s+Gold Coin\s*$", re.I)


def load_goods_id_name_map():
    """从 session_cache.json 的 goodslist 构建物品 ID→名称（需先 bootstrap）；无则返回空 dict。"""
    m = {}
    path = os.path.join(_cache_dir(), "session_cache.json")
    if not os.path.isfile(path):
        return m
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError):
        return m
    gl = data.get("goodslist") if isinstance(data, dict) else None
    if not isinstance(gl, list):
        return m
    for g in gl:
        if not isinstance(g, dict):
            continue
        gid = g.get("ID")
        if gid is None:
            continue
        try:
            ig = int(gid)
        except (TypeError, ValueError):
            continue
        name = (g.get("name") or g.get("Name") or "").strip()
        m[ig] = name or f"物品#{ig}"
    return m


def _goods_pair_pretty(goods_map, gid: int, count: int) -> str:
    name = goods_map.get(gid) if goods_map else None
    label = name if name else f"物品ID {gid}"
    return f"{label} ×{count}"


def _humanize_svr_gift_tip(payload: str, goods_map: dict) -> str:
    """
    服务端 /svr svr_gift_tip 含义见 Action.cs：类型 2=礼包未随到物时补空投次数；4=goodsId,count；等。
    """
    payload = (payload or "").strip()
    if not payload:
        return "【奖励提示】（空）"

    gm = _gold_coin_pat.match(payload)
    if gm:
        return f"【奖励】金币 ×{gm.group(1)}"

    parts = payload.split(None, 1)
    head, rest = parts[0], (parts[1].strip() if len(parts) > 1 else "")

    if head == "2" and rest.isdigit():
        n = int(rest)
        return (
            f"【礼包补偿】礼包未随机到道具，系统已发放空投补给 ×{n} 次"
            f"（数字为补给次数，不是物品 ID）"
        )

    if head == "3":
        return "【道具效果】立即完成（相关队列）"

    if head == "4":
        if not rest:
            return "【获得物品】（无明细）"
        segs = []
        for chunk in rest.replace(" ", "").split(";"):
            if not chunk:
                continue
            sub = chunk.split(",")
            if len(sub) >= 2:
                try:
                    gid, cnt = int(sub[0]), int(sub[1])
                    segs.append(_goods_pair_pretty(goods_map, gid, cnt))
                except ValueError:
                    segs.append(chunk)
            else:
                segs.append(chunk)
        return "【获得物品】" + "；".join(segs)

    if head == "5":
        return f"【获得兵种】{rest}" if rest else "【获得兵种】"

    if head == "9" and rest.isdigit():
        return f"【地图】地块 {rest} 资源已转换为雷岩"

    if head == "10" and rest.isdigit():
        return f"【地图】地块 {rest} 已创建野怪点"

    return f"【奖励提示】子类型 {head} {rest}".strip()


def _humanize_svr_line(line: str, goods_map: dict) -> str:
    line = line.strip()
    if not line.lower().startswith("/svr"):
        return line
    rest = line[4:].lstrip()
    parts = rest.split(None, 1)
    cmd = (parts[0] or "").lower()
    payload = parts[1] if len(parts) > 1 else ""

    if cmd == "svr_gift_tip":
        return _humanize_svr_gift_tip(payload, goods_map)

    if cmd == "heroinventory":
        pl = payload.strip()
        low = pl.lower()
        if low.startswith("ok"):
            extra = pl[2:].strip()
            return f"【背包】操作成功（{extra}）" if extra else "【背包】道具操作成功"
        if low.startswith("err"):
            return f"【背包】失败：{pl[3:].strip()}"
        return f"【背包】{payload}"

    pls = payload.strip()
    if pls.startswith("{") or pls.startswith("["):
        try:
            j = json.loads(pls)
            pretty = json.dumps(j, ensure_ascii=False, indent=2)
            title = {
                "getresource": "【城内资源】",
                "citylist": "【城市列表】",
                "userinfo": "【用户信息】",
                "getbuildcost": "【建造成本】",
                "addbuildqueue": "【建造入队】",
                "getaccount": "【账户】",
                "goodslist": "【物品目录】",
                "usergoodslist": "【背包实例列表】",
            }.get(cmd, f"【{cmd}】")
            return f"{title}\n{pretty}"
        except json.JSONDecodeError:
            pass

    if cmd == "airdropres" and payload.strip().lower() == "ok":
        return "【空投】领取成功"

    if cmd == "airinfo":
        return f"【空投次数】{payload.strip()}"

    return f"【{cmd}】{payload}".strip()


def humanize_command_output(raw: str) -> str:
    """
    将 POST /game/command 返回的多行 /svr 协议文本转为玩家可读说明（OpenClaw 展示用）。
    调试原样输出可设环境变量 EARTH2037_RAW_SVR=1。
    物品名称依赖 session_cache.json 的 goodslist（请先 bootstrap）。
    """
    if os.environ.get("EARTH2037_RAW_SVR", "").strip().lower() in ("1", "true", "yes"):
        return raw
    if raw is None or not isinstance(raw, str) or not raw.strip():
        return raw
    goods_map = load_goods_id_name_map()
    out_lines = []
    for line in raw.splitlines():
        if line.strip():
            out_lines.append(_humanize_svr_line(line, goods_map))
        else:
            out_lines.append("")
    return "\n".join(out_lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        try:
            ui, cs = sync()
            print("✅ 缓存已更新")
            print(f"  userinfo.json: userID={ui.get('UserID')}, CapitalID={ui.get('CapitalID')}")
            print(f"  citys.json: {len(cs)} 座城市")
        except Exception as e:
            print(f"❌ 同步失败: {e}")
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "bootstrap":
        try:
            data = bootstrap()
            keys = list(data.keys()) if isinstance(data, dict) else []
            print("✅ session_cache.json 已写入（含多路游戏数据）")
            print(f"  键: {', '.join(keys[:12])}{'...' if len(keys) > 12 else ''}")
        except Exception as e:
            print(f"❌ bootstrap 失败: {e}")
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "show":
        focus = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(show_cache(focus))
    else:
        print("用法: python3 cache.py sync | bootstrap | show [分类]")
        print("  sync: 仅 USERINFO + CITYLIST")
        print("  bootstrap: 登录后整包缓存 → session_cache.json（推荐）")
        print("  show: 按块打印 session_cache.json（查城市/建筑/军队等，不连网）")
        print("  show 分类: city | build | troops | task | queue | hero | goods | all")
        print("  需 token: sync/bootstrap；show 只读本地文件")
