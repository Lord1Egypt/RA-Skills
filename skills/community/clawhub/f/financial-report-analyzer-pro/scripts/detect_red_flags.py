"""Apply heuristic red-flag checks. Returns a list of findings."""
from __future__ import annotations
from typing import Any, Dict, List

def detect_red_flags(fin: Dict[str, Any]) -> List[Dict[str, Any]]:
    flags: List[Dict[str, Any]] = []
    is_ = fin.get("income_statement", {}) or {}
    bs = fin.get("balance_sheet", {}) or {}
    cf = fin.get("cash_flow", {}) or {}

    revenue = is_.get("revenue") or 0
    receivables = bs.get("accounts_receivable") or 0
    prev_revenue = (fin.get("prior_year") or {}).get("revenue") or 0
    prev_receivables = (fin.get("prior_year") or {}).get("accounts_receivable") or 0
    net_income = is_.get("net_income") or 0
    ocf = cf.get("operating_cash_flow") or 0
    goodwill = bs.get("goodwill") or 0
    equity = bs.get("total_equity") or 0

    if prev_revenue and prev_receivables:
        rev_growth = (revenue - prev_revenue) / prev_revenue if prev_revenue else 0
        ar_growth = (receivables - prev_receivables) / prev_receivables if prev_receivables else 0
        if ar_growth > rev_growth + 0.15:
            flags.append({
                "code": "RF01", "severity": "🟡",
                "title": "应收账款增速显著高于营收增速",
                "evidence": f"AR growth {ar_growth:.1%} vs Revenue growth {rev_growth:.1%}",
            })

    if net_income and ocf / max(net_income, 1) < 0.5:
        flags.append({
            "code": "RF02", "severity": "🟡",
            "title": "经营性现金流/净利润比 < 0.5",
            "evidence": f"OCF/NI = {ocf/max(net_income,1):.2f}",
        })

    if equity and goodwill / max(equity, 1) > 0.3:
        flags.append({
            "code": "RF03", "severity": "🔴",
            "title": "商誉占净资产 > 30%",
            "evidence": f"Goodwill/Equity = {goodwill/max(equity,1):.1%}",
        })

    return flags
