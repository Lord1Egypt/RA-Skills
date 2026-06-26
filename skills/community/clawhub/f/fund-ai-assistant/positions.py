"""
持仓记录模块 - 管理用户的基金买入/卖出操作

直接 import 使用（推荐）：
  from positions import add_record, get_position, get_all_positions

直接运行测试：
  python3 positions.py
  （仅当 positions.json 不存在时，自动创建3条示例数据用于演示）

数据文件：positions.json（由本模块自动创建于同目录）
"""
import json
import os
import uuid
from datetime import datetime, date
from typing import Optional

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
POSITIONS_FILE = os.path.join(SKILL_DIR, "positions.json")


def _load() -> dict:
    if os.path.exists(POSITIONS_FILE):
        try:
            with open(POSITIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save(data: dict):
    with open(POSITIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_record(fund_code: str, op_type: str, price: float, quantity: int,
               op_date: str, note: str = "") -> dict:
    """
    添加一条买入/卖出记录
    op_type: "buy" 或 "sell"
    """
    record = {
        "id": str(uuid.uuid4())[:8],
        "type": op_type,
        "date": op_date,
        "price": float(price),
        "quantity": int(quantity),
        "note": note,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    data = _load()
    data.setdefault(fund_code, [])
    data[fund_code].append(record)
    _save(data)
    return record


def remove_record(fund_code: str, record_id: str) -> bool:
    """删除指定记录"""
    data = _load()
    if fund_code not in data:
        return False
    original_len = len(data[fund_code])
    data[fund_code] = [r for r in data[fund_code] if r["id"] != record_id]
    if len(data[fund_code]) == original_len:
        return False
    if not data[fund_code]:
        del data[fund_code]
    _save(data)
    return True


def get_records(fund_code: str) -> list:
    """获取某基金所有记录，按日期排序（从早到晚）"""
    data = _load()
    records = data.get(fund_code, [])
    # 按日期排序
    try:
        records.sort(key=lambda r: r["date"])
    except Exception:
        pass
    return records


def get_all_positions() -> dict:
    """获取所有基金的当前持仓汇总"""
    data = _load()
    result = {}
    for fund_code, records in data.items():
        position = compute_position(records)
        if position:
            result[fund_code] = position
    return result


def compute_position(records: list) -> Optional[dict]:
    """
    根据买卖记录计算当前持仓
    records: 按日期排序的记录列表
    """
    if not records:
        return None

    total_quantity = 0
    total_cost = 0.0

    for r in records:
        if r["type"] == "buy":
            total_quantity += r["quantity"]
            total_cost += r["price"] * r["quantity"]
        elif r["type"] == "sell":
            # 减少份额和成本（按比例）
            if total_quantity > 0:
                sell_ratio = min(r["quantity"] / total_quantity, 1.0)
                total_cost *= (1 - sell_ratio)
                total_quantity -= r["quantity"]

    if total_quantity <= 0:
        return None

    avg_cost = total_cost / total_quantity

    # 持仓时长（从第一笔买入算起）
    try:
        first_buy_date = next(
            r["date"] for r in records if r["type"] == "buy"
        )
        hold_days = (date.today() - datetime.strptime(first_buy_date, "%Y-%m-%d").date()).days
    except Exception:
        hold_days = None

    # 各笔买入的时间（用于持仓曲线参考）
    buy_records = [r for r in records if r["type"] == "buy"]
    sell_records = [r for r in records if r["type"] == "sell"]

    return {
        "total_quantity": total_quantity,
        "avg_cost": round(avg_cost, 4),
        "total_cost": round(total_cost, 2),
        "hold_days": hold_days,
        "buy_count": len(buy_records),
        "sell_count": len(sell_records),
        "records": records,
    }


def get_position_for_fund(fund_code: str) -> Optional[dict]:
    """获取某基金的当前持仓"""
    records = get_records(fund_code)
    return compute_position(records) if records else None


if __name__ == "__main__":
    # 简单测试
    print("=== 持仓模块测试 ===")
    # 添加测试数据（仅当文件为空时）
    if not os.path.exists(POSITIONS_FILE):
        add_record("000001", "buy", 2.10, 1000, "2026-01-10", "测试买入")
        add_record("000001", "buy", 2.30, 500, "2026-02-01", "加仓")
        add_record("000001", "sell", 2.50, 300, "2026-03-01", "减仓")
        print("已创建测试数据")

    all_pos = get_all_positions()
    for code, pos in all_pos.items():
        print(f"\n{code}:")
        print(f"  持仓: {pos['total_quantity']}份")
        print(f"  成本价: {pos['avg_cost']:.4f}")
        print(f"  持仓天数: {pos['hold_days']}")
