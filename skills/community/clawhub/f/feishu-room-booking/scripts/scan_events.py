#!/usr/bin/env python3
"""
扫描用户日程，找出缺少会议室的日程并自动补订

用法:
  # 扫描未来24小时缺会议室的日程（dry-run 模式，不实际预订）
  python3 scan_events.py --user "ou_xxx" --hours 24 --dry-run

  # 扫描并自动补订（使用用户偏好）
  python3 scan_events.py --user "ou_xxx" --hours 24 --auto-book

  # 扫描指定日期范围
  python3 scan_events.py --user "ou_xxx" --start "2026-04-20T00:00:00+08:00" --end "2026-04-20T23:59:59+08:00" --auto-book

输出: JSON 格式，列出缺会议室的日程和建议方案
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import workspace_manager
from booking_verifier import (
    classify_event_for_scan,
    get_self_attendee_status,
    get_attendee_identifier,
    is_self_attendee,
    normalize_status_value,
)

PREFS_FILE = SCRIPT_DIR.parent / "references" / "user-preferences.json"
WAITLIST_FILE = SCRIPT_DIR.parent / "references" / "room-waitlist.json"


def load_json(filepath: Path, default: Optional[dict] = None) -> dict:
    if not filepath.exists():
        return default or {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath: Path, data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_preferences(user_id: str) -> dict:
    """读取用户偏好"""
    prefs = load_json(PREFS_FILE, {"preferences": {}})
    return prefs.get("preferences", {}).get(user_id, {})


def get_default_building_for_user(user_id: str, target_date: Optional[str] = None) -> str:
    preferences = get_user_preferences(user_id)
    default_building = preferences.get("default_building", "")
    if isinstance(default_building, str) and default_building:
        return default_building

    workspace_data = workspace_manager.load_workspace()
    resolved_workspace = workspace_manager.resolve_workspace_for_date(
        workspace_data,
        target_date or datetime.now().date().isoformat(),
    )
    return resolved_workspace or ""


def parse_events_from_list_output(output: Any) -> list[dict[str, Any]]:
    """从 feishu_calendar_event list 的输出中解析日程"""
    try:
        data = json.loads(output) if isinstance(output, str) else output
    except json.JSONDecodeError:
        return []

    if not isinstance(data, dict):
        return []

    events = data.get("events", [])
    if not isinstance(events, list):
        return []
    return [event for event in events if isinstance(event, dict)]


def get_event_datetime(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        datetime_value = value.get("datetime")
        if isinstance(datetime_value, str):
            return datetime_value
        date_value = value.get("date")
        if isinstance(date_value, str):
            return date_value
    return ""



def parse_event_datetime(value: str) -> Optional[datetime]:
    if not isinstance(value, str) or len(value) == 10:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None



def is_all_day_event(event: dict) -> bool:
    start = get_event_datetime(event.get("start_time"))
    end = get_event_datetime(event.get("end_time"))
    if not start:
        return False
    if len(start) == 10 or len(end) == 10:
        return True

    start_dt = parse_event_datetime(start)
    end_dt = parse_event_datetime(end)
    if not start_dt or not end_dt:
        return False

    return (
        start_dt.date() == end_dt.date()
        and start_dt.hour == 0
        and start_dt.minute == 0
        and start_dt.second == 0
        and end_dt.hour == 23
        and end_dt.minute == 59
        and end_dt.second == 59
    )



SCAN_REASON_MESSAGES = {
    "self_not_accepted": (False, "当前用户尚未接受会议"),
    "self_status_missing": (False, "当前用户接受状态待确认"),
    "already_has_confirmed_room": (False, "已有会议室"),
    "room_pending": (False, "会议室状态待确认"),
    "room_declined": (True, "会议室预订失败，需要补订"),
    "needs_room": (True, "需要补订会议室"),
}


PENDING_SCAN_REASONS = {"self_status_missing", "room_pending"}


def evaluate_scan_result(event: dict, user_id: str) -> dict[str, Any]:
    if is_all_day_event(event):
        return {
            "should_book": False,
            "verification_status": "failed",
            "reason_code": "all_day_event",
            "reason": "",
        }

    classification = classify_event_for_scan(event, user_id)
    should_book, reason = SCAN_REASON_MESSAGES.get(
        classification["reason"],
        (False, "会议状态待确认"),
    )
    return {
        "should_book": should_book,
        "verification_status": classification["status"],
        "reason_code": classification["reason"],
        "reason": reason,
    }


def needs_room(event: dict, user_id: str) -> tuple[bool, str]:
    """判断日程是否需要补订会议室"""
    result = evaluate_scan_result(event, user_id)
    return result["should_book"], result["reason"]


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描缺会议室的日程")
    parser.add_argument("--user", "-u", help="用户 open_id")
    parser.add_argument("--hours", type=int, default=24, help="扫描未来 N 小时")
    parser.add_argument("--start", "-s", help="开始时间")
    parser.add_argument("--end", "-e", help="结束时间")
    parser.add_argument("--dry-run", action="store_true", help="只扫描不预订")
    parser.add_argument("--auto-book", action="store_true", help="自动补订会议室")
    parser.add_argument("--events-file", help="日程 JSON 文件路径（agent 传入）")
    parser.add_argument("--output", "-o", choices=["json", "table"], default="table")

    args = parser.parse_args()

    # 计算时间范围
    now = datetime.now()
    if args.start:
        time_min = args.start
    else:
        time_min = (now + timedelta(hours=0)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    if args.end:
        time_max = args.end
    else:
        time_max = (now + timedelta(hours=args.hours)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    if not args.user:
        print("错误: 必须指定 --user")
        sys.exit(1)

    # 获取用户偏好
    prefs = get_user_preferences(args.user)
    default_building = get_default_building_for_user(args.user, time_min[:10])
    capacity_gte = prefs.get("capacity_gte", 0)

    # 注意：实际日程获取需要通过飞书 API 或工具
    # 这里输出扫描参数，由 agent 调用飞书工具获取日程后传入
    scan_config = {
        "user_id": args.user,
        "time_min": time_min,
        "time_max": time_max,
        "default_building": default_building,
        "capacity_gte": capacity_gte,
        "dry_run": args.dry_run,
        "auto_book": args.auto_book,
    }

    if args.output != "json":
        print(f"🔍 扫描日程: {time_min} ~ {time_max}")
        if default_building:
            print(f"🏠 默认楼栋: {default_building} (容量≥{capacity_gte})")
        print()
        print("📋 扫描配置:")
        print(json.dumps(scan_config, ensure_ascii=False, indent=2))
        print()
        print("⚠️ 此脚本需要配合 agent 使用。agent 应:")
        print("  1. 调用 feishu_calendar_event list 获取日程")
        print("  2. 传入 --events-file 参数进行分析")
        print()
        print("完整用法: 先导出日程到 JSON，再传入分析")
        print(f"  feishu_calendar_event list → 保存到 /tmp/events.json")
        print(f"  python3 scan_events.py --user {args.user} --events-file /tmp/events.json --dry-run")

    # 支持 events-file 模式：agent 传入已获取的日程 JSON
    if args.events_file:
        try:
            with open(args.events_file, "r", encoding="utf-8") as f:
                raw_events = json.load(f)
                events = raw_events if isinstance(raw_events, list) else parse_events_from_list_output(raw_events)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"错误: 无法读取 events 文件: {exc}", file=sys.stderr)
            sys.exit(1)

        needs = []
        pending_verification = []
        for event in events:
            scan_result = evaluate_scan_result(event, args.user)
            if scan_result["should_book"]:
                needs.append({
                    "event_id": event.get("event_id", ""),
                    "summary": event.get("summary", ""),
                    "start_time": event.get("start_time", ""),
                    "end_time": event.get("end_time", ""),
                    "organizer": event.get("event_organizer", {}).get("display_name", ""),
                    "reason": scan_result["reason"],
                    "verification_status": scan_result["verification_status"],
                })
                continue

            if scan_result["reason_code"] in PENDING_SCAN_REASONS:
                pending_verification.append({
                    "event_id": event.get("event_id", ""),
                    "summary": event.get("summary", ""),
                    "start_time": event.get("start_time", ""),
                    "end_time": event.get("end_time", ""),
                    "organizer": event.get("event_organizer", {}).get("display_name", ""),
                    "reason": scan_result["reason"],
                    "verification_status": scan_result["verification_status"],
                })

        if args.output == "json":
            print(json.dumps({
                "scan_config": scan_config,
                "needs": needs,
                "pending_verification": pending_verification,
            }, ensure_ascii=False, indent=2))
            return

        if not needs and not pending_verification:
            print("✅ 所有日程都已安排会议室")
            return

        if needs:
            print(f"找到 {len(needs)} 个需要补订会议室的日程:")
            for n in needs:
                print(f"  📌 {n['summary']}")
                print(f"     时间: {n['start_time']} ~ {n['end_time']}")
                print(f"     组织者: {n['organizer']}")
                print(f"     状态: {n['verification_status']}")

        if pending_verification:
            print(f"\n有 {len(pending_verification)} 个日程需要二次确认:")
            for item in pending_verification:
                print(f"  ⏳ {item['summary']}")
                print(f"     时间: {item['start_time']} ~ {item['end_time']}")
                print(f"     原因: {item['reason']}")

    if args.output == "json":
        print(json.dumps({"scan_config": scan_config}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
