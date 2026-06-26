#!/usr/bin/env python3
"""
A-SOUL 动态点赞 — 批量给成员的动态（图文/视频/转发）点赞。
零外部依赖，纯标准库。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple

from http.cookiejar import CookieJar

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

_cookie_jar = CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cookie_jar))
_cookies_ready = False


def _ensure_cookies():
    """访问 bilibili.com 获取 buvid3 等反爬 cookie"""
    global _cookies_ready
    if _cookies_ready:
        return
    try:
        req = urllib.request.Request("https://www.bilibili.com", headers={"User-Agent": _UA})
        _opener.open(req, timeout=5)
    except Exception:
        pass
    _cookies_ready = True


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

CST = timezone(timedelta(hours=8))

DYN_TYPE_NAMES = {
    "DYNAMIC_TYPE_AV": "视频",
    "DYNAMIC_TYPE_DRAW": "图文",
    "DYNAMIC_TYPE_WORD": "文字",
    "DYNAMIC_TYPE_FORWARD": "转发",
    "DYNAMIC_TYPE_LIVE_RCMD": "直播",
    "DYNAMIC_TYPE_ARTICLE": "专栏",
}


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
    _ensure_cookies()
    jar_cookies = "; ".join(f"{c.name}={c.value}" for c in _cookie_jar)
    auth_cookies = f"SESSDATA={sessdata}; bili_jct={bili_jct}"
    combined = f"{jar_cookies}; {auth_cookies}" if jar_cookies else auth_cookies
    return {
        "User-Agent": _UA,
        "Cookie": combined,
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
# Fetch Dynamics
# ──────────────────────────────────────────

def fetch_user_dynamics(uid: int, sessdata: str, bili_jct: str,
                        max_pages: int = 3) -> List[Dict]:
    """获取 UP 主的动态列表"""
    headers = _make_headers(sessdata, bili_jct, f"https://space.bilibili.com/{uid}/dynamic")
    dynamics = []
    offset = ""

    for _ in range(max_pages):
        url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={uid}&features=itemOpusStyle"
        if offset:
            url += f"&offset={offset}"

        resp = _get(url, headers)
        if not resp or resp.get("code") != 0:
            break

        items = resp.get("data", {}).get("items", [])
        if not items:
            break

        for item in items:
            dyn_id = item.get("id_str", "")
            dyn_type = item.get("type", "")
            pub_ts_raw = item.get("modules", {}).get("module_author", {}).get("pub_ts", 0)
            pub_ts = int(pub_ts_raw) if pub_ts_raw else 0

            desc_text = ""
            major = item.get("modules", {}).get("module_dynamic", {})
            desc = major.get("desc", {})
            if desc:
                desc_text = desc.get("text", "")

            opus = major.get("major", {})
            if opus and opus.get("type") == "MAJOR_TYPE_ARCHIVE":
                archive = opus.get("archive", {})
                desc_text = desc_text or archive.get("title", "")
            elif opus and opus.get("type") == "MAJOR_TYPE_OPUS":
                opus_summary = opus.get("opus", {}).get("summary", {})
                if opus_summary and opus_summary.get("text"):
                    desc_text = desc_text or opus_summary["text"]

            dynamics.append({
                "dyn_id": dyn_id,
                "type": dyn_type,
                "type_name": DYN_TYPE_NAMES.get(dyn_type, dyn_type),
                "pub_ts": pub_ts,
                "text": desc_text[:60],
            })

        offset = resp.get("data", {}).get("offset", "")
        has_more = resp.get("data", {}).get("has_more", False)
        if not has_more or not offset:
            break

    return dynamics


def filter_by_days(dynamics: List[Dict], days: int) -> List[Dict]:
    cutoff = int(time.time()) - days * 86400
    return [d for d in dynamics if d.get("pub_ts", 0) >= cutoff]


def filter_by_month(dynamics: List[Dict], year: int, month: int) -> List[Dict]:
    start = datetime(year, month, 1, tzinfo=CST)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=CST)
    else:
        end = datetime(year, month + 1, 1, tzinfo=CST)
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())
    return [d for d in dynamics if start_ts <= d.get("pub_ts", 0) < end_ts]


# ──────────────────────────────────────────
# Like Dynamic
# ──────────────────────────────────────────

def like_dynamic(dyn_id: str, sessdata: str, bili_jct: str) -> Dict:
    url = "https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb"
    data = {
        "dynamic_id": dyn_id,
        "up": "1",
        "csrf": bili_jct,
        "csrf_token": bili_jct,
    }
    headers = _make_headers(sessdata, bili_jct, "https://t.bilibili.com")
    headers["Origin"] = "https://t.bilibili.com"
    resp = _post(url, data, headers)

    if resp and resp.get("code") == 0:
        return {"success": True}
    already = resp and resp.get("code") in (65006, 500)
    return {
        "success": already,
        "already_done": already,
        "error": None if already else (resp.get("message", "未知错误") if resp else "请求失败"),
    }


# ──────────────────────────────────────────
# Batch Processing
# ──────────────────────────────────────────

def process_member_dynamics(member: Dict, dynamics: List[Dict],
                            sessdata: str, bili_jct: str,
                            delay: float = 8) -> List[Dict]:
    results = []
    for i, d in enumerate(dynamics):
        r = like_dynamic(d["dyn_id"], sessdata, bili_jct)
        results.append({
            "member": member["name"],
            "dyn_id": d["dyn_id"],
            "type": d["type_name"],
            "text": d["text"],
            "pub_ts": d["pub_ts"],
            "url": f"https://t.bilibili.com/{d['dyn_id']}",
            **r,
        })
        if i < len(dynamics) - 1:
            time.sleep(delay)
    return results


def parse_month(s: str) -> Tuple[int, int]:
    import re
    s = s.strip()
    if re.match(r"^\d{4}[-/]\d{1,2}$", s):
        parts = re.split(r"[-/]", s)
        return int(parts[0]), int(parts[1])
    if re.match(r"^\d{1,2}$", s):
        now = datetime.now(CST)
        return now.year, int(s)
    raise ValueError(f"无法解析月份: {s}")


def format_output(all_results: List[Dict]) -> str:
    lines = ["🌟 A-SOUL 动态点赞结果", ""]

    total = 0
    new_likes = 0
    current_member = None

    for r in all_results:
        if r["member"] != current_member:
            current_member = r["member"]
            lines.append(f"  👤 {current_member}:")

        total += 1
        dt = datetime.fromtimestamp(r["pub_ts"], CST).strftime("%m-%d")
        text_short = r["text"][:25] + ("..." if len(r["text"]) > 25 else "")

        if r.get("success"):
            if r.get("already_done"):
                icon = "👍⏭"
            else:
                icon = "👍✅"
                new_likes += 1
        else:
            icon = "👍❌"

        lines.append(f"    [{dt}] [{r['type']}] {text_short}  {icon}")

    lines.append("")
    lines.append(f"📊 共处理 {total} 条动态，新点赞 {new_likes} 条")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="A-SOUL 动态点赞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 给本月动态全部点赞
  python3 dynamics.py --month 3

  # 给最近7天动态点赞
  python3 dynamics.py --days 7

  # 只给嘉然的动态点赞
  python3 dynamics.py --month 3 --members 嘉然
""",
    )
    parser.add_argument("--month", help="指定月份（如 3、03、2026-03）")
    parser.add_argument("--days", type=int, help="最近 N 天的动态")
    parser.add_argument("--members", help="指定成员（逗号分隔）")
    parser.add_argument("--delay", type=float, default=8, help="动态之间的间隔秒数（默认 8）")
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    if not args.month and not args.days:
        print("❌ 请指定 --month 或 --days")
        sys.exit(1)

    sessdata = args.sessdata
    bili_jct = args.bili_jct
    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到 Cookie。")
            sys.exit(1)

    targets = MEMBERS
    if args.members:
        names = [n.strip() for n in args.members.split(",")]
        targets = [m for m in MEMBERS if m["name"] in names]
        if not targets:
            print(f"❌ 未找到成员: {args.members}")
            sys.exit(1)

    all_results = []
    for member in targets:
        print(f"  📡 正在获取 {member['name']} 的动态...", file=sys.stderr)
        dynamics = fetch_user_dynamics(member["uid"], sessdata, bili_jct)

        if args.month:
            year, month = parse_month(args.month)
            dynamics = filter_by_month(dynamics, year, month)
        elif args.days:
            dynamics = filter_by_days(dynamics, args.days)

        if not dynamics:
            print(f"  ℹ️  {member['name']} 在指定时间段内没有新动态", file=sys.stderr)
            continue

        print(f"  💬 找到 {len(dynamics)} 条动态，开始点赞...", file=sys.stderr)
        results = process_member_dynamics(member, dynamics, sessdata, bili_jct, delay=args.delay)
        all_results.extend(results)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        if all_results:
            print(format_output(all_results))
        else:
            print("ℹ️  指定时间段内没有找到任何动态")


if __name__ == "__main__":
    main()
