#!/usr/bin/env python3
"""
A-SOUL 直播间粉丝牌点亮 + 日常应援。
自动佩戴对应粉丝牌 → 发送 10 条弹幕点亮牌子（保持 3 天可见）。
零外部依赖，纯标准库。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, List

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
_SEND_URL = "https://api.live.bilibili.com/msg/send"

LIGHT_UP_COUNT = 10

DEFAULT_MESSAGES = [
    "哈哈哈哈哈哈哈",
    "早上好",
    "晚上好",
    "中午好",
    "❤️❤️❤️",
    "好好好",
    "来了来了",
    "冲冲冲",
    "加油",
    "干杯",
    "比心",
    "爱了爱了",
    "支持",
    "一直在",
]

MEMBERS = [
    {"name": "嘉然",   "uid": 672328094,         "room": 22637261},
    {"name": "贝拉",   "uid": 672353429,         "room": 22632424},
    {"name": "乃琳",   "uid": 672342685,         "room": 22625027},
    {"name": "心宜",   "uid": 3537115310721181,  "room": 30849777},
    {"name": "思诺",   "uid": 3537115310721781,  "room": 30858592},
]

_COOKIE_PATHS = [
    Path(__file__).resolve().parent.parent / ".cookies.json",
    Path(__file__).resolve().parent.parent.parent / "bilibili-live-checkin" / ".cookies.json",
]


def load_cookies() -> Optional[Dict[str, str]]:
    for p in _COOKIE_PATHS:
        if p.exists():
            try:
                with open(p, "r") as f:
                    data = json.load(f)
                if data.get("SESSDATA") and data.get("bili_jct"):
                    return data
            except Exception:
                continue
    return None


def save_cookies(sessdata: str, bili_jct: str):
    path = _COOKIE_PATHS[0]
    with open(path, "w") as f:
        json.dump({"SESSDATA": sessdata, "bili_jct": bili_jct}, f)
    os.chmod(path, 0o600)
    print(f"💾 Cookie 已保存到 {path}")


# ──────────────────────────────────────────
# Live Status Detection
# ──────────────────────────────────────────

def check_live_status(members: List[Dict], sessdata: str, bili_jct: str) -> Dict[int, bool]:
    """返回 {room_id: is_live}"""
    url = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
    headers = {
        "User-Agent": _UA,
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://live.bilibili.com",
        "Referer": "https://live.bilibili.com",
    }
    form_parts = [f"uids[]={m['uid']}" for m in members]
    form_body = "&".join(form_parts).encode("utf-8")
    req = urllib.request.Request(url, data=form_body, headers=headers)

    uid_to_room = {m["uid"]: m["room"] for m in members}
    result = {m["room"]: False for m in members}

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        if body.get("code") == 0 and body.get("data"):
            for uid_str, info in body["data"].items():
                uid = int(uid_str)
                if uid in uid_to_room:
                    result[uid_to_room[uid]] = info.get("live_status", 0) == 1
    except Exception:
        pass
    return result


# ──────────────────────────────────────────
# Fan Medal (粉丝牌)
# ──────────────────────────────────────────

def _get_json(url: str, headers: dict, timeout: int = 10) -> Optional[dict]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _post_form(url: str, data: dict, headers: dict, timeout: int = 10) -> Optional[dict]:
    form = urllib.parse.urlencode(data).encode("utf-8")
    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, data=form, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def get_my_medals(sessdata: str, bili_jct: str) -> Dict[int, Dict]:
    """获取我的所有粉丝牌，返回 {target_uid: medal_info}"""
    medals = {}
    page = 1
    while True:
        url = f"https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel?page={page}&page_size=50"
        headers = {
            "User-Agent": _UA,
            "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
            "Referer": "https://live.bilibili.com",
        }
        resp = _get_json(url, headers)
        if not resp or resp.get("code") != 0:
            break
        data = resp.get("data", {})

        special = data.get("special_list", []) or []
        normal = data.get("list", []) or []
        for item in special + normal:
            info = item.get("medal", item)
            target_id = info.get("target_id", 0)
            if target_id:
                medals[target_id] = {
                    "medal_id": info.get("medal_id"),
                    "medal_name": info.get("medal_name", ""),
                    "level": info.get("level", 0),
                    "target_id": target_id,
                    "is_lighted": info.get("is_lighted", 0),
                }

        if not data.get("page_info", {}).get("has_more", False) and page > 1:
            break
        total_page = data.get("page_info", {}).get("total_page", 1)
        if page >= total_page:
            break
        page += 1

    return medals


def wear_medal(medal_id: int, sessdata: str, bili_jct: str) -> bool:
    """佩戴指定粉丝牌"""
    url = "https://api.live.bilibili.com/xlive/web-room/v1/fansMedal/wear"
    headers = {
        "User-Agent": _UA,
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Origin": "https://live.bilibili.com",
        "Referer": "https://live.bilibili.com",
    }
    data = {"medal_id": str(medal_id), "csrf": bili_jct, "csrf_token": bili_jct}
    resp = _post_form(url, data, headers)
    return resp is not None and resp.get("code") == 0


def send_danmaku(room_id: int, msg: str, sessdata: str, bili_jct: str) -> Dict:
    form_data = urllib.parse.urlencode({
        "bubble": "0",
        "msg": msg,
        "color": "16777215",
        "mode": "1",
        "room_type": "0",
        "jumpfrom": "0",
        "reply_mid": "0",
        "reply_attr": "0",
        "replay_dmid": "",
        "statistics": json.dumps({"appId": 100, "platform": 5}),
        "fontsize": "25",
        "rnd": str(int(time.time())),
        "roomid": str(room_id),
        "csrf": bili_jct,
        "csrf_token": bili_jct,
    }).encode("utf-8")

    headers = {
        "User-Agent": _UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Origin": "https://live.bilibili.com",
        "Referer": f"https://live.bilibili.com/{room_id}",
    }

    req = urllib.request.Request(_SEND_URL, data=form_data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"code": e.code, "message": f"HTTP {e.code}", "data": body}
    except Exception as e:
        return {"code": -1, "message": str(e)}


def _pick_messages(msgs: List[str], count: int) -> List[str]:
    """从消息池中选取 count 条不重复的弹幕；池不够则循环复用。"""
    import random
    pool = list(msgs)
    random.shuffle(pool)
    result = []
    for i in range(count):
        result.append(pool[i % len(pool)])
    return result


def batch_checkin(members: List[Dict], msgs: List[str], sessdata: str, bili_jct: str,
                  auto_medal: bool = True, count: int = LIGHT_UP_COUNT,
                  delay: float = 8, danmaku_delay: float = 3) -> List[Dict]:
    medals = {}
    if auto_medal:
        print("  🏅 正在获取粉丝牌列表...", file=sys.stderr)
        medals = get_my_medals(sessdata, bili_jct)

    results = []
    for i, m in enumerate(members):
        medal_info = None
        medal_worn = False

        if auto_medal and m["uid"] in medals:
            medal_info = medals[m["uid"]]
            medal_worn = wear_medal(medal_info["medal_id"], sessdata, bili_jct)
            time.sleep(1)

        picked = _pick_messages(msgs, count)
        sent_ok = 0
        sent_fail = 0
        last_error = None

        for j, msg in enumerate(picked):
            resp = send_danmaku(m["room"], msg, sessdata, bili_jct)
            if resp.get("code") == 0:
                sent_ok += 1
            else:
                sent_fail += 1
                last_error = resp.get("message", resp.get("msg", "未知错误"))
            if j < len(picked) - 1:
                time.sleep(danmaku_delay)

        lit = sent_ok >= LIGHT_UP_COUNT
        results.append({
            "name": m["name"],
            "room": m["room"],
            "url": f"https://live.bilibili.com/{m['room']}",
            "sent_ok": sent_ok,
            "sent_fail": sent_fail,
            "count": count,
            "lit": lit,
            "success": sent_ok > 0,
            "error": last_error,
            "medal": medal_info,
            "medal_worn": medal_worn,
        })
        if i < len(members) - 1:
            time.sleep(delay)
    return results


def format_output(results: List[Dict]) -> str:
    lines = ["🌟 A-SOUL 粉丝牌点亮结果", ""]
    lit_count = sum(1 for r in results if r["lit"])

    for r in results:
        medal = r.get("medal")
        medal_str = ""
        if medal:
            if r.get("medal_worn"):
                medal_str = f"  🏅{medal['medal_name']}Lv{medal['level']}"
            else:
                medal_str = f"  🏅{medal['medal_name']}(佩戴失败)"
        elif r.get("success"):
            medal_str = "  (无粉丝牌)"

        if r["lit"]:
            lines.append(f"  ✅ {r['name']}{medal_str}  — 已点亮  💬{r['sent_ok']}/{r['count']}条")
        elif r["success"]:
            lines.append(f"  ⚠️ {r['name']}{medal_str}  — 部分成功  💬{r['sent_ok']}/{r['count']}条")
        else:
            err = r["error"] or "未知错误"
            if "login" in err.lower():
                lines.append(f"  ❌ {r['name']}  — Cookie 过期，请重新设置")
            else:
                lines.append(f"  ❌ {r['name']}  — {err}")

    lines.append("")
    if lit_count == len(results):
        lines.append(f"🎉 全部点亮成功！({lit_count}/{len(results)}) 牌子 3 天内不会熄灭")
    elif lit_count > 0:
        lines.append(f"📊 部分点亮：{lit_count}/{len(results)}，未满 {LIGHT_UP_COUNT} 条的牌子可能无法点亮")
    else:
        lines.append(f"💔 全部失败，请检查 Cookie 是否有效")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="A-SOUL 粉丝牌点亮 + 直播间弹幕应援")
    parser.add_argument("--msg", action="append", dest="msgs",
                        help="自定义弹幕内容（可多次指定，如 --msg 签到 --msg 加油）")
    parser.add_argument("--count", type=int, default=LIGHT_UP_COUNT,
                        help=f"每个直播间发送的弹幕条数（默认 {LIGHT_UP_COUNT}，发满 10 条可点亮牌子）")
    parser.add_argument("--members", help="指定成员（逗号分隔，如：嘉然,贝拉）默认全部")
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--save-cookie", action="store_true", help="保存 cookie")
    parser.add_argument("--no-medal", action="store_true", help="不自动佩戴粉丝牌")
    parser.add_argument("--live-only", action="store_true",
                        help="只对正在直播的成员发弹幕（需要开播才能点亮牌子）")
    parser.add_argument("--delay", type=float, default=8, help="成员之间的间隔秒数（默认 8）")
    parser.add_argument("--danmaku-delay", type=float, default=3,
                        help="同一直播间内弹幕之间的间隔秒数（默认 3）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--list", action="store_true", help="列出所有成员")
    args = parser.parse_args()

    if args.list:
        print("🌟 A-SOUL 现役成员：")
        for m in MEMBERS:
            print(f"  {m['name']}  UID:{m['uid']}  直播间:{m['room']}  https://live.bilibili.com/{m['room']}")
        return

    sessdata = args.sessdata
    bili_jct = args.bili_jct

    if args.save_cookie:
        if not sessdata or not bili_jct:
            print("❌ --save-cookie 需要同时提供 --sessdata 和 --bili-jct")
            sys.exit(1)
        save_cookies(sessdata, bili_jct)
        return

    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到 Cookie。请先设置：")
            print("  python3 checkin.py --save-cookie --sessdata \"你的SESSDATA\" --bili-jct \"你的bili_jct\"")
            print("")
            print("或在 bilibili-live-checkin skill 中已保存的 Cookie 会自动复用。")
            sys.exit(1)

    targets = MEMBERS
    if args.members:
        names = [n.strip() for n in args.members.split(",")]
        targets = [m for m in MEMBERS if m["name"] in names]
        if not targets:
            print(f"❌ 未找到指定成员：{args.members}")
            print(f"   可用成员：{', '.join(m['name'] for m in MEMBERS)}")
            sys.exit(1)

    if args.live_only:
        print("  📡 正在检测直播状态...", file=sys.stderr)
        live_status = check_live_status(targets, sessdata, bili_jct)
        live_targets = [m for m in targets if live_status.get(m["room"], False)]
        offline = [m["name"] for m in targets if not live_status.get(m["room"], False)]
        if offline:
            print(f"  💤 未开播（跳过）：{', '.join(offline)}", file=sys.stderr)
        if not live_targets:
            print("\nℹ️  当前没有成员在播，本次跳过")
            return
        targets = live_targets
        print(f"  🔴 在播：{', '.join(m['name'] for m in targets)}", file=sys.stderr)

    msgs = args.msgs if args.msgs else DEFAULT_MESSAGES

    results = batch_checkin(targets, msgs, sessdata, bili_jct,
                            auto_medal=not args.no_medal, count=args.count,
                            delay=args.delay, danmaku_delay=args.danmaku_delay)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()
