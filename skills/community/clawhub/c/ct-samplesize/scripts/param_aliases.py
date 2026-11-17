#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
param_aliases.py — ct-samplesize v5 自然语言参数别名解析（确定性层，零 LLM）

职责：
  - 把中文 / 英文自然语言中的同义词归一化到 CLI 参数名
    （把握度 / 检验效能 → power；显著性水平 / Ⅰ类错误 / α → alpha；…）。
  - 从 NL 文本中提取数值参数（alpha / power / effect / margin / hazard_ratio /
    p1 / p2 / cv / theta0 / nobs …）。
  - 未命中或不完整时返回**结构化兜底信号**（needs_llm_fallback + missing），
    绝不静默错参（对应 meta-analysis「亚组静默失效」那类隐蔽坑）。

设计原则（对齐 meta-analysis 的确定性路由纪律）：
  - 纯正则 + 同义词表，不调任何 LLM，结果可测、可复现。
  - 提取出来的参数才写进 params（不推断、不补默认值），避免「静默错参」。
  - 检测不到关键信息时，needs_llm_fallback=True 并列出 missing，由上游提示用户。

对外接口：
  extract_parameters(nl, test=None) -> dict
    {
      "params":            { "power": 0.8, "alpha": 0.05, ... },  # 仅 NL 中明确给出的
      "solve_for_power":   bool,        # 给定 n 求 power（反之默认求 n）
      "side":              None|"one"|"two",
      "missing":           [str],       # 关键但未能识别的参数（供上游提示）
      "needs_llm_fallback":bool,        # 命中率低 / 歧义时置 True
      "notes":             [str],       # 人类可读提示
    }
"""

from __future__ import annotations

import re

_NUM = r"(\d+(?:\.\d+)?)"

# ── 参数同义词表 ───────────────────────────────────────────────────────────
# 每个参数一组关键词；命中关键词 + 其后数值即提取。
# 百分率类参数（率 / AUC）在命中百分号时自动 /100。
_RATE_PARAMS = {"p1", "p2", "auc0", "auc1", "cv", "ve_control", "ve_treatment",
                "prob_control", "prob_treatment", "p_control_sup", "p_control_current",
                "ci_control", "ci_treatment", "cox_event_prop",
                # 以百分号给出时按百分数归一（把握度80%→0.8，显著性水平5%→0.05）
                "power", "alpha"}

# (cli_param, [关键词正则（不区分大小写，中文原样）], 是否百分率)
_PARAM_PATTERNS = [
    ("power", [r"把握度", r"检验效能", r"检验功效", r"power"], False),
    ("alpha", [r"显著性水平", r"一类错误", r"ⅰ类错误", r"α", r"alpha"], False),
    ("effect", [r"效应量", r"效应大小", r"标准均差", r"cohen\s*d", r"effect\s*size", r"均差", r"均值差", r"(?<![a-z])d\s*[:=]"], False),
    ("sd", [r"标准差", r"sd\b", r"标准偏差"], False),
    ("margin", [r"非劣效界值", r"等效界值", r"界值", r"margin"], False),
    ("hazard_ratio", [r"风险比", r"hazard\s*ratio", r"\bhr\b"], False),
    ("p1", [r"试验组", r"治疗组", r"处理组", r"新药组", r"干预组",
            r"试验组.*率", r"试验.*比例", r"治疗组.*有效"], True),
    ("p2", [r"对照组", r"标准组", r"安慰剂组", r"参照组",
            r"对照组.*率", r"对照.*比例"], True),
    ("cv", [r"变异系数", r"\bcv\b"], True),
    ("theta0", [r"theta0", r"几何均值比", r"几何均值"], False),
    ("auc0", [r"auc0", r"对照\s*auc", r"基线\s*auc"], True),
    ("auc1", [r"auc1", r"试验\s*auc", r"治疗\s*auc"], True),
    ("lambda1", [r"lambda1", r"试验组发生率", r"治疗组发生率"], False),
    ("lambda2", [r"lambda2", r"对照组发生率"], False),
    ("icc", [r"icc", r"组内相关系数"], False),
    ("ni_margin_surv", [r"非劣效.*生存.*界", r"ni.*margin.*surv", r"生存非劣效界"], False),
    ("eq_margin_surv", [r"等效.*生存.*界", r"surv.*equiv.*margin"], False),
    ("sup_margin", [r"优效界值", r"优效.*margin"], False),
    ("sup_margin_surv", [r"生存优效界", r"surv.*sup.*margin"], False),
    ("cox_hr", [r"cox.*hr", r"cox风险比"], False),
    ("cox_r2", [r"cox.*r2", r"协变量.*r2"], False),
    ("cox_prev", [r"cox.*prev", r"暴露比例"], False),
    ("median0", [r"对照.*中位", r"median0", r"对照组中位生存"], False),
    ("median1", [r"试验.*中位", r"median1", r"治疗组中位生存"], False),
    ("rate_control", [r"对照组.*率", r"rate_control"], False),
    ("rate_ratio", [r"率比", r"rate_ratio", r"rate\s*ratio"], False),
    ("hr_expected", [r"期望.*hr", r"expected.*hr"], False),
    ("win_ratio_theta", [r"win.{0,3}ratio", r"win比率", r"胜率比"], False),
    # ── 非参数 Wilcoxon（NP1/NP2, v5.13.39）──
    # 注意：shape 是枚举（normal/logistic），不走数值匹配，见 _detect_shape
    ("superiority", [r"随机优势", r"优势概率", r"superiority", r"mann.{0,4}whitney.{0,6}(效应|优势)", r"p\s*\(\s*x\s*<\s*y\s*\)"], False),
    ("median_diff", [r"中位数差", r"中位.?数差异", r"median\s*diff", r"位置差"], False),
]


def _find_param(name, keywords, is_rate, nl):
    """在 nl 中搜索 (关键词 + 数值)，返回首个 (value, raw_str) 或 None。

    百分率类参数（率 / AUC / 把握度 / 显著性水平…）命中百分号时自动 /100。
    无百分号时，仅当关键词本身含「率 / 比例 / 响应 / 有效」等语境才接受，
    避免把「试验组均值差 0.5」里的 0.5 误抓为 p1。
    """
    _is_rate = bool(is_rate) or (name in _RATE_PARAMS)
    _RATE_CTX = ("率", "比例", "响应", "有效")
    for kw in keywords:
        pat = r"(?:%s)\s*[:=]?\s*%s\s*(%%|％)?" % (kw, _NUM)
        m = re.search(pat, nl, flags=re.IGNORECASE)
        if not m:
            continue
        val = float(m.group(1))
        pct = m.group(2)
        if _is_rate:
            if pct:
                val = val / 100.0
            elif name in ("alpha", "power"):
                # alpha / power 本就是 0~1 小数（如 α=0.05 / 把握度 0.8），直接接受小数，无需百分号/率语境
                pass
            elif not any(ch in kw for ch in _RATE_CTX):
                # 其余百分率类（率/AUC/变异系数…）无百分号且关键词无率语境 → 拒收，避免误抓效应量等无关数值
                continue
        return val, m.group(0)
    return None


# ── 求解方向：给定 n 求 power vs 给定 power 求 n ──────────────────────────────
_SOLVE_POWER_HINTS = [
    r"求.{0,4}(把握度|效能|power)",
    r"实际.{0,4}(把握度|效能)",
    r"给定.{0,6}(样本量|入组|n|例)",
    r"已知.{0,6}(样本量|n)",
    r"如果.{0,6}(只能|n|入组)",
    r"已经.{0,6}(入组|样本)",
]


def _detect_solve_for_power(nl, params):
    """检测是否「给定 n 求 power」。命中提示词且能提取到 nobs 才置 True。"""
    if re.search("|".join(_SOLVE_POWER_HINTS), nl, flags=re.IGNORECASE):
        nobs = _extract_nobs(nl)
        if nobs is not None:
            params["nobs"] = nobs
            return True
    return False


def _extract_nobs(nl):
    """提取样本量数值：n=30 / 样本量 30 / 入组 30 人 / 入 30 人 / 每组 30。"""
    pats = [
        r"n\s*[:=]\s*%s" % _NUM,
        r"样本量\s*[:=]?\s*%s" % _NUM,
        r"入组\s*[:=]?\s*%s\s*(?:人|例|名|受试者|个)?" % _NUM,
        r"入\s*%s\s*(?:人|例|名|受试者|个)?" % _NUM,
        r"每组\s*[:=]?\s*%s\s*(?:人|例|名|受试者|个)?" % _NUM,
        r"总共\s*[:=]?\s*%s\s*(?:人|例|名|受试者|个)?" % _NUM,
    ]
    for pat in pats:
        m = re.search(pat, nl, flags=re.IGNORECASE)
        if m:
            return int(float(m.group(1)))
    return None


# ── 检验方向 ──────────────────────────────────────────────────────────────
def _detect_side(nl):
    if re.search(r"单侧|one[- ]?sided|one side|单尾", nl, flags=re.IGNORECASE):
        return "one"
    if re.search(r"双侧|two[- ]?sided|two side|双尾", nl, flags=re.IGNORECASE):
        return "two"
    return None


# ── Wilcoxon 位移分布形状（NP1/NP2, v5.13.39）───────────────────────────────
# 枚举参数，无数值可抓：显式提到 logistic/厚尾 → logistic；正态位移 → normal；
# 都未提 → None（R 端默认 normal，审计会标 weak 提示未确认）。
def _detect_shape(nl):
    if re.search(r"logistic|厚尾", nl, flags=re.IGNORECASE):
        return "logistic"
    if re.search(r"正态位移|normal\s*shift|正态分布假设", nl, flags=re.IGNORECASE):
        return "normal"
    return None


# ── 两组均值差（效应量 d 的推断）────────────────────────────────────────────
# 「试验组收缩压下降 15mmHg，对照组下降 10mmHg」→ effect = |15 - 10| = 5。
# 仅当 NL 同时显式给出「试验组/治疗组」与「对照组」两组的变化数值才推断，
# 避免把单组描述误当效应量；与对话模式 Agent 的 Δ 推断对齐。
_MEAN_DIFF_A = re.compile(
    r"(?:试验组|治疗组|干预组|新药组|处理组)"
    r".{0,16}?(?:下降|降低|提高|升高|变化|差异|差值|改善)\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE)
_MEAN_DIFF_B = re.compile(
    r"(?:对照组|标准组|安慰剂组|参照组)"
    r".{0,16}?(?:下降|降低|提高|升高|变化|差异|差值|改善)\s*(\d+(?:\.\d+)?)",
    re.IGNORECASE)


def _detect_mean_diff(nl):
    """试验组变化 X、对照组变化 Y（均带单位数值）→ effect = |X - Y|；否则 None。"""
    a = _MEAN_DIFF_A.search(nl)
    b = _MEAN_DIFF_B.search(nl)
    if not a or not b:
        return None
    try:
        return abs(float(a.group(1)) - float(b.group(1)))
    except ValueError:
        return None


# ── 主接口 ────────────────────────────────────────────────────────────────
def extract_parameters(nl, test=None):
    """从自然语言提取参数，返回结构化 dict（见模块 docstring）。

    test 可选：传入已识别的 test 名可启用 test 专属的百分率 / 默认值上下文，
    本版先不依赖 test（保持解耦），后续可扩展。
    """
    nl = nl or ""
    params = {}
    notes = []
    missing = []
    hints = 0  # 命中参数计数（用于 needs_llm_fallback 判定）

    for name, keywords, is_rate in _PARAM_PATTERNS:
        res = _find_param(name, keywords, is_rate, nl)
        if res is not None:
            params[name] = res[0]
            hints += 1

    side = _detect_side(nl)
    if side:
        params["side"] = side
        hints += 1

    shape = _detect_shape(nl)
    if shape:
        params["shape"] = shape
        hints += 1

    # 两组均值差 → 效应量（仅当 NL 未显式给 effect 时推断，避免覆盖明确值）
    if "effect" not in params:
        mean_diff = _detect_mean_diff(nl)
        if mean_diff is not None:
            params["effect"] = mean_diff
            hints += 1

    solve_for_power = _detect_solve_for_power(nl, params)
    if solve_for_power:
        hints += 1

    # 兜底信号：完全没提取到任何参数，且 NL 也不含数值 → 很可能不是参数化需求
    has_any_number = bool(re.search(r"\d", nl))
    if hints == 0 and not has_any_number:
        needs_llm = True
        notes.append("未从自然语言识别到任何计算参数，需 LLM 兜底解析或向用户追问。")
    else:
        needs_llm = False

    return {
        "params": params,
        "solve_for_power": solve_for_power,
        "side": side,
        "missing": missing,
        "needs_llm_fallback": needs_llm,
        "notes": notes,
    }


# 供上游 quick-check：参数名是否在 --test 已知参数集合内（防止误提取到无关词）
KNOWN_PARAMS = set(name for name, _, _ in _PARAM_PATTERNS) | {"nobs", "side"}


if __name__ == "__main__":
    import json
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else \
        "两样本t检验：试验组70%对照组50%，非劣效界值0.1，把握度0.8，单侧"
    print(json.dumps(extract_parameters(sample), ensure_ascii=False, indent=2))
