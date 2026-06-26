#!/usr/bin/env python3
"""
deal-closer 商机数据管理模块

提供商机数据的 CRUD 操作，支持 JSON 文件存储、CSV 导入导出、阶段历史追踪。
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
    mask_email,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    validate_deal_stage,
    write_json_file,
    format_currency,
    parse_amount,
    get_stage_probability,
    calculate_days_since,
    DEAL_STAGES,
)


# ============================================================
# 数据文件路径
# ============================================================

DEALS_FILE = "deals.json"


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


def _save_deals(deals: List[Dict[str, Any]]) -> None:
    """保存商机数据到文件。"""
    write_json_file(get_data_file(DEALS_FILE), deals)


def _find_deal(deals: List[Dict], deal_id: str) -> Optional[Dict]:
    """根据 ID 查找商机。"""
    for d in deals:
        if d.get("id") == deal_id:
            return d
    return None


def _mask_deal(deal: Dict[str, Any]) -> Dict[str, Any]:
    """对商机中的敏感字段进行脱敏处理。"""
    display = dict(deal)
    if display.get("contact_phone"):
        display["contact_phone"] = mask_phone(display["contact_phone"])
    if display.get("contact_email"):
        display["contact_email"] = mask_email(display["contact_email"])
    return display


# ============================================================
# CRUD 操作
# ============================================================

def add_deal(data: Dict[str, Any]) -> None:
    """添加新商机。

    必填字段: name
    可选字段: contact_name, contact_phone, contact_email, company, amount,
              stage, probability, source, expected_close_date, notes, tags

    Args:
        data: 商机数据字典。
    """
    if not data.get("name"):
        output_error("商机名称（name）为必填字段", code="VALIDATION_ERROR")
        return

    sub = check_subscription()
    deals = _get_deals()

    # 检查商机数量限制
    if len(deals) >= sub["max_deals"]:
        limit = sub["max_deals"]
        if sub["tier"] == "free":
            output_error(
                f"免费版最多管理 {limit} 个商机，当前已有 {len(deals)} 个。"
                "请升级至付费版（¥149/月）以管理更多商机。",
                code="LIMIT_EXCEEDED",
            )
        else:
            output_error(
                f"已达到商机数量上限 {limit} 个。",
                code="LIMIT_EXCEEDED",
            )
        return

    # 校验阶段
    stage = data.get("stage", "线索")
    try:
        validate_deal_stage(stage)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 解析金额
    amount = 0.0
    if "amount" in data:
        amount = parse_amount(str(data["amount"]))

    # 概率：若未提供则根据阶段自动设定
    probability = data.get("probability")
    if probability is None:
        probability = get_stage_probability(stage)
    else:
        try:
            probability = int(probability)
            probability = max(0, min(100, probability))
        except (TypeError, ValueError):
            probability = get_stage_probability(stage)

    # 标签处理
    tags = data.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    now = now_iso()
    deal = {
        "id": generate_id("D"),
        "name": data["name"],
        "contact_name": data.get("contact_name", ""),
        "contact_phone": data.get("contact_phone", ""),
        "contact_email": data.get("contact_email", ""),
        "company": data.get("company", ""),
        "amount": amount,
        "stage": stage,
        "probability": probability,
        "source": data.get("source", ""),
        "expected_close_date": data.get("expected_close_date", ""),
        "notes": data.get("notes", ""),
        "tags": tags,
        "created_at": now,
        "updated_at": now,
        "stage_history": [
            {"stage": stage, "timestamp": now},
        ],
    }

    deals.append(deal)
    _save_deals(deals)

    display = _mask_deal(deal)
    display["amount_display"] = format_currency(deal["amount"])
    output_success({"message": f"商机「{deal['name']}」已添加", "deal": display})


def update_deal(data: Dict[str, Any]) -> None:
    """更新商机信息。

    必填字段: id
    可更新字段: name, contact_name, contact_phone, contact_email, company,
                amount, stage, probability, source, expected_close_date, notes, tags

    Args:
        data: 包含商机 ID 和待更新字段的字典。
    """
    deal_id = data.get("id")
    if not deal_id:
        output_error("商机ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    deals = _get_deals()
    deal = _find_deal(deals, deal_id)
    if not deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    updatable_fields = [
        "name", "contact_name", "contact_phone", "contact_email",
        "company", "source", "expected_close_date", "notes",
    ]
    updated = False

    for field in updatable_fields:
        if field in data:
            deal[field] = data[field]
            updated = True

    # 金额特殊处理
    if "amount" in data:
        deal["amount"] = parse_amount(str(data["amount"]))
        updated = True

    # 概率特殊处理
    if "probability" in data:
        try:
            deal["probability"] = max(0, min(100, int(data["probability"])))
            updated = True
        except (TypeError, ValueError):
            output_error("概率（probability）必须为 0-100 的整数", code="VALIDATION_ERROR")
            return

    # 标签特殊处理
    if "tags" in data:
        tags = data["tags"]
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        deal["tags"] = tags
        updated = True

    # 阶段变更追踪
    if "stage" in data:
        new_stage = data["stage"]
        try:
            validate_deal_stage(new_stage)
        except ValueError as e:
            output_error(str(e), code="VALIDATION_ERROR")
            return

        old_stage = deal.get("stage")
        if new_stage != old_stage:
            deal["stage"] = new_stage
            # 若未手动设置概率，自动更新为新阶段的默认概率
            if "probability" not in data:
                deal["probability"] = get_stage_probability(new_stage)
            # 记录阶段历史
            if "stage_history" not in deal:
                deal["stage_history"] = []
            deal["stage_history"].append({
                "stage": new_stage,
                "timestamp": now_iso(),
            })
            updated = True

    if not updated:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    deal["updated_at"] = now_iso()
    _save_deals(deals)

    display = _mask_deal(deal)
    display["amount_display"] = format_currency(deal["amount"])
    output_success({"message": f"商机「{deal['name']}」已更新", "deal": display})


def delete_deal(data: Dict[str, Any]) -> None:
    """删除商机。

    必填字段: id

    Args:
        data: 包含商机 ID 的字典。
    """
    deal_id = data.get("id")
    if not deal_id:
        output_error("商机ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    deals = _get_deals()
    original_count = len(deals)
    deals = [d for d in deals if d.get("id") != deal_id]

    if len(deals) == original_count:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    _save_deals(deals)
    output_success({"message": f"商机 {deal_id} 已删除"})


def get_deal(data: Dict[str, Any]) -> None:
    """获取单个商机详情。

    必填字段: id

    Args:
        data: 包含商机 ID 的字典。
    """
    deal_id = data.get("id")
    if not deal_id:
        output_error("商机ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    deals = _get_deals()
    deal = _find_deal(deals, deal_id)
    if not deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    display = _mask_deal(deal)
    display["amount_display"] = format_currency(deal["amount"])
    display["days_since_update"] = calculate_days_since(deal.get("updated_at", ""))
    output_success(display)


def list_deals(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有商机。

    可选过滤: stage, keyword（搜索名称/公司/联系人）, tag, min_amount, max_amount

    Args:
        data: 可选的过滤条件字典。
    """
    deals = _get_deals()

    if data:
        # 阶段过滤
        stage_filter = data.get("stage")
        if stage_filter:
            deals = [d for d in deals if d.get("stage") == stage_filter]

        # 关键词搜索
        keyword = data.get("keyword", "").strip()
        if keyword:
            keyword_lower = keyword.lower()
            deals = [
                d for d in deals
                if keyword_lower in d.get("name", "").lower()
                or keyword_lower in d.get("company", "").lower()
                or keyword_lower in d.get("contact_name", "").lower()
            ]

        # 标签过滤
        tag_filter = data.get("tag")
        if tag_filter:
            deals = [d for d in deals if tag_filter in d.get("tags", [])]

        # 金额范围过滤
        min_amount = data.get("min_amount")
        if min_amount is not None:
            deals = [d for d in deals if d.get("amount", 0) >= float(min_amount)]

        max_amount = data.get("max_amount")
        if max_amount is not None:
            deals = [d for d in deals if d.get("amount", 0) <= float(max_amount)]

    # 按更新时间倒序排列
    deals.sort(key=lambda d: d.get("updated_at", ""), reverse=True)

    # 脱敏处理
    display_list = []
    for d in deals:
        display = _mask_deal(d)
        display["amount_display"] = format_currency(d.get("amount", 0))
        display_list.append(display)

    # 按阶段分组统计
    stage_stats = {}
    for stage in DEAL_STAGES:
        stage_deals = [d for d in deals if d.get("stage") == stage]
        stage_stats[stage] = {
            "count": len(stage_deals),
            "total_amount": sum(d.get("amount", 0) for d in stage_deals),
        }

    # 汇总
    total_amount = sum(d.get("amount", 0) for d in deals)

    output_success({
        "total": len(display_list),
        "total_amount": total_amount,
        "total_amount_display": format_currency(total_amount),
        "stage_stats": stage_stats,
        "deals": display_list,
    })


def stage_history(data: Dict[str, Any]) -> None:
    """查看商机的阶段变更历史。

    必填字段: id

    Args:
        data: 包含商机 ID 的字典。
    """
    deal_id = data.get("id")
    if not deal_id:
        output_error("商机ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    deals = _get_deals()
    deal = _find_deal(deals, deal_id)
    if not deal:
        output_error(f"未找到ID为 {deal_id} 的商机", code="NOT_FOUND")
        return

    history = deal.get("stage_history", [])
    output_success({
        "deal_id": deal_id,
        "deal_name": deal.get("name", ""),
        "current_stage": deal.get("stage", ""),
        "history": history,
        "total_changes": len(history),
    })


def import_deals(data: Dict[str, Any]) -> None:
    """从 CSV 文件导入商机数据。

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
    deals = _get_deals()
    imported = 0
    skipped = 0
    errors = []

    # 中英文列名映射
    column_map = {
        "名称": "name", "商机名称": "name",
        "联系人": "contact_name", "联系人姓名": "contact_name",
        "手机": "contact_phone", "电话": "contact_phone",
        "邮箱": "contact_email",
        "公司": "company", "公司名称": "company",
        "金额": "amount", "预算": "amount",
        "阶段": "stage",
        "概率": "probability",
        "来源": "source",
        "预计成交日期": "expected_close_date",
        "备注": "notes",
        "标签": "tags",
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                if len(deals) >= sub["max_deals"]:
                    errors.append(f"行 {row_num}: 已达商机数量上限 {sub['max_deals']}")
                    skipped += 1
                    continue

                # 映射中文列名
                mapped = {}
                for key, value in row.items():
                    mapped_key = column_map.get(key, key)
                    mapped[mapped_key] = value

                name = mapped.get("name", "").strip()
                if not name:
                    errors.append(f"行 {row_num}: 缺少商机名称")
                    skipped += 1
                    continue

                stage = mapped.get("stage", "").strip() or "线索"
                if stage not in DEAL_STAGES:
                    stage = "线索"

                amount = parse_amount(mapped.get("amount", ""))

                probability = mapped.get("probability", "")
                if probability:
                    try:
                        probability = max(0, min(100, int(probability)))
                    except (TypeError, ValueError):
                        probability = get_stage_probability(stage)
                else:
                    probability = get_stage_probability(stage)

                tags = mapped.get("tags", "")
                if isinstance(tags, str) and tags:
                    tags = [t.strip() for t in tags.split(",") if t.strip()]
                else:
                    tags = []

                now = now_iso()
                deal = {
                    "id": generate_id("D"),
                    "name": name,
                    "contact_name": mapped.get("contact_name", "").strip(),
                    "contact_phone": mapped.get("contact_phone", "").strip(),
                    "contact_email": mapped.get("contact_email", "").strip(),
                    "company": mapped.get("company", "").strip(),
                    "amount": amount,
                    "stage": stage,
                    "probability": probability,
                    "source": mapped.get("source", "").strip(),
                    "expected_close_date": mapped.get("expected_close_date", "").strip(),
                    "notes": mapped.get("notes", "").strip(),
                    "tags": tags,
                    "created_at": now,
                    "updated_at": now,
                    "stage_history": [
                        {"stage": stage, "timestamp": now},
                    ],
                }
                deals.append(deal)
                imported += 1

    except Exception as e:
        output_error(f"导入失败: {e}", code="IMPORT_ERROR")
        return

    _save_deals(deals)
    result = {
        "message": f"导入完成：成功 {imported} 条，跳过 {skipped} 条",
        "imported": imported,
        "skipped": skipped,
        "total": len(deals),
    }
    if errors:
        result["errors"] = errors[:10]
    output_success(result)


def export_deals(data: Optional[Dict[str, Any]] = None) -> None:
    """导出商机数据到 CSV 格式。

    可选字段: file_path（若不指定则输出到 stdout）

    Args:
        data: 可选的配置字典。
    """
    deals = _get_deals()
    if not deals:
        output_error("暂无商机数据可导出", code="NO_DATA")
        return

    file_path = data.get("file_path") if data else None
    fieldnames = [
        "id", "name", "contact_name", "contact_phone", "contact_email",
        "company", "amount", "stage", "probability", "source",
        "expected_close_date", "notes", "tags", "created_at", "updated_at",
    ]

    try:
        if file_path:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for d in deals:
                    row = {}
                    for k in fieldnames:
                        val = d.get(k, "")
                        if k == "tags" and isinstance(val, list):
                            val = ",".join(val)
                        row[k] = val
                    writer.writerow(row)
            output_success({
                "message": f"已导出 {len(deals)} 条商机数据到 {file_path}",
                "count": len(deals),
            })
        else:
            output_buf = io.StringIO()
            writer = csv.DictWriter(output_buf, fieldnames=fieldnames)
            writer.writeheader()
            for d in deals:
                row = {}
                for k in fieldnames:
                    val = d.get(k, "")
                    if k == "tags" and isinstance(val, list):
                        val = ",".join(val)
                    row[k] = val
                writer.writerow(row)
            output_success({"csv": output_buf.getvalue(), "count": len(deals)})
    except IOError as e:
        output_error(f"导出失败: {e}", code="EXPORT_ERROR")


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer 商机数据管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "add": lambda: add_deal(data or {}),
        "update": lambda: update_deal(data or {}),
        "delete": lambda: delete_deal(data or {}),
        "get": lambda: get_deal(data or {}),
        "list": lambda: list_deals(data),
        "import": lambda: import_deals(data or {}),
        "export": lambda: export_deals(data),
        "stage-history": lambda: stage_history(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
