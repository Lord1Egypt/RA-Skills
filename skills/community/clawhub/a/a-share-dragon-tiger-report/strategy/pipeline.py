#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管道：候选 → 过闸 → 评分 → 风控信号表。

产出的 `SignalRow` 列表就是报告 §14 / §16+ 的表格数据源。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from . import calibers as C
from . import filters as FLT
from . import formulas as F
from . import risk as RK


@dataclass
class SignalRow:
    code: str
    name: str
    sector: str
    score: float
    action: str                 # BUY / WATCH / AVOID
    layer: str = "L3"
    blocked_by: str = ""        # 被哪一层拦下
    reasons: list[str] = field(default_factory=list)
    shares: int = 0
    notional: float = 0.0
    notes: list[str] = field(default_factory=list)


ACTION_BUY = "BUY"
ACTION_WATCH = "WATCH"
ACTION_AVOID = "AVOID"

# 评分 → 动作 的分界
BUY_THRESHOLD = 70.0
WATCH_THRESHOLD = 55.0


def score_row(row: Mapping[str, Any]) -> F.ScoreBreakdown:
    """对单只标的打分。

    技术/资金/周期/位置四项若缺失，按「不给分」处理并记 note，
    **不做均值替代** —— 均值替代会系统性高估数据缺失的标的。
    """
    bd = F.composite_score(
        tech=float(row.get("tech", 0.0) or 0.0),
        flow=float(row.get("flow", 0.0) or 0.0),
        fund=float(row.get("fund", 0.0) or 0.0),
        cycle=float(row.get("cycle", 0.0) or 0.0),
        fib=float(row.get("fib", 0.0) or 0.0),
        bonus=float(row.get("bonus", 0.0) or 0.0),
        penalty=float(row.get("penalty", 0.0) or 0.0),
    )
    missing = [k for k in ("tech", "flow", "fund", "cycle", "fib")
               if row.get(k) is None]
    if missing:
        bd.notes.append("缺项未计分：" + "、".join(missing))
    return bd


def run_pipeline(
    candidates: Sequence[Mapping[str, Any]],
    equity: float = 1_000_000.0,
    stage: str = "II",
    ice_point: bool = False,
) -> dict[str, Any]:
    """主管道。返回 {"rows": [...], "ledger": {...}, "stats": {...}}。"""
    ledger = RK.AlphaLedger(equity=equity, stage=stage, ice_point=ice_point)
    rows: list[SignalRow] = []

    # 先过闸，再按分数从高到低排序分配仓位 —— 顺序影响谁能拿到 α 额度
    gated: list[tuple[Mapping[str, Any], FLT.GateResult]] = []
    for cand in candidates:
        gated.append((cand, FLT.apply_gates(cand)))

    scored = []
    for cand, g in gated:
        bd = score_row(cand)
        scored.append((cand, g, bd))
    scored.sort(key=lambda t: t[2].total, reverse=True)

    for cand, g, bd in scored:
        code = str(cand.get("code", ""))
        name = str(cand.get("name", ""))
        sector = str(cand.get("sector", ""))

        if not g.passed:
            rows.append(SignalRow(
                code=code, name=name, sector=sector, score=bd.total,
                action=ACTION_AVOID, layer=g.layer,
                blocked_by=f"{g.layer}：{g.reasons[0] if g.reasons else '未说明'}",
                reasons=list(g.reasons), notes=list(g.warnings),
            ))
            continue

        # 合并口径加分/减分
        total = round(max(0.0, min(100.0, bd.total + g.score_bonus - g.score_penalty)), 3)
        if total >= BUY_THRESHOLD:
            action = ACTION_BUY
        elif total >= WATCH_THRESHOLD:
            action = ACTION_WATCH
        else:
            action = ACTION_WATCH if total > 0 else ACTION_AVOID

        shares = notional = 0
        notes = list(bd.notes) + list(g.warnings)
        if action == ACTION_BUY:
            sized = RK.suggested_size({**cand, "sector": sector}, ledger)
            shares, notional = sized["shares"], sized["notional"]
            if sized["allowed"] and shares > 0:
                ledger.add(RK.Position(
                    code=code, name=name, shares=shares,
                    entry=float(cand["entry"]), stop=float(cand["stop"]), sector=sector,
                ))
            else:
                action = ACTION_WATCH
                notes.append(f"仓位受限 → 降级为 WATCH：{sized['note']}")

        rows.append(SignalRow(
            code=code, name=name, sector=sector, score=total, action=action,
            shares=shares, notional=notional, notes=notes,
        ))

    stats = {
        "total": len(rows),
        "buy": sum(1 for r in rows if r.action == ACTION_BUY),
        "watch": sum(1 for r in rows if r.action == ACTION_WATCH),
        "avoid": sum(1 for r in rows if r.action == ACTION_AVOID),
        "rejected_by_L2_5": sum(1 for r in rows if r.blocked_by.startswith(C.TRADABILITY_LAYER)),
        "rejected_by_L3": sum(1 for r in rows if r.blocked_by.startswith("L3")),
    }
    return {
        "caliber": C.CALIBER_VERSION,
        "rows": rows,
        "ledger": ledger.snapshot(),
        "stats": stats,
    }


def render_signal_table(result: Mapping[str, Any]) -> str:
    """把管道结果渲染为 Markdown 表，可直接贴进报告 §14。"""
    rows: Iterable[SignalRow] = result["rows"]  # type: ignore[assignment]
    head = "| 代码 | 名称 | 板块 | 综合分 | 动作 | 股数 | 名义 | 拦截面 | 说明 |\n"
    head += "|---|---|---|---:|---|---:|---:|---|---|\n"
    body = []
    for r in rows:
        note = r.blocked_by or ("；".join(r.notes) if r.notes else "—")
        body.append(
            f"| {r.code} | {r.name} | {r.sector} | {r.score:.1f} | {r.action} | "
            f"{r.shares or '—'} | {r.notional or '—'} | {r.layer if not r.blocked_by else r.blocked_by.split('：')[0]} | {note} |"
        )
    led = result["ledger"]
    tail = (
        f"\n**α 账本**：阶段 {led['stage']}｜上限 {led['alpha_budget']:.0%}｜"
        f"已用 {led['used_pct']:.2%}｜剩余 {led['remaining']:,.0f} 元｜"
        f"持仓 {led['positions']} 笔｜合计风险 {led['total_risk']:,.0f} 元\n"
    )
    return head + "\n".join(body) + "\n" + tail
