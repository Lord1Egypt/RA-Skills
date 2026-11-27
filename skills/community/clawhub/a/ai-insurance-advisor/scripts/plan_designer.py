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
# ⚠ 官方 2026-11-18 线上复扫（2.4.17）SDI-4 remediation 原文：
#   「recognize constructions such as 「不可报销」 and post-treatment
#     negation, suppress ambiguous statements」
# → 「不可报销」「不可支付」「不可赔付」与「不予报销」同口径：**双向**绑定
#   （否定词在治疗手段**之前** / **之后**都生效 → post-treatment negation）。
# ⚠ 「报销」本身在 _AFFIRM_MARKERS 里 → 「不可报销」内的「报销」必须被
#   否定作用域吃掉（不得同时被当成肯定授权证据）——由否定词跨度天然满足。
# ⚠ 官方 SDI-4 残余 V（2026-11-24 公开复扫 · v2.4.36 · Excessive Agency · MEDIUM）
#   finding（ai · 原文）：
#     "Medical benefit generation can convert explicit noncoverage into an
#      affirmative treatment claim."
#   explanation（ai · 原文）：
#     "Medical claim authorization still relies on affirmative keywords and an
#      incomplete exclusion vocabulary: “CAR-T治疗不予给付” contains the
#      affirmative marker “给付”, but “不予给付” is not recognized by the medical
#      negation rules. With no other blocking evidence, this can become
#      “含CAR-T治疗”, reversing an explicit noncoverage statement into a
#      covered-benefit claim. …"
#   remediation（ai · 原文）：
#     "…consistently recognize nonpayment expressions such as “不予给付” in both
#      authorization and record-wide exclusion checks, ensuring words within
#      those expressions cannot authorize coverage. …"
# → 「不予给付」「不予赔付」与「不予报销」**同口径**：**双向**绑定
#   （否定跨度吃掉内部的「给付 / 赔付」→ 其不得充当肯定授权证据；
#    记录级除外证据 `_record_exclusion_keywords` 复用同一套表 → 同步收录）。
#
# ⚠ 官方 SDI-4 残余 W（2026-11-24 公开复扫 · china v2.4.37 · Excessive Agency ·
#   MEDIUM · confidence 0.99）remediation 原文：
#     「Use a shared, consistently normalized nonpayment vocabulary across
#       structured-entry validation and free-text checks, including 「不予给付」
#       and 「不予赔付」. Validate treatment entries against an explicit schema and
#       associate every payment or exclusion value with its treatment before
#       deciding coverage; contradictory or uninterpretable entries must suppress
#       affirmative claims.」
# ⚠ 官方 SDI-4 残余 Y（2026-11-24 公开复扫 · ai v2.4.41 · Excessive Agency ·
#   MEDIUM · confidence 0.99）remediation 原文：
#     「…use a shared exclusion interpretation for authorization and record-wide
#       checks, recognize expressions such as 「不予承保」 in both word orders,
#       and prevent affirmative words inside exclusion phrases from authorizing
#       coverage.」
# → **共享「不予给付」词表**（官方原文要求的 "shared … nonpayment vocabulary"）：
#   结构化校验（`_structured_text_is_negative` → `_STRUCTURED_NEGATION_TOKENS`）
#   与自由文本检查（`_NEG_MARKERS_BOTH`）**同源** —— 两者都从下面这一份
#   共享词表取「不予给付 / 不予赔付 / 不予承保」等**不予给付**表达。
#   ⇒ 残余 W：「不予给付」「不予赔付」进结构化词表 → 同条目内的
#     `payment_status="不予给付"` 与 `covered=True` **自相矛盾** → contradictory
#     → **主动压制**（不再授权、也不再让自由文本肯定证据兜底）；
#   ⇒ 残余 Y：「不予承保」进共享词表 → 医疗授权路径与记录级除外路径
#     **同口径**、**双向**词序都认，且否定短语内部的「承保」不得充当肯定授权。
# ⚠ 共享词表**只增不改**既有自由文本口径（残余 V 已验收）——「不承保」等
#   既有自由文本否定词仍留在 `_NEG_MARKERS_BOTH` 里单独维护。
#
# ══════════════════════════════════════════════════════════════════════
# ⚠ 官方 SDI-4 残余 Z / AA / AB（2026-11-25 公开复扫 · china v2.4.38 /
#   ai v2.4.42）三份 remediation 的**共同主线**（官方原文 · 逐字）：
#     「Use a shared, normalized exclusion vocabulary across mild-illness,
#       critical-illness-category, and medical coverage checks」
#     「…explicitly recognizing 「不予承保」 before and after the subject」
#     「recognize 「不含」「不包含」「不包括」 and equivalent category
#       exclusions with appropriate local scope across the entire record」
#     「…including 「不在承保范围」, and prevent words inside exclusion
#       phrases from authorizing coverage」
# → 本文件建**一份共享归一化除外词表** `_SHARED_EXCLUSION_VOCAB`（单一事实源），
#   三条路径各自从**同一份来源**取用（**同源**）：
#     ① 医疗否定路径    → `_SHARED_EXCLUSION_SCOPE`    → `_NEG_MARKERS_BOTH`
#     ② 轻症 / 主体路径 → `_SHARED_EXCLUSION_SUBJECT`  → `_CRX_EXCLUSION_MARKERS`
#     ③ 类别级重疾路径  → `_SHARED_EXCLUSION_CATEGORY` → `_CRX_CI_EXCLUSION_MARKERS`
#   三处**词序双向**（主体前 / 主体后都命中）：
#     「CAR-T治疗不在承保范围」与「不在承保范围CAR-T治疗」同样成立；
#     「轻症不予承保」与「不予承保轻症」同样成立；
#     「不含重大疾病保障」与「重大疾病保障不含」同样成立。
# ⚠ 派生只做**并集**（既有成员一律保留 · 官方「既有口径只增不改」）；
#   各路径仍保留自己的**收紧口径**（紧贴类别名词 / 填充词上限 / 其它保障对象
#   线索 / 条件性语境 …）—— 共享的是**词**，不是判定逻辑。
# ⚠ 除外短语内部的肯定词（「不在承保范围」里的「承保」）**不得**充当授权证据：
#   否定词**字符跨度**（`_negation_marker_spans`）已覆盖该短语 → `_has_affirmative`
#   的①「不落在否定词字符跨度内」判定自然把它排除（既有机制，本轮只补词表）。
#
# ── 残余 Z · 医疗除外（承保范围级）──
_SHARED_EXCLUSION_SCOPE = (
    "不在承保范围", "不属于承保范围",
)
# ── 残余 AA · 主体级除外（轻症等）──
_SHARED_EXCLUSION_SUBJECT = (
    "不予承保",
)
# ── 残余 AB · 类别级除外（含 / 包含 / 包括）──
_SHARED_EXCLUSION_CATEGORY = (
    "不含", "不包含", "不包括",
)
# 共享归一化除外词表（**单一事实源** · 三条路径由它派生）
_SHARED_EXCLUSION_VOCAB = (
    *_SHARED_EXCLUSION_SCOPE,
    *_SHARED_EXCLUSION_SUBJECT,
    *_SHARED_EXCLUSION_CATEGORY,
)
_SHARED_NONPAYMENT_NEGATIONS = (
    # ── 官方原文点名的三种「不予给付」表达（残余 W / 残余 Y）──
    "不予给付", "不予赔付", "不予承保",
    # ── 既有「不予报销 / 不予支付」口径（残余 V · 同源保留）──
    "不予报销", "不可报销", "不报销", "无法报销", "不能报销",
    "不予支付", "不可支付", "不可赔付",
)
_NEG_MARKERS_BOTH = (
    # 共享「不予给付」词表（结构化校验**同源** · 官方残余 W / Y）
    *_SHARED_NONPAYMENT_NEGATIONS,
    # 「不承保」= **承保**层面的否定（既有口径 · 残余 V 之前就有）
    "不承保",
    # ⚠ 共享归一化除外词表 · 医疗侧（官方残余 Z · 2026-11-25 公开复扫）
    #   「不在承保范围」「不属于承保范围」**双向**绑定（治疗手段在标记**前** /
    #   **后**都命中）→ 授权路径（`_medical_treatment_claims`）与记录级除外
    #   路径（`_record_exclusion_keywords`）**同口径**（同一份 `_NEG_MARKERS`）。
    #   其内部的「承保」落在否定词**字符跨度**内 → 不得充当肯定授权证据。
    *_SHARED_EXCLUSION_SCOPE,
)
_NEG_MARKERS = tuple(sorted(
    set(_NEG_MARKERS_FORWARD + _NEG_MARKERS_BACKWARD + _NEG_MARKERS_BOTH),
    key=len, reverse=True))

# ══════════════════════════════════════════════════════════════════════
# ⚠ 官方 SDI-4 残余 AC（2026-11-26 公开复扫 · china v2.4.41 · Excessive
#   Agency · MEDIUM · confidence 0.99）remediation 原文：
#     「Structured exclusion validation omits expressions recognized
#       elsewhere, including 「不在承保范围」 and 「不属于承保范围」 …
#       an entry such as {"CAR-T":{"covered":true,"payment_status":
#       "不在承保范围"}} is therefore treated as affirmative rather than
#       contradictory.」
#
# ⚠ **根因是结构性的，不是「又漏抄了两个词」**：
#   本文件历史上维护**多份互相独立**的否定/除外词表 ——
#     ① 自由文本侧：_NEG_MARKERS_FORWARD / _NEG_MARKERS_BACKWARD / _NEG_MARKERS_BOTH
#     ② 结构化侧：  _STRUCTURED_NEGATION_TOKENS
#     ③ 主体级侧：  _CRX_EXCLUSION_MARKERS
#     ④ 类别级侧：  _CRX_CI_EXCLUSION_MARKERS
#   官方每轮复扫只点出**其中一份**漏掉的短语 → 上一轮补进自由文本侧，
#   结构化侧照样漏 → 「同类问题反复出现」的**结构性根因**：
#   **词表之间没有任何一致性约束** = 结构性漂移 = 必然复发。
#
# ⚠ **一次性修法（结构性 · 终结逐条打补丁）**：
#   A. **单一事实源**：下面 `_EXCL_*` 语义族是**唯一**词表来源；
#      全部路径（自由文本 / 结构化 / 主体级 / 类别级）都从它派生
#      → 一处增词，四处同步生效。
#   B. **超集不变量**：结构化侧词表 **⊇** 自由文本侧词表
#      （守卫断言见 `scripts/test_exclusion_vocab.py`）→ 结构化侧**不可能**
#      再漏掉自由文本侧已认得的除外表达（官方本轮 finding 正是此类）。
#   C. **通用模式**（终结「下一轮换个词再来」）：语义族除逐条枚举外，另给
#      **正则模式**（如「不在/不属于 …… 范围」）→ 同族**任意**新表述无需
#      改代码即命中（自由文本侧 + 结构化侧**共用同一份模式**）。
#   D. 既有成员**一律保留**（只增不改）→ 既有口径零漂移。
# ══════════════════════════════════════════════════════════════════════

# ── 范围级补充（「不在/不属于 …… 范围」的其余表述）──
#    ⚠ 共享族 `_SHARED_EXCLUSION_SCOPE` 已定义 → 本处**不得**重复抄写
#      （重复 = 二次漂移的温床）。
_EXCL_SCOPE_EXTRA_LITERALS = (
    "不在保障范围", "不在保险范围",
    "不属于保障范围", "不属于保险范围",
    "不在责任范围", "不在赔付范围", "不在报销范围",
)
# ── 语义族 ② · 不予给付级（「不予/不可/不能 …… 给付|赔付|支付|报销」）──
#   ⚠ **直接引用**共享「不予给付」词表（残余 W 的单一事实源）——
#     不得在此**另抄一份**（那正是本轮根因：同一语义两份定义 → 必然漂移）。
_EXCL_NONPAYMENT_LITERALS = _SHARED_NONPAYMENT_NEGATIONS
# ── 类别级补充 ──
_EXCL_CATEGORY_EXTRA_LITERALS = ("不纳入", "不涵盖", "不覆盖")
# ── 主体级补充 ──
_EXCL_SUBJECT_EXTRA_LITERALS = ("不承保",)
# ── 语义族 ⑤ · 通用除外（责任免除 / 不支持 / 不赔）──
_EXCL_GENERAL_LITERALS = (
    "除外", "不支持", "不赔",
)

# ⚠ **全部语义族的并集** —— 结构化侧词表由它派生。
#   不变量：`_STRUCTURED_NEGATION_TOKENS` ⊇ `_NEG_MARKERS`（自由文本侧全部）
#   （守卫断言在 `scripts/test_exclusion_vocab.py`）。
_EXCL_ALL_LITERALS = (
    *_SHARED_EXCLUSION_VOCAB,
    *_SHARED_NONPAYMENT_NEGATIONS,
    *_EXCL_SCOPE_EXTRA_LITERALS,
    *_EXCL_CATEGORY_EXTRA_LITERALS,
    *_EXCL_SUBJECT_EXTRA_LITERALS,
    *_EXCL_GENERAL_LITERALS,
)

# ── 语义族**别名**（任务书口径 · 共享族 + 补充族的完整并集）──
#   china 库现行命名为 `*_EXTRA_LITERALS`（**补充**族），本库同时给出
#   **任务书口径**的族名（= 共享族 ∪ 补充族）→ 两侧都能按各自的名字
#   引用**同一份**词表 → **不产生第二份抄写**（抄写 = 二次漂移的温床）。
#   ⚠ 别名只改**引用**，不新增任何词 → 既有口径零漂移。
_EXCL_SCOPE_LITERALS = (
    *_SHARED_EXCLUSION_SCOPE,
    *_EXCL_SCOPE_EXTRA_LITERALS,
)
_EXCL_CATEGORY_LITERALS = (
    *_SHARED_EXCLUSION_CATEGORY,
    *_EXCL_CATEGORY_EXTRA_LITERALS,
)
_EXCL_SUBJECT_LITERALS = (
    *_SHARED_EXCLUSION_SUBJECT,
    *_EXCL_SUBJECT_EXTRA_LITERALS,
)

# ── 通用模式（**同一份** · 自由文本侧 + 结构化侧共用）──
#   逐条枚举只能覆盖「已经想到的表述」；官方复扫每轮换一个词 → 逐条打补丁
#   必然复发。模式把「同族语义」**按构式**覆盖 → 新表述无需改代码即命中。
# ⚠ 模式**不跨语义子句边界**（。；，、！？ 与空白）→ 不跨字段、不跨句子误伤。
_EXCL_PATTERNS = (
    # ① 范围级：「不在/不属于 …… 范围」（中间 ≤ 8 个非边界字符）
    r"不(?:在|属于)[^。；，、！？!?;:,\s]{0,8}范围",
    # ② 不予给付级：「不予/不可/不能/不得/无法 …… 给付|赔付|支付|报销|承保|承担」
    #    （中间 ≤ 1 个非边界字符 → 不会误伤「不能确定是否给付」这类存疑表述）
    r"(?:不(?:予|可|能|得)|无法)[^。；，、！？!?;:,\s]{0,1}(?:给付|赔付|支付|报销|承保|承担)",
    # ③ 类别级：「不 + 含|包含|包括|纳入|涵盖|覆盖」
    r"不(?:含|包含|包括|纳入|涵盖|覆盖)",
)

# ── 存疑对冲词（**不得**被当成除外）──
#   ⚠ 官方 SDI-4 残余 AC **已知坑**（任务书 §④·1）：
#     「可能无法给付，需以条款为准」这类**存疑**表述**不得**被当除外 ——
#     通用模式 ② 会命中「无法给付」→ 若照单全收 → 把「待核实」说成
#     「确定不保」（把**不确定性**说成了**确定性**）→ 与官方口径
#     「contradictory or **uninterpretable** entries must … emit an explicit
#      unverified limitation」相悖。
#   ⇒ 处置：**定长否定前瞻**（窗口 `_EXCL_HEDGE_LOOKBACK` 字符）——
#     否定表达**紧邻前置**对冲词 → 该命中判为**存疑**（ambiguous），
#     **不是** negative（官方口径：存疑一律不授权 + 产出「待核实」限制说明）。
#   ⚠ 对冲词**全部取自 `_UNCERTAINTY_MARKERS`** → 对冲 ⟹ 必然命中
#     `_structured_text_is_uncertain` → 判 **ambiguous** → **仍然压制**
#     （「存疑」与「除外」**两者都压制** → 安全方向一致）。
_EXCL_HEDGE_PREFIXES = (
    "可能", "或许", "也许", "大概", "或将", "原则上", "尚未",
)
# 定长前瞻窗口（字符）：对冲词与否定表达之间最多隔这几个字符
_EXCL_HEDGE_LOOKBACK = 6

# ⚠ 官方 SDI-4 残余 J（2026-11-18 线上复扫 · insurance-advisor-china v2.4.19
#   · MEDIUM · Excessive Agency · issueCount=1 · score=12）remediation 原文：
#     「Handle post-treatment exclusions such as 「CAR-T治疗不支持报销」 and
#       「CAR-T治疗不包含在保障范围」 by binding exclusion semantics to the
#       relevant treatment regardless of word order, while preventing
#       reimbursement words inside those exclusions from authorizing coverage.
#       Treat uncertain or conflicting interpretations as unverified and
#       suppress affirmative claims.」
#
# 根因：「不支持」「不包含」等是**纯前瞻型**否定词 —— 否定词出现在治疗手段
#      **之后**（post-treatment negation）时：
#      ① 前瞻作用域落在治疗手段**之后** → 绑不到前面的治疗手段；
#      ② 否定词跨度不含谓词 → 其后的「报销」**落在跨度之外**
#         → 通过肯定授权检查 → 产出「含CAR-T治疗」的**承保宣称**；
#      ③ 记录级除外证据复用同一套判定 → 同样漏判。
#
# 修法（两处，均在否定/除外判定层）：
#   A. **复合除外短语**：「<否定词><除外谓词>」（如「不支持报销」「不包含在保障
#      范围」）是**一个**除外短语 —— 谓词纳入否定词跨度（其内的「报销」不再
#      充当肯定授权证据）+ 该短语**双向**绑定（否定词在治疗手段之后时同样
#      绑定到相关治疗手段）；
#   B. **post-treatment 回溯绑定**：纯前瞻型否定词若**前瞻作用域内没有任何
#      治疗手段** → 其被排除对象在它**之前** → 回溯绑定到最近一次治疗手段
#      出现（真实语料存在「质子重离子不含」形态）。
#
# 除外谓词表（跟在否定词**后面**、表示「不做什么」的谓语部分）
_PREDICATE_TAILS = ("在保障范围", "在承保范围", "在保险范围",
                    "报销", "支付", "赔付", "给付", "承保")
# post-treatment 回溯绑定：否定词与被否定治疗手段之间的**连接词**长度上限
_POST_TREATMENT_MAX_GAP = 12

# 肯定/授权词（用于「明确肯定表述」判定；落在否定词内部的一律不算）
_AFFIRM_MARKERS = ("含", "包含", "涵盖", "覆盖", "可报销", "报销", "给付", "支持", "承保")

# ⚠ 官方 SDI-4 残余 K（2026-11-18 线上复扫 · insurance-advisor-china v2.4.20
#   · Excessive Agency · MEDIUM · issueCount=1 · score=12）remediation 原文：
#     「Require validated, treatment-specific affirmative coverage decisions and
#       preserve applicable conditions before emitting benefit claims. Treat questions,
#       uncertainty, conditional eligibility, pending verification, and conflicting
#       evidence as unverified, suppressing affirmative claims rather than relying on
#       keyword presence.」
# → 肯定授权**不能只看关键字在场**：疑问 / 不确定性 / 条件性 / 待核实表述
#   → 该次出现的肯定证据**不成立** → 按 unverified 压制（**不**产出无条件承保宣称）。
#
#   官方给的三个反例：
#     「CAR-T治疗是否报销待核实」（疑问 + 待核实）
#     「可能包含CAR-T治疗」（可能性）
#     「CAR-T报销以核保结果为准」（条件性）
#
# ⚠ 语料实测（2584 款 products.json）：事实源字段（key_benefits / highlights）里
#   「含治疗手段 + 不确定词」的共现为 **0 处** → 本守卫对真实数据零影响，
#   只针对扫描器的**对抗样本**生效。
_UNCERTAINTY_MARKERS = (
    # 疑问（是否 / 能否 …）
    "是否", "能否", "可否", "有无", "是不是",
    # 待核实 / 未确定
    "待核实", "待确认", "待明确", "待定", "需核实", "需确认", "尚待",
    "不确定", "未知", "存疑", "尚未",
    # 可能性（非确定表述）
    "可能", "或许", "也许", "大概", "或将", "原则上",
    # 条件性 / 视情况 / 需另行确认
    "视情况", "视实际", "视情形", "视核保", "视保险",
    "详见条款", "具体以", "另行确认", "需另行", "经确认",
)
# 「以……为准」通用形态（以核保结果为准 / 以实际理赔为准 / 以合同为准 …）
_RE_SUBJECT_TO = re.compile(r"以[^。；！？!?;:\n，,]{0,14}为准")

# ⚠ 官方 SDI-4 残余 L（2026-11-18 线上复扫 · insurance-advisor-china v2.4.21 ·
#   L1359-1376 · Excessive Agency · MEDIUM）remediation 原文：
#     「Require validated, treatment-specific coverage decisions with explicit
#       applicability conditions before generating benefit claims. Preserve those
#       conditions in the output, or suppress the claim when conditions cannot be
#       reliably interpreted; do not treat affirmative free-text keywords as sufficient
#       authorization. Add regression tests for hospital restrictions, prior
#       authorization, designated-drug lists, eligibility requirements, and conditional
#       structured entries.」
# → **适用条件 / 限制**（仅限指定医院、需转诊、预授权、目录内、符合条件 …）同样
#   不构成「无条件承保授权」：条件无法在对外文案里渲染 → 肯定授权证据**不成立**。
#
# ⚠ 语料实测（2584 款 products.json）：事实源字段里「含治疗手段 + 条件词」的共现
#   为 **0 处**（479 款含「N种重疾」的 highlights 里也为 0 处）→ 本闸对真实数据
#   零影响，只针对扫描器的**对抗样本**生效。
_CONDITION_MARKERS = (
    # 适用范围限制（仅限 / 只限 / 限于 …）
    "仅限", "仅在", "仅可", "仅能", "只限", "限于", "限指定", "限特定",
    # 医疗机构 / 医院等级限制
    "指定医院", "指定医疗", "二级以上", "三级以上", "三甲", "定点医院",
    "定点医疗", "公立医院", "医院等级",
    # 转诊 / 预授权 / 审批
    "需转诊", "预授权", "事先授权", "事前审批", "需审批", "经审批",
    # 药品目录 / 清单 / 社保范围
    "药品目录", "目录内", "目录外", "社保目录", "清单内", "指定药品",
    "限社保", "社保范围内",
    # 资格条件 / 审核
    "符合条件", "满足条件", "达到条件", "经审核", "审核通过", "须经", "需经",
)

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
    """blob 中全部否定/除外词的出现位置 → [(start, end, marker), ...]

    ⚠ 官方 SDI-4 残余 J：**复合除外短语**（否定词 + 紧邻除外谓词，如
       「不支持报销」「不包含在保障范围」）会**额外**产出一条跨度更大的复合标记 ——
       谓词被纳入否定跨度（其内的「报销」不再充当肯定授权证据），且该复合
       标记**双向**绑定（否定词在治疗手段**之后**时同样绑定到它）。
    """
    spans = []
    if not blob:
        return spans
    for m in _NEG_MARKERS:
        i = blob.find(m)
        while i != -1:
            spans.append((i, i + len(m), m))
            i = blob.find(m, i + 1)
    # ⚠ 通用模式命中（**单一事实源** · 官方残余 AC 一次性修法 C）——
    #   同族**任意**新表述（「不在保险范围」「无法给付」…）无需再改词表即命中。
    #   与结构化侧**共用同一份** `_EXCL_PATTERNS` → 两路口径永远一致。
    #   ⚠ 与既有字面词表**同口径**：已被字面词覆盖的跨度不重复登记；
    #     模式标记文本若命中既有词表 → `_marker_directions` 沿用既有方向
    #     （如「不在保障范围」仍为回溯型）；全新表述 → 双向绑定。
    if _EXCL_PATTERNS:
        _seen = {(s, e) for s, e, _m in spans}
        for _pat in _EXCL_PATTERNS:
            for _mm in re.finditer(_pat, blob):
                _s, _e = _mm.start(), _mm.end()
                if (_s, _e) in _seen:
                    continue              # 已被字面词表覆盖 → 不重复登记
                _seen.add((_s, _e))
                spans.append((_s, _e, _mm.group(0)))
    for ms, me, marker in list(spans):
        comp = _compound_exclusion_span(blob, ms, me, marker)
        if comp:
            spans.append(comp)
    spans.sort(key=lambda s: (s[0], s[1]))
    return spans


def _marker_directions(marker):
    """否定词的绑定方向 → (forward, backward)

    ⚠ 静态词表口径**不变**（_NEG_MARKERS_FORWARD / _NEG_MARKERS_BACKWARD /
       _NEG_MARKERS_BOTH）；**不在任何静态词表里**的是**动态复合除外短语**
       （如「不支持报销」「不包含在保障范围」）→ **双向**绑定
       （官方 SDI-4 残余 J：regardless of word order）。
    """
    if marker in _NEG_MARKERS_BOTH:
        return True, True
    if marker in _NEG_MARKERS_BACKWARD:
        return False, True
    if marker in _NEG_MARKERS_FORWARD:
        return True, False
    return True, True


def _predicate_tail_after(blob, pos):
    """否定词之后**紧邻**的除外谓词 → (谓词结束位置, 谓词) 或 None

    ⚠ 扫描在遇到**语义子句边界**或**另一个治疗手段出现**时停止 ——
       「不支持CAR-T治疗费用报销」这种（治疗手段在否定词**之后**）形态由
       原有的**前瞻绑定**处理，不得误判成复合短语（否则会把「报销」整个
       圈进否定跨度，破坏「治疗手段在否定词之后」的绑定口径）。
    """
    i = pos
    n = len(blob)
    while i < n:
        ch = blob[i]
        if ch in _CLAUSE_BREAKS:
            return None
        if ch in _WHITESPACE_CHARS:
            i += 1
            continue
        for kw in _TREATMENT_CLAIMS:
            if blob.startswith(kw, i):
                return None
        for pt in _PREDICATE_TAILS:
            if blob.startswith(pt, i):
                return i + len(pt), pt
        i += 1
    return None


def _compound_exclusion_span(blob, ms, me, marker):
    """否定词 + 紧邻除外谓词 → 复合除外短语 (start, end, compound_text) 或 None

    ⚠ 只对**纯前瞻型**否定词生效（_NEG_MARKERS_BOTH 里的「不可报销」等本身
       已含谓词；_NEG_MARKERS_BACKWARD 本身就是回溯型）。
    """
    if marker not in _NEG_MARKERS_FORWARD:
        return None
    hit = _predicate_tail_after(blob, me)
    if not hit:
        return None
    pe, _pt = hit
    return (ms, pe, blob[ms:pe])


def _post_treatment_bindings(blob, occurrences, spans, owner=None):
    """post-treatment negation（否定词在治疗手段**之后**）→ [(o_s, o_e, sc, ec), ...]

    官方 SDI-4 残余 J（2026-11-18 线上复扫 · v2.4.19 · MEDIUM）remediation 原文：
      「... by binding exclusion semantics to the relevant treatment regardless
        of word order ...」

    口径：
      ① 否定词的**前瞻作用域**内**没有**任何治疗手段出现
         → 该否定词的被排除对象在**它之前**；
      ② 回溯作用域（同一语义子句内 · 字段边界截断 · 上下文窗口内）里
         **最近**的一次治疗手段出现 → 即被否定的那个治疗手段；
      ③ 否定词与该次出现之间的**连接词**长度 ≤ _POST_TREATMENT_MAX_GAP
         （避免跨句跨词误绑）。

    ⚠ 复合除外短语（「不支持报销」等）本身已是**双向**标记 → 由通用回溯绑定
       处理；这里只处理**纯前瞻型**且**没有**复合短语的否定词。
    """
    out = []
    if not blob or not occurrences:
        return out
    for ms, me, marker in spans:
        forward, backward = _marker_directions(marker)
        if not forward or backward:
            continue              # 已是双向（复合短语 / BOTH 词）→ 通用回溯已覆盖
        fs, fe = _scope_bounds(blob, ms, me, True, owner)
        if any(fs <= o_s < fe for _kw, o_s, o_e in occurrences):
            continue              # ① 前瞻作用域里有治疗手段 → 被排除对象在否定词之后
        bs, be = _scope_bounds(blob, ms, me, False, owner)
        best = None
        for _kw, o_s, o_e in occurrences:
            if not (bs <= o_e <= be):
                continue
            if ms - o_e > _NEG_CONTEXT_WINDOW:
                continue
            if ms - o_e > _POST_TREATMENT_MAX_GAP:
                continue          # ③ 连接词过长 → 不绑
            if best is None or o_e > best[1]:
                best = (o_s, o_e)
        if best is not None:
            out.append((best[0], best[1], bs, be))
    return out


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
        forward, backward = _marker_directions(marker)
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
    # ⚠ post-treatment 回溯绑定（官方 SDI-4 残余 J · 2026-11-18 线上复扫）
    for o_s, o_e, _sc, _ec in _post_treatment_bindings(blob, occurrences, spans, owner):
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
        forward, backward = _marker_directions(marker)
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
    # ⚠ post-treatment 回溯绑定（官方 SDI-4 残余 J · 2026-11-18 线上复扫）
    #    —— 该次出现的除外作用域 = 回溯作用域（否定词之前的语义片段）
    for o_s, o_e, sc, ec in _post_treatment_bindings(blob, occurrences, spans, owner):
        f_m = owner[o_s] if (owner is not None and o_s < len(owner)) else -1
        out.setdefault((o_s, o_e), []).append((sc, ec, f_m))
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

# ⚠ 官方 SDI-4 残余 M（2026-11-18 线上复扫 · ai-insurance-advisor v2.4.21 ·
#   L1617-1629 · Excessive Agency · MEDIUM）remediation 原文：
#     「Require treatment-specific, validated coverage decisions that explicitly
#       resolve conflicting exclusions and include applicable conditions. Preserve those
#       conditions in generated benefit descriptions; if a conflict or condition cannot be
#       reliably interpreted and rendered, suppress the claim and report it as unverified.」
# → 结构化条目携带**适用条件** → 条件无法渲染 → **不得**无条件宣称；
# → 覆盖文本除外证据必须有**显式**的「除外已裁决」信号。
_STRUCTURED_CONDITION_KEYS = ("condition", "conditions", "eligibility",
                               "eligibility_conditions", "requirement", "requirements",
                               "condition_note", "precondition", "preconditions",
                               "notes", "note", "caveat", "caveats", "restriction",
                               "restrictions", "subject_to", "limit", "limits")
# 「除外冲突已裁决」的**显式**信号（必须是布尔 True）
_STRUCTURED_RESOLUTION_KEYS = ("exclusion_resolved", "exclusions_resolved",
                               "conflict_resolved", "conflicts_resolved",
                               "exclusion_resolution", "resolves_exclusion")
# 结构化字段值里的**否定语义**词表（已规范化：小写 + 去空白）
# ⚠️ 命中否定语义 → 该治疗手段**不得**被授权，且必须**主动压制**。
_STRUCTURED_NEGATION_TOKENS = (
    # ── 英文否定 token（既有口径 · 不变）──
    "excluded", "exclude", "exclusion", "notcovered", "notcover", "notinclude",
    "noteligible", "notpayable", "notreimbursed", "nocoverage", "uncovered",
    "false",
    # ── 中文否定词：**全部语义族**（**单一事实源**派生 · 官方残余 AC）──
    #   官方残余 AC（2026-11-26 公开复扫）finding 原文：
    #     「Structured exclusion validation omits expressions recognized
    #       elsewhere, including 「不在承保范围」 and 「不属于承保范围」 …
    #       an entry such as {"CAR-T":{"covered":true,"payment_status":
    #       "不在承保范围"}} is therefore treated as affirmative rather than
    #       contradictory.」
    #   → 结构化侧词表 **⊇ 自由文本侧词表**（`_NEG_MARKERS`）：
    #     本轮把「不在承保范围」「不属于承保范围」等**全部**范围级表达并入
    #     → 结构化条目 `{"covered": True, "payment_status": "不在承保范围"}`
    #       同条目既有肯定决定又有除外证据 → **contradictory** → **主动压制**
    #       （不再授权 CAR-T 治疗）。
    #   ⚠ **超集不变量**由 `scripts/test_exclusion_vocab.py` 守卫断言
    #     （`_STRUCTURED_NEGATION_TOKENS` ⊇ `_NEG_MARKERS`）
    #     → 「结构化侧漏掉自由文本侧已认得的除外表达」这一类**不可能**再复发。
    # ⚠ 各语义族**直接引用**（不在此处另抄一份 → 杜绝词表二次漂移）：
    *_SHARED_EXCLUSION_VOCAB,
    *_SHARED_NONPAYMENT_NEGATIONS,
    *_EXCL_SCOPE_EXTRA_LITERALS,
    *_EXCL_CATEGORY_EXTRA_LITERALS,
    *_EXCL_SUBJECT_EXTRA_LITERALS,
    *_EXCL_GENERAL_LITERALS,
    # ── 中文否定词：结构化侧既有额外口径（**保持不变**）──
    "不保", "未覆盖", "拒绝承保", "非承保",
)

# ⚠⚠ **超集不变量**（模块级自检 · 官方残余 AC 一次性修法 B）——
#   结构化侧词表必须 **⊇** 自由文本侧词表。
#
#   为什么必须在**发布产物内部**自检，而不是只靠本地测试：
#     官方每轮复扫点出的都是「这一侧漏了那一侧已认得的表达」。
#     若只在本地测试里断言，某次改动可能绕过测试直接把漂移**发出去**；
#     放在模块级 → 漂移**根本无法上线**（导入即失败），而不是等下一轮
#     官方复扫再暴露一次。
#
#   ⚠ 这条不变量正是本轮官方 finding 的**反面**：
#     官方 finding = 结构化侧 ⊉ 自由文本侧（「不在承保范围」被自由文本侧
#     认得、结构化侧不认）→ 本断言**从结构上封死**该方向。
assert set(_NEG_MARKERS) <= set(_STRUCTURED_NEGATION_TOKENS), (
    "除外词表漂移：结构化侧词表必须 ⊇ 自由文本侧词表（官方残余 AC 一次性修法 B）"
)
assert set(_NEG_MARKERS) <= set(_EXCL_ALL_LITERALS), (
    "除外词表漂移：单一事实源必须 ⊇ 自由文本侧词表"
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


def _excl_hit_is_hedged(s, start):
    """该否定命中是否被**对冲词**前置（→ 存疑，**不得**判为除外）。

    ⚠ 官方 SDI-4 残余 AC **已知坑**（任务书 §④·1）：通用模式 ② 会命中
      「可能无法给付，需以条款为准」里的「无法给付」→ 若照单全收 →
      存疑表述被当成**确定性的除外** → 与官方口径
      「contradictory or **uninterpretable** entries must … emit an explicit
       unverified limitation」相悖。
    ⇒ **定长否定前瞻**（窗口 `_EXCL_HEDGE_LOOKBACK` 字符）：否定表达**紧邻
      前置**的对冲词 → 该命中判为**存疑**（ambiguous），**不是** negative。

    ⚠ 窗口内若出现**语义子句边界** → **不**判为存疑
      （保守方向：仍按除外压制 —— 存疑只影响**状态标签**，不影响**压制**）。
    ⚠ 对冲词全部取自 `_UNCERTAINTY_MARKERS` → 对冲 ⟹ 必然命中
      `_structured_text_is_uncertain` → 判 **ambiguous** → **仍然压制**
      （官方口径：存疑一律不授权 + 产出「待核实」限制说明）。
    """
    if start <= 0:
        return False
    lo = max(0, start - _EXCL_HEDGE_LOOKBACK)
    prefix = s[lo:start]
    if not prefix:
        return False
    for _b in _CLAUSE_BREAKS:
        if _b in prefix:
            return False              # 跨子句 → 不算存疑（保守：仍按除外）
    return any(prefix.endswith(_h) for _h in _EXCL_HEDGE_PREFIXES)


def _structured_text_is_negative(text):
    """结构化字段的**字符串值**是否带否定语义（excluded / 除外 / 不承保 …）。

    ⚠ 命中**字面词表**或**通用模式**即判否定；**存疑对冲**的命中
      （`_excl_hit_is_hedged`）**不算**否定 → 由 `_structured_contains_uncertainty`
      判 **ambiguous** → **仍然压制**（官方残余 AC 已知坑 · 任务书 §④·1）。
    """
    if not isinstance(text, str):
        return False
    s = unicodedata.normalize("NFKC", text).casefold()
    s = "".join(ch for ch in s if not ch.isspace())
    if not s:
        return False
    # ① 字面词表（**单一事实源**派生）—— 逐处命中判定（存疑对冲除外）
    for _tok in _STRUCTURED_NEGATION_TOKENS:
        _start = s.find(_tok)
        while _start != -1:
            if not _excl_hit_is_hedged(s, _start):
                return True
            _start = s.find(_tok, _start + 1)
    # ② 通用模式（**与自由文本侧同一份** `_EXCL_PATTERNS` · 官方残余 AC
    #   一次性修法 C）→ 结构化侧与自由文本侧**永远**同口径：
    #   同族任意新表述（「不在保险范围」「无法给付」…）无需再改词表即命中。
    for _pat in _EXCL_PATTERNS:
        for _mm in re.finditer(_pat, s):
            if not _excl_hit_is_hedged(s, _mm.start()):
                return True
    return False


def _structured_subtree_has_text(value, predicate):
    """结构化子树里是否存在满足 predicate 的**字符串叶子**（**递归**下钻）

    ⚠ 官方 SDI-4 残余 AE-1（2026-11-27 公开复扫 · ai v2.4.48 / china v2.4.45 ·
      Excessive Agency · MEDIUM · confidence 0.99）finding 原文：
        「Structured validation checks immediate string values and string elements of
          lists, but does not recursively inspect nested dictionaries.」
      explanation 原文：
        「… A CAR-T entry containing covered=true and payment={"status":"不予给付"},
          alongside affirmative benefit text, can therefore authorize a treatment
          claim; the record-wide text scan also loses the association between the
          nested exclusion and its treatment identifier.」
      remediation 原文：
        「… recursively evaluate their evidence while retaining the parent treatment
          identifier, and use the same resulting state for authorization, suppression,
          and limitations.」

    ⇒ 结构化条目里的除外 / 存疑证据**必须递归**下钻 dict / list / tuple
      （任意深度）→ 嵌套里的「不予给付」「不在承保范围」同样**可见**。
    ⇒ **只对字符串叶子**做语义判定 → 非字符串（bool / int / None）**不得**当否定
      （`covered=True` 是**肯定**授权证据，绝不可被当成否定）。
    """
    if isinstance(value, str):
        return bool(predicate(value))
    if isinstance(value, dict):
        for val in value.values():
            if _structured_subtree_has_text(val, predicate):
                return True
        return False
    if isinstance(value, (list, tuple)):
        for item in value:
            if _structured_subtree_has_text(item, predicate):
                return True
        return False
    return False


def _structured_contains_negation(mapping):
    """结构化条目（dict）里是否**另有**否定语义（自相矛盾 → 不得授权）。

    ⚠ 官方 SDI-4 残余 AE-1：**递归**下钻嵌套结构（`_structured_subtree_has_text`）
      → 嵌套 dict 里的除外证据（`payment={"status":"不予给付"}`）不再被漏检
      → 该条目判 **contradictory** → 授权 / 压制 / 限制**同一状态**。
    ⚠ **既有扁平口径零漂移**：顶层字符串 / 顶层 list 的字符串元素判定**完全不变**。
    """
    if not isinstance(mapping, dict):
        return False
    return _structured_subtree_has_text(mapping, _structured_text_is_negative)


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


def _structured_text_is_uncertain(text):
    """结构化字段的**字符串值**是否带**疑问 / 不确定 / 待核实**语义。

    ⚠ 官方 SDI-4 残余 W（2026-11-24 公开复扫）remediation 原文：
      「…contradictory or **uninterpretable** entries must suppress affirmative
        claims.」
      「Treat questions, uncertainty, conditional eligibility, pending
        verification, and conflicting evidence as unverified, suppressing
        affirmative claims rather than relying on keyword presence.」

    ⚠ 本函数与自由文本侧**共用同一份** `_UNCERTAINTY_MARKERS` / `_RE_SUBJECT_TO`
       → 两路口径一致。
    """
    if not isinstance(text, str):
        return False
    s = unicodedata.normalize("NFKC", text).casefold()
    s = "".join(ch for ch in s if not ch.isspace())
    if not s:
        return False
    if any(m in s for m in _UNCERTAINTY_MARKERS):
        return True
    return bool(_RE_SUBJECT_TO.search(s))


def _structured_contains_uncertainty(mapping):
    """结构化条目（dict）里是否**另有**不可解释 / 待核实语义。

    ⚠ 为什么必须有这一闸（与 `_structured_contains_negation` 对称）：
       `payment_status` **不是**承保决定键（`_STRUCTURED_DECISION_KEYS` 只有
       `covered` / `is_covered`）→ 条目的决定状态只看 `covered=True`
       → 若 `payment_status` 写的是**不可解释**的值
       （「不能确定是否给付」「待核实」「以核保结果为准」…），
       该条目会被当成**干净肯定授权** → 产出**不实承保宣称**。
       → 不可解释 → 判 **ambiguous**（压制，且**不可**被裁决信号翻案）。
    """
    if not isinstance(mapping, dict):
        return False
    # ⚠ 官方 SDI-4 残余 AE-1：**递归**下钻嵌套结构 → 嵌套 dict / list 里的
    #   「待核实」「以核保结果为准」同样**可见**（不可解释 → 压制）。
    return _structured_subtree_has_text(mapping, _structured_text_is_uncertain)


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
      · dict 且 affirmative 决定 + 同条目另有否定语义 → **contradictory**
        （官方 2.4.17 复扫原文「treat affirmative decisions accompanied by
          exclusion evidence as contradictory or negative」→ 必须**压制**，
          不得是 ambiguous：ambiguous 既不授权**也不**压制 → 自由文本肯定
          证据照样产出无条件承保宣称）
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
                # 官方 2026-11-18 线上复扫（2.4.17）SDI-4 remediation 原文：
                #   「treat affirmative decisions accompanied by exclusion
                #     evidence as contradictory or negative」
                # → affirmative 决定 + 同条目排除证据 → **contradictory**
                #   （**压制**，不得只是「不授权」）
                return "contradictory"
            # ⚠ 不可解释 / 待核实（官方残余 W「uninterpretable entries must
            #   suppress affirmative claims」）→ **ambiguous**（压制）。
            #   ⚠ 用 ambiguous 而非 contradictory：ambiguous **不可**被
            #     「显式声明已裁决」信号翻案 → 保守方向。
            if _structured_contains_uncertainty(value):
                return "ambiguous"
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


# ---------------------------------------------------------------------------
# 裸字符串（bare string）治疗条目 —— **授权与压制共用的唯一 schema**
#
# 官方 2026-11-18 线上复扫（2.4.18）SDI-4 finding 原文：
#   「Ambiguous bare-string treatment entries bypass the documented
#     claim-suppression gate.」
# 官方 remediation 原文：
#   「Validate treatment entries against a single explicit schema shared by
#     authorization and suppression checks. Classify a matching bare-string
#     treatment identifier as ambiguous and suppress its claim rather than
#     falling back to affirmative free text; retain suppression for explicit
#     exclusions. Add regression tests for bare-string identifiers, ambiguous
#     entries alongside affirmative text, and conflict…」
#
# ⚠️ 根因（此前「三不管」状态）：
#   ① `_structured_authority_states()` 遇到裸字符串**直接 continue** → 不产生
#      任何状态 → states 为空 → 不授权（✅ 但状态缺失 → 与「无条目」混淆）；
#   ② `_structured_authority_denies()` 裸字符串**只在自带否定语义时**才压制
#      → 裸标识符（"CAR-T"）**不压制**；
#   → 裸标识符既不授权、也不压制 → 自由文本的肯定证据照样产出**无条件承保
#      宣称**（官方口径：应判 **ambiguous** 并压制，**不得** fallback 到肯定
#      自由文本）。
#
# 修法（两库同口径）：
#   ① 裸字符串与 dict 条目走**同一套显式 schema**（`_structured_bare_string_state`）
#      → 授权判定（`_structured_authority_states`）与压制判定
#        （`_structured_authority_denies`）**共用同一个状态函数**；
#   ② **匹配**该治疗手段的裸标识符 → 判 **ambiguous** → **必须压制**
#      （官方：suppress its claim，**不得** fallback 到肯定自由文本）；
#   ③ 裸字符串**自带否定语义** → 判 negative（保留显式除外的压制）；
#   ④ 标识匹配一律走**规范化标识**（`_normalize_treatment_identifier`）
#      + **标识边界**判定 → **不得**用裸子串判定。
# ---------------------------------------------------------------------------

# 标识的**延续字符**：紧跟在标识之后 → 说明那是**另一个更长的**标识
# （"CAR-TX" ≠ "CAR-T"；CJK 字符不算延续字符 → "CAR-T治疗" 仍是 CAR-T）。
_STRUCTURED_IDENTIFIER_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789-_"
)


def _structured_is_identifier_char(ch):
    """该字符是否为**标识延续字符**（ASCII 字母 / 数字 / 连字符 / 下划线）。"""
    return bool(ch) and ch in _STRUCTURED_IDENTIFIER_CHARS


def _structured_bare_string_matches(ident, norm_kw):
    """规范化后的裸字符串是否**匹配**该治疗手段的规范化标识。

    判定口径（**规范化标识**匹配 —— 不是裸子串匹配）：
      ① **逐字相等** → 匹配（典型裸标识符："CAR-T" / "car-t" / "CAR_T" /
         "ＣＡＲ－Ｔ" —— 全部由 `_normalize_treatment_identifier` 归一）；
      ② 标识**出现在字符串中**且两侧**都不是标识延续字符** → 匹配
         （标识 + 措辞："CAR-T治疗费用" / "CAR-T 除外"）。
    ⚠️ **不得**用无边界子串判定 → "CAR-TX" 不得匹配 "CAR-T"；
       "质子重离子" 不得匹配 "CAR-T"。
    """
    if not ident or not norm_kw:
        return False
    if ident == norm_kw:
        return True
    start = 0
    while True:
        idx = ident.find(norm_kw, start)
        if idx == -1:
            return False
        end = idx + len(norm_kw)
        before = ident[idx - 1] if idx > 0 else ""
        after = ident[end] if end < len(ident) else ""
        if not _structured_is_identifier_char(before) and \
                not _structured_is_identifier_char(after):
            return True
        start = idx + 1


def _structured_bare_string_state(item, norm_kw):
    """**裸字符串**治疗条目的承保决定状态（授权与压制**共用**的唯一 schema）。

    返回：
      "negative"  → 显式除外（自带否定语义）→ **压制**
      "ambiguous" → **匹配**该治疗手段的裸标识符（无显式承保决定）→ **压制**
      None        → 不匹配（与本治疗手段无关）→ **不得**误压制
    """
    if not isinstance(item, str) or not norm_kw:
        return None
    ident = _normalize_treatment_identifier(item)
    if not ident:
        return None
    if not _structured_bare_string_matches(ident, norm_kw):
        # 显式除外（自带否定语义且提及该治疗手段）→ negative
        # （官方 2026-11-18 线上复扫 2.4.18 SDI-4 remediation 原文：
        #   「retain suppression for explicit exclusions」→ 保留既有压制口径）
        if _structured_text_is_negative(item) and norm_kw in ident:
            return "negative"
        return None
    # 匹配的裸条目：自带否定语义 → 显式除外（negative，保留既有压制）；
    # 否则 → **ambiguous**（官方口径：压制其宣称，**不得** fallback 到
    # 肯定自由文本）。
    if _structured_text_is_negative(item):
        return "negative"
    return "ambiguous"


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
                if isinstance(item, str):
                    # 裸字符串 → **共享 schema**（与压制判定同一个函数）：
                    #   匹配该治疗手段的裸标识符 → 产生 **ambiguous** 状态
                    #   （官方 2026-11-18 线上复扫 2.4.18 SDI-4：
                    #     裸字符串不得绕过压制闸 → **不得**直接 continue 掉）
                    state = _structured_bare_string_state(item, norm_kw)
                    if state is not None:
                        states.append(state)
                    continue
                if not isinstance(item, dict):
                    continue                # 非字符串 / 非 dict → 畸形 → 不授权
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if _normalize_treatment_identifier(ident) != norm_kw:
                    continue
                states.append(_structured_value_state(item))
    return states


def _structured_matching_entries(product, keyword):
    """该治疗手段在**全部**结构化权威字段里的**匹配条目**（dict 形态）→ [entry, ...]

    ⚠ 只收 dict 形态条目（承载条件 / 裁决信号的字段只可能出现在 dict 里）。
    """
    out = []
    if not product:
        return out
    norm_kw = _normalize_treatment_identifier(keyword)
    if not norm_kw:
        return out
    for field in _STRUCTURED_AUTHORITY_FIELDS:
        value = product.get(field)
        if isinstance(value, dict):
            for key, val in value.items():
                if not isinstance(key, str):
                    continue
                if _normalize_treatment_identifier(key) != norm_kw:
                    continue
                if isinstance(val, dict):
                    out.append(val)
        elif isinstance(value, (list, tuple)):
            for item in value:
                if not isinstance(item, dict):
                    continue
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if _normalize_treatment_identifier(ident) != norm_kw:
                    continue
                out.append(item)
    return out


def _structured_entry_has_condition(entry):
    """该结构化条目是否携带**适用条件**（条件无法渲染 → 不得无条件宣称）"""
    if not isinstance(entry, dict):
        return False
    for key, val in entry.items():
        if not isinstance(key, str):
            continue
        if key.strip().lower() not in _STRUCTURED_CONDITION_KEYS:
            continue
        if val is None or val is False:
            continue
        if isinstance(val, str) and not val.strip():
            continue
        if isinstance(val, (list, tuple, dict, set)) and not val:
            continue
        return True
    return False


def _treatment_keywords_for_identifier(identifier):
    """结构化条目的**治疗手段标识** → 它命中的对外宣称关键词集合

    口径：与文本侧**同一套**规范化标识 + 标识边界判定
         （`_normalize_treatment_identifier` + `_structured_bare_string_matches`）
         → 「CAR-T」「CAR-T治疗」「car-t」都命中关键词「CAR-T」；
           「CAR-TX」**不**命中（「X」是标识延续字符 → 不得越界授权）。
    """
    out = set()
    if not isinstance(identifier, str) or not identifier.strip():
        return out
    norm = _normalize_treatment_identifier(identifier)
    if not norm:
        return out
    for kw in _TREATMENT_CLAIMS:
        if _structured_bare_string_matches(
                norm, _normalize_treatment_identifier(kw)):
            out.add(kw)
    return out


def _structured_condition_keywords(product):
    """结构化权威字段里**携带适用条件**的治疗手段集合（官方 SDI-4 残余 L/M）

    ⚠ 官方 2026-11-18 线上复扫（v2.4.21）SDI-4 remediation 原文：
      「if a conflict or condition cannot be reliably interpreted and rendered,
        suppress the claim and report it as unverified.」
      → 「适用条件」通道**不得**只扫自由文本叶子 —— 结构化条目里的条件字段
        （condition / eligibility / requirement / restrictions …）此前**漏扫**
        → 条件无法渲染却照样产出无条件宣称（**S3 泄漏**）。

    口径：结构化权威字段里的条目（dict 形态 / list 形态）若携带
         `_STRUCTURED_CONDITION_KEYS` 里的条件字段 → 该条目对应的治疗手段
         属「带条件」→ 条件无法在对外文案里渲染 → **不得无条件宣称**。
         与自由文本叶子的条件通道**同一口径**（合并进 `record_condition`）。
    """
    out = set()
    if not product:
        return out
    for field in _STRUCTURED_AUTHORITY_FIELDS:
        value = product.get(field)
        if isinstance(value, dict):
            for key, val in value.items():
                if not isinstance(key, str):
                    continue
                # ⚠ 值不是 dict / 值里没有条件字段 → 该条目**不带**条件
                if not _structured_entry_has_condition(val):
                    continue
                out |= _treatment_keywords_for_identifier(key)
        elif isinstance(value, (list, tuple)):
            for item in value:
                if not isinstance(item, dict):
                    continue
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if not _structured_entry_has_condition(item):
                    continue
                out |= _treatment_keywords_for_identifier(ident)
    return out


def _structured_entry_resolves_exclusion(entry):
    """该结构化条目是否**显式**声明「除外冲突已裁决」（布尔 True）。

    ⚠ 该信号是**加强**信号（结构化条目显式确认冲突已解决），
       **不是**结构化肯定授权的**普遍前置条件** —— 结构化 `covered=True`
       本身就是权威裁决（详见 `_structured_entry_declares_unresolved`）。
    """
    if not isinstance(entry, dict):
        return False
    for key, val in entry.items():
        if not isinstance(key, str):
            continue
        if key.strip().lower() in _STRUCTURED_RESOLUTION_KEYS and val is True:
            return True
    return False


def _structured_entry_declares_unresolved(entry):
    """该结构化条目是否**显式声明**「除外冲突**未**裁决」→ 不得给出肯定裁决

    ⚠ 官方 2.4.15 复扫 SDI-4 #1 remediation 原文：
      「Require an affirmative coverage decision plus applicable conditions and
        explicit resolution of conflicting exclusions」
      → 「显式声明**已**裁决」（布尔 True）是**加强**信号；
        「显式声明**未**裁决」（False / 其它非 True 值）→ 冲突**未**解决
        → **不得**授权。

    ⚠ 「显式声明已裁决」**不是**结构化肯定授权的**普遍前置条件** ——
       结构化 `covered=True` 本身就是**权威裁决**（官方口径：记录级冲突由
       结构化字段逐项裁决）。把「显式声明已裁决」当成普遍前置条件会让
       「结构化 covered=True 解决记录级冲突」的正例**永远无法授权**
       → **过度收紧**（把实际可保的 CAR-T 说成不可保）。
    """
    if not isinstance(entry, dict):
        return False
    if _structured_entry_resolves_exclusion(entry):
        return False                   # 显式声明**已**裁决 → 不阻断
    for key, val in entry.items():
        if not isinstance(key, str):
            continue
        if key.strip().lower() not in _STRUCTURED_RESOLUTION_KEYS:
            continue
        # 声明了裁决信号但值**不是**布尔 True → 未裁决 / 畸形 → 阻断
        return True
    return False


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
    if not all(state == "affirmative" for state in states):
        return False
    # ⚠ 官方 SDI-4 残余 M（2026-11-18 线上复扫 · ai v2.4.21 · L1617-1629）：
    #   「Structured affirmative flags can override exclusions without preserving coverage
    #     conditions.」
    entries = _structured_matching_entries(product, keyword)
    # ① 条目携带**适用条件** → 条件无法在对外文案里渲染 → 不得无条件宣称
    #    （条件通道与记录级条件集合 **同一口径**：`_record_condition_keywords`
    #      已把结构化条目的条件字段纳入 `record_condition` → 非否定分支 /
    #      mixed-negation 分支两个产出分支行为一致）
    if any(_structured_entry_has_condition(e) for e in entries):
        return False
    # ② 「除外冲突已裁决」：**显式声明未裁决** → 冲突未解决 → 不得授权。
    #    ⚠ 「显式声明已裁决」**不是**普遍前置条件 —— 结构化 `covered=True`
    #      本身就是权威裁决（官方口径：记录级冲突由结构化字段逐项裁决）。
    #      若把它当成普遍前置条件：布尔形态 `{"CAR-T": True}` 取不到 dict 条目
    #      （entries 为空 → any([]) 恒假）、list dict 形态条目也没有裁决信号
    #      → 结构化 covered=True **永远**无法解决记录级冲突 → 过度收紧
    #      （把实际可保的 CAR-T 说成不可保）。
    if any(_structured_entry_declares_unresolved(e) for e in entries):
        return False
    return True


def _structured_authority_denies(product, keyword):
    """结构化、权威的产品字段是否**显式否定**该治疗手段 → 主动压制（不得宣称）。

    官方 2.4.15 复扫 SDI-4 #1 remediation（原文）：
      「false, excluded, unknown, malformed, or ambiguous values must not
        authorize a claim.」

    ⚠️ 「不授权」只说明**不能用来授权**；「否定」更进一步 —— 该治疗手段在
       本产品上**一律不得**被宣称（无论条款正文怎么写）。
       否定形态：布尔 False / None / 数值 0 / 带否定语义的字符串
       （"excluded" / "not covered" / "除外" / "不承保" …）。

    官方 2026-11-18 线上复扫（2.4.17）SDI-4 remediation 原文：
      「suppress the claim if any entry is negative, contradictory,
        ambiguous, or malformed; free text must not override these states.」
    → 压制集合 = negative / contradictory / **ambiguous**（含未知 / 畸形）。
      · negative     → 显式否定
      · contradictory → 自相矛盾（含 affirmative + 同条目排除证据）
      · ambiguous    → 未知 / 畸形（无决定键、未知值、裸字符串 …）
    ⚠️ affirmative **不在**压制集合里 → 一致 affirmative 仍可授权。
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
                # 官方 2026-11-18 线上复扫（2.4.17）SDI-4 remediation 原文：
                #   「suppress the claim if any entry is negative,
                #     contradictory, ambiguous, or malformed」
                # → 压制集合必须覆盖 negative / contradictory / ambiguous
                #   （ambiguous 同时覆盖「未知」与「畸形」两类）。
                # ⚠ 不得因此误伤「一致 affirmative」——affirmative 不在集合里。
                if _structured_value_state(val) in ("negative", "contradictory",
                                                  "ambiguous"):
                    return True
        elif isinstance(value, (list, tuple)):
            for item in value:
                if isinstance(item, str):
                    # 裸字符串 → **共享 schema**（与授权判定同一个函数）：
                    #   匹配该治疗手段的裸标识符 → ambiguous（无显式决定）
                    #   或 negative（自带否定语义 = 显式除外）→ **一律压制**
                    #   （官方 2026-11-18 线上复扫 2.4.18 SDI-4：
                    #     suppress its claim rather than falling back to
                    #     affirmative free text；retain suppression for
                    #     explicit exclusions）
                    state = _structured_bare_string_state(item, norm_kw)
                    if state in ("negative", "ambiguous"):
                        return True
                    continue
                if not isinstance(item, dict):
                    continue
                ident = _structured_item_identifier(item)
                if not ident:
                    continue
                if _normalize_treatment_identifier(ident) != norm_kw:
                    continue
                # 同上：list 形态的匹配条目同样覆盖 ambiguous（畸形）。
                if _structured_value_state(item) in ("negative", "contradictory",
                                                   "ambiguous"):
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


def _structured_entry_has_exclusion(value):
    """结构化条目是否**携带除外证据**（显式否定 / 自相矛盾 / 裸否定串）。

    ⚠ 与授权判定**共用同一份 schema**（`_structured_text_is_negative` /
      `_STRUCTURED_DECISION_KEYS`）→ 授权与记录级视图**永远**同口径。
    """
    if isinstance(value, dict):
        if _structured_contains_negation(value):
            return True
        # 显式否定决定（covered=False / is_covered=False）→ 除外证据
        for key in _STRUCTURED_DECISION_KEYS:
            if key in value and value[key] is False:
                return True
        return False
    if isinstance(value, str):
        return _structured_text_is_negative(value)
    return False


def _structured_excluded_identifiers(product):
    """产品记录里**结构化**除外证据所指向的治疗手段集合。

    ⚠ 官方 SDI-4 残余 AC（2026-11-26 公开复扫）finding 原文：
      「…the separate payment-status text contains no treatment identifier,
        so record-wide checks do not associate its exclusion with CAR-T…」

    根因：结构化条目的**键**（或 list 元素的标识字段）**就是**治疗手段标识，
    而除外证据写在**条目的其它字段**里（如 `payment_status`）→ 该文本叶子
    本身**不含**治疗手段标识 → 纯文本口径的记录级除外集合**看不到**它。

    → 本函数按**标识**关联：键 / 标识字段匹配某个治疗手段关键词，且该条目
      携带除外证据 → 该治疗手段在**记录级**视图中同样属「存在除外证据」。
      （结构化路径本身已能压制 → 本函数是**同一事实**在记录级视图里的
      补齐，属纵深防御：任一路径失效，另一条仍能拦住。）
    """
    out = set()
    if not isinstance(product, dict):
        return out

    def _match(identifier):
        if not isinstance(identifier, str):
            return None
        norm = _normalize_treatment_identifier(identifier)
        if not norm:
            return None
        for kw in _TREATMENT_CLAIMS:
            if _normalize_treatment_identifier(kw) == norm:
                return kw
        return None

    for _value in product.values():
        if isinstance(_value, dict):
            for _key, _val in _value.items():
                _kw = _match(_key)
                if _kw and _structured_entry_has_exclusion(_val):
                    out.add(_kw)
        elif isinstance(_value, (list, tuple)):
            for _item in _value:
                if not isinstance(_item, dict):
                    continue
                _kw = _match(_structured_item_identifier(_item))
                if _kw and _structured_entry_has_exclusion(_item):
                    out.add(_kw)
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

    ⚠ 官方残余 AC：结构化条目的除外证据（`payment_status="不在承保范围"`）
      所在文本叶子**不含**治疗手段标识 → 纯文本口径看不到它
      → 由 `_structured_excluded_identifiers` 按**标识**补齐
      （两路合并 → 记录级视图**完整**）。
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
    out |= _structured_excluded_identifiers(product)
    return out


def _split_clauses(text):
    """按**语义子句边界**切分文本 → [clause, ...]

    ⚠ 子句边界口径与 `_CLAUSE_BREAKS` 一致（普通空白**不是**边界）。
       官方 SDI-4 残余 K：不确定表述必须与**相关治疗手段同子句**才算数 ——
       否则「产品名含治疗手段 + 其它段落含可能」这类偶然共现会造成误压制。
    """
    if not text:
        return []
    out = []
    buf = []
    for ch in text:
        buf.append(ch)
        if ch in _CLAUSE_BREAKS:
            out.append("".join(buf))
            buf = []
    if buf:
        out.append("".join(buf))
    return out


def _record_uncertain_keywords(product):
    """**整条产品记录**内存在**不确定表述**的治疗手段集合（官方 SDI-4 残余 K）

    口径：逐个**文本叶子**独立判定 —— 某个治疗手段出现所在的**子句**里带
          疑问 / 不确定性 / 条件性 / 待核实表述 → 该治疗手段在本产品记录内
          属「未经确认」→ 不得对外宣称（**跨字段 / 跨元素同样成立**，
          与官方 2.4.15 的记录级冲突口径一致）。

    ⚠ 官方 remediation 原文：
      「Treat questions, uncertainty, conditional eligibility, pending verification,
        and conflicting evidence as unverified, suppressing affirmative claims rather
        than relying on keyword presence.」
    """
    return _record_flagged_keywords(product, _has_uncertainty)


def _record_flagged_keywords(product, checker):
    """**整条产品记录**内被 checker 判为「未经确认」的治疗手段集合

    checker(文本, lo, hi) → bool（片段是否命中某类表述：不确定 / 适用条件 …）

    口径：逐个**文本叶子**独立判定 —— 某个治疗手段出现所在的**子句**里命中 checker
          → 该治疗手段在本产品记录内属「未经确认」→ 不得对外宣称
          （**跨字段 / 跨元素同样成立**，与官方 2.4.15 的记录级冲突口径一致）。
    """
    out = set()
    if not product:
        return out
    for text in _product_text_leaves(product):
        if not text or not text.strip():
            continue
        if not any(kw in text for kw in _TREATMENT_CLAIMS):
            continue                      # 不含任何治疗手段 → 跳过（性能）
        for clause in _split_clauses(text):
            if not any(kw in clause for kw in _TREATMENT_CLAIMS):
                continue
            if not checker(clause, 0, len(clause)):
                continue
            for kw, _s, _e in _treatment_occurrences(clause):
                out.add(kw)
    return out


# ⚠ 官方 SDI-4 残余 L · F23.1 **跨字段条件泄漏**（2026-11-22 复扫复现）：
#   条件出现在**别的叶子**（key_benefits 的另一个元素 / highlights）时，
#   该条件**无法可靠归属**到具体治疗手段 → 条件无法在对外文案里渲染 →
#   不得无条件宣称（官方 remediation 原文：
#     「suppress the claim when conditions cannot be reliably interpreted」）。
#   ⚠「突破 / 不限 …」类**肯定表述**（如「突破社保目录限制」）**不是**限制
#   → 不算条件（否则会把「突破目录限制」误当限制 → 过度收紧）。
_MEDICAL_CONDITION_OVERRIDE_CUES = (
    "突破", "打破", "不限", "无需", "免于", "不受限", "跨过",
)


def _medical_cross_leaf_condition_keywords(product):
    """记录内**跨叶子**的适用条件 → 治疗手段集合（该记录内的宣称一律压制）

    口径：
      · 条件子句所在叶子**不含**该治疗手段（≠ 同叶子）→ 条件**跨字段 / 跨元素**
        → 无法可靠归属 → 该治疗手段在本产品记录内属「带条件」；
      · 「突破 / 不限 …」类肯定表述不算条件。
    """
    out = set()
    if not product:
        return out
    cond_leaves = []
    for text in _product_text_leaves(product):
        if not isinstance(text, str) or not text.strip():
            continue
        for clause in _split_clauses(text):
            if not _has_condition(clause, 0, len(clause)):
                continue
            if any(cue in clause for cue in _MEDICAL_CONDITION_OVERRIDE_CUES):
                continue
            cond_leaves.append((text, clause))
    if not cond_leaves:
        return out
    for kw in _TREATMENT_CLAIMS:
        for (text, _clause) in cond_leaves:
            if kw in text:
                continue          # 同叶子 → 既有子句级判定负责
            out.add(kw)
            break
    return out


def _record_condition_keywords(product):
    """**整条产品记录**内存在**适用条件 / 限制**表述的治疗手段集合（官方 SDI-4 残余 L）

    口径（**三条通道合并成一个集合** → 两个产出分支行为一致）：
      ① 文本叶子：逐个**文本叶子**独立判定 —— 某个治疗手段出现所在的**子句**里
         带适用条件（仅限指定医院 / 需转诊 / 预授权 / 目录内 / 符合条件 …）
         → 该治疗手段在本产品记录内**带条件** → 不得**无条件**宣称
         （跨字段 / 跨元素同样成立）；
      ② 结构化条目：结构化权威字段里的条目携带**适用条件字段**
         （condition / eligibility / requirement / restrictions …）
         → 同样属「带条件」→ 条件无法在对外文案里渲染 → 不得无条件宣称；
      ③ **跨叶子**条件（官方 SDI-4 残余 L · F23.1）：条件出现在**别的叶子**
         （key_benefits 的另一个元素 / highlights）→ 无法可靠归属到具体治疗
         手段 → 该手段在本产品记录内属「带条件」→ 不得无条件宣称。

    ⚠ 官方 2026-11-18 线上复扫（v2.4.21）SDI-4 remediation 原文：
      「if a conflict or condition cannot be reliably interpreted and rendered,
        suppress the claim and report it as unverified.」
      → 条件通道**不得**只扫自由文本叶子（结构化条件此前**漏扫** → 泄漏）。
    """
    out = _record_flagged_keywords(product, _has_condition)
    out |= _structured_condition_keywords(product)
    out |= _medical_cross_leaf_condition_keywords(product)
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


def _has_uncertainty(blob, lo, hi):
    """片段内是否存在**疑问 / 不确定 / 条件性 / 待核实**表述 → 肯定授权证据不成立

    ⚠ 官方 SDI-4 残余 K（2026-11-18 线上复扫 · v2.4.20 · Excessive Agency · MEDIUM）：
      「The affirmative-evidence check accepts words such as 「报销」 or 「含」 without
        establishing that the surrounding statement actually confirms coverage.」

    口径：肯定授权**不能只靠关键字在场**。字段元素里出现疑问（是否报销）、
          不确定性（可能包含）、条件性（以核保结果为准）、待核实（待核实）
          → 该次出现的肯定证据**不成立** → 按 unverified 压制，**不**产出无条件宣称。
    """
    if not blob or lo >= hi or hi > len(blob):
        return False
    seg = blob[lo:hi]
    for m in _UNCERTAINTY_MARKERS:
        if m in seg:
            return True
    return bool(_RE_SUBJECT_TO.search(seg))


def _has_condition(blob, lo, hi):
    """片段内是否存在**适用条件 / 限制** → 肯定授权证据不成立

    ⚠ 官方 SDI-4 残余 L（2026-11-18 线上复扫 · v2.4.21 · Excessive Agency · MEDIUM）：
      「conditional text such as 「仅限指定医院CAR-T治疗可报销」 can pass and become the
        unconditional output 「含CAR-T治疗」, losing the hospital restriction.」

    口径：条件无法在对外文案里渲染 → 该次出现的肯定证据**不成立** → 压制。
    """
    if not blob or lo >= hi or hi > len(blob):
        return False
    seg = blob[lo:hi]
    for m in _CONDITION_MARKERS:
        if m in seg:
            return True
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
    # ⚠ 不确定 / 条件性表述 → 该次出现的肯定授权证据**不成立**（官方 SDI-4 残余 K）
    #    （「CAR-T治疗是否报销待核实」「可能包含CAR-T治疗」「CAR-T报销以核保结果为准」
    #      → 肯定关键字在场，但这句话**并没有**确认承保 → 按 unverified 压制）
    if _has_uncertainty(blob, el_lo, el_hi):
        return False
    # ⚠ 适用条件 / 限制 → 同样不构成无条件授权（官方 SDI-4 残余 L）
    if _has_condition(blob, el_lo, el_hi):
        return False
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
    # ⚠ 记录级**不确定**证据（官方 SDI-4 残余 K · 2026-11-18 线上复扫 · v2.4.20）：
    #   同一治疗手段在记录内任一处带疑问 / 不确定 / 条件性 / 待核实表述
    #   → 属「未经确认」→ 一律不宣称（跨字段 / 跨元素同样成立）。
    record_uncertain = _record_uncertain_keywords(product)
    # ⚠ 记录级**适用条件**证据（官方 SDI-4 残余 L · 2026-11-18 线上复扫 · v2.4.21）：
    #   同一治疗手段在记录内任一处带适用条件（仅限指定医院 / 需转诊 / 目录内 …）
    #   → 条件无法渲染 → 不得**无条件**宣称。
    record_condition = _record_condition_keywords(product)
    claims = []
    for kw in _TREATMENT_CLAIMS:
        k_occ = [o for o in occurrences if o[0] == kw]
        if not k_occ:
            continue
        negated = [o for o in k_occ
                   if _keyword_is_negated(blob, o[1], o[2],
                                          (occurrences, spans, bound))]
        # ⑩-1 **结构化压制闸**（官方 2026-11-18 线上复扫 · 2.4.17 · SDI-4
        #      remediation 原文）：
        #        「suppress the claim if any entry is negative, contradictory,
        #          ambiguous, or malformed; free text must not override these
        #          states」
        #        「apply this gate to every claim-generation branch」
        #      → 匹配条目为 negative / contradictory / ambiguous（= 畸形）时，
        #        该治疗手段在本产品上**一律不得**被宣称（与条款正文怎么写无关）。
        #      → 该闸在**每一个宣称生成分支**（非否定分支 + mixed-negation
        #        分支）都必须过 —— 自由文本**不得**覆盖结构化状态。
        structured_denies = _structured_authority_denies(product, kw)
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
            if ok and kw in record_uncertain:
                # 不确定证据出现在**其它字段**（记录级）→ 同样按 unverified 处理
                ok = False
            if ok and kw in record_condition:
                # 适用条件出现在**其它字段**（记录级）→ 不得无条件宣称
                ok = False
            # ⑩-1-1 结构化压制闸（**每一个宣称生成分支**都必须过）：
            #      自由文本肯定证据**不得**覆盖结构化状态
            #      （官方 2.4.17 复扫 SDI-4 · free text must not override）。
            if ok and structured_denies:
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
        # ⚠ 记录级不确定证据 → 一律压制（**不得**被结构化裁决翻案：
        #   官方口径「Treat ... uncertainty ... and conflicting evidence as unverified」）
        if ok and kw in record_uncertain:
            ok = False
        if ok and kw in record_condition:
            ok = False
        # ⑩-1-2 结构化压制闸（**每一个宣称生成分支**都必须过）：
        #      自由文本肯定证据**不得**覆盖结构化状态
        #      （官方 2.4.17 复扫 SDI-4 · free text must not override）。
        if ok and structured_denies:
            ok = False
        if ok:
            claims.append(kw)
    return claims


def _medical_treatment_suffix(product):
    """治疗手段后缀（仅当产品真实字段授权时才有；无授权返回空串）。"""
    claims = _medical_treatment_claims(product)
    if not claims:
        return ""
    return "，含" + "、".join(claims) + "治疗"


def _medical_treatment_unverified_limitation(product):
    """医疗险治疗手段被**结构化权威条目**压制时的**如实限制说明** → dict | None

    官方 SDI-4 残余 W（2026-11-24 公开复扫 · china v2.4.37 / ai v2.4.41 ·
    Excessive Agency · MEDIUM · confidence 0.99）remediation 原文：
      「…contradictory or uninterpretable entries must suppress affirmative claims.」
      「…asserting that no treatment claim is emitted and an unverified limitation
        is reported.」

    ⇒ 结构化条目（`treatment_coverage` / `coverage_items` / …）对某个治疗手段
      给出**自相矛盾**（`covered=True` + `payment_status="不予给付"`）或
      **畸形 / 不可解释**的决定 → 该治疗手段**不得**被宣称
      → 方案层必须**如实报告**该限制，**不得**静默留空。

    ⚠ 口径**只覆盖结构化权威字段**（`_structured_authority_denies`）：
      自由文本的除外证据由 `_record_exclusion_keywords` 通道处理（残余 V/Y
      已验收），**不**在本限制通道里重复报告（避免与既有口径冲突）。
    ⚠ 真实语料实测：`coverage_items` / `covered_treatments` /
      `treatment_coverage` / `treatment_responsibilities` 四个结构化权威字段
      在两库产品库中**均为 0 款** → 本通道对真实语料**零影响**。
    """
    if not product:
        return None
    text = _medical_fact_text(product)
    if not text:
        return None
    denied = [kw for kw in _TREATMENT_CLAIMS
              if kw in text and _structured_authority_denies(product, kw)]
    if not denied:
        return None
    return {
        "type": "coverage_limit",
        "product_type": "医疗险",
        "product": product.get("name"),
        "requirement": "治疗手段保障责任",
        "reason": ("产品结构化保障条目对「%s」的承保决定自相矛盾或无法解释，"
                   "相关治疗手段保障范围待核实，已不作对外宣称"
                   % "、".join(denied)),
    }


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


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 N · 第二轮（2026-11-21 线上复扫 · v2.4.26 · Excessive Agency）
#
#   finding (china 2.4.26):
#     「The critical-illness benefit generator can turn an explicit mild-illness
#       exclusion into an affirmative coverage claim.」
#   explanation (china 2.4.26):
#     「The exclusion guard remains incomplete: highlights such as 「120种重疾，不保轻症」
#       pass because _crx_subject_unconfirmed does not recognize 「不保」 before the
#       subject, causing _crx_disease_claim to output 「120种重疾+轻症保障」.」
#   explanation (ai 2.4.26):
#     「The exclusion guard recognizes only selected negation phrases and word orders:
#       for example, highlights containing 「120种重疾，不承保轻症」 pass because
#       「不承保」 is checked after the subject but not before it.」
#   remediation:
#     「If free-text interpretation remains necessary, handle exclusions before and
#       after the subject consistently rather than relying on a small prefix list,
#       and reconcile contradictory evidence throughout the product record.」
#
# 旧实现的缺陷（**词序单向**）：
#   head（subject 之前）只用极小的前缀表（不含 / 不包含 / 不包括 / 不纳入 / 不涵盖 /
#   不覆盖 + head.endswith("无")），tail（subject 之后）才有完整标记表
#   → 「120种重疾，不承保轻症」「不保轻症」「不赔轻症」等**前置除外**被漏判
#   → 明确除外被反转成肯定承保宣称。
#
# 本轮修复：
#   ① head / tail **共用同一套**除外标记集合（词序双向，词序无关）；
#   ② 标记与 subject 之间**允许填充词**（不承保的轻症 / 不承保轻症疾病）；
#   ③ post-subject 除外（轻症不保 / 轻症除外 / 轻症不予赔付）同样压制；
#   ④ 矛盾陈述（既有肯定又有除外）压制；
#   ⑤ 弱标记「无」必须**紧邻** subject（避免「无明显缺点 / 无重大既往症」误伤）；
#   ⑥ 除外标记若指向**另一个保障对象**（住院津贴 / 身故责任 …）→ 与 subject 无关。
# ══════════════════════════════════════════════════════════════════════

# 统一除外标记集合（head / tail **双向共用**）
_CRX_EXCLUSION_MARKERS = (
    # ⚠⚠ 官方 SDI-4 残余 AD（2026-11-26 公开复扫 · ai v2.4.46 /
    #   china v2.4.43 · Excessive Agency · MEDIUM）：
    #   本路径**从未**消费共享归一化词表的**范围族**
    #   （`_SHARED_EXCLUSION_SCOPE` =「不在承保范围」「不属于承保范围」）
    #   → 记录级轻症除外漏判 → 官方场景（highlights「120种重疾，含轻症保障」
    #   + **另一字段**「轻症不在承保范围」）→ 产出「120种重疾+轻症保障」
    #   —— 把**明确除外**反转成**承保宣称**。
    # ⇒ 本路径改为**从共享语义族派生**（**单一事实源** · 官方 remediation 原文
    #   「Derive … exclusion recognition from one normalized vocabulary and
    #    shared semantic patterns」）—— **只引用、不另抄一份**：
    #   ① 类别级语义族（不含 / 不包含 / 不包括 + 不纳入 / 不涵盖 / 不覆盖）
    *_EXCL_CATEGORY_LITERALS,
    #   ② 范围级语义族（不在承保范围 / 不属于承保范围 + 不在保障范围 / …）
    #      ⚠ 官方残余 AD 的**核心**修复点：scope 家族**首次**进入本路径。
    *_EXCL_SCOPE_LITERALS,
    #   ③ 主体级语义族（官方残余 AA：「不予承保」**before and after the
    #      subject** 双向命中 —— 「轻症不予承保」与「不予承保轻症」**都**判除外 ✓
    #      官方原文：「explicitly recognizing 「不予承保」 before and after the
    #      subject」）
    *_SHARED_EXCLUSION_SUBJECT,
    *_EXCL_SUBJECT_EXTRA_LITERALS,
    #   ④ 不予给付级语义族（不予给付 / 不予赔付 / 不予支付 / 不予报销 …）
    *_EXCL_NONPAYMENT_LITERALS,
    # ── 路径**特有**成员（既有口径 · 只增不改）──
    "不保", "不赔", "不支持", "不负责", "不承担",
    "无保障", "责任免除", "除外",
)
# 弱标记：必须**紧邻** subject 才算除外
# （全语料 62 款产品的非 highlights 字段含「无」字样，如「无明显缺点」
#   「无重大既往症」「无条件」——子串匹配会大面积误伤）
_CRX_EXCLUSION_WEAK_MARKERS = ("无",)
# 弱标记在 subject **之后**时允许的搭配（避免「无上限」这类中性表述被当成除外）
_CRX_WEAK_TAIL_FORMS = (
    "无保障", "无理赔", "无给付", "无赔付", "无责任", "无条件",
    "无限制", "无承保", "无保单", "无豁免", "无附加",
)
# 除外标记若指向**另一个保障对象** → 该除外与 subject 无关
#
# ⚠ 官方 SDI-4 残余 P（remediation 后半句）落地后，本表**只服务于非「症」主体**
#   （= 「120种重疾」等**病种数**主体）路径，且口径**保持不变**（避免口径漂移）。
#   「症」结尾主体（轻症路径）改用**分层口径**：Tier A 确凿对象 / Tier B 泛用词
#   → 见 `_CRX_DISTINCT_OBJECT_CUES` / `_CRX_GENERIC_CUE_WORDS`。
_CRX_OTHER_OBJECT_CUES = (
    "住院津贴", "津贴", "身故", "死亡", "全残", "伤残", "豁免", "等待期",
    "犹豫期", "护理", "年金", "现金价值", "满期", "返还", "增值", "保费",
    "免赔额", "免赔", "投保", "地区", "城市", "医院", "门诊", "职业",
    "分红", "万能", "账户", "储蓄", "意外", "续保", "住院", "医疗",
    "费用", "手术", "药品", "特药", "交通", "救护", "康复", "母婴",
    "生育", "体检", "牙齿", "寿险", "定寿", "重疾", "疾病", "给付",
)
# 肯定承保线索（矛盾陈述判定用）
_CRX_AFFIRMATIVE_CUES = (
    "包含", "覆盖", "保障", "承保", "赔付", "给付", "保险金", "含", "保",
)

# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 P（2026-11-22 线上复扫 · v2.4.30 · Excessive Agency · MEDIUM）
#
#   finding（ai v2.4.30 · L2119-2125 · 原文）：
#     "The mild-illness exclusion guard can convert an explicit exclusion into an
#      affirmative benefit claim."
#   remediation（ai v2.4.30 · 原文）：
#     "Replace keyword-presence authorization with validated, structured mild-illness
#      coverage decisions, preserving applicable conditions and suppressing unresolved
#      claims. If free-text parsing remains necessary, recognize「轻症疾病」as the same
#      coverage subject as「轻症」rather than treating「疾病」as a different object, and
#      handle exclusions consistently before and after that subject. Add regression tests
#      for「120种重疾，轻症疾病不保」and similar variants, asserting that the final
#      generated plans never claim mild-illness coverage."
#
# 根因（主侧已坐实）：
#   `_crx_clause_excludes_subject` 的 tail 侧 gap 分析会检查「除外标记与 subject
#   之间的填充段」是否指向**别的保障对象** —— 而 `_CRX_OTHER_OBJECT_CUES` 里含
#   「疾病」/「给付」→ 「轻症**疾病**不保」的 before 段 = 「疾病」→ 命中 cue →
#   `continue` → **除外被跳过** → 轻症仍被宣称。
#
#   ⇒ 官方口径：「轻症疾病」与「轻症」是**同一 coverage subject**，
#     「疾病」不得被当成别的对象；且 subject 前后的除外须**一致处理**。
#
# 修法：subject occurrence 扫描时**向前（tail 侧）吞掉属于 subject 自身的
#   宾语尾巴**（「疾病」/「特定疾病」）→ tail 从「轻症疾病」之后开始算。
#   ⇒ 「轻症疾病不保」→ tail = 「不保」→ before 段 = "" → 判定为除外 ✓
#   ⇒ 「轻症疾病保险金」（利益名称，非除外）→ tail = 「保险金」→ 无除外标记 ✓
# ══════════════════════════════════════════════════════════════════════

# subject 自身的宾语尾巴（属于**同一 coverage subject**，不是别的保障对象）
_CRX_SUBJECT_OWN_TAILS = ("特定疾病", "疾病")


def _crx_subject_span_end(clause, occ, subject):
    """subject occurrence 的**结束位置**（含属于 subject 自身的宾语尾巴）。

    官方口径（残余 P · remediation 原文）：
      「recognize「轻症疾病」as the same coverage subject as「轻症」rather than
        treating「疾病」as a different object」

    → 「轻症」后面紧跟的「疾病 / 特定疾病」属于 subject 自身的措辞，
      **不得**被 `_crx_gap_targets_other_object` 当成「别的保障对象」。

    ⚠ 只对以「症」结尾的 subject 生效（轻症 / 重症 …）；
      「120种重疾」等**病种数** subject 不受影响（它不以「症」结尾）。
    """
    end = occ + len(subject)
    if not subject.endswith("症"):
        return end
    for tail_form in _CRX_SUBJECT_OWN_TAILS:
        if clause.startswith(tail_form, end):
            return end + len(tail_form)
    return end


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 R（2026-11-23 线上复扫 · v2.4.32 · Excessive Agency · MEDIUM）
#
#   finding（v2.4.32 · L2225-2232 · 原文）：
#     "The mild-illness exclusion guard still treats the excluded benefit's own
#      payment wording as another coverage object."
#   remediation（v2.4.32 · 原文）：
#     "Prefer explicitly validated, structured mild-illness coverage decisions
#      rather than keyword-presence authorization. If free-text parsing remains
#      necessary, recognize payment and benefit-responsibility wording as part of
#      the same coverage subject, bind exclusions consistently in both directions,
#      and suppress unresolved interpretations. Add regression tests for
#      「轻症给付责任除外」, related payment-wording variants, and conflicting fields,
#      asserting that final generated plans never advertise excluded mild-illness coverage."
#
#   finding（v2.4.32 · L2779-2795 · 原文）：
#     "Critical-illness exclusion suppression is bypassed by premium benefits and plan features."
#   remediation（v2.4.32 · 原文）：
#     "Compute a shared, validated critical-illness coverage state before generating any
#      benefits, features, or descriptions. Apply exclusion and unresolved-conflict
#      suppression to both standard and premium branches and every downstream claim
#      surface, preserving an explicit unverified limitation instead. Add end-to-end
#      tests with category-level exclusions that verify the final JSON contains no
#      affirmative claims about the excluded coverage."
#
# 根因（主侧已坐实 · 非猜测）：
#   ① 残余 R-1：`_CRX_OTHER_OBJECT_CUES` 含「给付」→ 主体**自身**的给付措辞
#      （「轻症给付责任除外」的 before 段 = 「给付责任」）被判成
#      「别的保障对象」→ 除外被跳过 → 轻症仍被肯定宣称。
#      ⇒ 同构先例：病种数路径已有 `_CRX_COUNT_OTHER_OBJECT_CUES`
#        （剔除「重疾 / 疾病 / 给付」）→ 轻症主体路径需**同构**的
#        「主体自身给付措辞」豁免表，且**双向一致**
#        （后向「轻症给付责任除外」+ 前向「给付责任不保轻症」）。
#   ② 残余 R-2 / R-3：`_crx_key_benefits` 的 premium 分支在除外闸门**之前**
#      就 return；`_crx_feature()` 完全无视除外状态；`_build_plan_description()`
#      仍拼「含重疾保障」→ benefits / features / description 三个宣称面全部泄漏。
#      ⇒ 官方正解：「Compute a shared, validated critical-illness coverage state
#        before generating any benefits, features, or descriptions.」
# ══════════════════════════════════════════════════════════════════════

# 主体**自身**的给付措辞（属于同一 coverage subject，**不是**别的保障对象）
#   官方 remediation 原文：「recognize payment and benefit-responsibility wording
#     as part of the same coverage subject」
_CRX_SUBJECT_OWN_PAYMENT_CUES = (
    "给付责任除外", "保险金责任除外", "给付责任", "保险金责任", "赔付责任",
    "给付", "保险金", "赔付", "责任",
)


def _crx_strip_subject_own_payment(gap):
    """剔除 gap 段中属于**主体自身**的给付措辞（给付 / 保险金 / 赔付 / 责任 …）

    ⇒ 剔除后仍含「别的保障对象」线索才算指向别的对象：
      「给付责任」     → ""            → 不再被当成别的对象 ✓（残余 R-1 修复点）
      「住院津贴给付」 → 「住院津贴」   → 仍是别的保障对象 ✓（不误伤）
      「重疾给付责任」 → 「重疾」       → 仍是别的保障对象 ✓（不误伤）
    """
    if not gap:
        return ""
    out = gap
    for cue in _CRX_SUBJECT_OWN_PAYMENT_CUES:
        if cue in out:
            out = out.replace(cue, "")
    return out


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 P · remediation **后半句**（2026-11-24 落地）
#
#   官方 remediation（china v2.4.30 · 逐字原文 · 同条 SDI-4 的另一半要求）：
#     "Normalize coverage subjects and their extensions, such as 「轻症」and
#      「轻症疾病」, before resolving exclusion scope. Require evidence of a
#      genuinely distinct coverage object rather than accepting any generic
#      cue substring; suppress claims when the exclusion target is ambiguous.
#      Add tests for post-subject exclusions, subject extensions, and
#      contradictory fields, checking final plan benefits rather than only
#      helper outputs."
#
#   未落地部分（本次修）：`_crx_gap_targets_other_object()` 只要 gap 里出现
#   **任意一个** `_CRX_OTHER_OBJECT_CUES` 子串就判定「指向别的保障对象」
#   → 该除外标记与 subject 无关 → 除外被跳过 → 轻症仍被肯定宣称（泄漏）。
#   而 `_CRX_OTHER_OBJECT_CUES` 混入了大量**泛用词 / 政策词**
#   （疾病 / 给付 / 医疗 / 住院 / 费用 / 保费 / 等待期 …）→
#   「轻症医疗保障不保」「轻症费用不赔」这类**明确针对轻症**的除外
#   会被误当成「指向别的保障对象」→ 除外被跳过 → 轻症仍被宣称。
#
#   修法（官方口径落地）：
#     ① gap 必须命中 **Tier A · 确凿的独立保障对象** 才算「指向别的保障对象」；
#        只命中 **Tier B · 泛用词 / 政策词**（或完全不认识）→ **歧义**
#        → 官方口径「suppress claims when the exclusion target is ambiguous」
#        → 判定为**对 subject 的除外** → 压制轻症宣称。
#     ② 主体**自身的延伸措辞**（疾病 / 给付 / 保险金 / 赔付 / 责任 / 保障 …）
#        在 gap 判定前先剔除（官方口径「Normalize coverage subjects and
#        their extensions」）。
#
#   ⚠ 与**病种数**路径的口径差异（官方对此敏感 · 必须写清）：
#     · 病种数路径（`_crx_clause_excludes_disease_count` +
#       `_crx_count_object_is_other`）判的是「除外标记**之后**的宾语是否指向
#       别的对象」，其线索表 `_CRX_COUNT_OTHER_OBJECT_CUES` 建表时已**剔除**
#       「重疾 / 疾病 / 给付」（病种数自身的给付对象不能算别的对象）；
#     · 轻症主体路径（`_crx_subject_gap_targets_other_object`）判的是
#       「主体与除外标记之间的**缺口**是否指向别的对象」，且**必须**命中
#       Tier A 确凿对象才算证据（泛用词**不**算证据）；
#     · 两条路径**口径不同且各自保持不变** —— 本轮**不动**病种数路径
#       （避免口径漂移引发新回归）。
# ══════════════════════════════════════════════════════════════════════

# Tier A：**确凿的独立保障对象**（命中其一 ⇒ 该除外确实指向别的保障对象）
#   收录标准：① 该词本身就是**另一个险种 / 保障责任**的名称；
#            ② **不可能**是「轻症」这个 coverage subject 的自身措辞
#               （自身措辞 = 疾病 / 给付 / 保险金 / 赔付 / 责任 / 保障 …）。
#   ⚠ 多字短语必须**显式**收录 —— 剥离主体自身措辞时不得吃掉区分性成分：
#     「住院医疗」→ 剥「医疗」后仍剩「住院」✓、「意外医疗」→ 仍剩「意外」✓。
_CRX_DISTINCT_OBJECT_CUES = (
    # ── 多字短语（区分性成分优先）──
    "住院津贴", "住院医疗", "住院费用", "住院观察",
    "意外医疗", "意外伤害", "意外身故", "意外伤残", "意外死亡",
    "医疗费用", "百万医疗", "门急诊", "门诊医疗", "门诊费用",
    "特药费用", "特定药品", "特殊药品", "疾病终末期",
    # ── 独立保障对象 / 险种名词（不可能是「轻症」的自身措辞）──
    "津贴", "身故", "死亡", "全残", "伤残", "残疾", "豁免",
    "护理", "年金", "现金价值", "满期", "返还", "增值",
    "分红", "万能", "账户", "储蓄", "寿险", "定寿",
    "住院", "意外", "门诊", "手术", "药品", "特药",
    "交通", "救护", "康复", "母婴", "生育", "体检", "牙齿",
    "重疾", "重大疾病", "中症",
)
# Tier B：**泛用词 / 政策词**（**单独**出现**不构成**「别的保障对象」的证据）
#   官方口径：generic cue substring **不得**被当成「指向别的保障对象」的证据。
_CRX_GENERIC_CUE_WORDS = (
    # 主体自身的措辞（部分已由 own-payment / own-extension 表先行剔除）
    "疾病", "特定疾病", "给付", "保险金", "赔付", "责任", "保障",
    # 泛用业务词
    "费用", "保费", "保额", "保险", "医疗", "范围", "条件", "标准", "比例", "金额",
    # 政策 / 流程词
    "等待期", "犹豫期", "续保", "投保", "地区", "城市", "医院", "职业",
    "免赔额", "免赔", "核保", "等待", "生效",
)
# 主体**自身**的延伸措辞（coverage subject 的 extension）
#   官方口径：「Normalize coverage subjects and their extensions」
#   ⚠ 这类词**不得**计入 Tier A 判定（否则「轻症保障」「轻症保险」会被当成
#     别的保障对象 → 除外被跳过 → 泄漏）。
_CRX_SUBJECT_OWN_EXTENSION_CUES = ("保障", "保险")


# 同家族（**重疾家族**）保障名词 —— **不得**作为「别的保障对象」的证据
#   语义：「重疾 / 重大疾病 / 中症」与「轻症」属于**同一保障家族**
#     （同一 coverage family），**不是**「另一个保障对象」。
#   ⇒ 「120种重疾不含轻症」=「120 种重疾，**不含**轻症」→ 「不含」**后向绑定**
#     「轻症」→ 轻症被除外 → 整句「N种重疾+轻症保障」必须被压制。
#   ⚠ 作用域**仅限** head 侧「前序片段是否指向别的保障对象」这条判定；
#     病种数路径（`_crx_clause_excludes_disease_count` /
#     `_crx_count_object_is_other` / `_CRX_COUNT_OTHER_OBJECT_CUES`）与
#     残余 P 的 Tier A·B 分层口径（`_CRX_DISTINCT_OBJECT_CUES` /
#     `_CRX_GENERIC_CUE_WORDS` / `_crx_gap_object_evidence`）**一字不动**
#     （避免口径漂移引发新回归）。
_CRX_SAME_FAMILY_CUES = ("重疾", "重大疾病", "中症", "轻症")


def _crx_strip_same_family_cues(text):
    """剔除**同家族**（重疾家族）保障名词 —— 用于「是否指向**别的**保障对象」判定

    ⇒ 前序片段若**只**靠同家族 cue 命中 Tier A → 不算「别的对象」：
      「120种重疾」   → 「120种」   → 不再命中 Tier A → **不是别的对象** ✓
      「重疾」         → 「」        → 不是别的对象 ✓
      「住院津贴」     → 「住院津贴」 → 仍是别的对象 ✓（不误伤）
      「重疾住院津贴」 → 「住院津贴」 → 仍是别的对象 ✓（不误伤）
    """
    if not text:
        return ""
    out = text
    for cue in _CRX_SAME_FAMILY_CUES:
        if cue in out:
            out = out.replace(cue, "")
    return out


def _crx_strip_subject_own_extension(gap):
    """剔除 gap 段中属于**主体自身**的延伸措辞（保障 / 保险 …）

    ⇒ 剔除后仍含「确凿的独立保障对象」才算指向别的对象：
      「医疗保障」 → 「医疗」     → 只是泛用词 → **歧义** → 判为对轻症的除外 ✓
      「住院保障」 → 「住院」     → 仍是别的保障对象 ✓（不误伤）
      「意外医疗」 → 「意外医疗」 → 仍是别的保障对象 ✓（不误伤）
    """
    if not gap:
        return ""
    out = gap
    for cue in _CRX_SUBJECT_OWN_EXTENSION_CUES:
        if cue in out:
            out = out.replace(cue, "")
    return out


def _crx_gap_object_evidence(gap):
    """gap 段的「指向别的保障对象」证据分类 → "distinct" | "generic" | "unknown"

    官方 remediation（逐字）：
      "Require evidence of a genuinely distinct coverage object rather than
       accepting any generic cue substring; suppress claims when the
       exclusion target is ambiguous."

    · "distinct" → gap 命中 Tier A（**确凿的独立保障对象**）→ 该除外指向别的对象
    · "generic"  → gap 只含 Tier B 泛用词 / 政策词 → **不构成**证据 → 歧义
    · "unknown"  → gap 既非确凿对象、也非已知泛用词 → 同样**不构成**证据 → 歧义
    ⚠ 「generic」与「unknown」都**不构成**证据 → 官方口径「歧义时压制宣称」。
    """
    if not gap:
        return "unknown"
    stripped = _crx_strip_subject_own_payment(gap)
    stripped = _crx_strip_subject_own_extension(stripped)
    if not stripped:
        return "unknown"
    for cue in _CRX_DISTINCT_OBJECT_CUES:
        if cue in stripped:
            return "distinct"
    for cue in _CRX_GENERIC_CUE_WORDS:
        if cue in stripped:
            return "generic"
    return "unknown"


def _crx_subject_gap_targets_other_object(gap, subject):
    """gap 段是否指向**另一个保障对象**（**主体自身**措辞先剔除 + 须有**确凿**证据）

    ⚠ 只对「轻症」类主体（以「症」结尾）生效 ——
      「N种重疾」等病种数主体走**病种数专属**口径
      （`_crx_count_object_is_other`），不受本口径影响（避免口径漂移）。

    官方口径（残余 P · remediation 后半句 · 逐字）：
      "Require evidence of a genuinely distinct coverage object rather than
       accepting any generic cue substring; suppress claims when the
       exclusion target is ambiguous."
    → 「症」结尾主体（轻症路径）：gap 必须命中 Tier A **确凿的独立保障对象**
      才算「指向别的保障对象」；只命中泛用词 / 不认识 → **歧义** → False
      （= 该除外视为针对本主体 → 压制轻症宣称）。
    → 非「症」主体（病种数路径）：沿用既有 `_CRX_OTHER_OBJECT_CUES` 口径（**不动**）。
    """
    if subject and subject.endswith("症"):
        return _crx_gap_object_evidence(gap) == "distinct"
    return _crx_gap_targets_other_object(gap)


# 否定语境守卫：线索**前 2 字**内出现这些字 → 该线索不是肯定表述
_CRX_NEGATION_GUARDS = ("不", "未", "无", "非", "除", "免", "拒", "勿")


def _crx_occurrences(text, subject):
    """subject 在 text 中的**全部**出现位置（词序无关的扫描基础）。"""
    out = []
    if not text or not subject:
        return out
    start = 0
    while True:
        i = text.find(subject, start)
        if i == -1:
            return out
        out.append(i)
        start = i + len(subject)


def _crx_gap_targets_other_object(gap):
    """gap 段是否指向**另一个保障对象**（住院津贴 / 身故责任 …）

    → 该除外表述与 subject 无关（避免「含轻症，不保住院津贴」被误伤）。
    """
    if not gap:
        return False
    for cue in _CRX_OTHER_OBJECT_CUES:
        if cue in gap:
            return True
    return False


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 T（2026-11-24 落地 · v2.4.35 公开复扫 · Excessive Agency · MEDIUM）
#
#   T-1（china v2.4.35 · L3060-3081 · 原文 · 同条 SDI-4）：
#     "The documented record-wide mild-illness exclusion guard can still turn an
#      explicit exclusion into an affirmative benefit claim."
#     explanation（原文）：
#     "The record-wide mild-illness guard relies on an incomplete exclusion
#      vocabulary: for example, highlights containing 「120种重疾，轻症责任免除」 are
#      not recognized as excluding mild-illness coverage because 「责任免除」 is absent
#      from _CRX_EXCLUSION_MARKERS. The shared state consequently permits
#      _crx_disease_claim to produce 「120种重疾+轻症保障」 without an unverified
#      limitation. In an insurance-advice skill, this reversal of an exclusion into an
#      affirmative benefit can mislead purchasing decisions and leave users with
#      unexpected coverage gaps; filesystem and network restrictions do not mitigate
#      this output-integrity risk."
#     remediation（原文）：
#     "Require validated, structured mild-illness coverage decisions before generating
#      affirmative claims, preserving applicable conditions and treating missing,
#      ambiguous, or conflicting evidence as unverified. If free-text parsing remains,
#      recognize responsibility-exemption wording such as 「轻症责任免除」 in both word
#      orders and reconcile exclusions across the entire product record. Apply the
#      resulting state to every benefits, features, and description output, propagate an
#      explicit limitation, and add end-to-end regression tests asserting that excluded
#      mild-illness coverage is never advertised."
#
#   T-2（ai v2.4.35 · L2309-2313 · 原文 · 本库官方原文）：
#     "The mild-illness exclusion guard can discard an explicit exclusion when a
#      different benefit is mentioned afterward, contradicting the documented
#      record-wide suppression guarantee."
#     explanation（原文）：
#     "The tail-side exclusion check discards an exclusion whenever its remaining
#      suffix mentions another benefit, even when the exclusion clearly applies to mild
#      illness. For example, highlights reading 「120种重疾，轻症除外但含身故保障」 cause
#      the guard to overlook 「轻症除外」 because 「身故」 appears afterward, allowing
#      downstream generation of 「120种重疾+轻症保障」 without an unverified-coverage
#      warning."
#     remediation（原文）：
#     "Bind each exclusion to its coverage subject using local grammatical scope; do not
#      discard an already-bound exclusion merely because a subsequent clause introduces
#      another benefit. Prefer validated structured coverage decisions, suppress
#      unresolved interpretations, and propagate the resulting state to benefits,
#      features, descriptions, and explicit limitations. Add end-to-end regression tests
#      for 「120种重疾，轻症除外但含身故保障」 and equivalent conflicting-field variants in
#      both standard and comprehensive plans."
#
#   修法：
#     ① T-1（词表）：`_CRX_EXCLUSION_MARKERS` 补入 **「责任免除」**
#        → 「轻症责任免除」（后向）/「责任免除轻症」（前向）**双向**生效。
#     ② T-2（绑定）：除外标记按**局部语法作用域**绑定到 coverage subject ——
#        · **后置型**标记（「除外」/「责任免除」/「不在保障范围」/「无保障」）
#          出现在 subject **之后** → 绑定**前面的** subject；
#          其后的文本属**后续子句**（「但含身故保障」）→ **不得**推翻已绑定的除外；
#        · **前置型**标记（「不保」/「不含」…）→ 绑定**紧邻的后置宾语**；
#          只有紧邻宾语是**确凿的独立保障对象**时，才与 subject 无关；
#        · head 侧：标记若**紧邻**地跟在**别的保障对象**之后
#          （「住院津贴不保轻症」）→ 它绑定的是**那个对象** → 与 subject 无关。
#
#   ⚠ 口径边界（官方对此敏感）：
#     · 本轮 T-2 的**局部语法作用域**绑定**只对「症」结尾主体**（轻症路径）生效；
#       非「症」主体（病种数路径）沿用既有口径（**一字未动**，避免口径漂移）。
#     · 「责任免除」补入的是**共享**标记表 → 病种数路径同步受益
#       （「120种重疾责任免除」此前不被识别为病种数除外）。
# ══════════════════════════════════════════════════════════════════════

# **后置型**除外标记：标记出现在 subject **之后** → 绑定**前面的** subject
#   （「轻症除外」/「轻症责任免除」= 轻症被除外）
#   → 其后的文本属**后续子句**（「但含身故保障」）→ **不得**推翻已绑定的除外
#   （官方 T-2 原文：do not discard an already-bound exclusion merely because a
#     subsequent clause introduces another benefit.）
_CRX_POSTPOSED_EXCLUSION_MARKERS = (
    "责任免除", "除外", "不在保障范围", "无保障",
    # ⚠ 官方 SDI-4 残余 AD：共享归一化词表的**范围族**与「不在保障范围」**同口径**
    #   （后置型 → 绑定**前面的** subject；后续子句不得撤销已绑定的除外）。
    *_SHARED_EXCLUSION_SCOPE,
)
# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 U（2026-11-24 公开复扫 · v2.4.36 · Excessive Agency · MEDIUM）
#
#   除外标记的**绑定方向**（局部语法作用域 · 官方 remediation 原文）：
#     "postposed markers such as 「除外」 and 「责任免除」 must remain attached to
#      the preceding disease-count subject, regardless of a subsequent benefit
#      clause. Distinguish these from forward-binding exclusions such as
#      「不含轻症」 …"
#
#   · **后向绑定**（postposed）→ 绑定到标记**前面**的主体；
#     其后的「但含身故保障」属**后续子句** → **不得**撤销已绑定的除外。
#   · **前向绑定**（preposed）→ 绑定到标记**后面**的宾语
#     （现行口径**保持不变**：「不含轻症」→ 除外的是轻症，不是病种数）。
#
# ⚠ **不得**复用 / 扩写 `_CRX_POSTPOSED_EXCLUSION_MARKERS`（那是**轻症路径**
#   残余 T 的口径，扩写会改变「轻症不予给付住院津贴」的判定 → 回归）。
_CRX_BACKWARD_BINDING_MARKERS = (
    "不在保障责任范围", "不在保障范围", "无保障", "责任免除", "除外",
    "不予给付", "不予赔付", "不予支付",
    # ⚠ 官方 SDI-4 残余 AD：共享归一化词表的**范围族**进入两条 CRX 路径
    #   → 范围级除外标记与「不在保障范围」**同口径**（后向绑定：绑定**前面**的
    #     主体；其后的「但含身故保障」属**后续子句** → **不得**撤销已绑定的除外）。
    *_SHARED_EXCLUSION_SCOPE,
)
# 局部语法作用域的边界 ①：子句分隔符
_CRX_SCOPE_BREAK_CHARS = "，。；！？、,;!?"
# 局部语法作用域的边界 ②：引入**后续子句**的连接词 / 保障动词
_CRX_SCOPE_CONNECTORS = (
    "但", "而", "且", "并", "同时", "另", "以及", "不过", "然而", "其中",
    "则", "还", "也", "含", "包含", "覆盖", "涵盖", "包括", "保障", "承保",
    "赠送", "可选", "提供",
)
# 紧邻宾语片段的窗口长度上限（与既有肯定线索窗口同口径：12 字）
_CRX_ADJACENT_OBJECT_WINDOW = 12


def _crx_scope_starts_with_connector(text):
    """片段是否以「连接词 / 保障动词」开头（→ 其前面是**另一个**子句）"""
    if not text:
        return False
    for conn in _CRX_SCOPE_CONNECTORS:
        if text.startswith(conn):
            return True
    return False


def _crx_adjacent_object(text):
    """标记**之后**紧邻的宾语片段（局部语法作用域内 · 官方 T-2）

    → 「不保住院津贴」    → 「住院津贴」（前置标记的宾语 → 别的保障对象 ✓）
    → 「不保，但含身故保障」→ 「」（子句分隔符截断 → 后面不是宾语）
    """
    if not text:
        return ""
    out = []
    for ch in text[:_CRX_ADJACENT_OBJECT_WINDOW]:
        if ch in _CRX_SCOPE_BREAK_CHARS:
            break
        out.append(ch)
    return "".join(out)


def _crx_preceding_object(text):
    """标记**之前**紧邻的宾语片段（局部语法作用域内 · 官方 T-2）

    → 「住院津贴不保轻症」→ 「住院津贴」（标记绑定的是**前面的**对象 → 与轻症无关）
    → 「含重疾不保轻症」  → ""（以保障动词「含」开头 → 前面是另一个子句）
    """
    if not text:
        return ""
    frag = ""
    for ch in reversed(text[-_CRX_ADJACENT_OBJECT_WINDOW:]):
        if ch in _CRX_SCOPE_BREAK_CHARS:
            break
        frag = ch + frag
    if _crx_scope_starts_with_connector(frag):
        return ""
    return frag


def _crx_preceding_binds_other_object(text, pos, subject):
    """标记（位于 text[pos:]）之前紧邻的片段是否指向**别的保障对象**

    官方 T-2（局部语法作用域）：「住院津贴不保轻症」里的「不保」绑定的是
    **前面的**「住院津贴」→ 与轻症无关 → 不得把轻症判成被除外。
    """
    frag = _crx_preceding_object(text[:pos])
    if not frag:
        return False
    if subject and subject in frag:
        return False        # 片段里含 subject **自身** → 不是「别的对象」
    if subject and subject.endswith("症"):
        # ⚠ 同家族（重疾家族）证据**不得**当作「别的保障对象」
        #   「120种重疾不含轻症」→ 前序片段「120种重疾」只是**同家族**主体
        #   → 「不含」**后向绑定**「轻症」→ 除外成立 → 轻症宣称必须压制。
        frag = _crx_strip_same_family_cues(frag)
        if not frag:
            return False
    return _crx_subject_gap_targets_other_object(frag, subject)


# ══════════════════════════════════════════════════════════════════════
# ⚠ 官方 SDI-4 残余 AD（2026-11-26 公开复扫 · ai v2.4.46 / china v2.4.43）
#   官方 china explanation 原文：「they also do not use the shared exclusion
#   regexes」→ 两条 CRX 路径必须消费**同一份** `_EXCL_PATTERNS`。
#
#   通用模式命中 → **等价字面标记**（保证与字面标记**同口径**）：
#     ① 范围级     ≡「不在保障范围」（**后向绑定**）
#     ② 不予给付级 ≡「不予给付」（**后向绑定**）
#     ③ 类别级     ≡「不含」（**前向绑定**）
#   ⇒ 命中后仍走各路径原有的**收紧口径**（紧贴主体 / 填充词上限 /
#     其它保障对象线索 / 条件性语境 …）—— 共享的是**词**与**模式**，
#     不是判定逻辑。
_CRX_PATTERN_EQUIV_MARKER = (
    "不在保障范围",
    "不予给付",
    "不含",
)

# 类别级路径消费的**通用模式**下标（官方残余 AD）
#   ⚠ 模式 ③（类别级「不 + 含|包含|包括|纳入|涵盖|覆盖」）**不**进入类别级路径：
#     类别级路径的类别族**已由共享词表派生**（`_SHARED_EXCLUSION_CATEGORY`
#     = 不含 / 不包含 / 不包括 · 官方残余 AB 原文），而模式 ③ 还会带进
#     「不纳入 / 不涵盖 / 不覆盖」三个**主体路径**专属口径的词 ——
#     真实语料实证：「平安少儿鑫福星2025重疾险**不覆盖**核爆炸」属
#     **其它对象**（核爆炸 / 核辐射）的限定，引入类别级路径会**过度收紧**
#     （误压制该产品的真实重疾宣称）→ 按官方口径
#     「preserving subject-specific scope handling」保持**主体路径专属**。
#   ⇒ 类别级路径消费模式 ①（范围级）+ ②（不予给付级）；主体级路径消费全部。
_CRX_CI_PATTERN_INDICES = (0, 1)


def _crx_pattern_marker_hits(segment, exclude_spans=(), pattern_indices=None):
    """segment 内由**通用模式**（`_EXCL_PATTERNS` · 同一份）命中的除外跨度

    → [(start, end, 等价字面标记), ...]

    ⚠ **只补充**不被**字面标记**覆盖的跨度 → 既有口径**零漂移**
      （既有判定完全由字面标记决定 → 补进去只会**新增**命中，
        不会改变任何既有结论）。
    """
    hits = []
    if not segment:
        return hits
    for _i, _pat in enumerate(_EXCL_PATTERNS):
        if _i >= len(_CRX_PATTERN_EQUIV_MARKER):
            break
        if pattern_indices is not None and _i not in pattern_indices:
            continue
        for _m in re.finditer(_pat, segment):
            _s, _e = _m.start(), _m.end()
            if any(not (_e <= _xs or _s >= _xe) for _xs, _xe in exclude_spans):
                continue
            hits.append((_s, _e, _CRX_PATTERN_EQUIV_MARKER[_i]))
    # 同一跨度只保留一次；重叠时保留**最长**（与既有「同位置取最长匹配」口径一致）
    hits.sort(key=lambda h: (h[0], -h[1]))
    _uniq = []
    _last_end = -1
    for _h in hits:
        if _h[0] < _last_end:
            continue
        _uniq.append(_h)
        _last_end = _h[1]
    return _uniq


def _crx_excl_hit_is_ambiguous(clause, start):
    """该除外命中是否被**对冲词**前置（→ **存疑**，**不是**确定的除外）

    ⚠ 官方 SDI-4 残余 AD · 已知坑（任务书 §⑤·2）：
      「可能无法给付，需以条款为准」这类**存疑**表述**不得**被当成除外 ——
      通用模式 ② 会命中「无法给付」→ 若照单全收 → 把「待核实」说成
      「确定不保」；但**存疑仍然压制**（官方口径：存疑一律不授权 +
      产出「待核实」限制说明）。

    ⇒ 处置：**定长否定前瞻**（窗口 `_EXCL_HEDGE_LOOKBACK` 字符）——
      否定表达**紧邻前置**对冲词 → 该命中判为**存疑**（ambiguous）。
    ⚠ 对冲词**全部取自 `_UNCERTAINTY_MARKERS`** → 对冲 ⟹ 必然命中
      `_has_uncertainty` → 记录级状态判 **unverified** → **仍然压制**。
    ⚠ 窗口在**子句**内取（`_split_clauses` 已按语义边界切分）→ 不跨子句误判。
    """
    if not clause or start <= 0:
        return False
    lo = max(0, start - _EXCL_HEDGE_LOOKBACK)
    prefix = clause[lo:start]
    if not prefix:
        return False
    for _b in _CLAUSE_BREAKS:
        if _b in prefix:
            return False              # 跨子句 → 不算存疑（保守：仍按除外）
    return any(prefix.endswith(_h) for _h in _EXCL_HEDGE_PREFIXES)


def _crx_clause_excludes_subject(clause, subject):
    """clause 内是否存在**指向 subject** 的明确除外表述（双向 + 允许填充词）

    口径：
      · head（subject 之前）出现标记 → 除外（中文否定**前向**绑定：「不承保轻症」）
      · tail（subject 之后）出现标记 → 除外（中文否定**后向**绑定：「轻症不保」）
      · 标记与 subject 之间**允许填充词**（「不承保的轻症」「不承保轻症疾病」）
      · 标记若指向**另一个保障对象** → 与 subject 无关（不压制）
      · ⚠ 官方 SDI-4 残余 P：subject 的**自身措辞**（「轻症疾病」=「轻症」的
        同一 coverage subject）不计入 gap → 「轻症疾病不保」判定为除外 ✓
      · ⚠ 官方 SDI-4 残余 T-2：**局部语法作用域**绑定 ——
        后置型标记绑定**前面的** subject（后续子句里的别的保障对象不得推翻它）；
        前置型标记绑定**紧邻的后置宾语**；head 侧标记若紧邻跟在别的保障对象之后
        → 它绑定的是**那个对象**（「住院津贴不保轻症」→ 与轻症无关）。
    """
    if not clause or not subject:
        return False
    # 「症」结尾主体（轻症路径）走**局部语法作用域**绑定（官方 T-2）；
    # 非「症」主体（病种数路径）沿用既有口径（**不动**，避免口径漂移）。
    _is_mild = bool(subject.endswith("症"))
    for occ in _crx_occurrences(clause, subject):
        head = clause[:occ]
        # ⚠ 官方 SDI-4 残余 P：tail 起点必须落在**subject 自身措辞**之后
        #   （「轻症疾病」= 同一 coverage subject）→ 否则「疾病」会被当成别的对象
        tail = clause[_crx_subject_span_end(clause, occ, subject):]

        # ── head 侧：否定**前向**绑定（标记 → subject）──
        #   ⚠ 官方 SDI-4 残余 AD：head 侧同时消费**同一份** `_EXCL_PATTERNS`
        #     （模式命中按**等价字面标记**参与判定 → 与字面标记同口径）。
        #   ⚠ 模式命中**只补充**不被字面标记覆盖的跨度 → 既有口径零漂移。
        _head_hits = []
        for mk in _CRX_EXCLUSION_MARKERS:
            pos = head.rfind(mk)
            while pos != -1:
                _head_hits.append((pos, pos + len(mk), mk))
                pos = head.rfind(mk, 0, pos)
        _head_hits.sort(key=lambda h: (-h[0], h[1]))
        _lit_head = [(_s, _e) for (_s, _e, _m) in _head_hits]
        for (_s, _e, _mk) in _crx_pattern_marker_hits(head, _lit_head):
            _head_hits.append((_s, _e, _mk))
        _head_hits.sort(key=lambda h: (-h[0], h[1]))
        for (pos, _mk_end, mk) in _head_hits:
            gap = head[pos + len(mk):]
            # ⚠ 官方 SDI-4 残余 T-2：标记若**紧邻**跟在别的保障对象之后
            #   → 它绑定的是**那个对象**（与 subject 无关）→ 跳过
            if _is_mild and _crx_preceding_binds_other_object(head, pos, subject):
                continue
            if (mk in _CRX_BACKWARD_BINDING_MARKERS
                    and _crx_subject_gap_targets_other_object(head[:pos], subject)):
                # ⚠ 官方 SDI-4 残余 U（根因④ · 同源第三处）：
                #   后向绑定标记绑定的是标记**之前**的主体 → 看「标记之前」
                #   的片段；命中**别的保障对象** → 与本主体无关（跳过）。
                continue
            if not _crx_subject_gap_targets_other_object(gap, subject):
                # ⚠ 官方 SDI-4 残余 AD · 已知坑：被对冲词前置的命中
                #   （「可能无法给付」/「可能不在承保范围」）→ **存疑**
                #   （ambiguous，**不是**确定的除外）→ 不算「确定除外」，
                #   但记录级的**存疑**判定仍会压制肯定宣称。
                if _crx_excl_hit_is_ambiguous(clause, occ + pos):
                    continue
                return True
        # 弱标记「无」必须**紧邻** subject
        if head.rstrip().endswith(_CRX_EXCLUSION_WEAK_MARKERS):
            return True

        # ── tail 侧：否定**后向**绑定（subject → 标记）──
        #   ⚠ 官方 SDI-4 残余 AD：tail 侧同时消费**同一份** `_EXCL_PATTERNS`。
        hits = []
        for mk in _CRX_EXCLUSION_MARKERS:
            start = 0
            while True:
                pos = tail.find(mk, start)
                if pos == -1:
                    break
                hits.append((pos, pos + len(mk), mk))
                start = pos + len(mk)
        # 同位置取**最长**匹配（避免「不含」/「不包含」等重叠标记重复计入）
        hits.sort(key=lambda h: (h[0], -h[1]))
        _uniq = []
        _last_end = -1
        for _h in hits:
            if _h[0] < _last_end:
                continue
            _uniq.append(_h)
            _last_end = _h[1]
        hits = _uniq
        # ⚠ 官方 SDI-4 残余 AD：通用模式命中**只补充**不被字面标记覆盖的跨度
        _lit_tail = [(_s, _e) for (_s, _e, _m) in hits]
        for (_s, _e, _mk) in _crx_pattern_marker_hits(tail, _lit_tail):
            hits.append((_s, _e, _mk))
        hits.sort(key=lambda h: (h[0], -h[1]))
        _uniq = []
        _last_end = -1
        for _h in hits:
            if _h[0] < _last_end:
                continue
            _uniq.append(_h)
            _last_end = _h[1]
        hits = _uniq
        for i, (s, e, mk) in enumerate(hits):
            before = tail[hits[i - 1][1] if i else 0:s]
            after = tail[e:]
            if _crx_subject_gap_targets_other_object(before, subject):
                continue
            # ⚠ 官方 SDI-4 残余 AD · 已知坑：被对冲词前置的命中 → **存疑**
            #   （ambiguous）→ 不算「确定除外」，但记录级的**存疑**判定仍压制。
            _abs_start = _crx_subject_span_end(clause, occ, subject) + s
            if _crx_excl_hit_is_ambiguous(clause, _abs_start):
                continue
            if _is_mild:
                # ⚠ 官方 SDI-4 残余 T-2：**局部语法作用域**绑定
                if mk in _CRX_POSTPOSED_EXCLUSION_MARKERS:
                    # 后置型标记 → 绑定**前面的** subject；其后的「但含身故保障」
                    #   属**后续子句** → 不得推翻已绑定的除外
                    return True
                # 前置型标记 → 绑定**紧邻的后置宾语**
                adj = _crx_adjacent_object(after)
                if adj and not _crx_scope_starts_with_connector(adj):
                    if _crx_subject_gap_targets_other_object(adj, subject):
                        continue
                return True
            # 病种数路径（非「症」主体）
            if mk in _CRX_BACKWARD_BINDING_MARKERS:
                # ⚠ 官方 SDI-4 残余 U（根因④ · 同源第三处）：
                #   后向绑定标记 → 绑定**前面**的主体；**后续子句**里的别的保障
                #   对象**不得**撤销已绑定的除外 → **不再**用「标记之后」的窗口
                #   撤销（只看标记**之前**的片段，见上方 `before` 判定）。
                return True
            if _crx_subject_gap_targets_other_object(after, subject):
                continue
            return True
        # 弱标记「无」：仅在紧邻 subject 且搭配属除外语义时成立
        if tail == "无" or any(tail.startswith(f) for f in _CRX_WEAK_TAIL_FORMS):
            return True
    return False


def _crx_has_affirmative_cue(seg):
    """seg 内是否存在**未被否定**的肯定承保线索（否定守卫：线索前 2 字）"""
    if not seg:
        return False
    for cue in _CRX_AFFIRMATIVE_CUES:
        start = 0
        while True:
            pos = seg.find(cue, start)
            if pos == -1:
                break
            start = pos + len(cue)
            pre = seg[max(0, pos - 2):pos]
            if any(g in pre for g in _CRX_NEGATION_GUARDS):
                continue
            return True
    return False


def _crx_clause_affirms_subject(clause, subject):
    """clause 内是否存在**指向 subject 的肯定承保表述**（矛盾陈述判定用）"""
    if not clause or not subject:
        return False
    for occ in _crx_occurrences(clause, subject):
        lo = max(0, occ - 12)
        hi = min(len(clause), occ + len(subject) + 12)
        if _crx_has_affirmative_cue(clause[lo:hi]):
            return True
        pre = clause[max(0, occ - 4):occ].rstrip()
        if pre.endswith("种"):          # 「N种轻症」形态的病种数肯定
            return True
    return False


def _crx_record_contradiction(product, subject):
    """产品记录内是否存在**矛盾陈述**（肯定承保 + 除外并存）→ 未经确认 → 压制

    官方 remediation（原文）：
      「reconcile contradictory evidence throughout the product record」
      「Add regression tests for ... conflicting statements, checking the final
        generated plan.」
    """
    if not product or not subject:
        return False
    affirmative = False
    excluded = False
    for text in _product_text_leaves(product):
        if not isinstance(text, str) or subject not in text:
            continue
        for clause in _split_clauses(text):
            if subject not in clause:
                continue
            if _crx_clause_excludes_subject(clause, subject):
                excluded = True
            if _crx_clause_affirms_subject(clause, subject):
                affirmative = True
    return affirmative and excluded


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 O（2026-11-22 线上复扫 · v2.4.28 · Excessive Agency · MEDIUM）
#
#   finding（两库原文逐字相同）：
#     "Critical-illness disease-count claims bypass the documented record-wide
#      contradiction check."
#   remediation（ai 2.4.28 · 原文）：
#     "Validate disease-count coverage across the entire product record before
#      generating claims, rather than applying record-wide checks only to
#      mild-illness coverage. Prefer a validated, structured disease-count
#      decision with applicable conditions; suppress the count and report it as
#      unverified when exclusions, uncertainty, or conflicting evidence remain
#      unresolved. Add regression tests with affirmativ..."
#   remediation（china 2.4.28 · 原文）：
#     "Before emitting disease-count claims, reconcile evidence for
#      critical-illness coverage and its count across the entire product
#      record, rather than checking only mild-illness contradictions. Prefer
#      validated structured coverage fields; suppress the count and report it
#      as unverified when exclusions, conflicting counts, uncertainty, or
#      uninterpretable conditions remain. Add regression tests that plac..."
#
# 旧实现的缺陷：
#   记录级矛盾校验**只作用于轻症**（`_crx_record_contradiction(product, "轻症")`），
#   **病种数**（「120种重疾」）从未做过记录级校验 → 记录内自相矛盾的病种数
#   （highlights「120种重疾」vs key_benefits「100种重疾」）被原样对外宣称。
#
# 本轮修复（病种数专属闸门 · 记录级）：
#   ① 记录内出现 ≥2 个不同病种数 → 证据冲突 → 压制；
#   ② 病种数所在子句命中**除外 / 适用条件 / 不确定** → 压制；
#   ③ 泛化病种数子句（病种数 / 疾病种类 … 且同句提到重疾）命中条件 / 不确定 → 压制；
#   ④ 记录级矛盾陈述（复用既有 `_crx_record_contradiction`）→ 压制。
#   → 命中即返回空串 → 自动落回既有 `_crx_key_benefits` 降级路径
#     「重疾保障，确诊即赔付N万」（**不另造文案口径**）。
#
# ⚠ 关键坑（**不可**复用既有 `_crx_clause_excludes_subject` 去判「120种重疾」）：
#   尾随除外标记的**作用对象**可能不是病种数 —— 「120种重疾不含轻症」里的
#   「不含」指向的是**轻症**，不是「120种重疾」这个病种数；既有判定对
#   「轻症」与「轻症疾病」的处理还不一致（取决于宾语里是否碰巧出现
#   「疾病」「给付」等 cue）→ 误判。
#   → 必须做**病种数专属**判定：除外标记**后紧跟的宾语**若是别的保障对象
#     （轻症 / 中症 / 住院津贴 …）→ 该除外与病种数无关 → 不算命中；
#     head 侧的除外（「不保120种重疾」）仍应命中。
# ══════════════════════════════════════════════════════════════════════

# 病种数（重疾病种数量）识别 —— module 级常量
_CRX_DISEASE_COUNT_RE = re.compile(r"(\d+)\s*种重疾")
# 泛化病种数表述（含这些词 → 该子句谈的是「病种数」而非具体数字）
_CRX_GENERIC_COUNT_TOKENS = (
    "病种数", "病种数量", "疾病数量", "疾病种类", "重疾种类", "重疾病种", "保障病种",
)
# 病种数**专属**的「其它保障对象」线索表：
#   = 既有 `_CRX_OTHER_OBJECT_CUES` **剔除**「重疾 / 疾病 / 给付」
#     （病种数自身的给付对象不能算「别的保障对象」）
#     **并入**「轻症 / 中症」（轻症责任的除外标记宾语 —— 常见误判源）
_CRX_COUNT_OTHER_OBJECT_CUES = (
    "住院津贴", "津贴", "身故", "死亡", "全残", "伤残", "豁免", "等待期",
    "犹豫期", "护理", "年金", "现金价值", "满期", "返还", "增值", "保费",
    "免赔额", "免赔", "投保", "地区", "城市", "医院", "门诊", "职业",
    "分红", "万能", "账户", "储蓄", "意外", "续保", "住院", "医疗",
    "费用", "手术", "药品", "特药", "交通", "救护", "康复", "母婴",
    "生育", "体检", "牙齿", "寿险", "定寿",
    "轻症", "中症", "少儿特定疾病",
)
# 宾语窗口长度（与既有肯定线索窗口 `_crx_clause_affirms_subject` 同口径：12 字）
_CRX_COUNT_OBJECT_WINDOW = 12


def _crx_record_disease_counts(product):
    """产品记录内出现的**全部**数字病种数 → set[str]

    官方 remediation（ai 2.4.28 · 原文）：
      「Validate disease-count coverage across the entire product record before
        generating claims …」
    官方 remediation（china 2.4.28 · 原文）：
      「…reconcile evidence for critical-illness coverage and its count across
        the entire product record …」
    """
    out = set()
    if not product:
        return out
    for text in _product_text_leaves(product):
        if not isinstance(text, str):
            continue
        for m in _CRX_DISEASE_COUNT_RE.finditer(text):
            out.add(m.group(1))
    return out


def _crx_count_object_is_other(segment):
    """segment（除外标记的宾语窗口）是否指向**别的保障对象**"""
    if not segment:
        return False
    for cue in _CRX_COUNT_OTHER_OBJECT_CUES:
        if cue in segment:
            return True
    return False


def _crx_clause_excludes_disease_count(clause, subject):
    """clause 内是否存在**指向病种数本身**的明确除外表述（病种数专属判定）

    ⚠ 与 `_crx_clause_excludes_subject` 的差别：**病种数专属**。
      除外标记**后紧跟的宾语**若指向**别的保障对象**（轻症 / 中症 / 住院津贴 …）
      → 该除外与病种数**无关** → 不算命中：
        「120种重疾不含轻症」 → 「不含」指向轻症 → 病种数仍成立（**不命中**）
        「不保120种重疾」     → head 侧直接指向病种数 → **命中**
        「120种重疾除外」     → tail 侧直接指向病种数 → **命中**
      （复用既有判定会把「轻症除外」误当成「病种数除外」→ 过度收紧。）
    """
    if not clause or not subject:
        return False
    for occ in _crx_occurrences(clause, subject):
        head = clause[:occ]
        tail = clause[occ + len(subject):]

        # ── head 侧：否定**前向**绑定（标记 → 病种数）──
        for mk in _CRX_EXCLUSION_MARKERS:
            pos = head.rfind(mk)
            while pos != -1:
                if mk in _CRX_BACKWARD_BINDING_MARKERS:
                    # ⚠ 官方 SDI-4 残余 U：后向绑定标记（除外 / 责任免除 …）
                    #   绑定的是标记**之前**的主体 → 只看「标记之前」的片段；
                    #   命中**别的保障对象** → 与病种数无关（跳过）；
                    #   否则 → 保守判除外（后续从句不得撤销）。
                    if not _crx_count_object_is_other(head[:pos]):
                        return True
                    pos = head.rfind(mk, 0, pos)
                    continue
                gap = head[pos + len(mk):]
                if not _crx_count_object_is_other(gap):
                    return True
                pos = head.rfind(mk, 0, pos)
        # 弱标记「无」必须**紧邻**病种数
        if head.rstrip().endswith(_CRX_EXCLUSION_WEAK_MARKERS):
            return True

        # ── tail 侧：否定**后向**绑定（病种数 → 标记 → 宾语）──
        #    宾语在标记**之后**（「不含轻症」→ 宾语是轻症 → 与病种数无关）
        hits = []
        for mk in _CRX_EXCLUSION_MARKERS:
            start = 0
            while True:
                pos = tail.find(mk, start)
                if pos == -1:
                    break
                hits.append((pos, pos + len(mk), mk))
                start = pos + len(mk)
        hits.sort()
        for _s, e, mk in hits:
            if mk in _CRX_BACKWARD_BINDING_MARKERS:
                # ⚠ 官方 SDI-4 残余 U（remediation 原文）：
                #   "postposed markers such as 「除外」 and 「责任免除」 must
                #    remain attached to the preceding disease-count subject,
                #    regardless of a subsequent benefit clause."
                #   → 后向绑定标记 → 绑定**前面**的病种数主体；
                #     其后的「但含身故保障」属**后续子句** → **不得**撤销
                #     （**不再**用「标记之后」的窗口撤销已绑定的除外）；
                #     只看标记**之前**的片段（绑定的是别的保障对象 → 跳过）。
                if _crx_count_object_is_other(tail[:_s]):
                    continue
                return True
            after = tail[e:e + _CRX_COUNT_OBJECT_WINDOW]
            # 除外标记指向**别的保障对象** → 与病种数无关（不压制）
            if _crx_count_object_is_other(after):
                continue
            return True
        # 弱标记「无」：仅在紧邻病种数且搭配属除外语义时成立
        if tail == "无" or any(tail.startswith(f) for f in _CRX_WEAK_TAIL_FORMS):
            return True
    return False


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 Q（2026-11-22 线上复扫 · v2.4.29/2.4.30 · Excessive Agency · MEDIUM）
#
#   finding（ai v2.4.29 · L2368-2391 · 原文）：
#     "The documented record-wide disease-count safeguard misses exclusions of
#      critical-illness coverage when they do not repeat the numeric count."
#   finding（china v2.4.29/2.4.30 · L2364-2387 · 原文）：
#     "Disease-count claims bypass record-wide exclusions that omit the numeric count."
#   remediation（china v2.4.29/2.4.30 · 原文）：
#     "Validate critical-illness coverage and disease count separately across the entire
#      product record, binding exclusions to the underlying coverage category even when
#      no number is present. Suppress unsupported claims and explicitly report unresolved
#      evidence as unverified; ensure fallback benefit text does not continue asserting
#      excluded coverage. Add end-to-end regression tests combining affirmative counted
#      highlights with nonnumeric exclusions in other fields and verify the final plan output."
#
# 根因（主侧已坐实）：
#   记录级病种数闸 `_crx_record_disease_count_issue` 只扫两类子句 ——
#     ① 匹配 `_CRX_DISEASE_COUNT_RE`（「N种重疾」）的子句；
#     ② 含泛化病种数 token（病种数 / 疾病种类 …）且提到「重疾」的子句。
#   ⇒ 「重疾疾病不保」「重大疾病责任免除」这类**不含量化数字**的
#     **类别级**重疾除外子句**整段被跳过** → 记录级闸完全看不到 →
#     病种数宣称照样对外输出。
#
# 修法：新增**类别级**（无数字）重疾除外判定 → 绑定到病种数宣称 → 压制；
#   并按官方 remediation 让兜底文案**不得继续断言被除外的保障**。
#
# ⚠ 防过度收紧（真实语料 8 条红线 · 主侧已定位）：
#   · 恒大人寿重疾保险**续保不保证**，保费随年龄增加   → 不保证的是「续保」
#   · 国华人寿重大疾病保险**续保不保证**，…            → 同上
#   · 「健康福·百万重疾(保1年)」**不保证续保**           → 同上
#   · 康福重疾险**可能不保证续保**                      → 同上
#   · 若未达到重疾标准**身故则不赔付**                  → 不赔付的是「身故责任」
#   · 等待期为90天，未满期内**轻重疾病不赔付**          → 是「等待期内」不赔付
#   · 安心保险…**不需要体检**，仅需健康告知             → 根本不是除外
#   · 「重疾疾病不保」/「重大疾病责任免除」             → **确实是**类别除外
# ⇒ 判定必须**紧贴**类别名词（只允许极短填充词），且排除其它对象线索
#   （身故 / 续保 / 保费 / 等待期 / 犹豫期 / 体检 / 标准 / 轻症 …）与条件性语境。
# ══════════════════════════════════════════════════════════════════════

# 类别级重疾除外：coverage category 名词
_CRX_CI_CATEGORY_TOKENS = ("重大疾病", "重疾")
# 类别级除外标记（**紧贴**类别名词才生效）
# ⚠⚠ 官方 SDI-4 残余 AE-4（2026-11-27 公开复扫 · china v2.4.45 · Excessive
#   Agency · MEDIUM · confidence 0.99）finding 原文：
#     「The shared critical-illness state labels coverage as validated despite
#       explicit category exclusions that its checks deliberately omit.」
#   explanation 原文：
#     「The category-level exclusion checks deliberately omit expressions such as
#       「不覆盖」 and 「不涵盖」, yet the shared state treats the absence of
#       recognized exclusions as validated coverage.」
#   remediation 原文：
#     「… using subject-specific scope to distinguish exclusions of critical-illness
#       coverage from exclusions of particular causes or benefits.」
#
# ⚠ 这三个标记**不得**直接当类别级除外（真实语料反例）：
#     「平安少儿鑫福星2025重疾险**不覆盖核爆炸**、核辐射或遗传性疾病」
#     → 是**特定病因**的除外 → 直接进类别级路径会**误压制**该产品的真实宣称。
#   ⇒ 走**主体作用域**判别：被排除的对象**就是重疾保障本身**才算类别级除外
#     （`_crx_ci_subject_scope_ok`）。
# ⚠ **引用**共享词表（`_EXCL_CATEGORY_EXTRA_LITERALS` = 不纳入 / 不涵盖 / 不覆盖）
#   —— **不另抄一份**（单一事实源 · 杜绝二次漂移）。
_CRX_CI_SUBJECT_SCOPE_MARKERS = (
    *_EXCL_CATEGORY_EXTRA_LITERALS,
)


_CRX_CI_EXCLUSION_MARKERS = (
    # ⚠⚠ 官方 SDI-4 残余 AD（2026-11-26 公开复扫 · ai v2.4.46 /
    #   china v2.4.43 · Excessive Agency · MEDIUM）：
    #   本路径**从未**消费共享归一化词表的**范围族**
    #   （`_SHARED_EXCLUSION_SCOPE` =「不在承保范围」「不属于承保范围」）
    #   → 官方场景（highlights「120种重疾，含轻症保障」+ **另一字段**
    #   「重大疾病不在承保范围」）→ `_crx_ci_claim_state` 算出 allowed=True
    #   → 产出肯定宣称（把**明确除外**反转成**承保宣称**）。
    #   官方 china explanation 原文另点名：「they also do not use the shared
    #   exclusion regexes」→ 本路径还须消费**同一份** `_EXCL_PATTERNS`
    #   （见 `_crx_ci_marker_positions`）。
    # ⇒ 改为**从共享语义族派生**（**单一事实源**）—— **只引用、不另抄一份**：
    #   ① 范围级语义族（**含**共享 scope 家族 · 官方残余 AD 的核心修复点）
    *_EXCL_SCOPE_LITERALS,
    #   ② 主体级语义族（不予承保 + 不承保）
    *_SHARED_EXCLUSION_SUBJECT,
    *_EXCL_SUBJECT_EXTRA_LITERALS,
    #   ③ 不予给付级语义族（不予给付 / 不予赔付 / 不予支付 / 不予报销 …）
    *_EXCL_NONPAYMENT_LITERALS,
    #   ④ 类别级语义族（官方残余 AB：「不含」「不包含」「不包括」→
    #      「不含重大疾病保障」/「重大疾病保障不含」/「重疾不含保障」
    #      **都**判类别级除外 ✓（官方原文：
    #      「recognize 「不含」「不包含」「不包括」 … with appropriate local scope」）。
    #      ⚠ **只取共享族**（不含 / 不包含 / 不包括）——「不纳入 / 不涵盖 / 不覆盖」
    #        属**主体路径**口径（残余 AB 之前就有），**不**引入本路径：
    #        真实语料「XX重疾险不覆盖核爆炸」「保险不涵盖因酗酒导致的疾病」
    #        属**其它对象**的限定，引入本路径会**过度收紧**（误压制真实宣称）。
    #   ⚠ 既有「不保证 ≠ 不保」特判（`_crx_ci_marker_positions` 里 `不保` + `证`
    #     的 continue）**保留不变**；既有成员**一律保留**（只增不改）。
    *_SHARED_EXCLUSION_CATEGORY,
    #   ⑤ 主体作用域标记（官方残余 AE-4：不纳入 / 不涵盖 / 不覆盖）→
    #      **必须**通过**主体作用域判别**（`_crx_ci_subject_scope_ok`）才生效：
    #      被排除的对象**就是重疾保障本身**才算类别级除外；
    #      「不覆盖核爆炸」（特定病因）**不是**类别级除外。
    *_CRX_CI_SUBJECT_SCOPE_MARKERS,
    # ── 路径**特有**成员（既有口径 · 只增不改）──
    "不在保障责任范围", "不承担", "不负责", "不保", "不赔",
    "责任免除", "除外", "无保障",
)

# 类别级除外判定必须排除的「其它保障对象 / 条件性」线索
_CRX_CI_OTHER_OBJECT_CUES = (
    "身故", "死亡", "全残", "伤残", "豁免", "津贴", "等待期", "犹豫期",
    "保费", "续保", "体检", "标准", "轻症", "中症", "住院", "医疗", "护理",
    "年金", "返还", "投保", "职业", "地区", "现金价值", "分红", "门诊",
    "意外", "定期", "终身",
)
# 条件性语境（该子句的除外是**有条件的** → 不是无条件类别除外）
_CRX_CI_CONDITIONAL_CUES = (
    "等待期", "犹豫期", "未满", "未达到", "达到标准", "符合标准",
    "若", "如果",
)
# 类别名词与除外标记之间允许的**填充词**长度上限（紧贴）
_CRX_CI_BRIDGE_MAX = 4
# 除外标记之后的宾语窗口长度（与既有肯定线索窗口同口径：12 字）
_CRX_CI_OBJECT_WINDOW = 12


def _crx_ci_marker_positions(segment):
    """segment 内「类别级除外标记」的位置 → [(start, end, marker)]（已剔除「不保证」）

    ⚠ 官方 SDI-4 残余 AD：类别级路径**必须消费同一份** `_EXCL_PATTERNS`
      （官方 china explanation 原文：「they also do not use the shared
      exclusion regexes」）→ 模式命中按**等价字面标记**参与判定
      （① ≡「不在保障范围」后向绑定 / ② ≡「不予给付」后向绑定 / ③ ≡「不含」前向绑定）。
    ⚠ 模式命中**只补充**不被字面标记覆盖的跨度 → 既有口径**零漂移**。
    ⚠ 既有「不保证 ≠ 不保」特判**保留不变**。
    """
    hits = []
    for mk in _CRX_CI_EXCLUSION_MARKERS:
        pos = 0
        while True:
            i = segment.find(mk, pos)
            if i == -1:
                break
            pos = i + len(mk)
            # 「不保证」（续保不保证）不是除外标记 —— 保证 ≠ 承保
            if mk == "不保" and segment[i + len(mk):i + len(mk) + 1] == "证":
                continue
            hits.append((i, i + len(mk), mk))
    hits.sort()
    _lit_spans = [(_s, _e) for (_s, _e, _m) in hits]
    for (_s, _e, _mk) in _crx_pattern_marker_hits(segment, _lit_spans,
                                                 _CRX_CI_PATTERN_INDICES):
        hits.append((_s, _e, _mk))
    hits.sort()
    return hits


def _crx_ci_segment_has_other_object(segment):
    """segment 是否出现「其它保障对象 / 条件性」线索（→ 该除外与重疾类别无关）"""
    if not segment:
        return False
    for cue in _CRX_CI_OTHER_OBJECT_CUES:
        if cue in segment:
            return True
    return False


def _crx_ci_object_is_ci_subject(obj):
    """被排除的宾语是否**就是重疾保障主体**（含「重疾 / 重大疾病」类别词）

    ⚠ 官方 SDI-4 残余 AE-4 remediation 原文（主体作用域）：
      「… using subject-specific scope to distinguish exclusions of critical-illness
        coverage from exclusions of particular causes or benefits.」

    ⇒ **正向**要求宾语含重疾类别词 → 「不涵盖重大疾病保障」✓ 类别级除外；
      「不覆盖核爆炸」✗（宾语是**别的病因** → 不是类别级除外）。
    """
    if not obj or not isinstance(obj, str):
        return False
    return any(cat in obj for cat in _CRX_CI_CATEGORY_TOKENS)


def _crx_ci_subject_scope_ok(marker, obj, tail_subject):
    """该类别级除外命中的**主体作用域**是否成立（官方残余 AE-4）

    · 仅对**主体作用域标记**（不纳入 / 不涵盖 / 不覆盖）生效；
      其余标记（不含 / 不包含 / 不包括 / 范围族 / 主体级 …）**既有口径零漂移**。
    · `tail_subject=True`  → 类别名词在标记**之前** → 被排除的主体**就是**该
      类别名词本身；但若标记之后紧跟**别的**（非重疾类）对象 → 除外只针对那个
      对象（如「重疾不覆盖核爆炸」）→ **不是**类别级除外。
    · `tail_subject=False` → 标记在类别名词**之前** → 被排除的对象 = 标记之后的
      宾语 → 必须**就是**重疾保障主体（如「不涵盖重大疾病保障」）才算类别级除外。
    """
    if marker not in _CRX_CI_SUBJECT_SCOPE_MARKERS:
        return True
    if tail_subject:
        return (not obj) or _crx_ci_object_is_ci_subject(obj)
    return _crx_ci_object_is_ci_subject(obj)


def _crx_ci_local_object(text):
    """标记**之后**的宾语片段（**只取标记所在子句内的部分**）

    ⚠ 官方 SDI-4 残余 X（2026-11-24 公开复扫 · china v2.4.37 · Excessive Agency ·
      MEDIUM · confidence 0.99）remediation 原文：
        「Bind exclusions to their coverage subjects using local grammatical scope,
          splitting subsequent clauses at connectors such as 「但」 before evaluating
          other objects. Once 「重疾不保」 is bound, do not let a later benefit reverse
          that exclusion.」
      explanation（原文）：
        「The category-level exclusion check can discard an exclusion when its
          following text mentions another benefit: for example, 「重疾不保但含身故保障」
          is skipped because the object window contains 「身故」.」

    ⇒ **判定「别的保障对象」之前，先在连接词处切掉后续子句**：
      · 「重疾不保但含身故保障」→ 标记所在子句 = 「不保」→ 后续子句
        「但含身故保障」在连接词「但」处被切掉 → 子句内**无**别的保障对象
        → 除外**绑定**到「重疾」→ 成立（官方口径：已绑定的除外不得被后续
          保障撤销）；
      · 「重疾不保轻症」→ 子句 = 「不保轻症」（无连接词）→ 命中「轻症」
        → 与重疾类别无关 → 不成立（既有口径**保持**）。
    """
    if not text:
        return ""
    out = []
    for i, ch in enumerate(text[:_CRX_CI_OBJECT_WINDOW]):
        if ch in _CRX_SCOPE_BREAK_CHARS:
            break
        # ⚠ 连接词 / 保障动词处 → 后续子句开始 → **切掉**（官方残余 X）
        if _crx_scope_starts_with_connector(text[i:]):
            break
        out.append(ch)
    return "".join(out)


def _crx_clause_ci_category_hits(clause):
    """clause 内的**类别级**（不含数字）重疾除外命中 → [(abs_start, abs_end, marker)]

    ⚠ 判定逻辑与既有 `_crx_clause_excludes_ci_category` **逐条一致**
      （只把 `return True` 改成「记录命中」）→ 判定口径**零漂移**。
    ⚠ 官方 SDI-4 残余 AD：命中集合里同时包含
      · **字面标记**命中（`_CRX_CI_EXCLUSION_MARKERS`）
      · **通用模式**命中（`_EXCL_PATTERNS` · 同一份）
    """
    hits = []
    if not clause:
        return hits
    # ⚠ 带**量化数字**的子句由「病种数专属」判定处理（`_crx_clause_excludes_disease_count`）
    #   → 类别级判定只负责**不含量化数字**的重疾除外（官方 remediation 原文：
    #     「binding exclusions to the underlying coverage category even when no
    #       number is present」）
    #   → 否则「120种重疾除外」会被误当成**类别**除外 → 兜底文案被过度收紧。
    if _CRX_DISEASE_COUNT_RE.search(clause):
        return hits
    for cue in _CRX_CI_CONDITIONAL_CUES:
        if cue in clause:
            return hits
    for cat in _CRX_CI_CATEGORY_TOKENS:
        start = 0
        while True:
            i = clause.find(cat, start)
            if i == -1:
                break
            start = i + len(cat)
            # 「轻重疾病」中的「重疾」是并称，不是类别名词
            if cat == "重疾" and i > 0 and clause[i - 1] == "轻":
                continue
            # ── tail 侧：类别名词 → 除外标记 ──
            tail = clause[i + len(cat):]
            for (s, e, mk) in _crx_ci_marker_positions(tail):
                bridge = tail[:s]
                if len(bridge) > _CRX_CI_BRIDGE_MAX:
                    continue
                if _crx_ci_segment_has_other_object(bridge):
                    continue
                if mk in _CRX_BACKWARD_BINDING_MARKERS:
                    # ⚠ 官方 SDI-4 残余 U：后向绑定标记（除外 / 责任免除 …）
                    #   → 绑定**前面**的类别名词；其后的「但含身故保障」属
                    #     **后续子句** → **不得**撤销 → 不查标记之后的宾语窗口
                    hits.append((i + len(cat) + s, i + len(cat) + e, mk))
                    continue
                obj = _crx_ci_local_object(tail[e:])
                if _crx_ci_segment_has_other_object(obj):
                    continue
                # ⚠ 官方 SDI-4 残余 AE-4：**主体作用域**判别（仅对
                #   「不纳入 / 不涵盖 / 不覆盖」生效 · 既有口径零漂移）
                if not _crx_ci_subject_scope_ok(mk, obj, tail_subject=True):
                    continue
                hits.append((i + len(cat) + s, i + len(cat) + e, mk))
            # ── head 侧：除外标记 → 类别名词 ──
            head = clause[:i]
            for (s, e, mk) in _crx_ci_marker_positions(head):
                bridge = head[e:]
                if len(bridge) > _CRX_CI_BRIDGE_MAX:
                    continue
                if _crx_ci_segment_has_other_object(bridge):
                    continue
                if mk in _CRX_BACKWARD_BINDING_MARKERS:
                    # 后向绑定标记出现在类别名词**之前** → 它绑定的是**更前面**
                    #   的对象；前置片段命中别的保障对象 → 与类别无关（跳过）
                    if _crx_ci_segment_has_other_object(head[:s]):
                        continue
                    hits.append((s, e, mk))
                    continue
                obj = _crx_ci_local_object(clause[e:])
                if _crx_ci_segment_has_other_object(obj):
                    continue
                # ⚠ 官方 SDI-4 残余 AE-4：**主体作用域**判别（见上）
                if not _crx_ci_subject_scope_ok(mk, obj, tail_subject=False):
                    continue
                hits.append((s, e, mk))
    return hits


def _crx_clause_ci_category_unresolved(clause):
    """类别级重疾除外命中**存疑**（ambiguous）→ True

    ⚠ 官方 SDI-4 残余 AD · 已知坑（任务书 §⑤·2）：存疑表述**不得**被当成
      「确定不保」→ 但**仍然压制**肯定宣称（官方口径：存疑一律不授权 +
      产出「待核实」限制说明）。
    """
    for (s, _e, _mk) in _crx_clause_ci_category_hits(clause):
        if _crx_excl_hit_is_ambiguous(clause, s):
            return True
    return False


def _crx_clause_excludes_ci_category(clause):
    """clause 内是否存在**类别级**（不含数字）重疾**确定**除外 → True

    官方 remediation（残余 Q · 原文）：
      「binding exclusions to the underlying coverage category even when no
        number is present」

    口径（防过度收紧）：
      · 除外标记必须**紧贴**类别名词（填充词 ≤ 4 字）；
      · 类别名词与标记之间 / 标记之后若出现**其它保障对象**线索
        （身故 / 续保 / 保费 / 等待期 / 津贴 / 轻症 …）→ 与重疾类别无关；
      · ⚠ 官方 SDI-4 残余 X：判定「别的保障对象」**之前**先在**连接词**处
        切掉后续子句（`_crx_ci_local_object`）→ 「重疾不保但含身故保障」
        的除外**绑定**到「重疾」（后续保障不得撤销已绑定的除外）；
      · 子句带**条件性语境**（等待期 / 犹豫期 / 未满 / 若 …）→ 不是无条件类别除外；
      · 「轻重疾病」= 轻症 + 重疾的**并称** → 其中的「重疾」不是类别名词。
    """
    for (s, _e, _mk) in _crx_clause_ci_category_hits(clause):
        # ⚠ 存疑（对冲词前置）→ **不算**「确定除外」（官方口径：存疑一律不授权
        #   + 产出「待核实」限制说明 → 由 `_crx_record_ci_category_state` 承接）
        if not _crx_excl_hit_is_ambiguous(clause, s):
            return True
    return False


def _crx_record_ci_category_state(product):
    """产品记录内**类别级**（不含数字）重疾除外的**记录级状态**

    → {"excluded": bool, "unresolved": bool}

      ① excluded   —— 存在**确定**的类别级重疾除外（如「重大疾病不在承保范围」）
      ② unresolved —— 存在**存疑**的类别级除外（对冲词前置，如
                      「重大疾病可能不在承保范围」）→ 官方口径：未经确认
                      （unverified）→ **不得**授权肯定宣称。

    官方 remediation（残余 AD · 原文）：
      「Treat unresolved exclusions or conflicting evidence as unverified,
        suppress affirmative claims on every output surface, and propagate an
        explicit limitation into the final plan.」

    官方 remediation（残余 Q · 原文）：
      「Validate critical-illness coverage and disease count separately across the
        entire product record, binding exclusions to the underlying coverage category
        even when no number is present.」
    """
    excluded = False
    unresolved = False
    if not product:
        return {"excluded": False, "unresolved": False}
    for text in _product_text_leaves(product):
        if not isinstance(text, str):
            continue
        if "重疾" not in text and "重大疾病" not in text:
            continue
        for clause in _split_clauses(text):
            if _crx_clause_excludes_ci_category(clause):
                excluded = True
            elif _crx_clause_ci_category_unresolved(clause):
                unresolved = True
    return {"excluded": excluded, "unresolved": unresolved}


def _crx_record_ci_category_excluded(product):
    """产品记录内是否存在**类别级**（不含数字）重疾**确定**除外 → True

    官方 remediation（残余 Q · 原文）：
      「Validate critical-illness coverage and disease count separately across the
        entire product record, binding exclusions to the underlying coverage category
        even when no number is present.」
    """
    return bool(_crx_record_ci_category_state(product)["excluded"])


def _crx_record_disease_count_issue(product, subject):
    """产品记录内**病种数**是否「未经确认」→ 问题码（空串 = 无问题）

    官方 remediation（ai 2.4.28 · 原文）：
      「…suppress the count and report it as unverified when exclusions,
        uncertainty, or conflicting evidence remain unresolved.」
    官方 remediation（china 2.4.28 · 原文）：
      「…suppress the count and report it as unverified when exclusions,
        conflicting counts, uncertainty, or uninterpretable conditions remain.」

    问题码：
      conflicting-count  记录内出现 ≥2 个不同病种数（证据冲突）
      excluded           病种数所在子句命中除外
      conditional        病种数所在子句命中适用条件
      uncertain          病种数所在子句命中不确定表述
      contradiction      记录级矛盾陈述（复用既有 `_crx_record_contradiction`）
    """
    if not product:
        return ""
    # ① 记录内病种数互相冲突 → 证据冲突（记录级）
    if len(_crx_record_disease_counts(product)) > 1:
        return "conflicting-count"
    # ② 子句级（遵循残余 K 的「不确定表述必须与相关对象同子句才算数」原则）
    for text in _product_text_leaves(product):
        if not isinstance(text, str):
            continue
        for clause in _split_clauses(text):
            m = _CRX_DISEASE_COUNT_RE.search(clause)
            if m:
                # 数字病种数子句 → 除外 / 条件 / 不确定
                if _crx_clause_excludes_disease_count(clause, m.group(0)):
                    return "excluded"
                if _has_condition(clause, 0, len(clause)):
                    return "conditional"
                if _has_uncertainty(clause, 0, len(clause)):
                    return "uncertain"
                continue
            # 泛化病种数子句（无具体数值 → 只查条件 / 不确定）
            if not any(tok in clause for tok in _CRX_GENERIC_COUNT_TOKENS):
                continue
            if "重疾" not in clause:
                continue
            if _has_condition(clause, 0, len(clause)):
                return "conditional"
            if _has_uncertainty(clause, 0, len(clause)):
                return "uncertain"
    # ③ 记录级矛盾陈述（肯定承保 + 除外并存）
    subj = re.sub(r"\s+", "", subject or "")
    if subj and _crx_record_contradiction(product, subj):
        return "contradiction"
    # ④ 官方 SDI-4 残余 Q：**类别级**（不含数字）重疾除外 → 绑定到病种数宣称
    #   「重疾疾病不保」/「重大疾病责任免除」这类子句不带数字 → ② 的子句级扫描
    #   完全看不到 → 必须由**记录级**类别判定兜住（官方 remediation：
    #   「binding exclusions to the underlying coverage category even when no
    #     number is present」）
    if _crx_record_ci_category_excluded(product):
        return "category-excluded"
    return ""


def _crx_subject_unconfirmed(text, subject):
    """subject（轻症 / 「N种重疾」）在 text 中是否**未经确认**

    口径（**子句级**）：subject 出现所在的子句内出现
          ① 明确除外（不含 / 不包含 / 除外 / 不保 / 不赔 …），或
          ② 适用条件（仅限指定医院 / 需转诊 / 目录内 …），或
          ③ 不确定表述（是否 / 待核实 / 以…为准 …）
          → 该项**未经确认** → 不得产出肯定宣称。

    ⚠ 官方 SDI-4 残余 N（2026-11-21 线上复扫 · v2.4.26 · Excessive Agency）：
      finding:「The critical-illness benefit generator can turn an explicit
        mild-illness exclusion into an affirmative coverage claim.」
      explanation（china）:「…highlights such as 「120种重疾，不保轻症」 pass because
        _crx_subject_unconfirmed does not recognize 「不保」 **before** the subject,
        causing _crx_disease_claim to output 「120种重疾+轻症保障」.」
      explanation（ai）:「…the exclusion guard recognizes only selected negation phrases
        and word orders: for example, highlights containing 「120种重疾，不承保轻症」 pass
        because 「不承保」 is checked after the subject but not before it.」
      remediation:「…handle exclusions before and after the subject consistently rather
        than relying on a small prefix list, and reconcile contradictory evidence
        throughout the product record.」

      → **head（subject 之前）与 tail（subject 之后）必须共用同一套除外标记集合**
        （词序双向），且标记与 subject 之间允许填充词；post-subject 除外同样压制。
    """
    if not text or not subject:
        return False
    for clause in _split_clauses(text):
        if subject not in clause:
            continue
        if _crx_clause_excludes_subject(clause, subject):
            return True
        if _has_condition(clause, 0, len(clause)):
            return True
        if _has_uncertainty(clause, 0, len(clause)):
            return True
    return False


def _crx_disease_claim(product):
    """重疾病种/轻症宣称：只认 highlights 字符串（须含「轻症」且能提取到「N种重疾」）。

    ⚠️ key_benefits 是 list → 元素级 "轻症" in list 恒 False → 不可作事实源。

    ⚠️ 官方 SDI-4 残余 N（2026-11-21 线上复扫 · v2.4.26 · Excessive Agency）：轻症 /
       病种数被**明确除外**（含 subject **之前**的除外 —— 词序双向）、带
       **条件 / 不确定**表述、或产品记录内**存在矛盾陈述**时，
       **不得**产出「N种重疾+轻症保障」。
    """
    if not product:
        return ""
    hl = product.get("highlights")
    if not isinstance(hl, str) or "轻症" not in hl:
        return ""
    m = re.search(r"(\d+)\s*种重疾", hl)
    if not m:
        return ""
    if _crx_subject_unconfirmed(hl, "轻症"):
        return ""
    if _crx_subject_unconfirmed(hl, m.group(0)):
        return ""
    # 官方 remediation：reconcile contradictory evidence throughout the product record
    if _crx_record_contradiction(product, "轻症"):
        return ""
    # ⚠ 官方 SDI-4 残余 S-2：记录级轻症覆盖状态（**其它字段**里的除外 / 待核实 /
    #   条件性表述）→ 不得只认 highlights 内的表述 → 轻症宣称必须压制。
    if _crx_record_mild_state(product)["unverified"]:
        return ""
    # 官方 SDI-4 残余 O：病种数**记录级**闸门
    #   （冲突病种数 / 病种数除外 / 病种数条件 / 病种数不确定 / 记录级矛盾）
    #   → 命中即返回空串 → 自动落回 `_crx_key_benefits` 降级路径
    #     「重疾保障，确诊即赔付N万」（不另造文案口径）
    if _crx_record_disease_count_issue(product, m.group(0)):
        return ""
    return f"{m.group(1)}种重疾+轻症保障"


def _crx_key_benefits(product, coverage, style="standard"):
    """按产品真实字段派生重疾险对外卖点文案。

    style="standard" → 「{病种轻症}，确诊即赔付{n}万」（无轻症来源时降级为「重疾保障，确诊即赔付{n}万」）
    style="premium"  → 「{重疾多次赔付?}{，终身保障?}，保额{n}万」（两项均无授权时 → 「重疾保障，保额{n}万」）

    ⚠ 官方 SDI-4 残余 Q（remediation 原文）：
      「ensure fallback benefit text does not continue asserting excluded coverage」
      → 记录级**类别级重疾除外**（如「重疾疾病不保」）时，兜底文案
        「重疾保障，确诊即赔付{n}万」**本身就在断言被除外的保障**
        → standard 样式一律返回**空串**（**不宣称**；与医疗险
        `_medical_treatment_suffix` 无授权即空串同口径，不另造文案）。
      → 解除限制由调用方在方案层如实报告（见 `_crx_ci_category_limitation`）。
    """
    coverage = int(coverage or 0)
    amount = coverage // 10000
    multi = _crx_is_multi(product)
    lifetime = _crx_is_lifetime(product)

    # ⚠ 官方 SDI-4 残余 R（finding L2779-2795 · 原文）：
    #   「Critical-illness exclusion suppression is bypassed by premium benefits
    #     and plan features.」
    #   ⇒ 共享的「重疾保障已验证状态」必须在**任何** benefits 生成**之前**算出，
    #     standard / premium 两个分支受**同一状态**约束。
    state = _crx_ci_claim_state(product)
    if not state["allowed"]:
        # 解除限制由调用方在方案层如实报告（见 `_crx_ci_category_limitation`）
        return ""

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


def _crx_ci_category_unverified_limitation(product, no_evidence=False):
    """类别级重疾除外**存疑**（未决）时的**如实限制说明** → dict | None

    ⚠ 官方 SDI-4 残余 AD（2026-11-26 公开复扫）remediation 原文：
      「Treat unresolved exclusions or conflicting evidence as unverified,
        suppress affirmative claims on every output surface, and propagate an
        explicit limitation into the final plan.」
    ⚠ 文案**不得**断言「确定不保」（那是把**不确定性**说成**确定性**）；
      也不得断言保障成立 → 只如实报告「记录中存在待核实的表述」。

    ⚠ 官方 SDI-4 残余 AE-2（2026-11-27 公开复扫）新增 `no_evidence=True`：
      记录里**缺少**肯定的重疾承保证据时，同样必须**如实报告限制**
      （**不得**静默留空）→ **复用同一套**限制文案体系（**不新造体系**）。
    """
    if not product:
        return None
    if no_evidence:
        basis = "产品记录中缺少对重疾保障范围的肯定证据"
    else:
        if not _crx_record_ci_category_state(product)["unresolved"]:
            return None
        basis = "产品记录中存在重疾保障范围待核实的表述"
    return {
        "type": "coverage_limit",
        "product_type": "重疾险",
        "product": product.get("name"),
        "requirement": "重疾保障责任",
        "reason": (basis + "，重疾保障范围待核实，"
                   "已不作对外宣称；保费在预算内仅说明预算可行，不代表保障范围已核实"),
    }


def _crx_ci_category_limitation(product):
    """类别级重疾除外时的**如实限制说明** → dict | None

    官方 SDI-4 残余 Q（remediation 原文）：
      「Suppress unsupported claims and explicitly report unresolved evidence as
        unverified」
      「ensure fallback benefit text does not continue asserting excluded coverage」

    → 兜底文案已置空（不宣称被除外保障）→ 必须在方案层**如实报告**该限制，
      不得静默留空。
    """
    if not product or not _crx_record_ci_category_excluded(product):
        return None
    return {
        "type": "coverage_limit",
        "product_type": "重疾险",
        "product": product.get("name"),
        "requirement": "重疾保障责任",
        "reason": ("产品记录中存在重疾类别级除外表述，重疾保障范围待核实，已不作对外宣称；"
                   "保费在预算内仅说明预算可行，不代表保障范围已核实"),
    }


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 S（2026-11-23 线上复扫 · v2.4.33 · Excessive Agency · MEDIUM）
#
#   finding（china v2.4.33 · L2950-2959 · 原文）：
#     "The shared critical-illness state omits the promised unverified limitation when
#      mild-illness coverage is excluded."
#   finding（ai v2.4.33 · L2825-2838 · 原文）：
#     "Record-wide mild-illness conditions and uncertainty can be discarded when generating
#      affirmative benefit claims."
#
#   explanation（china v2.4.33 · 原文）：
#     "When mild-illness coverage is excluded, `_crx_ci_claim_state` sets `unverified=True`
#      and `allowed=False`, but obtains its limitation exclusively from
#      `_crx_ci_category_limitation`, which returns nothing unless critical-illness coverage
#      itself has a category-level exclusion. Both plan builders likewise attach only
#      category-level limitations, leaving an unverified product's premium and coverage in
#      the plan without a corresponding explicit warning; this is particularly consequential
#      in insurance advice, where users may mistake a budget-feasible plan for verified
#      protection."
#   explanation（ai v2.4.33 · 原文）：
#     "Mild-illness conditions and uncertainty are checked in highlights, but the record-wide
#      checks only reconcile explicit mild-illness exclusions or contradictions, not
#      conditions and uncertainty elsewhere. For example, highlights stating
#      「120种重疾，含轻症保障」 alongside another field stating 「轻症保障待核实」 can still
#      produce 「120种重疾+轻症保障」. In an insurance-advice skill, this turns unresolved
#      coverage evidence into an affirmative customer-facing benefit claim, potentially
#      misleading purchase decisions."
#
#   remediation（china v2.4.33 · 原文）：
#     "Return an explicit limitation whenever the shared state is unverified, distinguishing
#      mild-illness exclusions from critical-illness category exclusions. Have both plan
#      builders or the finalizer propagate that shared limitation into the final JSON for
#      retained products, and clarify that budget feasibility does not establish coverage
#      validity. Add end-to-end tests for mild-illness-only exclusions in both standard and
#      comprehensive plans, checking that unsupported claims are suppressed and the explicit
#      warning remains present."
#   remediation（ai v2.4.33 · 原文）：
#     "Compute a shared, record-wide mild-illness coverage state before generating claims,
#      checking all relevant fields for exclusions, uncertainty, conditions, and conflicting
#      evidence. Prefer validated, treatment-specific structured coverage decisions; preserve
#      applicable conditions in output, or suppress the mild-illness claim and add an explicit
#      unverified limitation when they cannot be reliably interpreted. Add end-to-end tests
#      pairing affirmative highlights with conditional or uncertain mild-illness statements in
#      other fields, asserting that final JSON does not advertise unconditional mild-illness
#      coverage."
#
# 本轮修法（三处，缺一不可）：
#   ① 记录级「轻症覆盖状态」`_crx_record_mild_state`（**单一事实源**）：扫描
#      **全部文本叶子**（`_product_text_leaves`）的轻症相关子句，覆盖
#      除外 / 不确定 / 条件 / 矛盾 四类证据（官方 S-2 明确要求）。
#      → 修掉「其它字段的待核实/条件表述被丢弃 → 仍产出「120种重疾+轻症保障」」。
#   ② 共享状态 `_crx_ci_claim_state` 在 `unverified` 时**必须**返回非空 limitation，
#      且轻症除外与重疾**类别级**除外**可区分**（官方 S-1 明确要求 distinguishing）。
#   ③ 两个 plan builder 用**共享状态**的 limitation 传导进最终 JSON
#      （官方 S-1："propagate that shared limitation into the final JSON"）。
# ══════════════════════════════════════════════════════════════════════

# 轻症专属的「条件性」线索（记录级轻症覆盖状态专用）
#   ⚠ 通用 `_CONDITION_MARKERS` 只含「满足条件」等**紧邻**写法，
#     「轻症需满足特定条件方可赔付」这类**带填充词**的写法不命中 → 轻症专属线索表补齐。
#   ⚠ 语料实测（两库各 2588 款 products.json · 含「轻症」的子句共 2490 个）：
#     命中本正则的 **0** 个 → 对真实语料零影响，只针对扫描器的**对抗样本**生效。
_CRX_MILD_CONDITIONAL_RE = re.compile(
    r"(需|须|应|必须|符合|满足|达到|限于|限定|仅限|只限)[^，,。；;！!？?\n]{0,4}条件")


def _crx_record_mild_state(product):
    """记录级「轻症保障覆盖状态」→ dict（残余 S 的单一事实源）

    官方 SDI-4 残余 S-2（ai v2.4.33 · 原文）：
      "Compute a shared, record-wide mild-illness coverage state before generating claims,
       checking all relevant fields for exclusions, uncertainty, conditions, and conflicting
       evidence. Prefer validated, treatment-specific structured coverage decisions; preserve
       applicable conditions in output, or suppress the mild-illness claim and add an explicit
       unverified limitation when they cannot be reliably interpreted."

    口径（扫描**全部文本叶子** `_product_text_leaves`，**逐子句**判定 · 与「轻症」
    **同子句**才算数 —— 沿用残余 K「不确定/条件必须与相关对象同子句」的既有口径）：
      ① 除外     → `_crx_record_mild_excluded`（记录级双向除外判定）
      ② 不确定   → `_has_uncertainty`（待核实 / 是否 / 以…为准 …）
      ③ 条件     → `_has_condition` + `_CRX_MILD_CONDITIONAL_RE`（需满足特定条件 …）
      ④ 矛盾     → `_crx_record_contradiction(product, "轻症")`（肯定承保 + 除外并存）

    返回：
      {
        "excluded":   bool,  # ① 记录级轻症除外
        "uncertain":  bool,  # ②③ 记录级轻症待核实 / 条件性表述
        "conflict":   bool,  # ④ 记录级轻症矛盾
        "unverified": bool,  # ①②③④ 任一命中 → 轻症保障未经确认
      }
    """
    excluded = bool(_crx_record_mild_excluded(product))
    uncertain = False
    for text in _product_text_leaves(product):
        if not isinstance(text, str) or "轻症" not in text:
            continue
        for clause in _split_clauses(text):
            if "轻症" not in clause:
                continue
            if _has_uncertainty(clause, 0, len(clause)):
                uncertain = True
            elif _has_condition(clause, 0, len(clause)):
                uncertain = True
            elif _CRX_MILD_CONDITIONAL_RE.search(clause):
                uncertain = True
    conflict = bool(_crx_record_contradiction(product, "轻症"))
    return {
        "excluded": excluded,
        "uncertain": uncertain,
        "conflict": conflict,
        "unverified": bool(excluded or uncertain or conflict),
    }


def _crx_mild_unverified_limitation(product, mild_state=None):
    """轻症保障**记录级未经确认**时的如实限制说明 → dict | None

    官方 SDI-4 残余 S-1（china v2.4.33 · 原文）：
      "Return an explicit limitation whenever the shared state is unverified, distinguishing
       mild-illness exclusions from critical-illness category exclusions. Have both plan
       builders or the finalizer propagate that shared limitation into the final JSON for
       retained products, and clarify that budget feasibility does not establish coverage
       validity."

    ⚠ 与 `_crx_ci_category_limitation`（重疾**类别级**除外）的 reason **必须可区分**
      （官方 remediation 原文要求 distinguishing）。
    ⚠ 文案**不得**断言被除外 / 未经证实的保障（只如实报告「记录中的表述 + 待核实
      + 不作对外宣称」）。
    ⚠ 官方要求明确「预算可行 ≠ 保障已核实」→ reason 末尾如实点明。
    """
    if not product:
        return None
    st = mild_state if mild_state is not None else _crx_record_mild_state(product)
    if not st.get("unverified"):
        return None
    if st.get("excluded"):
        basis = "产品记录中存在轻症保障除外表述"
    else:
        basis = "产品记录中轻症保障存在待核实或条件性表述"
    return {
        "type": "coverage_limit",
        "product_type": "重疾险",
        "product": product.get("name"),
        "requirement": "轻症保障责任",
        "reason": (basis + "，轻症保障范围待核实，已不作对外宣称；"
                   "保费在预算内仅说明预算可行，不代表保障范围已核实"),
    }

def _crx_record_mild_excluded(product):
    """产品记录内是否存在**明确指向轻症**的除外表述（记录级）→ True

    官方 remediation（残余 R-1 · 原文）：
      「recognize payment and benefit-responsibility wording as part of the same
        coverage subject, bind exclusions consistently in both directions, and
        suppress unresolved interpretations.」

    ⇒ 轻症主体路径的除外判定**双向一致**
      （后向「轻症给付责任除外」+ 前向「给付责任不保轻症」都命中），
      且给付措辞不再被当成「别的保障对象」。
    """
    if not product:
        return False
    for text in _product_text_leaves(product):
        if not isinstance(text, str) or "轻症" not in text:
            continue
        for clause in _split_clauses(text):
            if "轻症" not in clause:
                continue
            if _crx_clause_excludes_subject(clause, "轻症"):
                return True
    return False


# ══════════════════════════════════════════════════════════════════════
# 官方 SDI-4 残余 AE-2（2026-11-27 公开复扫）· **肯定证据闸**（单一事实源）
#
#   官方 finding / explanation / remediation 原文见 `_crx_ci_claim_state` 注释。
#
#   ⇒ 「肯定证据」= 记录级存在下列**任一**：
#     ① 结构化条目：`covered=True`（或 `is_covered=True`）且**条目标识含重疾类词**
#        （重疾 / 重大疾病）；
#     ② 文本子句：某子句含「重疾 / 重大疾病」，且该子句**不是**否定、
#        **不是**存疑、**不是**条件性（复用既有 `_structured_text_is_negative` /
#        `_structured_text_is_uncertain` / `_has_uncertainty` / `_has_condition`
#        + 类别级除外判定 → **不新造词表**）。
#
#   ⚠ **宽口径**（主侧已量化：真实语料 168/168 款重疾险**全部**保留 →
#     0 款因缺肯定证据被压掉）→ **不得**再收紧（收紧会压掉真实宣称）。
#   ⚠ 判定**子句级**（一句话里既有肯定又有否定时，否定子句不提供肯定证据）。
# ══════════════════════════════════════════════════════════════════════


def _crx_ci_clause_is_affirmative(clause):
    """子句是否构成**肯定的重疾承保证据**（宽口径 · 子句级）

    口径：含重疾类词 + 非否定 + 非存疑 + 非条件 + 非类别级除外。
    """
    if not clause or not isinstance(clause, str):
        return False
    if not any(tok in clause for tok in _CRX_CI_CATEGORY_TOKENS):
        return False
    # ⚠ 否定（与结构化侧**同一份**词表 / 通用模式）
    if _structured_text_is_negative(clause):
        return False
    # ⚠ 存疑（待核实 / 是否 / 以…为准 / 可能 …）
    if _structured_text_is_uncertain(clause):
        return False
    if _has_uncertainty(clause, 0, len(clause)):
        return False
    # ⚠ 条件性（条件无法渲染 → 不得无条件宣称）
    if _has_condition(clause, 0, len(clause)):
        return False
    # ⚠ 类别级除外（本子句本身就是除外 → 不提供肯定证据）
    if _crx_clause_excludes_ci_category(clause):
        return False
    return True


def _crx_ci_structured_affirmative_evidence(product):
    """结构化权威字段里是否存在**重疾类**的肯定承保证据 → bool

    ⚠ 与授权路径**同一状态**（`_structured_value_state`）→ contradictory /
      ambiguous 的条目**不**算肯定证据。
    """
    if not isinstance(product, dict):
        return False
    for field in _STRUCTURED_AUTHORITY_FIELDS:
        value = product.get(field)
        entries = []
        if isinstance(value, dict):
            entries = list(value.items())
        elif isinstance(value, (list, tuple)):
            entries = [(None, item) for item in value]
        for key, entry in entries:
            ident = key if isinstance(key, str) else None
            if isinstance(entry, dict):
                if not ident:
                    ident = _structured_item_identifier(entry)
                if not isinstance(ident, str) or not ident.strip():
                    continue
                if not any(tok in ident for tok in _CRX_CI_CATEGORY_TOKENS):
                    continue
                if _structured_value_state(entry) != "affirmative":
                    continue
                return True
            # 布尔形态：{"重疾": true}
            if not ident:
                continue
            if not any(tok in ident for tok in _CRX_CI_CATEGORY_TOKENS):
                continue
            if _structured_decision_state(entry) != "affirmative":
                continue
            return True
    return False


def _crx_ci_text_affirmative_evidence(product):
    """**文本子句**里是否存在肯定的重疾承保证据 → bool（宽口径）"""
    if not isinstance(product, dict):
        return False
    for text in _product_text_leaves(product):
        if not isinstance(text, str) or not text.strip():
            continue
        if not any(tok in text for tok in _CRX_CI_CATEGORY_TOKENS):
            continue
        for clause in _split_clauses(text):
            if _crx_ci_clause_is_affirmative(clause):
                return True
    return False


def _crx_ci_affirmative_evidence(product):
    """记录级是否存在**肯定的重疾承保证据** → bool（AE-2 的单一事实源）

    ⚠ 官方 SDI-4 残余 AE-2 remediation 原文：
      「requiring validated affirmative evidence before marking a benefit allowed」
    ⇒ 结构化（`covered=True` + 重疾类标识）**或** 文本（子句含重疾类词 +
      非否定 / 非存疑 / 非条件）任一成立即视为**有肯定证据**。
    """
    if _crx_ci_structured_affirmative_evidence(product):
        return True
    return _crx_ci_text_affirmative_evidence(product)


def _crx_ci_claim_state(product):
    """**共享**的「重疾保障已验证状态」→ dict（残余 R 的单一事实源）

    官方 remediation（残余 R-2 / R-3 · 原文）：
      「Compute a shared, validated critical-illness coverage state before
        generating any benefits, features, or descriptions.」
      「Apply exclusion and unresolved-conflict suppression to both standard and
        premium branches and every downstream claim surface, preserving an
        explicit unverified limitation instead.」

    返回：
      {
        "excluded":   bool,       # 记录级**类别级**重疾除外
        "unverified": bool,       # 记录级**轻症除外** → 疾病保障族未经确认
        "allowed":    bool,       # 是否允许产出肯定的重疾/轻症保障宣称
        "limitation": dict|None,  # 如实限制文案（unverified · **不得**删除）
      }
    """
    # ⚠ 官方 SDI-4 残余 AD（2026-11-26 公开复扫）：类别级状态**同时**给出
    #   「确定除外」与「存疑未决」两类信号。
    ci_state = _crx_record_ci_category_state(product)
    excluded = bool(ci_state["excluded"])
    ci_unresolved = bool(ci_state["unresolved"])
    # ⚠ 官方 SDI-4 残余 S-2：记录级轻症覆盖状态（除外 / 待核实 / 条件 / 矛盾）
    #   必须在**任何轻症/重疾宣称生成之前**算出 → 单一事实源。
    mild = _crx_record_mild_state(product)
    unverified = False
    if not excluded:
        unverified = bool(mild["unverified"]) or ci_unresolved
    # ⚠⚠ 官方 SDI-4 残余 AE-2（2026-11-27 公开复扫 · ai v2.4.48 / china v2.4.45 ·
    #   Excessive Agency · MEDIUM · confidence 0.99）finding 原文：
    #     「The supposedly validated critical-illness state treats absence of
    #       detected problems as positive coverage verification.」
    #   explanation 原文：
    #     「… a record stating 「重疾保障待核实」 without mild-illness wording or a
    #       numeric disease count can pass this state and receive the unconditional
    #       fallback 「重疾保障，确诊即赔付…」.」
    #   remediation 原文：
    #     「Represent coverage as explicit verified, excluded, and unverified states,
    #       requiring validated affirmative evidence before marking a benefit
    #       allowed. … missing evidence must remain unverified.」
    #
    #   ⇒ 根因（**方向反了**）：旧口径 `validated = not excluded and not unverified`
    #     → 「**没查到问题**」被当成「**已验证承保**」。
    #   ⇒ 修法：**肯定证据闸**（`_crx_ci_affirmative_evidence`）——
    #     记录级必须存在**肯定的重疾承保证据**才允许产出肯定宣称。
    has_evidence = _crx_ci_affirmative_evidence(product)
    if not has_evidence:
        unverified = True
    limitation = _crx_ci_category_limitation(product)
    if limitation is None and unverified:
        # ⚠ 官方 SDI-4 残余 S-1：共享状态 `unverified` 时**必须**返回非空 limitation
        #   （轻症**单独**除外时不得返回 None → 方案层不得静默），且须与
        #   「重疾类别级除外」的限制文案**可区分**。
        limitation = _crx_mild_unverified_limitation(product, mild)
        if limitation is None:
            # ⚠ 官方 SDI-4 残余 AD：类别级**存疑**未决 → 如实报告限制
            #   （**不得**静默留空）。
            limitation = _crx_ci_category_unverified_limitation(product)
        if limitation is None and not has_evidence:
            # ⚠ 官方 SDI-4 残余 AE-2：**缺少肯定承保证据** → 如实报告限制
            #   （**不得**静默留空 · 复用既有「类别级未核实」文案体系）。
            limitation = _crx_ci_category_unverified_limitation(
                product, no_evidence=True)
    # ⚠ 官方 SDI-4 残余 AD + AE-2：肯定宣称**必须**依赖**已验证的覆盖证据**
    #   （官方 remediation 原文：「Require validated coverage evidence before
    #    emitting affirmative claims」）→ `allowed` ≡ `validated`。
    validated = bool(not excluded and not unverified and has_evidence)
    if not validated:
        # ⚠ 官方口径三态（verified / excluded / unverified）：
        #   **未验证**（validated=False）→ 一律按 unverified 如实报告
        #   （**不得**让「没验证过」看起来像「已验证」）。
        unverified = True
    return {
        "excluded": excluded,
        "unverified": unverified,
        "validated": validated,
        "allowed": validated,
        "limitation": limitation,
    }


def _crx_plan_ci_allowed(plan_products, product_records):
    """方案内保留的重疾险条目，其重疾保障是否**已验证**（可对外宣称）

    官方 remediation（残余 R-3 · 原文）：
      「Propagate the validated coverage state into plan descriptions, features,
        and recommendations so retaining a product entry cannot reintroduce
        excluded-coverage claims」

    ⇒ 保留条目**不得**重新引入被除外的重疾保障宣称。
    """
    if not plan_products or not product_records:
        return True          # 无记录可查 → 不压制（保持既有调用兼容）
    by_name = {}
    for rec in product_records:
        if isinstance(rec, dict):
            nm = rec.get("name")
            if nm and nm not in by_name:
                by_name[nm] = rec
    for entry in plan_products:
        if not isinstance(entry, dict) or entry.get("type") != "重疾险":
            continue
        rec = by_name.get(entry.get("product_name"))
        if rec is None:
            continue
        if not _crx_ci_claim_state(rec)["allowed"]:
            return False
    return True


def _crx_feature(product):
    """标准版 features 中的重疾卖点：按真实选中产品派生，不写死「终身保障」。

    ⚠ 官方 SDI-4 残余 R（finding L2779-2795 · 原文）：
      「…bypassed by premium benefits and plan features.」
      「Apply exclusion and unresolved-conflict suppression to … every downstream
        claim surface, preserving an explicit unverified limitation instead.」
    ⇒ features 属**下游宣称面** → 必须与 benefits 受**同一**共享状态约束。
    """
    if not product:
        return "重疾保障按实际需求配置"
    state = _crx_ci_claim_state(product)
    if not state["allowed"]:
        # 不宣称被除外 / 未经确认的重疾保障（限制由 `_crx_ci_category_limitation` 如实报告）
        return "重疾保障范围待核实"
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


def _build_plan_description(plan_name, products, product_records=None):
    """按**实际剩余险种**生成方案描述。

    ⚠️ R7 整改 2026-11-07：原先 description 写死（如「保障全面，含重疾保障」
    「高保额全方位保障，另含养老储蓄规划」），在产品被移除后不再成立 → 属于
    对外虚报。本函数以 plan["products"] 为唯一事实来源动态生成。

    ⚠️ 官方 SDI-4 残余 R（finding L2780-2788 · 原文）：
      「The comprehensive plan still asserts critical-illness benefits when the
        product record explicitly excludes that coverage.」
      「Propagate the validated coverage state into plan descriptions, features,
        and recommendations so retaining a product entry cannot reintroduce
        excluded-coverage claims」

    Args:
        plan_name: 方案名（基础版 / 标准版 / 全面版）
        products: 方案实际保留的产品列表
        product_records: 产品库记录列表（用于读取保留产品的**已验证状态**；
            缺省时不做状态压制，保持既有调用兼容）

    Returns:
        描述文本；产品为空时明确说明方案不覆盖任何险种。
    """
    present = {p.get("type") for p in (products or [])}
    if not present:
        return f"{plan_name}：当前预算不足以配置任何险种，方案暂不覆盖具体保障责任"

    # ⚠ 官方 SDI-4 残余 R：保留重疾险条目**不得**重新引入被除外的重疾保障宣称
    #   → 重疾保障未经确认（类别级除外 / 轻症除外）时，描述不得宣称「含重疾保障」
    if ("重疾险" in present
            and not _crx_plan_ci_allowed(products, product_records)):
        present = present - {"重疾险"}
        if not present:
            return f"{plan_name}：重疾保障范围待核实，方案暂不覆盖具体保障责任"

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
            # ⚠ 官方 SDI-4 残余 W：结构化条目自相矛盾 / 不可解释 → 治疗手段不得宣称
            #   → 方案层必须**如实报告**该限制（不得静默留空）。
            _mi_treat_lim = _medical_treatment_unverified_limitation(mi_product)
            if _mi_treat_lim:
                plan.setdefault("limitations", []).append(_mi_treat_lim)
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
        # ⚠ 官方 SDI-4 残余 Q：类别级重疾除外 → 兜底文案已置空 → 如实报告限制
        # ⚠️ 官方 SDI-4 残余 Q + 残余 S-1：统一取**共享状态**的 limitation
        #   （类别级除外 / 轻症单独除外 / 轻症待核实 —— 统一如实报告，不得静默）
        _crx_lim = _crx_ci_claim_state(crx_product).get("limitation")
        if _crx_lim:
            plan.setdefault("limitations", []).append(_crx_lim)
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
        # ⚠ 官方 SDI-4 残余 W：结构化条目自相矛盾 / 不可解释 → 治疗手段不得宣称
        #   → 方案层必须**如实报告**该限制（不得静默留空）。
        _mi_treat_lim = _medical_treatment_unverified_limitation(mi_product)
        if _mi_treat_lim:
            plan.setdefault("limitations", []).append(_mi_treat_lim)

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
    # ⚠ 官方 SDI-4 残余 R：features 属**下游宣称面** → 共享的已验证状态
    #   必须传导到方案级卖点（重疾保障未经确认时不得宣称「重疾」）。
    _crx_state = _crx_ci_claim_state(crx_product)
    _scope_types = ["寿险", "重疾", "医疗", "意外"]
    if not _crx_state["allowed"]:
        _scope_types = [t for t in _scope_types if t != "重疾"]
    plan["features"] = [
        "保障全面：" + "+".join(_scope_types),
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
    crx_product = None
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
        # ⚠ 官方 SDI-4 残余 Q：类别级重疾除外 → 如实报告限制
        # ⚠️ 官方 SDI-4 残余 Q + 残余 S-1：统一取**共享状态**的 limitation
        #   （类别级除外 / 轻症单独除外 / 轻症待核实 —— 统一如实报告，不得静默）
        _crx_lim = _crx_ci_claim_state(crx_product).get("limitation")
        if _crx_lim:
            plan.setdefault("limitations", []).append(_crx_lim)
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
        # ⚠ 官方 SDI-4 残余 W：结构化条目自相矛盾 / 不可解释 → 治疗手段不得宣称
        #   → 方案层必须**如实报告**该限制（不得静默留空）。
        _mi_treat_lim = _medical_treatment_unverified_limitation(mi_product)
        if _mi_treat_lim:
            plan.setdefault("limitations", []).append(_mi_treat_lim)

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
    # ⚠ 官方 SDI-4 残余 R：全面版 features 属**下游宣称面** → 共享的已验证状态
    #   必须传导到方案级卖点（重疾保障未经确认时不得宣称「重疾」/「重疾险保额」）。
    _crx_state = _crx_ci_claim_state(crx_product)
    _scope_types = ["寿险", "重疾", "医疗", "意外"]
    if not _crx_state["allowed"]:
        _scope_types = [t for t in _scope_types if t != "重疾"]
    _features = ["全方位高保额保障：" + "+".join(_scope_types)]
    if _crx_state["allowed"]:
        _features.append("重疾险保额高达年收入5倍")
    _features += [
        mi_feature,
        "定期寿险高保额，覆盖所有家庭财务责任",
        "可选储蓄险，为养老做准备",
        "年保费已按年度保费上限（min(年度预算, 年收入×20%)）校验"
    ]
    plan["features"] = _features

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
        plan.get("plan_name", ""), plan.get("products", []), products)
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
