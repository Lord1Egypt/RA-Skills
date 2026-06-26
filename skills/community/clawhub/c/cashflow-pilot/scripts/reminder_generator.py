#!/usr/bin/env python3
"""
cashflow-pilot 应收应付提醒生成模块

管理应收账款和应付账款，生成按逾期天数排序的提醒清单，
支持催款通知生成。
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription,
    create_parser,
    format_currency,
    format_number,
    get_data_dir,
    load_input_data,
    output_error,
    output_success,
)


# ============================================================
# 数据管理
# ============================================================

def get_receivables_file() -> str:
    """获取应收账款数据文件路径。"""
    return os.path.join(get_data_dir(), "receivables.json")


def get_payables_file() -> str:
    """获取应付账款数据文件路径。"""
    return os.path.join(get_data_dir(), "payables.json")


def load_items(file_path: str) -> List[Dict[str, Any]]:
    """加载应收/应付记录。

    Args:
        file_path: 数据文件路径。

    Returns:
        记录列表。
    """
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_items(items: List[Dict[str, Any]], file_path: str) -> None:
    """保存应收/应付记录。

    Args:
        items: 记录列表。
        file_path: 数据文件路径。
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2, default=str)


# ============================================================
# 应收账款管理
# ============================================================

def add_receivable(data: Dict[str, Any]) -> Dict[str, Any]:
    """添加一条应收账款记录。

    Args:
        data: 应收账款信息，包含:
            - customer: 客户名称
            - amount: 应收金额
            - due_date: 到期日期 (YYYY-MM-DD)
            - invoice_no: 发票号（可选）
            - description: 说明（可选）

    Returns:
        添加后的完整记录。
    """
    required = ["customer", "amount", "due_date"]
    for field in required:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    record = {
        "id": f"recv_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "customer": data["customer"],
        "amount": round(float(data["amount"]), 2),
        "due_date": data["due_date"],
        "invoice_no": data.get("invoice_no", ""),
        "description": data.get("description", ""),
        "status": "pending",  # pending / paid / overdue
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }

    items = load_items(get_receivables_file())
    items.append(record)
    save_items(items, get_receivables_file())

    return record


def add_payable(data: Dict[str, Any]) -> Dict[str, Any]:
    """添加一条应付账款记录。

    Args:
        data: 应付账款信息，包含:
            - vendor: 供应商名称
            - amount: 应付金额
            - due_date: 到期日期 (YYYY-MM-DD)
            - invoice_no: 发票号（可选）
            - description: 说明（可选）

    Returns:
        添加后的完整记录。
    """
    required = ["vendor", "amount", "due_date"]
    for field in required:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    record = {
        "id": f"pay_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "vendor": data["vendor"],
        "amount": round(float(data["amount"]), 2),
        "due_date": data["due_date"],
        "invoice_no": data.get("invoice_no", ""),
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }

    items = load_items(get_payables_file())
    items.append(record)
    save_items(items, get_payables_file())

    return record


# ============================================================
# 查询与排序
# ============================================================

def calculate_overdue_days(due_date_str: str) -> int:
    """计算逾期天数。

    Args:
        due_date_str: 到期日期字符串 (YYYY-MM-DD)。

    Returns:
        逾期天数，正数表示已逾期，负数表示未到期。
    """
    try:
        due = datetime.strptime(due_date_str, "%Y-%m-%d")
        delta = datetime.now() - due
        return delta.days
    except (ValueError, TypeError):
        return 0


def enrich_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """为记录添加逾期天数和状态标签。

    Args:
        item: 原始记录。

    Returns:
        增强后的记录。
    """
    enriched = dict(item)
    overdue_days = calculate_overdue_days(item.get("due_date", ""))
    enriched["overdue_days"] = overdue_days

    if item.get("status") == "paid":
        enriched["status_label"] = "已收款"
    elif overdue_days > 0:
        enriched["status"] = "overdue"
        enriched["status_label"] = f"已逾期 {overdue_days} 天"
    elif overdue_days == 0:
        enriched["status_label"] = "今日到期"
    else:
        enriched["status_label"] = f"还有 {abs(overdue_days)} 天到期"

    return enriched


def list_receivables(
    status_filter: Optional[str] = None, sort_by_overdue: bool = True
) -> List[Dict[str, Any]]:
    """列出应收账款。

    Args:
        status_filter: 状态筛选（pending/paid/overdue），None 表示全部。
        sort_by_overdue: 是否按逾期天数排序（逾期最久的在前）。

    Returns:
        增强后的应收账款列表。
    """
    items = load_items(get_receivables_file())
    enriched = [enrich_item(item) for item in items]

    if status_filter:
        enriched = [item for item in enriched if item["status"] == status_filter]

    if sort_by_overdue:
        enriched.sort(key=lambda x: x["overdue_days"], reverse=True)

    return enriched


def list_payables(
    status_filter: Optional[str] = None, sort_by_overdue: bool = True
) -> List[Dict[str, Any]]:
    """列出应付账款。

    Args:
        status_filter: 状态筛选。
        sort_by_overdue: 是否按逾期天数排序。

    Returns:
        增强后的应付账款列表。
    """
    items = load_items(get_payables_file())
    enriched = [enrich_item(item) for item in items]

    if status_filter:
        enriched = [item for item in enriched if item["status"] == status_filter]

    if sort_by_overdue:
        enriched.sort(key=lambda x: x["overdue_days"], reverse=True)

    return enriched


# ============================================================
# 提醒生成
# ============================================================

def generate_reminders(item_type: str = "receivable") -> Dict[str, Any]:
    """生成应收/应付提醒清单。

    免费版限制：最多显示 3 条提醒。
    付费版：无限制。

    Args:
        item_type: "receivable"（应收）或 "payable"（应付）。

    Returns:
        提醒清单数据。
    """
    sub = check_subscription()
    max_reminders = sub["max_reminders"]  # -1 表示无限制

    if item_type == "receivable":
        items = list_receivables(status_filter=None)
        # 只显示未收款的
        items = [i for i in items if i["status"] != "paid"]
    else:
        items = list_payables(status_filter=None)
        items = [i for i in items if i["status"] != "paid"]

    # 分类
    overdue = [i for i in items if i["overdue_days"] > 0]
    due_soon = [i for i in items if -7 <= i["overdue_days"] <= 0]
    upcoming = [i for i in items if i["overdue_days"] < -7]

    # 构建提醒列表
    reminders = []

    for item in overdue:
        name_key = "customer" if item_type == "receivable" else "vendor"
        reminders.append({
            "priority": "高",
            "name": item.get(name_key, "未知"),
            "amount": item["amount"],
            "due_date": item["due_date"],
            "overdue_days": item["overdue_days"],
            "message": (
                f"【逾期】{item.get(name_key, '未知')} — "
                f"{format_currency(item['amount'])}，已逾期 {item['overdue_days']} 天"
            ),
        })

    for item in due_soon:
        name_key = "customer" if item_type == "receivable" else "vendor"
        reminders.append({
            "priority": "中",
            "name": item.get(name_key, "未知"),
            "amount": item["amount"],
            "due_date": item["due_date"],
            "overdue_days": item["overdue_days"],
            "message": (
                f"【即将到期】{item.get(name_key, '未知')} — "
                f"{format_currency(item['amount'])}，{item['status_label']}"
            ),
        })

    for item in upcoming:
        name_key = "customer" if item_type == "receivable" else "vendor"
        reminders.append({
            "priority": "低",
            "name": item.get(name_key, "未知"),
            "amount": item["amount"],
            "due_date": item["due_date"],
            "overdue_days": item["overdue_days"],
            "message": (
                f"【待处理】{item.get(name_key, '未知')} — "
                f"{format_currency(item['amount'])}，{item['status_label']}"
            ),
        })

    # 免费版限制
    truncated = False
    total_count = len(reminders)
    if max_reminders > 0 and len(reminders) > max_reminders:
        reminders = reminders[:max_reminders]
        truncated = True

    # 统计
    total_overdue_amount = sum(i["amount"] for i in overdue)
    total_due_soon_amount = sum(i["amount"] for i in due_soon)

    result = {
        "type": "应收账款" if item_type == "receivable" else "应付账款",
        "reminders": reminders,
        "total_count": total_count,
        "shown_count": len(reminders),
        "overdue_count": len(overdue),
        "due_soon_count": len(due_soon),
        "total_overdue_amount": round(total_overdue_amount, 2),
        "total_due_soon_amount": round(total_due_soon_amount, 2),
    }

    if truncated:
        result["notice"] = (
            f"免费版仅显示前 {max_reminders} 条提醒（共 {total_count} 条）。"
            "升级至付费版（¥79/月）可查看全部提醒。"
        )

    # 生成 Markdown
    result["markdown"] = _render_reminders_markdown(result, item_type)

    return result


def generate_collection_notice(receivable_id: str) -> Dict[str, Any]:
    """生成单条催款通知。

    Args:
        receivable_id: 应收账款记录 ID。

    Returns:
        催款通知内容。
    """
    items = load_items(get_receivables_file())
    target = None
    for item in items:
        if item.get("id") == receivable_id:
            target = enrich_item(item)
            break

    if not target:
        raise ValueError(f"未找到应收账款记录: {receivable_id}")

    customer = target.get("customer", "客户")
    amount = format_currency(target["amount"])
    due_date = target["due_date"]
    overdue_days = target["overdue_days"]
    invoice = target.get("invoice_no", "")

    if overdue_days > 0:
        notice = (
            f"尊敬的 {customer}：\n\n"
            f"贵公司有一笔款项 {amount}（发票号：{invoice}）"
            f"已于 {due_date} 到期，目前已逾期 {overdue_days} 天。\n\n"
            f"请尽快安排付款，如已付款请忽略此提醒。\n\n"
            f"如有疑问，请随时联系我们。\n\n谢谢！"
        )
    else:
        notice = (
            f"尊敬的 {customer}：\n\n"
            f"温馨提醒，贵公司有一笔款项 {amount}（发票号：{invoice}）"
            f"将于 {due_date} 到期。\n\n"
            f"请提前安排付款，感谢您的合作！"
        )

    return {
        "receivable_id": receivable_id,
        "customer": customer,
        "amount": target["amount"],
        "due_date": due_date,
        "overdue_days": overdue_days,
        "notice": notice,
    }


def _render_reminders_markdown(result: Dict[str, Any], item_type: str) -> str:
    """渲染提醒清单为 Markdown 格式。"""
    type_label = result["type"]
    lines = [
        f"# {type_label}提醒清单\n",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
    ]

    if not result["reminders"]:
        lines.append(f"\n暂无待处理的{type_label}记录。\n")
        return "".join(lines)

    # 汇总统计
    lines.extend([
        "\n## 概览\n",
        f"- 逾期数量：{result['overdue_count']} 笔，"
        f"合计 {format_currency(result['total_overdue_amount'])}\n",
        f"- 即将到期：{result['due_soon_count']} 笔，"
        f"合计 {format_currency(result['total_due_soon_amount'])}\n",
        f"- 总计：{result['total_count']} 笔\n",
    ])

    # 明细表
    name_header = "客户" if item_type == "receivable" else "供应商"
    lines.extend([
        "\n## 明细\n",
        f"| 优先级 | {name_header} | 金额 | 到期日 | 状态 |\n",
        "|--------|------|-----:|--------|------|\n",
    ])

    for r in result["reminders"]:
        lines.append(
            f"| {r['priority']} | {r['name']} | {format_currency(r['amount'])} | "
            f"{r['due_date']} | {'逾期' + str(r['overdue_days']) + '天' if r['overdue_days'] > 0 else '待处理'} |\n"
        )

    if result.get("notice"):
        lines.extend(["\n---\n", f"> {result['notice']}\n"])

    lines.append("\n---\n*由 cashflow-pilot 自动生成*\n")
    return "".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口函数。"""
    parser = create_parser("cashflow-pilot 应收应付提醒生成工具")
    parser.add_argument(
        "--type",
        choices=["receivable", "payable"],
        default="receivable",
        help="类型：receivable（应收）或 payable（应付）",
    )
    parser.add_argument("--id", default=None, help="记录 ID（用于催款通知生成）")

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        if args.action == "add":
            data = load_input_data(args)
            if not data:
                output_error("请通过 --data 或 --data-file 提供数据", "MISSING_DATA")
                return

            if args.type == "receivable":
                record = add_receivable(data)
            else:
                record = add_payable(data)

            output_success({"message": "记录添加成功", "record": record})

        elif args.action == "list":
            if args.type == "receivable":
                items = list_receivables()
            else:
                items = list_payables()

            output_success({
                "type": args.type,
                "count": len(items),
                "items": items,
            })

        elif args.action == "overdue":
            if args.type == "receivable":
                items = list_receivables(status_filter="overdue")
            else:
                items = list_payables(status_filter="overdue")

            total_amount = sum(i["amount"] for i in items)
            output_success({
                "type": args.type,
                "overdue_count": len(items),
                "total_overdue_amount": round(total_amount, 2),
                "items": items,
            })

        elif args.action == "generate":
            result = generate_reminders(args.type)
            output_success(result)

        elif args.action == "notice":
            if not args.id:
                output_error("请使用 --id 参数指定应收账款记录 ID", "MISSING_ID")
                return
            notice = generate_collection_notice(args.id)
            output_success(notice)

        else:
            output_error(
                f"不支持的操作: {args.action}。"
                "支持的操作: add, list, overdue, generate, notice",
                "INVALID_ACTION",
            )

    except ValueError as e:
        output_error(str(e), "REMINDER_ERROR")
    except Exception as e:
        output_error(f"执行失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
