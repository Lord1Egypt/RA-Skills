#!/usr/bin/env python3
"""
家庭财务数据管理器
处理：资产负债表、现金流量表、投资组合
数据存储：本地 JSON 文件
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "family-finances"
DATA_DIR.mkdir(parents=True, exist_ok=True)

BALANCE_FILE = DATA_DIR / "balance_sheet.json"
CASHFLOW_FILE = DATA_DIR / "cashflow.json"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
METADATA_FILE = DATA_DIR / "metadata.json"


def _load_json(path: Path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── 资产负债表 ───────────────────────────────────────────

def get_balance_sheet():
    return _load_json(BALANCE_FILE, {
        "assets": {},
        "liabilities": {},
        "last_updated": None
    })


def save_balance_sheet(assets: dict, liabilities: dict):
    now = datetime.now().isoformat()
    data = {"assets": assets, "liabilities": liabilities, "last_updated": now}
    _save_json(BALANCE_FILE, data)
    return {"status": "ok", "last_updated": now}


def update_asset(name: str, amount: float, category: str = "其他", note: str = ""):
    bs = get_balance_sheet()
    bs["assets"][name] = {
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "updated_at": datetime.now().isoformat()
    }
    save_balance_sheet(bs["assets"], bs["liabilities"])


def update_liability(name: str, amount: float, category: str = "其他", note: str = ""):
    bs = get_balance_sheet()
    bs["liabilities"][name] = {
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "updated_at": datetime.now().isoformat()
    }
    save_balance_sheet(bs["assets"], bs["liabilities"])


def delete_asset(name: str):
    bs = get_balance_sheet()
    bs["assets"].pop(name, None)
    save_balance_sheet(bs["assets"], bs["liabilities"])


def delete_liability(name: str):
    bs = get_balance_sheet()
    bs["liabilities"].pop(name, None)
    save_balance_sheet(bs["assets"], bs["liabilities"])


def calc_net_worth():
    bs = get_balance_sheet()
    total_assets = sum(v["amount"] for v in bs["assets"].values())
    total_liabilities = sum(v["amount"] for v in bs["liabilities"].values())
    net_worth = total_assets - total_liabilities
    return {
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "net_worth": round(net_worth, 2),
        "debt_ratio": round(total_liabilities / total_assets * 100, 2) if total_assets > 0 else 0,
        "assets_count": len(bs["assets"]),
        "liabilities_count": len(bs["liabilities"])
    }


# ─── 现金流量表 ───────────────────────────────────────────

def get_cashflow(year_month: str = None) -> dict:
    """year_month: 'YYYY-MM' 格式，不传则返回所有月份"""
    all_data = _load_json(CASHFLOW_FILE, {})
    if year_month:
        return all_data.get(year_month, {"income": {}, "expenses": {}, "transfers": {}})
    return all_data


def save_cashflow_month(year_month: str, income: dict, expenses: dict, transfers: dict = None):
    all_data = _load_json(CASHFLOW_FILE, {})
    all_data[year_month] = {
        "income": income,
        "expenses": expenses,
        "transfers": transfers or {},
        "updated_at": datetime.now().isoformat()
    }
    _save_json(CASHFLOW_FILE, all_data)
    return {"status": "ok", "year_month": year_month}


def add_cashflow_item(year_month: str, item_type: str, category: str, amount: float, description: str = ""):
    """item_type: 'income' | 'expense' | 'transfer'"""
    # normalize key: income→income, expense→expenses
    storage_key = "income" if item_type == "income" else "expenses" if item_type == "expense" else "transfers"
    all_data = _load_json(CASHFLOW_FILE, {})
    if year_month not in all_data:
        all_data[year_month] = {"income": {}, "expenses": {}, "transfers": {}}
    key = f"{category}_{datetime.now().timestamp()}"
    item = {"amount": round(amount, 2), "description": description, "created_at": datetime.now().isoformat()}
    all_data[year_month][storage_key][key] = item
    _save_json(CASHFLOW_FILE, all_data)
    return {"status": "ok"}


def calc_cashflow_summary(year_month: str):
    data = get_cashflow(year_month)
    total_income = sum(v["amount"] for v in data.get("income", {}).values())
    total_expenses = sum(v["amount"] for v in data.get("expenses", {}).values())
    net_cashflow = total_income - total_expenses
    savings_rate = round(net_cashflow / total_income * 100, 2) if total_income > 0 else 0
    return {
        "year_month": year_month,
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_cashflow": round(net_cashflow, 2),
        "savings_rate": savings_rate,
        "income_breakdown": data.get("income", {}),
        "expense_breakdown": data.get("expenses", {}),
    }


# ─── 投资组合 ─────────────────────────────────────────────

CATEGORIES = ["股票", "基金", "债券", "保险", "房产", "车辆", "现金存款", "数字资产", "其他"]

def get_portfolio():
    return _load_json(PORTFOLIO_FILE, {
        "holdings": {},
        "last_updated": None
    })


def save_portfolio(holdings: dict):
    now = datetime.now().isoformat()
    data = {"holdings": holdings, "last_updated": now}
    _save_json(PORTFOLIO_FILE, data)
    return {"status": "ok", "last_updated": now}


def update_holding(name: str, amount: float, category: str, note: str = ""):
    pf = get_portfolio()
    if category not in CATEGORIES:
        category = "其他"
    pf["holdings"][name] = {
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "updated_at": datetime.now().isoformat()
    }
    save_portfolio(pf["holdings"])


def delete_holding(name: str):
    pf = get_portfolio()
    pf["holdings"].pop(name, None)
    save_portfolio(pf["holdings"])


def calc_portfolio_summary():
    pf = get_portfolio()
    holdings = pf["holdings"]
    total = sum(v["amount"] for v in holdings.values())
    breakdown = {}
    for name, v in holdings.items():
        cat = v["category"]
        if cat not in breakdown:
            breakdown[cat] = 0
        breakdown[cat] += v["amount"]
    pct_breakdown = {
        cat: {"amount": round(amount, 2), "pct": round(amount / total * 100, 2) if total > 0 else 0}
        for cat, amount in breakdown.items()
    }
    return {
        "total": round(total, 2),
        "holdings_count": len(holdings),
        "category_breakdown": pct_breakdown
    }


# ─── 综合报告 ─────────────────────────────────────────────

def generate_report(year_month: str = None):
    """生成完整财务报告"""
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")
    
    nw = calc_net_worth()
    cf = calc_cashflow_summary(year_month) if year_month else None
    ps = calc_portfolio_summary()
    
    report = {
        "report_date": datetime.now().isoformat(),
        "year_month": year_month,
        "balance_sheet": nw,
        "portfolio": ps,
    }
    
    if cf:
        report["cashflow"] = cf
        
        # 财务健康评分
        scores = {}
        # 储蓄率评分 (满分25)
        sr = cf.get("savings_rate", 0)
        scores["savings_rate"] = min(25, round(sr / 40 * 25, 1)) if sr >= 0 else 0
        # 净资产评分 (满分25)
        nw_val = nw.get("net_worth", 0)
        scores["net_worth"] = min(25, round(nw_val / 1000000 * 25, 1))
        # 资产结构评分 (满分25)
        debt_ratio = nw.get("debt_ratio", 0)
        scores["asset_structure"] = round(max(0, 25 - debt_ratio / 4), 1)
        # 投资评分 (满分25)
        inv_ratio = round(ps.get("total", 0) / nw.get("total_assets", 1) * 100, 2) if nw.get("total_assets", 0) > 0 else 0
        scores["investment"] = min(25, round(inv_ratio / 50 * 25, 1))
        
        total_score = round(sum(scores.values()), 1)
        if total_score >= 90:
            grade = "优秀"
        elif total_score >= 70:
            grade = "良好"
        elif total_score >= 50:
            grade = "一般"
        else:
            grade = "需改善"
        
        report["health_score"] = {
            "total": total_score,
            "grade": grade,
            "dimensions": scores
        }
    
    return report


# ─── CLI 入口 ─────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    
    if cmd == "report":
        ym = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(generate_report(ym), ensure_ascii=False, indent=2))
    
    elif cmd == "balance":
        print(json.dumps(get_balance_sheet(), ensure_ascii=False, indent=2))
    
    elif cmd == "net-worth":
        print(json.dumps(calc_net_worth(), ensure_ascii=False, indent=2))
    
    elif cmd == "cashflow":
        ym = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m")
        print(json.dumps(calc_cashflow_summary(ym), ensure_ascii=False, indent=2))
    
    elif cmd == "portfolio":
        print(json.dumps(calc_portfolio_summary(), ensure_ascii=False, indent=2))
    
    elif cmd == "add-asset":
        # python finances.py add-asset "存款" 500000 "现金存款" "备注"
        name, amount, cat = sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "其他"
        note = sys.argv[5] if len(sys.argv) > 5 else ""
        print(json.dumps(update_asset(name, amount, cat, note), ensure_ascii=False))
    
    elif cmd == "add-liability":
        name, amount, cat = sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "其他"
        note = sys.argv[5] if len(sys.argv) > 5 else ""
        print(json.dumps(update_liability(name, amount, cat, note), ensure_ascii=False))
    
    elif cmd == "add-portfolio":
        name, amount, cat = sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "其他"
        note = sys.argv[5] if len(sys.argv) > 5 else ""
        print(json.dumps(update_holding(name, amount, cat, note), ensure_ascii=False))
    
    elif cmd == "add-cashflow":
        # python finances.py add-cashflow 2026-04 income "工资" 30000 "月薪"
        ym, itype, cat = sys.argv[2], sys.argv[3], sys.argv[4]
        amount = float(sys.argv[5])
        desc = sys.argv[6] if len(sys.argv) > 6 else ""
        print(json.dumps(add_cashflow_item(ym, itype, cat, amount, desc), ensure_ascii=False))
    
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
