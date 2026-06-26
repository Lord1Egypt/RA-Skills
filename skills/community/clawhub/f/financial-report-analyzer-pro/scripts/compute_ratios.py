"""Compute the headline financial ratios."""
from __future__ import annotations
from typing import Any, Dict

def _g(d: Dict[str, Any], *keys: str) -> float:
    for k in keys:
        v = d.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return 0.0

def compute_ratios(fin: Dict[str, Any]) -> Dict[str, Any]:
    is_ = fin.get("income_statement", {}) or {}
    bs = fin.get("balance_sheet", {}) or {}
    cf = fin.get("cash_flow", {}) or {}

    revenue = _g(is_, "revenue", "营业收入")
    gross_profit = revenue - _g(is_, "cost_of_revenue", "营业成本")
    operating_income = _g(is_, "operating_income", "营业利润")
    net_income = _g(is_, "net_income", "净利润")
    total_assets = _g(bs, "total_assets", "资产总计")
    total_equity = _g(bs, "total_equity", "股东权益合计")
    total_liab = _g(bs, "total_liabilities", "负债合计")
    ocf = _g(cf, "operating_cash_flow", "经营活动产生的现金流量净额")

    def safe_div(num: float, den: float) -> float:
        return round(num / den, 4) if den else 0.0

    return {
        "profitability": {
            "gross_margin": safe_div(gross_profit, revenue),
            "operating_margin": safe_div(operating_income, revenue),
            "net_margin": safe_div(net_income, revenue),
            "roa": safe_div(net_income, total_assets),
            "roe": safe_div(net_income, total_equity),
        },
        "leverage": {
            "debt_ratio": safe_div(total_liab, total_assets),
            "equity_multiplier": safe_div(total_assets, total_equity),
        },
        "cash_quality": {
            "ocf_to_net_income": safe_div(ocf, net_income),
        },
    }
