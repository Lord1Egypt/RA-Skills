#!/usr/bin/env python3
"""
Bilibili 每日经验任务 — 自动完成登录、观看、分享、投币。
每天最多 65 经验值（登录5 + 观看5 + 分享5 + 投币50）。
零外部依赖，纯标准库。
"""

import argparse
import json
import random
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, List

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
_COOKIE_FILE = Path(__file__).resolve().parent.parent / ".cookies.json"


def _load_cookies() -> Optional[Dict[str, str]]:
    if not _COOKIE_FILE.exists():
        return None
    try:
        with open(_COOKIE_FILE, "r") as f:
            data = json.load(f)
        if data.get("SESSDATA") and data.get("bili_jct"):
            return data
    except Exception:
        pass
    return None


def _make_headers(sessdata: str, bili_jct: str, referer: str = "https://www.bilibili.com") -> dict:
    return {
        "User-Agent": _UA,
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Referer": referer,
    }


def _get(url: str, headers: dict, timeout: int = 10) -> Optional[dict]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"code": -1, "message": str(e)}


def _post(url: str, data: dict, headers: dict, timeout: int = 10) -> Optional[dict]:
    form = urllib.parse.urlencode(data).encode("utf-8")
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=form, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except Exception:
            return {"code": e.code, "message": f"HTTP {e.code}"}
    except Exception as e:
        return {"code": -1, "message": str(e)}


# ──────────────────────────────────────────
# Task: Check reward status
# ──────────────────────────────────────────

def check_reward(sessdata: str, bili_jct: str) -> dict:
    """查询今日任务完成状态"""
    url = "https://api.bilibili.com/x/member/web/exp/reward"
    headers = _make_headers(sessdata, bili_jct, "https://account.bilibili.com/")
    resp = _get(url, headers)
    if not resp or resp.get("code") != 0:
        url2 = "https://account.bilibili.com/home/reward"
        resp = _get(url2, headers)
    if not resp or resp.get("code") != 0:
        return {"error": resp.get("message", "无法获取任务状态") if resp else "请求失败"}

    data = resp.get("data", {})
    return {
        "login": data.get("login", False),
        "watch": data.get("watch", data.get("watch_av", False)),
        "share": data.get("share", data.get("share_av", False)),
        "coins": data.get("coins", data.get("coins_av", 0)),
    }


# ──────────────────────────────────────────
# Task: Get random video for watch/share/coin
# ──────────────────────────────────────────

def _get_popular_videos(sessdata: str, bili_jct: str) -> List[dict]:
    """获取热门视频列表"""
    url = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1"
    headers = _make_headers(sessdata, bili_jct)
    resp = _get(url, headers)
    if not resp or resp.get("code") != 0:
        return []
    items = resp.get("data", {}).get("list", [])
    return [{"aid": v.get("aid"), "bvid": v.get("bvid"), "cid": v.get("cid"),
             "title": v.get("title", ""), "duration": v.get("duration", 100)} for v in items if v.get("aid")]


def _pick_video(sessdata: str, bili_jct: str) -> Optional[dict]:
    videos = _get_popular_videos(sessdata, bili_jct)
    if not videos:
        return None
    return random.choice(videos)


# ──────────────────────────────────────────
# Task: Watch video (heartbeat)
# ──────────────────────────────────────────

def do_watch(sessdata: str, bili_jct: str) -> dict:
    """模拟观看视频（发送心跳）+5 EXP"""
    video = _pick_video(sessdata, bili_jct)
    if not video:
        return {"success": False, "task": "watch", "message": "无法获取视频列表"}

    url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
    data = {
        "aid": str(video["aid"]),
        "cid": str(video["cid"]),
        "bvid": video.get("bvid", ""),
        "mid": "",
        "csrf": bili_jct,
        "played_time": str(random.randint(10, min(video["duration"], 300))),
        "real_played_time": str(random.randint(10, min(video["duration"], 300))),
        "realtime": str(video["duration"]),
        "start_ts": str(int(time.time())),
        "type": "3",
        "dt": "2",
        "play_type": "1",
    }
    headers = _make_headers(sessdata, bili_jct, f"https://www.bilibili.com/video/{video.get('bvid', '')}")
    resp = _post(url, data, headers)

    if resp and resp.get("code") == 0:
        return {"success": True, "task": "watch", "exp": 5, "video": video["title"]}
    return {"success": False, "task": "watch", "message": resp.get("message", "未知错误") if resp else "请求失败"}


# ──────────────────────────────────────────
# Task: Share video
# ──────────────────────────────────────────

def do_share(sessdata: str, bili_jct: str) -> dict:
    """分享视频 +5 EXP"""
    video = _pick_video(sessdata, bili_jct)
    if not video:
        return {"success": False, "task": "share", "message": "无法获取视频列表"}

    url = "https://api.bilibili.com/x/web-interface/share/add"
    data = {
        "aid": str(video["aid"]),
        "bvid": video.get("bvid", ""),
        "csrf": bili_jct,
    }
    headers = _make_headers(sessdata, bili_jct)
    resp = _post(url, data, headers)

    if resp and resp.get("code") == 0:
        return {"success": True, "task": "share", "exp": 5, "video": video["title"]}
    return {"success": False, "task": "share", "message": resp.get("message", "未知错误") if resp else "请求失败"}


# ──────────────────────────────────────────
# Task: Coin video
# ──────────────────────────────────────────

def do_coin(sessdata: str, bili_jct: str, count: int = 5) -> dict:
    """投币 +10 EXP/枚，最多 5 枚 = 50 EXP"""
    results = []
    total_exp = 0

    for i in range(count):
        video = _pick_video(sessdata, bili_jct)
        if not video:
            results.append({"index": i + 1, "success": False, "message": "无法获取视频"})
            continue

        url = "https://api.bilibili.com/x/web-interface/coin/add"
        data = {
            "aid": str(video["aid"]),
            "bvid": video.get("bvid", ""),
            "multiply": "1",
            "select_like": "1",
            "csrf": bili_jct,
        }
        headers = _make_headers(sessdata, bili_jct)
        resp = _post(url, data, headers)

        if resp and resp.get("code") == 0:
            total_exp += 10
            results.append({"index": i + 1, "success": True, "video": video["title"]})
        else:
            msg = resp.get("message", "未知错误") if resp else "请求失败"
            results.append({"index": i + 1, "success": False, "message": msg})
            if resp and resp.get("code") == 34005:
                break

        if i < count - 1:
            time.sleep(random.uniform(1, 3))

    succeeded = sum(1 for r in results if r["success"])
    return {
        "success": succeeded > 0,
        "task": "coin",
        "exp": total_exp,
        "count": succeeded,
        "target": count,
        "details": results,
    }


# ──────────────────────────────────────────
# Task: Live sign (直播签到)
# ──────────────────────────────────────────

def do_live_sign(sessdata: str, bili_jct: str) -> dict:
    """直播区签到"""
    url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
    headers = _make_headers(sessdata, bili_jct, "https://live.bilibili.com")
    resp = _get(url, headers)

    if resp and resp.get("code") == 0:
        data = resp.get("data", {})
        return {
            "success": True,
            "task": "live_sign",
            "text": data.get("text", "签到成功"),
            "bonus_day": data.get("specialText", ""),
        }
    msg = resp.get("message", "未知错误") if resp else "请求失败"
    already = "已签到" in msg or resp.get("code") == 1011040
    return {
        "success": already,
        "task": "live_sign",
        "message": "今日已签到" if already else msg,
        "already_done": already,
    }


# ──────────────────────────────────────────
# Task: Get user info
# ──────────────────────────────────────────

def get_user_info(sessdata: str, bili_jct: str) -> Optional[dict]:
    """获取用户信息（等级、经验等）"""
    url = "https://api.bilibili.com/x/web-interface/nav"
    headers = _make_headers(sessdata, bili_jct)
    resp = _get(url, headers)
    if not resp or resp.get("code") != 0:
        return None
    data = resp.get("data", {})
    level_info = data.get("level_info", {})
    return {
        "uid": data.get("mid"),
        "name": data.get("uname"),
        "level": level_info.get("current_level"),
        "current_exp": level_info.get("current_exp"),
        "next_exp": level_info.get("next_exp", 0),
        "coins": data.get("money", 0),
        "is_login": data.get("isLogin", False),
    }


# ──────────────────────────────────────────
# Main
# ──────────────────────────────────────────

def run_all(sessdata: str, bili_jct: str, skip_coin: bool = False, coin_count: int = 5) -> dict:
    """执行所有每日任务"""
    user = get_user_info(sessdata, bili_jct)
    if not user or not user.get("is_login"):
        return {"error": "Cookie 无效或已过期"}

    status_before = check_reward(sessdata, bili_jct)

    results = []
    total_exp = 0

    if not status_before.get("login"):
        total_exp += 5
    results.append({"task": "login", "exp": 5, "success": True, "message": "登录奖励"})

    if not status_before.get("watch"):
        r = do_watch(sessdata, bili_jct)
        results.append(r)
        if r["success"]:
            total_exp += 5
        time.sleep(random.uniform(1, 2))
    else:
        results.append({"task": "watch", "exp": 0, "success": True, "message": "今日已完成"})

    if not status_before.get("share"):
        r = do_share(sessdata, bili_jct)
        results.append(r)
        if r["success"]:
            total_exp += 5
        time.sleep(random.uniform(1, 2))
    else:
        results.append({"task": "share", "exp": 0, "success": True, "message": "今日已完成"})

    coins_done = status_before.get("coins", 0)
    if isinstance(coins_done, bool):
        coins_done = 50 if coins_done else 0
    remaining_coins = max(0, (coin_count * 10 - coins_done) // 10)

    if not skip_coin and remaining_coins > 0:
        r = do_coin(sessdata, bili_jct, remaining_coins)
        results.append(r)
        if r["success"]:
            total_exp += r.get("exp", 0)
    elif skip_coin:
        results.append({"task": "coin", "exp": 0, "success": True, "message": "已跳过（--skip-coin）"})
    else:
        results.append({"task": "coin", "exp": 0, "success": True, "message": "今日投币已满"})

    r = do_live_sign(sessdata, bili_jct)
    results.append(r)

    status_after = check_reward(sessdata, bili_jct)

    return {
        "user": user,
        "tasks": results,
        "total_exp_gained": total_exp,
        "status_before": status_before,
        "status_after": status_after,
    }


def format_output(result: dict) -> str:
    if "error" in result:
        return f"❌ {result['error']}"

    user = result["user"]
    tasks = result["tasks"]
    total = result["total_exp_gained"]

    lines = []
    lines.append(f"📊 B站每日任务 — {user['name']} (Lv{user['level']})")
    lines.append(f"   经验：{user['current_exp']}/{user['next_exp']}  硬币：{user['coins']}")
    lines.append("")

    task_names = {
        "login": "🔑 登录",
        "watch": "▶️  观看",
        "share": "🔗 分享",
        "coin": "🪙 投币",
        "live_sign": "📺 直播签到",
    }

    for t in tasks:
        name = task_names.get(t.get("task", ""), t.get("task", ""))
        if t.get("success"):
            exp = t.get("exp", 0)
            extra = ""
            if t.get("video"):
                extra = f" ({t['video'][:20]})"
            elif t.get("message"):
                extra = f" ({t['message']})"
            elif t.get("text"):
                extra = f" ({t['text']})"
            elif t.get("count"):
                extra = f" ({t['count']}/{t['target']}枚)"
            if exp > 0:
                lines.append(f"  ✅ {name}  +{exp} EXP{extra}")
            else:
                lines.append(f"  ✅ {name}{extra}")
        else:
            msg = t.get("message", "失败")
            lines.append(f"  ❌ {name}  {msg}")

    lines.append("")
    lines.append(f"📈 本次获得：+{total} EXP")

    exp_remaining = user["next_exp"] - user["current_exp"] - total
    if exp_remaining > 0:
        days = exp_remaining // 65 + 1
        lines.append(f"🎯 距离 Lv{user['level'] + 1} 还需 {exp_remaining} EXP（约 {days} 天）")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Bilibili 每日经验任务（登录+观看+分享+投币+直播签到）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 执行所有任务（使用已保存的 cookie）
  python3 daily.py

  # 跳过投币（不消耗硬币）
  python3 daily.py --skip-coin

  # 只投 3 枚
  python3 daily.py --coin 3

  # 查看当前任务状态
  python3 daily.py --status

  # JSON 输出
  python3 daily.py --json
""",
    )
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--skip-coin", action="store_true", default=True, help="跳过投币任务（默认跳过，硬币不好获得）")
    parser.add_argument("--coin", type=int, default=5, help="投币数量（默认5枚=50EXP，需配合 --do-coin 使用）")
    parser.add_argument("--do-coin", action="store_true", help="启用投币任务（每枚消耗1硬币）")
    parser.add_argument("--status", action="store_true", help="仅查看当前任务状态")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    sessdata = args.sessdata
    bili_jct = args.bili_jct

    if not sessdata or not bili_jct:
        saved = _load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到保存的 Cookie。请先运行 checkin.py --save-cookie 保存 Cookie。")
            sys.exit(1)

    if args.status:
        user = get_user_info(sessdata, bili_jct)
        if not user or not user.get("is_login"):
            print("❌ Cookie 无效或已过期")
            sys.exit(1)
        status = check_reward(sessdata, bili_jct)
        if args.json:
            print(json.dumps({"user": user, "status": status}, ensure_ascii=False, indent=2))
        else:
            print(f"📊 {user['name']} (Lv{user['level']})  经验：{user['current_exp']}/{user['next_exp']}  硬币：{user['coins']}")
            print("")
            s = status
            print(f"  🔑 登录：{'✅' if s.get('login') else '❌'}")
            print(f"  ▶️  观看：{'✅' if s.get('watch') else '❌'}")
            print(f"  🔗 分享：{'✅' if s.get('share') else '❌'}")
            coins = s.get('coins', 0)
            if isinstance(coins, bool):
                coins = 50 if coins else 0
            print(f"  🪙 投币：{coins}/50 EXP")
        return

    skip_coin = not args.do_coin
    result = run_all(sessdata, bili_jct, skip_coin=skip_coin, coin_count=args.coin)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
