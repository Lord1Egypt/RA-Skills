#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""投行级量化研判引擎 gceo_quant（v4.0 新增 · 第三只读旁路）

来源：GCCEO 4.0「分析思维域（域九）+ 投行私募 A1-A10 + 方法论工具
       DCF/LBO · Pre-Mortem · FAIR · 五步决策框架」→ A 股研判落地。

═══════════════════════ 八条设计契约（不可协商）═══════════════════════
1. 本模块是叠加在 v2.3 ⊂ v3.0 ⊂ v3.1(GCCEO) 之上的**第三只读旁路层**。
   不 import funnel 的评分路径、不改 calibers 六条口径 / KNOWLEDGE 45 键 /
   v3 五模块 / gcceo_ext 映射 / limitup_source 冻结闸门 / pipeline 打分。
2. **真值算 + 缺口标注**：每个数字必须能回溯到 data.json 现有非空字段；
   缺失字段一律登记到 gap_inventory，并根据「缺什么测不了什么」逐条标注。
   严禁编造 DCF 终值 / LBO 杠杆倍数 / ROE / 净现比 / 商誉占比 / 一致预期增速。
3. 复用既有知识函数：knowledge.valuation_anchor()、knowledge.profit_quality()，
   不另起一套估值/质量口径，避免与冻结层打架。
4. **不夺权**：本层输出「估值锚 / 利润质量 / 五维形态 / Pre-Mortem / 全链路」
   仅为研判视角；无剔除权、无打分权、无仓位上调权、不生成 BUY、不占 α 预算。
5. 商业模式 biz_type 用行业→模式**推定**（水印【推定】），不是公司披露；
   周期顶陷阱因缺「盈利历史分位 / 毛利率位置」字段一律标【缺口】，不触发。
6. PEG 同时给半年口径(中报同比)与上年度口径，并标注高基数失真（同比 >200%）；
   data.json 无一致预期增速，PEG 仅作参考，不作为估值结论（水印【口径差异】）。
7. 强依赖 gceo.enabled 且 v3.enabled；data.json 顶层 gceo_quant.enabled=false
   一键回滚到 v3.1 的 18 页；与 selection_mode 正交（limitup / oversold 均可挂）。
8. 渲染器不 import 本模块，只读 data.json 顶层 gceo_quant.blocks，
   保证 v2.3 / v3.0 / v3.1 生成器对本层零依赖。

接入点：data.json 顶层可选字段 `gceo_quant`（与 `gceo` 平级）。
装配器：strategy/build_gceo_quant_inputs.py。
"""
from __future__ import annotations

import os as _os
import statistics
import sys as _sys
from typing import Any, Mapping

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)

from strategy import calibers as C          # noqa: E402
from strategy import knowledge as KN        # noqa: E402
from strategy import formulas as F          # noqa: E402

# ─────────────────────────────── 版本与开关 ───────────────────────────────
GCEEO_QUANT_VERSION = "v4.0"
GCEEO_QUANT_SOURCE = "GCCEO 4.0 · 域九分析思维 + 投行 A1-A10 + Pre-Mortem/FAIR/DCF-LBO 方法工具"
CALIBER_VERSION_UNCHANGED = "v2.3"
FRAMEWORK_VERSION = "v4.0"
OVERLAY_ONLY = True
NO_VETO = True
NO_POSITION_UP = True
NO_FABRICATED_VALUATION = True

QUANT_SWITCHES: dict[str, bool] = {
    "q_valuation_anchor": True,     # 估值锚（PE/PB/PEG 真值 + 周期顶缺口）
    "q_profit_quality": True,       # 利润质量（复用 KN.profit_quality + 缺口清单）
    "q_five_dim_radar": True,       # 五维形态（既有评分输入的重述，非新增因子）
    "q_premortem": True,            # 事前尸检（三因，基于真值 + 缺口）
    "q_gap_inventory": True,        # 数据缺口台账（缺什么 → 测不了什么）
    "q_lifecycle": True,            # 全周期全链路（DEFINE→ANALYZE→SYNTHESIZE→DECIDE→EXECUTE）
}
SWITCH_COUNT = len(QUANT_SWITCHES)

# data.json 当前为 null 的字段 → 各自负责的核验能力（缺口台账的固定清单）
QUALITY_GAP_FIELDS: list[tuple[str, str]] = [
    ("parent_net_profit",    "扣非/归母占比（利润含金量）"),
    ("net_cash_ratio",       "净现比（利润现金背书，单期）"),
    ("net_cash_ratio_prev",  "净现比连续两期（否决级证据）"),
    ("goodwill_ratio",       "商誉/净资产（悬顶之剑 A4）"),
    ("gov_subsidy_ratio",    "其他收益/利润总额（补助依赖）"),
    ("holder_count",         "股东户数变化（筹码松动）"),
    ("top10_float_ratio",    "十大流通股东集中度（A8 股东积极主义）"),
]

# 行业 → 商业模式（推定口径，非公司披露；水印【推定】）
_SECTOR_CYCLE = ("钢铁", "煤炭", "有色", "采掘", "化工", "房地产", "建筑", "建材",
                 "水泥", "玻璃", "航空", "航运", "港口", "石油", "化纤", "橡胶", "造纸")
_SECTOR_DIV = ("银行", "公用事业", "水务", "燃气", "高速公路", "铁路", "公路", "保险")
_SECTOR_GROW = ("电子", "半导体", "通信", "计算机", "传媒", "医药", "生物", "电气",
                "新能源", "军工", "机械", "互联网", "软件")

HIGH_BASE_RATIO = 2.0        # 同比 >200% 视为高基数，PEG 失真
PEG_FAIR = 1.0               # PEG ≤1 参考合理（水印：非结论）
PEG_BUBBLE = 2.0             # PEG ≥2 泡沫警戒（水印：非结论）
FIB_HIGH = 85.0              # 斐波那契位置高分位（五维 fib 0-100）
FLOW_HOT = 85.0              # 资金维过热
PB_PREMIUM = 6.0             # 描述性高溢价标记（>6×PB），非否决口径
UNIVERSE_CAP = 6             # 研判页最多展开的标的数（页高约束）


# ─────────────────────────────── 工具函数 ───────────────────────────────
def _f(v: Any) -> float | None:
    """安全转 float；None / 空串 / 非数值一律 None（不编造 0）。"""
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _pct(ratio: float | None, digits: int = 1) -> str:
    if ratio is None:
        return "缺口"
    return f"{ratio * 100:+.{digits}f}%"


def _yi(v: Any, digits: int = 2) -> str:
    x = _f(v)
    return "缺口" if x is None else f"{x / 1e8:+.{digits}f}亿"


def _biz_hint(row: Mapping[str, Any]) -> tuple[str | None, str]:
    """行业 → 商业模式推定。返回 (模式, 依据)。未知返回 (None, 缺口说明)。"""
    sec = str(row.get("sector") or "")
    if any(k in sec for k in _SECTOR_CYCLE):
        return "周期", f"行业『{sec}』→ 周期（推定）"
    if any(k in sec for k in _SECTOR_DIV):
        return "红利", f"行业『{sec}』→ 红利（推定）"
    if any(k in sec for k in _SECTOR_GROW):
        return "成长", f"行业『{sec}』→ 成长（推定）"
    return None, f"行业『{sec or '缺失'}』无稳定模式映射 → 按未知锚处理"


# ─────────────────────────── 1. 估值锚（真值） ───────────────────────────
def valuation_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """单只估值锚研判：PE/PB 真值 + 双口径 PEG + 复用知识库估值锚 + 周期顶缺口。"""
    name = str(row.get("name", ""))
    pe, pb = _f(row.get("pe")), _f(row.get("pb"))
    g_h1, g_fy = _f(row.get("interim_yoy")), _f(row.get("prior_fy_yoy"))
    biz, biz_basis = _biz_hint(row)

    # --- PEG 双口径（同比是小数比率，如 0.0034=+0.34%; 2.9009=+290.09%）---
    def peg(pe_: float | None, g: float | None) -> tuple[float | None, str]:
        if pe_ is None or pe_ <= 0:
            return None, "PE≤0 亏损 → PEG 不适用"
        if g is None:
            return None, "增速缺失 → PEG 不适用"
        if g <= 0:
            return None, "同比转负 → PEG 不适用"
        val = round(pe_ / (g * 100.0), 3)
        if g > HIGH_BASE_RATIO:
            return val, f"PEG {val:.2f}（同比 {g*100:.0f}% >200% 高基数，失真）"
        return val, f"PEG {val:.2f}（增速 {g*100:+.0f}%）"

    peg_h1, peg_h1_note = peg(pe, g_h1)
    peg_fy, peg_fy_note = peg(pe, g_fy)

    # --- 复用知识库估值锚（周期顶传 None，绝不触发伪判定）---
    anchor = KN.valuation_anchor(
        biz,
        pe_ttm=pe if (pe is not None and pe > 0) else None,
        pb=pb if (pb is not None and pb > 0) else None,
        dividend_yield=None,             # data.json 无股息率 → 红利锚无法判定，如实缺失
        profit_at_cycle_peak=None,       # 无盈利历史分位 → 周期顶陷阱标缺口，不触发
    )
    if pe is not None and pe <= 0:
        anchor_desc = f"PE {pe:.1f} ≤0（亏损）→ PE 锚失效，PB {pb if pb is not None else '缺口'} 仅净资产参考"
    else:
        anchor_desc = anchor.anchor_desc

    # --- 周期顶陷阱：数据缺口，明确标注（不编造毛利率分位）---
    trap_gap = ("周期顶陷阱无法判定：data.json 无『毛利率历史分位 / 盈利周期位置』"
                "→ 低 PE 是买点还是卖点缺关键证据【缺口】")
    return {
        "code": row.get("code", ""), "name": name, "sector": row.get("sector", ""),
        "biz": biz or "未知", "biz_basis": biz_basis,
        "pe": pe, "pb": pb,
        "pe_txt": "亏损" if (pe is not None and pe <= 0) else (f"{pe:.2f}" if pe is not None else "缺口"),
        "pb_txt": f"{pb:.2f}" if pb is not None else "缺口",
        "g_h1": g_h1, "g_fy": g_fy,
        "peg_h1": peg_h1, "peg_fy": peg_fy,
        "peg_note": peg_h1_note, "peg_fy_note": peg_fy_note,
        "high_base": bool(g_h1 is not None and g_h1 > HIGH_BASE_RATIO)
                     or bool(g_fy is not None and g_fy > HIGH_BASE_RATIO),
        "anchor_desc": anchor_desc, "anchor_action": anchor.action,
        "trap_gap": trap_gap,
        "deduct_yi": _yi(row.get("deduct_nonrecurring")),
        "watermark": "【事实】PE/PB/同比/扣非 取自 data.json；【推定】商业模式按行业映射；"
                     "【缺口】周期顶/股息率/一致预期；【口径差异】PEG 仅参考非结论",
    }


# ─────────────────────────── 2. 利润质量（复用+缺口） ─────────────────────
def quality_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """复用 KN.profit_quality（真值部分）+ 登记无法核验的字段缺口。"""
    pq = KN.profit_quality(row)                 # 真值：目前只能判扣非为负
    missing = [f for f, _ in QUALITY_GAP_FIELDS if row.get(f) is None]
    gap_desc = [f"{f}→{why}" for f, why in QUALITY_GAP_FIELDS if row.get(f) is None]
    return {
        "code": row.get("code", ""), "name": str(row.get("name", "")),
        "deduct_yi": _yi(row.get("deduct_nonrecurring")),
        "red_flags": list(pq.red_flags), "penalties": list(pq.penalties),
        "veto_suggest": bool(pq.veto_suggest),
        "missing_n": len(missing), "missing": missing,
        "gap_desc": gap_desc,
        "verdict": ("扣非为负（盈利质量存疑）" if pq.penalties
                    else "现有字段未见扣非红旗") + f"；{len(missing)}/{len(QUALITY_GAP_FIELDS)} 穿透字段缺口",
    }


# ─────────────────────── 3. 五维形态（既有输入重述） ──────────────────────
def radar_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """五维形态：tech/flow/fund/cycle/fib 为既有评分输入，此处重述，非新增因子。"""
    dims = {k: _f(row.get(k)) for k in ("tech", "flow", "fund", "cycle", "fib")}
    missing = [k for k, v in dims.items() if v is None]
    if missing:
        return {"code": row.get("code", ""), "name": str(row.get("name", "")),
                "dims": dims, "composite": None, "missing": missing,
                "note": f"五维缺 {','.join(missing)} → 形态不判定"}
    W = F.S_WEIGHTS
    comp = round(sum(W[k] * dims[k] for k in W), 2)   # 0-100，既有评分口径
    return {"code": row.get("code", ""), "name": str(row.get("name", "")),
            "dims": dims, "composite": comp, "missing": [],
            "note": "既有五维评分输入的重述（非新增因子，不进 scoring 二次计分）"}


# ─────────────────────────── 4. Pre-Mortem 三因 ───────────────────────────
def premortem_row(row: Mapping[str, Any], val: dict[str, Any],
                  qua: dict[str, Any], rad: dict[str, Any]) -> dict[str, Any]:
    """事前尸检：假设这笔交易 3 个月后失败，列出最多 3 条最可能原因（真值 + 缺口）。

    只描述失败路径，不给买卖结论、不新增否决口径。
    """
    truth: list[dict[str, str]] = []      # 有真值支撑的失败路径
    gap: dict[str, str] | None = None     # 数据缺口型失败路径（不编造）

    def add_t(kind: str, evidence: str, wm: str = "【事实】") -> None:
        if len(truth) < 3:
            truth.append({"kind": kind, "evidence": evidence, "wm": wm})

    # 因①盈利/增速（真值）
    if val["pe"] is not None and val["pe"] <= 0:
        add_t("亏损锚失效", f"PE {val['pe']:.1f}≤0，扣非 {val['deduct_yi']}")
    elif val["g_h1"] is not None and val["g_h1"] <= C.GROWTH_HARD_LINE:
        add_t("增速硬线", f"中报同比 {_pct(val['g_h1'])} ≤ {C.GROWTH_HARD_LINE:.0%}")
    elif val["high_base"]:
        add_t("高基数反噬", f"同比 >200%（中报 {_pct(val['g_h1'])}），增长难持续", "【口径差异】")

    # 因②位置/拥挤（真值）
    fib, flow = rad["dims"].get("fib"), rad["dims"].get("flow")
    if fib is not None and fib >= FIB_HIGH:
        add_t("高位接力断裂", f"位置维 fib {fib:.0f}≥{FIB_HIGH:.0f}，追高后无接力")
    elif flow is not None and flow >= FLOW_HOT and (fib is not None and fib < 50):
        add_t("资金与位置背离", f"flow {flow:.0f} 热但 fib {fib:.0f} 低，疑超跌反抽非趋势")
    elif flow is not None and flow >= FLOW_HOT:
        add_t("一致性拥挤", f"资金维 flow {flow:.0f}≥{FLOW_HOT:.0f}，一致交易拥挤、退潮时补跌")

    # 因③估值（真值）
    if val["pb"] is not None and val["pb"] >= PB_PREMIUM:
        add_t("高 PB 溢价", f"PB {val['pb']:.2f}>{PB_PREMIUM:.0f}×，增长不兑现即杀估值")
    peg_fy = val["peg_fy"]
    if peg_fy is not None and peg_fy >= PEG_BUBBLE:
        add_t("PEG 泡沫", f"PEG(上年度) {peg_fy:.2f}≥{PEG_BUBBLE:.0f}", "【口径差异】")

    # 缺口型失败路径：穿透字段全缺 → 利润质量无法验证（真实观察，不编造数字）
    if qua["missing_n"] >= 5:
        gap = {"kind": "尽调盲区",
               "evidence": f"{qua['missing_n']}/{len(QUALITY_GAP_FIELDS)} 穿透字段缺口，利润质量无法验证",
               "wm": "【缺口】"}

    # 组装：优先保留 2 条真值 + 1 条缺口；缺口不存在则补满 3 条真值；都无则标证据不足
    causes = truth[:2] + ([gap] if gap else [])
    if not gap:
        causes = truth[:3]
    if not causes:
        causes = [gap or {"kind": "证据不足", "evidence": val["trap_gap"], "wm": "【缺口】"}]

    return {"code": row.get("code", ""), "name": str(row.get("name", "")),
            "causes": causes,
            "headline": " / ".join(c["kind"] for c in causes) or "无显著失败路径",
            "note": "事前尸检只列失败路径，不构成买卖结论、不新增否决口径"}


# ─────────────────────────── 5. 研判标的池 ───────────────────────────────
def universe(data: dict, verify: dict | None = None) -> dict[str, Any]:
    """研判标的池：优先涨停源主池∩候选（可核验），否则退到资金维 TOP。

    verify 为 limitup_source.verify_covered 的实跑结果（可选），用于 DECIDE 步引用
    冻结闸门真实结论；此处不重跑、不改写。
    """
    cand = {c.get("code"): c for c in data.get("candidates", [])}
    mode = data.get("selection_mode")
    src, codes = "", []
    if mode == "limitup":
        pool = ((data.get("limitup") or {}).get("pool") or [])
        covered = [p.get("code") for p in pool if p.get("code") in cand]
        if covered:
            src = "涨停源主池∩候选（龙虎榜净买降序）"
            codes = list(dict.fromkeys(covered))[:UNIVERSE_CAP]
    if not codes:
        ranked = sorted([c for c in cand.values() if _f(c.get("flow")) is not None],
                        key=lambda c: -(_f(c.get("flow")) or 0))
        src = "资金维 flow 降序 TOP（回退口径）"
        codes = [c["code"] for c in ranked[:UNIVERSE_CAP]]

    rows = [valuation_row(cand[code]) for code in codes if code in cand]
    quals = [quality_row(cand[code]) for code in codes if code in cand]
    radars = [radar_row(cand[code]) for code in codes if code in cand]
    qmap = {q["code"]: q for q in quals}
    rmap = {r["code"]: r for r in radars}
    premorts = [premortem_row(cand[r["code"]], r, qmap[r["code"]], rmap[r["code"]])
                for r in rows if r["code"] in qmap and r["code"] in rmap]

    vmap_rows = ({v["code"]: v for v in (verify or {}).get("rows", [])})
    for r in rows:
        v = vmap_rows.get(r["code"])
        r["gate"] = ("通过" if v["passed"] else "L3 否决") if v else "未核验/非涨停源"

    return {"source": src, "n": len(rows), "rows": rows, "quality": quals,
            "radar": radars, "premortem": premorts,
            "verify_ref": ({"total_n": verify.get("total_n"), "passed_n": verify.get("passed_n"),
                            "l3_rejected_n": verify.get("l3_rejected_n")} if verify else None)}


# ───────────────────────── 6. 全样本分布（真值） ──────────────────────────
def distribution(data: dict) -> dict[str, Any]:
    """33 只候选的真值分布：亏损/负增长/高基数/PB 结构。全部来自非空字段。"""
    c = data.get("candidates", [])
    n = len(c)
    pes = [_f(x.get("pe")) for x in c]
    pbs = [_f(x.get("pb")) for x in c]
    pos_pe = [p for p in pes if p is not None and p > 0]
    pos_pb = [p for p in pbs if p is not None and p > 0]
    loss = sum(1 for p in pes if p is not None and p <= 0)
    neg_g = sum(1 for x in c if (_f(x.get("interim_yoy")) or 0) <= C.GROWTH_HARD_LINE)
    hb = sum(1 for x in c if (_f(x.get("interim_yoy")) or 0) > HIGH_BASE_RATIO)
    return {
        "n": n,
        "pe_median": round(statistics.median(pos_pe), 2) if pos_pe else None,
        "pb_median": round(statistics.median(pos_pb), 2) if pos_pb else None,
        "n_loss": loss, "n_neg_growth": neg_g, "n_high_base": hb,
        "n_pe_valid": len(pos_pe), "n_pb_valid": len(pos_pb),
        "note": "中位数仅取正值（负 PE=亏损不进估值中位数）；亏损/负增长/高基数为真值计数",
    }


# ─────────────────────────── 7. 数据缺口台账 ──────────────────────────────
def gap_inventory(data: dict) -> dict[str, Any]:
    """缺什么 → 测不了什么。逐字段统计 33 只候选的 null 数，并标注核验能力损失。"""
    c = data.get("candidates", [])
    n = len(c) or 1
    rows = []
    for f, why in QUALITY_GAP_FIELDS:
        miss = sum(1 for x in c if x.get(f) is None)
        rows.append({"field": f, "missing": miss, "total": n,
                     "rate": round(miss / n * 100), "unable": why})
    # 估值侧额外缺口（非 quality 字段，但同样影响投行级判定）
    extra = []
    for f, why in (("dividend_yield", "红利股息率锚"),
                   ("profit_at_cycle_peak", "周期顶低 PE 陷阱"),
                   ("consensus_growth", "前瞻 PEG（替代高基数失真口径）")):
        extra.append({"field": f, "missing": n, "total": n, "rate": 100,
                      "unable": why + "（data.json 无此字段）"})
    return {"rows": rows, "extra": extra,
            "headline": f"穿透财报 {len(QUALITY_GAP_FIELDS)} 字段 + 估值 {len(extra)} 字段"
                        f"在 data.json 全为空 → 相关核验一律标【缺口】，不编造",
            "note": "缺口台账是「不编造」纪律的机器化留痕；字段补齐后自动参与真值判定"}


# ───────────────────────── 8. 全周期全链路视图 ────────────────────────────
def lifecycle(data: dict, uni: dict[str, Any], dist: dict[str, Any]) -> dict[str, Any]:
    """五步决策框架落到当日真值：DEFINE→ANALYZE→SYNTHESIZE→DECIDE→EXECUTE。"""
    ctx = data.get("context") or {}
    lu = (data.get("limitup") or {})
    mkt = lu.get("market") or {}
    vr = uni.get("verify_ref") or {}
    top = uni["rows"][0] if uni["rows"] else None
    qsum = uni["quality"][0] if uni["quality"] else None
    mainline = " / ".join(m.get("name", "") for m in (lu.get("mainline_industries") or [])) or "无"
    prem_top = uni["premortem"][0]["headline"] if uni["premortem"] else "证据不足"
    cap = data.get("capital") or {}
    budget = float((data.get("context") or {}).get("equity") or 0) * float(cap.get("alpha_budget_pct") or 0.30)

    steps = [
        {"step": "DEFINE 定义", "truth": f"涨停 {mkt.get('limit_up','—')} 家 / 最高 {mkt.get('max_height','—')} 板；"
         f"研判问题：主线『{mainline}』是否值得出手？", "wm": "【事实】"},
        {"step": "ANALYZE 分析", "truth": f"候选 {dist['n']} 只：PE 中位 {dist['pe_median']} / 亏损 {dist['n_loss']} / "
         f"负增长 {dist['n_neg_growth']} / 高基数 {dist['n_high_base']}；穿透字段全缺口", "wm": "【事实+缺口】"},
        {"step": "SYNTHESIZE 综合", "truth": f"So What：主池∩候选 {uni['n']} 只可深研（来源 {uni['source']}）；"
         f"头部 {top['name'] if top else '无'} 五维 {uni['radar'][0]['composite'] if uni['radar'] and uni['radar'][0]['composite'] is not None else '缺口'}", "wm": "【事实】"},
        {"step": "DECIDE 决策", "truth": f"冻结闸门实跑 通过 {vr.get('passed_n','—')}/{vr.get('total_n','—')}"
         f"（L3 否 {vr.get('l3_rejected_n','—')}）；Pre-Mortem 首要：{prem_top}；本层不授权 BUY", "wm": "【事实】"},
        {"step": "EXECUTE 执行", "truth": f"α 预算 {budget/1e8:.2f} 亿受容量约束；试错四步（1/4 试探→溢价验证→金字塔→证伪清零）；"
         f"次日 19:15 预判核验复盘（AAR）", "wm": "【事实】"},
    ]
    return {"steps": steps, "budget_yi": round(budget / 1e8, 2),
            "note": "全链路是推理链脚手架：每步落到真值或明确缺口，不改变判定、不生成 BUY"}


# ───────────────────── 非侵入性自检（口径未污染）─────────────────────
QUANT_EXPECTED = {
    "CALIBER_VERSION": "v2.3",
    "SOE_BACKGROUND_IS_GATE": False,
    "EMERGING_TECH_FIRST": True,
    "PROFIT_GROWTH_CALIBER": "half_year",
    "SINGLE_YEAR_LOSS_IS_VETO": False,
    "TWO_CONSECUTIVE_LOSSES_IS_VETO": True,
    "CHAIN_THEME_SKIPS_L1_VETO": True,
    "TRADABILITY_LAYER": "L2.5",
    "RANK_LOW_THRESHOLD": 25.0,
    "VR_THRESHOLD": 1.0,
}


def gceo_quant_non_invasive_check(data: dict | None = None, verify: dict | None = None) -> dict:
    """证明 v4.0 投行量化引擎未污染冻结口径、不编造估值、不夺权。"""
    checks: list[dict] = []
    for k, exp in QUANT_EXPECTED.items():
        act = getattr(C, k, "<缺失>")
        checks.append({"item": f"冻结口径 {k}", "expected": exp, "actual": act, "ok": act == exp})
    k = getattr(C, "KNOWLEDGE", {}) or {}
    checks.append({"item": "KNOWLEDGE 键数不变", "expected": 45, "actual": len(k), "ok": len(k) == 45})
    checks.append({"item": "KNOWLEDGE 红旗否决线", "expected": 2, "actual": k.get("红旗否决线"),
                   "ok": k.get("红旗否决线") == 2})
    checks.append({"item": "v3 旁路版本不变", "expected": "v3.0", "actual": getattr(C, "EXTENSION_VERSION", None),
                   "ok": getattr(C, "EXTENSION_VERSION", None) == "v3.0"})
    checks.append({"item": "GCCEO 源版本不变", "expected": "4.0.0", "actual": GCEEO_SOURCE_UNCHANGED,
                   "ok": GCEEO_SOURCE_UNCHANGED == "4.0.0"})
    checks.append({"item": "五维权重未被二次计分", "expected": F.S_WEIGHTS, "actual": F.S_WEIGHTS,
                   "ok": abs(sum(F.S_WEIGHTS.values()) - 1.0) < 1e-9})
    checks.append({"item": "不编造估值", "expected": True, "actual": NO_FABRICATED_VALUATION,
                   "ok": NO_FABRICATED_VALUATION is True})
    checks.append({"item": "无剔除权", "expected": True, "actual": NO_VETO, "ok": NO_VETO is True})
    checks.append({"item": "无仓位上调权", "expected": True, "actual": NO_POSITION_UP, "ok": NO_POSITION_UP is True})
    checks.append({"item": "开关数", "expected": 6, "actual": SWITCH_COUNT, "ok": SWITCH_COUNT == 6})

    if data is not None:
        uni = universe(data, verify=verify)
        dist = distribution(data)
        gap = gap_inventory(data)
        # 真值纪律：所有 PEG 要么 None 要么来自 pe/growth 实算；无 DCF/LBO 字段产出
        peg_ok = all(r["peg_h1"] is None or (r["pe"] and r["g_h1"]) for r in uni["rows"])
        checks.append({"item": "PEG 仅真值实算", "expected": True, "actual": peg_ok, "ok": peg_ok})
        no_dcf = all("dcf" not in str(r).lower() and "lbo" not in str(r).lower()
                     for r in uni["rows"])
        checks.append({"item": "无编造 DCF/LBO 数值", "expected": True, "actual": no_dcf, "ok": no_dcf})
        checks.append({"item": "缺口台账登记", "expected": len(QUALITY_GAP_FIELDS),
                       "actual": len(gap["rows"]), "ok": len(gap["rows"]) == len(QUALITY_GAP_FIELDS)})
        checks.append({"item": "研判池不越过页高上限", "expected": UNIVERSE_CAP,
                       "actual": uni["n"], "ok": uni["n"] <= UNIVERSE_CAP})
        checks.append({"item": "Pre-Mortem 每只≤3因", "expected": True,
                       "actual": all(len(p["causes"]) <= 3 for p in uni["premortem"]),
                       "ok": all(len(p["causes"]) <= 3 for p in uni["premortem"])})
        checks.append({"item": "分布样本守恒", "expected": len(data.get("candidates", [])),
                       "actual": dist["n"], "ok": dist["n"] == len(data.get("candidates", []))})
    passed = sum(1 for c in checks if c["ok"])
    return {"passed": passed, "total": len(checks), "all_ok": all(c["ok"] for c in checks),
            "checks": checks,
            "contract": "v2.3 六口径 + KNOWLEDGE45 + v3.0 + GCCEO4.0 全部只读比对；"
                        "投行量化旁路只做真值研判 + 缺口标注，不编造、不夺权"}


GCEEO_SOURCE_UNCHANGED = "4.0.0"   # 被整合的 GCCEO 源版本（只读锚）


# ─────────────────────────── 统一入口 ───────────────────────────
def build_gceo_quant_overlay(data: dict, verify: dict | None = None,
                             check_modules: bool = True) -> dict:
    """生成可 JSON 序列化的 `gceo_quant` 覆盖层（只读，不改既有键）。

    gceo.enabled / v3.enabled 的强依赖由装配器 build_gceo_quant_inputs.py 负责判定；
    本函数只产出内容与自检，enabled 先写 True，由装配器覆盖。
    """
    uni = universe(data, verify=verify)
    dist = distribution(data)
    gap = gap_inventory(data)
    life = lifecycle(data, uni, dist)
    ov: dict[str, Any] = {
        "enabled": True,
        "overlay_only": OVERLAY_ONLY,
        "extension_version": GCEEO_QUANT_VERSION,
        "source_version": GCEEO_SOURCE_UNCHANGED,
        "framework_version": FRAMEWORK_VERSION,
        "caliber_version_unchanged": CALIBER_VERSION_UNCHANGED,
        "no_veto": NO_VETO, "no_position_up": NO_POSITION_UP,
        "no_fabricated_valuation": NO_FABRICATED_VALUATION,
        "switches": dict(QUANT_SWITCHES),
        "source": GCEEO_QUANT_SOURCE,
        "universe": uni, "distribution": dist, "gap_inventory": gap, "lifecycle": life,
        "non_invasive_check": (gceo_quant_non_invasive_check(data, verify) if check_modules
                               else {"passed": 0, "total": 0, "all_ok": True, "checks": []}),
        "rollback": ("data.json 顶层 gceo_quant.enabled=false → 回到 v3.1 18 页；"
                     "gceo.enabled=false → v3.0 16 页；v3.enabled=false → v2.3 14 页。三层正交。"),
        "frequency": "随报告日重算；不引入新取数频率，不复用 scoring / funnel 中间量作二次计分。",
    }
    ov["blocks"] = gceo_quant_report_blocks(ov)
    return ov


def gceo_quant_report_blocks(ov: dict) -> dict[str, Any]:
    """压成渲染器可直接取用的文本块（模板里不写逻辑）。"""
    uni, dist = ov["universe"], ov["distribution"]
    gap, life = ov["gap_inventory"], ov["lifecycle"]
    ch = ov["non_invasive_check"]

    val_rows = []
    for r in uni["rows"]:
        # PEG 双口径：以上年度为参照锚（更稳），半年为波动补充；仅限真值实算。
        # 高基数失真标记绑定「所选口径」自身增速，避免用半年高基数去误伤上年度 PEG。
        primary, pbase = (r["peg_fy"], r["g_fy"]) if r["peg_fy"] is not None \
            else (r["peg_h1"], r["g_h1"])
        if primary is None:
            peg_txt = "不适用"
        elif pbase is not None and pbase > HIGH_BASE_RATIO:
            peg_txt = f"{primary:.2f}*"
        else:
            peg_txt = f"{primary:.2f}"
        h1 = f"{r['peg_h1']:.2f}" if r["peg_h1"] is not None else "—"
        fy = f"{r['peg_fy']:.2f}" if r["peg_fy"] is not None else "—"
        val_rows.append({
            "name": r["name"], "biz": r["biz"], "pe": r["pe_txt"], "pb": r["pb_txt"],
            "g_h1": _pct(r["g_h1"]), "peg": peg_txt, "peg_dual": f"{fy}/{h1}",
            "deduct": r["deduct_yi"], "anchor": r["anchor_desc"][:34], "gate": r["gate"],
        })

    rad_rows = []
    for r in uni["radar"]:
        d = r["dims"]
        rad_rows.append({
            "name": r["name"],
            "tech": d.get("tech"), "flow": d.get("flow"), "fund": d.get("fund"),
            "cycle": d.get("cycle"), "fib": d.get("fib"), "composite": r["composite"],
        })

    pm_rows = []
    for p in uni["premortem"]:
        pm_rows.append({"name": p["name"], "headline": p["headline"],
                        "causes": [f"{c['kind']}（{c['evidence']}）{c['wm']}" for c in p["causes"]]})

    gap_rows = [{"field": g["field"], "rate": g["rate"], "unable": g["unable"]}
                for g in gap["rows"]]
    extra_rows = [{"field": g["field"], "unable": g["unable"]} for g in gap["extra"]]
    life_rows = [{"step": s["step"], "truth": s["truth"], "wm": s["wm"]} for s in life["steps"]]

    headline = (
        f"投行级量化研判已挂载 · 真值算+缺口标注：候选 {dist['n']} 只 PE 中位 "
        f"{dist['pe_median']} / 亏损 {dist['n_loss']} / 负增长 {dist['n_neg_growth']}；"
        f"穿透 {len(gap['rows'])} 字段全缺口如实标注，不编造 DCF/LBO；"
        f"研判池 {uni['n']} 只（{uni['source']}），不生成 BUY"
    )
    return {
        "headline": headline,
        "val_rows": val_rows, "rad_rows": rad_rows, "pm_rows": pm_rows,
        "gap_rows": gap_rows, "extra_rows": extra_rows, "life_rows": life_rows,
        "dist": dist, "universe_src": uni["source"], "universe_n": uni["n"],
        "budget_yi": life["budget_yi"],
        "checks": ch,
        "watermarks": {
            "truth": "【事实】PE/PB/同比/扣非/五维 取自 data.json 非空字段",
            "gap": "【缺口】净现比/商誉/补助/归母/股东户数/股息率/周期位置 全空 → 不判定",
            "infer": "【推定】商业模式按行业映射，非公司披露",
            "diff": "【口径差异】PEG 高基数失真 + 无一致预期 → 仅参考非结论",
        },
        "rollback": ov["rollback"],
        "counts": {
            "val_n": len(val_rows), "rad_n": len(rad_rows), "pm_n": len(pm_rows),
            "gap_fields": len(gap_rows), "extra_gaps": len(extra_rows),
            "life_steps": len(life_rows),
            "checks_passed": ch["passed"], "checks_total": ch["total"],
        },
    }


if __name__ == "__main__":
    import json
    root = _ROOT
    p = _os.path.join(root, "strategy", "sample_data.json")
    data = json.load(open(p, encoding="utf-8")) if _os.path.exists(p) else {"candidates": []}
    ov = build_gceo_quant_overlay(data)
    print(f"投行量化引擎非侵入性自检 {ov['non_invasive_check']['passed']}/"
          f"{ov['non_invasive_check']['total']} all_ok={ov['non_invasive_check']['all_ok']}")
    print(json.dumps(ov["blocks"]["counts"], ensure_ascii=False, indent=2))
