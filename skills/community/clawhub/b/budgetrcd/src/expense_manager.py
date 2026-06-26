"""
Expense Manager - 开销记录 CRUD 操作
- add_expense:     追加记录（无需确认，完全权限）
- get_expenses:   读取指定月份所有记录
- update_expense: 更新记录（需用户确认）
- delete_expense: 删除记录（需用户确认）
- get_date_total: 计算指定日期总支出
"""
import os, json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("~/Documents/02_Personal/01_Budget").expanduser()
DATA_DIR_DATA = DATA_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"

def _read_expenses(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def _write_expenses(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def _get_file_path(month=None):
    """获取 expense 文件路径"""
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    m = month.replace("-", "")
    return DATA_DIR_DATA / f"expense_{m}.json"

def get_expenses(month=None):
    """
    读取指定月份所有开销记录
    month: YYYY-MM 格式
    """
    path = _get_file_path(month)
    return _read_expenses(path)

def add_expense(date, pool, amount, note, image_path=None, source_text=None):
    """
    追加一笔开销记录（完全权限，无需确认）
    
    Args:
        date: YYYY-MM-DD
        pool: 分类如 "food", "transport", "fun"
        amount: 金额（正数）
        note: 描述
        image_path: 可选，图片路径
        source_text: 可选，原始文本
    
    Returns:
        新增的记录对象
    """
    month = date[:7]  # YYYY-MM
    path = _get_file_path(month)
    records = _read_expenses(path)
    
    new_record = {
        "date": date,
        "pool": pool,
        "amount": amount,
        "note": note
    }
    if image_path:
        new_record["image_path"] = image_path
    if source_text:
        new_record["source_text"] = source_text
    
    records.append(new_record)
    _write_expenses(path, records)
    
    return new_record

def add_expenses_from_list(records):
    """
    批量追加开销记录（完全权限）
    
    Args:
        records: list of dict, 每项包含 date, pool, amount, note, 可选 image_path, source_text
    """
    # 按月份分组
    by_month = {}
    for r in records:
        month = r["date"][:7]
        by_month.setdefault(month, []).append(r)
    
    results = []
    for month, recs in by_month.items():
        path = _get_file_path(month)
        existing = _read_expenses(path)
        existing.extend(recs)
        _write_expenses(path, existing)
        results.extend(recs)
    
    return results

def update_expense(date, pool, amount, note, image_path=None):
    """
    更新已存在的记录（需要用户确认后才能调用）
    """
    month = date[:7]
    path = _get_file_path(month)
    records = _read_expenses(path)
    
    for i, r in enumerate(records):
        if r["date"] == date and r["pool"] == pool and r["amount"] == amount and r.get("note") == note:
            records[i] = {
                "date": date,
                "pool": pool,
                "amount": amount,
                "note": note
            }
            if image_path:
                records[i]["image_path"] = image_path
            _write_expenses(path, records)
            return records[i]
    
    return None

def delete_expense(date, pool, amount, note):
    """
    删除指定记录（需要用户确认后才能调用）
    返回被删除的记录，失败返回 None
    """
    month = date[:7]
    path = _get_file_path(month)
    records = _read_expenses(path)
    
    for i, r in enumerate(records):
        if r["date"] == date and r["pool"] == pool and r["amount"] == amount and r.get("note") == note:
            deleted = records.pop(i)
            _write_expenses(path, records)
            return deleted
    
    return None

def get_date_total(date):
    """计算指定日期的总支出"""
    month = date[:7]
    records = get_expenses(month)
    return sum(r["amount"] for r in records if r["date"] == date)

def get_month_total(month=None):
    """计算指定月份的总支出"""
    records = get_expenses(month)
    return sum(r["amount"] for r in records)

def copy_image_to_budget(source_path, date, merchant_keyword):
    """
    复制图片到 budget-data/images 目录
    返回新的图片路径
    """
    if not source_path or not Path(source_path).exists():
        return None
    
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    new_name = f"{date}_{merchant_keyword}.jpg"
    new_path = IMAGES_DIR / new_name
    
    import shutil
    shutil.copy2(source_path, new_path)
    return str(new_path)
