#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fallback_key_dimensions.py

Step 4.5 关键维度兜底召回脚本。

解决问题：Step 4 语义召回（TF-IDF）对短标签（如"女"/"男"）和结构化标签（如合作伙伴的
"基本属性_居住城市级别_一线城市"）容易因相似度偏低被 TopK 截断，导致性别/年龄/城市级别等
互斥关键维度在候选池中缺失。
"""

import argparse
import json
import re
from typing import Dict, List, Optional, Tuple

# 标签前缀兼容：明略和合作伙伴标签前缀可能是"基础属性_"或"基本属性_"
_PREFIX = r"(?:基础属性|基本属性)"

# ============================================================
# 关键维度兜底规则（配置化，无硬编码tagId）
# ============================================================

GENDER_RULES = {
    "female": {
        "match_names": {"女", "女性"},
        "match_patterns": [rf"^{_PREFIX}_性别_女$", r"^性别_女$"],
        "exclude_keywords": ["护理", "向", "装", "健康", "频道"],
        "similarity": 0.95,
        "label": "女",
        "dim_hint": "性别",
    },
    "male": {
        "match_names": {"男", "男性"},
        "match_patterns": [rf"^{_PREFIX}_性别_男$", r"^性别_男$"],
        "exclude_keywords": ["护理", "装", "频道"],
        "similarity": 0.95,
        "label": "男",
        "dim_hint": "性别",
    },
}

# 年龄段映射：兼容5岁段（明略）和合并段（合作伙伴18-24/25-34/35-44）
AGE_RULES = {
    "15-17": {"match_names": {"15-17", "15-17岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$"], "similarity": 0.60, "dim_hint": "年龄"},
    "18-19": {"match_names": {"18-19", "18-19岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$", rf"^{_PREFIX}_年龄_18-19$"], "similarity": 0.85, "dim_hint": "年龄"},
    "20-24": {"match_names": {"20-24", "20-24岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$", rf"^{_PREFIX}_年龄_20-24$"], "similarity": 0.88, "dim_hint": "年龄"},
    "25-29": {"match_names": {"25-29", "25-29岁"}, "patterns": [rf"^{_PREFIX}_年龄_25-34$", rf"^{_PREFIX}_年龄_25-29$"], "similarity": 0.88, "dim_hint": "年龄"},
    "30-34": {"match_names": {"30-34", "30-34岁"}, "patterns": [rf"^{_PREFIX}_年龄_25-34$", rf"^{_PREFIX}_年龄_30-34$", rf"^{_PREFIX}_年龄_35-44$"], "similarity": 0.86, "dim_hint": "年龄"},
    "35-39": {"match_names": {"35-39", "35-39岁"}, "patterns": [rf"^{_PREFIX}_年龄_35-44$", rf"^{_PREFIX}_年龄_35-39$"], "similarity": 0.82, "dim_hint": "年龄"},
    "40-44": {"match_names": {"40-44", "40-44岁"}, "patterns": [rf"^{_PREFIX}_年龄_35-44$", rf"^{_PREFIX}_年龄_40-44$"], "similarity": 0.80, "dim_hint": "年龄"},
    "45-49": {"match_names": {"45-49", "45-49岁"}, "patterns": [rf"^{_PREFIX}_年龄_45\+$", rf"^{_PREFIX}_年龄_45-49$"], "similarity": 0.80, "dim_hint": "年龄"},
    "50-54": {"match_names": {"50-54", "50-54岁"}, "patterns": [rf"^{_PREFIX}_年龄_45\+$", rf"^{_PREFIX}_年龄_50-54$"], "similarity": 0.78, "dim_hint": "年龄"},
    "55-59": {"match_names": {"55-59", "55-59岁"}, "patterns": [rf"^{_PREFIX}_年龄_55-59$"], "similarity": 0.78, "dim_hint": "年龄"},
    # 合作伙伴合并段
    "18-24": {"match_names": {"18-24", "18-24岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$"], "similarity": 0.90, "dim_hint": "年龄"},
    "25-34": {"match_names": {"25-34", "25-34岁"}, "patterns": [rf"^{_PREFIX}_年龄_25-34$"], "similarity": 0.90, "dim_hint": "年龄"},
    "35-44": {"match_names": {"35-44", "35-44岁"}, "patterns": [rf"^{_PREFIX}_年龄_35-44$"], "similarity": 0.88, "dim_hint": "年龄"},
    "25-35": {"match_names": {"25-35", "25-35岁"}, "patterns": [rf"^{_PREFIX}_年龄_25-34$"], "similarity": 0.85, "dim_hint": "年龄"},
    "18-30": {"match_names": {"18-30", "18-30岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$", rf"^{_PREFIX}_年龄_25-34$"], "similarity": 0.82, "dim_hint": "年龄"},
    "18-35": {"match_names": {"18-35", "18-35岁"}, "patterns": [rf"^{_PREFIX}_年龄_18-24$", rf"^{_PREFIX}_年龄_25-34$"], "similarity": 0.82, "dim_hint": "年龄"},
}

# 城市级别（合作伙伴标签格式：基本属性_居住城市级别_xx城市）
CITY_LEVEL_RULES = {
    "一线": {
        "match_names": {"一线城市"},
        "match_keywords": ["一线城市"],
        "match_patterns": [rf"^{_PREFIX}_居住城市级别_一线城市$"],
        "similarity": 0.90,
        "dim_hint": "城市级别",
    },
    "新一线": {
        "match_names": {"新一线城市"},
        "match_keywords": ["新一线城市"],
        "match_patterns": [rf"^{_PREFIX}_居住城市级别_新一线城市$"],
        "similarity": 0.88,
        "dim_hint": "城市级别",
    },
    "二线": {
        "match_names": {"二线城市"},
        "match_keywords": ["二线城市"],
        "match_patterns": [rf"^{_PREFIX}_居住城市级别_二线城市$"],
        "similarity": 0.88,
        "dim_hint": "城市级别",
    },
    "三线": {
        "match_names": {"三线城市"},
        "match_keywords": ["三线城市"],
        "match_patterns": [rf"^{_PREFIX}_居住城市级别_三线城市$"],
        "similarity": 0.85,
        "dim_hint": "城市级别",
    },
    "四线及以下": {
        "match_names": {"四线及以下城市", "四线城市"},
        "match_keywords": ["四线及以下", "四线城市"],
        "match_patterns": [rf"^{_PREFIX}_居住城市级别_四线"],
        "similarity": 0.82,
        "dim_hint": "城市级别",
    },
}


def _matches_any(name, names_set, patterns=None, keywords=None, exclude_keywords=None):
    if exclude_keywords and any(kw in name for kw in exclude_keywords):
        return False
    if name in names_set:
        return True
    if keywords and any(kw in name for kw in keywords):
        return True
    if patterns:
        for p in patterns:
            if re.search(p, name):
                return True
    return False


def _load_usable_pool(tag_pool_path):
    with open(tag_pool_path, "r", encoding="utf-8") as f:
        pool = json.load(f)
    return [t for t in pool if t.get("isDirectory") == 1]


def _detect_schema_gender(schema):
    demo = schema.get("demographics", {}) or {}
    gender_raw = demo.get("gender", "")
    gender = str(gender_raw).lower().strip()
    raw = schema.get("_raw_text", "")
    if gender in ("女", "female", "f", "w"):
        return "female"
    if gender in ("男", "male", "m"):
        return "male"
    if any(k in raw for k in ["女孩", "女性", "女士", "女生", "她", "美女", "精致女孩", "宝妈", "少女", "妈妈"]):
        return "female"
    if any(k in raw for k in ["男孩", "男性", "男士", "男生", "他", "帅哥", "大叔", "先生", "爸爸"]):
        return "male"
    return None


def _detect_schema_ages(schema):
    """从Schema中检测目标年龄段列表，精确匹配不超范围"""
    demo = schema.get("demographics", {}) or {}
    age_raw = demo.get("age", "") or ""
    if isinstance(age_raw, list):
        age_str = " ".join(str(a) for a in age_raw)
    else:
        age_str = str(age_raw)
    if not age_str:
        return []
    ages = set()
    # 尝试匹配范围字符串，如"18-30"、"25~35岁"
    range_match = re.search(r'(\d{1,2})\s*[-~到至]\s*(\d{1,2})', age_str)
    if range_match:
        start, end = int(range_match.group(1)), int(range_match.group(2))
        # 先尝试匹配合作伙伴合并段
        merged_segs = [(18,24,"18-24"), (25,34,"25-34"), (35,44,"35-44")]
        for ms, me, mlabel in merged_segs:
            if ms <= end and me >= start:
                ages.add(mlabel)
        # 如果合并段不够精确（比如18-30不完全=18-24+25-34），再补5岁段
        for seg_start in [18, 20, 25, 30, 35, 40, 45, 50, 55]:
            seg_end = seg_start + 4
            if seg_start == 18:
                seg_end = 19
            if seg_start <= end and seg_end >= start:
                ages.add(f"{seg_start}-{seg_end}")
    else:
        for k in AGE_RULES:
            if k in age_str:
                ages.add(k)
    return [a for a in ages if a in AGE_RULES]


def _detect_schema_city_levels(schema):
    """从Schema中检测目标城市级别（修复：先判断类型再取值）"""
    loc = schema.get("location", {}) or {}
    city_raw = loc.get("city_level") or loc.get("city_tier") or []
    # 正确处理列表和字符串
    if isinstance(city_raw, list):
        text = " ".join(str(c) for c in city_raw)
    elif isinstance(city_raw, str):
        text = city_raw
    else:
        text = ""
    raw = schema.get("_raw_text", "")
    text = (text + " " + raw) if text else raw
    levels = []
    # 注意顺序：先判断"新一线"再判断"一线"，避免"新一线"误匹配"一线"
    for keyword, label in [("新一线", "新一线"), ("一线", "一线"), ("二线", "二线"), ("三线", "三线"), ("四线", "四线及以下"), ("低线", "四线及以下")]:
        if keyword in text and label not in levels:
            levels.append(label)
    return levels


def _check_dim_exists(candidates, match_fn, tag_type=None):
    """检查候选池中是否已存在某维度（可选指定来源tag_type: 1=明略,3=合作）的标签"""
    for c in candidates:
        if tag_type is not None and c.get("tagType") != tag_type:
            continue
        if match_fn(c):
            return True
    return False


def _find_tag_in_pool(pool, existing_ids, rule, target_tag_type=None):
    """在标签池中找匹配规则的标签，可选限定来源"""
    for t in pool:
        tid = t["tagId"]
        if tid in existing_ids:
            continue
        if target_tag_type is not None and t.get("tagType") != target_tag_type:
            continue
        if _matches_any(t["tagName"], rule["match_names"],
                        patterns=rule.get("match_patterns"),
                        keywords=rule.get("match_keywords"),
                        exclude_keywords=rule.get("exclude_keywords")):
            return t
    return None


def _is_gender_tag(c, target):
    """通用性别匹配：同时兼容明略/合作标签名格式"""
    name = c.get("tagName", "")
    target_cn = "女" if target == "female" else "男"
    if name in {target_cn, target_cn + "性"}:
        return True
    if re.search(rf"^性别_{target_cn}$", name):
        return True
    if re.search(rf"^{_PREFIX}_性别_{target_cn}$", name):
        return True
    return False


def _is_age_tag(c, age_key):
    name = c.get("tagName", "")
    rule = AGE_RULES.get(age_key, {})
    # 1. 精确match_names匹配（如"25-29"、"25-29岁"）
    if name in rule.get("match_names", set()):
        return True
    # 2. patterns匹配（合作前缀段 + 明略纯数字段）
    for p in rule.get("patterns", []):
        if re.search(p, name):
            return True
    # 3. 明略纯年龄段名（如"25-29"直接匹配标签名，不带"年龄_"前缀）
    if re.match(r'^\d{2}-\d{2}岁?$', name.strip()):
        # 解析数字范围
        m = re.match(r'^(\d{2})-(\d{2})', name.strip())
        if m:
            s, e = int(m.group(1)), int(m.group(2))
            # 检查age_key对应的范围是否重叠
            if "-" in age_key:
                parts = age_key.split("-")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    ks, ke = int(parts[0]), int(parts[1])
                    return ks <= e and ke >= s
    return False


def _is_city_tag(c, level_key):
    name = c.get("tagName", "")
    rule = CITY_LEVEL_RULES.get(level_key, {})
    if name in rule.get("match_names", set()):
        return True
    for kw in rule.get("match_keywords", []):
        if kw in name:
            return True
    for p in rule.get("match_patterns", []):
        if re.search(p, name):
            return True
    return False


def _make_fallback_tag(t, rule, reason):
    return {
        "tagId": t["tagId"],
        "tagName": t["tagName"],
        "parentId": t.get("parentId"),
        "tagType": t.get("tagType"),
        "isDirectory": 1,
        "similarity": rule["similarity"],
        "recall_source": "fallback_dict",
        "_dim_hint": rule.get("dim_hint", ""),
        "_fallback_reason": reason,
    }


def _ensure_both_sources(pool, existing_ids, rule, reason_prefix, match_fn, fallback_added, candidates):
    """确保核心维度明略(tagType=1)和合作(tagType=3)两个来源都存在，缺哪个补哪个"""
    merged = list(candidates) + list(fallback_added)
    for src_type in [1, 3]:
        if not _check_dim_exists(merged, match_fn, tag_type=src_type):
            t = _find_tag_in_pool(pool, existing_ids, rule, target_tag_type=src_type)
            if t:
                src_name = "明略" if src_type == 1 else "合作"
                fb = _make_fallback_tag(t, rule, f"{reason_prefix}_{src_name}")
                fallback_added.append(fb)
                existing_ids.add(t["tagId"])


def fallback_recall(candidates, pool, schema):
    existing_ids = {c["tagId"] for c in candidates}
    for c in candidates:
        c["recall_source"] = "semantic"

    fallback_added = []

    # 1) 性别兜底（确保明略+合作双来源都存在）
    target_gender = _detect_schema_gender(schema)
    if target_gender:
        def _match_fn(c, tg=target_gender):
            return _is_gender_tag(c, tg)
        rule = GENDER_RULES[target_gender]
        _ensure_both_sources(pool, existing_ids, rule, f"gender_{target_gender}", _match_fn, fallback_added, candidates)

    # 2) 年龄段兜底（每个年龄段确保双来源）
    target_ages = _detect_schema_ages(schema)
    for age_key in target_ages:
        def _match_fn(c, ak=age_key):
            return _is_age_tag(c, ak)
        rule = AGE_RULES[age_key]
        _ensure_both_sources(pool, existing_ids, rule, f"age_{age_key}", _match_fn, fallback_added, candidates)

    # 3) 城市级别兜底（确保双来源）
    target_levels = _detect_schema_city_levels(schema)
    for level_key in target_levels:
        def _match_fn(c, lk=level_key):
            return _is_city_tag(c, lk)
        rule = CITY_LEVEL_RULES[level_key]
        _ensure_both_sources(pool, existing_ids, rule, f"city_{level_key}", _match_fn, fallback_added, candidates)

    merged = candidates + fallback_added
    return merged, fallback_added


def main():
    ap = argparse.ArgumentParser(description="Step 4.5 关键维度兜底召回")
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--tag-pool", required=True)
    ap.add_argument("--schema", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.candidates, "r", encoding="utf-8") as f:
        candidates = json.load(f)
    with open(args.schema, "r", encoding="utf-8") as f:
        schema = json.load(f)

    pool = _load_usable_pool(args.tag_pool)
    merged, fallback_added = fallback_recall(candidates, pool, schema)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    result = {
        "ok": True,
        "semantic_count": len(candidates),
        "fallback_added": len(fallback_added),
        "merged_total": len(merged),
        "fallback_details": [{"tagId": fb["tagId"], "tagName": fb["tagName"], "reason": fb["_fallback_reason"]} for fb in fallback_added],
        "out": args.out,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
