#!/usr/bin/env python3
"""
Bilibili UP主 → 直播间查询工具。
支持 UID、用户名、直播间链接三种输入。
零依赖，纯标准库。
"""

import json
import re
import sys
import urllib.request
import urllib.parse
import uuid
from http.cookiejar import CookieJar
from typing import Optional, Dict

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

_cookie_jar = CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cookie_jar))
_cookies_initialized = False


def _ensure_cookies():
    """Bilibili 搜索 API 需要 buvid3 cookie，先访问首页获取"""
    global _cookies_initialized
    if _cookies_initialized:
        return
    try:
        req = urllib.request.Request(
            "https://www.bilibili.com",
            headers={"User-Agent": _UA},
        )
        _opener.open(req, timeout=5)
    except Exception:
        pass
    _cookies_initialized = True


def _get_json(url: str, timeout: int = 10, need_cookie: bool = False) -> Optional[Dict]:
    headers = {
        "User-Agent": _UA,
        "Referer": "https://www.bilibili.com",
    }
    if need_cookie:
        _ensure_cookies()
    req = urllib.request.Request(url, headers=headers)
    try:
        opener = _opener if need_cookie else urllib.request.build_opener()
        with opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return None


def get_live_room_by_uid(uid: int) -> Optional[Dict]:
    """通过 UID 查询直播间信息"""
    url = f"https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={uid}"
    data = _get_json(url)
    if not data or data.get("code") != 0:
        return None
    info = data.get("data", {})
    if not info.get("roomid"):
        return None
    return {
        "uid": uid,
        "room_id": info["roomid"],
        "url": f"https://live.bilibili.com/{info['roomid']}",
        "title": info.get("title", ""),
        "live_status": "直播中" if info.get("roomStatus") == 1 and info.get("liveStatus") == 1 else "未开播",
        "cover": info.get("cover", ""),
    }


def search_user(keyword: str, limit: int = 5) -> list:
    """通过用户名搜索UP主，返回匹配列表。先尝试带 cookie 的搜索 API，失败则尝试 suggest API。"""
    results = _search_via_api(keyword, limit)
    if results:
        return results
    return _search_via_suggest(keyword, limit)


def _search_via_api(keyword: str, limit: int = 5) -> list:
    """搜索 API（需要 cookie 绕过 412）"""
    encoded = urllib.parse.quote(keyword)
    url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword={encoded}"
    data = _get_json(url, need_cookie=True)
    if not data or data.get("code") != 0:
        return []

    results = []
    for item in (data.get("data", {}).get("result") or [])[:limit]:
        uid = item.get("mid", 0)
        name = item.get("uname", "")
        name = re.sub(r"<[^>]+>", "", name)
        fans = item.get("fans", 0)
        results.append({
            "uid": uid,
            "name": name,
            "fans": fans,
            "fans_display": _human_fans(fans),
        })
    return results


def _search_via_suggest(keyword: str, limit: int = 5) -> list:
    """备用：搜索建议 API（不需要 cookie，但结果不如主 API 精确）"""
    encoded = urllib.parse.quote(keyword)
    url = f"https://s.search.bilibili.com/main/suggest?term={encoded}&main_ver=v1&highlight="
    data = _get_json(url)
    if not data or "result" not in data:
        return []

    results = []
    for tag_group in data.get("result", {}).get("tag", [])[:limit]:
        name = tag_group.get("value", "")
        ref = tag_group.get("ref", 0)
        if name and ref:
            results.append({
                "uid": ref,
                "name": name,
                "fans": 0,
                "fans_display": "未知",
            })
    return results


def _human_fans(n: int) -> str:
    if n >= 10000:
        return f"{n / 10000:.1f}万"
    return str(n)


def parse_input(text: str) -> dict:
    """
    智能解析用户输入，返回查询结果。

    支持三种格式:
      1. 纯数字 → 当作 UID
      2. live.bilibili.com/xxx → 提取 room_id
      3. 其他 → 当作用户名搜索
    """
    text = text.strip()

    if text.isdigit():
        uid = int(text)
        room = get_live_room_by_uid(uid)
        if room:
            return {"type": "found", "data": room}
        return {"type": "error", "message": f"UID {uid} 没有开通直播间"}

    if "live.bilibili.com" in text:
        m = re.search(r"live\.bilibili\.com/(\d+)", text)
        if m:
            room_id = m.group(1)
            return {
                "type": "found",
                "data": {
                    "room_id": int(room_id),
                    "url": f"https://live.bilibili.com/{room_id}",
                    "title": "",
                    "live_status": "未知",
                }
            }
        return {"type": "error", "message": f"无法从链接中解析 room_id: {text}"}

    if "space.bilibili.com" in text:
        m = re.search(r"space\.bilibili\.com/(\d+)", text)
        if m:
            uid = int(m.group(1))
            room = get_live_room_by_uid(uid)
            if room:
                return {"type": "found", "data": room}
            return {"type": "error", "message": f"UID {uid} 没有开通直播间"}

    users = search_user(text)
    if not users:
        return {"type": "error", "message": f"找不到用户: {text}"}

    if len(users) == 1:
        room = get_live_room_by_uid(users[0]["uid"])
        if room:
            room["name"] = users[0]["name"]
            return {"type": "found", "data": room}
        return {"type": "error", "message": f"用户 {users[0]['name']} 没有开通直播间"}

    results = []
    for u in users:
        room = get_live_room_by_uid(u["uid"])
        results.append({
            "uid": u["uid"],
            "name": u["name"],
            "fans": u["fans_display"],
            "has_live": room is not None,
            "room_id": room["room_id"] if room else None,
            "url": room["url"] if room else None,
            "live_status": room["live_status"] if room else "无直播间",
        })

    return {"type": "multiple", "data": results}


def format_output(result: dict) -> str:
    if result["type"] == "error":
        return f"❌ {result['message']}"

    if result["type"] == "found":
        d = result["data"]
        lines = ["✅ 找到直播间", ""]
        if d.get("name"):
            lines.append(f"  UP主：{d['name']}")
        if d.get("uid"):
            lines.append(f"  UID：{d['uid']}")
        lines.append(f"  房间号：{d['room_id']}")
        lines.append(f"  链接：{d['url']}")
        if d.get("title"):
            lines.append(f"  标题：{d['title']}")
        lines.append(f"  状态：{d.get('live_status', '未知')}")
        return "\n".join(lines)

    if result["type"] == "multiple":
        lines = ["🔍 找到多个匹配用户：", ""]
        for i, u in enumerate(result["data"], 1):
            status = u["live_status"]
            if u["has_live"]:
                lines.append(f"  {i}. {u['name']} (UID:{u['uid']}, 粉丝:{u['fans']}) — {u['url']} [{status}]")
            else:
                lines.append(f"  {i}. {u['name']} (UID:{u['uid']}, 粉丝:{u['fans']}) — 无直播间")
        lines.append("")
        lines.append("请告诉我要签到哪一个（输入编号或名字）")
        return "\n".join(lines)

    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="查询B站UP主的直播间信息")
    parser.add_argument("query", help="UP主名字、UID、直播间链接、或个人空间链接")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    result = parse_input(args.query)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
