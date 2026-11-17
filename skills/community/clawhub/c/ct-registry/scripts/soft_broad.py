#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
soft_broad.py -- ct-registry 本地「软宽词」层（Tier-2 宽病类检测）

为何独立于 ct-base 的 keyword_breadth.py（单一真源）：
  - is_soft_broad 是 ct-registry 专属业务逻辑（常见疾病大类如糖尿病/高血压，
    单独检索可能过宽但属合法需求），不属于全 ct- 库共享的 keyword_breadth。
  - 把它塞进 keyword_breadth 会污染 ct-base 单一真源，导致发布闸门 §16.8 漂移，
    故下沉到本本地模块；keyword_breadth.py 须与 ct-base 字节级一致。

依赖：复用 keyword_breadth 的归一化（_norm）与药物判定（looks_like_drug），
不重复实现，避免又一份漂移源。

语义：仅整词匹配（不碰子串/词根），避免误伤组合检索。返回 True = 「软宽词」
（会进 soft_warns 警告层，不触发 is_broad_keyword 的硬退 sys.exit(2)，也不影响
choose_primary_keyword 重排——组合检索照常放行）。
"""

from keyword_breadth import _norm, looks_like_drug

# ---------------------------------------------------------------------------
# Tier-2 宽病类（软警告层，不硬退）：单独检索可能过宽、但属合法需求
# （用户可能就是要某疾病领域的宽概览）。仅整词匹配——绝不碰子串/词根，
# 以免误伤组合检索：如 "diabetes metformin" 归一化为 "diabetesmetformin"
# 整词，不在表内，自然放行。
# ---------------------------------------------------------------------------
BROAD_TERMS_SOFT_EN = {
    "diabetes", "diabetic", "hypertension", "asthma", "stroke", "obesity", "obese",
    "depression", "depressive", "alzheimer", "dementia", "parkinson", "epilepsy",
    "arthritis", "osteoporosis", "copd", "hiv", "aids", "hepatitis", "cirrhosis",
    "renal", "cardiac", "heart",
}
BROAD_TERMS_SOFT_ZH = {
    "糖尿病", "高血压", "哮喘", "卒中", "中风", "肥胖", "抑郁", "抑郁症",
    "阿尔茨海默", "痴呆", "帕金森", "癫痫", "关节炎", "骨质疏松", "慢阻肺",
    "艾滋", "艾滋病", "肝炎", "肝硬化", "肾病", "心脏病", "心衰",
}


def is_soft_broad(kw):
    """Tier-2 宽病类判定：单独检索可能过宽但属合法需求（用户可能要宽领域概览）。

    仅整词匹配（不碰子串/词根），避免误伤组合检索。返回 True 表示「软宽词」。
    注意：不进 is_broad_keyword（硬退词典），所以软词不会触发 sys.exit(2)，
    也不影响 choose_primary_keyword 的重排——组合检索照常放行。
    """
    if not kw:
        return False
    if looks_like_drug(kw):
        return False
    n = _norm(kw)
    if not n:
        return False
    return n in BROAD_TERMS_SOFT_EN or n in BROAD_TERMS_SOFT_ZH


if __name__ == "__main__":
    # 自测：改动后跑 `python soft_broad.py` 验证。
    tests = [("diabetes", True), ("糖尿病", True), ("cancer", False),
             ("diabetes metformin", False), ("肺癌", False), ("osimertinib", False)]
    for kw, exp in tests:
        got = is_soft_broad(kw)
        print(f"{'OK ' if got == exp else 'XX '} is_soft_broad({kw!r}) = {got} (exp {exp})")
