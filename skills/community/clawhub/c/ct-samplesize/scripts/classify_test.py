#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify_test.py — ct-samplesize v5 自然语言 → --test 确定性路由（零 LLM）

把自然语言需求映射到 --test。纯关键词 + research-question 映射（来源：
references/menu.md Part 0「按研究问题找 test」+ references/cli_examples.md
Quick Menu），不调任何 LLM。

匹配策略（最具体优先，对应 meta-analysis classify 的确定性纪律）：
  1. 显式 test 名（ttest_ind / logrank / 两样本t检验 / …）权重最高。
  2. 修饰族词（非劣效 / 等效 / 优效 / 成组序贯 / 自适应 / 贝叶斯 / 聚类 …）
     命中时强烈倾向「修饰后」的 test（如「非劣效生存」→ ni_survival 而非 survival）。
  3. 终点类型词（连续均值 / 率 / 生存 / 诊断 / 计数）作为基础 test 依据。
  每条规则带特异性权重；最终取加权命中分最高的 test。

输出结构化 dict：
  {
    "test": "ttest_ind",
    "confidence": "high" | "medium" | "low",
    "matched": ["两样本", "t检验"],     # 命中的关键词（用于可解释性 / 审计）
    "candidates": ["ttest_ind", "ttest_paired"],
    "needs_llm_fallback": bool,        # 完全没命中任何规则 → True
    "missing": [],                      # 识别到终点但缺关键修饰时提示
    "notes": [],
  }
"""

from __future__ import annotations

import re

# ── 规则表 ─────────────────────────────────────────────────────────────────
# 每条：(test, [关键词], weight)。
# weight 越大越特异：修饰族 > 终点类型 > 泛义词。
# 关键词同时匹配中英文（IGNORECASE 对中文无副作用，对英文生效）。
RULES = [
    # ── 显式 test 名（最高权重，几乎一锤定音）──
    ("ttest_ind", [r"ttest_ind", r"两样本\s*t", r"独立\s*t", r"独立样本\s*t", r"独立样本", r"两独立样本", r"平行组.*均值", r"两样本t检验", r"两组.*均数", r"两组.*均值", r"两独立", r"独立两组", r"two[- ]?sample", r"t[- ]?test", r"independent"], 10),
    # v5.13.33 C：泛化「两组比较」降权至 4 + 负例——出现生存/率/卡方等终点词时禁用，
    # 防「两组 PFS 比较」「两组生存曲线比较」被抢成 t 检验（历史误判案例）。
    ("ttest_ind", [r"两组.*比较", r"两组.*对比"], 4,
     [r"生存", r"率", r"比例", r"卡方", r"χ2", r"PFS", r"OS\b", r"logrank", r"HR\b", r"风险比", r"无进展", r"总生存", r"死亡"]),
    # 基础连续终点（低权重兜底，对齐对话模式对泛化表述的推断：
    # 「两种降压药/收缩压下降…标准差」「血糖/胆固醇」等连续结局 → 两样本 t 检验）
    ("ttest_ind", [r"收缩压", r"舒张压", r"血糖", r"胆固醇",
                   r"两组.*(下降|降低|提高|升高|差异|差值|变化).*(标准差|sd)",
                   r"均数差", r"均值差"], 8),
    ("ttest_paired", [r"ttest_paired", r"配对\s*t", r"配对检验", r"2×2\s*交叉", r"交叉设计", r"paired"], 10),
    ("ttest_one", [r"ttest_one", r"单组\s*t", r"单样本\s*t", r"已知标准", r"one.sample", r"已知均值"], 10),
    ("anova", [r"anova", r"方差分析", r"多组", r"三组以上", r"三组比较", r"k组"], 10),
    ("proportion_two", [r"proportion_two", r"两比例", r"两率", r"两组率", r"率差", r"两样本率", r"卡方", r"卡方检验", r"χ2", r"chi[- ]?square", r"chi[- ]?squared"], 12),
    ("proportion_one", [r"proportion_one", r"单组率", r"单组比例", r"一组率"], 10),
    ("proportion_paired", [r"proportion_paired", r"配对率", r"mcnemar", r"前后率"], 10),
    ("odds_ratio", [r"odds_ratio", r"比值比", r"\bor\b", r"优势比"], 10),
    ("risk_ratio", [r"risk_ratio", r"风险比.*(率|比例)", r"相对危险度", r"\brr\b"], 10),
    ("non_inferiority", [r"non_inferiority", r"非劣效", r"非劣"], 10),
    ("superiority_margin", [r"superiority_margin", r"优效.*界", r"优效性.*margin"], 10),
    ("equivalence", [r"equivalence", r"等效性", r"等效检验.*均值"], 10),
    ("be_tost", [r"be_tost", r"生物等效", r"bioequivalence", r"tost", r"交叉.*be"], 10),
    ("survival", [r"logrank", r"生存分析", r"生存终点", r"风险比.*样本", r"survival"], 10),
    ("ni_survival", [r"非劣效.*生存", r"ni_survival", r"生存.*非劣", r"ni\s*生存", r"ni生存"], 12),
    ("survival_equivalence", [r"等效.*生存", r"survival_equivalence", r"生存等效"], 12),
    ("survival_superiority", [r"优效.*生存", r"survival_superiority", r"生存优效"], 12),
    ("survival_exact", [r"survival_exact", r"精确.*生存", r"生存.*精确"], 10),
    ("cox_covariate", [r"cox_covariate", r"cox.*协变量", r"cox回归", r"cox回归"], 10),
    ("survival_one_sample", [r"survival_one_sample", r"单样本.*指数", r"单组.*生存", r"单样本生存"], 10),
    ("competing_risks", [r"competing_risks", r"竞争风险", r"累积发生率"], 10),
    ("recurrent_events", [r"recurrent_events", r"复发事件", r"anderson", r"gill", r"重复事件"], 10),
    ("survival_historical", [r"survival_historical", r"历史对照.*logrank", r"历史对照生存"], 10),
    ("poisson", [r"poisson", r"泊松", r"发生率", r"计数资料"], 10),
    ("roc", [r"\broc\b", r"roc曲线", r"诊断试验", r"auc", r"判别"], 10),
    ("bland_altman", [r"bland_altman", r"bland", r"一致性", r"方法比较", r"方法学对比"], 10),
    ("cluster", [r"cluster", r"整群", r"聚类随机", r"cluster.random"], 10),
    ("vaccine_efficacy", [r"vaccine_efficacy", r"疫苗效力", r"ve\b", r"疫苗效价"], 10),
    ("multiple_endpoints", [r"multiple_endpoints", r"多重终点", r"复合终点", r"多个终点"], 10),
    ("bayesian", [r"bayesian", r"贝叶斯", r"bayes", r"先验"], 10),
    ("dose_escalation", [r"dose_escalation", r"剂量爬坡", r"phase\s*i", r"一期剂量", r"剂量递增"], 10),
    ("win_ratio", [r"win_ratio", r"win-ratio", r"胜率比", r"win比率"], 10),
    ("must_win", [r"must_win", r"must-win", r"共同主要", r"co-primary"], 10),
    ("historical_controls", [r"historical_controls", r"历史对照", r"历史数据借用", r"borrowing"], 10),
    ("mams", [r"mams", r"多臂多阶段", r"multi-arm", r"多臂"], 10),
    ("dunnett", [r"dunnett", r"多组比较.*dunnett", r"多重比较校正"], 10),
    ("mediation", [r"mediation", r"中介效应", r"中介分析"], 10),
    ("mixed_model", [r"mixed_model", r"混合模型", r"重复测量", r"纵向", r"mixed model", r"重复测量.*纵向"], 10),
    ("group_sequential", [r"group_sequential", r"成组序贯", r"期中分析", r"group sequential", r"interim"], 10),
    ("gsd_proportion", [r"成组序贯.*比例", r"gsd_proportion", r"组序贯.*率"], 12),
    ("gsd_survival", [r"成组序贯.*logrank", r"gsd_survival", r"组序贯.*生存",
                      r"期中分析.*生存", r"生存.*期中分析", r"interim.*surviv",
                      r"含.*期中.*生存"], 12),
    ("gsd_hazard", [r"成组序贯.*hr", r"gsd_hazard", r"组序贯.*风险比",
                    r"期中分析.*hr", r"hr.*期中分析", r"interim.*hazard"], 12),
    ("gsd_poisson", [r"成组序贯.*poisson", r"gsd_poisson", r"组序贯.*发生率"], 12),
    ("gsd_survival_sim", [r"成组序贯.*模拟", r"gsd_survival_sim", r"组序贯.*蒙特卡洛"], 12),
    ("gsd_hazard_sim", [r"成组序贯.*hr.*模拟", r"gsd_hazard_sim"], 12),
    ("adaptive", [r"adaptive", r"适应性设计", r"自适应", r"adaptive design"], 10),
    ("adaptive_simulate", [r"adaptive_simulate", r"蒙特卡洛.*仿真", r"模拟.*验证.*设计", r"adaptive.*sim"], 10),
    ("conditional_power", [r"conditional_power", r"条件功效", r"样本量再估计", r"ssr"], 10),
    ("assurance", [r"assurance", r"贝叶斯保证", r"assurance"], 10),
    # ── 非参数 Wilcoxon（NP1/NP2, v5.13.39）──
    # 显式 test 名/中英文标准名一锤定音；「秩和/符号秩/非参数」为族信号。
    # 负例防误抢：出现 logrank/生存分析等词时那是生存族，不抢；
    # 含「符号秩/signed-rank」时归符号秩检验，不抢通用秩和。
    ("wilcoxon_signed_rank", [r"wilcoxon.*符号秩", r"signed[- ]?rank", r"符号秩", r"配对.*秩"], 10),
    ("wilcoxon", [r"wilcoxon", r"mann[- ]?whitney", r"秩和", r"rank[- ]?sum"], 10,
     [r"符号秩", r"signed[- ]?rank", r"生存", r"logrank", r"PFS", r"OS\b", r"风险比", r"\bHR\b"]),
    ("wilcoxon", [r"非参数.*(样本量|检验|设计)", r"(样本量|检验|设计).*非参数", r"偏态.*(样本量|检验|设计)", r"中位数.*(标准误|四分位).*(样本量|检验|设计)"], 8),

    # ── 基础终点类型（低权重，作为兜底归并）──
    ("ttest_ind", [r"均值", r"均数", r"t\s*检验", r"连续变量", r"血压", r"hb[a1]?c", r"评分", r"连续结局"], 4),
    ("proportion_two", [r"率", r"比例", r"响应率", r"有效率"], 4),
    ("survival", [r"生存", r"事件", r"时间.*事件", r"无进展", r"总生存", r"pfs", r"os\b"], 4),
    ("poisson", [r"计数", r"发生率", r"率.*时间"], 4),
    ("mixed_model", [r"重复测量", r"纵向", r"mmrm"], 4),
]


# 族修饰词（命中显著提升对应「修饰后」test 的权重，已在 RULES 内用高 weight 体现）
_FAMILY_MODIFIERS = ["非劣效", "等效", "优效", "成组序贯", "适应性", "自适应",
                     "贝叶斯", "聚类", "历史对照", "多臂", "竞争风险", "复发"]


def _score_test(keywords, nl):
    """对一个 test 的关键词组打分：同义前缀重叠只计一次。

    例：「非劣效」同时命中关键词「非劣」与「非劣效」→ 仅计 1 次，避免基础 test
    （non_inferiority）因重复计分虚高，反向压过本应胜出的修饰 test（ni_survival）。
    机制：记录已计分的字符区间，新命中区间与既有区间重叠则跳过。
    """
    used_spans = []
    matched = []
    for kw in keywords:
        m = re.search(kw, nl, flags=re.IGNORECASE)
        if not m:
            continue
        span = m.span()
        # 与本 test 已计分区间重叠 → 同义重复，跳过
        if any(not (span[1] <= s[0] or span[0] >= s[1]) for s in used_spans):
            continue
        used_spans.append(span)
        matched.append(kw)
    return matched


def classify(nl, test_hint=None):
    """NL → test 结构化路由结果。test_hint 可选（上游已识别时的强信号）。"""
    nl = nl or ""
    scores = {}
    matched_by_test = {}

    # 1) 显式 test_hint 直接给最高置信
    if test_hint and re.search(r"^[a-z_]+$", test_hint or ""):
        return {
            "test": test_hint,
            "confidence": "high",
            "matched": ["<hint>%s" % test_hint],
            "candidates": [test_hint],
            "needs_llm_fallback": False,
            "missing": [],
            "notes": ["由上游显式 test_hint 直接路由"],
        }

    # 2) 关键词加权打分（同 test 同义关键词重叠仅计一次）
    #    同一 test 的得分取「最高单次权重」(max)，而非 weight*命中数 累加——
    #    避免基础终点词（如 survival 在 RULES 中双定义：显式「生存分析」w10 + 基础「生存」w4）
    #    多次命中累加虚高，反向压过更特异的修饰族（ni_survival w12 等）。
    for rule in RULES:
        test, keywords, weight = rule[0], rule[1], rule[2]
        neg = rule[3] if len(rule) > 3 else None
        if neg and any(re.search(n, nl, flags=re.IGNORECASE) for n in neg):
            continue    # v5.13.33 C：负例命中——泛化模式在该语境下禁用
        hits = _score_test(keywords, nl)
        if hits:
            scores[test] = max(scores.get(test, 0), weight)
            matched_by_test.setdefault(test, []).extend(hits)

    if not scores:
        return {
            "test": None,
            "confidence": "low",
            "matched": [],
            "candidates": [],
            "needs_llm_fallback": True,
            "missing": [],
            "notes": ["未从自然语言识别到任何已知 test 关键词，需 LLM 兜底或向用户追问终点类型"],
        }

    # 3) 取最高分；并列时取规则表中更靠前的（更特异）
    best = max(scores, key=lambda t: (scores[t], -RULES_ORDER.index(t) if t in RULES_ORDER else 0))
    best_score = scores[best]
    # 候选：分数 >= 最佳分 * 0.6 的都列出
    candidates = [t for t, s in scores.items() if s >= best_score * 0.6]
    candidates.sort(key=lambda t: -scores[t])

    confidence = "high" if best_score >= 12 else ("medium" if best_score >= 6 else "low")
    needs_llm = best_score < 6

    notes = []
    missing = []
    # 注：R 引擎 dispatch 的 65 个 test 均为具体设计（含 survival/logrank 等基础型），
    # 不再对基础终点词误报「缺设计族」；design_family 仅留给真正抽象、需追问的场景。

    return {
        "test": best,
        "confidence": confidence,
        "matched": matched_by_test.get(best, []),
        "candidates": candidates,
        "needs_llm_fallback": needs_llm,
        "missing": missing,
        "notes": notes,
    }


# RULES 中 test 出现顺序（best 并列时靠前优先 → 更特异规则先定义在前）
RULES_ORDER = [r[0] for r in RULES]


if __name__ == "__main__":
    import json
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else \
        "非劣效生存试验，NI界值1.25，期望HR=1.0，入组12个月随访12个月"
    print(json.dumps(classify(sample), ensure_ascii=False, indent=2))
