#!/usr/bin/env python3
"""
Brown Dust 2 — Web Shop 签到（每日 + 每周 + 活动出席）。
通过官方 API 实现，需要 accessToken。
零外部依赖。
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Optional

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

_API_BASE = "https://bd2-webshop-api.bd2.pmang.cloud"

_ATTEND_DAILY = 0
_ATTEND_WEEKLY = 1

_TOKEN_FILE = Path(__file__).resolve().parent.parent / ".token"


def save_token(token: str):
    _TOKEN_FILE.write_text(token.strip())
    _TOKEN_FILE.chmod(0o600)
    print("💾 Token 已保存", file=sys.stderr)


def load_token() -> Optional[str]:
    if _TOKEN_FILE.exists():
        t = _TOKEN_FILE.read_text().strip()
        if t:
            return t
    return None


def _api(method: str, path: str, token: str, body: Optional[dict] = None) -> Dict:
    url = f"{_API_BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body else None

    headers = {
        "User-Agent": _UA,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body_text)
        except Exception:
            return {"code": "FAIL", "message": f"HTTP {e.code}: {body_text[:200]}"}
    except Exception as e:
        return {"code": "FAIL", "message": str(e)}


def get_event_info() -> Dict:
    """获取当前活动信息（不需要 token）"""
    url = f"{_API_BASE}/api/event/event-info"
    req = urllib.request.Request(url, headers={
        "User-Agent": _UA,
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("data", {})
    except Exception as e:
        return {"error": str(e)}


def do_daily_attend(token: str) -> Dict:
    """每日签到"""
    resp = _api("POST", "/api/user/attend", token, {"type": _ATTEND_DAILY})
    data = resp.get("data", resp)
    success = data.get("success", False) if isinstance(data, dict) else False
    return {
        "task": "daily_attend",
        "success": success,
        "raw": resp,
    }


def do_weekly_attend(token: str) -> Dict:
    """每周签到"""
    resp = _api("POST", "/api/user/attend", token, {"type": _ATTEND_WEEKLY})
    data = resp.get("data", resp)
    success = data.get("success", False) if isinstance(data, dict) else False
    return {
        "task": "weekly_attend",
        "success": success,
        "raw": resp,
    }


def get_event_user_info(token: str) -> Dict:
    """获取用户活动出席状态"""
    resp = _api("POST", "/api/event/event-user-info", token)
    return resp.get("data", resp)


def do_event_attend(token: str, schedule_id: int) -> Dict:
    """活动出席签到"""
    resp = _api("POST", "/api/event/attend-reward", token, {"eventScheduleId": schedule_id})
    data = resp.get("data", resp)
    success = data.get("success", False) if isinstance(data, dict) else False
    return {
        "task": "event_attend",
        "success": success,
        "schedule_id": schedule_id,
        "raw": resp,
    }


def get_products_info(token: str) -> Dict:
    """获取商品列表（检查是否已签到）"""
    resp = _api("GET", "/api/products?countryCode=zh-TW&order=sales", token)
    return resp.get("data", resp)


def run_all(token: str, skip_event: bool = False) -> Dict:
    results = []
    errors = []

    # 1) Daily attend
    r = do_daily_attend(token)
    results.append(r)
    if not r["success"]:
        raw_msg = r.get("raw", {})
        if isinstance(raw_msg, dict):
            msg = raw_msg.get("message", "") or raw_msg.get("data", {}).get("errorMsg", "")
        else:
            msg = str(raw_msg)
        if "Unauthorized" in str(msg):
            return {"error": "Token 无效或已过期，请重新获取", "results": results}

    time.sleep(0.5)

    # 2) Weekly attend
    r = do_weekly_attend(token)
    results.append(r)

    time.sleep(0.5)

    # 3) Event attend
    if not skip_event:
        event_info = get_event_info()
        schedule = event_info.get("scheduleInfo", {})
        schedule_id = schedule.get("eventScheduleId", 0)

        if schedule_id > 0:
            user_event = get_event_user_info(token)
            count = user_event.get("attendanceCount", -1)
            is_last = user_event.get("isLastAttendance", False)
            can_attend = count >= 0 and not is_last

            reward_list = schedule.get("rewardInfoList", [])
            total_days = len(reward_list)

            results.append({
                "task": "event_info",
                "success": True,
                "schedule_id": schedule_id,
                "start": schedule.get("startDate", ""),
                "end": schedule.get("endDate", ""),
                "attended_days": count,
                "total_days": total_days,
                "can_attend_today": can_attend,
            })

            if can_attend:
                time.sleep(0.5)
                r = do_event_attend(token, schedule_id)
                results.append(r)
            else:
                results.append({
                    "task": "event_attend",
                    "success": True,
                    "message": f"今日活动已签到 ({count}/{total_days}天)" if is_last or count >= total_days else f"已完成全部 {total_days} 天活动",
                })
        else:
            results.append({
                "task": "event_attend",
                "success": True,
                "message": "当前没有进行中的出席活动",
            })

    return {"results": results}


def format_output(data: Dict) -> str:
    lines = ["🎮 Brown Dust 2 Web Shop 签到结果", ""]

    if "error" in data:
        lines.append(f"❌ {data['error']}")
        return "\n".join(lines)

    for r in data.get("results", []):
        task = r.get("task", "")
        success = r.get("success", False)

        if task == "daily_attend":
            if success:
                lines.append("  ✅ 每日签到 — 成功！")
            else:
                raw = r.get("raw", {})
                msg = ""
                if isinstance(raw, dict):
                    msg = raw.get("message", "") or str(raw.get("data", {}).get("errorMsg", ""))
                lines.append(f"  ⚠️  每日签到 — {msg or '已签到或失败'}")

        elif task == "weekly_attend":
            if success:
                lines.append("  ✅ 每周签到 — 成功！")
            else:
                raw = r.get("raw", {})
                msg = ""
                if isinstance(raw, dict):
                    msg = raw.get("message", "") or str(raw.get("data", {}).get("errorMsg", ""))
                lines.append(f"  ⚠️  每周签到 — {msg or '已签到或失败'}")

        elif task == "event_info":
            days = r.get("attended_days", 0)
            total = r.get("total_days", 0)
            start = r.get("start", "")
            end = r.get("end", "")
            lines.append(f"  📅 活动出席 — {start} ~ {end}")
            lines.append(f"     已签 {days}/{total} 天")

        elif task == "event_attend":
            if "message" in r:
                lines.append(f"  ⏭️  活动出席 — {r['message']}")
            elif success:
                lines.append("  ✅ 活动出席 — 今日签到成功！")
            else:
                raw = r.get("raw", {})
                msg = ""
                if isinstance(raw, dict):
                    msg = raw.get("message", "") or str(raw.get("data", {}).get("errorMsg", ""))
                lines.append(f"  ❌ 活动出席 — {msg or '失败'}")

    lines.append("")
    lines.append("📬 奖励已发送到游戏内邮箱，重启游戏后领取！")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Brown Dust 2 Web Shop 签到",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 保存 accessToken（只需一次，过期后重新保存）
  python3 signin.py --save-token "eyJhbGci..."

  # 执行全部签到（每日+每周+活动）
  python3 signin.py

  # 只做每日签到
  python3 signin.py --daily-only

  # 手动指定 token
  python3 signin.py --token "eyJhbGci..."

  # 查看当前活动信息
  python3 signin.py --event-info

  # JSON 输出
  python3 signin.py --json
""",
    )
    parser.add_argument("--token", help="accessToken (Bearer token)")
    parser.add_argument("--save-token", help="保存 token 到本地")
    parser.add_argument("--daily-only", action="store_true", help="仅执行每日签到")
    parser.add_argument("--event-info", action="store_true", help="查看当前活动信息")
    parser.add_argument("--skip-event", action="store_true", help="跳过活动出席签到")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.save_token:
        save_token(args.save_token)
        print("✅ Token 已保存")
        return

    if args.event_info:
        info = get_event_info()
        if args.json:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            schedule = info.get("scheduleInfo", {})
            if schedule.get("eventScheduleId", 0) > 0:
                print(f"📅 当前活动: {schedule.get('startDate', '')} ~ {schedule.get('endDate', '')}")
                print(f"   活动ID: {schedule.get('eventScheduleId', 0)}")
                rewards = schedule.get("rewardInfoList", [])
                print(f"   总天数: {len(rewards)} 天")
            else:
                print("当前没有进行中的出席活动")
        return

    token = args.token
    if not token:
        token = load_token()
    if not token:
        print("❌ 需要 accessToken。请运行：")
        print("")
        print('  python3 signin.py --save-token "你的accessToken"')
        print("")
        print("获取方式：在已登录的 Web Shop 页面，按 F12 → Console → 输入：")
        print('  JSON.parse(localStorage.getItem("session-storage")).state.session.accessToken')
        sys.exit(1)

    if args.daily_only:
        r = do_daily_attend(token)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            if r["success"]:
                print("✅ 每日签到成功！奖励已发送到游戏内邮箱。")
            else:
                print(f"⚠️  每日签到: {r.get('raw', {}).get('message', '已签到或失败')}")
        return

    results = run_all(token, skip_event=args.skip_event)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()
