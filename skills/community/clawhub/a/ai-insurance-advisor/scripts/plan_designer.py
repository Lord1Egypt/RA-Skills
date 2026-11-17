#!/usr/bin/env python3
"""
方案设计工具
根据需求分析结果，自动生成2-3套方案（基础版/标准版/全面版）

🆕 2026-10-27 计算口径修正（收入/预算）+ 预算硬约束
   1) I2 预算硬约束：新增 _enforce_budget(plan, budget, annual_income)。
      保费上限口径统一为 min(年度预算, 年收入 × 档位比例)：
        基础版 10% / 标准版 15% / 全面版 20%
      超预算时先按比例下调最后加入产品的保额（下限 = 产品 min_coverage，
      无 min_coverage 时用原保额 60%），用同一 calculate_product_premium 重算；
      仍超预算则按档位顺序移除可选险种（基础版 医疗险→意外险；标准/全面版 意外险→医疗险）。
      每次调整写入 plan["budget_adjustments"]。
      基础版：意外险保费校验改用 budget（不再是 budget * 1.2），
              医疗险加入前必须校验累计保费 ≤ budget。
   2) I3 产品池与 premium_calculator.py 对齐：默认不推荐已停售/已下架产品
      （探查结论见 premium_calculator.py 顶部注释）。
      china 版原已有部分过滤（is_active / is_duplicate / delisting_time == 已停售 /
      data_quality == garbage），本次统一为同一判定口径。
   3) 每个方案输出 budget_planning 块（年度保费上限 / 方案年保费 / 占年收入比 /
      是否在预算内 / 说明）。
   保费计算公式本身未改动。
"""

import json
import math
import os
import re
import sys
import unicodedata

# ---------------------------------------------------------------------------
# 产品有效性判定（与 premium_calculator.py 同一口径）
#
# references/products.json 字段取值分布探查结论（2536 款）：
#   is_active          : True 603 / False 1933
#   validity_status    : 已停售 1897 / DISCONTINUED 80 / 在售新品 222 / 在售老品 176
#                        / 在售常规 116 / MODIFIED 17 / VALID 5 / SKIPPED 4
#                        / 信息缺失 3 / 字段缺失 16
#   delisting_time     : "已停售" 1880 / "仍在售" 454 / 日期串(YYYY 或 YYYY-MM) 57
#                        / "待核实" 37 / 缺失或 null 108
#   data_quality       : garbage 37 / 其余无此字段
#   is_duplicate       : True 56 / False 68 / 字段缺失 2412
# 判定：is_active is False 或 validity_status ∈ {已停售, DISCONTINUED}
#       或 delisting_time == "已停售" 或 delisting_time 为日期串 → 视为已停售/已下架。
# 三条信号并集排除 2017 款；剩余 519 款再剔除 garbage 37 + duplicate 1 → 481 款进入产品池。
# ---------------------------------------------------------------------------
_RE_DELIST_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


def _is_product_discontinued(product):
    """产品是否已停售/已下架（基于真实字段分布判定）。"""
    if product.get("is_active") is False:
        return True
    if product.get("validity_status") in ("已停售", "DISCONTINUED"):
        return True
    delisting = str(product.get("delisting_time") or "").strip()
    if delisting == "已停售":
        return True
    if delisting and _RE_DELIST_DATE.match(delisting):
        return True
    return False


def _is_product_eligible(product, include_discontinued=False):
    """产品是否可进入推荐池。"""
    if not include_discontinued and _is_product_discontinued(product):
        return False
    if product.get("data_quality") == "garbage":
        return False
    if product.get("is_duplicate") is True:
        return False
    return True


# ---------------------------------------------------------------------------
# 医疗险续保条款派生（ClawHub 安全审计整改 2026-11-07 · SDI-4）
#
# 背景：旧实现用「子串包含」选品，并在**任何**选中的产品上都写死
#       "coverage_period": "保证续保20年"。兜底分支可能选到
#       coverage_period_guaranteed_renewable=False 的产品（如「1年（可续保）」），
#       却仍对外宣称「保证续保20年」→ 续保条款虚假陈述。
#
# 现在：选品与展示字段**一律按产品真实字段派生**：
#   - coverage_period_guaranteed_renewable : 是否保证续保（bool）
#   - coverage_period_duration_value/unit : 保证续保年限（数值 + 单位）
#   - coverage_period                      : 原始保险期间文本
#   - coverage_period_is_lifetime          : 是否终身
# 无合格产品时**如实报告限制**，不替换任意产品却宣称保证续保20年。
# ---------------------------------------------------------------------------

# 产品库解析器写入的权威保证续保年限标记：'guaranteed_renewable_20年' / 'guaranteed_renewable_6年'
_RE_GUARANTEED_YEARS = re.compile(r"guaranteed_renewable_(\d+)\s*年")
# 长期保证续保标记
_RE_LONG_TERM_MARK = re.compile(r"long_term_with_guaranteed_renewable")


def _parse_notes_list(product):
    """返回产品库解析标记列表（统一成 list[str]）。"""
    notes = product.get("coverage_period_parse_notes")
    if notes is None:
        return []
    if isinstance(notes, str):
        return [notes]
    if isinstance(notes, (list, tuple)):
        return [str(n) for n in notes]
    return []
# ---------------------------------------------------------------------------

def _renewal_duration_years(product):
    """返回该产品保证续保的年限（年）。无法确定时返回 None。

    判定口径（**只用结构化字段**，不做子串猜测）：
      1. `coverage_period_parse_notes` 是产品库解析器写入的**权威标记**：
         - 'guaranteed_renewable_20年' → 20
         - 'guaranteed_renewable_6年'  → 6
         - 'long_term_with_guaranteed_renewable' → None（长期，不按年限计）
         ⚠️ 该标记**优先于** duration_value：实测有 14 款「1年（保证续保20年）」的
         duration_value=1（保险期间 1 年），但保证续保期是 20 年 —— 只看
         duration_value 会把 20 年保证续保误判成 1 年。
      2. 次选 `coverage_period_duration_unit == 'year'` → 取 `coverage_period_duration_value`。
      3. `coverage_period_duration_unit == 'long_term'` → None（长期）。
      4. `coverage_period_is_lifetime is True` → None（终身）。
    """
    notes = _parse_notes_list(product)
    # ⚠️ SDI-4 整改 2026-11-10（v2.4.1）：**必须分两轮扫描，且 long_term 轮在前**。
    #
    # 审计原文：「The loop returns immediately upon finding a numeric renewal marker,
    # so a later long-term marker never receives its documented precedence.
    # For example, notes ordered as ['guaranteed_renewable_1年',
    # 'long_term_with_guaranteed_renewable'] cause the tool to report one-year
    # guaranteed renewal rather than long-term guaranteed renewal, making
    # customer-facing insurance advice depend on list order.」
    #
    # 修法：**先扫完整张 notes 列表找 long_term 标记**（只要有一个就返回 None，
    # 长期保证续保不按年限计）；**没有 long_term 标记时**再扫数值型标记。
    # → 结果不再依赖 notes 的排列顺序。
    for note in notes:
        if _RE_LONG_TERM_MARK.search(note):
            return None
    for note in notes:
        m = _RE_GUARANTEED_YEARS.search(note)
        if m:
            return int(m.group(1))

    if product.get("coverage_period_is_lifetime") is True:
        return None
    unit = (product.get("coverage_period_duration_unit") or "").strip().lower()
    if unit == "long_term":
        # 单位本身就是 long_term → 长期，不按年限计
        return None
    value = product.get("coverage_period_duration_value")
    if unit == "year" and isinstance(value, (int, float)):
        return int(value)
    return None


def _is_guaranteed_renewable(product):
    """产品是否明确标注「保证续保」。"""
    return product.get("coverage_period_guaranteed_renewable") is True


def _has_long_term_renewal(product):
    """产品是否带长期保证续保（long_term 单位、解析标记或终身）。"""
    for note in _parse_notes_list(product):
        if _RE_LONG_TERM_MARK.search(note):
            return True
    if product.get("coverage_period_is_lifetime") is True:
        return True
    unit = (product.get("coverage_period_duration_unit") or "").strip().lower()
    return unit == "long_term"


def select_medical_product(products, min_guaranteed_years=None, prefer=None):
    """按真实续保字段选医疗险。

    Args:
        products: 候选医疗险列表。
        min_guaranteed_years: 要求的最低保证续保年限（如 20）。None = 不要求。
        prefer: 可选的选品偏好函数（如按 core_coverage 含 '600' 选 600 万产品）。

    Returns:
        tuple[dict|None, dict|None]: (选中产品, 未满足要求时的限制说明)
            第二个元素为 None 表示选品成功满足要求。
    """
    candidates = [p for p in products if p.get("type") == "医疗险"]
    if not candidates:
        return None, {
            "reason": "产品库中没有在售医疗险，无法在方案中加入医疗保障。",
            "requirement": None,
        }

    # 第 1 优先：满足「保证续保 ≥ N 年」的（结构化字段判定，非子串匹配）
    if min_guaranteed_years:
        qualified = [
            p for p in candidates
            if _is_guaranteed_renewable(p)
            and (_renewal_duration_years(p) is not None
                 and _renewal_duration_years(p) >= min_guaranteed_years
                 or _has_long_term_renewal(p))
        ]
        if qualified:
            chosen = prefer(qualified) if prefer else qualified[0]
            return chosen, None

        # 无合格产品 → 如实报告限制，**不**替换为任意产品
        guaranteed_any = [p for p in candidates if _is_guaranteed_renewable(p)]
        if guaranteed_any:
            best_years = max(
                (_renewal_duration_years(p) or 0) for p in guaranteed_any
            )
            limitation = {
                "reason": (
                    f"产品库中无满足「保证续保{min_guaranteed_years}年」的在售医疗险；"
                    f"现有保证续保医疗险的最高保证续保年限为 {best_years} 年。"
                ),
                "requirement": f"保证续保{min_guaranteed_years}年",
                "fallback_product": None,
            }
        else:
            limitation = {
                "reason": (
                    f"产品库中无任何标明保证续保的在售医疗险，"
                    f"无法满足「保证续保{min_guaranteed_years}年」的要求。"
                ),
                "requirement": f"保证续保{min_guaranteed_years}年",
                "fallback_product": None,
            }
        # 兜底选品：按真实字段选一款**确实带保证续保（年限不足）**的产品；
        # 若连保证续保的都没有，则选续保条件最清晰的一款，并如实标注。
        fallback_pool = guaranteed_any or [
            p for p in candidates if _is_guaranteed_renewable(p)
        ] or candidates
        fallback = prefer(fallback_pool) if prefer else fallback_pool[0]
        limitation["fallback_product"] = fallback.get("name")
        return fallback, limitation

    # 无年限要求：优先带保证续保的
    guaranteed = [p for p in candidates if _is_guaranteed_renewable(p)]
    pool = guaranteed or candidates
    chosen = prefer(pool) if prefer else pool[0]
    return chosen, None


def derive_medical_coverage_period(product):
    """从产品真实字段派生医疗险的 `coverage_period` 展示文本。"""
    if not product:
        return "未明确"
    raw = product.get("coverage_period")
    if _is_guaranteed_renewable(product):
        years = _renewal_duration_years(product)
        if years is not None:
            return f"{years}年保证续保"
        if _has_long_term_renewal(product):
            return "长期保证续保"
        return "保证续保"
    if raw:
        return raw
    return "未明确"


def derive_medical_key_benefits(product, base_benefits, coverage_period=None):
    """从产品真实字段派生医疗险的 `key_benefits` 展示文本。

    续保描述**只陈述产品自身字段所载的事实**，不套用与实际条款不符的年限。
    """
    benefits = base_benefits
    if not product:
        return benefits
    # ⚠️ SDI-4 残余整改 2026-11-13：治疗手段**只认产品真实字段**
    #    （key_benefits 元素 + highlights 字符串）；base 文本里不得再写死。
    benefits = f"{benefits}{_medical_treatment_suffix(product)}"
    if _is_guaranteed_renewable(product):
        years = _renewal_duration_years(product)
        if years is not None:
            return f"{benefits}，{years}年保证续保"
        if _has_long_term_renewal(product):
            return f"{benefits}，长期保证续保"
        return f"{benefits}，保证续保"
    # 无保证续保：不得使用「保证续保N年」措辞；如实表述为「续保条件以产品条款为准」
    return f"{benefits}，续保条件以产品条款为准"


# ----------------------------------------------------------------------
# 医疗险对外宣称的事实源派生（SDI-4 残余整改 2026-11-13）
#
# 官方 ClawHub 2.4.6 复扫 finding（SDI-4 · MEDIUM · 置信 0.99）：
#   「The comprehensive plan assigns the claim "质子重离子与 CAR-T 治疗" to the
#     selected medical product without verifying those benefits against its actual terms.」
#
# 根因：key_benefits 的 base 文本**写死**了「质子重离子与 CAR-T 治疗」
#      「不限社保」「进口药/靶向药均可报销」等治疗手段 → 与选中产品的真实条款无关；
#      选品只查「类型 + 续保」，从不校验治疗手段是否被该产品真实条款授权。
#
# 修法：治疗手段**只认产品真实字段**；无授权就不宣称（如实降级，不虚构卖点）。
# ----------------------------------------------------------------------
_TREATMENT_CLAIMS = ("质子重离子", "CAR-T", "靶向药", "外购药", "特药", "进口药")

# ---------------------------------------------------------------------------
# 否定语境判定（SDI-4 官方 2.4.7 复扫整改 · 2026-11-14）
#
# 官方 finding（scanner 2.12.0 · SDI-4 · Excessive Agency · MEDIUM · 置信 0.99）：
#   「Treatment claims are presented as covered benefits based on keyword presence,
#     even when the source excludes them.」
#
# 根因：v2.4.7 引入的 `_medical_treatment_claims` 只判「关键词是否出现」，
#      **不判**「这次出现是否被条款排除」→ 「不含CAR-T」「质子重离子不予报销」
#      也会被转成「，含CAR-T治疗」的**承保宣称**。
#
# 修法：**逐次出现**判定 —— 每次出现都取上下文窗口判断是否落在否定/除外语境；
#      同一关键词若全部出现皆为否定 → 不计入 claims；
#      存在非否定出现 → 计入（肯定 + 否定并存仍算有授权）。
#
# ⚠️ 2026-11-17 官方 2.4.15 复扫 **SDI-4 #2** 口径收紧（上面最后一句**已失效**）：
#      官方 remediation 原文：
#        「Treat positive and negative evidence for the same treatment anywhere
#          in the product record as an unresolved conflict, regardless of element
#          or field boundaries.」
#      → 同一治疗手段在**整条产品记录**内既有肯定证据又有除外证据 → 一律
#        conflict_unresolved（unverified）→ **不宣称**（不论同元素 / 同字段）；
#        只有**收紧后的结构化权威规则**（显式类型化肯定决定）解决冲突时才可宣称。
# ---------------------------------------------------------------------------
# 否定/除外词：前瞻型（词在关键词之前）与回溯型（词在关键词之后）
_NEG_MARKERS_FORWARD = ("不含", "不包含", "不包括", "不纳入", "不涵盖", "不覆盖", "不支持")
_NEG_MARKERS_BACKWARD = ("除外", "不在保障范围", "不赔", "不予支付")
_NEG_MARKERS_BOTH = ("不予报销", "不报销", "无法报销", "不能报销", "不承保")
_NEG_MARKERS = tuple(sorted(
    set(_NEG_MARKERS_FORWARD + _NEG_MARKERS_BACKWARD + _NEG_MARKERS_BOTH),
    key=len, reverse=True))

# 肯定/授权词（用于「明确肯定表述」判定；落在否定词内部的一律不算）
_AFFIRM_MARKERS = ("含", "包含", "涵盖", "覆盖", "可报销", "报销", "给付", "支持", "承保")

# 上下文窗口：否定词与其绑定的关键词出现之间的距离上限（字符）
_NEG_CONTEXT_WINDOW = 30
# 语义子句边界：句号/分号/问号/叹号/冒号/换行/逗号 —— 否定语境不跨子句传播
#
# ⚠️ 普通空白（空格/制表符）**不再是**子句边界 —— 官方 SDI-4 残余 D
#    （2026-11-16 线上复扫 · 2.4.13 · issueCount=1 / score=12 / MEDIUM）：
#    「不含 CAR-T治疗费用报销」若在空格处截断否定作用域，CAR-T 就落到作用域之外，
#    紧邻的「报销」会通过肯定授权检查 → 输出「含CAR-T治疗」的**承保宣称**。
#    官方 remediation 原文：
#      「Do not treat ordinary whitespace as a semantic boundary for exclusion scope;
#        normalize spacing while preserving field boundaries, and bind negation to
#        the relevant treatment across spaces and tabs.」
#    → 空白在语义上**透明**：作用域扫描时跳过空白，否定作用域跨空格/制表符绑定到
#      相关治疗手段；**字段边界**（key_benefits ↔ highlights）另由 owner 映射保证。
_CLAUSE_BREAKS = "。；！？!?;:\n，,"

# 普通空白字符（空格/制表符/全角空格/不换行空格）—— **不是**语义边界
_WHITESPACE_CHARS = " \t\u3000\xa0"


def _treatment_occurrences(blob):
    """blob 中每个治疗手段关键词的**全部**出现位置 → [(kw, start, end), ...]"""
    occ = []
    if not blob:
        return occ
    for kw in _TREATMENT_CLAIMS:
        i = blob.find(kw)
        while i != -1:
            occ.append((kw, i, i + len(kw)))
            i = blob.find(kw, i + 1)
    occ.sort(key=lambda o: o[1])
    return occ


def _negation_marker_spans(blob):
    """blob 中全部否定/除外词的出现位置 → [(start, end, marker), ...]"""
    spans = []
    if not blob:
        return spans
    for m in _NEG_MARKERS:
        i = blob.find(m)
        while i != -1:
            spans.append((i, i + len(m), m))
            i = blob.find(m, i + 1)
    spans.sort(key=lambda s: (s[0], s[1]))
    return spans


def _is_scope_boundary(blob, i, owner=None):
    """该字符是否为**语义**子句边界 / 字段边界（普通空白**不算**边界）

    官方 SDI-4 残余 D（2026-11-16 线上复扫）remediation 原文：
      「Do not treat ordinary whitespace as a semantic boundary for exclusion scope;
        normalize spacing while preserving field boundaries, and bind negation to
        the relevant treatment across spaces and tabs.」

    ① 普通空白（空格/制表符/全角空格）**不是**边界 —— 不得截断否定作用域；
    ② **字段边界必须保留**：key_benefits 与 highlights 之间的分隔符
       （owner == -1）仍然截断作用域 —— 否则「不含」会把**别的字段**里的
       治疗手段也绑进除外作用域，跨字段冲突口径（unverified）会被破坏。
    """
    if i < 0 or i >= len(blob):
        return True
    if blob[i] in _CLAUSE_BREAKS:
        return True
    if owner is not None and i < len(owner) and owner[i] == -1:
        return True
    return False


def _scope_bounds(blob, lo, hi, forward, owner=None):
    """从否定词位置沿 forward（或反向）扫描到最近的**语义**边界 → (scope_start, scope_end)

    ⚠️ 普通空白**不**是边界（官方 SDI-4 残余 D）：否定作用域跨空格/制表符绑定
       到相关治疗手段（「不含 CAR-T治疗费用报销」必须整体绑定，不能在空格处截断）。
    ⚠️ owner 给出时，**字段边界**（owner == -1）同样截断作用域。
    """
    if forward:
        end = len(blob)
        for i in range(hi, len(blob)):
            if _is_scope_boundary(blob, i, owner):
                end = i
                break
        return hi, end
    start = 0
    for i in range(lo - 1, -1, -1):
        if _is_scope_boundary(blob, i, owner):
            start = i + 1
            break
    return start, lo


def _negation_context(blob, owner=None):
    """否定语境上下文（单一事实来源）：(occurrences, spans, bound)

    bound = 被否定语境绑定的出现位置集合 {(start, end), ...}

    ⚠️ owner = 字段归属映射（`_medical_fact_owner_map` 产出）—— 给出时
       **字段边界**会截断否定作用域（跨字段不得互相绑定）；None → 不做字段判定。
    ⚠️ 普通空白**不**截断作用域（官方 SDI-4 残余 D）。
    """
    occurrences = _treatment_occurrences(blob)
    spans = _negation_marker_spans(blob)
    bound = set()
    for ms, me, marker in spans:
        forward = marker in _NEG_MARKERS_FORWARD or marker in _NEG_MARKERS_BOTH
        backward = marker in _NEG_MARKERS_BACKWARD or marker in _NEG_MARKERS_BOTH
        if forward:
            s, e = _scope_bounds(blob, ms, me, True, owner)
            for _kw, o_s, o_e in occurrences:
                if s <= o_s < e and o_s - me <= _NEG_CONTEXT_WINDOW:
                    bound.add((o_s, o_e))
        if backward:
            s, e = _scope_bounds(blob, ms, me, False, owner)
            for _kw, o_s, o_e in occurrences:
                if s <= o_e <= e and ms - o_e <= _NEG_CONTEXT_WINDOW:
                    bound.add((o_s, o_e))
    return occurrences, spans, bound


def _keyword_is_negated(blob, start, end, context=None):
    """该次出现是否落在否定/除外语境（**单一事实来源**）。

    context 省略时自建；返回 True 表示该次出现属于「被排除」的表述。
    """
    if not blob or start < 0 or end > len(blob):
        return False
    occurrences, spans, bound = context if context else _negation_context(blob)
    del occurrences, spans
    return (start, end) in bound


def _clause_head(text):
    """取片段中最后一个子句边界**之后**的部分（子句前缀）→ (text, 偏移)

    ⚠️ 普通空白**不是**子句边界（官方 SDI-4 残余 D）→ 空白分隔的前后文
       属于同一语义片段（「含 CAR-T治疗」与「含CAR-T治疗」口径一致）。
    """
    cut = -1
    for ch in _CLAUSE_BREAKS:
        j = text.rfind(ch)
        if j > cut:
            cut = j
    if cut < 0:
        return text, 0
    return text[cut + 1:], cut + 1


def _clause_tail(text):
    """取片段中第一个子句边界**之前**的部分（子句后缀）→ (text, 偏移)

    ⚠️ 普通空白**不是**子句边界（官方 SDI-4 残余 D）→ 空白分隔的前后文
       属于同一语义片段（「不含 CAR-T治疗费用报销」整体成句）。
    """
    cut = len(text)
    for ch in _CLAUSE_BREAKS:
        j = text.find(ch)
        if j != -1 and j < cut:
            cut = j
    if cut == len(text):
        return text, 0
    return text[:cut], 0


def _negation_scope_map(blob, occurrences=None, spans=None, owner=None):
    """否定**作用域**映射：{(occ_start, occ_end): [(scope_start, scope_end, field_id), ...]}

    ⚠️ 为什么必须单独建这个映射（2026-11-14 官方 2.4.8 复扫 SDI-4 新变体）：
    否定**作用域**与否定**词字符跨度**是两个不同的东西。
    「不含CAR-T治疗费用报销」里，否定词「不含」的字符跨度只有 (0,2)，
    但它的作用域是 (2, 13) —— 「报销」就在这个作用域内，
    属于除外条款自己的一部分，**不得**当作对 CAR-T 的承保授权。

    官方 remediation 原文：
      「Require affirmative evidence to apply to the same treatment occurrence
        and to lie outside its entire exclusion scope, not merely outside the
        negation marker's character span.」
    """
    occurrences = occurrences if occurrences is not None else _treatment_occurrences(blob)
    spans = spans if spans is not None else _negation_marker_spans(blob)
    out = {}
    for ms, me, marker in spans:
        f_m = owner[ms] if (owner is not None and ms < len(owner)) else -1
        forward = marker in _NEG_MARKERS_FORWARD or marker in _NEG_MARKERS_BOTH
        backward = marker in _NEG_MARKERS_BACKWARD or marker in _NEG_MARKERS_BOTH
        if forward:
            s, e = _scope_bounds(blob, ms, me, True, owner)
            for _kw, o_s, o_e in occurrences:
                if s <= o_s < e and o_s - me <= _NEG_CONTEXT_WINDOW:
                    out.setdefault((o_s, o_e), []).append((s, e, f_m))
        if backward:
            s, e = _scope_bounds(blob, ms, me, False, owner)
            for _kw, o_s, o_e in occurrences:
                if s <= o_e <= e and ms - o_e <= _NEG_CONTEXT_WINDOW:
                    out.setdefault((o_s, o_e), []).append((s, e, f_m))
    return out


def _element_ordinal_map(owner):
    """每个字符所属的**字段元素**序号（分隔符 owner == -1 处递增）。

    ⚠️ 官方 SDI-4 残余 E：mixed-negation 分支必须能判断「肯定证据」与
       「除外证据」是否落在**同一个字段元素**（同一 key_benefits 元素 /
       同一 highlights 字段）—— 同一元素内既有包含又有除外 → 冲突 →
       按官方口径 unverified（不宣称）。

    owner[i] == -1（字段之间的分隔空格）处序号 +1 → 同元素的字符序号相同。
    """
    if not owner:
        return []
    out = []
    n = 0
    for f in owner:
        out.append(n)
        if f == -1:
            n += 1
    return out


# 结构化、权威的产品字段（**非**自由文本）—— 若产品用这类字段**逐项**列明
# 治疗手段的承保责任，则可裁决「包含 / 除外」证据冲突。
_STRUCTURED_AUTHORITY_FIELDS = ("coverage_items", "covered_treatments",
                                "treatment_coverage", "treatment_responsibilities")

# 结构化字段里**治疗手段标识**的键名（list 元素 / 嵌套 dict 用）
_STRUCTURED_ITEM_ID_KEYS = ("treatment", "treatment_name", "treatment_id",
                            "name", "id", "key", "item", "benefit")
# 结构化字段里**承保决定**的键名 —— 必须是显式布尔 True 才算肯定授权
_STRUCTURED_DECISION_KEYS = ("covered", "is_covered")
# 结构化字段值里的**否定语义**词表（已规范化：小写 + 去空白）
# ⚠️ 命中否定语义 → 该治疗手段**不得**被授权，且必须**主动压制**。
_STRUCTURED_NEGATION_TOKENS = (
    "excluded", "exclude", "exclusion", "notcovered", "notcover", "notinclude",
    "noteligible", "notpayable", "notreimbursed", "nocoverage", "uncovered",
    "false",
    "除外", "不承保", "不保", "不含", "不覆盖", "未覆盖", "不在保障范围",
    "不予报销", "不报销", "无法报销", "不能报销", "不予支付", "不赔",
    "拒绝承保", "非承保", "不纳入", "不支持",
)


def _normalize_treatment_identifier(text):
    """规范化治疗手段标识（**规范化标识匹配**，不是子串匹配）。

    官方 2.4.15 复扫 SDI-4 #1 remediation 原文：
      「... using canonical treatment identifiers and typed coverage decisions
        rather than substring matches.」

    规范化口径：NFKC（全角 → 半角）→ 去**全部**空白（含全角空格 / NBSP）→
    统一连字符（- ‐ ‑ – — ― → -）→ 下划线 → 连字符 → 大小写归一（casefold）。
    """
    if not isinstance(text, str):
        return ""
    s = unicodedata.normalize("NFKC", text)
    s = "".join(ch for ch in s if not ch.isspace())
    s = "".join("-" if ch in "-‐‑‒–—―−﹣_" else ch for ch in s)
    return s.casefold()


def _structured_text_is_negative(text):
    """结构化字段的**字符串值**是否带否定语义（excluded / 除外 / 不承保 …）。"""
    if not isinstance(text, str):
        return False
    s = unicodedata.normalize("NFKC", text).casefold()
    s = "".join(ch for ch in s if not ch.isspace())
    if not s:
        return False
    return any(tok in s for tok in _STRUCTURED_NEGATION_TOKENS)


def _structured_contains_negation(mapping):
    """结构化条目（dict）里是否**另有**否定语义（自相矛盾 → 不得授权）。"""
    if not isinstance(mapping, dict):
        return False
    for val in mapping.values():
        if isinstance(val, str) and _structured_text_is_negative(val):
            return True
        if isinstance(val, (list, tuple)):
            for item in val:
                if isinstance(item, str) and _structured_text_is_negative(item):
                    return True
    return False


def _structured_decision_state(value):
    """单个**承保决定值**的状态 → "affirmative" / "negative" / "ambiguous"

    官方 2.4.16 复扫 SDI-4 remediation 原文：
      「Validate structured coverage entries against an explicit schema and evaluate
        every recognized decision key before assigning a state. Reject conflicting
        decisions or classify them as unresolved and suppress the claim; also
        reconcile matching entries across all structured authority fields before
        allowing any affirmative resolution.」

    标量口径：
      · 布尔 True                      → affirmative（**唯一**的肯定授权形态）
      · 布尔 False / None / 数值 0      → negative（显式否定 → 主动压制）
      · 否定语义字符串（"excluded" / 除外 …）→ negative
      · 其它（字符串非否定 / 未知类型 / 畸形）→ ambiguous（**不授权**）
    """
    if value is True:
        return "affirmative"
    if value is False or value is None:
        return "negative"
    if isinstance(value, (int, float)):
        return "negative" if value == 0 else "ambiguous"
    if isinstance(value, str):
        return "negative" if _structured_text_is_negative(value) else "ambiguous"
    return "ambiguous"


def _structured_value_state(value):
    """结构化字段里单个值的**承保决定**状态
    → "affirmative" / "negative" / "ambiguous" / "contradictory"

    官方 2.4.15 复扫 SDI-4 #1 remediation 原文：
      「Require an affirmative coverage decision ... false, excluded, unknown,
        malformed, or ambiguous values must not authorize a claim.」

    官方 2.4.16 复扫 SDI-4 remediation 原文（**全部**决定键都要求值）：
      「Validate structured coverage entries against an explicit schema and evaluate
        every recognized decision key before assigning a state. Reject conflicting
        decisions or classify them as unresolved and suppress the claim; also
        reconcile matching entries across all structured authority fields before
        allowing any affirmative resolution.」

      · 布尔 True                     → affirmative（**唯一**的肯定授权形态）
      · 布尔 False / None / 数值 0     → negative（显式否定 → 主动压制）
      · dict：**全部**命中 _STRUCTURED_DECISION_KEYS 的键都要求值（不得只看第一个）
        - 各键状态一致（全 affirmative / 全 negative）→ 按一致状态走
        - 各键状态不一致（affirmative+negative / affirmative+ambiguous /
          negative+ambiguous）→ **contradictory**（自相矛盾 → 不得授权 + 压制）
      · dict 且 affirmative 决定 + 同条目另有否定语义 → ambiguous（不得授权）
      · 其它（字符串值 / 未知键 / 畸形）→ ambiguous（**不授权**）
    """
    if value is True:
        return "affirmative"
    if value is False or value is None:
        return "negative"
    if isinstance(value, bool):          # 理论不可达（上面已覆盖 True/False）
        return "ambiguous"
    if isinstance(value, (int, float)):
        return "negative" if value == 0 else "ambiguous"
    if isinstance(value, dict):
        # 官方 2.4.16 复扫 SDI-4：**全部**决定键都要求值（不得只看第一个命中）
        states = []
        for key in _STRUCTURED_DECISION_KEYS:
            if key in value:
                states.append(_structured_decision_state(value[key]))
        if not states:
            return "ambiguous"           # 无承保决定字段 → 未知 → ambiguous
        if len(set(states)) > 1:
            # 同一条目内多个决定键互相矛盾（affirmative+negative /
            # affirmative+ambiguous / negative+ambiguous）
            # → 官方口径「classify them as unresolved and suppress the claim」
            # → contradictory：**不得**判为 affirmative（不得授权），
            #   且必须能被 _structured_authority_denies 命中 → **主动压制**。
            return "contradictory"
        state = states[0]
        if state == "affirmative":
            if _structured_contains_negation(value):
                return "ambiguous"       # 同一条目另有否定语义 → 不得授权
            return "affirmative"
        if state == "negative":
            return "negative"
        return "ambiguous"
    if isinstance(value, str):
        return "negative" if _structured_text_is_negative(value) else "ambiguous"
    return "ambiguous"


def _structured_item_identifier(item):
    """结构化 list 元素 / dict 里的**治疗手段标识**（无 → None）。"""
    if not isinstance(item, dict):
        return None
    for key in _STRUCTURED_ITEM_ID_KEYS:
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return None


def _structured_authority_states(product, norm_kw):
    """收集该治疗手段在**全部**结构化权威字段里的**匹配条目**的承保决定状态。

    官方 2.4.16 复扫 SDI-4 remediation 原文：
      「Validate structured coverage entries against an explicit schema and evaluate
        every recognized decision key before assigning a state. ... also reconcile
        matching entries across all structured authority fields before allowing any
        affirmative resolution.」

    返回状态列表（可能为空 → 该产品**没有**任何结构化条目提及该治疗手段）：
      "affirmative" / "negative" / "ambiguous" / "contradictory"
    """
    states = []
    if not product:
        return states
    for field in _STRUCTURED_AUTHORITY_FIELDS:
        value = product.get(field)
        if isinstance(value, dict):
            for key, val in value.items():
                if not isinstance(key, str):
                    continue
                if _normalize_treatment_identifier(key) != norm_kw:
                    continue
                states.append(_structured_value_state(val))
        elif isinstance(value, (list, tuple)):
            for item in value:
                if not isinstance(item, dict):
                    continue                # 裸字符串 → ambiguous → 不授权
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if _normalize_treatment_identifier(ident) != norm_kw:
                    continue
                states.append(_structured_value_state(item))
    return states


def _structured_authority_resolves(product, keyword):
    """结构化、权威的产品字段能否裁决该治疗手段的「包含 / 除外」冲突。

    官方 2.4.15 复扫 SDI-4 #1 remediation（原文）：
      「Define and validate an explicit schema for structured treatment coverage,
        using canonical treatment identifiers and typed coverage decisions rather
        than substring matches. Require an affirmative coverage decision plus
        applicable conditions and explicit resolution of conflicting exclusions;
        false, excluded, unknown, malformed, or ambiguous values must not
        authorize a claim.」

    落实口径（**只有显式类型化的肯定决定**才可授权）：
      · dict：键为**规范化治疗手段标识**且值为布尔 True；或值为 dict 且其
        covered 键为布尔 True；
      · list / tuple：元素为 dict，形如 {"treatment": "CAR-T", "covered": true}；
      · 其余一律**不授权**：裸字符串列表（["CAR-T"]）、字符串值、未知值、
        否定值（False / None / "excluded" / 除外 …）全部视为 ambiguous；
      · 标识匹配一律走**规范化标识**（`_normalize_treatment_identifier`），
        **不得**用「字符串包含关键词」的子串判定。

    ⚠️ key_benefits / highlights / tags 都是**自由文本**（同一句话里可能既
       包含又除外），**不得**用来裁决冲突 → 只认**结构化**字段。
       本产品库实测无此类字段（0 / 2577 款）→ 冲突一律 unverified。
    """
    if not product:
        return False
    norm_kw = _normalize_treatment_identifier(keyword)
    if not norm_kw:
        return False
    states = _structured_authority_states(product, norm_kw)
    if not states:
        return False
    # 官方 2.4.16 复扫 SDI-4 remediation 原文：
    #   「... reconcile matching entries across all structured authority fields
    #     before allowing any affirmative resolution.」
    # → 全部**匹配条目**（跨所有结构化权威字段）都必须是 affirmative；
    #   任意一条 negative / contradictory / ambiguous → **不得**给出肯定裁决。
    return all(state == "affirmative" for state in states)


def _structured_authority_denies(product, keyword):
    """结构化、权威的产品字段是否**显式否定**该治疗手段 → 主动压制（不得宣称）。

    官方 2.4.15 复扫 SDI-4 #1 remediation（原文）：
      「false, excluded, unknown, malformed, or ambiguous values must not
        authorize a claim.」

    ⚠️ 「不授权」只说明**不能用来授权**；「否定」更进一步 —— 该治疗手段在
       本产品上**一律不得**被宣称（无论条款正文怎么写）。
       否定形态：布尔 False / None / 数值 0 / 带否定语义的字符串
       （"excluded" / "not covered" / "除外" / "不承保" …）。
    """
    if not product:
        return False
    norm_kw = _normalize_treatment_identifier(keyword)
    if not norm_kw:
        return False
    for field in _STRUCTURED_AUTHORITY_FIELDS:
        value = product.get(field)
        if isinstance(value, dict):
            for key, val in value.items():
                if not isinstance(key, str):
                    continue
                if _normalize_treatment_identifier(key) != norm_kw:
                    continue
                if _structured_value_state(val) in ("negative", "contradictory"):
                    return True
        elif isinstance(value, (list, tuple)):
            for item in value:
                if isinstance(item, str):
                    # 裸字符串：ambiguous → 不授权；但**自带否定语义** → 压制
                    if _structured_text_is_negative(item) and \
                            norm_kw in _normalize_treatment_identifier(item):
                        return True
                    continue
                if not isinstance(item, dict):
                    continue
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if _normalize_treatment_identifier(ident) != norm_kw:
                    continue
                if _structured_value_state(item) in ("negative", "contradictory"):
                    return True
    return False


def _product_text_leaves(product):
    """产品记录里**全部文本叶子**（字符串值；列表元素逐个独立成句）。"""
    out = []

    def walk(value):
        if isinstance(value, str):
            out.append(value)
        elif isinstance(value, dict):
            for val in value.values():
                walk(val)
        elif isinstance(value, (list, tuple)):
            for val in value:
                walk(val)

    if isinstance(product, dict):
        for val in product.values():
            walk(val)
    return out


def _record_exclusion_keywords(product):
    """**整条产品记录**内存在除外证据的治疗手段集合（官方 2.4.15 SDI-4 #2）。

    官方 remediation（原文）：
      「Treat positive and negative evidence for the same treatment anywhere in the
        product record as an unresolved conflict, regardless of element or field
        boundaries.」

    口径：逐个**文本叶子**（key_benefits 元素 / highlights / notes / tags …）
    独立判定 —— 同一治疗手段只要在**任意一个**文本叶子里落在否定 / 除外作用域内，
    即视为「该产品记录内存在除外证据」。
    """
    out = set()
    if not product:
        return out
    for text in _product_text_leaves(product):
        if not text or not text.strip():
            continue
        if not any(kw in text for kw in _TREATMENT_CLAIMS):
            continue                      # 不含任何治疗手段 → 跳过（性能）
        occurrences, _spans, bound = _negation_context(text, None)
        for kw, s, e in occurrences:
            if (s, e) in bound:
                out.add(kw)
    return out


def _medical_fact_owner_map(product):
    """事实源文本的**字段归属映射** → (blob, owner)

    owner[i] = blob 第 i 个字符所属的字段 id（0 = key_benefits，1 = highlights，
    -1 = 字段之间的分隔空格）。

    ⚠️ 必须与 `_medical_fact_text` 口径**完全一致**（同样的字段、同样的顺序、
    同样的空格拼接）—— 跨字段的冲突表述（key_benefits 说含、highlights 说不含）
    必须按「unverified」处理，不得互相授权。
    """
    if not product:
        return "", []
    parts = []
    owners = []
    kb = product.get("key_benefits")
    if isinstance(kb, (list, tuple)):
        for x in kb:
            parts.append(str(x))
            owners.append(0)
    elif isinstance(kb, str):
        parts.append(kb)
        owners.append(0)
    hl = product.get("highlights")
    if isinstance(hl, str):
        parts.append(hl)
        owners.append(1)
    blob = ""
    owner = []
    for i, (p, f) in enumerate(zip(parts, owners)):
        if i:
            blob += " "
            owner.append(-1)
        blob += p
        owner.extend([f] * len(p))
    return blob, owner


def _scope_has_affirmative(blob, negated_occ, scope_map):
    """除外作用域内是否出现**肯定字样** → 该除外表述自相矛盾 → 按 unverified 处理

    官方 remediation：「Treat conflicting or ambiguous coverage statements as
    unverified rather than emitting unconditional coverage claims.」
    """
    for o in negated_occ:
        for (sc, ec, _f) in scope_map.get((o[1], o[2]), ()):
            if sc >= ec:
                continue
            seg = blob[sc:ec]
            if any(tok in seg for tok in _AFFIRM_MARKERS):
                return True
    return False


def _has_affirmative(text, base, spans, excluded=(), owner=None, field=None):
    """片段内是否存在**有效的**明确肯定表述

    有效性三条硬要求（都要满足）：
      ① 不落在否定词**字符跨度**内（「不含」里的「含」不算肯定）；
      ② 不落在该次出现的**否定作用域**内 —— 官方 2.4.8 SDI-4 remediation：
         肯定证据必须落在整个除外作用域之外，而不只是否定词字符跨度之外；
      ③ 肯定证据与该次出现**同字段**（owner/field 给出时生效）——
         key_benefits 的授权不得授权 highlights 的关键词（反之亦然）。

    excluded = [(scope_start, scope_end, field_id), ...] —— 该次出现的除外作用域。
    owner    = 字段归属映射（`_medical_fact_owner_map` 产出）；None → 不做同字段判定。
    field    = 该次出现所属字段 id（0 = key_benefits，1 = highlights）；
               None → 不做同字段判定。
    """
    if not text:
        return False
    for token in _AFFIRM_MARKERS:
        i = text.find(token)
        while i != -1:
            ts, te = base + i, base + i + len(token)
            ok = not any(ms < te and ts < me for ms, me, _m in spans)
            if ok:
                ok = not any(sc <= ts and te <= ec for sc, ec, _f in excluded)
            if ok and owner is not None and field is not None:
                ok = ts < len(owner) and owner[ts] == field
            if ok:
                return True
            i = text.find(token, i + 1)
    return False


def _element_bounds(blob, owner, s, e):
    """该次出现所属**字段元素**的边界 → (lo, hi)

    字段元素 = key_benefits 的**单个元素** 或 highlights 整个串。
    `_medical_fact_owner_map` 把元素之间的分隔符标成 owner == -1，
    这里用它把肯定证据窗口收敛在**同一个元素**内。

    ⚠️ 官方 SDI-4 残余 D：「normalize spacing while preserving field
       boundaries」—— 空白在元素**内**透明（"含 CAR-T治疗" 与 "含CAR-T治疗"
       同口径），但**不得**跨元素借用肯定字样：
       「包含原位癌」里的「含」**不是**对「质子重离子」的承保授权。
    """
    lo, hi = 0, len(blob)
    if owner is not None:
        for i in range(s - 1, -1, -1):
            if i < len(owner) and owner[i] == -1:
                lo = i + 1
                break
        for i in range(e, len(blob)):
            if i < len(owner) and owner[i] == -1:
                hi = i
                break
    return lo, hi


def _occurrence_is_affirmative(blob, occ, occurrences, spans, scope_map=None,
                               owner=None, extra_excluded=()):
    """该次出现附近是否有**有效的**明确肯定表述（"含…"/"…可报销"等）

    ⚠️ excluded = 该次出现的**否定作用域** —— 作用域内的「报销」「给付」等字样
    属于除外条款本身，**不得**作为承保授权（官方 2.4.8 SDI-4 原文要求：
    肯定证据必须落在整个除外作用域之外，而不只是否定词字符跨度之外）。

    ⚠️ owner/field = **同字段**判定（SDI-4 残余 C · 2026-11-14）——
    肯定证据必须与该次出现**同字段**（key_benefits 的授权不得授权 highlights 的
    关键词，反之亦然）；owner=None → 不做同字段判定。

    ⚠️ extra_excluded = 事实源文本中**全部**除外作用域 —— 落在**别的**治疗手段
    除外条款里的「报销」等字样同样**不得**作为承保授权。

    ⚠️ 证据窗口按**字段元素**收敛（官方 SDI-4 残余 D）：空白在元素内透明，
       但不得跨元素借用肯定字样。
    """
    _kw, s, e = occ
    prev_end = 0
    next_start = len(blob)
    for _kw2, o_s, o_e in occurrences:
        if o_e <= s and o_e > prev_end:
            prev_end = o_e
        if o_s >= e and o_s < next_start:
            next_start = o_s
    el_lo, el_hi = _element_bounds(blob, owner, s, e)
    win_lo = max(prev_end, el_lo)
    win_hi = min(next_start, el_hi)
    head, head_off = _clause_head(blob[win_lo:s])
    tail, tail_off = _clause_tail(blob[e:win_hi])
    excluded = tuple((sc, ec, f) for (sc, ec, f) in (scope_map or {}).get((s, e), ()))
    excluded = excluded + tuple(extra_excluded or ())
    field = None
    if owner is not None and s < len(owner):
        field = owner[s]
    return (_has_affirmative(head, win_lo + head_off, spans, excluded, owner, field)
            or _has_affirmative(tail, e + tail_off, spans, excluded, owner, field))


def _medical_fact_text(product):
    """医疗险条款事实源文本：key_benefits 元素 + highlights 字符串。

    ⚠️ key_benefits 是 **list** → 必须元素级匹配（`"质子重离子" in list` 恒 False）。
    ⚠️ highlights 是 **str** → 子串匹配有效。
    ⚠️ notes / suitable_for / competitive_edge 是营销软文 → **不**作事实源。
    """
    if not product:
        return ""
    parts = []
    kb = product.get("key_benefits")
    if isinstance(kb, (list, tuple)):
        parts.extend(str(x) for x in kb)
    elif isinstance(kb, str):
        parts.append(kb)
    hl = product.get("highlights")
    if isinstance(hl, str):
        parts.append(hl)
    return " ".join(parts)


def _medical_treatment_claims(product):
    """该产品真实字段里出现过的治疗手段关键词（固定顺序 · **逐次出现**否定语境判定）。

    判定口径（SDI-4 官方 2.4.7 复扫整改 + 2.4.9 复扫**残余 C** 整改）：
      ① 每个关键词遍历事实源文本中的**全部**出现位置；
      ② 每次出现都取上下文窗口（命中点前后）判断是否落在否定/除外语境
         （不含 / 不包含 / 不予报销 / 不报销 / 除外 / 不在保障范围 / 不覆盖 /
           无法报销 / 不能报销 / 不承保 / 不赔 / 不予支付 …）；
      ③ 该关键词**全部**出现皆为否定 → **不**计入 claims（纯除外条款不得转为承保宣称）；
      ④ 存在**非否定**出现 → 进入**肯定授权判定**（见 ⑤⑥）；
      ⑤ 若同时存在否定出现与**明确肯定**表述（"含…"/"…可报销"）→ 仍计入
         （⚠️ 2026-11-17 官方 2.4.15 SDI-4 #2 口径收紧：**本条已失效** ——
          肯定证据与除外证据只要在**整条产品记录**内并存 → 一律 unverified
          → 不宣称；只有**收紧后的结构化权威规则**解决冲突时才可宣称）。
      ⑥ **完全没有否定出现**时（`not negated` 分支）：关键词「在条款里出现过」
         **不构成**承保授权 —— 必须在**同一次出现**、**同一字段**找到落在
         除外作用域之外的**明确肯定表述**才可对外宣称；找不到 → 按官方口径
         「unverified」处理 → **不宣称**（**不得改写措辞继续宣称**）。
    """
    blob = _medical_fact_text(product)
    if not blob:
        return []
    owner_blob, owner = _medical_fact_owner_map(product)
    assert owner_blob == blob, "事实源口径漂移：owner map 与 _medical_fact_text 不一致"
    # 字段元素序号（SDI-4 残余 E）：mixed-negation 分支要判断「肯定证据」与
    # 「除外证据」是否落在**同一个字段元素**（同一 key_benefits 元素 / 同一
    # highlights 字段）—— 同元素内既有包含又有除外 → 冲突 → unverified。
    elem_ord = _element_ordinal_map(owner)
    occurrences, spans, bound = _negation_context(blob, owner)
    if not occurrences:
        return []
    scope_map = _negation_scope_map(blob, occurrences, spans, owner)
    # 事实源文本中**全部**除外作用域（跨关键词）：落在**别的**治疗手段除外条款
    # 里的「报销」「给付」等字样，同样**不得**作为承保授权。
    all_scopes = tuple(sc for scopes in scope_map.values() for sc in scopes)
    # ⑩-0 **记录级**除外证据（整条产品记录，不限字段 / 元素）—— 官方 2.4.15 SDI-4 #2
    record_excluded = _record_exclusion_keywords(product)
    claims = []
    for kw in _TREATMENT_CLAIMS:
        k_occ = [o for o in occurrences if o[0] == kw]
        if not k_occ:
            continue
        negated = [o for o in k_occ
                   if _keyword_is_negated(blob, o[1], o[2],
                                          (occurrences, spans, bound))]
        # ⑩-1 结构化权威字段**显式否定** → 主动压制：该治疗手段在本产品上
        #      **一律不得**被宣称（与条款正文怎么写无关）。
        if _structured_authority_denies(product, kw):
            continue
        # ⑩-2 **记录级**冲突（官方 2.4.15 复扫 SDI-4 #2）：同一治疗手段在
        #      **整条产品记录**内同时存在肯定证据与除外证据 → 一律冲突
        #      （unverified）→ 不宣称，**不论**是否同元素 / 同字段。
        record_conflict = kw in record_excluded
        if not negated:
            # SDI-4 残余 C（官方 2.4.9 复扫）：**没有否定出现 ≠ 有肯定授权**。
            # 关键词裸列在 key_benefits / highlights 里只说明「条款提到过」，
            # **不构成**承保授权 —— 必须能在**同一次出现**、**同一字段**找到
            # 落在除外作用域之外的**明确肯定表述**（"含…"/"…可报销"/"…给付" …）
            # 才可对外宣称；找不到 → unverified → **不宣称**。
            ok = False
            for o in k_occ:
                if _occurrence_is_affirmative(blob, o, occurrences, spans,
                                             scope_map, owner, all_scopes):
                    ok = True
                    break
            if ok and record_conflict:
                # 除外证据出现在**其它字段**（记录级）→ 同样按 unverified 处理
                ok = False
            if ok:
                claims.append(kw)
            continue
        # ⑦ 除外表述**自身**含肯定字样（如「不含CAR-T治疗费用报销」里的「报销」）
        #    → 该表述自相矛盾 → 按官方口径「conflicting statements as unverified」
        #    处理，**不**对外宣称。
        if _scope_has_affirmative(blob, negated, scope_map):
            continue
        # ⑧ mixed-negation 分支：同一关键词既有**肯定**证据又有**除外**证据。
        #
        #    官方 remediation（2.4.15 复扫口径，原文）：
        #      「Pass scope_map, owner, and all_scopes consistently to
        #        _occurrence_is_affirmative in the mixed-negation branch,
        #        preserving same-element authorization checks. Treat conflicting
        #        positive and negative coverage evidence as unverified unless a
        #        structured, validated rule resolves the conflict, and suppress
        #        unconditional treatment claims in that case.」
        #
        #    落实口径（两库同口径）：
        #      ① 肯定证据必须与该次出现**同字段**、**同元素** → 传全
        #         scope_map / owner / all_scopes（与 ⑥ 非否定分支一致）——
        #         跨字段、跨元素借用授权一律不成立；
        #      ② 肯定证据与除外证据落在**同一元素**（同一 key_benefits 元素 /
        #         同一 highlights 字段）→ 同一处既包含又除外 → **冲突**；
        #      ③ 冲突只有被**结构化、权威**的产品字段逐项裁决时才可宣称，
        #         否则按官方口径 unverified → **一律不宣称**；
        #      ④ 跨字段（key_benefits ↔ highlights）冲突 → 无法裁决 → 不宣称。
        neg_fields = set()
        neg_elems = set()
        for o in negated:
            if o[1] < len(owner):
                neg_fields.add(owner[o[1]])
                neg_elems.add((owner[o[1]], elem_ord[o[1]]))
        ok = False
        conflict_unresolved = False
        for o in k_occ:
            if (o[1], o[2]) in bound:
                continue                      # 这次出现本身落在除外语境里
            if owner[o[1]] not in neg_fields:
                continue                      # 跨字段冲突 → unverified
            same_elem = (owner[o[1]], elem_ord[o[1]]) in neg_elems
            if not _occurrence_is_affirmative(blob, o, occurrences, spans,
                                             scope_map, owner, all_scopes):
                continue                      # 该次出现没有有效的肯定授权证据
            if same_elem:
                conflict_unresolved = True    # 同元素包含/除外冲突 → 待裁决
                continue
            ok = True
            break
        # ⑧-3 **记录级**冲突（官方 2.4.15 复扫 SDI-4 #2 · 跨元素 / 跨字段）：
        #      肯定证据与除外证据**不论是否同元素 / 同字段**都算冲突 →
        #      一律 conflict_unresolved（unverified）→ 不得无条件宣称；
        #      只有**收紧后的结构化权威规则**（显式类型化肯定决定）解决时才可宣称。
        if ok:
            ok = False
            conflict_unresolved = True
        if not ok and conflict_unresolved and _structured_authority_resolves(product, kw):
            ok = True                        # 结构化、权威字段裁决适用性
        if ok:
            claims.append(kw)
    return claims


def _medical_treatment_suffix(product):
    """治疗手段后缀（仅当产品真实字段授权时才有；无授权返回空串）。"""
    claims = _medical_treatment_claims(product)
    if not claims:
        return ""
    return "，含" + "、".join(claims) + "治疗"


def _medical_form_claim(product):
    """医疗险形态宣称：只认 subtype（如「百万医疗」）。无 subtype 返回空串。"""
    if not product:
        return ""
    return (product.get("subtype") or "").strip()


def _medical_base_claim(product):
    """医疗险卖点基底：只由产品真实字段（subtype）决定，不含未经授权的治疗手段。"""
    form = _medical_form_claim(product)
    return f"{form}保障" if form else "医疗保障"


# ----------------------------------------------------------------------
# 重疾险对外宣称的事实源派生（SDI-4 整改 2026-11-13）
# ----------------------------------------------------------------------
def _crx_is_multi(product):
    """「多次赔付」的唯一权威来源是产品库 subtype 字段。

    ⚠️ 不可用 key_benefits / highlights 判定：实测 660 款重疾险中有 84 款
       key_benefits、76 款 highlights 写着「多次赔付」但 subtype 不含「多次」
       （真实口径是单次赔付型）→ 抄原文会把属性说反。
    """
    if not product:
        return False
    return "多次" in (product.get("subtype") or "")


def _crx_is_lifetime(product):
    """「终身」判定：coverage_period_is_lifetime 优先，其次 coverage_period 文本。"""
    if not product:
        return False
    flag = product.get("coverage_period_is_lifetime")
    if flag is True:
        return True
    if flag is False:
        return False
    return (product.get("coverage_period") or "").strip() == "终身"


def _crx_coverage_period(product):
    """重疾险保障期对外表述：原样取产品库 coverage_period（strip 后），不拼接不改写。

    为空时返回空串（与产品库字段严格一致）→ 由调用方记录 limitation。
    """
    if not product:
        return ""
    return (product.get("coverage_period") or "").strip()


def _crx_disease_claim(product):
    """重疾病种/轻症宣称：只认 highlights 字符串（须含「轻症」且能提取到「N种重疾」）。

    ⚠️ key_benefits 是 list → 元素级 "轻症" in list 恒 False → 不可作事实源。
    """
    if not product:
        return ""
    hl = product.get("highlights")
    if not isinstance(hl, str) or "轻症" not in hl:
        return ""
    m = re.search(r"(\d+)\s*种重疾", hl)
    if not m:
        return ""
    return f"{m.group(1)}种重疾+轻症保障"


def _crx_key_benefits(product, coverage, style="standard"):
    """按产品真实字段派生重疾险对外卖点文案。

    style="standard" → 「{病种轻症}，确诊即赔付{n}万」（无轻症来源时降级为「重疾保障，确诊即赔付{n}万」）
    style="premium"  → 「{重疾多次赔付?}{，终身保障?}，保额{n}万」（两项均无授权时 → 「重疾保障，保额{n}万」）
    """
    coverage = int(coverage or 0)
    amount = coverage // 10000
    multi = _crx_is_multi(product)
    lifetime = _crx_is_lifetime(product)

    if style == "premium":
        parts = []
        if multi:
            parts.append("重疾多次赔付")
        if lifetime:
            parts.append("终身保障")
        if parts:
            return "，".join(parts) + f"，保额{amount}万"
        return f"重疾保障，保额{amount}万"

    disease = _crx_disease_claim(product)
    if disease:
        return f"{disease}，确诊即赔付{amount}万"
    return f"重疾保障，确诊即赔付{amount}万"


def _crx_feature(product):
    """标准版 features 中的重疾卖点：按真实选中产品派生，不写死「终身保障」。"""
    if not product:
        return "重疾保障按实际需求配置"
    if _crx_is_lifetime(product):
        return "重疾险提供终身保障，确诊即赔付"
    return "重疾险确诊即赔付"


def load_products(include_discontinued=False):
    """加载产品数据（默认已应用有效性过滤，排除已停售/重复/脏数据）。"""
    product_file = os.path.join(os.path.dirname(__file__), "../references/products.json")
    with open(product_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    products = [p for p in data["products"]
                if _is_product_eligible(p, include_discontinued=include_discontinued)]
    return products


def select_products(products, product_type, criteria="recommended"):
    """按类型筛选产品"""
    filtered = [p for p in products if p["type"] == product_type]
    if not filtered:
        return []
    # 按保费排序（性价比）
    if criteria == "cheapest":
        return sorted(filtered, key=lambda x: x.get("premium_per_10k", 999))
    elif criteria == "recommended":
        # 推荐中等价位产品
        return sorted(filtered, key=lambda x: x.get("premium_per_10k", 999))
    return filtered

def design_plan(plan_type, age, gender, annual_income, annual_budget, coverage_needs):
    """设计保险方案"""
    products = load_products()

    if plan_type == "基础版":
        return design_basic_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    elif plan_type == "标准版":
        return design_standard_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    elif plan_type == "全面版":
        return design_premium_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    else:
        return None


def calculate_product_premium(product, age, gender, coverage, payment_term):
    """计算产品保费"""
    age_factor = 1.0
    if age >= 18 and age <= 30:
        age_factor = 0.8
    elif age >= 31 and age <= 40:
        age_factor = 1.0
    elif age >= 41 and age <= 50:
        age_factor = 1.3
    elif age >= 51 and age <= 55:
        age_factor = 1.6

    gender_factor = 1.0 if gender in ["男", "男性"] else 0.85

    if product["type"] == "医疗险":
        if age <= 30:
            return max(coverage * 0.0003, 200)
        elif age <= 40:
            return max(coverage * 0.0004, 200)
        elif age <= 50:
            return max(coverage * 0.0006, 200)
        else:
            return max(coverage * 0.001, 200)

    if product["type"] == "意外险":
        return max(coverage * 0.001, 100)

    payment_factor = 1.0
    if payment_term == "趸交":
        payment_factor = 0.85
    elif payment_term == "3年":
        payment_factor = 0.95
    elif payment_term == "5年":
        payment_factor = 1.0
    elif payment_term == "10年":
        payment_factor = 1.05
    elif payment_term == "20年":
        payment_factor = 1.15

    base = (coverage / 10000) * product.get("premium_per_10k", 250)
    return round(base * age_factor * gender_factor * payment_factor, 2)


# ---------------------------------------------------------------------------
# I2 预算硬约束
# ---------------------------------------------------------------------------

# 核心保障险种：移除顺序在可选险种之后作为兜底
# （重疾险 → 定期寿险）。min_coverage 是「可售最小保额」，不是「必须卖这么多」，
# 因此降到下限仍超预算时允许移除。
_CORE_COVERAGE_TYPES = ("重疾险", "定期寿险")


def _product_index(products):
    """建立 (type, product_name) → 产品记录 的索引，供保费重算使用。"""
    return {(p.get("type"), p.get("name")): p for p in products}


# 保额单位合同：唯一受支持的单位 → 换算为「元」的系数。
# 「元」与「万元」是产品库当前唯一支持的两种单位（实测 2542 条记录：
# 万元 2267 / 缺失 275 / 无其他取值）。**不做静默兜底**。
_COVERAGE_UNIT_FACTORS = {
    "元": 1,
    "万元": 10000,
}


def _coverage_unit_factor(product):
    """保额单位换算系数（单一事实来源）：返回 (factor, status)。

    status:
      - "ok"               —— 单位明确且受支持（"元" / "万元"），factor 为换算系数
      - "unit_missing"     —— coverage_unit 缺失 / 空串 / 非字符串
      - "unit_unsupported" —— coverage_unit 是受支持之外的值（如 "亿元" / "USD"）

    ⚠️ SDI-4 整改 2026-11-09：**不做静默兜底**。
    旧实现在单位缺失时静默套「万元」系数（×10000），而旧 docstring 却把缺省单位
    写成「元」—— 文档与实现相反，单位缺失时可售上限会被**放大 10000 倍**，
    反而放行超出真实可售上限的保额。
    现在：单位缺失 → 不猜、不换算（factor=None, status="unit_missing"）；
    单位不受支持 → 显式标记（factor=None, status="unit_unsupported"），
    两者都**不静默套任何乘数**，交由调用方如实留痕 + 对外披露。

    ⚠️ 口径选择说明（重要，勿擅自改为缺省「元」）：
    若把缺省单位改成「元」，实测产品库 2267 条「万元」记录的换算结果会**缩小
    10000 倍** → 击穿可售上限夹逼保护（上限保护失效比「文档↔实现矛盾」更严重）。
    因此本轮口径 = 显式支持「元」/「万元」；缺失与不支持一律**不换算**。
    （实测「有保额上下限但缺单位」的记录数为 0、「元/万元」之外的单位为 0 条
      → 对现有数据零行为影响。）

    Returns:
        tuple[int | None, str]: (换算系数, 状态)。factor 为 None 时**不得**套任何乘数。
    """
    if not product:
        return None, "unit_missing"
    unit = product.get("coverage_unit")
    if unit is None or not isinstance(unit, str):
        return None, "unit_missing"
    unit = unit.strip()
    if not unit:
        return None, "unit_missing"
    if unit not in _COVERAGE_UNIT_FACTORS:
        return None, "unit_unsupported"
    return _COVERAGE_UNIT_FACTORS[unit], "ok"


def _coverage_floor(product, entry):
    """保额下调下限：产品 min_coverage 按**单位合同**换算为元。

    单位口径（与 _coverage_unit_factor 严格一致）：
      - `coverage_unit == "万元"` → min_coverage × 10000
      - `coverage_unit == "元"`    → min_coverage × 1
      - 单位缺失 / 空串 / 非字符串 → **不换算**（不猜单位、不套任何乘数）
      - 单位不受支持（如 "亿元"）  → **不换算**（不静默套乘数）

    当 min_coverage 缺失、或单位不可信（无法确定可售最小保额）时，
    沿用既有兜底语义：**原保额的 60%**（`current * 0.6`）。

    ⚠️ SDI-4 整改 2026-11-09：旧实现在单位缺失时静默按「万元」换算 min_coverage，
    与旧 docstring 把缺省单位写成「元」相反 → 下限被放大 10000 倍，
    预算下调时的保额下限形同虚设。现与 _coverage_unit_factor 共用同一合同，
    **单位不可信时不套任何乘数**。
    """
    current = entry.get("coverage") or 0
    floor = None
    if product:
        raw_min = product.get("min_coverage")
        if raw_min is not None:
            factor, _unit_status = _coverage_unit_factor(product)
            if factor is not None:
                try:
                    floor = float(raw_min) * factor
                except (TypeError, ValueError):
                    floor = None
    if not floor or floor <= 0:
        return current * 0.6
    return min(floor, current)


def _coverage_cap_status(product):
    """返回 (cap, status)：可售保额上限（元）与该上限的可信度状态。

    status 取值：
      - "ok"                   —— max_coverage 与单位均可信，cap 为换算后的元值
      - "no_product"           —— 产品记录缺失
      - "max_coverage_missing" —— 产品库未提供 max_coverage
      - "max_coverage_invalid" —— max_coverage 非数值或非正数
      - "unit_untrusted"       —— max_coverage 有值但 coverage_unit 缺失/为空/非字符串
      - "unit_unsupported"     —— max_coverage 有值但 coverage_unit 是受支持之外的值

    ⚠️ SDI-4 整改 2026-11-09：**单位口径由 _coverage_unit_factor 单一来源定义**。
    旧实现在单位缺失时静默套「万元」系数（×10000），而旧 docstring 却把缺省单位
    写成「元」—— 文档与实现相反；若某条记录的真实单位是「元」，
    按万元换算会把上限**放大 10000 倍**，反而放行超出真实可售上限的保额。
    现在：
      - 单位缺失 → **不猜单位、不做换算**，返回 (None, "unit_untrusted")；
      - 单位不受支持 → **不静默套乘数**，返回 (None, "unit_unsupported")；
      两者都不设上限（不虚构上限），由调用方写入留痕 + 对外披露。

    ⚠️ 判定顺序：max_coverage 的三类状态（缺失 / 非数值 / 非正数）保持**原样不变**，
    单位合同仅在 max_coverage 存在且为正数时生效。
    """
    if not product:
        return None, "no_product"
    raw = product.get("max_coverage")
    if raw is None:
        return None, "max_coverage_missing"
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None, "max_coverage_invalid"
    if value <= 0:
        return None, "max_coverage_invalid"
    factor, unit_status = _coverage_unit_factor(product)
    if unit_status == "unit_missing":
        # 单位缺失 → 单位不可信：不换算、不设上限（交给调用方披露）
        return None, "unit_untrusted"
    if unit_status == "unit_unsupported":
        # 单位是受支持之外的值 → 显式标记：不换算、不设上限
        return None, "unit_unsupported"
    if factor is None:
        return None, "unit_untrusted"
    return int(value * factor), "ok"


def _coverage_cap(product):
    """保额上限：产品 max_coverage（可售保额上限）按 coverage_unit 换算为元；不可信时返回 None。

    ⚠️ R4 整改 2026-11-08（同步自 insurance-advisor-china 主库）：
    产品库中 max_coverage 是**可售保额上限**，
    如「安心少儿意外险」max_coverage=50（万元）= 500,000 元，
    方案原写死 2,500,000 元 → 超上限 50 倍（对外虚报可售保额）。

    ⚠️ SDI-4 整改 2026-11-09：**单位口径（与实现严格一致，来源 = _coverage_unit_factor）**
      - `coverage_unit == "万元"` → ×10000 换算为元；
      - `coverage_unit == "元"`    → ×1，不换算；
      - `coverage_unit` 缺失/为空/非字符串 且 max_coverage 有值 → **单位不可信**：
        **不**按万元、也**不**按元静默换算 → 返回 None（不设上限），
        由调用方写入留痕并对外披露（见 _apply_coverage_cap / _build_coverage_disclaimers）。
        （实测产品库中 max_coverage 有值的记录 `coverage_unit` 全部为「万元」，
          「有值但缺单位」的记录数为 0；此分支为防御性口径。）
      - `coverage_unit` 为受支持之外的值（如 "亿元" / "USD"） → **不静默套乘数**：
        返回 None（不设上限），并由调用方以 `unit_unsupported` 状态留痕 + 披露。
      - max_coverage 缺失（None / 非数值 / 非正数）→ 返回 None，**不设上限**，
        调用方须如实标注「该产品未提供可售保额上限」，不得假装有上限。

    Returns:
        int | None: 可售保额上限（元）；上限未知或不可信时为 None。
    """
    cap, _status = _coverage_cap_status(product)
    return cap


def _apply_coverage_cap(plan, product, desired_coverage, entry_type=None, entry_name=None):
    """把期望保额夹到产品 max_coverage 上限；触顶时写入 budget_adjustments。

    ⚠️ F4 整改 2026-11-09：**上限未知（cap is None）时不再静默放行**。
    旧实现原样返回期望保额且**不留任何痕迹** → 最终方案呈现一个「看起来很具体」
    却未经可售上限核实的保额，对用户构成误导。
    现在写入 `coverage_cap_unknown` 留痕（可审计），
    并由 _finalize_plan 汇总为对外披露（plan["coverage_disclaimers"]）。

    Returns:
        tuple[int, bool]: (最终保额, 是否因上限而被下调)
    """
    cap, cap_status = _coverage_cap_status(product)
    desired = int(desired_coverage or 0)
    if cap is None:
        # 上限未知/不可信 → 不设上限（不虚构上限），但必须留痕并披露
        plan.setdefault("budget_adjustments", []).append({
            "type": "coverage_cap_unknown",
            "product": entry_name,
            "product_type": entry_type,
            "requested_coverage": desired,
            "cap_status": cap_status,
            "max_coverage": (product or {}).get("max_coverage"),
            "coverage_unit": (product or {}).get("coverage_unit"),
            "reason": "该产品在产品库中未提供可核实的可售保额上限"
                      "（max_coverage 缺失/非数值/非正数，或保额单位不可信/不受支持），"
                      "此保额未经可售上限核实，请以保险公司正式测算为准",
        })
        return desired, False
    if desired <= cap:
        return desired, False
    plan.setdefault("budget_adjustments", []).append({
        "type": "coverage_capped",
        "product": entry_name,
        "product_type": entry_type,
        "requested_coverage": desired,
        "capped_to": cap,
        "max_coverage": product.get("max_coverage"),
        "coverage_unit": product.get("coverage_unit"),
        "reason": "方案保额超过该产品在产品库的可售保额上限（max_coverage），已按上限下调",
    })
    return cap, True


def _build_coverage_disclaimers(plan):
    """汇总「可售保额上限未经核实」的险种，生成对外披露文案。

    ⚠️ F4 整改 2026-11-09：审计原文指出
    「_coverage_cap 返回 None 时，_apply_coverage_cap 原样返回期望保额且不留痕迹，
      finalization 也不加对应披露 → 缺失/畸形/非正的 max_coverage 会产出
      一个看似具体、但无可核实可售上限的保险建议」。

    本函数把 budget_adjustments 中的 `coverage_cap_unknown` 记录汇总为
    顶层 `coverage_disclaimers`（list[str]），**必须真实出现在最终 JSON 输出里**。

    仅当确实存在上限未知的险种时才写入该键（无未知上限时**不新增空数组**，
    以免给所有方案引入无意义的空字段）。

    Returns:
        list[str]: 披露文案列表；无上限未知险种时返回空列表。
    """
    unknown = [a for a in (plan.get("budget_adjustments") or [])
               if isinstance(a, dict) and a.get("type") == "coverage_cap_unknown"]
    if not unknown:
        return []

    # 只披露**最终方案里实际保留**的险种：
    #   若某产品因保费超预算从未加入方案（或被 _enforce_budget 移除），
    #   它不在 plan["products"] 里 → 不该出现在本方案的保额披露中。
    final_names = {p.get("product_name") for p in (plan.get("products") or [])}
    if not final_names:
        return []
    unknown = [a for a in unknown if a.get("product") in final_names]
    if not unknown:
        return []

    # 按险种去重（同一险种可能多次留痕），保持出现顺序
    seen = []
    details = []
    for adj in unknown:
        label = adj.get("product_type") or "险种"
        name = adj.get("product")
        key = (label, name)
        if key in seen:
            continue
        seen.append(key)
        detail = f"{label}" + (f"「{name}」" if name else "")
        details.append(detail)

    n = len(details)
    plural = "、".join(details)
    return [
        f"本方案中有 {n} 个险种（{plural}）的可售保额上限未在产品库中核实："
        "产品库未提供可售保额上限，或保额单位不可信/不受支持，无法确认其可售上限。"
        "上述险种的建议保额**未经可售上限核实**，请以保险公司正式测算结果为准。",
    ]


def _refresh_coverage_text(entry, from_coverage, to_coverage):
    """保额变化后同步 key_benefits 中内嵌的保额数字。

    ⚠️ R7 整改 2026-11-07：原实现只在 `old_wan` 非零且文本里恰含「{old_wan}万」
    时替换 —— 以下两种虚报场景修不掉：
      ① 文本写死「100万保额」而实际保额并非 100 万（设计期硬编码 ≠ 实际保额）；
      ② 保额下调到 <1 万时 old_wan == 0，整段数字描述被原样保留。
    现改为：统一由**实际保额**派生出对外的保额表述。
    """
    kb = entry.get("key_benefits")
    if not isinstance(kb, str):
        return
    new_wan = to_coverage // 10000

    # ① 先做旧数字的精确替换（保留原有行为）
    old_wan = from_coverage // 10000
    if old_wan and f"{old_wan}万" in kb:
        kb = kb.replace(f"{old_wan}万", f"{new_wan}万")

    # ② 再统一校正文本中的**保额量词表述**，避免硬编码数字与实际保额不符
    entry["key_benefits"] = _normalize_coverage_claim(kb, to_coverage)


# 正文中「保额」前置的量词表述（含硬编码 100万 / 600万 / 百万医疗 等）
_COVERAGE_CLAIM_PATTERNS = (
    r"(\d+(?:\.\d+)?)万(?=保额|意外|医疗|重疾|身故|赔付|保障)",
    r"(\d+(?:\.\d+)?)万(?=，(?:仅需|含|含质子))",
    r"百万医疗",
)


def _coverage_claim_text(coverage):
    """由实际保额派生出对外的保额表述（万元）。"""
    wan = coverage // 10000
    if wan >= 1:
        return f"{wan}万"
    # < 1 万：如实表述为具体金额（千元级），不得谎称「百万」
    qian = round(coverage / 1000)
    return f"{qian}千" if qian else "保额较低"


def _normalize_coverage_claim(text, coverage):
    """把文本里的保额量词表述替换为由**实际保额**派生的表述。

    ⚠️ SDI-4 整改 2026-11-10：**补齐「数字+万+高保额」与「险种名+数字+万」两种形态**。
    旧实现只匹配「100万保额」「600万医疗」等「数字+万」紧跟关键词的形态，
    **漏掉了**「600万高保额」「医疗险600万保额」这类写法 →
    保额被 max_coverage 夹到 400 万后，对外仍宣称 600 万（虚报可售保额）。
    官方扫描原文（ai-insurance-advisor 2.3.8 SDI-4）：
    「The promised final reconciliation of coverage claims leaves the premium medical plan's
     hard-coded "600万高保额" unchanged when actual coverage is reduced.」
    修法：凡文本中出现「数字+万」且位于保额语境的，一律替换为实际保额表述。
    """
    if not isinstance(text, str) or not text:
        return text

    claim = _coverage_claim_text(coverage)

    def _sub_num(m):
        # 形如「100万保额」：用实际保额量词替换整个「数字+万」，保留后缀
        return claim + m.group(2)

    # ① 「数字+万」后紧跟保额类关键词（保额/高保额/意外/医疗/重疾/身故/赔付/保障/，）
    out = re.sub(r"(\d+(?:\.\d+)?)万(保额|高保额|意外|医疗|重疾|身故|赔付|保障|，)",
                 _sub_num, text)
    # ② 「数字+万」后紧跟逗号 + 常见后缀（，仅需 / ，含 / ，含质子）
    out = re.sub(r"(\d+(?:\.\d+)?)万(，(?:仅需|含|含质子))",
                 _sub_num, out)
    # ③ 「医疗险600万保额」这类「险种名+数字+万」已在 ① 覆盖（后缀是「保额」），
    #    但残留的裸「数字+万」紧跟在险种名之后（如「医疗险600万，…」）也替换。
    out = re.sub(r"((?:医疗险|意外险|重疾险|寿险|储蓄险))(\d+(?:\.\d+)?)万",
                 lambda m: m.group(1) + claim, out)
    # ④ 「百万医疗」——实际保额 <100 万时不得再称「百万」
    if "百万医疗" in out and coverage < 1000000:
        out = out.replace("百万医疗", f"{claim}医疗")
    # ⑤ 「百万」独立出现（无「医疗」后缀）时同样按实际保额校正
    if "百万" in out and coverage < 1000000:
        out = out.replace("百万", claim)
    return out


# ---------------------------------------------------------------------------
# R7 整改 2026-11-07：方案描述与实际构成一致性
# ---------------------------------------------------------------------------
# 险种类型 → 描述中使用的名称（顺序即描述中列举的优先级）
_TYPE_LABELS = (
    ("定期寿险", "定期寿险"),
    ("重疾险", "重疾保障"),
    ("医疗险", "医疗保障"),
    ("意外险", "意外保障"),
    ("储蓄险", "养老储蓄规划"),
)

# 险种类型 → 该险种被移除后不得出现在描述/卖点中的关键词
_TYPE_BANNED_WORDS = {
    "定期寿险": ("寿险",),
    "重疾险": ("重疾",),
    "医疗险": ("医疗",),
    "意外险": ("意外",),
    "储蓄险": ("养老", "储蓄"),
}


def _build_plan_description(plan_name, products):
    """按**实际剩余险种**生成方案描述。

    ⚠️ R7 整改 2026-11-07：原先 description 写死（如「保障全面，含重疾保障」
    「高保额全方位保障，另含养老储蓄规划」），在产品被移除后不再成立 → 属于
    对外虚报。本函数以 plan["products"] 为唯一事实来源动态生成。

    Args:
        plan_name: 方案名（基础版 / 标准版 / 全面版）
        products: 方案实际保留的产品列表

    Returns:
        描述文本；产品为空时明确说明方案不覆盖任何险种。
    """
    present = {p.get("type") for p in (products or [])}
    if not present:
        return f"{plan_name}：当前预算不足以配置任何险种，方案暂不覆盖具体保障责任"

    labels = [label for ptype, label in _TYPE_LABELS if ptype in present]
    scope = "、".join(labels)

    # 全面版卖点：仅当储蓄险真实保留时才提「养老储蓄规划」
    if plan_name == "全面版":
        if "储蓄险" in present:
            others = [l for ptype, l in _TYPE_LABELS
                      if ptype in present and ptype != "储蓄险"]
            other_scope = "、".join(others)
            return (f"高保额全方位保障（{other_scope}），另含养老储蓄规划")
        return f"高保额全方位保障（{scope}）"

    # 标准版卖点：仅当重疾险真实保留时才提「含重疾保障」
    if plan_name == "标准版":
        if "重疾险" in present:
            return f"保障全面，含重疾保障（{scope}），适合大多数家庭"
        return f"保障基础，含{scope}，适合大多数家庭"

    # 基础版
    return f"以最低成本建立基础保障，覆盖核心风险（{scope}）"


def _prune_plan_features(plan, features):
    """剔除 features 中与实际保留险种不符的条目。

    被移除险种对应的卖点（如「重疾险提供终身保障」「医疗险600万保额」
    「可选储蓄险，为养老做准备」）必须同步消失。
    """
    present = {p.get("type") for p in plan.get("products", [])}
    kept = []
    for feat in features or []:
        if not isinstance(feat, str):
            continue
        drop = False
        for ptype, words in _TYPE_BANNED_WORDS.items():
            if ptype in present:
                continue
            # 只在该条目明确提到被移除险种时剔除；
            # 「医疗险20年保证续保」这类提及具体险种的条目同样处理。
            if any(w in feat for w in words):
                drop = True
                break
        if not drop:
            kept.append(feat)
    return kept


def _sync_features_coverage_claims(plan):
    """按各险种的**最终保额**重算 features 中的保额表述。

    ⚠️ SDI-4 整改 2026-11-11（v2.4.2）：features 是在**设计期**生成的，
    早于 `_enforce_budget()` 的预算下调与产品上限夹逼；出口处只校正了
    `key_benefits`，features 里的保额数字仍停留在调整前的值 →
    对外出现「实际保额 100 万、卖点写 400 万」的虚报。

    修法：在**出口处**（所有调整完成后）按每个保留产品的最终保额，
    重写 features 中与该险种相关的保额表述。

    实现要点：
      - 先用 `_prune_plan_features` 剔除已移除险种的卖点；
      - 再对每条 feature：若它提及某个**仍保留**的险种，
        且包含「数字+万」形态的保额表述，则用该险种**最终保额**重算；
      - 未能确定对应险种的 feature 原样保留（不做猜测式替换）。
    """
    feats = _prune_plan_features(plan, plan.get("features") or [])
    if not feats:
        return feats

    type_words = {
        "医疗险": "医疗险", "意外险": "意外险", "重疾险": "重疾险",
        "定期寿险": "定期寿险", "寿险": "定期寿险", "储蓄险": "储蓄险",
    }
    cov_by_type = {}
    for e in plan.get("products", []):
        t = e.get("type")
        if t and t not in cov_by_type:
            cov_by_type[t] = e.get("coverage") or 0

    out = []
    for feat in feats:
        if not isinstance(feat, str):
            out.append(feat)
            continue
        matched = None
        for word, ptype in type_words.items():
            if word in feat and ptype in cov_by_type:
                matched = cov_by_type[ptype]
                break
        if matched is None:
            out.append(feat)
            continue
        out.append(_normalize_coverage_claim(feat, matched))
    return out


# ---------------------------------------------------------------------------
# SDI-4 整改 2026-11-13：「年收入 N 倍」形态的卖点必须随最终保额同步
# ---------------------------------------------------------------------------
# ⚠️ 根因（官方复扫 ai-insurance-advisor 2.4.3 / insurance-advisor-china 2.4.3）：
#    出口同步 `_sync_features_coverage_claims()` 只处理「数字+万」形态的保额表述，
#    而 `_normalize_coverage_claim()` 的所有正则都围绕 `(\d+(?:\.\d+)?)万` 展开 ——
#    「年收入5倍」**不含「万」→ 根本不匹配** → 出口同步对它完全无效。
#    结果：预算下调（_enforce_budget）/ 上限夹逼（_apply_coverage_cap）之后，
#    重疾险实际保额可能远低于 annual_income × 5，卖点却仍宣称 5 倍 → **虚报保额**。
#    官方原文：
#    「The comprehensive plan retains a five-times-income coverage claim even when
#     actual critical-illness coverage is capped or reduced.」

# 「X险保额[高达|可达|达|为]年收入N倍」形态的卖点表述。
_INCOME_MULTIPLE_CLAIM_RE = re.compile(
    r"(?P<ptype>定期寿险|储蓄险|重疾险|医疗险|意外险|寿险)保额"
    r"(?:高达|可达|达|为)?年收入(?P<mult>\d+(?:\.\d+)?)倍")

# 险种关键词 → 方案产品表中的 type（与 _sync_features_coverage_claims 同口径）
_FEATURE_TYPE_WORDS = {
    "医疗险": "医疗险", "意外险": "意外险", "重疾险": "重疾险",
    "定期寿险": "定期寿险", "寿险": "定期寿险", "储蓄险": "储蓄险",
}


def _format_income_multiple(value):
    """倍数的对外表述：1 位小数，去掉多余的 .0（5.0 → 5；4.6 → 4.6）。"""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


def _income_multiple_fallback(ptype, coverage):
    """倍数无法给出时的如实表述：直接说明实际保额（复用库内单位单一事实来源）。

    ⚠️ 绝对金额一律走 `_coverage_claim_text()` —— 不另立换算规则（F5/F7 铁律）。
    """
    claim = _coverage_claim_text(coverage)
    if claim == "保额较低":
        # 避免出现「重疾险保额保额较低」这类重复表述
        return f"{ptype}保额较低"
    return f"{ptype}保额{claim}"


def _sync_features_income_multiple_claims(plan, annual_income):
    """按**最终保额**重算 features 中「年收入 N 倍」形态的卖点表述。

    ⚠️ SDI-4 整改 2026-11-13（官方 2.4.3 复扫）：
       「重疾险保额高达年收入5倍」是**设计期写死**的卖点，而出口同步只处理
       「数字+万」形态 → 该表述在预算下调 / 上限夹逼后仍宣称 5 倍（虚报保额）。

    修法：在**出口处**（`_enforce_budget` 完成后）按最终保额重算倍数：
      - 倍数 = 最终保额 / 年收入（两者同为「元」，比值与单位无关 → 无需换算；
        绝对金额的对外渲染一律走 `_coverage_claim_text()`，沿用库内单位单一事实来源）；
      - 实际倍数 ≥ 原文案声明的倍数 → **保持原样**（不得弱于原文案，
        且不产生「5倍 → 5.0倍」这类无意义 diff）；
      - 实际倍数 < 原文案 → 按实际倍数重写（**向下**取到 1 位小数，
        保证对外表述永远不大于实际值 —— 宁可少说不可多说）；
      - 年收入缺失 / 为 0 → **不写倍数**，改用实际保额表述。

    Args:
        plan: 方案 dict（`products` 为最终保额的唯一事实来源）
        annual_income: 年收入（元）

    Returns:
        list[str]: 同步后的 features（幂等）。
    """
    feats = plan.get("features") or []
    if not feats:
        return feats

    # 各险种最终保额（取第一个匹配项，与 _sync_features_coverage_claims 同口径）
    cov_by_type = {}
    for e in plan.get("products", []):
        t = e.get("type")
        if t and t not in cov_by_type:
            cov_by_type[t] = e.get("coverage") or 0
    if not cov_by_type:
        return feats

    def _rewrite(text):
        def _one(m):
            ptype = _FEATURE_TYPE_WORDS.get(m.group("ptype"))
            if ptype is None or ptype not in cov_by_type:
                # 该险种不在最终方案里 → 交由 _prune_plan_features 处理，不在此重复剔除
                return m.group(0)
            coverage = cov_by_type[ptype]
            claimed = float(m.group("mult"))
            if not annual_income or annual_income <= 0:
                # 年收入缺失 / 为 0 → **不写倍数**，改为如实表述实际保额
                return _income_multiple_fallback(m.group("ptype"), coverage)
            ratio = coverage / annual_income
            if ratio >= claimed:
                # 实际倍数仍 ≥ 原文案 → **保持原样**（不得弱于原文案）
                return m.group(0)
            # 实际倍数 < 原文案 → 按实际倍数重写。先按 1 位小数四舍五入，
            # 若四舍五入会**超过**真实倍数，则改为向下取整 —— 对外表述永远
            # 不大于实际值（宁可少说不可多说）。
            new_mult = round(ratio, 1)
            if new_mult > ratio:
                new_mult = math.floor(ratio * 10) / 10
            if new_mult < 0.1:
                # 倍数过小，倍数形态已无参考意义 → 改为如实表述实际保额
                return _income_multiple_fallback(m.group("ptype"), coverage)
            return (f"{m.group('ptype')}保额为年收入"
                    f"{_format_income_multiple(new_mult)}倍")
        return _INCOME_MULTIPLE_CLAIM_RE.sub(_one, text)

    return [_rewrite(f) if isinstance(f, str) else f for f in feats]


def _enforce_budget(plan, budget, annual_income, age=None, gender=None,
                    product_index=None, removal_order=None):
    """把方案年保费压到年度保费上限以内。

    步骤：
      1. 若 annual_premium > budget，从最后加入的产品开始按比例下调 coverage
         （下限 = 产品 min_coverage，无则用原保额 60%），用同一
         calculate_product_premium 重算，直到 <= budget 或无可下调空间。
      2. 仍超预算：按 removal_order 依次移除险种
         （可选险种优先；核心险种兜底：重疾险 → 定期寿险）。
      3. 兜底：removal_order 走完仍超预算时，从后往前移除剩余险种，
         直到年保费 <= 上限或产品列表为空（此时年保费 = 0）。
      4. 每次调整写入 plan["budget_adjustments"]。
      5. 产品列表为空 → budget_planning["方案可行性"] 明确说明预算不足，
         绝不允许返回「超预算却不说原因」的方案。

    Args:
        plan: 方案 dict（含 products / annual_premium）
        budget: 年度保费上限
        annual_income: 年收入（用于占年收入比）
        age / gender: 保费重算所需
        product_index: (type, name) → 产品记录
        removal_order: 移除可选险种的顺序（产品 type 列表）
    """
    plan.setdefault("budget_adjustments", [])
    adjustments = plan["budget_adjustments"]
    product_index = product_index or {}
    removal_order = removal_order or []

    if budget is None:
        return plan
    if budget <= 0:
        # 年度保费上限为 0（或收入为 0 导致上限为 0）：无法配置任何险种，
        # 方案置为「不可行」：年保费 0、产品列表为空，并留下审计记录。
        for entry in list(plan.get("products", [])):
            adjustments.append({
                "type": "product_removed",
                "product": entry.get("product_name"),
                "product_type": entry.get("type"),
                "removed_coverage": entry.get("coverage"),
                "removed_premium": round(entry.get("annual_premium", 0), 2),
                "reason": "年度保费上限为 0，无法配置任何险种，方案置为不可行",
            })
        plan["products"] = []
        plan["annual_premium"] = 0
        plan["total_coverage"] = 0
        return plan

    # ---- 步骤 1：按比例下调保额 ----
    # 从最后加入的产品开始；逐个下调到「该产品可承受的最大保额」或下限。
    # 即使某产品降到下限仍无法独自把总保费拉进预算，也照样降到下限，
    # 然后继续处理更早加入的产品（直到总保费 <= budget 或所有产品都无下调空间）。
    for entry in reversed(list(plan.get("products", []))):
        if plan["annual_premium"] <= budget:
            break
        product = product_index.get((entry.get("type"), entry.get("product_name")))
        if product is None or age is None or gender is None:
            continue
        current_coverage = entry.get("coverage") or 0
        floor = _coverage_floor(product, entry)
        if current_coverage <= floor:
            continue  # 已到下限，无下调空间

        payment_term = entry.get("payment_term")

        def total_at(coverage, _entry=entry, _product=product, _term=payment_term):
            """给定保额下的方案总保费。"""
            premium = calculate_product_premium(_product, age, gender, coverage, _term)
            return plan["annual_premium"] - _entry["annual_premium"] + premium

        # 保额与保费单调相关 → 二分查找可行上限（找不到则取下限）
        lo, hi = int(floor), int(current_coverage)
        best = int(floor)
        while lo <= hi:
            mid = (lo + hi) // 2
            if total_at(mid) <= budget:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        old_coverage = current_coverage
        old_premium = entry["annual_premium"]
        entry["coverage"] = best
        entry["annual_premium"] = calculate_product_premium(product, age, gender, best, payment_term)
        plan["annual_premium"] = plan["annual_premium"] - old_premium + entry["annual_premium"]
        # ⚠️ R7 整改 2026-11-07：下调保额时必须同步扣减 total_coverage，
        #    否则会出现「实际保额 5 万、对外报告 630 万」的保额虚报。
        plan["total_coverage"] = plan.get("total_coverage", 0) - (old_coverage - best)
        _refresh_coverage_text(entry, old_coverage, best)
        adjustments.append({
            "type": "coverage_downscale",
            "product": entry.get("product_name"),
            "product_type": entry.get("type"),
            "from_coverage": old_coverage,
            "to_coverage": best,
            "premium_before": round(old_premium, 2),
            "premium_after": round(entry["annual_premium"], 2),
            "reason": "超出年度保费预算，按比例下调保额",
        })

    # ---- 步骤 2：移除险种（可选险种优先，核心险种兜底）----
    # removal_order 中排在后面的为核心险种（重疾险 / 定期寿险）：
    # min_coverage 是产品「可售」的最小保额，不是「必须卖这么多」，
    # 因此降到下限仍超预算时，允许移除该产品，而不是硬撑出一个超预算方案。
    def _remove_entry(idx, reason, level):
        """移除一个险种并同步 total_coverage（沿用原有增量口径）。"""
        entry = plan["products"].pop(idx)
        premium = entry.get("annual_premium", 0)
        plan["annual_premium"] -= premium
        plan["total_coverage"] -= entry.get("coverage", 0)
        adjustments.append({
            "type": "product_removed",
            "product": entry.get("product_name"),
            "product_type": entry.get("type"),
            "removed_coverage": entry.get("coverage"),
            "removed_premium": round(premium, 2),
            "reason": reason,
            "coverage_level": level,
        })

    for product_type in removal_order:
        if plan["annual_premium"] <= budget:
            break
        for idx in range(len(plan.get("products", [])) - 1, -1, -1):
            entry = plan["products"][idx]
            if entry.get("type") != product_type:
                continue
            is_core = product_type in _CORE_COVERAGE_TYPES
            _remove_entry(
                idx,
                ("超出年度保费预算且保额已降至可售最小保额仍超上限，兜底移除该核心险种"
                 if is_core else
                 "超出年度保费预算且保额无可下调空间，移除该可选险种"),
                "core" if is_core else "optional",
            )
            break

    # ---- 步骤 3：兜底移除剩余险种（removal_order 未覆盖的类型）----
    # 目的只有一个：保证返回的方案年保费恒不超过年度保费上限。
    while plan["annual_premium"] > budget and plan.get("products"):
        entry = plan["products"][-1]
        _remove_entry(
            len(plan["products"]) - 1,
            "超出年度保费上限，兜底移除该险种以保证方案不超预算",
            "core" if entry.get("type") in _CORE_COVERAGE_TYPES else "optional",
        )

    plan["annual_premium"] = max(0.0, round(plan["annual_premium"], 2))
    plan["total_coverage"] = max(0, plan.get("total_coverage", 0))
    return plan


def _attach_budget_planning(plan, budget, annual_income, ratio, note=""):
    """为方案附加 budget_planning 块。"""
    premium = round(plan["annual_premium"], 2)
    cap = round(budget, 2)
    in_budget = premium <= cap + 0.01
    plan["budget_planning"] = {
        "年度保费上限": cap,
        "方案年保费": premium,
        "占年收入比": round(premium / annual_income * 100, 1) if annual_income else None,
        "是否在预算内": in_budget,
        "说明": "保费上限 = min(年度预算, 年收入×比例)；超出部分已自动下调保额、"
                "移除可选险种，必要时兜底移除核心险种（重疾险→定期寿险）",
        "上限口径": f"min(年度预算 {budget}, 年收入 × {int(ratio * 100)}%)",
    }
    if not plan.get("products"):
        # 产品列表为空 → 方案不可行，必须说明原因，不允许静默返回一个空壳方案
        removed_core = [a for a in plan.get("budget_adjustments", [])
                        if a.get("type") == "product_removed"
                        and a.get("product_type") in _CORE_COVERAGE_TYPES]
        if removed_core:
            detail = ("核心险种（重疾险/定期寿险）已降至可售最小保额仍超上限，"
                      "兜底移除后方案为空")
        else:
            detail = "年度保费上限过低，任何一个险种（含最低保额）都无法在上限内配置"
        plan["budget_planning"]["方案可行性"] = (
            f"不可行：{detail}。当前方案年保费已置为 0，"
            "请提高年度保费预算，或仅在预算内配置基础医疗/意外保障后再行评估。"
        )
        plan["budget_planning"]["方案状态"] = "不可行"
    else:
        removed_core = [a for a in plan.get("budget_adjustments", [])
                        if a.get("type") == "product_removed"
                        and a.get("product_type") in _CORE_COVERAGE_TYPES]
        if removed_core:
            plan["budget_planning"]["方案可行性"] = (
                "可行（已按预算上限调整）：因年度保费上限偏低，"
                f"已移除核心险种 {'、'.join(a.get('product_type') for a in removed_core)}，"
                "剩余保障不足以覆盖该险种责任，请知悉保障缺口。"
            )
        else:
            plan["budget_planning"]["方案可行性"] = "可行：方案年保费在年度保费上限内"
        plan["budget_planning"]["方案状态"] = "可行"
    if note:
        plan["budget_planning"]["备注"] = note
    return plan


def design_basic_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """基础版方案：低保费基本保障"""
    budget = min(annual_budget, annual_income * 0.10)  # 上限 = min(年度预算, 年收入 10%)
    plan = {
        "plan_name": "基础版",
        "description": "以最低成本建立基础保障，覆盖核心风险",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 选择性价比高的
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    if not tl_products:
        return _finalize_plan(plan, budget, annual_income, 0.10, age, gender, products)
    tl_product = min(tl_products, key=lambda x: x.get("premium_per_10k", 999))
    tl_coverage = min(coverage_needs.get("death", 500000), 1000000)
    # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
    tl_coverage, _capped = _apply_coverage_cap(
        plan, tl_product, tl_coverage, "定期寿险", tl_product.get("name"))
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    if plan["annual_premium"] + tl_premium <= budget:
        plan["products"].append({
            "type": "定期寿险",
            "product_name": tl_product["name"],
            "company": tl_product["company"],
            "coverage": tl_coverage,
            "annual_premium": tl_premium,
            "payment_term": "20年",
            "coverage_period": "至60周岁",
            "key_benefits": "身故/全残保障，保护家人"
        })
        plan["annual_premium"] += tl_premium
        plan["total_coverage"] += tl_coverage

    # 意外险（保费校验使用 budget，不再使用 budget * 1.2）
    ac_products = [p for p in products if p["type"] == "意外险"]
    if ac_products:
        ac_product = min(ac_products, key=lambda x: x.get("premium_per_10k", 999))
        ac_coverage = min(annual_income * 5, 3000000)
        # ⚠️ R4 整改 2026-11-08：意外险保额夹到产品 max_coverage
        #    （如「安心少儿意外险」max_coverage=50 万 → 上限 500,000 元）
        ac_coverage, _capped = _apply_coverage_cap(
            plan, ac_product, ac_coverage, "意外险", ac_product.get("name"))
        ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
        if plan["annual_premium"] + ac_premium <= budget:
            plan["products"].append({
                "type": "意外险",
                "product_name": ac_product["name"],
                "company": ac_product["company"],
                "coverage": ac_coverage,
                "annual_premium": ac_premium,
                "payment_term": "年交",
                "coverage_period": "1年",
                "key_benefits": "意外身故/伤残/医疗，100万保额仅需几百元"
            })
            plan["annual_premium"] += ac_premium
            plan["total_coverage"] += ac_coverage

    # 医疗险（加入前必须校验累计保费 ≤ budget）
    # ⚠️ SDI-4 整改 2026-11-07：选品改用**结构化续保字段**（原先对 notes 做子串匹配），
    #    展示字段由真实字段派生（原先无条件写死 "coverage_period": "1年"）。
    mi_product, mi_limitation = select_medical_product(products, min_guaranteed_years=None)
    if mi_product:
        mi_coverage = 2000000
        mi_coverage, _capped = _apply_coverage_cap(
            plan, mi_product, mi_coverage, "医疗险", mi_product.get("name"))
        mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
        if plan["annual_premium"] + mi_premium <= budget:
            mi_coverage_period = derive_medical_coverage_period(mi_product)
            plan["products"].append({
                "type": "医疗险",
                "product_name": mi_product["name"],
                "company": mi_product["company"],
                "coverage": mi_coverage,
                "annual_premium": mi_premium,
                "payment_term": "年交",
                "coverage_period": mi_coverage_period,
                "key_benefits": derive_medical_key_benefits(
                    mi_product, _medical_base_claim(mi_product), mi_coverage_period)
            })
            plan["annual_premium"] += mi_premium
            plan["total_coverage"] += mi_coverage
            if mi_limitation:
                plan.setdefault("limitations", []).append({
                    "type": "coverage_limit",
                    "product_type": "医疗险",
                    "product": mi_product["name"],
                    "requirement": mi_limitation["requirement"],
                    "reason": mi_limitation["reason"],
                    "actual_coverage_period": mi_coverage_period,
                })
        else:
            plan.setdefault("budget_adjustments", []).append({
                "type": "product_skipped",
                "product": mi_product["name"],
                "product_type": "医疗险",
                "reason": "加入医疗险后累计保费将超出年度保费上限，未加入",
            })

    return _finalize_plan(plan, budget, annual_income, 0.10, age, gender, products,
                          removal_order=["医疗险", "意外险", "定期寿险"])


def design_standard_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """标准版方案：全面基础保障+重疾"""
    budget = min(annual_budget, annual_income * 0.15)  # 上限 = min(年度预算, 年收入 15%)
    plan = {
        "plan_name": "标准版",
        "description": "保障全面，含重疾保障，适合大多数家庭",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 推荐中国人寿星Combo
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    if not tl_products:
        return _finalize_plan(plan, budget, annual_income, 0.15, age, gender, products)
    tl_product = next((p for p in tl_products if "星" in p["name"]), tl_products[0])
    tl_coverage = min(coverage_needs.get("death", 1000000), 2000000)
    # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
    tl_coverage, _capped = _apply_coverage_cap(
        plan, tl_product, tl_coverage, "定期寿险", tl_product.get("name"))
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    plan["products"].append({
        "type": "定期寿险",
        "product_name": tl_product["name"],
        "company": tl_product["company"],
        "coverage": tl_coverage,
        "annual_premium": tl_premium,
        "payment_term": "20年",
        "coverage_period": "至60周岁",
        "key_benefits": "身故/全残保障，保费低保障高"
    })
    plan["annual_premium"] += tl_premium
    plan["total_coverage"] += tl_coverage

    # 重疾险 - 推荐平安福或国寿福（SDI-4 整改 2026-11-13）
    crx_products = [p for p in products if p["type"] == "重疾险"]
    # 兜底优先取 coverage_period 非空的产品（空值无法对外表述保障期）
    crx_products_nonempty = [p for p in crx_products
                              if (p.get("coverage_period") or "").strip()]
    crx_product = None
    if crx_products:
        crx_product = next(
            (p for p in crx_products
             if "福" in p["name"] and "终身" in (p.get("coverage_period") or "")),
            (crx_products_nonempty or crx_products)[0])
        crx_coverage = min(coverage_needs.get("critical_illness", annual_income * 3), 500000)
        # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
        crx_coverage, _capped = _apply_coverage_cap(
            plan, crx_product, crx_coverage, "重疾险", crx_product.get("name"))
        crx_premium = calculate_product_premium(crx_product, age, gender, crx_coverage, "20年")
        plan["products"].append({
            "type": "重疾险",
            "product_name": crx_product["name"],
            "company": crx_product["company"],
            "coverage": crx_coverage,
            "annual_premium": crx_premium,
            "payment_term": "20年",
            # ⚠️ SDI-4 整改 2026-11-13：保障期由**产品真实字段**派生，不写死
            "coverage_period": _crx_coverage_period(crx_product),
            # ⚠️ SDI-4 整改 2026-11-13：病种/轻症宣称须有 highlights 来源
            "key_benefits": _crx_key_benefits(crx_product, crx_coverage, "standard")
        })
        plan["annual_premium"] += crx_premium
        plan["total_coverage"] += crx_coverage

    # 医疗险 - 按**真实续保字段**选保证续保20年的（SDI-4 整改 2026-11-07）
    mi_product, mi_limitation = select_medical_product(products, min_guaranteed_years=20)
    if mi_product:
        mi_coverage = 4000000
        mi_coverage, _capped = _apply_coverage_cap(
            plan, mi_product, mi_coverage, "医疗险", mi_product.get("name"))
        mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
        mi_coverage_period = derive_medical_coverage_period(mi_product)
        plan["products"].append({
            "type": "医疗险",
            "product_name": mi_product["name"],
            "company": mi_product["company"],
            "coverage": mi_coverage,
            "annual_premium": mi_premium,
            "payment_term": "年交",
            "coverage_period": mi_coverage_period,
            "key_benefits": derive_medical_key_benefits(
                mi_product, _medical_base_claim(mi_product), mi_coverage_period)
        })
        plan["annual_premium"] += mi_premium
        plan["total_coverage"] += mi_coverage
        if mi_limitation:
            # 无「保证续保20年」的合格产品 → 如实报告限制，不谎称已满足
            plan.setdefault("limitations", []).append({
                "type": "coverage_limit",
                "product_type": "医疗险",
                "product": mi_product["name"],
                "requirement": mi_limitation["requirement"],
                "reason": mi_limitation["reason"],
                "actual_coverage_period": mi_coverage_period,
            })

    # 意外险
    ac_products = [p for p in products if p["type"] == "意外险"]
    if ac_products:
        ac_product = next((p for p in ac_products if "百万" in p["name"]), ac_products[0])
        ac_coverage = min(annual_income * 5, 3000000)
        # ⚠️ R4 整改 2026-11-08：意外险保额夹到产品 max_coverage
        ac_coverage, _capped = _apply_coverage_cap(
            plan, ac_product, ac_coverage, "意外险", ac_product.get("name"))
        ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
        plan["products"].append({
            "type": "意外险",
            "product_name": ac_product["name"],
            "company": ac_product["company"],
            "coverage": ac_coverage,
            "annual_premium": ac_premium,
            "payment_term": "年交",
            "coverage_period": "1年",
            "key_benefits": "含猝死保障，意外医疗不限社保"
        })
        plan["annual_premium"] += ac_premium
        plan["total_coverage"] += ac_coverage

    # features 中的医疗险描述由**真实选中产品**派生（SDI-4 整改 2026-11-07）
    mi_entry = next((e for e in plan["products"] if e["type"] == "医疗险"), None)
    if mi_entry:
        mi_feature = f"医疗险{mi_entry['coverage_period']}"
    else:
        mi_feature = "本方案未包含医疗险"
    plan["features"] = [
        "保障全面：寿险+重疾+医疗+意外",
        # ⚠️ SDI-4 整改 2026-11-13：重疾卖点由**真实选中产品**派生（原写死「终身保障」）
        _crx_feature(crx_product),
        mi_feature,
        "定期寿险覆盖家庭经济责任期",
        "年保费已按年度保费上限（min(年度预算, 年收入×15%））校验"
    ]

    return _finalize_plan(plan, budget, annual_income, 0.15, age, gender, products,
                          removal_order=["意外险", "医疗险", "重疾险", "定期寿险"])


def design_premium_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """全面版方案：高保额全面保障+储蓄"""
    budget = min(annual_budget, annual_income * 0.20)  # 上限 = min(年度预算, 年收入 20%)
    plan = {
        "plan_name": "全面版",
        "description": "高保额全方位保障，另含养老储蓄规划",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 高保额
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    if not tl_products:
        return _finalize_plan(plan, budget, annual_income, 0.20, age, gender, products)
    tl_product = tl_products[0]
    tl_coverage = min(coverage_needs.get("death", 2000000), 5000000)
    # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
    tl_coverage, _capped = _apply_coverage_cap(
        plan, tl_product, tl_coverage, "定期寿险", tl_product.get("name"))
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    plan["products"].append({
        "type": "定期寿险",
        "product_name": tl_product["name"],
        "company": tl_product["company"],
        "coverage": tl_coverage,
        "annual_premium": tl_premium,
        "payment_term": "20年",
        "coverage_period": "至60/65周岁",
        "key_benefits": f"高保额{tl_coverage//10000}万，覆盖所有家庭责任"
    })
    plan["annual_premium"] += tl_premium
    plan["total_coverage"] += tl_coverage

    # 重疾险 - 多次赔付型（SDI-4 整改 2026-11-13）
    # ⚠️ 原条件 "多次" in (p.get("core_coverage") or "") 对 660 款重疾险**恒为假**
    #    （core_coverage 全空）→ 永远退化成兜底任意一款 → 官方 finding 的
    #    「fallback product whose terms have not been verified」根源。
    #    修法：口径改为权威字段 subtype（含「多次」的在售 27 款）。
    crx_products = [p for p in products if p["type"] == "重疾险"
                    and _crx_is_multi(p)]
    crx_multi_selected = bool(crx_products)
    if not crx_products:
        crx_products = [p for p in products if p["type"] == "重疾险"]
        crx_products_nonempty = [p for p in crx_products
                                  if (p.get("coverage_period") or "").strip()]
        crx_products = crx_products_nonempty or crx_products
    if crx_products:
        crx_product = crx_products[0]
        crx_coverage = min(coverage_needs.get("critical_illness", annual_income * 5), 500000)
        # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
        crx_coverage, _capped = _apply_coverage_cap(
            plan, crx_product, crx_coverage, "重疾险", crx_product.get("name"))
        crx_premium = calculate_product_premium(crx_product, age, gender, crx_coverage, "20年")
        plan["products"].append({
            "type": "重疾险",
            "product_name": crx_product["name"],
            "company": crx_product["company"],
            "coverage": crx_coverage,
            "annual_premium": crx_premium,
            "payment_term": "20年",
            # ⚠️ SDI-4 整改 2026-11-13：保障期由**产品真实字段**派生，不写死
            "coverage_period": _crx_coverage_period(crx_product),
            # ⚠️ SDI-4 整改 2026-11-13：多次赔付/终身保障须分别按 subtype / is_lifetime 授权
            "key_benefits": _crx_key_benefits(crx_product, crx_coverage, "premium")
        })
        plan["annual_premium"] += crx_premium
        plan["total_coverage"] += crx_coverage
        if not crx_multi_selected:
            # 无多次赔付型合格品 → 如实报告限制，不谎称已满足
            # ⚠️ 文案刻意不用「多次赔付」字样，避免与对外宣称混淆
            plan.setdefault("limitations", []).append({
                "type": "coverage_limit",
                "product_type": "重疾险",
                "product": crx_product["name"],
                "requirement": "含多次给付责任的重疾险",
                "reason": "当前产品库在售重疾险中无符合该责任结构的产品，已选保障范围最接近者",
            })

    # 医疗险 - 600万高保额
    # ⚠️ SDI-4 整改 2026-11-07：选品规则（600 万偏好）保持原样，
    #    仅把展示字段由**真实续保字段**派生（原先无条件写死 "1年可续保"）。
    def _prefer_600w(pool):
        return next((p for p in pool if "600" in (p.get("core_coverage") or "")), pool[0])

    mi_product, mi_limitation = select_medical_product(
        products, min_guaranteed_years=None, prefer=_prefer_600w)
    if mi_product:
        mi_coverage = 6000000
        mi_coverage, _capped = _apply_coverage_cap(
            plan, mi_product, mi_coverage, "医疗险", mi_product.get("name"))
        mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
        mi_coverage_period = derive_medical_coverage_period(mi_product)
        plan["products"].append({
            "type": "医疗险",
            "product_name": mi_product["name"],
            "company": mi_product["company"],
            "coverage": mi_coverage,
            "annual_premium": mi_premium,
            "payment_term": "年交",
            "coverage_period": mi_coverage_period,
            "key_benefits": derive_medical_key_benefits(
                mi_product, f"{_coverage_claim_text(mi_coverage)}高保额", mi_coverage_period)
        })
        plan["annual_premium"] += mi_premium
        plan["total_coverage"] += mi_coverage
        if mi_limitation:
            plan.setdefault("limitations", []).append({
                "type": "coverage_limit",
                "product_type": "医疗险",
                "product": mi_product["name"],
                "requirement": mi_limitation["requirement"],
                "reason": mi_limitation["reason"],
                "actual_coverage_period": mi_coverage_period,
            })

    # 意外险 - 100万
    ac_products = [p for p in products if p["type"] == "意外险"]
    if ac_products:
        ac_product = next((p for p in ac_products if "百万" in p["name"]), ac_products[0])
        ac_coverage = 1000000
        # ⚠️ R4 整改 2026-11-08：意外险保额夹到产品 max_coverage
        ac_coverage, _capped = _apply_coverage_cap(
            plan, ac_product, ac_coverage, "意外险", ac_product.get("name"))
        ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
        plan["products"].append({
            "type": "意外险",
            "product_name": ac_product["name"],
            "company": ac_product["company"],
            "coverage": ac_coverage,
            "annual_premium": ac_premium,
            "payment_term": "年交",
            "coverage_period": "1年",
            "key_benefits": "100万意外+猝死保障，意外医疗不限社保"
        })
        plan["annual_premium"] += ac_premium
        plan["total_coverage"] += ac_coverage

    # 储蓄险 - 养老规划（可选）
    if age <= 45:
        sa_products = [p for p in products if p["type"] == "储蓄险" and "养老" in (p.get("notes") or "")]
        if not sa_products:
            sa_products = [p for p in products if p["type"] == "储蓄险"]
        if sa_products and plan["annual_premium"] + 10000 <= budget:
            sa_product = sa_products[0]
            sa_coverage = 100000
            # ⚠️ R4 整改 2026-11-08：保额不得超产品可售上限（max_coverage）
            sa_coverage, _capped = _apply_coverage_cap(
                plan, sa_product, sa_coverage, "储蓄险", sa_product.get("name"))
            sa_premium = calculate_product_premium(sa_product, age, gender, sa_coverage, "10年")
            plan["products"].append({
                "type": "储蓄险",
                "product_name": sa_product["name"],
                "company": sa_product["company"],
                "coverage": sa_coverage,
                "annual_premium": sa_premium,
                "payment_term": "10年",
                "coverage_period": "至60/65周岁",
                "key_benefits": "强制储蓄，养老规划，兼具保障和收益"
            })
            plan["annual_premium"] += sa_premium

    # features 中的医疗险描述由**真实选中产品与实际保额**派生
    # ⚠️ SDI-4 整改 2026-11-10：原写死「医疗险600万保额」，
    #    保额被 max_coverage 夹到 400 万后对外仍宣称 600 万（虚报可售保额）。
    mi_entry = next((e for e in plan["products"] if e["type"] == "医疗险"), None)
    if mi_entry:
        mi_feature = (f"医疗险{mi_entry['coverage'] // 10000}万保额，"
                      f"{mi_entry['coverage_period']}"
                      f"{_medical_treatment_suffix(mi_product)}")
    else:
        mi_feature = "本方案未包含医疗险"
    plan["features"] = [
        "全方位高保额保障：寿险+重疾+医疗+意外",
        "重疾险保额高达年收入5倍",
        mi_feature,
        "定期寿险高保额，覆盖所有家庭财务责任",
        "可选储蓄险，为养老做准备",
        "年保费已按年度保费上限（min(年度预算, 年收入×20%)）校验"
    ]

    return _finalize_plan(plan, budget, annual_income, 0.20, age, gender, products,
                          removal_order=["意外险", "医疗险", "储蓄险", "重疾险", "定期寿险"])


def _finalize_plan(plan, budget, annual_income, ratio, age, gender, products,
                   removal_order=None):
    """统一收尾：执行预算硬约束 + 附加 budget_planning 块。"""
    plan.setdefault("budget_adjustments", [])
    # 移除顺序：可选险种优先，核心险种兜底（重疾险 → 定期寿险）
    _enforce_budget(plan, budget, annual_income, age=age, gender=gender,
                    product_index=_product_index(products),
                    removal_order=removal_order or ["医疗险", "意外险", "定期寿险"])
    _attach_budget_planning(plan, budget, annual_income, ratio)
    # 🆕 2026-10-30 SDI-4：出口处最终校验 —— 单一硬上限 min(年度预算, 年收入×比例)。
    # 审计要求「validate the final total before returning the plan」。
    # _enforce_budget 已保证，但这里再兜一层：任何未来改动若引入放宽乘数
    # （如历史上的 budget * 1.2），也会在这里被拦住。
    if budget and plan["annual_premium"] > budget + 0.01:
        raise AssertionError(
            f"方案年保费 {plan['annual_premium']} 超过年度保费上限 {budget}（{plan.get('plan_name')}）"
        )
    # ⚠️ R7 整改 2026-11-07：**出口兜底重算** total_coverage。
    #    以 plan["products"] 为唯一事实来源 —— 任何新增的保额调整路径
    #    （下调保额 / 移除险种 / 未来新增逻辑）若漏了增量同步，
    #    都会在这里被重算纠正，杜绝保额虚报。
    plan["total_coverage"] = sum(p.get("coverage", 0) or 0
                                 for p in plan.get("products", []))
    # ⚠️ R7 整改 2026-11-07：描述与卖点必须与**实际保留险种**一致。
    #    _enforce_budget 可能已移除险种 → 此时重写 description / features，
    #    确保被移除险种（如重疾、养老储蓄）不再出现在对外文案中。
    plan["description"] = _build_plan_description(
        plan.get("plan_name", ""), plan.get("products", []))
    if plan.get("features"):
        plan["features"] = _prune_plan_features(plan, plan["features"])
    # ⚠️ R7 整改 2026-11-07：key_benefits 中的保额表述必须与实际保额一致。
    #    _refresh_coverage_text 只在**下调保额**时被调用 → 设计期写死的
    #    「100万保额」「百万医疗」等硬编码表述可能与实际保额不符，
    #    故在出口处对每个产品统一校正（幂等）。
    for _entry in plan.get("products", []):
        _cov = _entry.get("coverage") or 0
        _entry["key_benefits"] = _normalize_coverage_claim(
            _entry.get("key_benefits"), _cov)
    # ⚠️ SDI-4 整改 2026-11-11（v2.4.2）：**features 里的保额数字也必须与最终保额一致**。
    #    官方扫描原文：
    #    「The premium plan constructs its medical coverage feature before _finalize_plan
    #     applies budget-driven coverage reductions. Finalization updates the product coverage
    #     and key_benefits but only prunes features for removed insurance types, so a retained
    #     medical product can have a lower final coverage amount while its feature still
    #     advertises the original amount.」
    #    修法：在**出口处**（预算调整已完成后）按各险种的**最终保额**重算 features 中的保额表述。
    if plan.get("features"):
        plan["features"] = _sync_features_coverage_claims(plan)
    # ⚠️ SDI-4 整改 2026-11-13（官方 2.4.3 复扫）：**「年收入 N 倍」形态的卖点
    #    同样必须随最终保额同步**。
    #    官方原文（ai-insurance-advisor 2.4.3）：
    #    「The comprehensive plan retains a five-times-income coverage claim even when
    #     actual critical-illness coverage is capped or reduced.」
    #    官方原文（insurance-advisor-china 2.4.3）：
    #    「Final coverage synchronization leaves the premium plan's income-multiple
    #     coverage claim unchanged.」
    #    根因：`_sync_features_coverage_claims()` / `_normalize_coverage_claim()`
    #    只认「数字+万」形态 → 「重疾险保额高达年收入5倍」不被校正，
    #    保额被下调/夹逼后仍宣称 5 倍（虚报保额）。
    #    修法：在**出口处**按重疾险**最终保额**重算收入倍数（幂等，
    #    正常场景不产生「5倍 → 5.0倍」的无意义 diff）。
    if plan.get("features"):
        plan["features"] = _sync_features_income_multiple_claims(plan, annual_income)
    # ⚠️ F4 整改 2026-11-09：把「可售保额上限未核实」的险种汇总为**对外披露**。
    #    必须写在**出口处**（与 total_coverage 重算同一位置），
    #    否则上限未知的保额会以一种「看起来很具体」但未经核实的形式呈现给用户。
    #    无上限未知的险种时**不新增该键**（避免给所有方案引入空字段）。
    _coverage_disclaimers = _build_coverage_disclaimers(plan)
    if _coverage_disclaimers:
        plan["coverage_disclaimers"] = _coverage_disclaimers
    else:
        plan.pop("coverage_disclaimers", None)
    return plan


def generate_all_plans(age, gender, annual_income, annual_budget, coverage_needs):
    """生成三套方案"""
    plans = {
        "基础版": design_plan("基础版", age, gender, annual_income, annual_budget, coverage_needs),
        "标准版": design_plan("标准版", age, gender, annual_income, annual_budget, coverage_needs),
        "全面版": design_plan("全面版", age, gender, annual_income, annual_budget, coverage_needs)
    }

    return plans


# 示例档案（仅在 stdin 未提供输入时作为演示数据打印，并明确标注来源）
EXAMPLE_PLAN_INPUT = {
    "age": 35,
    "gender": "男",
    "annual_income": 500000,
    "annual_budget": 500000,
    "coverage_needs": {
        "death": 2000000,
        "critical_illness": 1500000,
        "hospital": 4000000
    }
}


def _read_stdin_text():
    """读取 stdin 文本；TTY（无管道输入）返回空串。"""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return ""
        return sys.stdin.read() or ""
    except Exception:
        return ""


def main():
    raw = _read_stdin_text().strip()
    if not raw:
        # 未提供输入：明确标注示例数据，不静默把示例档案当作正式结果
        sys.stderr.write("⚠️ 未提供输入，以下为示例数据（示例档案，非真实客户数据）：\n")
        sys.stderr.write(json.dumps(EXAMPLE_PLAN_INPUT, ensure_ascii=False, indent=2) + "\n")
        params = EXAMPLE_PLAN_INPUT
    else:
        try:
            params = json.loads(raw)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            return 0
    try:
        plans = generate_all_plans(
            params.get("age", 35),
            params.get("gender", "男"),
            params.get("annual_income", 500000),
            params.get("annual_budget", 500000),
            params.get("coverage_needs", {})
        )
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 0
    print(json.dumps(plans, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
