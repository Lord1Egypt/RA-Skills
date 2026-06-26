#!/usr/bin/env python3
"""
Budget Skill - Agent Entry Point
模块化数据访问，职责分离：
- config_manager:  配置读写
- expense_manager: 记账 CRUD（add 完全权限，update/delete 需确认）
- calculator:     预算计算
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.expense_manager import (
    add_expense,
    add_expenses_from_list,
    get_expenses,
    get_date_total,
    get_month_total,
    copy_image_to_budget
)
from src.config_manager import get_config, get_budget, set_budget
from src.calculator import calculate_budget_status

# ========================
# 读操作接口（直接调用）
# ========================

def read_budget_status(month=None):
    """读取月度预算状态"""
    return calculate_budget_status(month)

def read_month_expenses(month=None):
    """读取月度开销列表"""
    return get_expenses(month)

def read_today_expenses():
    """读取今日开销"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    expenses = get_expenses(today[:7])
    return [e for e in expenses if e["date"] == today]

def read_date_total(date):
    """读取指定日期总支出"""
    return get_date_total(date)

# ========================
# 写操作接口（权限分级）
# ========================

def add_expense_record(date, pool, amount, note, image_path=None, source_text=None):
    """
    新增开销记录【完全权限，无需确认】
    """
    new_path = None
    if image_path:
        new_path = copy_image_to_budget(image_path, date, note[:10])
    
    return add_expense(
        date=date,
        pool=pool,
        amount=amount,
        note=note,
        image_path=new_path,
        source_text=source_text
    )

def add_expense_batch(records):
    """
    批量新增开销记录【完全权限，无需确认】
    records: [{"date": "2026-04-05", "pool": "food", "amount": 20, "note": "鸡蛋灌饼"}, ...]
    """
    # 先处理图片复制
    for r in records:
        if r.get("image_path"):
            r["image_path"] = copy_image_to_budget(
                r["image_path"], r["date"], r.get("note", "")[:10]
            )
    return add_expenses_from_list(records)

# ========================
# 修改/删除接口【需用户确认】
# ========================
# 以下函数供 Agent 调用前，需先向用户确认：
#   "确认修改/删除这条记录吗？"

def update_expense_record(date, pool, amount, note, new_amount=None, new_note=None, new_image_path=None):
    """
    更新已存在的开销记录【需确认】
    """
    from src.expense_manager import update_expense
    if new_amount is None: new_amount = amount
    if new_note is None: new_note = note
    
    new_path = None
    if new_image_path:
        new_path = copy_image_to_budget(new_image_path, date, new_note[:10])
    
    return update_expense(date, pool, new_amount, new_note, new_path)

def delete_expense_record(date, pool, amount, note):
    """
    删除开销记录【需确认】
    """
    from src.expense_manager import delete_expense
    return delete_expense(date, pool, amount, note)

# ========================
# 工具函数
# ========================

def need_confirmation(action, record_desc):
    """
    检查是否需要确认的辅助函数
    返回需要确认的操作描述，供 Agent 显示给用户
    """
    if action in ("update", "delete", "modify", "remove"):
        return f"请确认要{action}这条记录吗？ {record_desc}"
    return None

if __name__ == "__main__":
    import json
    print("Budget Skill Modules Loaded:")
    print("  read: read_budget_status, read_month_expenses, read_today_expenses, read_date_total")
    print("  write (free): add_expense_record, add_expense_batch")
    print("  write (need confirm): update_expense_record, delete_expense_record")
