#!/usr/bin/env python3
"""
A-SOUL 视频三连助手 — 批量点赞/投币/收藏成员新发布的视频。
需要 WBI 签名来访问 B站 Space API。
零外部依赖，纯标准库。
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, List, Tuple

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

MEMBERS = [
    {"name": "嘉然",   "uid": 672328094},
    {"name": "贝拉",   "uid": 672353429},
    {"name": "乃琳",   "uid": 672342685},
    {"name": "心宜",   "uid": 3537115310721181},
    {"name": "思诺",   "uid": 3537115310721781},
]

_COOKIE_PATHS = [
    Path(__file__).resolve().parent.parent / ".cookies.json",
    Path(__file__).resolve().parent.parent.parent / "bilibili-live-checkin" / ".cookies.json",
]

MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
    27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
    37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
    22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
]

CST = timezone(timedelta(hours=8))


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
    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
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
# WBI Signing (required for space API)
# ──────────────────────────────────────────

def _get_wbi_keys(sessdata: str, bili_jct: str) -> Tuple[str, str]:
    """从 nav API 获取 WBI img_key 和 sub_key"""
    url = "https://api.bilibili.com/x/web-interface/nav"
    headers = _make_headers(sessdata, bili_jct)
    resp = _get(url, headers)
    if not resp or resp.get("code") != 0:
        raise RuntimeError(f"获取 WBI keys 失败: {resp}")
    wbi_img = resp["data"]["wbi_img"]
    img_url = wbi_img["img_url"]
    sub_url = wbi_img["sub_url"]
    img_key = img_url.rsplit("/", 1)[-1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[-1].split(".")[0]
    return img_key, sub_key


def _get_mixin_key(img_key: str, sub_key: str) -> str:
    orig = img_key + sub_key
    return "".join(orig[i] for i in MIXIN_KEY_ENC_TAB)[:32]


def _sign_wbi(params: dict, mixin_key: str) -> dict:
    params["wts"] = int(time.time())
    params.pop("w_rid", None)
    filtered = {
        k: "".join(c for c in str(v) if c not in "!'()*")
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(sorted(filtered.items()))
    w_rid = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = w_rid
    return params


_wbi_mixin_key_cache: Optional[str] = None


def get_mixin_key(sessdata: str, bili_jct: str) -> str:
    global _wbi_mixin_key_cache
    if _wbi_mixin_key_cache:
        return _wbi_mixin_key_cache
    img_key, sub_key = _get_wbi_keys(sessdata, bili_jct)
    _wbi_mixin_key_cache = _get_mixin_key(img_key, sub_key)
    return _wbi_mixin_key_cache


# ──────────────────────────────────────────
# Fetch Videos
# ──────────────────────────────────────────

def fetch_user_videos(uid: int, sessdata: str, bili_jct: str,
                      page_size: int = 30, page: int = 1) -> List[Dict]:
    """获取 UP 主的视频列表（按发布时间倒序）"""
    mixin_key = get_mixin_key(sessdata, bili_jct)
    params = {
        "mid": str(uid),
        "ps": str(page_size),
        "pn": str(page),
        "order": "pubdate",
        "tid": "0",
    }
    signed = _sign_wbi(params, mixin_key)
    query = urllib.parse.urlencode(signed)
    url = f"https://api.bilibili.com/x/space/wbi/arc/search?{query}"
    headers = _make_headers(sessdata, bili_jct, f"https://space.bilibili.com/{uid}/video")

    resp = _get(url, headers)
    if not resp or resp.get("code") != 0:
        return []

    vlist = resp.get("data", {}).get("list", {}).get("vlist", [])
    videos = []
    for v in vlist:
        videos.append({
            "aid": v.get("aid"),
            "bvid": v.get("bvid", ""),
            "title": v.get("title", ""),
            "created": v.get("created", 0),
            "length": v.get("length", ""),
            "play": v.get("play", 0),
            "comment": v.get("comment", 0),
        })
    return videos


def filter_by_month(videos: List[Dict], year: int, month: int) -> List[Dict]:
    """筛选指定月份的视频"""
    start = datetime(year, month, 1, tzinfo=CST)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=CST)
    else:
        end = datetime(year, month + 1, 1, tzinfo=CST)

    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    return [v for v in videos if start_ts <= v.get("created", 0) < end_ts]


def filter_recent_days(videos: List[Dict], days: int) -> List[Dict]:
    """筛选最近 N 天内的视频"""
    cutoff = int(time.time()) - days * 86400
    return [v for v in videos if v.get("created", 0) >= cutoff]


# ──────────────────────────────────────────
# Video Interactions
# ──────────────────────────────────────────

def like_video(aid: int, sessdata: str, bili_jct: str) -> Dict:
    url = "https://api.bilibili.com/x/web-interface/archive/like"
    data = {"aid": str(aid), "like": "1", "csrf": bili_jct}
    headers = _make_headers(sessdata, bili_jct)
    resp = _post(url, data, headers)
    if resp and resp.get("code") == 0:
        return {"success": True, "action": "like"}
    already = resp and resp.get("code") == 65006
    return {
        "success": already,
        "action": "like",
        "already_done": already,
        "error": None if already else (resp.get("message", "未知错误") if resp else "请求失败"),
    }


def coin_video(aid: int, sessdata: str, bili_jct: str, multiply: int = 1) -> Dict:
    url = "https://api.bilibili.com/x/web-interface/coin/add"
    data = {
        "aid": str(aid),
        "multiply": str(multiply),
        "select_like": "0",
        "csrf": bili_jct,
    }
    headers = _make_headers(sessdata, bili_jct)
    resp = _post(url, data, headers)
    if resp and resp.get("code") == 0:
        return {"success": True, "action": "coin", "multiply": multiply}
    already = resp and resp.get("code") == 34005
    return {
        "success": already,
        "action": "coin",
        "already_done": already,
        "error": None if already else (resp.get("message", "未知错误") if resp else "请求失败"),
    }


def fav_video(aid: int, sessdata: str, bili_jct: str, fav_id: Optional[int] = None) -> Dict:
    if not fav_id:
        fav_id = _get_default_fav(sessdata, bili_jct)
    if not fav_id:
        return {"success": False, "action": "fav", "error": "无法获取默认收藏夹"}

    url = "https://api.bilibili.com/x/v3/fav/resource/deal"
    data = {
        "rid": str(aid),
        "type": "2",
        "add_media_ids": str(fav_id),
        "csrf": bili_jct,
    }
    headers = _make_headers(sessdata, bili_jct)
    resp = _post(url, data, headers)
    if resp and resp.get("code") == 0:
        prompt = resp.get("data", {}).get("prompt", False)
        return {"success": True, "action": "fav", "already_done": prompt}
    already = resp and resp.get("code") == 11201
    return {
        "success": already,
        "action": "fav",
        "already_done": already,
        "error": None if already else (resp.get("message", "未知错误") if resp else "请求失败"),
    }


def _get_default_fav(sessdata: str, bili_jct: str) -> Optional[int]:
    """获取用户默认收藏夹 ID"""
    nav_url = "https://api.bilibili.com/x/web-interface/nav"
    headers = _make_headers(sessdata, bili_jct)
    resp = _get(nav_url, headers)
    if not resp or resp.get("code") != 0:
        return None
    my_uid = resp.get("data", {}).get("mid")
    if not my_uid:
        return None

    fav_url = f"https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={my_uid}&type=2"
    resp = _get(fav_url, headers)
    if not resp or resp.get("code") != 0:
        return None
    folders = resp.get("data", {}).get("list", [])
    if not folders:
        return None
    return folders[0].get("id")


# ──────────────────────────────────────────
# Batch Processing
# ──────────────────────────────────────────

def process_member_videos(member: Dict, videos: List[Dict],
                          sessdata: str, bili_jct: str,
                          do_like: bool = True, do_coin: bool = False,
                          do_fav: bool = False, fav_id: Optional[int] = None,
                          delay: float = 8) -> List[Dict]:
    results = []
    for i, v in enumerate(videos):
        aid = v["aid"]
        title = v["title"]
        actions = []

        if do_like:
            r = like_video(aid, sessdata, bili_jct)
            actions.append(r)
            if do_coin or do_fav:
                time.sleep(2)

        if do_coin:
            r = coin_video(aid, sessdata, bili_jct)
            actions.append(r)
            if do_fav:
                time.sleep(2)

        if do_fav:
            r = fav_video(aid, sessdata, bili_jct, fav_id)
            actions.append(r)

        results.append({
            "member": member["name"],
            "title": title,
            "bvid": v.get("bvid", ""),
            "aid": aid,
            "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
            "created": v.get("created", 0),
            "actions": actions,
        })
        if i < len(videos) - 1:
            time.sleep(delay)

    return results


def format_output(all_results: List[Dict], do_like: bool, do_coin: bool, do_fav: bool) -> str:
    action_names = []
    if do_like:
        action_names.append("点赞")
    if do_coin:
        action_names.append("投币")
    if do_fav:
        action_names.append("收藏")
    action_str = "+".join(action_names)

    lines = [f"🌟 A-SOUL 视频{action_str}结果", ""]

    total_videos = 0
    total_success = 0

    current_member = None
    for r in all_results:
        if r["member"] != current_member:
            current_member = r["member"]
            lines.append(f"  👤 {current_member}:")

        total_videos += 1
        title_short = r["title"][:30] + ("..." if len(r["title"]) > 30 else "")
        dt = datetime.fromtimestamp(r["created"], CST).strftime("%m-%d")

        action_icons = []
        all_ok = True
        for a in r["actions"]:
            act = a["action"]
            if a.get("success"):
                if a.get("already_done"):
                    action_icons.append({"like": "👍⏭", "coin": "🪙⏭", "fav": "⭐⏭"}[act])
                else:
                    action_icons.append({"like": "👍✅", "coin": "🪙✅", "fav": "⭐✅"}[act])
                    total_success += 1
            else:
                action_icons.append({"like": "👍❌", "coin": "🪙❌", "fav": "⭐❌"}[act])
                all_ok = False

        status = " ".join(action_icons)
        lines.append(f"    [{dt}] {title_short}  {status}")

    lines.append("")
    lines.append(f"📊 共处理 {total_videos} 个视频")

    return "\n".join(lines)


def parse_month(s: str) -> Tuple[int, int]:
    """解析月份字符串，支持 '3', '03', '2026-03', '2026/3' 等格式"""
    s = s.strip()
    if re.match(r"^\d{4}[-/]\d{1,2}$", s):
        parts = re.split(r"[-/]", s)
        return int(parts[0]), int(parts[1])
    if re.match(r"^\d{1,2}$", s):
        now = datetime.now(CST)
        return now.year, int(s)
    raise ValueError(f"无法解析月份: {s}（格式示例: 3, 03, 2026-03）")


def main():
    parser = argparse.ArgumentParser(
        description="A-SOUL 视频点赞/投币/收藏",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 给 A-SOUL 3月新视频全部点赞（默认）
  python3 videos.py --month 3

  # 给最近7天视频点赞+投币+收藏
  python3 videos.py --days 7 --coin --fav

  # 只给嘉然和贝拉的视频点赞
  python3 videos.py --month 3 --members 嘉然,贝拉

  # 不点赞，只投币
  python3 videos.py --month 3 --no-like --coin
""",
    )
    parser.add_argument("--month", help="指定月份（如 3、03、2026-03）")
    parser.add_argument("--days", type=int, help="最近 N 天的视频")
    parser.add_argument("--like", dest="do_like", action="store_true", default=True, help="点赞（默认开启）")
    parser.add_argument("--no-like", dest="do_like", action="store_false", help="不点赞")
    parser.add_argument("--coin", action="store_true", default=False, help="投币（默认关闭）")
    parser.add_argument("--fav", action="store_true", default=False, help="收藏（默认关闭）")
    parser.add_argument("--members", help="指定成员（逗号分隔）")
    parser.add_argument("--delay", type=float, default=8, help="视频之间的间隔秒数（默认 8）")
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    if not args.month and not args.days:
        print("❌ 请指定 --month 或 --days 参数")
        print("   例: --month 3  或  --days 7")
        sys.exit(1)

    sessdata = args.sessdata
    bili_jct = args.bili_jct
    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到 Cookie。请先在 bilibili-live-checkin 中保存 Cookie。")
            sys.exit(1)

    targets = MEMBERS
    if args.members:
        names = [n.strip() for n in args.members.split(",")]
        targets = [m for m in MEMBERS if m["name"] in names]
        if not targets:
            print(f"❌ 未找到成员: {args.members}")
            sys.exit(1)

    fav_id = None
    if args.fav:
        fav_id = _get_default_fav(sessdata, bili_jct)
        if not fav_id:
            print("⚠️ 无法获取默认收藏夹，收藏功能将跳过")
            args.fav = False

    all_results = []
    for member in targets:
        print(f"  📡 正在获取 {member['name']} 的视频...", file=sys.stderr)
        videos = fetch_user_videos(member["uid"], sessdata, bili_jct)

        if args.month:
            year, month = parse_month(args.month)
            videos = filter_by_month(videos, year, month)
        elif args.days:
            videos = filter_recent_days(videos, args.days)

        if not videos:
            print(f"  ℹ️  {member['name']} 在指定时间段内没有新视频", file=sys.stderr)
            continue

        print(f"  📹 找到 {len(videos)} 个视频，开始处理...", file=sys.stderr)
        results = process_member_videos(
            member, videos, sessdata, bili_jct,
            do_like=args.do_like, do_coin=args.coin,
            do_fav=args.fav, fav_id=fav_id, delay=args.delay,
        )
        all_results.extend(results)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        if all_results:
            print(format_output(all_results, args.do_like, args.coin, args.fav))
        else:
            print("ℹ️  指定时间段内没有找到任何视频")


if __name__ == "__main__":
    main()
