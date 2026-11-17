#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""财富密码核心公式：综合分 S、α 预算、仓位 N、斐波那契、凯利、冰点系数。

所有函数均为纯函数，无 IO、无全局状态，便于 `test_formulas.py` 自检。
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Mapping

# ------------------------------------------------------------------ 权重
S_WEIGHTS: Mapping[str, float] = {
    "tech": 0.30,    # 技术形态（低位 + 放量）
    "flow": 0.25,    # 资金流（龙虎榜净买、主力净流入）
    "fund": 0.20,    # 基本面（盈利、增速、筹码）
    "cycle": 0.15,   # 产业周期位置（政策 / 景气）
    "fib": 0.10,     # 位置（斐波那契回撤）
}

# α 预算上限（按市场阶段）
ALPHA_MAX: Mapping[str, float] = {
    "I": 0.40,     # 阶段 I：趋势启动
    "II": 0.30,    # 阶段 II：趋势延续
    "III": 0.15,   # 阶段 III：高位震荡
    "IV": 0.05,    # 阶段 IV：退潮
}

ICE_POINT_ALPHA_MULTIPLIER = 0.5   # 冰点期 α 预算 ×0.5

# 风险预算 r（单笔风险占权益比）
RISK_R_ICE = 0.005      # 冰点 0.5%
RISK_R_NORMAL = 0.01    # 常态 1%

# 熔断阈值
CIRCUIT_REDUCE = 0.15   # 回撤 >=15% 减仓
CIRCUIT_HALT = 0.25     # 回撤 >=25% 停机

KELLY_CAP = 0.25        # 凯利单次上限
KELLY_HAIRCUT = 0.5     # 凯利折半（保守）

# 考核带
TARGET_ANNUAL_LOW = 0.12
TARGET_ANNUAL_HIGH = 0.25


# ------------------------------------------------------------------ S 公式
@dataclass
class ScoreBreakdown:
    """综合分拆解，便于报告逐项展示。"""
    tech: float = 0.0
    flow: float = 0.0
    fund: float = 0.0
    cycle: float = 0.0
    fib: float = 0.0
    bonus: float = 0.0
    penalty: float = 0.0
    total: float = 0.0
    notes: list[str] = field(default_factory=list)


def composite_score(
    tech: float,
    flow: float,
    fund: float,
    cycle: float,
    fib: float,
    bonus: float = 0.0,
    penalty: float = 0.0,
) -> ScoreBreakdown:
    """S = 0.30·tech + 0.25·flow + 0.20·fund + 0.15·cycle + 0.10·fib (+bonus −penalty)

    各子项约定取值 0–100；bonus/penalty 为口径① ② ④ 带来的加减分。
    最终总分裁剪到 [0, 100]。
    """
    for name, v in (("tech", tech), ("flow", flow), ("fund", fund),
                    ("cycle", cycle), ("fib", fib)):
        if v is None:
            raise ValueError(f"子项 {name} 不能为 None")
        if not 0.0 <= float(v) <= 100.0:
            raise ValueError(f"子项 {name} 应在 0–100，实际 {v}")

    raw = (
        S_WEIGHTS["tech"] * tech
        + S_WEIGHTS["flow"] * flow
        + S_WEIGHTS["fund"] * fund
        + S_WEIGHTS["cycle"] * cycle
        + S_WEIGHTS["fib"] * fib
        + bonus
        - penalty
    )
    return ScoreBreakdown(
        tech=tech, flow=flow, fund=fund, cycle=cycle, fib=fib,
        bonus=bonus, penalty=penalty,
        total=round(max(0.0, min(100.0, raw)), 3),
    )


def weighted_parts(bd: ScoreBreakdown) -> list[tuple[str, float, float]]:
    """返回 [(子项, 权重, 加权得分)]，用于报告表格。"""
    return [
        ("技术 tech", S_WEIGHTS["tech"], round(S_WEIGHTS["tech"] * bd.tech, 3)),
        ("资金 flow", S_WEIGHTS["flow"], round(S_WEIGHTS["flow"] * bd.flow, 3)),
        ("基本面 fund", S_WEIGHTS["fund"], round(S_WEIGHTS["fund"] * bd.fund, 3)),
        ("周期 cycle", S_WEIGHTS["cycle"], round(S_WEIGHTS["cycle"] * bd.cycle, 3)),
        ("位置 fib", S_WEIGHTS["fib"], round(S_WEIGHTS["fib"] * bd.fib, 3)),
    ]


# ------------------------------------------------------------------ α 预算
def alpha_max(stage: str, ice_point: bool = False) -> float:
    """α_max = 阶段上限（冰点期 ×0.5）。

    stage ∈ {"I","II","III","IV"}；非法阶段抛 ValueError（不猜测）。
    """
    key = (stage or "").strip().upper()
    if key not in ALPHA_MAX:
        raise ValueError(f"未知市场阶段 {stage!r}，应为 {sorted(ALPHA_MAX)} 之一")
    base = ALPHA_MAX[key]
    return round(base * (ICE_POINT_ALPHA_MULTIPLIER if ice_point else 1.0), 6)


def cumulative_alpha_ok(open_notional: float, equity: float, alpha_budget: float) -> bool:
    """累计 α 约束：Σ开仓名义 <= α_max × 权益。"""
    if equity <= 0:
        raise ValueError("权益必须为正")
    return open_notional <= alpha_budget * equity + 1e-9


def alpha_remaining(open_notional: float, equity: float, alpha_budget: float) -> float:
    """剩余可开仓额度（元）。"""
    if equity <= 0:
        raise ValueError("权益必须为正")
    return max(0.0, alpha_budget * equity - open_notional)


# ------------------------------------------------------------------ 仓位 N
def position_size(
    equity: float,
    entry: float,
    stop: float,
    ice_point: bool = False,
    r: float | None = None,
) -> int:
    """N = floor(权益 × r / (entry − stop))

    r 缺省时按冰点 0.5% / 常态 1% 取。entry 必须 > stop，否则逻辑不成立。
    """
    if equity <= 0:
        raise ValueError("权益必须为正")
    if entry <= stop:
        raise ValueError(f"entry({entry}) 必须大于 stop({stop})，否则风险为负")
    rr = RISK_R_ICE if ice_point else RISK_R_NORMAL
    if r is not None:
        if r <= 0:
            raise ValueError("r 必须为正")
        rr = r
    return int(math.floor(equity * rr / (entry - stop)))


def position_notional(shares: int, entry: float) -> float:
    """开仓名义金额。"""
    if shares < 0:
        raise ValueError("股数不能为负")
    return round(shares * entry, 2)


# ------------------------------------------------------------------ 斐波那契
FIB_RATIOS: Mapping[str, float] = {
    "0.236": 0.236,
    "0.382": 0.382,
    "0.500": 0.500,
    "0.618": 0.618,
    "0.786": 0.786,
}


def fib_retracement(high: float, low: float) -> dict[str, float]:
    """由区间高低点给出各档回撤位（自高点向下）。"""
    if high <= low:
        raise ValueError("high 必须大于 low")
    span = high - low
    return {k: round(high - span * v, 4) for k, v in FIB_RATIOS.items()}


def fib_score(price: float, high: float, low: float) -> float:
    """位置分：峰值在**0.618 回撤位**（即自底向上 38.2% 处），向两侧线性衰减，返回 0–100。

    该点是经典「黄金坑」：既足够低，又未破位。
      * 价格 = 0.618 回撤位（pos 0.382）→ 100 分
      * 价格在区间顶（pos 1.0）→ 0 分（离高点太近，无安全垫）
      * 价格在区间底（pos 0.0）→ 约 38 分（深度超跌但已破位，风险高于黄金坑）
    """
    if high <= low:
        raise ValueError("high 必须大于 low")
    span = high - low
    pos = (price - low) / span          # 0=区间底 1=区间顶
    pos = max(0.0, min(1.0, pos))
    target = 1.0 - FIB_RATIOS["0.618"]  # 0.382 —— 0.618 回撤位在「自底向上」坐标中的位置
    return round(100.0 * (1.0 - min(1.0, abs(pos - target) / 0.618)), 3)


# ------------------------------------------------------------------ 凯利
def kelly_fraction(p: float, b: float) -> float:
    """凯利 = min(p − (1−p)/b, 0.25) × 0.5，负值归零。

    p = 胜率(0–1)，b = 赔率（盈亏比，>0）。
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError("胜率 p 应在 0–1")
    if b <= 0:
        raise ValueError("赔率 b 必须为正")
    raw = p - (1.0 - p) / b
    return round(max(0.0, min(raw, KELLY_CAP)) * KELLY_HAIRCUT, 6)


# ------------------------------------------------------------------ 熔断
@dataclass
class CircuitState:
    drawdown: float
    action: str
    note: str


def circuit_breaker(drawdown: float) -> CircuitState:
    """回撤熔断：>=25% 停机；>=15% 减仓；否则正常。

    drawdown 传正数（例如 0.18 表示回撤 18%）。
    """
    d = abs(drawdown)
    if d >= CIRCUIT_HALT:
        return CircuitState(d, "HALT", f"回撤 {d:.1%} ≥ {CIRCUIT_HALT:.0%} → 停机，停止一切开仓并复盘")
    if d >= CIRCUIT_REDUCE:
        return CircuitState(d, "REDUCE", f"回撤 {d:.1%} ≥ {CIRCUIT_REDUCE:.0%} → 减仓至 α 预算的 50%")
    return CircuitState(d, "NORMAL", f"回撤 {d:.1%} 未触发熔断")


# ------------------------------------------------------------------ 冰点判定
def is_ice_point(limit_up_count: int, broken_rate: float, index_pct: float) -> bool:
    """冰点：涨停家数少 + 炸板率高 + 指数下跌，三者同时成立。

    阈值：涨停 < 40 家 且 炸板率 > 40% 且 指数跌幅 > 1%。
    """
    return limit_up_count < 40 and broken_rate > 0.40 and index_pct < -1.0


def target_band() -> tuple[float, float]:
    """考核带：年化 12%–25%。"""
    return TARGET_ANNUAL_LOW, TARGET_ANNUAL_HIGH


def within_target(annual_return: float) -> bool:
    lo, hi = target_band()
    return lo <= annual_return <= hi


def summarize(iterable: Iterable[ScoreBreakdown]) -> dict[str, float]:
    """对一组评分做汇总，供报告用。"""
    items = list(iterable)
    if not items:
        return {"count": 0, "avg": 0.0, "max": 0.0, "min": 0.0}
    totals = [i.total for i in items]
    return {
        "count": float(len(items)),
        "avg": round(sum(totals) / len(totals), 3),
        "max": round(max(totals), 3),
        "min": round(min(totals), 3),
    }
