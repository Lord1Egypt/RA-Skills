#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assumption_block.py — 样本量计算的「假设清单显式化」

问题：主流程静默使用大量默认参数（不传 --alpha 即 0.05、默认双侧、默认脱落率…），
用户拿不到「这次到底用了哪些假设、参数落在什么区间、有什么解读风险」的显式清单，
可审计性不足。

本模块产出四段结构化清单：
  inputs     —— 用户**显式**给过的参数（与 parser 默认值逐项比对，等于默认不算显式）
  assumptions—— 走了默认值的参数（这是「静默默认值」的唯一出口）
  bounds     —— 每个关键参数的合理区间与单位，越界显式标出提示（不拦截计算）
  risks      —— 按 test 绑定的解读风险条目静态表

纯标准库，不触动数值真相源（不调用 R / coze）。
"""

import argparse
import json
import sys


# 参与审计的关键参数（其余纯内部开关不进清单，避免噪音）
KEY_PARAMS = [
    "alpha", "power", "nobs", "side", "effect", "sd", "ratio",
    "margin", "hazard_ratio", "dropout_rate", "k_groups", "p1", "p2",
    "theta0", "theta1", "theta2", "cv", "design", "correlation", "icc",
    "auc0", "auc1", "lambda1", "lambda2", "ve_control", "ve_treatment",
    "prob_control", "prob_treatment", "n_doses", "target_dlt",
    "ni_margin_surv", "hr_expected", "accrual_time", "followup_time",
    "event_rate", "sup_margin", "win_ratio_theta", "n_endpoints_must",
    "effect_must", "correlation_must", "n_arms_mams", "n_stages_mams",
    "delta_effect", "timing", "observed_effect", "planned_effect",
    "n_completed", "n_planned", "varcorr", "sigma", "nsim",
]

# 合理区间表：param -> (lo, hi, unit, note)；lo/hi 为 None 表示无界
BOUNDS = {
    "alpha": (0.0, 0.5, "（单侧/双侧总 I 类错误率）", "通常取 0.025（单侧）或 0.05（双侧）"),
    "power": (0.0, 1.0, "目标检验效能", "监管常用 0.8 / 0.9"),
    "nobs": (1, None, "样本量/组", "给定时转为求效能"),
    "side": (None, None, "one/two", "单侧更灵敏但需事先设定方向"),
    "effect": (None, None, "效应量（或 Cohen's d）", "须有临床/先验依据"),
    "sd": (0.0, None, "标准差", "与 effect 同单位"),
    "ratio": (0.0, None, "组间例数比 n2/n1", "≠1 时不等例，需说明合理性"),
    "margin": (0.0, None, "非劣效/等效界值", "须临床判定，统计只验证把握度"),
    "hazard_ratio": (0.0, None, "风险比 HR", "期望 HR<1 表示处理更优"),
    "dropout_rate": (0.0, 0.5, "脱落率", "过高会显著放大所需样本量"),
    "k_groups": (2, None, "组数", "ANOVA/多组比较"),
    "p1": (0.0, 1.0, "治疗组比例", ""),
    "p2": (0.0, 1.0, "对照组比例", ""),
    "cv": (0.0, None, "变异系数", "BE 设计，通常 0.2~0.3"),
    "theta0": (0.0, None, "BE 真实比值", "默认 0.95（MAP 假设）"),
    "theta1": (0.0, None, "BE 等效下界", "默认 0.8"),
    "theta2": (0.0, None, "BE 等效上界", "默认 1.25"),
    "icc": (0.0, 1.0, "组内相关系数", "群随机设计"),
    "correlation": (-1.0, 1.0, "相关系数", "多重终点/重复测量"),
    "event_rate": (0.0, 1.0, "事件率", "生存设计事件驱动"),
    "nsim": (1, None, "模拟次数", "过小蒙特卡洛误差大"),
}

# 按 test 绑定的解读风险静态表
RISKS = {
    "ttest_one": ["单侧检验：结果不可按双侧解读，方向须事先设定"],
    "non_inferiority": ["非劣效 margin 需临床判定；统计仅验证在 margin 内不劣的把握度",
                        "若期望效应接近 0，可能同时支持优效与'不劣'，需预设分析层级"],
    "ni_survival": ["非劣效生存 margin 通常取 HR 1.2~1.3，须临床论证",
                    "事件驱动：样本量由事件数而非仅入组数决定"],
    "superiority_margin": ["优效性 margin 设置影响所需样本量"],
    "equivalence": ["等效为双侧结论，依赖界值设定；区间外即不等效"],
    "be_tost": ["BE 等效界值双侧，结论依赖 theta1/theta2 设定",
                "默认 0.8~1.25；CV 估计误差会传导到样本量"],
    "survival": ["样本量由事件数驱动，需准确估计事件率与随访时长",
                 "脱落/删失过高会稀释检验效能"],
    "survival_exact": ["精确法较保守，样本量可能偏大"],
    "cox_covariate": ["协变量调整提升效能，但需满足比例风险假设"],
    "group_sequential": ["成组序贯消耗函数（O'Brien-Fleming / Pocock）选择影响中期 α 拆分"],
    "gsd_proportion": ["成组序贯比例的消耗函数选择影响中期分析 α"],
    "gsd_survival": ["成组序贯生存消耗函数选择影响中期 α 与事件数"],
    "gsd_hazard": ["成组序贯 HR 消耗函数选择影响中期 α"],
    "gsd_poisson": ["成组序贯泊松消耗函数选择影响中期 α"],
    "adaptive": ["自适应设计需预先规定调整规则，避免操纵α"],
    "adaptive_simulate": ["模拟法结果受随机种子与模拟次数影响"],
    "bayesian": ["保证概率（assurance）依赖先验设定，非经典频率派把握度"],
    "assurance": ["assurance 依赖先验，与经典 power 不可直接比较"],
    "mams": ["多臂多阶段：各阶段停止边界需预先设定"],
    "dose_escalation": ["剂量爬坡基于 DLT 概率，目标 DLT 率设定敏感"],
    "win_ratio": ["Win-Ratio 依赖序次结局定义，复合终点权重隐含其中"],
    "must_win": ["Must-Win 强约束：需全部终点显著，整体 α 保守"],
    "historical_controls": ["借外部对照需论证同质性，借用比例影响 I 类错误"],
    "vaccine_efficacy": ["疫苗效力由两组发病风险差推算"],
    "cluster": ["群随机需 ICC 与群大小，ICC 估计误差显著放大样本量"],
    "roc": ["ROC 样本量依赖 AUC 差异与判别阈值"],
    "poisson": ["泊松率比较需暴露时间口径一致"],
    "competing_risks": ["竞争风险需明确事件类型，删失机制假设敏感"],
    "recurrent_events": ["复发事件需设定复发过程模型"],
    "mixed_model": ["MMRM 依赖协方差结构设定，脱落机制假设敏感"],
    "multiple_endpoints": ["多终点须做多重性校正（见 mult_alloc.py），否则族错误率膨胀"],
    "dunnett": ["Dunnett 多对一比较，α 分配隐含在临界值表"],
    "mediation": ["中介分析需因果识别假设（无未测混杂）"],
    "conditional_power": ["条件效能用于期中决策，依赖当前效应估计"],
}


def build_assumption_block(args, test, parser, effect_ref=None):
    """构造假设清单（四段 + 可选公开证据参考段）。

    Parameters
    ----------
    args : argparse.Namespace   已解析的命令行参数
    test : str | None           终点类型（决定 risks 段）
    parser : argparse.ArgumentParser  用于取默认值

    Returns
    -------
    dict: {test, inputs, assumptions, bounds, risks, flagged}
    """
    dests = {a.dest for a in parser._actions}

    inputs, assumptions = [], []
    bounds_out, flagged = [], []

    for k in KEY_PARAMS:
        if k not in dests:
            continue
        value = getattr(args, k, None)
        default = parser.get_default(k)
        explicit = (value is not None) and (default is None or value != default)
        if explicit:
            inputs.append({"param": k, "value": value, "source": "user"})
        else:
            assumptions.append({"param": k, "value": value, "source": "default"})

        # bounds 检查（仅对实际有值的参数）
        if value is not None and k in BOUNDS:
            lo, hi, unit, note = BOUNDS[k]
            oob = False
            if lo is not None and value < lo:
                oob = True
            if hi is not None and value > hi:
                oob = True
            bounds_out.append({
                "param": k, "value": value, "unit": unit,
                "expected": _fmt_range(lo, hi),
                "note": note, "out_of_range": oob,
            })
            if oob:
                flagged.append("参数 %s=%s 超出合理区间 %s" % (k, value, _fmt_range(lo, hi)))

    risks = RISKS.get(test, []) if test else []

    # 公开证据效应量参考段（路线 A，2026-10-14）：仅展示，采纳状态显式标注。
    # 参考 ≠ 代入：人群/终点/尺度可比性由使用人复核（effect_ref.compatible 已挡尺度硬冲突）。
    references = None
    if effect_ref:
        references = {
            "ta": effect_ref.get("ta"),
            "endpoint": effect_ref.get("endpoint"),
            "summary": effect_ref.get("summary"),
            "adopted": effect_ref.get("adopted"),
            "disclaimer": effect_ref.get("disclaimer"),
        }
        risks = risks + ["公开参考 ≠ 本试验假设：人群/终点/效应量尺度须可比"]

    return {
        "test": test,
        "inputs": inputs,
        "assumptions": assumptions,
        "bounds": bounds_out,
        "references": references,
        "risks": risks,
        "flagged": flagged,
    }


def _fmt_range(lo, hi):
    if lo is not None and hi is not None:
        return "(%s, %s)" % (lo, hi)
    if lo is not None:
        return "(%s, +inf)" % lo
    if hi is not None:
        return "(-inf, %s)" % hi
    return "(-inf, +inf)"


def _main():
    ap = argparse.ArgumentParser(description="样本量假设清单显式化（独立冒烟用）")
    ap.add_argument("--test", default="ttest_ind")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--effect", type=float, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    block = build_assumption_block(a, a.test, ap)
    text = json.dumps(block, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
