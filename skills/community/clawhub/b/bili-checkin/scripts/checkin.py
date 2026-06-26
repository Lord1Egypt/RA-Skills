#!/usr/bin/env python3
"""
Bilibili 直播间签到 — 通过 API 发送弹幕。
不依赖浏览器自动化，直接调用 Bilibili 接口，更快更稳定。
零外部依赖。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
_COOKIE_FILE = Path(__file__).resolve().parent.parent / ".cookies.json"
_SEND_URL = "https://api.live.bilibili.com/msg/send"


def load_cookies() -> Optional[Dict[str, str]]:
    """从本地文件读取保存的 cookie"""
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


def save_cookies(sessdata: str, bili_jct: str):
    """保存 cookie 到本地文件"""
    data = {"SESSDATA": sessdata, "bili_jct": bili_jct}
    with open(_COOKIE_FILE, "w") as f:
        json.dump(data, f)
    os.chmod(_COOKIE_FILE, 0o600)
    print(f"💾 Cookie 已保存到 {_COOKIE_FILE}", file=sys.stderr)


def send_danmaku(room_id: int, msg: str, sessdata: str, bili_jct: str) -> Dict:
    """通过 API 发送直播间弹幕"""
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
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"code": e.code, "message": f"HTTP {e.code}", "data": body}
    except Exception as e:
        return {"code": -1, "message": str(e)}


def verify_user(sessdata: str, bili_jct: str) -> Optional[Dict]:
    """验证 cookie 是否有效，返回用户信息"""
    url = "https://api.bilibili.com/x/web-interface/nav"
    headers = {
        "User-Agent": _UA,
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") == 0:
            info = data.get("data", {})
            return {
                "uid": info.get("mid"),
                "name": info.get("uname"),
                "level": info.get("level_info", {}).get("current_level"),
                "is_login": info.get("isLogin", False),
            }
    except Exception:
        pass
    return None


def get_room_title(room_id: int) -> str:
    """获取直播间标题/主播名"""
    url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
    headers = {"User-Agent": _UA}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") == 0:
            return data.get("data", {}).get("title", "")
    except Exception:
        pass
    return ""


def get_anchor_name(room_id: int) -> str:
    """获取主播名"""
    url = f"https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={room_id}"
    headers = {"User-Agent": _UA}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") == 0:
            return data.get("data", {}).get("info", {}).get("uname", "")
    except Exception:
        pass
    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Bilibili 直播间弹幕签到（API 模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 首次使用，保存 cookie
  python3 checkin.py --save-cookie --sessdata "YOUR_SESSDATA" --bili-jct "YOUR_BILI_JCT"

  # 签到（使用已保存的 cookie）
  python3 checkin.py --room 30858592
  python3 checkin.py --room 30858592 --msg "打卡"

  # 签到多个直播间
  python3 checkin.py --room 30858592,22637261 --msg "签到"

  # 验证 cookie 是否有效
  python3 checkin.py --verify
""",
    )
    parser.add_argument("--room", help="直播间 room_id，多个用逗号分隔")
    parser.add_argument("--msg", default="签到", help="弹幕内容（默认：签到）")
    parser.add_argument("--sessdata", help="SESSDATA cookie 值")
    parser.add_argument("--bili-jct", help="bili_jct cookie 值")
    parser.add_argument("--save-cookie", action="store_true", help="保存 cookie 到本地")
    parser.add_argument("--verify", action="store_true", help="验证 cookie 是否有效")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    sessdata = args.sessdata
    bili_jct = args.bili_jct

    if args.save_cookie:
        if not sessdata or not bili_jct:
            print("❌ --save-cookie 需要同时提供 --sessdata 和 --bili-jct", file=sys.stderr)
            sys.exit(1)
        save_cookies(sessdata, bili_jct)
        user = verify_user(sessdata, bili_jct)
        if user and user.get("is_login"):
            print(f"✅ Cookie 有效！用户：{user['name']} (UID:{user['uid']}, Lv{user['level']})")
        else:
            print("⚠️ Cookie 已保存但验证失败，可能已过期")
        return

    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到保存的 Cookie。请先运行：")
            print("")
            print("  python3 checkin.py --save-cookie --sessdata \"你的SESSDATA\" --bili-jct \"你的bili_jct\"")
            print("")
            print("获取方法：")
            print("  1. 在 Chrome 中打开 bilibili.com（确保已登录）")
            print("  2. 按 F12 打开开发者工具")
            print("  3. 切到 Application → Cookies → bilibili.com")
            print("  4. 找到 SESSDATA 和 bili_jct，复制它们的值")
            sys.exit(1)

    if args.verify:
        user = verify_user(sessdata, bili_jct)
        if user and user.get("is_login"):
            print(f"✅ Cookie 有效！用户：{user['name']} (UID:{user['uid']}, Lv{user['level']})")
        else:
            print("❌ Cookie 无效或已过期，请重新获取并保存")
        return

    if not args.room:
        print("❌ 请指定直播间 room_id，例如：--room 30858592", file=sys.stderr)
        sys.exit(1)

    room_ids = [int(r.strip()) for r in args.room.split(",") if r.strip().isdigit()]
    if not room_ids:
        print("❌ 无效的 room_id", file=sys.stderr)
        sys.exit(1)

    results = []
    for room_id in room_ids:
        anchor = get_anchor_name(room_id)
        resp = send_danmaku(room_id, args.msg, sessdata, bili_jct)

        success = resp.get("code") == 0
        result = {
            "room_id": room_id,
            "anchor": anchor,
            "url": f"https://live.bilibili.com/{room_id}",
            "msg": args.msg,
            "success": success,
            "response": resp,
        }
        results.append(result)

        if not args.json:
            if success:
                print(f"✅ 签到成功！")
                print(f"")
                print(f"  🏠 主播：{anchor}")
                print(f"  🔗 直播间：https://live.bilibili.com/{room_id}")
                print(f"  💬 弹幕：{args.msg}")
                print(f"  📈 预计亲密度 +2，经验值 +5")
                print(f"")
                print(f"  👉 点击上方链接可验证签到结果")
            else:
                err_msg = resp.get("message", resp.get("msg", "未知错误"))
                print(f"❌ 签到失败！")
                print(f"")
                print(f"  🏠 主播：{anchor}")
                print(f"  🔗 直播间：https://live.bilibili.com/{room_id}")
                print(f"  ❗ 原因：{err_msg}")
                if "login" in str(err_msg).lower() or resp.get("code") == -101:
                    print(f"  💡 Cookie 可能已过期，请重新获取")
                elif "msg in 1s" in str(resp.get("data", {}).get("message", "")):
                    print(f"  💡 发送太频繁，请稍后再试")

        if len(room_ids) > 1:
            time.sleep(2)
            if not args.json:
                print("")

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
