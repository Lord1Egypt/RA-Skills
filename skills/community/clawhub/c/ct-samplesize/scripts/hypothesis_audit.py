#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hypothesis_audit.py — 假设质量审计四分级 + 设计逻辑族选择 + fallback 场景规划
（ct-update upgrade J，v5.13.13，对标 CONSORT 2025 item 16a + ICH E9(R1) estimand +
 CDE《药物临床试验样本量估计指导原则（试行）》2024-12-23）

定位（与 assumption_block.py 的分工）：
  * assumption_block.py 回答「这次计算用了哪些参数、走没走默认」——**计算层**审计。
  * 本模块回答「每个设计假设的**证据强度**如何、设计逻辑族是否自洽、
    假设被推翻时**退路是什么**」——**方案规划层**审计，方案/SAP 撰写前使用。

四个能力：
  1. 四分级（grade）：逐个假设评定
       known        证据充分（历史数据/文献锚定/监管共识），可直接写入 SAP
       weak         有方向但量级不确定（如仅专家意见、外推的变异度），需灵敏度分析覆盖
       unknown      关键假设完全无依据（如首次在新适应症用该类终点），建议先做先导/适应性
       missing      该 test 逻辑上必需但用户未提供（会回退静默默认），必须补齐
  2. 设计逻辑族选择（family）：把 65 个 test 归入七个规划族，逐族给出「该族假设
     重心」提示，回答「我的整套假设在这个设计族里是否自洽」。
  3. fallback 场景规划（contingency）：按最脆弱的假设给出退路模板
     （事件数不足→延长随访/合并终点；ICC 超预期→加群；CV 高→中间再估样本量…），
     并标注哪些设计族天然支持期中重估（adaptive / group_sequential / assurance）。
  4. CONSORT 2025 合规检查表 + 监管就绪评分 + 引用推荐（v5.13.13 新增）：
      逐参数给出具体引文格式建议、CONSORT 2025 条目 16a 对齐检查、整体就绪量化评分。

纯标准库、零联网、不调 coze——规划层文本工作，不触动数值真相源。
可独立运行（--test 冒烟）；samplesize_power.py 在 --audit 下附加渲染。
"""
import argparse
import json
import sys


# ---------------------------------------------------------------------------
# 1) 假设维度定义：param -> (维度, 何时必需, known/weak 的证据标准)
# ---------------------------------------------------------------------------
ASSUMPTION_DIMS = {
    "effect":          ("效应量依据",     "求 n 时必需",
                        "prior RCT/荟萃给出的同类终点效应（CI 可报告）",
                        "仅专家共识、跨适应症外推、或预实验小样本 n<20"),
    # ── v5.13.39：非参数 Wilcoxon 维度（NP1/NP2）──
    "superiority":     ("随机优势依据",   "Wilcoxon 求 n 必需（与 median_diff 二选一）",
                        "既往同类试验报告的 P(优于) / Mann-Whitney 效应（如 OR→φ 折算带出处）",
                        "凭「中位数看着差不少」直觉拍值、或跨终点外推"),
    "median_diff":     ("位置差依据",     "Wilcoxon 求 n 必需（与 superiority 二选一，需配 sd）",
                        "既往研究报告中位数（IQR 可还原），差幅有 CI 或范围",
                        "单篇小样本中位数、或均数与中位数混用未核偏态"),
    "shape":           ("分布形状假设",   "median_diff 折算路径",
                        "有直方图/分位数支持 normal 或 logistic 假设",
                        "未核分布形态、默认 normal 但数据明显重尾"),
    "sd":              ("变异度依据",     "连续终点求 n 必需",
                        "同人群同检测方法的实测 SD（文献或≥30 例预实验）",
                        "不同人群/方法外推、或来源不明"),
    "p1":              ("对照率依据",     "两比例检验必需",
                        "本机构/注册库历史率（n≥200 观察）",
                        "文献异质率取均值、或凭经验估"),
    "p2":              ("试验率依据",     "两比例检验必需",
                        "同 effect 维度", "同 effect 维度"),
    "hazard_ratio":    ("HR 依据",        "生存优效必需",
                        "同类靶点已发表 HR（带 CI）",
                        "仅动物/替代终点外推"),
    "hr_expected":     ("HR 依据",        "NI 生存必需", "同 hazard_ratio", "同 hazard_ratio"),
    "lambda1":         ("事件率依据",     "生存参数化必需",
                        "本人群实测 Kaplan-Meier 或大型登记数据",
                        "跨线数/跨人群外推"),
    "lambda2":         ("事件率依据",     "生存参数化必需", "同 lambda1", "同 lambda1"),
    "event_rate":      ("事件率依据",     "事件驱动设计必需", "同 lambda1", "同 lambda1"),
    "margin":          ("界值依据",       "NI/EQ 必需",
                        "临床界值有 regulators/共识文档背书（如 FDA guidance 明文）",
                        "由「保留对照疗效 50%」类推导但未与临床委员会确认"),
    "ni_margin_surv":  ("界值依据",       "NI 生存必需", "同 margin", "同 margin"),
    "sup_margin":      ("界值依据",       "优效 margin 设计必需", "同 margin", "同 margin"),
    "win_ratio_theta": ("界值依据",       "win-ratio 必需", "同 margin", "同 margin"),
    "cv":              ("变异系数依据",   "BE 必需",
                        "制剂桥接预试验几何 CV（≥24 例交叉）",
                        "引用文献 CV 未核对制剂/人群一致"),
    "icc":             ("群内相关依据",   "cluster 必需",
                        "同类干预/人群发表 ICC（给出区间）",
                        "借用远缘领域 ICC 点值"),
    "k_groups":        ("结构参数",       "多组设计必需", "设计决定，无证据问题", "—"),
    "ratio":           ("结构参数",       "不等分配设计", "设计决定", "—"),
    "correlation":     ("相关结构依据",   "多重终点/配对必需",
                        "同人群实测相关（或文献带样本量）",
                        "假设值（0.5/0.7 等整数直觉值）"),
    "power":           ("监管预期",       "全部", "目标效能符合适应症监管惯例",
                        "无适应症参照随意取 0.8"),
    "alpha":           ("监管预期",       "全部", "按 ICH E9 单/双侧与 α 拆分明确", "—"),
    "sigma":           ("变异度依据",     "部分生存/纵向", "同 sd", "同 sd"),
    "dropout_rate":    ("脱落依据",       "全部（校正项）",
                        "同类试验实测脱落率",
                        "拍脑袋 5%/10% 惯例值"),
    "accrual_time":    ("可行性依据",     "生存/序贯必需",
                        "多中心启动计划+历史入组速率",
                        "线性外推乐观假设"),
    "followup_time":   ("可行性依据",     "生存必需", "同 accrual", "同 accrual"),
    "nsim":            ("计算精度",       "模拟法", "—", "—"),
    # ── v5.13.9：检验专属 dest 维度（与 REQUIRED_BY_TEST 对齐 catalog 真名）──
    "hr_exact":        ("HR 依据",        "生存精确法必需", "同 hazard_ratio", "同 hazard_ratio"),
    "cox_hr":          ("HR 依据",        "Cox 协变量必需", "同 hazard_ratio", "同 hazard_ratio"),
    "sup_hr":          ("HR 依据",        "生存优效 margin 必需", "同 hazard_ratio", "同 hazard_ratio"),
    "eq_margin_surv":  ("界值依据",       "生存等效必需", "同 margin", "同 margin"),
    "sup_margin_surv": ("界值依据",       "生存优效 margin 必需", "同 margin", "同 margin"),
    "theta0":          ("界值依据",       "BE 必需", "同 margin", "同 margin"),
    "ci_control":      ("累积发生率依据", "竞争风险必需",
                        "本人群累积发生率（Kaplan-Meier 带 CI）", "文献粗率直接挪用未核人群"),
    "ci_treatment":    ("累积发生率依据", "竞争风险必需", "同 ci_control", "同 ci_control"),
    "rate_control":    ("事件率依据",     "复发事件必需", "同 lambda1", "同 lambda1"),
    "rate_ratio":      ("效应量依据",     "复发事件必需",
                        "既往复发率比研究（带 CI）", "仅专家预期"),
    "new_median":      ("效应量依据",     "历史对照必需", "同 hazard_ratio", "同 hazard_ratio"),
    "median0":         ("效应量依据",     "单样本生存必需",
                        "本人群历史中位生存（登记数据）", "跨人群/跨线数外推"),
    "median1":         ("效应量依据",     "单样本生存必需",
                        "预期中位生存（先导数据/文献）", "拍定期望值"),
    "gs_rate1":        ("事件率依据",     "GSD Poisson 必需", "同 lambda1", "同 lambda1"),
    "gs_rate2":        ("事件率依据",     "GSD Poisson 必需", "同 lambda1", "同 lambda1"),
    "ve_control":      ("对照效力依据",   "疫苗必需", "同 p1", "同 p1"),
    "ve_treatment":    ("效应量依据",     "疫苗必需",
                        "预期保护效力（先导/文献带 CI）", "仅专家预期"),
    "varcorr":         ("相关结构依据",   "混合模型必需", "同 correlation", "同 correlation"),
    "sd_diff":         ("变异度依据",     "Bland-Altman 必需", "同 sd", "同 sd"),
    "effect_size":     ("效应量依据",     "自适应模拟必需", "同 effect", "同 effect"),
    "effect_must":     ("效应量依据",     "must-win 必需", "同 effect", "同 effect"),
    "effect_dunnett":  ("效应量依据",     "Dunnett 必需", "同 effect", "同 effect"),
    "delta_effect":    ("效应量依据",     "MAMS 必需", "同 effect", "同 effect"),
    "p_control_current": ("对照率依据",   "历史对照必需", "同 p1", "同 p1"),
    "historical_response": ("效应量依据", "历史对照必需", "同 hazard_ratio", "同 hazard_ratio"),
    "n_sim":           ("计算精度",       "模拟法", "—", "—"),
    "n_doses":         ("结构参数",       "剂量爬坡必需", "设计决定，无证据问题", "—"),
    "target_dlt":      ("结构参数",       "剂量爬坡必需", "协议既定 DLT 阈值", "—"),
}

# 各 test 的逻辑必需参数（missing 判定用；solve_for_power 方向不要求 nobs）
# v5.13.9：参数名与 params_catalog 逐检验对齐（diff 全 65 检验字段集修正）——
#   旧版沿用通用名（hazard_ratio/margin/theta1/lambda1/nsim…）而部分检验实际消费
#   检验专属 dest（hr_expected/hr_exact/cox_hr/eq_margin_surv/n_sim…），导致该检验
#   真实必填参数"被静默判 missing"→ 假 NOT_READY 误报。alpha/power 为全检验通用
#   监管预期参数，恒列入；可行性类（accrual/followup）仅在用户显式给出时评分。
REQUIRED_BY_TEST = {
    "_default": ["effect", "alpha", "power"],
    "ttest_ind": ["effect", "alpha", "power"],
    "ttest_one": ["effect", "alpha", "power"],
    "ttest_paired": ["effect", "alpha", "power"],
    "anova": ["effect", "alpha", "power", "k_groups"],
    "proportion_one": ["p1", "alpha", "power"],
    "proportion_two": ["p1", "p2", "alpha", "power"],
    "proportion_paired": ["p1", "p2", "alpha", "power"],
    "odds_ratio": ["p1", "alpha", "power"],
    "risk_ratio": ["p1", "alpha", "power"],
    "non_inferiority": ["effect", "margin", "alpha", "power"],
    "equivalence": ["effect", "sd", "alpha", "power"],
    "be_tost": ["cv", "theta0", "alpha", "power"],
    "survival": ["hazard_ratio", "alpha", "power"],
    "ni_survival": ["ni_margin_surv", "hr_expected", "alpha", "power"],
    "survival_exact": ["hr_exact", "alpha", "power"],
    "survival_equivalence": ["hr_expected", "eq_margin_surv", "alpha", "power"],
    "survival_superiority": ["sup_hr", "sup_margin_surv", "alpha", "power"],
    "cox_covariate": ["cox_hr", "alpha", "power"],
    "survival_one_sample": ["median0", "median1", "alpha", "power"],
    "competing_risks": ["ci_control", "ci_treatment", "alpha", "power"],
    "recurrent_events": ["rate_control", "rate_ratio", "alpha", "power"],
    "survival_historical": ["new_median", "hist_n", "alpha", "power"],
    "cluster": ["effect", "icc", "alpha", "power"],
    "poisson": ["lambda1", "lambda2", "alpha", "power"],
    "roc": ["auc0", "auc1", "alpha", "power"],
    "bland_altman": ["sd_diff", "w", "alpha", "power"],
    "mixed_model": ["effect", "varcorr", "alpha", "power"],
    "multiple_endpoints": ["effect", "correlation", "alpha", "power"],
    "vaccine_efficacy": ["ve_control", "ve_treatment", "alpha", "power"],
    "win_ratio": ["win_ratio_theta", "alpha", "power"],
    "must_win": ["effect_must", "n_endpoints_must", "alpha", "power"],
    "historical_controls": ["p_control_current", "historical_response", "alpha", "power"],
    "dose_escalation": ["target_dlt", "n_doses", "alpha"],
    "mams": ["n_arms_mams", "delta_effect", "alpha", "power"],
    "assurance": ["effect", "sd", "alpha"],
    "conditional_power": ["observed_effect", "planned_effect", "n_completed", "n_planned"],
    "group_sequential": ["effect", "alpha", "power"],
    "adaptive": ["effect", "alpha", "power"],
    "adaptive_simulate": ["effect_size", "alpha", "power"],
    "bayesian": ["effect", "sd", "alpha"],
    "gsd_proportion": ["p1", "p2", "alpha", "power"],
    "gsd_survival": ["hr_expected", "alpha", "power"],
    "gsd_hazard": ["hr_expected", "alpha", "power"],
    "gsd_poisson": ["gs_rate1", "gs_rate2", "alpha", "power"],
    "gsd_survival_sim": ["hr_expected", "alpha", "power", "n_sim"],
    "gsd_hazard_sim": ["hr_expected", "alpha", "power", "n_sim"],
    "dunnett": ["effect_dunnett", "n_groups_dunnett", "alpha", "power"],
    "mediation": ["effect", "alpha", "power"],
    "superiority_margin": ["effect", "sup_margin", "alpha", "power"],
    # 非参数 Wilcoxon（NP1/NP2, v5.13.39）：superiority 与 median_diff 二选一，
    # 审计时按「用户实际提供的那个」判 known/weak（见 _audit_params 的 or 语义）
    "wilcoxon": ["superiority", "median_diff", "sd", "shape", "alpha", "power"],
    "wilcoxon_signed_rank": ["superiority", "median_diff", "sd", "shape", "alpha", "power"],
}


# ---------------------------------------------------------------------------
# 2) 设计逻辑族（七个规划族；65 test 全覆盖归族）
# ---------------------------------------------------------------------------
DESIGN_FAMILIES = {
    "经典平行两组比较": {
        "tests": ["ttest_ind", "ttest_paired", "proportion_two", "odds_ratio",
                  "risk_ratio", "proportion_paired", "bland_altman",
                  "wilcoxon", "wilcoxon_signed_rank"],
        "assumption_focus": "效应量与变异度是唯一定盘星：两者的历史证据强度直接决定 n 可信度",
        "questions": [
            "效应量假设若向下修正 20%，样本量增幅是否仍在预算内？",
            "SD/率的历史数据与目标人群（线数、人群特征）是否同分布？",
            "Wilcoxon：中位数差的历史证据是否充分？偏态程度是否支持放弃正态近似？"],
    },
    "非劣效与等效": {
        "tests": ["non_inferiority", "equivalence", "be_tost", "ni_survival",
                  "survival_equivalence", "superiority_margin"],
        "assumption_focus": "界值(margin)是法律性假设、效应量是科学假设——两者必须分别独立论证",
        "questions": [
            "margin 是否有临床委员会/监管沟通纪要背书？",
            "若真实效应≈0，设计是否仍要在统计上区分「不劣」与「等效」？"],
    },
    "生存与事件驱动": {
        "tests": ["survival", "survival_exact", "survival_superiority", "cox_covariate",
                  "survival_one_sample", "competing_risks", "recurrent_events",
                  "survival_historical", "gsd_survival", "gsd_survival_sim",
                  "gsd_hazard", "gsd_hazard_sim", "poisson", "gsd_poisson"],
        "assumption_focus": "n 只是表象，事件数才是本质：HR、事件率、入组与随访窗四者互相锁死",
        "questions": [
            "目标事件数在计划随访窗内可达吗？历史入组速率支持吗？",
            "若事件率低于预期，延长随访 vs 追加例数 vs 合并终点的优先级？"],
    },
    "群随机与多层次": {
        "tests": ["cluster", "mixed_model", "multiple_endpoints", "dunnett", "anova",
                  "ttest_one", "proportion_one", "mediation"],
        "assumption_focus": "结构参数（ICC/相关/组数）的误差被非线性放大：ICC 0.01→0.05 可令 n 翻数倍",
        "questions": [
            "ICC 取值区间上下限分别对应什么样本量？",
            "群数与群内例数哪个更经济（增大 m 边际收益递减）？"],
    },
    "序贯与自适应": {
        "tests": ["group_sequential", "adaptive", "adaptive_simulate", "mams",
                  "conditional_power", "dose_escalation", "assurance", "bayesian",
                  "gsd_proportion"],
        "assumption_focus": "把『假设不确定』内化为设计特性：预留重估/停止节点，α 拆分是代价",
        "questions": [
            "中期重估的触发规则（效应阈值/无效性边界）写进 SAP 了吗？",
            "α 消耗函数选择（OBF/Pocock）与 DSMB 盲态审阅流程是否一致？"],
    },
    "诊断与方法比较": {
        "tests": ["roc", "vaccine_efficacy", "win_ratio", "must_win"],
        "assumption_focus": "判别/效力阈值是临床决策点而非统计量：AUC 界值、保护效力线须前置锁定",
        "questions": [
            "目标灵敏度/特异度对应的临床使用场景明确吗？",
            "win-ratio 的序次定义（死亡优先？）会根本改变结论，是否经临床确认？"],
    },
    "历史对照与借用": {
        "tests": ["historical_controls", "survival_historical"],
        "assumption_focus": "同质性论证是前提：人群/标准治疗/评价时点任一漂移都使借用失效",
        "questions": [
            "外部对照与本试验人群的协变量分布差异做过敏感性模拟吗？",
            "借用比例（Bayesian 先验强度）与监管可接受度沟通了吗？"],
    },
}

_FAMILY_OF = {}
for _fam, _d in DESIGN_FAMILIES.items():
    for _t in _d["tests"]:
        _FAMILY_OF[_t] = _fam


# unknown 档启发式「整数直觉值」特征：显式给值恰好等于教科书占位值，
# 高度疑似无据拍定（如 d=0.5、SD=1、r=0.5~0.9、ICC=0.05）。命中 → unknown，
# 建议先做先导/敏感性；未命中 → weak（有值但证据待补）。人工可 override。
FABRICATION_SIGNATURES = {
    "effect": {0.5, 0.3, 0.8},          # Cohen medium/small/large 直觉值
    "sd": {1.0},                        # 标准化占位
    "correlation": {0.5, 0.6, 0.7, 0.8, 0.9},
    "icc": {0.05},
    "p1": {0.5},
}


def _looks_fabricated(param, value):
    sigs = FABRICATION_SIGNATURES.get(param)
    if not sigs or value is None:
        return False
    try:
        return float(value) in sigs
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------------------
# 3) fallback 场景规划模板：按最脆弱假设维度给退路
# ---------------------------------------------------------------------------
FALLBACKS = {
    "效应量依据": [
        "样本量预算内可承受的最大效应折减（-20%）即为本设计的稳健边界；超出则改为适应性中期重估样本量",
        "若审计判为 weak：把该假设列入方案『假设与灵敏度』章节，附 ±1 SE 的 n 曲线（power_seq/effect_seq 曲线模式即产出）"],
    "随机优势依据": [
        "φ 无历史锚时，从既往 OR/RR 反算 P(优于)（如 OR=2 → φ≈0.64），或做 ≥20 对配对预实验直接估 φ",
        "φ 每降 0.02，n 约增 15%~20%：按 φ-0.05 情景单列一列样本量，主分析按预设 φ"],
    "位置差依据": [
        "中位数差若来自单篇小样本，改用 IQR/分位数还原的稳健差幅；偏态严重时优先换 Wilcoxon 并同时报 φ 与 Δ 双口径",
        "Δ 与 σ 必须同源（同研究同人群）：跨研究拼凑 Δ 与 σ 是静默错参高发点，审计标 weak 时以敏感性区间出数"],
    "变异度依据": [
        "预实验扩展至 ≥30 例重估 SD，或以外部数据元分析合并方差；持续不确定时改用成组序贯在中期合并实际方差",
        "若审计判为 weak：申请预算按 SD 上界（+25%）配置，主分析按预设 SD，差异写入 SAP 附表"],
    "对照率依据": [
        "对照率若不可靠，考虑内部随机对照替代外部锚定，或设最小对照例数下限（保证率的 CI 宽度可控）"],
    "试验率依据": [
        "同效应量维度退路：以差值（而非两率分别）作为假设载体，减少单点率估计误差传导"],
    "HR 依据": [
        "延长随访或事件富集（入组高危表型）替代盲目加例；预设『事件数驱动』而非『日历时间驱动』的分析时点"],
    "事件率依据": [
        "入组速率与事件率双假设耦合：以事件数为 stopping rule 主约束，日历时间为辅；随访窗预留一次官方延长选项"],
    "界值依据": [
        "界值未与监管/临床达成书面共识前不锁定 n：先提交 pre-ICE/审评沟通，界值定稿后再计算（否则整本方案数字失去意义）"],
    "变异系数依据": [
        "BE：预试验 CV 若来自不同制剂平台，用参考制剂重现性数据替代，或放宽等效界值申请（须监管同意）"],
    "群内相关依据": [
        "ICC 上界情景的样本量单独成列（cluster 敏感性表）；现场监测期做中期 ICC 盲态核查，超界即加群而非加群内例数"],
    "相关结构依据": [
        "相关系数不确定时按最不利值（相关最高）配置样本量；多重终点优先用 graphical α 回收（mult_alloc）换取效能"],
    "监管预期": [
        "效能目标低于适应症惯例（肿瘤<80%）会引发审评质疑；升档样本量或改优效设计二选一，事先与评审沟通"],
    "脱落依据": [
        "脱落率假设失准的退路是延长入组窗（保护事件/例数）而非事后放大 n；SAP 预注册『脱落监测规则』（超假设 1.5 倍触发 DSMB 评估）"],
    "可行性依据": [
        "入组/随访假设落空：预设滚动启动（分阶段中心开放）与随访窗一次性官方延长条款，两者都写入方案的 contingency 章节"],
    "计算精度": [
        "模拟类设计（adaptive/gsd_sim）nsim 不足时 MC 误差可与效应量假设误差同量级——先补 nsim 再谈假设"],
}


# ---------------------------------------------------------------------------
# 4) 参数→推荐引用格式（v5.13.13 新增）
# ---------------------------------------------------------------------------
_CITATION_FORMATS = {
    "effect": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告同类终点效应量，带 95% CI】",
        "example": "Smith A et al. (2023). Efficacy of X in Y population. Lancet 401:123-130. 【报告 Z 人群终点 W 的效应量 Δ=5.2 (95% CI 3.1–7.3)】",
    },
    "sd": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告同人群同方法实测 SD，带样本量】",
        "example": "Jones B et al. (2022). Variability of endpoint W in population Z. J Clin Epidemiol 145:88-95. 【n=120, SD=12.5, 测量方法：___】",
    },
    "p1": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告对照率，带观察例数】",
        "example": "Brown C et al. (2023). Event rate in control arm. NEJM 389:456-465. 【n=300/1500=20.0%, 多中心, 随访 12 月】",
    },
    "hazard_ratio": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告 HR，带 95% CI 与中位生存】",
        "example": "Wilson D et al. (2024). Survival outcomes with X vs Y. JCO 42:789-798. 【HR=0.65 (95% CI 0.52–0.81), 中位 OS 18.2 vs 12.5 月】",
    },
    "margin": {
        "format": "监管文档 / 临床共识文件编号 + 条款；或已发表界值论证研究",
        "example": "FDA Guidance (2016) Section III.B: 保留对照疗效≥50% 推导 δ=4.0；或 EMA CHMP Guideline (2005) Appendix 2",
    },
    "icc": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告同类干预/人群 ICC，带区间】",
        "example": "Adams E et al. (2021). ICC for cluster designs in X trials. Trials 22:123. 【ICC=0.03 (95% CI 0.01–0.08), 同类干预/人群】",
    },
    "cv": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告制剂桥接预试验 CV，带例数与方法】",
        "example": "Lee F et al. (2023). BE study of X formulation. Clin Pharmacol Ther 114:345-352. 【n=48 交叉, CV=23.5%, 制剂: ___】",
    },
    "dropout_rate": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告同类试验实测脱落率，带脱落原因分布】",
        "example": "Taylor G et al. (2022). Attrition in X trials: a systematic review. Clin Trials 19:234-243. 【加权脱落率 8.2%, 主要脱落原因：失访/退出/AE】",
    },
    "correlation": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告同人群实测相关系数，带样本量】",
        "example": "Martin H et al. (2023). Correlation between endpoints in X disease. Stat Med 42:567-578. 【r=0.62, n=150, Pearson/Spearman】",
    },
    "power": {
        "format": "ICH E9 / 监管指导原则；或适应症常规",
        "example": "ICH E9 (1998) Section 3.1: 确证性试验效能通常不低于 80%；肿瘤适应症惯例 90%",
    },
    "event_rate": {
        "format": "Author (Year). Title. Journal Volume:Pages. 【报告本人群实测事件率或大型登记数据】",
        "example": "National Registry (2024). Annual report of X disease. 【n=5000, 12 月事件率 15.3%; 或 KM 估计】",
    },
}

# ---------------------------------------------------------------------------
# 5) CONSORT 2025 条目 16a 合规检查表（v5.13.13 新增）
# ---------------------------------------------------------------------------
_CONSORT_16A_ITEMS = [
    ("主终点定义", "主要终点明确定义（评估变量/汇总度量/时点/分析人群）"),
    ("各组假设值", "每组的结局值假设（连续=均率；二分类=率；生存=HR/事件率）"),
    ("目标差值", "组间目标差值 + 依据（MCID/文献/监管共识）"),
    ("标准差", "连续终点的共同标准差（来源引用）"),
    ("检验水准", "α（单/双侧）+ 多重性校正（如适用）"),
    ("检验效能", "目标效能（1-β）+ 适应症常规依据"),
    ("校正项", "脱落/不依从/群集/不等分配校正"),
    ("软件版本", "计算软件 + 版本号 + 方法/R代码"),
    ("期中分析", "期中分析计划 + α 消耗函数（如适用）"),
]

# ===========================================================================
# 英文层（v5.13.36）：审计块中英双语，跟随 language
#   language="bilingual"（默认）→ 中文（English）；"en"→纯英；"zh"→纯中
#   与论证段（justify_text）一致：无论界面语言，审计块都提供英文。
# ===========================================================================
def _cell(zh, en, lang):
    """表格单元格级双语。"""
    if lang == "en":
        return en
    if lang == "zh":
        return zh
    return "%s（%s）" % (zh, en)


def _branch(zh, en, bi, lang):
    """结构化行（标题/表头/引用行）级双语；bi 为 bilingual 专用串。"""
    if lang == "en":
        return en
    if lang == "zh":
        return zh
    return bi


# 维度名 → 英文（key 与 ASSUMPTION_DIMS 维度列一致）
_DIM_NAME_EN = {
    "效应量依据": "Effect-size basis",
    "变异度依据": "Variability basis",
    "对照率依据": "Control-rate basis",
    "试验率依据": "Treatment-rate basis",
    "HR 依据": "HR basis",
    "事件率依据": "Event-rate basis",
    "界值依据": "Margin basis",
    "变异系数依据": "CV basis",
    "群内相关依据": "ICC basis",
    "结构参数": "Structural parameter",
    "相关结构依据": "Correlation basis",
    "监管预期": "Regulatory expectation",
    "脱落依据": "Attrition basis",
    "可行性依据": "Feasibility basis",
    "计算精度": "Computation precision",
    "累积发生率依据": "Cumulative-incidence basis",
    "对照效力依据": "Control-efficacy basis",
    "未归类参数": "Uncategorized parameter",
}

# param → (known 证据标准 EN, weak 特征 EN)；仅覆盖常用参数，其余留空
_ASSUMPTION_EN = {
    "effect": ("Prior RCT/meta effect on the same endpoint (CI reported)",
               "Expert opinion / cross-indication extrapolation / small pilot n<20"),
    "effect_size": ("Prior RCT/meta effect on the same endpoint (CI reported)",
                    "Expert opinion / cross-indication extrapolation / small pilot n<20"),
    "observed_effect": ("Prior RCT/meta effect on the same endpoint (CI reported)",
                        "Expert opinion / cross-indication extrapolation / small pilot n<20"),
    "planned_effect": ("Prior RCT/meta effect on the same endpoint (CI reported)",
                       "Expert opinion / cross-indication extrapolation / small pilot n<20"),
    "sd": ("Measured SD in the same population & method (lit or pilot n>=30)",
           "Extrapolated from a different population/method, or unknown source"),
    "sigma": ("Measured SD in the same population & method (lit or pilot n>=30)",
              "Extrapolated from a different population/method, or unknown source"),
    "p1": ("Institution/registry historic rate (n>=200 observations)",
           "Heterogeneous literature mean, or rule-of-thumb"),
    "hazard_ratio": ("Published HR for the same target (with CI)",
                     "Only animal/surrogate extrapolation"),
    "hr_expected": ("Published HR for the same target (with CI)",
                    "Only animal/surrogate extrapolation"),
    "event_rate": ("This-population Kaplan-Meier or large registry",
                   "Cross-line/cross-population extrapolation"),
    "lambda1": ("This-population Kaplan-Meier or large registry",
                "Cross-line/cross-population extrapolation"),
    "margin": ("Regulator/consensus document backing (e.g. FDA guidance text)",
               "Derived from 'retain >=50% control efficacy', unconfirmed by clinical committee"),
    "ni_margin_surv": ("Regulator/consensus document backing (e.g. FDA guidance text)",
                       "Derived from 'retain >=50% control efficacy', unconfirmed by clinical committee"),
    "cv": ("Geometric CV from a BE pilot (>=24 crossover)",
           "Cited literature CV without verifying formulation/population match"),
    "icc": ("Published ICC for a similar intervention/population (with interval)",
            "Borrowed point ICC from a distant field"),
    "correlation": ("Measured correlation in the same population (or lit with n)",
                    "Assumed value (0.5/0.7 etc.)"),
    "power": ("Target power matches indication practice",
              "0.8 chosen without an indication reference"),
    "alpha": ("ICH E9 single/double-sided and alpha split explicit", "-"),
    "dropout_rate": ("Measured attrition in similar trials",
                     "Arbitrary 5%/10% convention"),
    "accrual_time": ("Multi-site startup plan + historical accrual rate",
                     "Linear optimistic extrapolation"),
    "followup_time": ("Multi-site startup plan + historical accrual rate",
                      "Linear optimistic extrapolation"),
}

# 设计逻辑族 assumption_focus / questions → 英文（key 与 DESIGN_FAMILIES 一致）
DESIGN_FAMILIES_EN = {
    "经典平行两组比较": {
        "assumption_focus": "Effect size and variability are the only deciding stars: their historical evidence strength directly sets the credibility of n.",
        "questions": [
            "If the effect-size assumption is revised down by 20%, does the sample-size increase still fit the budget?",
            "Do the historical SD/rate data come from the same distribution as the target population (line of therapy, characteristics)?"],
    },
    "非劣效与等效": {
        "assumption_focus": "The margin is a legal assumption, the effect is a scientific one - both must be justified independently.",
        "questions": [
            "Is the margin backed by a clinical-committee / regulatory-communication record?",
            "If the true effect is ~0, does the design still statistically distinguish 'non-inferior' from 'equivalent'?"],
    },
    "生存与事件驱动": {
        "assumption_focus": "n is superficial; the event count is the essence: HR, event rate, and accrual/follow-up windows are mutually locked.",
        "questions": [
            "Is the target event count reachable within the planned follow-up window (supported by historical accrual)?",
            "If the event rate is lower than expected, what is the priority: extend follow-up vs add subjects vs combine endpoints?"],
    },
    "群随机与多层次": {
        "assumption_focus": "Errors in structural parameters (ICC/correlation/group count) are nonlinearly amplified: ICC 0.01->0.05 can multiply n several-fold.",
        "questions": [
            "What sample sizes correspond to the upper/lower bounds of the ICC range?",
            "Which is more economical: more clusters or more subjects per cluster (diminishing returns)?"],
    },
    "序贯与自适应": {
        "assumption_focus": "Internalize 'assumption uncertainty' as a design feature: reserve re-estimation/stopping nodes; the alpha split is the cost.",
        "questions": [
            "Is the interim re-estimation trigger rule (effect threshold / futility boundary) written into the SAP?",
            "Is the alpha-spending function choice (OBF/Pocock) consistent with the DSMB blinded-review process?"],
    },
    "诊断与方法比较": {
        "assumption_focus": "Discrimination/efficacy thresholds are clinical decision points, not statistics: the AUC threshold and protection-efficacy line must be locked upfront.",
        "questions": [
            "Is the clinical use scenario behind the target sensitivity/specificity clear?",
            "Will the win-ratio ordinal definition (death first?) fundamentally change the conclusion - clinically confirmed?"],
    },
    "历史对照与借用": {
        "assumption_focus": "The homogeneity argument is a prerequisite: any drift in population/SoC/assessment time invalidates borrowing.",
        "questions": [
            "Have covariate-distribution differences vs the external control been sensitivity-simulated?",
            "Is the borrowing fraction (Bayesian prior strength) communicated with regulators?"],
    },
}

# fallback 维度 → 英文（key 与 FALLBACKS 一致）
FALLBACKS_EN = {
    "效应量依据": [
        "The maximum tolerable effect reduction (-20%) within budget is this design's robustness boundary; beyond it, switch to adaptive interim sample-size re-estimation.",
        "If graded weak: list the assumption in the SAP 'Assumptions & Sensitivity' section with a +/-1 SE n-curve (power_seq/effect_seq curve mode produces it)."],
    "变异度依据": [
        "Extend the pilot to >=30 subjects to re-estimate SD, or meta-analyze variance from external data; if uncertainty persists, use group-sequential to merge actual variance at interim.",
        "If graded weak: budget by the SD upper bound (+25%), analyze by the preset SD, and document the difference in an SAP appendix."],
    "对照率依据": [
        "If the control rate is unreliable, consider internal randomization instead of external anchoring, or set a minimum control sample-size floor (to keep the rate's CI width controllable)."],
    "试验率依据": [
        "Same fallback as the effect-size dimension: use the difference (not the two rates separately) as the assumption carrier, reducing single-rate estimation error propagation."],
    "HR 依据": [
        "Extend follow-up or enrich events (enroll high-risk phenotype) instead of blindly adding subjects; preset an 'event-count-driven' (not calendar-time-driven) analysis timepoint."],
    "事件率依据": [
        "Accrual-rate and event-rate assumptions are coupled: use the event count as the primary stopping-rule constraint, calendar time secondary; reserve one official follow-up-window extension."],
    "界值依据": [
        "Do not lock n until the margin is in written consensus with regulators/clinical: submit pre-IND/communication first; recompute after the margin is finalized (otherwise the whole protocol's numbers lose meaning)."],
    "变异系数依据": [
        "BE: if the pilot CV comes from a different formulation platform, substitute reference-formulation reproducibility data, or apply for a relaxed equivalence margin (requires regulator approval)."],
    "群内相关依据": [
        "List the ICC-upper-bound sample size as a separate column (cluster sensitivity table); do a blinded interim ICC check during monitoring - if exceeded, add clusters not within-cluster subjects."],
    "相关结构依据": [
        "When correlation is uncertain, size by the worst case (highest correlation); for multiple endpoints prefer graphical alpha-recovery (mult_alloc) to recover power."],
    "监管预期": [
        "A power target below the indication convention (oncology <80%) invites agency queries; either up-size or switch to superiority - communicate with reviewers beforehand."],
    "脱落依据": [
        "The fallback for an inaccurate dropout rate is extending the accrual window (protecting events/subjects), not post-hoc inflating n; pre-register a 'dropout monitoring rule' in the SAP (trigger DSMB review at >1.5x assumed)."],
    "可行性依据": [
        "If accrual/follow-up assumptions fail: preset a rolling start (phased site opening) and a one-time official follow-up-window extension clause - both written into the contingency section."],
    "计算精度": [
        "For simulation designs (adaptive/gsd_sim), insufficient nsim makes the MC error comparable to the effect-size assumption error - fix nsim before discussing assumptions."],
}

# 引用推荐 → 英文（key 与 _CITATION_FORMATS 一致）
_CITATION_FORMATS_EN = {
    "effect": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the same-endpoint effect with 95% CI]",
        "example": "Smith A et al. (2023). Efficacy of X in Y population. Lancet 401:123-130. [delta=5.2 (95% CI 3.1-7.3) for endpoint W in population Z]"},
    "sd": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the measured SD in the same population & method, with n]",
        "example": "Jones B et al. (2022). Variability of endpoint W in population Z. J Clin Epidemiol 145:88-95. [n=120, SD=12.5, method: ___]"},
    "p1": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the control rate with the number observed]",
        "example": "Brown C et al. (2023). Event rate in the control arm. NEJM 389:456-465. [300/1500=20.0%, multicenter, 12-mo follow-up]"},
    "hazard_ratio": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the HR with 95% CI and median survival]",
        "example": "Wilson D et al. (2024). Survival outcomes with X vs Y. JCO 42:789-798. [HR=0.65 (95% CI 0.52-0.81), median OS 18.2 vs 12.5 mo]"},
    "margin": {
        "format": "Regulatory document / clinical-consensus document number + clause; or a published margin-justification study",
        "example": "FDA Guidance (2016) Section III.B: retain >=50% control efficacy -> delta=4.0; or EMA CHMP Guideline (2005) Appendix 2"},
    "icc": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the ICC for a similar intervention/population, with interval]",
        "example": "Adams E et al. (2021). ICC for cluster designs in X trials. Trials 22:123. [ICC=0.03 (95% CI 0.01-0.08), similar intervention/population]"},
    "cv": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the BE-pilot CV with n and method]",
        "example": "Lee F et al. (2023). BE study of X formulation. Clin Pharmacol Ther 114:345-352. [n=48 crossover, CV=23.5%, formulation: ___]"},
    "dropout_rate": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the measured attrition in similar trials, with the reason distribution]",
        "example": "Taylor G et al. (2022). Attrition in X trials: a systematic review. Clin Trials 19:234-243. [weighted attrition 8.2%, main reasons: loss-to-follow-up/withdrawal/AE]"},
    "correlation": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the measured correlation in the same population, with n]",
        "example": "Martin H et al. (2023). Correlation between endpoints in X disease. Stat Med 42:567-578. [r=0.62, n=150, Pearson/Spearman]"},
    "power": {
        "format": "ICH E9 / regulatory guidance; or the indication convention",
        "example": "ICH E9 (1998) Section 3.1: confirmatory-trial power is usually >=80%; oncology convention 90%"},
    "event_rate": {
        "format": "Author (Year). Title. Journal Volume:Pages. [Report the measured event rate in this population or large registry]",
        "example": "National Registry (2024). Annual report of X disease. [n=5000, 12-mo event rate 15.3%; or KM estimate]"},
}

# CONSORT 16a → 英文（与 _CONSORT_16A_ITEMS 按位置对应）
_CONSORT_16A_ITEMS_EN = [
    ("Primary endpoint definition", "Primary endpoint clearly defined (variable / summary measure / timepoint / analysis population)"),
    ("Assumed values per arm", "Outcome-value assumptions per arm (continuous=mean; binary=rate; survival=HR/event rate)"),
    ("Target difference", "Between-group target difference + basis (MCID/literature/regulatory consensus)"),
    ("Standard deviation", "Common SD for continuous endpoints (source cited)"),
    ("Type I error", "alpha (one/two-sided) + multiplicity adjustment (if applicable)"),
    ("Power", "Target power (1-beta) + indication-convention basis"),
    ("Correction terms", "Attrition/non-compliance/cluster/unequal-allocation correction"),
    ("Software version", "Computation software + version + method / R code"),
    ("Interim analysis", "Interim analysis plan + alpha-spending function (if applicable)"),
]

# 监管就绪等级 → 英文
_GRADE_DESC_EN = {
    "A": "Ready - proceed directly to SAP writing & submission",
    "B": "Basically ready - weak assumptions need sensitivity analysis",
    "C": "Conditionally ready - strengthen evidence or switch to an adaptive design first",
    "D": "Not ready - critical assumptions missing; pilot study or redesign needed",
}

# 设计逻辑族名 → 英文（key 与 DESIGN_FAMILIES 一致）
_FAMILY_NAME_EN = {
    "经典平行两组比较": "Classic two-group parallel comparison",
    "非劣效与等效": "Non-inferiority & equivalence",
    "生存与事件驱动": "Survival & event-driven",
    "群随机与多层次": "Cluster-randomized & multilevel",
    "序贯与自适应": "Sequential & adaptive",
    "诊断与方法比较": "Diagnostic & method comparison",
    "历史对照与借用": "Historical control & borrowing",
    "未归族（用默认必需参数集）": "Uncategorized (default required-parameter set)",
}

# 总体判定说明 → 英文（按 overall 代码，%d 占位数在 render 时填）
_OVERALL_NOTE_EN = {
    "NOT_READY": "%d required assumption(s) missing (will silently use defaults) — fill them in before computing, otherwise the result is not auditable",
    "ADAPTIVE_RECOMMENDED": "Evidence is generally thin: prefer a sequential/adaptive family (reserving re-estimation nodes), or run a pilot study first",
    "READY_WITH_SENSITIVITY": "Computable, but %d weak assumption(s) must be accompanied by a sensitivity analysis (curve mode yields ±20% scenarios)",
    "READY": "All key assumptions are known/structural — proceed directly to computation and SAP writing",
}

# known 档 rationale → 英文（含 %s 的动态值在 audit_hypotheses 已格式化，匹配不到的走 fallback）
_RATIONALE_EN = {
    "设计自定参数，无外部证据依赖": "Design-determined; no external evidence needed",
    "取默认值": "Default value",
    "人工复核回填（agent/统计师确认）": "Manual override (agent/statistician confirmed)",
    "该 test 逻辑必需但完全未提供（无值可算）": "Required by this test but not provided (no value to compute)",
    "显式给出且等于监管/ICH 常规值（α 0.05|0.025, power 0.8|0.9）":
        "Explicitly given and equals the regulatory/ICH convention (alpha 0.05|0.025, power 0.8|0.9)",
    "偏离惯例值，需适应症依据或审评沟通支撑":
        "Deviates from the convention; needs an indication basis or agency communication",
    "沿用默认惯例值未经显式确认（SAP 应写明 α/效能设定依据）":
        "Inherited the default convention without explicit confirmation (the SAP should state the alpha/power basis)",
    "使用工具默认值（%s），未显式确认": "Tool default (%s), not explicitly confirmed",
    "取值恰为常见『拍脑袋』占位值（无据特征），建议先导研究或文献锚定":
        "Value matches a textbook placeholder (fabrication signature); a pilot study or literature anchoring is advised",
    "已给数值但未附历史证据来源；按证据标准（%s）可升为 known":
        "Value given but no historical source; can be upgraded to known per the standard (%s)",
    "已声明证据来源（--evidence-source）": "Evidence source declared (--evidence-source)",
}

# ---------------------------------------------------------------------------
# 审计引擎
# ---------------------------------------------------------------------------
def _param_state(args, dests, k):
    """返回 (present, explicit)：参数是否可用、是否显式给出（≠默认）。"""
    if k not in dests:
        return False, False
    v = getattr(args, k, None)
    present = v is not None
    return present, present  # 上层再用 parser.get_default 判 explicit


def audit_hypotheses(args, test, parser, grades_override=None):
    """对一次样本量规划做三层审计。

    Parameters
    ----------
    args   : argparse.Namespace  已解析参数（samplesize_power 的 parser）
    test   : str | None          检验类型
    parser : argparse.ArgumentParser
    grades_override : dict|None  人工复核后的分级修正 {param: grade}（供 agent 访谈后回填）

    Returns
    -------
    dict: {test, family, grades:[{param,dimension,value,grade,evidence_standard,rationale}],
           summary:{known,weak,unknown,missing}, family_questions:[...],
           contingencies:[{weak_dimension, fallbacks:[...]}], overall}
    """
    dests = {a.dest for a in parser._actions}
    req = REQUIRED_BY_TEST.get(test or "", REQUIRED_BY_TEST["_default"])
    override = grades_override or {}

    grades, counters = [], {"known": 0, "weak": 0, "unknown": 0, "missing": 0}
    # 收集要评的参数：test 必需参数 ∪ 用户显式给过的证据类参数
    evidence_params = set(req)
    for k in list(ASSUMPTION_DIMS):
        if k in dests and k not in evidence_params:
            v = getattr(args, k, None)
            d = parser.get_default(k)
            if v is not None and (d is None or v != d):
                evidence_params.add(k)   # 用户主动给了证据参数也要评

    for k in sorted(evidence_params):
        dim, when, std_known, std_weak = ASSUMPTION_DIMS.get(
            k, ("未归类参数", "可选", "—", "—"))
        present = k in dests and getattr(args, k, None) is not None
        default = parser.get_default(k) if k in dests else None
        value = getattr(args, k, None) if k in dests else None
        explicit = present and (default is None or value != default)

        if k in override:
            grade = override[k]
            rationale = "人工复核回填（agent/统计师确认）"
        elif dim in ("结构参数", "计算精度"):
            grade = "known"
            rationale = "设计自定参数，无外部证据依赖" if explicit else "取默认值"
        elif value is None:
            # v5.13.39：Wilcoxon 效应输入互斥路径——superiority 直给 与
            # median_diff+sd 折算二选一。未选路径的参数不得判 missing
            # （否则用户只给 superiority 也会假 NOT_READY 误报）。
            if test in ("wilcoxon", "wilcoxon_signed_rank") and k in ("superiority", "median_diff", "sd"):
                sup_ok = getattr(args, "superiority", None) is not None
                md_ok = getattr(args, "median_diff", None) is not None
                sd_ok = getattr(args, "sd", None) is not None
                if sup_ok and k != "superiority":
                    grade = "known"
                    rationale = "superiority 直给路径生效，折算类参数（median_diff/sd）不参与计算"
                elif md_ok and sd_ok and k == "superiority":
                    grade = "known"
                    rationale = "median_diff+sd 折算路径生效，superiority 直给路径未选用"
                elif md_ok and not sd_ok and k == "sd":
                    grade, rationale = "missing", "median_diff 折算路径缺少 sd（分布尺度）——仅给中位数差无法折算随机优势，引擎将报错"
                elif not sup_ok and not md_ok and k in ("superiority", "median_diff"):
                    grade, rationale = "missing", "两条效应输入路径均未提供：需 superiority（随机优势）或 median_diff+sd（中位数差+尺度）"
                elif md_ok and not sd_ok and k == "superiority":
                    grade, rationale = "missing", "折算路径缺 sd 不完整、superiority 也未给——补任一路径即可"
                else:
                    grade, rationale = "missing", "该 test 逻辑必需但完全未提供（无值可算）"
            else:
                grade, rationale = "missing", "该 test 逻辑必需但完全未提供（无值可算）"
        elif dim == "监管预期":
            # α/power 惯例豁免：值等于监管常规值 → known；偏离且未声明 → weak
            conv = {"alpha": (0.025, 0.05), "power": (0.8, 0.9)}
            if explicit and value in conv.get(k, ()):
                grade, rationale = "known", "显式给出且等于监管/ICH 常规值（α 0.05|0.025, power 0.8|0.9）"
            elif explicit:
                grade, rationale = "weak", "偏离惯例值，需适应症依据或审评沟通支撑"
            else:
                grade, rationale = "weak", "沿用默认惯例值未经显式确认（SAP 应写明 α/效能设定依据）"
        elif not explicit:
            # 有默认值但用户未显式确认的证据类参数 → weak（默认参与计算）
            grade, rationale = "weak", "使用工具默认值（%s），未显式确认" % value
        else:
            # 显式给出：本地无法自动判定证据真伪。先过「整数直觉值」启发式，
            # 命中即 unknown（无据拍定嫌疑）；未命中默认 weak；附来源可升 known。
            src = (getattr(args, "evidence_source", None) or "") if "evidence_source" in dests else ""
            if src and k in src:
                grade, rationale = "known", "已声明证据来源（--evidence-source）"
            elif _looks_fabricated(k, value):
                grade, rationale = "unknown", "取值恰为常见『拍脑袋』占位值（无据特征），建议先导研究或文献锚定"
            else:
                grade, rationale = "weak", "已给数值但未附历史证据来源；按证据标准（%s）可升为 known" % std_known
        counters[grade] += 1
        grades.append({"param": k, "dimension": dim, "value": value, "grade": grade,
                       "known_standard": std_known, "weak_sign": std_weak,
                       "rationale": rationale})

    fam = _FAMILY_OF.get(test or "", None)
    fam_block = DESIGN_FAMILIES.get(fam, {})

    # fallback：按本次审计中最脆弱维度（weak/unknown/missing 的证据类维度）给退路
    weakest_dims = [g["dimension"] for g in grades if g["grade"] in ("weak", "unknown", "missing")
                    and g["dimension"] in FALLBACKS]
    seen, contingencies = set(), []
    for d in weakest_dims:
        if d in seen:
            continue
        seen.add(d)
        contingencies.append({"weak_dimension": d, "fallbacks": FALLBACKS[d]})

    # 总体判定：missing>0 → 不可直接出数；仅 weak → 出数但必须配灵敏度；全 known → 就绪
    if counters["missing"] > 0:
        overall = "NOT_READY"
        overall_note = "存在 %d 个必需假设缺失（将静默走默认）——先补齐再出数，否则结果不可审计" % counters["missing"]
    elif counters["unknown"] > 0 or counters["weak"] >= 3:
        overall = "ADAPTIVE_RECOMMENDED"
        overall_note = "假设证据普遍薄弱：优先改序贯/自适应族（预留重估节点），或先做先导研究"
    elif counters["weak"] > 0:
        overall = "READY_WITH_SENSITIVITY"
        overall_note = "可出数，但 %d 个 weak 假设须随结果附灵敏度分析（曲线模式产出 ±20%% 情景）" % counters["weak"]
    else:
        overall = "READY"
        overall_note = "全部关键假设为 known/结构参数——直接进入计算与 SAP 撰写"

    return {
        "test": test,
        "family": fam or "未归族（用默认必需参数集）",
        "family_assumption_focus": fam_block.get("assumption_focus", ""),
        "family_questions": fam_block.get("questions", []),
        "grades": grades,
        "summary": counters,
        "contingencies": contingencies,
        "overall": overall,
        "overall_note": overall_note,
    }


def _readiness_score(report):
    """计算监管就绪量化评分（v5.13.13 新增）。

    评分逻辑：
      - 基础分 = 100
      - missing 每个 -15（最高扣至 0）
      - unknown 每个 -10
      - weak 每个 -5
      - 全 known → 100
      - 90+ / 70-89 / 50-69 / <50 对应 A/B/C/D 四级
    """
    s = report["summary"]
    score = 100 - s["missing"] * 15 - s["unknown"] * 10 - s["weak"] * 5
    if score < 0:
        score = 0
    if score >= 90:
        grade = "A"
        desc = "就绪 — 可直接撰写 SAP 提交"
    elif score >= 70:
        grade = "B"
        desc = "基本就绪 — weak 假设需附灵敏度分析"
    elif score >= 50:
        grade = "C"
        desc = "条件就绪 — 建议先补强证据或改用自适应设计"
    else:
        grade = "D"
        desc = "不就绪 — 关键假设缺失，需先导研究或重新设计"
    return score, grade, desc


def render_text(report, language="bilingual"):
    """中英双语渲染（v5.13.36）。language:
       "bilingual"（默认）→ 中文（English）；"en"→纯英；"zh"→纯中。
       与论证段（justify_text）一致：审计块始终提供英文。"""
    L = language
    zh_g = {"known": "✔ known 有据", "weak": "△ weak 薄弱",
            "unknown": "✗ unknown 无据", "missing": "⚠ missing 未给（静默默认）"}
    en_g = {"known": "✔ known (evidenced)", "weak": "△ weak (thin)",
            "unknown": "✗ unknown (no basis)", "missing": "⚠ missing (silent default)"}
    score, grade, desc = _readiness_score(report)
    desc_en = _GRADE_DESC_EN.get(grade, "")
    fam_en = _FAMILY_NAME_EN.get(report["family"], report["family"])
    _ov = report["overall"]
    _onote_en = _OVERALL_NOTE_EN.get(_ov, report["overall_note"])
    if "%d" in _onote_en:
        _cnt = report["summary"]["missing"] if _ov == "NOT_READY" else report["summary"].get("weak", 0)
        _onote_en = _onote_en % _cnt
    lines = []
    lines.append(_branch(
        "## 假设质量审计 / Hypothesis Audit (upgrade J, v5.13.13)",
        "## Hypothesis Audit (upgrade J, v5.13.13)",
        "## 假设质量审计 / Hypothesis Audit (upgrade J, v5.13.13)", L))
    lines.append(_branch(
        "检验类型: **%s** ｜ 设计逻辑族: **%s** ｜ 总体判定: **%s — %s** ｜ 监管就绪评分: **%d/100 (%s) — %s**"
        % (report["test"], report["family"], report["overall"], report["overall_note"],
           score, grade, desc),
        "Test: **%s** | Design family: **%s** | Overall: **%s — %s** | Regulatory readiness: **%d/100 (%s) — %s**"
        % (report["test"], fam_en, report["overall"], _onote_en,
           score, grade, desc_en),
        "检验类型: **%s** ｜ 设计逻辑族: **%s** ｜ 总体判定: **%s — %s** ｜ 监管就绪评分: **%d/100 (%s) — %s** ／ Test: **%s** | Family: **%s** | Overall: **%s — %s** | Readiness: **%d/100 (%s) — %s**"
        % (report["test"], report["family"], report["overall"], report["overall_note"],
           score, grade, desc,
           report["test"], fam_en, report["overall"], _onote_en,
           score, grade, desc_en), L))
    if report["family_assumption_focus"]:
        en_focus = DESIGN_FAMILIES_EN.get(report["family"], {}).get("assumption_focus", "")
        lines.append(_branch(
            "> 本族假设重心：%s" % report["family_assumption_focus"],
            "> Assumption focus of this family: %s" % en_focus,
            "> 本族假设重心：%s ／ Assumption focus: %s" % (report["family_assumption_focus"], en_focus), L))
    s = report["summary"]
    lines.append(_branch(
        "### 1. 四分级明细（known %s / weak %s / unknown %s / missing %s）"
        % (s["known"], s["weak"], s["unknown"], s["missing"]),
        "### 1. Graded details (known %s / weak %s / unknown %s / missing %s)"
        % (s["known"], s["weak"], s["unknown"], s["missing"]),
        "### 1. 四分级明细 / Graded details (known %s / weak %s / unknown %s / missing %s)"
        % (s["known"], s["weak"], s["unknown"], s["missing"]), L))
    lines.append(_branch(
        "| 参数 | 假设维度 | 值 | 分级 | 判定依据 / known 证据标准 |",
        "| Param | Dimension | Value | Grade | Evidence standard |",
        "| 参数 Param | 假设维度 Dimension | 值 Value | 分级 Grade | 判定依据 / Evidence standard |", L))
    lines.append("|---|---|---|---|---|")
    for g in report["grades"]:
        val = "—" if g["value"] is None else g["value"]
        if g["grade"] == "known":
            std_zh, std_en = g["rationale"], _RATIONALE_EN.get(g["rationale"], "Confirmed / as stated")
        elif g["grade"] == "missing":
            std_zh = g["rationale"]
            std_en = _RATIONALE_EN.get(g["rationale"], "Required by this test but not provided")
        else:  # weak / unknown
            std_zh, std_en = g["known_standard"], _ASSUMPTION_EN.get(g["param"], ("", ""))[0]
        d_en = _DIM_NAME_EN.get(g["dimension"], "")
        lines.append("| %s | %s | %s | %s | %s |" % (
            g["param"],
            _cell(g["dimension"], d_en, L),
            val,
            _cell(zh_g.get(g["grade"], g["grade"]), en_g.get(g["grade"], g["grade"]), L),
            _cell(std_zh, std_en, L)))
    if report["family_questions"]:
        lines.append(_branch("\n### 2. 族内自洽性核查问题\n", "\n### 2. Internal consistency questions\n",
                             "\n### 2. 族内自洽性核查问题 / Internal consistency questions\n", L))
        en_qs = DESIGN_FAMILIES_EN.get(report["family"], {}).get("questions", [])
        for i, q in enumerate(report["family_questions"]):
            eq = en_qs[i] if i < len(en_qs) else ""
            lines.append(_cell("- %s" % q, "- %s" % eq, L))
    if report["contingencies"]:
        lines.append(_branch("\n### 3. Fallback 场景规划（按最脆弱假设）\n",
                             "\n### 3. Fallback scenario planning (by weakest assumption)\n",
                             "\n### 3. Fallback 场景规划 / Scenario planning (by weakest assumption)\n", L))
        for c in report["contingencies"]:
            en_fb = FALLBACKS_EN.get(c["weak_dimension"], [])
            lines.append(_branch(
                "**%s** 假设失准时：" % c["weak_dimension"],
                "**%s** assumption fails:" % c["weak_dimension"],
                "**%s** 假设失准时 / assumption fails:" % c["weak_dimension"], L))
            for j, fb in enumerate(c["fallbacks"]):
                ef = en_fb[j] if j < len(en_fb) else ""
                lines.append(_cell("  - %s" % fb, "  - %s" % ef, L))
    else:
        lines.append(_branch(
            "\n### 3. Fallback 场景规划\n\n- 无薄弱假设，暂无需预注册退路。",
            "\n### 3. Fallback scenario planning\n\n- No weak assumptions; no pre-registered fallback needed.",
            "\n### 3. Fallback 场景规划 / Scenario planning\n\n- 无薄弱假设，暂无需预注册退路。/ No weak assumptions; no pre-registered fallback needed.", L))
    lines.append(_branch("\n### 4. CONSORT 2025 条目 16a 合规检查表\n",
                         "\n### 4. CONSORT 2025 item 16a compliance checklist\n",
                         "\n### 4. CONSORT 2025 条目 16a 合规检查表 / item 16a compliance checklist\n", L))
    for i, (item, desc_item) in enumerate(_CONSORT_16A_ITEMS, 1):
        ei = _CONSORT_16A_ITEMS_EN[i - 1] if i - 1 < len(_CONSORT_16A_ITEMS_EN) else ("", "")
        lines.append(_branch(
            "%d. □ %s — %s" % (i, item, desc_item),
            "%d. □ %s — %s" % (i, ei[0], ei[1]),
            "%d. □ %s — %s ／ %s — %s" % (i, item, desc_item, ei[0], ei[1]), L))
    weak_unk = [g for g in report["grades"] if g["grade"] in ("weak", "unknown")
                and g["param"] in _CITATION_FORMATS]
    if weak_unk:
        lines.append(_branch("\n### 5. 弱/未知假设的引用推荐（提升为 known 的具体引文格式）\n",
                             "\n### 5. Citation recommendations for weak/unknown assumptions\n",
                             "\n### 5. 弱/未知假设的引用推荐 / Citation recommendations (to upgrade to known)\n", L))
        for g in weak_unk:
            cf = _CITATION_FORMATS[g["param"]]
            cfe = _CITATION_FORMATS_EN.get(g["param"], {"format": "", "example": ""})
            d_en = _DIM_NAME_EN.get(g["dimension"], "")
            lines.append(_branch(
                "**%s**（%s）：" % (g["param"], g["dimension"]),
                "**%s** (%s):" % (g["param"], d_en),
                "**%s**（%s / %s）：" % (g["param"], g["dimension"], d_en), L))
            lines.append(_cell("  推荐格式：%s" % cf["format"], "  Format: %s" % cfe["format"], L))
            lines.append(_cell("  示例：%s" % cf["example"], "  Example: %s" % cfe["example"], L))
    else:
        lines.append(_branch(
            "\n### 5. 引用推荐\n\n- 所有假设均已标注已知来源，无需额外引用推荐。",
            "\n### 5. Citation recommendations\n\n- All assumptions are already tagged with known sources; no extra citation needed.",
            "\n### 5. 引用推荐 / Citation recommendations\n\n- 所有假设均已标注已知来源，无需额外引用推荐。/ All assumptions are already tagged with known sources; no extra citation needed.", L))
    lines.append(_branch("\n### 6. 监管就绪量化评分\n", "\n### 6. Regulatory readiness score\n",
                         "\n### 6. 监管就绪量化评分 / Regulatory readiness score\n", L))
    lines.append(_branch("| 维度 | 数值 |", "| Dimension | Value |", "| 维度 Dimension | 数值 Value |", L))
    lines.append("|---|---|")
    lines.append(_cell("| 总分 | %d / 100 |" % score, "| Total | %d / 100 |" % score, L))
    lines.append(_cell("| 等级 | %s — %s |" % (grade, desc), "| Grade | %s — %s |" % (grade, desc_en), L))
    lines.append(_cell("| 评分逻辑 | missing×15 + unknown×10 + weak×5 扣分；最低 0 |",
                       "| Scoring | missingx15 + unknownx10 + weakx5 deducted; floor 0 |", L))
    lines.append(_branch(
        "\n> 评分说明：90+ = A 就绪 / 70-89 = B 基本就绪 / 50-69 = C 条件就绪 / <50 = D 不就绪。",
        "\n> Scoring: 90+ = A ready / 70-89 = B basically ready / 50-69 = C conditionally ready / <50 = D not ready.",
        "\n> 评分说明：90+ = A 就绪 / 70-89 = B 基本就绪 / 50-69 = C 条件就绪 / <50 = D 不就绪。/ Scoring: 90+ = A ready / 70-89 = B basically ready / 50-69 = C conditionally ready / <50 = D not ready.", L))
    lines.append(_branch(
        "> 评分目的：辅助研究者识别证据薄弱环节，不替代统计师/监管专家判断。",
        "> Purpose: help researchers spot weak-evidence links; not a substitute for statistician/regulator judgment.",
        "> 评分目的：辅助研究者识别证据薄弱环节，不替代统计师/监管专家判断。/ Purpose: help researchers spot weak-evidence links; not a substitute for statistician/regulator judgment.", L))
    lines.append(_branch(
        "\n> 本审计为**规划层**文本评估，不参与数值计算；分级可经 agent 访谈或统计师复核后用 grades_override 回填修正。输出供方案/SAP 撰写参考，非监管意见。",
        "\n> This audit is a **planning-layer** textual assessment, not part of numeric computation; grades can be corrected via grades_override after an agent interview or statistician review. Output is for protocol/SAP drafting, not a regulatory opinion.",
        "\n> 本审计为**规划层**文本评估，不参与数值计算；分级可经 agent 访谈或统计师复核后用 grades_override 回填修正。输出供方案/SAP 撰写参考，非监管意见。/ This audit is a **planning-layer** textual assessment, not part of numeric computation; grades can be corrected via grades_override after an agent interview or statistician review. Output is for protocol/SAP drafting, not a regulatory opinion.", L))
    return "\n".join(lines)


def _main():
    ap = argparse.ArgumentParser(description="假设质量审计四分级（独立冒烟）")
    ap.add_argument("--test", default="ttest_ind")
    ap.add_argument("--alpha", type=float, default=None)
    ap.add_argument("--power", type=float, default=None)
    ap.add_argument("--effect", type=float, default=None)
    ap.add_argument("--sd", type=float, default=None)
    ap.add_argument("--hazard-ratio", dest="hazard_ratio", type=float, default=None)
    ap.add_argument("--margin", type=float, default=None)
    ap.add_argument("--icc", type=float, default=None)
    ap.add_argument("--evidence-source", default="",
                     help="已附历史证据来源的参数名清单（逗号分隔），命中者升 known")
    ap.add_argument("--json", dest="as_json", action="store_true")
    a = ap.parse_args()
    ov = {}
    if a.evidence_source:
        for p in a.evidence_source.split(","):
            if p.strip():
                ov[p.strip()] = "known"
    rep = audit_hypotheses(a, a.test, ap, grades_override=ov)
    if a.as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render_text(rep))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
