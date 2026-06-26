#!/usr/bin/env python3
"""
customer-pulse 跟进记录与提醒模块

记录客户跟进活动，计算下次跟进日期，生成待跟进提醒清单。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    calculate_days_since,
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    mask_phone,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    today_str,
    write_json_file,
)


# ============================================================
# 数据文件
# ============================================================

FOLLOWUPS_FILE = "followups.json"
CUSTOMERS_FILE = "customers.json"


def _get_followups() -> List[Dict[str, Any]]:
    """读取所有跟进记录。"""
    return read_json_file(get_data_file(FOLLOWUPS_FILE))


def _save_followups(followups: List[Dict[str, Any]]) -> None:
    """保存跟进记录。"""
    write_json_file(get_data_file(FOLLOWUPS_FILE), followups)


def _get_customers() -> List[Dict[str, Any]]:
    """读取所有客户数据。"""
    return read_json_file(get_data_file(CUSTOMERS_FILE))


def _find_customer(customers: List[Dict], customer_id: str) -> Optional[Dict]:
    """根据 ID 查找客户。"""
    for c in customers:
        if c.get("id") == customer_id:
            return c
    return None


def _find_customer_by_name(customers: List[Dict], name: str) -> Optional[Dict]:
    """根据姓名查找客户（模糊匹配）。"""
    name = name.strip()
    for c in customers:
        if c.get("name", "").strip() == name:
            return c
    for c in customers:
        if name in c.get("name", ""):
            return c
    return None


# ============================================================
# 跟进操作
# ============================================================

def record_followup(data: Dict[str, Any]) -> None:
    """记录一次跟进活动。

    必填字段: customer_id 或 customer_name, content
    可选字段: date, next_action, next_followup_date, reminder_days

    Args:
        data: 跟进数据字典。
    """
    customers = _get_customers()

    # 支持通过 ID 或姓名查找客户
    customer_id = data.get("customer_id")
    customer_name = data.get("customer_name")

    customer = None
    if customer_id:
        customer = _find_customer(customers, customer_id)
    elif customer_name:
        customer = _find_customer_by_name(customers, customer_name)

    if not customer:
        identifier = customer_id or customer_name or "未指定"
        output_error(f"未找到客户: {identifier}", code="NOT_FOUND")
        return

    content = data.get("content", "").strip()
    if not content:
        output_error("跟进内容（content）为必填字段", code="VALIDATION_ERROR")
        return

    sub = check_subscription()
    followup_date = data.get("date", today_str())

    # 计算下次跟进日期
    if sub["tier"] == "paid" and data.get("next_followup_date"):
        next_followup_date = data["next_followup_date"]
    elif sub["tier"] == "paid" and data.get("reminder_days"):
        days = int(data["reminder_days"])
        next_dt = datetime.strptime(followup_date, "%Y-%m-%d") + timedelta(days=days)
        next_followup_date = next_dt.strftime("%Y-%m-%d")
    else:
        # 免费版固定 3 天后提醒
        next_dt = datetime.strptime(followup_date, "%Y-%m-%d") + timedelta(days=3)
        next_followup_date = next_dt.strftime("%Y-%m-%d")

    followup = {
        "id": generate_id("F"),
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "date": followup_date,
        "content": content,
        "next_action": data.get("next_action", ""),
        "next_followup_date": next_followup_date,
        "created_at": now_iso(),
    }

    followups = _get_followups()
    followups.append(followup)
    _save_followups(followups)

    output_success({
        "message": f"已记录对「{customer['name']}」的跟进",
        "followup": followup,
        "reminder": f"下次跟进提醒: {next_followup_date}",
    })


def list_pending(data: Optional[Dict[str, Any]] = None) -> None:
    """列出待跟进客户清单。

    按最后跟进时间排序，标注超期未跟进的客户。

    Args:
        data: 可选过滤参数。
    """
    customers = _get_customers()
    followups = _get_followups()

    # 排除已成交和已流失的客户
    active_customers = [
        c for c in customers
        if c.get("stage") not in ("成交", "流失")
    ]

    # 构建每个客户的最后跟进信息
    today = today_str()
    pending_list = []

    for customer in active_customers:
        cid = customer["id"]
        customer_followups = [f for f in followups if f.get("customer_id") == cid]
        customer_followups.sort(key=lambda f: f.get("date", ""), reverse=True)

        if customer_followups:
            last_followup = customer_followups[0]
            last_date = last_followup.get("date", "")
            next_date = last_followup.get("next_followup_date", "")
            days_since = calculate_days_since(last_date)
            is_overdue = next_date <= today if next_date else days_since >= 3
        else:
            last_date = customer.get("created_at", "")[:10]
            next_date = ""
            days_since = calculate_days_since(last_date)
            is_overdue = days_since >= 3

        pending_list.append({
            "customer_id": cid,
            "customer_name": customer["name"],
            "company": customer.get("company", ""),
            "stage": customer.get("stage", ""),
            "phone": mask_phone(customer.get("phone", "")),
            "last_followup_date": last_date,
            "next_followup_date": next_date,
            "days_since_last": days_since,
            "is_overdue": is_overdue,
            "last_content": customer_followups[0].get("content", "") if customer_followups else "尚未跟进",
        })

    # 超期的排在前面，然后按最后跟进时间升序（最久未跟进的在前）
    pending_list.sort(key=lambda x: (not x["is_overdue"], -x["days_since_last"]))

    overdue_count = sum(1 for p in pending_list if p["is_overdue"])

    output_success({
        "total": len(pending_list),
        "overdue_count": overdue_count,
        "pending": pending_list,
    })


def get_reminders(data: Optional[Dict[str, Any]] = None) -> None:
    """获取今日跟进提醒。

    返回今日（及已过期）需要跟进的客户清单。

    Args:
        data: 可选参数。
    """
    customers = _get_customers()
    followups = _get_followups()
    today = today_str()

    # 收集需要提醒的客户
    reminders = []
    seen_customers = set()

    for f in followups:
        next_date = f.get("next_followup_date", "")
        cid = f.get("customer_id", "")

        if not next_date or cid in seen_customers:
            continue

        if next_date <= today:
            customer = _find_customer(customers, cid)
            if customer and customer.get("stage") not in ("成交", "流失"):
                seen_customers.add(cid)
                days_overdue = calculate_days_since(next_date)
                reminders.append({
                    "customer_id": cid,
                    "customer_name": customer["name"],
                    "company": customer.get("company", ""),
                    "stage": customer.get("stage", ""),
                    "phone": mask_phone(customer.get("phone", "")),
                    "planned_date": next_date,
                    "days_overdue": days_overdue,
                    "last_content": f.get("content", ""),
                    "next_action": f.get("next_action", ""),
                    "urgency": "高" if days_overdue >= 7 else ("中" if days_overdue >= 3 else "低"),
                })

    # 检查从未跟进过的客户
    followed_ids = {f.get("customer_id") for f in followups}
    for customer in customers:
        cid = customer["id"]
        if cid not in followed_ids and cid not in seen_customers:
            if customer.get("stage") not in ("成交", "流失"):
                days = calculate_days_since(customer.get("created_at", "")[:10])
                if days >= 3:
                    seen_customers.add(cid)
                    reminders.append({
                        "customer_id": cid,
                        "customer_name": customer["name"],
                        "company": customer.get("company", ""),
                        "stage": customer.get("stage", ""),
                        "phone": mask_phone(customer.get("phone", "")),
                        "planned_date": "",
                        "days_overdue": days,
                        "last_content": "尚未跟进",
                        "next_action": "首次跟进",
                        "urgency": "高" if days >= 7 else "中",
                    })

    reminders.sort(key=lambda r: (-r["days_overdue"]))

    output_success({
        "date": today,
        "total_reminders": len(reminders),
        "urgent_count": sum(1 for r in reminders if r["urgency"] == "高"),
        "reminders": reminders,
    })


def get_history(data: Dict[str, Any]) -> None:
    """获取指定客户的跟进历史。

    必填字段: customer_id 或 customer_name

    Args:
        data: 包含客户标识的字典。
    """
    customers = _get_customers()

    customer_id = data.get("customer_id")
    customer_name = data.get("customer_name")

    customer = None
    if customer_id:
        customer = _find_customer(customers, customer_id)
    elif customer_name:
        customer = _find_customer_by_name(customers, customer_name)

    if not customer:
        identifier = customer_id or customer_name or "未指定"
        output_error(f"未找到客户: {identifier}", code="NOT_FOUND")
        return

    followups = _get_followups()
    history = [f for f in followups if f.get("customer_id") == customer["id"]]
    history.sort(key=lambda f: f.get("date", ""), reverse=True)

    customer_display = dict(customer)
    customer_display["phone"] = mask_phone(customer_display.get("phone", ""))

    output_success({
        "customer": customer_display,
        "total_followups": len(history),
        "history": history,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("customer-pulse 跟进记录管理")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "record": lambda: record_followup(data or {}),
        "list_pending": lambda: list_pending(data),
        "reminders": lambda: get_reminders(data),
        "history": lambda: get_history(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
