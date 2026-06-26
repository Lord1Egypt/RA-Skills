#!/usr/bin/env python3
"""
customer-pulse 客户数据管理模块

提供客户数据的 CRUD 操作，支持 JSON 文件存储、CSV 导入导出。
"""

import csv
import io
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
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
    validate_stage,
    write_json_file,
    STAGES,
)


# ============================================================
# 数据文件路径
# ============================================================

CUSTOMERS_FILE = "customers.json"


def _get_customers() -> List[Dict[str, Any]]:
    """读取所有客户数据。"""
    return read_json_file(get_data_file(CUSTOMERS_FILE))


def _save_customers(customers: List[Dict[str, Any]]) -> None:
    """保存客户数据到文件。"""
    write_json_file(get_data_file(CUSTOMERS_FILE), customers)


def _find_customer(customers: List[Dict], customer_id: str) -> Optional[Dict]:
    """根据 ID 查找客户。"""
    for c in customers:
        if c.get("id") == customer_id:
            return c
    return None


# ============================================================
# CRUD 操作
# ============================================================

def add_customer(data: Dict[str, Any]) -> None:
    """添加新客户。

    必填字段: name
    可选字段: phone, company, product_interest, budget, stage, source

    Args:
        data: 客户数据字典。
    """
    if not data.get("name"):
        output_error("客户姓名（name）为必填字段", code="VALIDATION_ERROR")
        return

    sub = check_subscription()
    customers = _get_customers()

    if len(customers) >= sub["max_customers"]:
        limit = sub["max_customers"]
        if sub["tier"] == "free":
            output_error(
                f"免费版最多管理 {limit} 个客户，当前已有 {len(customers)} 个。"
                "请升级至付费版（¥99/月）以管理更多客户。",
                code="LIMIT_EXCEEDED",
            )
        else:
            output_error(
                f"已达到客户数量上限 {limit} 个。",
                code="LIMIT_EXCEEDED",
            )
        return

    stage = data.get("stage", "初步接触")
    try:
        validate_stage(stage)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    now = now_iso()
    customer = {
        "id": generate_id("C"),
        "name": data["name"],
        "phone": data.get("phone", ""),
        "company": data.get("company", ""),
        "product_interest": data.get("product_interest", ""),
        "budget": data.get("budget", 0),
        "stage": stage,
        "source": data.get("source", ""),
        "created_at": now,
        "updated_at": now,
    }

    customers.append(customer)
    _save_customers(customers)

    # 输出时脱敏手机号
    display = dict(customer)
    display["phone"] = mask_phone(display["phone"])
    output_success({"message": f"客户「{customer['name']}」已添加", "customer": display})


def update_customer(data: Dict[str, Any]) -> None:
    """更新客户信息。

    必填字段: id
    可更新字段: name, phone, company, product_interest, budget, stage, source

    Args:
        data: 包含客户 ID 和待更新字段的字典。
    """
    customer_id = data.get("id")
    if not customer_id:
        output_error("客户ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    customers = _get_customers()
    customer = _find_customer(customers, customer_id)
    if not customer:
        output_error(f"未找到ID为 {customer_id} 的客户", code="NOT_FOUND")
        return

    updatable_fields = ["name", "phone", "company", "product_interest", "budget", "stage", "source"]
    updated = False

    for field in updatable_fields:
        if field in data:
            if field == "stage":
                try:
                    validate_stage(data[field])
                except ValueError as e:
                    output_error(str(e), code="VALIDATION_ERROR")
                    return
            customer[field] = data[field]
            updated = True

    if not updated:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    customer["updated_at"] = now_iso()
    _save_customers(customers)

    display = dict(customer)
    display["phone"] = mask_phone(display["phone"])
    output_success({"message": f"客户「{customer['name']}」已更新", "customer": display})


def delete_customer(data: Dict[str, Any]) -> None:
    """删除客户。

    必填字段: id

    Args:
        data: 包含客户 ID 的字典。
    """
    customer_id = data.get("id")
    if not customer_id:
        output_error("客户ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    customers = _get_customers()
    original_count = len(customers)
    customers = [c for c in customers if c.get("id") != customer_id]

    if len(customers) == original_count:
        output_error(f"未找到ID为 {customer_id} 的客户", code="NOT_FOUND")
        return

    _save_customers(customers)
    output_success({"message": f"客户 {customer_id} 已删除"})


def get_customer(data: Dict[str, Any]) -> None:
    """获取单个客户详情。

    必填字段: id

    Args:
        data: 包含客户 ID 的字典。
    """
    customer_id = data.get("id")
    if not customer_id:
        output_error("客户ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    customers = _get_customers()
    customer = _find_customer(customers, customer_id)
    if not customer:
        output_error(f"未找到ID为 {customer_id} 的客户", code="NOT_FOUND")
        return

    display = dict(customer)
    display["phone"] = mask_phone(display["phone"])
    output_success(display)


def list_customers(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有客户。

    可选过滤: stage, keyword（搜索姓名/公司/产品）

    Args:
        data: 可选的过滤条件字典。
    """
    customers = _get_customers()

    if data:
        stage_filter = data.get("stage")
        keyword = data.get("keyword", "").strip()

        if stage_filter:
            customers = [c for c in customers if c.get("stage") == stage_filter]

        if keyword:
            keyword_lower = keyword.lower()
            customers = [
                c for c in customers
                if keyword_lower in c.get("name", "").lower()
                or keyword_lower in c.get("company", "").lower()
                or keyword_lower in c.get("product_interest", "").lower()
            ]

    # 按更新时间倒序排列
    customers.sort(key=lambda c: c.get("updated_at", ""), reverse=True)

    # 脱敏手机号
    display_list = []
    for c in customers:
        d = dict(c)
        d["phone"] = mask_phone(d["phone"])
        display_list.append(d)

    # 按阶段分组统计
    stage_stats = {}
    for stage in STAGES:
        stage_stats[stage] = sum(1 for c in customers if c.get("stage") == stage)

    output_success({
        "total": len(display_list),
        "stage_stats": stage_stats,
        "customers": display_list,
    })


def import_customers(data: Dict[str, Any]) -> None:
    """从 CSV 文件导入客户数据。

    必填字段: file_path

    Args:
        data: 包含 CSV 文件路径的字典。
    """
    file_path = data.get("file_path")
    if not file_path:
        output_error("CSV 文件路径（file_path）为必填字段", code="VALIDATION_ERROR")
        return

    if not os.path.exists(file_path):
        output_error(f"文件不存在: {file_path}", code="FILE_NOT_FOUND")
        return

    sub = check_subscription()
    customers = _get_customers()
    imported = 0
    skipped = 0
    errors = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                if len(customers) >= sub["max_customers"]:
                    errors.append(f"行 {row_num}: 已达客户数量上限 {sub['max_customers']}")
                    skipped += 1
                    continue

                name = row.get("name", "").strip() or row.get("姓名", "").strip()
                if not name:
                    errors.append(f"行 {row_num}: 缺少客户姓名")
                    skipped += 1
                    continue

                stage = row.get("stage", "").strip() or row.get("阶段", "").strip() or "初步接触"
                if stage not in STAGES:
                    stage = "初步接触"

                now = now_iso()
                customer = {
                    "id": generate_id("C"),
                    "name": name,
                    "phone": row.get("phone", "").strip() or row.get("手机", "").strip(),
                    "company": row.get("company", "").strip() or row.get("公司", "").strip(),
                    "product_interest": row.get("product_interest", "").strip() or row.get("意向产品", "").strip(),
                    "budget": _parse_budget(row.get("budget", "") or row.get("预算", "")),
                    "stage": stage,
                    "source": row.get("source", "").strip() or row.get("来源", "").strip(),
                    "created_at": now,
                    "updated_at": now,
                }
                customers.append(customer)
                imported += 1

    except Exception as e:
        output_error(f"导入失败: {e}", code="IMPORT_ERROR")
        return

    _save_customers(customers)
    result = {
        "message": f"导入完成：成功 {imported} 条，跳过 {skipped} 条",
        "imported": imported,
        "skipped": skipped,
        "total": len(customers),
    }
    if errors:
        result["errors"] = errors[:10]
    output_success(result)


def export_customers(data: Optional[Dict[str, Any]] = None) -> None:
    """导出客户数据到 CSV 格式。

    可选字段: file_path（若不指定则输出到 stdout）

    Args:
        data: 可选的配置字典。
    """
    customers = _get_customers()
    if not customers:
        output_error("暂无客户数据可导出", code="NO_DATA")
        return

    file_path = data.get("file_path") if data else None
    fieldnames = ["id", "name", "phone", "company", "product_interest", "budget", "stage", "source", "created_at", "updated_at"]

    try:
        if file_path:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for c in customers:
                    row = {k: c.get(k, "") for k in fieldnames}
                    writer.writerow(row)
            output_success({"message": f"已导出 {len(customers)} 条客户数据到 {file_path}", "count": len(customers)})
        else:
            output_buf = io.StringIO()
            writer = csv.DictWriter(output_buf, fieldnames=fieldnames)
            writer.writeheader()
            for c in customers:
                row = {k: c.get(k, "") for k in fieldnames}
                writer.writerow(row)
            output_success({"csv": output_buf.getvalue(), "count": len(customers)})
    except IOError as e:
        output_error(f"导出失败: {e}", code="EXPORT_ERROR")


# ============================================================
# 辅助函数
# ============================================================

def _parse_budget(value: str) -> float:
    """解析预算字符串为数值。

    支持带「万」「亿」等中文单位的数值。

    Args:
        value: 预算字符串。

    Returns:
        数值化的预算金额。
    """
    if not value:
        return 0
    value = str(value).strip().replace(",", "").replace("，", "")
    value = value.replace("¥", "").replace("￥", "").replace("元", "")

    try:
        if "亿" in value:
            return float(value.replace("亿", "")) * 1e8
        elif "万" in value:
            return float(value.replace("万", "")) * 1e4
        else:
            return float(value)
    except (ValueError, TypeError):
        return 0


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("customer-pulse 客户数据管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "add": lambda: add_customer(data or {}),
        "update": lambda: update_customer(data or {}),
        "delete": lambda: delete_customer(data or {}),
        "get": lambda: get_customer(data or {}),
        "list": lambda: list_customers(data),
        "import": lambda: import_customers(data or {}),
        "export": lambda: export_customers(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
