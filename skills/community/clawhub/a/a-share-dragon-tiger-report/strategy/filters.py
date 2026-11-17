#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""硬闸门：ST / 停牌 / 高度 / 板块 / 业绩 / 可交易性。

设计原则：闸门**只做否决，不做打分**。所有否决都必须给出可复核的理由字符串，
以便报告逐条列示「谁被拦、为什么被拦」。凡口径来自 `calibers.py` 的，
一律不在此处硬编码。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from . import calibers as C


@dataclass
class GateResult:
    """单只标的的闸门判定结果。"""
    code: str
    name: str = ""
    passed: bool = True
    layer: str = "L2"
    reasons: list[str] = field(default_factory=list)
    score_bonus: float = 0.0
    score_penalty: float = 0.0
    warnings: list[str] = field(default_factory=list)

    def reject(self, layer: str, reason: str) -> "GateResult":
        self.passed = False
        self.layer = layer
        self.reasons.append(reason)
        return self


# ------------------------------------------------------------------ L1 行业层
def gate_industry(
    name: str,
    rank: float | None,
    vr: float | None,
    is_chain: bool | None = None,
) -> GateResult:
    """L1 行业闸门：3 年月线收盘**历史分位**为主要判据，放量为辅助。

    rank = count(closes < current) / n   （主判据，越低越「超低位」）
    vr   = 近 3 个完整月成交额均值 / 前 12 个完整月成交额均值（额比）

    口径⑤：「链」形态主题跳过 L1 否决权，只做定性描述。
    """
    chain = C.is_chain_theme(name) if is_chain is None else is_chain
    r = GateResult(code=name, name=name, layer="L1")

    if rank is None or vr is None:
        r.warnings.append(f"{name}：分位或额比缺失，L1 无法判定，转定性描述")
        return r

    low_rank = rank <= C.RANK_LOW_THRESHOLD
    expanded = vr >= C.VR_THRESHOLD

    if low_rank and expanded:
        return r
    if low_rank and not expanded:
        r.warnings.append(f"{name}：分位 {rank:.1f}% 超低但额比 {vr:.2f}× 未放量")
    if not low_rank and expanded:
        r.warnings.append(f"{name}：分位 {rank:.1f}% 偏高但额比 {vr:.2f}× 放量（可能是高位放量）")

    if chain and C.CHAIN_THEME_SKIPS_L1_VETO:
        r.warnings.append(f"{name}：属「链」形态主题，按口径⑤跳过 L1 否决权（仅定性）")
        return r

    return r.reject(
        "L1",
        f"行业不满足「低位 + 放量」：分位 {rank:.1f}%（阈值 ≤{C.RANK_LOW_THRESHOLD:.0f}%）、"
        f"额比 {vr:.2f}×（阈值 ≥{C.VR_THRESHOLD}）",
    )


# ------------------------------------------------------------------ L2.5 可交易性
def gate_tradability(row: Mapping[str, Any]) -> GateResult:
    """L2.5 基础可交易性校验（口径⑥）。

    独立层，位于 L2 与 L3 之间。命中任一 NOTRADE_RULES 即剔除，
    且**不计入** L3 一票否决统计 —— 二者必须分开报告，
    否则会把「不可交易」误报成「基本面不通过」。
    """
    code = str(row.get("code", ""))
    name = str(row.get("name", ""))
    r = GateResult(code=code, name=name, layer=C.TRADABILITY_LAYER)

    if row.get("delisted"):
        return r.reject(C.TRADABILITY_LAYER, f"{name} 已退市 / 处退市整理期")
    if row.get("suspended"):
        return r.reject(C.TRADABILITY_LAYER, f"{name} 停牌")
    if row.get("is_st"):
        return r.reject(C.TRADABILITY_LAYER, f"{name} 为 ST / *ST")

    pb = row.get("pb")
    if pb is not None and float(pb) < 0:
        return r.reject(C.TRADABILITY_LAYER, f"{name} 净资产为负（PB {float(pb):.2f}）")

    listed_days = row.get("listed_days")
    if listed_days is not None and int(listed_days) < 60:
        return r.reject(C.TRADABILITY_LAYER, f"{name} 上市未满 60 个交易日（{listed_days} 日）")

    turnover = row.get("avg_turnover_20d")
    if turnover is not None and float(turnover) < 3_000_000:
        return r.reject(
            C.TRADABILITY_LAYER,
            f"{name} 近 20 日均成交额 {float(turnover)/1e4:.0f} 万元 < 3000 万元，流动性不足",
        )

    price = row.get("price")
    if price is not None and float(price) < 1.0:
        r.warnings.append(f"{name} 股价 {float(price):.2f} 元，接近面值退市红线")

    return r


# ------------------------------------------------------------------ L3 基本面
def gate_fundamental(row: Mapping[str, Any]) -> GateResult:
    """L3 基本面闸门（口径 ①③④ 全部在此生效）。

    关键字段（对齐 westock `data_finance` 的实际字段名，勿用近义字段）：
      * 营收同比      → TORGrowRate            （不是 OperatingRevenueYOY）
      * 归母同比      → NPParentCompanyYOY
      * 归母同比(单季) → NPParentCompanyYOY_Q
      * 扣非归母      → NPDeductNonRecurringPL
    """
    code = str(row.get("code", ""))
    name = str(row.get("name", ""))
    r = GateResult(code=code, name=name, layer="L3")

    # ---- 口径④：连续两年年报亏损 = 一票否决；单年亏损 = 减分
    losses = row.get("annual_loss_years") or []          # 例 [2024, 2025]
    losses = [int(y) for y in losses]
    consecutive = _max_consecutive(losses)
    if C.TWO_CONSECUTIVE_LOSSES_IS_VETO and consecutive >= 2:
        return r.reject("L3", f"{name} 连续 {consecutive} 个年报亏损（{[*losses]}）→ 一票否决")
    if losses and not C.SINGLE_YEAR_LOSS_IS_VETO:
        r.score_penalty += C.SINGLE_YEAR_LOSS_SCORE
        r.warnings.append(
            f"{name} 存在单年亏损（{losses}）→ 按口径④计为减分项 −{C.SINGLE_YEAR_LOSS_SCORE:.0f} 分，不否决"
        )

    # ---- 口径③：增速红线（半年口径）
    interim_yoy = row.get("interim_yoy")            # 最新中报年内同比，如 0.003 = +0.3%
    prior_fy_yoy = row.get("prior_fy_yoy")          # 上一年度年报同比

    if interim_yoy is None:
        # ⚠️ 契约第七章「一票否决清单」第 3 条：**关键数据缺失无法验证 → 否决**。
        #    此处曾只 append 一条 warning 就放行，等于让「取不到中报同比」的标的
        #    自动通过增速红线（2026-09-16 实测：龙源电力 / 浙江新能 / 华电国际
        #    三只因此混进过会名单，把过会数从 26 抬到 29）。
        #    增速红线是硬判据，判据缺料就不能判「通过」—— 与注释「不得默认通过」对齐。
        return r.reject(
            "L3",
            f"{name}：中报同比缺失，增速红线无法判定（关键数据缺失无法验证）→ 一票否决",
        )
    else:
        interim_yoy = float(interim_yoy)
        if interim_yoy <= C.GROWTH_HARD_LINE:
            return r.reject(
                "L3",
                f"{name} 中报归母同比 {interim_yoy:+.2%} ≤ {C.GROWTH_HARD_LINE:.0%} 转负 → 触发增速硬线",
            )
        if prior_fy_yoy is not None:
            prior_fy_yoy = float(prior_fy_yoy)
            rel = C.GROWTH_PENALTY_RELATIVE_LINE
            if prior_fy_yoy > 0 and interim_yoy < rel * prior_fy_yoy:
                r.score_penalty += C.GROWTH_PENALTY_SCORE
                r.warnings.append(
                    f"{name} 中报 {interim_yoy:+.2%} 仅为上一年度 {prior_fy_yoy:+.2%} 的 "
                    f"{interim_yoy/prior_fy_yoy:.1%}（< {rel:.0%}）→ 重大减分项 −{C.GROWTH_PENALTY_SCORE:.0f} 分"
                )

    # ---- 口径①：国企央企背景 = 偏好项，不是门槛
    soe = bool(row.get("soe_background"))
    if soe:
        r.score_bonus += C.SOE_SCORE_BONUS
        r.warnings.append(f"{name} 控股股东/实控人为国企央企背景 → 按口径①计为偏好加分 +{C.SOE_SCORE_BONUS:.0f} 分")

    # ---- 口径②：新兴科技成长优先
    if row.get("emerging_tech"):
        r.score_bonus += C.EMERGING_TECH_BONUS
        r.warnings.append(f"{name} 属新兴产业/科技成长 → 按口径②加分 +{C.EMERGING_TECH_BONUS:.0f} 分")

    # ---- 筹码集中度（十大流通股东占比越高越集中）
    top10 = row.get("top10_float_ratio")
    holders = row.get("holder_count")
    if top10 is not None and float(top10) < 0.30:
        r.warnings.append(f"{name} 十大流通股东占比 {float(top10):.1%} 偏低，筹码较分散")
    if top10 is not None and holders:
        r.warnings.append(
            f"{name} 十大流通占比 {float(top10):.1%} / 股东户数 {int(holders):,}（二者应成反比）"
        )

    # ---- 利润含金量与造假红旗（v2.3 知识蒸馏升级，源：穿透财报/简明财务/穿透叙事）
    # 既有字段即可判定：归母正而扣非负 → 罚分（不否决，口径④精神）；
    # 扣非/归母 <50% → 标记「增速判定应切扣非口径」。
    # 可选扩展字段（净现比/销售收现率/应收存货背离/商誉/少数股东扛亏等）补采后自动生效。
    from . import knowledge as KN
    pq = KN.profit_quality(row)
    if KN.K["扣非为负罚分"] and any("扣非" in p and "为负" in p for p in pq.penalties):
        r.score_penalty += KN.K["扣非为负罚分"]
    r.warnings.extend(pq.penalties)
    r.warnings.extend(pq.notes)
    if pq.red_flags:
        r.warnings.append(f"{name} 利润质量强红旗 {len(pq.red_flags)} 条：{'；'.join(pq.red_flags)}")
    if pq.veto_suggest:
        # ≥2 条强红旗（科目接力嫌疑）→ 一票否决级人工复核
        r.reject("L3", f"{name} 造假红旗 {len(pq.red_flags)} 条（科目接力嫌疑）→ 一票否决级人工复核")
        return r

    return r


# ------------------------------------------------------------------ 组合闸门
def apply_gates(row: Mapping[str, Any]) -> GateResult:
    """按 L2.5 → L3 顺序依次过闸，返回第一个否决结果（短路）。"""
    t = gate_tradability(row)
    if not t.passed:
        return t
    f = gate_fundamental(row)
    f.score_bonus += t.score_bonus
    f.score_penalty += t.score_penalty
    f.warnings = t.warnings + f.warnings
    return f


def gate_batch(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """批量过闸并分类统计（不可交易 / 基本面否决 / 通过），供报告直接渲染。"""
    notrade, vetoed, passed = [], [], []
    for row in rows:
        g = apply_gates(row)
        if not g.passed:
            (notrade if g.layer == C.TRADABILITY_LAYER else vetoed).append(g)
        else:
            passed.append(g)
    return {
        "notrade": notrade,
        "vetoed": vetoed,
        "passed": passed,
        "summary": {
            "total": len(rows),
            "notrade": len(notrade),
            "vetoed": len(vetoed),
            "passed": len(passed),
            "reject_rate": round(
                (len(notrade) + len(vetoed)) / len(rows), 4
            ) if rows else 0.0,
        },
    }


def _max_consecutive(years: Sequence[int]) -> int:
    """求连续年份的最大长度，如 [2023, 2024, 2026] → 2。"""
    if not years:
        return 0
    ys = sorted(set(int(y) for y in years))
    best = run = 1
    for prev, cur in zip(ys, ys[1:]):
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    return best
