#!/usr/bin/env python3
"""
工区时间线管理

用法:
  python3 workspace_manager.py --get
  python3 workspace_manager.py --set --workspace "丽金智地中心 B座"
  python3 workspace_manager.py --set --workspace "紫金" --from "2026-04-30"
  python3 workspace_manager.py --set --workspace "紫金" --from "2026-04-30" --to "2026-05-02"
  python3 workspace_manager.py --set-next --workspace "紫金数码园4号楼"
  python3 workspace_manager.py --recommend
  python3 workspace_manager.py --check-friday-reminder
  python3 workspace_manager.py --clear-next
  python3 workspace_manager.py --timeline
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_FILE = SCRIPT_DIR.parent / "references" / "weekly-workspace.json"
PREFS_FILE = SCRIPT_DIR.parent / "references" / "user-preferences.json"


def load_workspace(filepath: Optional[Path] = None) -> dict[str, Any]:
    resolved_path = filepath or WORKSPACE_FILE
    if not resolved_path.exists():
        return {"segments": [], "next_week": None}
    with open(resolved_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_workspace(data: dict[str, Any], filepath: Optional[Path] = None) -> None:
    resolved_path = filepath or WORKSPACE_FILE
    with open(resolved_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_preferences(filepath: Optional[Path] = None) -> dict[str, Any]:
    resolved_path = filepath or PREFS_FILE
    if not resolved_path.exists():
        return {"preferences": {}}
    with open(resolved_path, "r", encoding="utf-8") as file:
        return json.load(file)


def today_string() -> str:
    return date.today().isoformat()


def week_start_for(day: date) -> date:
    return day - timedelta(days=day.weekday())


def week_end_for(day: date) -> date:
    return week_start_for(day) + timedelta(days=6)


def shift_date(date_str: str, days: int) -> str:
    return (date.fromisoformat(date_str) + timedelta(days=days)).isoformat()


def weekday_name(date_str: str) -> str:
    names = ["一", "二", "三", "四", "五", "六", "日"]
    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return ""
    return f"周{names[day.weekday()]}"


def find_segment(data: dict[str, Any], target_date: str) -> Optional[dict[str, Any]]:
    matches = [
        segment
        for segment in data.get("segments", [])
        if segment.get("from", "") <= target_date <= segment.get("to", "")
    ]
    if not matches:
        return None
    return max(matches, key=lambda segment: segment.get("to", ""))


def find_current_workspace(data: dict[str, Any], target_date: Optional[str] = None) -> Optional[str]:
    segment = find_segment(data, target_date or today_string())
    if not segment:
        return None
    workspace = segment.get("workspace")
    return workspace if isinstance(workspace, str) and workspace else None


def resolve_workspace_for_date(data: dict[str, Any], target_date: Optional[str] = None) -> Optional[str]:
    resolved_date = target_date or today_string()
    current_workspace = find_current_workspace(data, resolved_date)
    if current_workspace:
        return current_workspace

    next_week = data.get("next_week")
    if not isinstance(next_week, dict):
        return None

    workspace = next_week.get("workspace")
    week_start = next_week.get("week_start")
    if not isinstance(workspace, str) or not workspace:
        return None
    if not isinstance(week_start, str) or not week_start:
        return None

    try:
        week_start_date = date.fromisoformat(week_start)
        target = date.fromisoformat(resolved_date)
    except ValueError:
        return None

    if week_start_date <= target <= week_start_date + timedelta(days=6):
        return workspace
    return None


def segment_overlaps(segment: dict[str, Any], from_date: str, to_date: str) -> bool:
    return not (segment.get("to", "") < from_date or segment.get("from", "") > to_date)


def merge_segment(data: dict[str, Any], workspace: str, from_date: str, to_date: str) -> dict[str, Any]:
    preserved_segments: list[dict[str, Any]] = []
    for segment in data.get("segments", []):
        if not segment_overlaps(segment, from_date, to_date):
            preserved_segments.append(segment)
            continue

        segment_from = segment.get("from", "")
        segment_to = segment.get("to", "")
        if segment_from < from_date:
            preserved_segments.append({**segment, "to": shift_date(from_date, -1)})
        if segment_to > to_date:
            preserved_segments.append({**segment, "from": shift_date(to_date, 1)})

    merged_segments = [
        *preserved_segments,
        {
            "from": from_date,
            "to": to_date,
            "workspace": workspace,
            "set_at": datetime.now().isoformat(),
            "set_by": "manual",
        },
    ]
    return {
        **data,
        "segments": sorted(merged_segments, key=lambda segment: segment.get("from", "")),
    }


def recommend_workspace(data: dict[str, Any], limit: int = 30) -> tuple[Optional[str], list[tuple[str, int]]]:
    selections: list[str] = []
    for preference in data.get("preferences", {}).values():
        if not isinstance(preference, dict):
            continue
        history = preference.get("selection_history", [])
        if not isinstance(history, list):
            continue
        for item in history:
            if isinstance(item, dict):
                building = item.get("building")
                if isinstance(building, str) and building:
                    selections.append(building)

    counts = Counter(selections[-limit:])
    ranking = counts.most_common()
    return (ranking[0][0] if ranking else None, ranking)


def build_get_payload(workspace_data: dict[str, Any], target_date: Optional[str] = None) -> dict[str, Any]:
    resolved_date = target_date or today_string()
    current_segment = find_segment(workspace_data, resolved_date)
    next_week = workspace_data.get("next_week")
    return {
        "today": resolved_date,
        "current_workspace": resolve_workspace_for_date(workspace_data, resolved_date),
        "current_segment": current_segment,
        "next_week": next_week if isinstance(next_week, dict) else None,
    }


def print_get_payload(payload: dict[str, Any]) -> None:
    today = payload["today"]
    current_workspace = payload.get("current_workspace")
    current_segment = payload.get("current_segment") or {}
    next_week = payload.get("next_week") or {}

    print(f"📅 今天: {today} ({weekday_name(today)})")
    if current_workspace:
        print(f"📍 当前工区: {current_workspace}")
        if current_segment:
            print(f"   有效期: {current_segment.get('from', '?')} ~ {current_segment.get('to', '?')}")
    else:
        print("⚠️ 未设置当前工区")

    next_workspace = next_week.get("workspace") if isinstance(next_week, dict) else None
    next_week_start = next_week.get("week_start") if isinstance(next_week, dict) else None
    print()
    if next_workspace and next_week_start:
        print(f"📅 下周 ({next_week_start} 起):")
        print(f"   🏢 工区: {next_workspace}")
    else:
        print("📅 下周:")
        print("   ⚠️ 未设置下周工区")


def command_get() -> int:
    payload = build_get_payload(load_workspace())
    print_get_payload(payload)
    return 0


def command_set(workspace: str, from_date: Optional[str], to_date: Optional[str]) -> int:
    start_date = from_date or today_string()
    parsed_start = date.fromisoformat(start_date)
    end_date = to_date or week_end_for(parsed_start).isoformat()
    date.fromisoformat(end_date)
    if start_date > end_date:
        print("错误: --from 不能晚于 --to", file=sys.stderr)
        return 1

    updated_data = merge_segment(load_workspace(), workspace, start_date, end_date)
    save_workspace(updated_data)
    print(f"✅ 工区已设置: {workspace}")
    print(f"   有效期: {start_date} ~ {end_date}")
    return 0


def command_set_next(workspace: str) -> int:
    next_week_start = (week_start_for(date.today()) + timedelta(weeks=1)).isoformat()
    updated_data = {
        **load_workspace(),
        "next_week": {
            "week_start": next_week_start,
            "workspace": workspace,
            "set_at": datetime.now().isoformat(),
            "set_by": "manual",
        },
    }
    save_workspace(updated_data)
    print(f"✅ 下周工区已设置: {workspace}")
    print(f"   周起始: {next_week_start}")
    return 0


def command_clear_next() -> int:
    updated_data = {**load_workspace(), "next_week": None}
    save_workspace(updated_data)
    print("✅ 已清空下周工区设置")
    return 0


def command_recommend() -> int:
    recommendation, ranking = recommend_workspace(load_preferences())
    if not ranking:
        print("❌ 没有历史选择记录，无法推荐")
        return 1

    print("📊 工区使用统计（最近 30 次选择）:")
    for building, count in ranking:
        print(f"   {building}: {'█' * count} ({count})")
    print()
    print(f"💡 推荐工区: {recommendation}")
    return 0


def command_check_friday_reminder() -> int:
    next_week = load_workspace().get("next_week")
    has_next_week = isinstance(next_week, dict) and bool(next_week.get("workspace"))
    print("NO_REMINDER" if has_next_week else "NEED_REMINDER")
    return 0


def command_timeline() -> int:
    workspace_data = load_workspace()
    today = today_string()
    print("📅 工区时间线:")
    print(f"   今天: {today} ({weekday_name(today)})")
    segments = workspace_data.get("segments", [])
    if not segments:
        print("   (暂无工区设置)")
        return 0

    for segment in segments:
        marker = " ◄ 今天" if segment.get("from", "") <= today <= segment.get("to", "") else ""
        print(f"   {segment.get('from', '?')} ~ {segment.get('to', '?')}: {segment.get('workspace', '?')}{marker}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="工区时间线管理")
    parser.add_argument("--get", action="store_true", help="获取当前工区")
    parser.add_argument("--set", action="store_true", help="设置工区")
    parser.add_argument("--set-next", action="store_true", help="设置下周工区")
    parser.add_argument("--recommend", action="store_true", help="推荐下周工区")
    parser.add_argument("--check-friday-reminder", action="store_true", help="检查是否需要周五提醒")
    parser.add_argument("--clear-next", action="store_true", help="清空下周工区")
    parser.add_argument("--timeline", action="store_true", help="查看工区时间线")
    parser.add_argument("--workspace", "-w", help="工区名称")
    parser.add_argument("--from", dest="from_date", help="开始日期")
    parser.add_argument("--to", dest="to_date", help="结束日期")

    args = parser.parse_args()

    try:
        if args.get:
            return command_get()
        if args.set:
            if not args.workspace:
                print("错误: --set 需要 --workspace", file=sys.stderr)
                return 1
            return command_set(args.workspace, args.from_date, args.to_date)
        if args.set_next:
            if not args.workspace:
                print("错误: --set-next 需要 --workspace", file=sys.stderr)
                return 1
            return command_set_next(args.workspace)
        if args.recommend:
            return command_recommend()
        if args.check_friday_reminder:
            return command_check_friday_reminder()
        if args.clear_next:
            return command_clear_next()
        if args.timeline:
            return command_timeline()
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
