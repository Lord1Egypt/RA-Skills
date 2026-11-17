#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
signal_score.py / 综合安全信号评分与证据分级（#4 多源三角验证）

将多个证据源综合为一个定量 Safety Signal Score (0-100) 与证据分级 T1-T4：

  源（权重上限）：
    1. FAERS 信号强度 (base, 0-50)   -- ROR/PRR/IC 综合，signal_overall 为假则打折
    2. FDR 多重比较一致性 (0-10)     -- 有 fdr_q 时 q<0.05 加分；单事件中性 +5
    3. 时间序列异常 #5 (0-15)        -- trend_flag 为真加分
    4. 中国 PV 定性佐证 (0-20)       -- cn_pv_hits 越多加分越高
    5. 控制验证一致性 #6 (0-10)      -- control_agreement 双组>=0.8 加分
    6. FDA Label 收录状态 (0-5)      -- unlabeled(新信号) 加分，labeled 不加

  证据分级 T1-T4：
    T1 强证据 (Strong)        : score>=80 且 FAERS signal 且 >=2 独立源佐证
    T2 中等 (Moderate)        : score>=60 且 FAERS signal 且 >=1 独立源佐证
    T3 弱 (Weak)              : score>=40 或 FAERS signal 为真（但佐证少）
    T4 不确定 (Indeterminate) : score<40 且 FAERS signal 为假

纯函数，不联网，不依赖外部库（仅 math）。所有分量权重集中在 WEIGHTS 常量，
可按需调整；评分逻辑透明可审计（各分量显式输出）。
"""
import math


WEIGHTS = {
    "ror_max": 25.0,
    "prr_max": 15.0,
    "ic_max": 10.0,
    "fdr_hit": 10.0,
    "fdr_neutral": 5.0,
    "trend": 15.0,
    "cn_pv_t1": 10.0,   # 1-2 hits
    "cn_pv_t2": 15.0,   # 3-5 hits
    "cn_pv_t3": 20.0,   # >5 hits
    "control_hit": 10.0,
    "control_partial": 5.0,
    "label_unlabeled": 5.0,
}

# 标签"已收录"的风险不再额外加分（已是预期）；新信号才提示价值。
TIERS = {
    "T1": "强证据 (Strong)",
    "T2": "中等 (Moderate)",
    "T3": "弱 (Weak)",
    "T4": "不确定 (Indeterminate)",
}


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def _log10_score(value, max_points):
    """Map a disproportionality value (>1) onto [0, max_points] via log10.
    value<=1 (no signal direction) yields 0."""
    if value is None or value <= 1:
        return 0.0
    return _clamp(max_points * (math.log10(value) / math.log10(10.0)),
                  0.0, max_points)


def safety_signal_score(faers_res, fda_label_status="skipped", cn_pv_hits=0,
                        trend_flag=False, control_agreement=None, control_pair=None):
    """Compute the composite Safety Signal Score (0-100) and evidence tier T1-T4.

    Args:
      faers_res          : dict from disproportionality.compute() (must contain
                           ROR/PRR/IC/signal_overall + optional fdr_q).
      fda_label_status   : "labeled" | "unlabeled" | "unknown" | "skipped"
      cn_pv_hits         : int, hit count from China PV bulletins (0 if none)
      trend_flag         : bool, time-series anomaly detected (#5)
      control_agreement  : dict {"positive": {"rate":..}, "negative": {"rate":..}}
                           or None if control validation not run (#6)
      control_pair       : lightweight single-anchor check for a NORMAL run:
                           {"group": "positive"|"negative", "expected": bool,
                            "signal": bool} when the queried (drug,event) is
                           itself a known control pair; None otherwise. No
                           network needed — lets a single --run report a control
                           component instead of always 0.

    Returns dict {score, tier, tier_label, components, label_status,
                  corroborate_sources, rationale}.
    """
    comp = {}
    # 1) FAERS base (ROR/PRR/IC -> up to 50)
    ror_v = (faers_res.get("ROR") or {}).get("value", 1.0)
    prr_v = (faers_res.get("PRR") or {}).get("value", 1.0)
    ic_v = (faers_res.get("IC") or {}).get("value", 0.0)
    ror_s = _log10_score(ror_v, WEIGHTS["ror_max"])
    prr_s = _log10_score(prr_v, WEIGHTS["prr_max"])
    ic_s = _clamp(WEIGHTS["ic_max"] * max(ic_v, 0.0) / 2.0, 0.0, WEIGHTS["ic_max"])
    base = ror_s + prr_s + ic_s  # up to 50
    if not faers_res.get("signal_overall", False):
        base *= 0.5
    comp["faers_base"] = round(base, 2)

    # 2) FDR (multiple-comparison control)
    if "fdr_q" in faers_res and faers_res["fdr_q"] is not None:
        comp["fdr"] = WEIGHTS["fdr_hit"] if faers_res["fdr_q"] < 0.05 else 0.0
    else:
        comp["fdr"] = WEIGHTS["fdr_neutral"]
    comp["fdr"] = round(comp["fdr"], 2)

    # 3) trend (#5)
    comp["trend"] = WEIGHTS["trend"] if trend_flag else 0.0

    # 4) China PV qualitative corroboration
    if cn_pv_hits <= 0:
        comp["cn_pv"] = 0.0
    elif cn_pv_hits <= 2:
        comp["cn_pv"] = WEIGHTS["cn_pv_t1"]
    elif cn_pv_hits <= 5:
        comp["cn_pv"] = WEIGHTS["cn_pv_t2"]
    else:
        comp["cn_pv"] = WEIGHTS["cn_pv_t3"]

    # 5) control validation (#6)
    #   control_agreement : 全量交叉核验（来自 --validate-controls，联网跑多组对照）
    #   control_pair      : 常规 run() 内的轻量单锚点核验（不联网）——若被查询的
    #                       (药物,事件) 本身就是已知阳/阴性对照，则按流水线是否
    #                       与既定预期一致给 controls 分量（≤10），让单 run 也有
    #                       控制证据反馈，而非恒为 0。
    if control_agreement:
        pr = control_agreement.get("positive", {}).get("rate")
        nr = control_agreement.get("negative", {}).get("rate")
        if pr is not None and nr is not None and pr >= 0.8 and nr >= 0.8:
            comp["controls"] = WEIGHTS["control_hit"]
        elif (pr is not None and pr >= 0.8) or (nr is not None and nr >= 0.8):
            comp["controls"] = WEIGHTS["control_partial"]
        else:
            comp["controls"] = 0.0
    elif control_pair:
        agree = bool(control_pair.get("signal")) == bool(control_pair.get("expected"))
        comp["controls"] = WEIGHTS["control_hit"] if agree else 0.0
    else:
        comp["controls"] = 0.0

    # 6) FDA Label (new-signal bonus only)
    comp["label_extra"] = WEIGHTS["label_unlabeled"] if fda_label_status == "unlabeled" else 0.0

    score = _clamp(sum(comp.values()), 0.0, 100.0)
    score = round(score, 1)

    # corroborating independent sources (FAERS is the primary source, not counted)
    corroborate = 0
    corr_list = []
    if cn_pv_hits > 0:
        corroborate += 1
        corr_list.append("中国PV")
    if fda_label_status in ("labeled", "unlabeled"):
        corroborate += 1
        corr_list.append("FDA Label")
    if trend_flag:
        corroborate += 1
        corr_list.append("时间序列")
    if control_agreement:
        corroborate += 1
        corr_list.append("控制验证")
    elif control_pair and bool(control_pair.get("signal")) == bool(control_pair.get("expected")):
        corroborate += 1
        corr_list.append("控制验证")

    signal = bool(faers_res.get("signal_overall", False))
    if score >= 80 and signal and corroborate >= 2:
        tier = "T1"
    elif score >= 60 and signal and corroborate >= 1:
        tier = "T2"
    elif score >= 40 or signal:
        tier = "T3"
    else:
        tier = "T4"

    rationale = _rationale(faers_res, fda_label_status, cn_pv_hits,
                           trend_flag, score, tier, corr_list)

    return {
        "score": score,
        "tier": tier,
        "tier_label": TIERS[tier],
        "components": {k: round(v, 2) for k, v in comp.items()},
        "label_status": fda_label_status,
        "corroborate_sources": corr_list,
        "rationale": rationale,
    }


def _rationale(faers_res, label_status, cn_pv_hits, trend_flag, score, tier, corr):
    ror = (faers_res.get("ROR") or {}).get("value")
    eb = (faers_res.get("EBGM") or {}).get("value")
    bits = []
    if ror is not None:
        bits.append("FAERS ROR=%.1f" % ror)
    if eb is not None:
        bits.append("EBGM=%.1f" % eb)
    if label_status == "unlabeled":
        bits.append("标签未收录(新信号)")
    elif label_status == "labeled":
        bits.append("标签已收录(已知)")
    if cn_pv_hits > 0:
        bits.append("中国PV %d条" % cn_pv_hits)
    if trend_flag:
        bits.append("时间序列异常")
    if corr:
        bits.append("佐证源=%s" % "/".join(corr))
    else:
        bits.append("无独立源佐证")
    return "%s -> %s / %s 分" % (" + ".join(bits), tier, score)
