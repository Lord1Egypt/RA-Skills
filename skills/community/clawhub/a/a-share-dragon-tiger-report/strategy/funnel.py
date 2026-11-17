#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四层漏斗：L1 行业 → L2 个股 → L2.5 可交易性 → L3 基本面。

这是与纯评分管道（pipeline.py）并列的**核验型**入口：先自上而下筛行业，
再在同一行业内筛个股，最后过可交易性与基本面。口径全部取自 calibers.py。

两层数据结构必须严格区分（这是最容易踩的坑）：
  * 历史分位 / 区间位置 / 上中下四分之一阈值 —— **保留**当月的未完结月线
  * 额比（成交额比）—— **剔除**当月，只算已完结月
两者若混用，报告之间将不可比。
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from . import calibers as C
from . import filters as FLT


# ------------------------------------------------------------------ 月线工具
def rank_percentile(closes: Sequence[float], current: float | None = None) -> float:
    """历史分位 = count(收盘 < 当前) / n，返回 0–100。

    主判据。比区间位置稳健：不受单一极值影响。
    """
    if not closes:
        raise ValueError("closes 不能为空")
    cur = float(closes[-1] if current is None else current)
    n = len(closes)
    below = sum(1 for c in closes if float(c) < cur)
    return round(100.0 * below / n, 2)


def interval_position(closes: Sequence[float], current: float | None = None) -> float:
    """区间位置 = (cur − min) / (max − min)，返回 0–1。"""
    if not closes:
        raise ValueError("closes 不能为空")
    lo, hi = min(closes), max(closes)
    cur = float(closes[-1] if current is None else current)
    if hi == lo:
        return 0.5
    return round((cur - lo) / (hi - lo), 4)


def lower_quarter_threshold(closes: Sequence[float]) -> float:
    """下 1/4 阈值 = min + 0.25 × (max − min)。"""
    lo, hi = min(closes), max(closes)
    return round(lo + 0.25 * (hi - lo), 4)


def downside_to_lower_quarter(closes: Sequence[float], current: float | None = None) -> float:
    """还需跌% = (下1/4阈值 / 现价 − 1) × 100。负值表示「现价已在下 1/4 区间内」。"""
    cur = float(closes[-1] if current is None else current)
    th = lower_quarter_threshold(closes)
    if cur <= 0:
        raise ValueError("现价必须为正")
    return round((th / cur - 1.0) * 100.0, 2)


def amount_ratio(amounts: Sequence[float]) -> float:
    """额比 = 近 3 个**已完结**月成交额均值 / 前 12 个已完结月均值。

    调用方必须自行剔除未完结的当月（传进来的序列应是已完结月）。
    必须用 amount（成交额），**不能用 volume（成交量）** —— 成交量不含量价修正。
    """
    a = [float(x) for x in amounts]
    if len(a) < 15:
        raise ValueError(f"额比需要至少 15 个已完结月，实际 {len(a)}")
    recent = a[-3:]
    prior = a[-15:-3]
    base = statistics.fmean(prior)
    if base <= 0:
        raise ValueError("基准期均值为 0，无法计算额比")
    return round(statistics.fmean(recent) / base, 4)


# ------------------------------------------------------------------ 数据类
@dataclass
class Industry:
    code: str
    name: str
    rank: float
    vr: float
    dispersion: float = 0.0
    note: str = ""


@dataclass
class Stock:
    code: str
    name: str
    industry: str = ""
    rank: float | None = None
    vr: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def merged(self) -> dict[str, Any]:
        """把技术面字段并入原始财务字段，供 filters 使用。"""
        d = dict(self.raw)
        d.setdefault("code", self.code)
        d.setdefault("name", self.name)
        if self.rank is not None:
            d.setdefault("rank", self.rank)
        if self.vr is not None:
            d.setdefault("vr", self.vr)
        return d


@dataclass
class FunnelResult:
    industries: list[Industry]
    l2_pass: list[Stock]
    l2_5_removed: list[FLT.GateResult]
    l3_pass: list[Stock]
    l3_vetoed: list[FLT.GateResult]
    sensitivity: dict[str, Any] = field(default_factory=dict)

    @property
    def final(self) -> list[Stock]:
        return self.l3_pass


# ------------------------------------------------------------------ 执行
def run_funnel(
    industries: Iterable[Industry],
    stocks: Iterable[Stock],
    *,
    strict_growth: bool = False,
) -> FunnelResult:
    """执行四层漏斗。

    strict_growth=True 时把「增速大幅下滑」的判定收紧为「任何减速即排除」，
    用于跑敏感度对照（框架默认 False = 50% 相对线）。
    """
    inds = list(industries)
    stks = list(stocks)

    # ---- L1：行业入池
    # ⚠️ 口径分工（v2 契约）：**L1 只判「位置」** —— 3 年分位 ≤ 25%；额比 ≥ 1.0× 是 **L2 个股层**
    #    的必要条件，不在 L1 重复设卡。
    #    曾在此处叠加行业级额比闸门（用 FLT.gate_industry 的双条件），导致「行业额比不足、
    #    但个股已放量」的机会被整体误杀：2026-09-16 实测 6 个分位 ≤25% 的行业中仅食品饮料
    #    额比达标，L2 池因此从 50 只塌缩到 21 只，与同日 classic 管线（56 只）分叉 ——
    #    而两套样式应当「共用同一套漏斗、结论必然一致」。
    li_pool: set[str] = {ind.name for ind in inds
                         if ind.rank is not None and ind.rank <= C.RANK_LOW_THRESHOLD}

    # ---- L2：个股低位+放量
    l2_pass: list[Stock] = []
    for s in stks:
        if li_pool and s.industry not in li_pool:
            # 口径⑤：链形态主题跳过 L1 否决，其个股仍可进入 L2
            if not (C.CHAIN_THEME_SKIPS_L1_VETO and C.is_chain_theme(s.industry)):
                continue
        if s.rank is None or s.vr is None:
            continue
        if s.rank <= C.RANK_LOW_THRESHOLD and s.vr >= C.VR_THRESHOLD:
            l2_pass.append(s)

    # ---- L2.5 + L3
    l2_5_removed: list[FLT.GateResult] = []
    l3_pass: list[Stock] = []
    l3_vetoed: list[FLT.GateResult] = []
    passed_codes: list[str] = []

    for s in l2_pass:
        t = FLT.gate_tradability(s.merged)
        if not t.passed:
            l2_5_removed.append(t)
            continue
        f = FLT.gate_fundamental(s.merged)
        if not f.passed:
            l3_vetoed.append(f)
            continue
        if strict_growth and _decelerating(s.merged):
            g = FLT.GateResult(code=s.code, name=s.name, layer="L3")
            g.reject("L3", f"{s.name} 增速减速（严格口径）→ 排除")
            l3_vetoed.append(g)
            continue
        l3_pass.append(s)
        passed_codes.append(s.code)

    sens = {
        "rule_50pct_relative": len(passed_codes),
        "rule_any_deceleration": _sensitivity_strict_count(l2_pass),
        "note": "口径③收紧会改变过会数量，报告必须写明该 ±N 只敏感度",
    }

    return FunnelResult(
        industries=inds,
        l2_pass=l2_pass,
        l2_5_removed=l2_5_removed,
        l3_pass=l3_pass,
        l3_vetoed=l3_vetoed,
        sensitivity=sens,
    )


def _decelerating(row: Mapping[str, Any]) -> bool:
    """严格口径：中报同比低于上一年度同比即算减速。"""
    a, b = row.get("interim_yoy"), row.get("prior_fy_yoy")
    if a is None or b is None:
        return False
    return float(a) < float(b)


def _sensitivity_strict_count(stocks: Sequence[Stock]) -> int:
    """跑一遍「任何减速即排除」的严格口径，返回过会数。"""
    n = 0
    for s in stocks:
        row = s.merged
        if not FLT.gate_tradability(row).passed:
            continue
        if not FLT.gate_fundamental(row).passed:
            continue
        if _decelerating(row):
            continue
        n += 1
    return n


def dispersion(stock_ranks: Sequence[float]) -> float:
    """个股分位离散度 = max − min（pp）。>=60pp 视为方向内部严重分化。"""
    if len(stock_ranks) < 2:
        return 0.0
    return round(max(stock_ranks) - min(stock_ranks), 2)


def dispersion_alert(value: float) -> str:
    if value >= C.DISPERSION_ALERT:
        return f"内部严重分化（{value:.1f}pp ≥ {C.DISPERSION_ALERT:.0f}pp）—— 「方向正确≠个股正确」"
    return f"内部分化可控（{value:.1f}pp）"


def render_funnel_summary(fr: FunnelResult) -> str:
    """生成一段纯文本漏斗摘要，脚本与报告都可直接引用。"""
    lines = [
        f"口径版本 {C.CALIBER_VERSION} · 四层漏斗",
        f"  L1 行业入池      ：{len(fr.industries)} 个扫描",
        f"  L2 个股入池      ：{len(fr.l2_pass)} 只",
        f"  L2.5 可交易性剔除 ：{len(fr.l2_5_removed)} 只",
        f"  L3 基本面否决    ：{len(fr.l3_vetoed)} 只",
        f"  最终通过         ：{len(fr.l3_pass)} 只 "
        f"（{', '.join(s.name for s in fr.l3_pass) or '无'}）",
        f"  敏感度           ：50% 相对线 → {fr.sensitivity['rule_50pct_relative']} 只；"
        f"任何减速即排除 → {fr.sensitivity['rule_any_deceleration']} 只",
    ]
    return "\n".join(lines)
