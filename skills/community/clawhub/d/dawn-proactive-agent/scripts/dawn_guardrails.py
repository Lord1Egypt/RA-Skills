# -*- coding: utf-8 -*-
"""
曙光 安全护栏引擎 v1.0 (OpenAI Agents SDK-Inspired Guardrails)
交易前强制自检：仓位/流动性/异常波动/连续亏损降仓/黑名单
"""
import json, os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = WORKSPACE / "session-state.json"
LEARNINGS_DIR = WORKSPACE / ".learnings"

def log(m): print(f"[GUARD] {m}")
def warn(m): print(f"[WARN] {m}")

CONFIG = {
    "max_single_weight": 40.0,
    "max_total_weight": 80.0,
    "max_daily_buy": 500000,
    "blacklist": [],
    "consecutive_loss_cut_ratio": 0.5,
    "abnormal_volatility": 7.0,
    "min_cash_reserve": 50000,
}

def check_blacklist(code: str) -> Tuple[bool, str]:
    if code in CONFIG["blacklist"]:
        return False, f"{code} in blacklist"
    return True, ""

def check_weight_limit(code: str, target: float) -> Tuple[bool, str]:
    if target > CONFIG["max_single_weight"]:
        return False, f"{code} weight {target}% > limit {CONFIG['max_single_weight']}%"
    return True, ""

def check_cash(cash: float) -> Tuple[bool, str]:
    if cash < CONFIG["min_cash_reserve"]:
        return False, f"cash {cash:.0f} < reserve {CONFIG['min_cash_reserve']:.0f}"
    return True, ""

def check_losses() -> Tuple[bool, str]:
    rf = LEARNINGS_DIR / "REFLECTIONS.json"
    if not rf.exists():
        return True, ""
    try:
        refs = json.loads(rf.read_text(encoding="utf-8"))
    except:
        return True, ""
    losses = [r for r in refs[-10:] if r.get("pnl_pct", 0) < 0]
    if len(losses) >= 5:
        r = CONFIG["consecutive_loss_cut_ratio"]
        return False, f"{len(losses)} consecutive losses, cut to {r*100:.0f}%"
    elif len(losses) >= 3:
        warn(f"{len(losses)} consecutive losses")
    return True, ""

def check_vol(quotes: Dict[str, Dict]) -> List[str]:
    w = []
    t = CONFIG["abnormal_volatility"]
    for c, q in quotes.items():
        chg = abs(q.get("change_pct", 0))
        if chg > t:
            w.append(f"{c} volatility {q.get('change_pct',0):+.2f}%")
    return w

def pre_trade(code: str, action: str, target: float, cash: float, quotes: Dict, state: Dict) -> Tuple[bool, List]:
    warns = []
    checks = []
    ok, msg = check_blacklist(code)
    if not ok:
        return False, [msg]
    if action in ("buy", "add"):
        ok, msg = check_weight_limit(code, target)
        if not ok:
            checks.append(msg)
        warns.append(msg)
    ok, msg = check_cash(cash)
    if not ok:
        checks.append(msg)
    ok, msg = check_losses()
    if not ok:
        checks.append(msg)
    vw = check_vol(quotes)
    warns.extend(vw)
    if checks:
        warn(f"[BLOCK] {code} {action}: {' | '.join(checks)}")
    return len(checks) == 0, warns

def daily_report(state: Dict) -> str:
    L = ["="*50, "Daily Risk Report", "="*50]
    tw = sum(h.get("weight", 0) for h in state.get("holdings", {}).values())
    L.append(f"Total weight: {tw:.1f}% (limit {CONFIG['max_single_weight']}%)")
    for c, h in state.get("holdings", {}).items():
        w = h.get("weight", 0)
        if w > CONFIG["max_single_weight"]:
            L.append(f"  [OVER] {c} {h.get('name','')} {w:.1f}%")
    cash = state.get("available_cash", 0)
    L.append(f"Cash: {cash:,.0f}")
    return "\n".join(L)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.report:
        state = {}
        sf = STATE_FILE
        if sf.exists():
            try:
                state = json.loads(sf.read_text(encoding="utf-8"))
            except:
                pass
        print(daily_report(state))
