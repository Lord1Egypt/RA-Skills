#!/usr/bin/env python3
"""
deal-closer 会议记录模块

提供会议记录的增删改查、按商机/日期筛选、会议摘要生成等功能。
支持手动记录和日历 API 同步（付费功能）。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
    calculate_days_since,
    days_until,
    MEETING_TYPES,
)


# ============================================================
# 数据文件路径
# ============================================================

MEETINGS_FILE = "meetings.json"
DEALS_FILE = "deals.json"


def _get_meetings() -> List[Dict[str, Any]]:
    """读取所有会议记录。"""
    return read_json_file(get_data_file(MEETINGS_FILE))


def _save_meetings(meetings: List[Dict[str, Any]]) -> None:
    """保存会议记录到文件。"""
    write_json_file(get_data_file(MEETINGS_FILE), meetings)


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


def _find_meeting(meetings: List[Dict], meeting_id: str) -> Optional[Dict]:
    """根据 ID 查找会议记录。"""
    for m in meetings:
        if m.get("id") == meeting_id:
            return m
    return None


# ============================================================
# 会议操作
# ============================================================

def log_meeting(data: Dict[str, Any]) -> None:
    """记录一次会议。

    必填字段: deal_id, date
    可选字段: attendees, type, location, notes, action_items, next_steps

    Args:
        data: 会议数据字典。
    """
    deal_id = data.get("deal_id")
    if not deal_id:
        output_error("商机ID（deal_id）为必填字段", code="VALIDATION_ERROR")
        return

    meeting_date = data.get("date")
    if not meeting_date:
        output_error("会议日期（date）为必填字段", code="VALIDATION_ERROR")
        return

    # 验证商机是否存在
    deals = _get_deals()
    target_deal = None
    for d in deals:
        if d.get("id") == deal_id:
            target_deal = d
            break

    if not target_deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    # 处理参会人列表
    attendees = data.get("attendees", [])
    if isinstance(attendees, str):
        attendees = [a.strip() for a in attendees.split(",") if a.strip()]

    # 处理行动项列表
    action_items = data.get("action_items", [])
    if isinstance(action_items, str):
        action_items = [a.strip() for a in action_items.split(";") if a.strip()]

    # 处理下一步列表
    next_steps = data.get("next_steps", [])
    if isinstance(next_steps, str):
        next_steps = [s.strip() for s in next_steps.split(";") if s.strip()]

    # 会议类型校验
    meeting_type = data.get("type", "其他")
    if meeting_type not in MEETING_TYPES:
        meeting_type = "其他"

    now = now_iso()
    meeting = {
        "id": generate_id("M"),
        "deal_id": deal_id,
        "date": meeting_date,
        "attendees": attendees,
        "type": meeting_type,
        "location": data.get("location", ""),
        "notes": data.get("notes", ""),
        "action_items": action_items,
        "next_steps": next_steps,
        "created_at": now,
    }

    meetings = _get_meetings()
    meetings.append(meeting)
    _save_meetings(meetings)

    output_success({
        "message": f"会议记录已添加（商机: {target_deal.get('name', '')}）",
        "meeting": meeting,
    })


def list_meetings(data: Optional[Dict[str, Any]] = None) -> None:
    """列出会议记录。

    可选过滤: deal_id, date_from, date_to, type

    Args:
        data: 可选的过滤条件字典。
    """
    meetings = _get_meetings()

    if data:
        # 按商机过滤
        deal_id = data.get("deal_id")
        if deal_id:
            meetings = [m for m in meetings if m.get("deal_id") == deal_id]

        # 按日期范围过滤
        date_from = data.get("date_from")
        if date_from:
            meetings = [m for m in meetings if m.get("date", "") >= date_from]

        date_to = data.get("date_to")
        if date_to:
            meetings = [m for m in meetings if m.get("date", "") <= date_to]

        # 按类型过滤
        type_filter = data.get("type")
        if type_filter:
            meetings = [m for m in meetings if m.get("type") == type_filter]

    # 按日期倒序
    meetings.sort(key=lambda m: m.get("date", ""), reverse=True)

    # 加载商机信息用于显示
    deals = _get_deals()
    deal_map = {d["id"]: d.get("name", "") for d in deals}

    display_list = []
    for m in meetings:
        display = dict(m)
        display["deal_name"] = deal_map.get(m.get("deal_id", ""), "未知商机")
        display_list.append(display)

    # 按类型统计
    type_stats = {}
    for mt in MEETING_TYPES:
        type_stats[mt] = sum(1 for m in meetings if m.get("type") == mt)

    output_success({
        "total": len(display_list),
        "type_stats": type_stats,
        "meetings": display_list,
    })


def upcoming_meetings(data: Optional[Dict[str, Any]] = None) -> None:
    """查看即将到来的会议。

    可选参数: days（查看未来 N 天，默认 7 天）

    Args:
        data: 可选参数字典。
    """
    data = data or {}
    days_ahead = data.get("days", 7)
    try:
        days_ahead = int(days_ahead)
    except (TypeError, ValueError):
        days_ahead = 7

    today = today_str()
    future_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    meetings = _get_meetings()

    # 筛选未来会议
    upcoming = []
    for m in meetings:
        meeting_date = m.get("date", "")
        if meeting_date and today <= meeting_date <= future_date:
            upcoming.append(m)

    # 按日期正序
    upcoming.sort(key=lambda m: m.get("date", ""))

    # 加载商机信息
    deals = _get_deals()
    deal_map = {d["id"]: d.get("name", "") for d in deals}

    display_list = []
    for m in upcoming:
        display = dict(m)
        display["deal_name"] = deal_map.get(m.get("deal_id", ""), "未知商机")
        meeting_date = m.get("date", "")
        if meeting_date:
            display["days_until"] = days_until(meeting_date)
        display_list.append(display)

    output_success({
        "total": len(display_list),
        "period": f"{today} 至 {future_date}",
        "meetings": display_list,
    })


def meeting_summary(data: Dict[str, Any]) -> None:
    """生成会议摘要。

    支持按商机汇总或按时间段汇总。

    Args:
        data: 参数字典，支持 deal_id 或 date_from + date_to。
    """
    meetings = _get_meetings()
    deals = _get_deals()
    deal_map = {d["id"]: d for d in deals}

    deal_id = data.get("deal_id")
    date_from = data.get("date_from")
    date_to = data.get("date_to")

    # 过滤
    if deal_id:
        meetings = [m for m in meetings if m.get("deal_id") == deal_id]
    if date_from:
        meetings = [m for m in meetings if m.get("date", "") >= date_from]
    if date_to:
        meetings = [m for m in meetings if m.get("date", "") <= date_to]

    if not meetings:
        output_error("指定范围内暂无会议记录", code="NO_DATA")
        return

    # 按日期正序
    meetings.sort(key=lambda m: m.get("date", ""))

    # 收集所有行动项和下一步
    all_action_items = []
    all_next_steps = []
    total_attendees = set()
    deal_summary = {}

    for m in meetings:
        for item in m.get("action_items", []):
            all_action_items.append({
                "item": item,
                "meeting_date": m.get("date", ""),
                "deal_id": m.get("deal_id", ""),
            })

        for step in m.get("next_steps", []):
            all_next_steps.append({
                "step": step,
                "meeting_date": m.get("date", ""),
                "deal_id": m.get("deal_id", ""),
            })

        for attendee in m.get("attendees", []):
            total_attendees.add(attendee)

        # 按商机汇总
        mid = m.get("deal_id", "未分类")
        if mid not in deal_summary:
            deal_info = deal_map.get(mid, {})
            deal_summary[mid] = {
                "deal_name": deal_info.get("name", "未知商机"),
                "meeting_count": 0,
                "latest_date": "",
                "types": [],
            }
        deal_summary[mid]["meeting_count"] += 1
        deal_summary[mid]["latest_date"] = m.get("date", "")
        mtype = m.get("type", "")
        if mtype and mtype not in deal_summary[mid]["types"]:
            deal_summary[mid]["types"].append(mtype)

    output_success({
        "total_meetings": len(meetings),
        "total_attendees": len(total_attendees),
        "attendees": sorted(list(total_attendees)),
        "action_items": all_action_items,
        "next_steps": all_next_steps,
        "deal_summary": deal_summary,
        "date_range": {
            "from": meetings[0].get("date", "") if meetings else "",
            "to": meetings[-1].get("date", "") if meetings else "",
        },
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer 会议记录")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "log": lambda: log_meeting(data or {}),
        "list": lambda: list_meetings(data),
        "upcoming": lambda: upcoming_meetings(data),
        "summary": lambda: meeting_summary(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
