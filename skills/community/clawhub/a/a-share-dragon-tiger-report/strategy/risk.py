#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""风控：α 预算账本、回撤熔断、单票/单行业暴露上限、凯利建议仓位。

账本（AlphaLedger）是有状态的，其余函数为纯函数。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from . import formulas as F

# 单一标的 / 单一行业的名义暴露上限（占权益比）
MAX_SINGLE_NAME = 0.10
MAX_SINGLE_SECTOR = 0.30


# ------------------------------------------------------------------ α 账本
@dataclass
class Position:
    code: str
    name: str
    shares: int
    entry: float
    stop: float
    sector: str = ""

    @property
    def notional(self) -> float:
        return self.shares * self.entry

    @property
    def risk_amount(self) -> float:
        return self.shares * max(0.0, self.entry - self.stop)


@dataclass
class AlphaLedger:
    """累计 α 预算账本。

    约束：Σ开仓名义 <= α_max × 权益。任何一笔加仓前必须先 `can_open` 检查。
    """
    equity: float
    stage: str = "II"
    ice_point: bool = False
    positions: list[Position] = field(default_factory=list)

    @property
    def alpha_budget(self) -> float:
        return F.alpha_max(self.stage, self.ice_point)

    @property
    def open_notional(self) -> float:
        return sum(p.notional for p in self.positions)

    @property
    def remaining(self) -> float:
        return F.alpha_remaining(self.open_notional, self.equity, self.alpha_budget)

    def can_open(self, notional: float, sector: str = "") -> tuple[bool, str]:
        """三道检查：α 总预算、单票上限、单行业上限。"""
        if notional <= 0:
            return False, "开仓名义必须为正"
        if not F.cumulative_alpha_ok(self.open_notional + notional, self.equity, self.alpha_budget):
            return False, (
                f"超 α 预算：已开 {self.open_notional/self.equity:.2%} + 本次 {notional/self.equity:.2%} "
                f"> 上限 {self.alpha_budget:.2%}"
            )
        if notional > MAX_SINGLE_NAME * self.equity + 1e-9:
            return False, f"超单票上限：{notional/self.equity:.2%} > {MAX_SINGLE_NAME:.0%}"
        if sector:
            same = sum(p.notional for p in self.positions if p.sector == sector)
            if same + notional > MAX_SINGLE_SECTOR * self.equity + 1e-9:
                return False, (
                    f"超单行业上限：{sector} 已 {same/self.equity:.2%} + 本次 {notional/self.equity:.2%} "
                    f"> {MAX_SINGLE_SECTOR:.0%}"
                )
        return True, "通过"

    def add(self, pos: Position) -> tuple[bool, str]:
        ok, msg = self.can_open(pos.notional, pos.sector)
        if ok:
            self.positions.append(pos)
        return ok, msg

    def snapshot(self) -> dict[str, Any]:
        return {
            "equity": self.equity,
            "stage": self.stage,
            "ice_point": self.ice_point,
            "alpha_budget": self.alpha_budget,
            "open_notional": round(self.open_notional, 2),
            "used_pct": round(self.open_notional / self.equity, 4) if self.equity else 0.0,
            "remaining": round(self.remaining, 2),
            "positions": len(self.positions),
            "total_risk": round(sum(p.risk_amount for p in self.positions), 2),
        }


# ------------------------------------------------------------------ 熔断
def risk_check(equity_peak: float, equity_now: float) -> dict[str, Any]:
    """回撤熔断检查。返回 action ∈ {NORMAL, REDUCE, HALT}。"""
    if equity_peak <= 0:
        raise ValueError("峰值权益必须为正")
    dd = max(0.0, (equity_peak - equity_now) / equity_peak)
    state = F.circuit_breaker(dd)
    return {
        "drawdown": round(dd, 4),
        "action": state.action,
        "note": state.note,
    }


def suggested_size(row: dict[str, Any], ledger: AlphaLedger) -> dict[str, Any]:
    """给定标的与账本，算出建议股数并做三道限额校验。"""
    entry, stop = float(row["entry"]), float(row["stop"])
    shares = F.position_size(ledger.equity, entry, stop, ledger.ice_point)
    notional = F.position_notional(shares, entry)
    ok, msg = ledger.can_open(notional, str(row.get("sector", "")))
    if not ok:
        # 收缩到剩余额度能容纳的股数
        cap = min(ledger.remaining, MAX_SINGLE_NAME * ledger.equity)
        shares = int(cap // entry) if entry > 0 else 0
        notional = F.position_notional(shares, entry)
        ok2, msg2 = ledger.can_open(notional, str(row.get("sector", "")))
        return {
            "shares": shares, "notional": notional, "allowed": ok2,
            "note": f"{msg} → 已收缩至 {shares} 股；复核：{msg2}",
        }
    return {"shares": shares, "notional": notional, "allowed": True, "note": msg}


def kelly_sizing(p: float, b: float, equity: float) -> dict[str, float]:
    """凯利建议仓位（已折半并封顶 25%）。"""
    frac = F.kelly_fraction(p, b)
    return {"fraction": frac, "notional": round(frac * equity, 2)}


def drawdown_table(thresholds: Sequence[float] = (0.05, 0.10, 0.15, 0.20, 0.25)) -> list[dict[str, Any]]:
    """熔断阶梯表，供报告渲染。"""
    out = []
    for t in thresholds:
        s = F.circuit_breaker(t)
        out.append({"threshold": t, "action": s.action, "note": s.note})
    return out
