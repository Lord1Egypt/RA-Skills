#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_queries.py - 根据Schema解析结果，确定性生成标签召回所需的query列表和boost-words。

⚠️ 确定性保证：相同Schema输入 → 完全相同的query列表和boost-words输出（字符串级一致）。
AI助手不得手动构造query列表或boost-words，必须通过本脚本生成。

用法：
  python3 build_queries.py --schema schema.json [--synonyms synonyms_map.json] --out queries.json

schema.json 格式（10维Schema简化版，只需填已解析的维度值）：
{
  "demographics": {
    "gender": "female",          // female/male/"(不填则不生成性别查询)
    "age": ["20-24","25-29","30-34"]  // 年龄段列表
  },
  "location": {
    "city_level": ["一线","新一线","二线"]  // 城市级别关键词
  },
  "interest": ["护肤","美妆","彩妆"],   // 核心兴趣关键词
  "activity": {
    "active_window": "近30天"     // 活跃窗口
  }
}

输出 queries.json：
{
  "queries": ["女","女性","20-24岁","25-29岁","30-34岁","一线城市",...],
  "boost_words": ["女","女性","20-24岁","25-29岁","30-34岁","一线",...],
  "query_hash": "xxxxxxxxxxxx",  // query列表MD5，用于版本追踪
  "schema_hash": "xxxxxxxxxxxx"  // 输入schema MD5
}
"""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

# ============================================================
# 维度值→标签查询词的确定性映射表
# ============================================================

# 性别映射
GENDER_MAP = {
    "female": ["女", "女性"],
    "male": ["男", "男性"],
    "女": ["女", "女性"],
    "男": ["男", "男性"],
    "all": [],  # 全性别不生成性别查询
}

# 年龄段映射（标准年龄标签名，兼容合作伙伴合并段）
AGE_MAP = {
    "15-17": ["15-17岁", "15-17"],
    "18-19": ["18-19岁", "18-19"],
    "18-24": ["18-24岁", "18-24"],
    "20-24": ["20-24岁", "20-24"],
    "25-29": ["25-29岁", "25-29"],
    "30-34": ["30-34岁", "30-34"],
    "35-39": ["35-39岁", "35-39"],
    "25-34": ["25-34岁", "25-34", "25-29岁", "25-29", "30-34岁", "30-34"],
    "35-44": ["35-44岁", "35-44", "35-39岁", "35-39"],
    "25-35": ["25-34岁", "25-34", "25-29岁", "25-29", "30-34岁", "30-34", "35-39岁", "35-39"],
    "40-44": ["40-44岁", "40-44"],
    "45-49": ["45-49岁", "45-49"],
    "50-54": ["50-54岁", "50-54"],
    "55-59": ["55-59岁", "55-59"],
    "60-100": ["60-100岁", "60岁以上"],
}

# 城市级别映射
CITY_MAP = {
    "一线": ["一线城市"],
    "新一线": ["新一线城市"],
    "二线": ["二线城市"],
    "三线": ["三线城市"],
    "四线及以下": ["四线及以下城市"],
}

# 活跃度映射
ACTIVE_MAP = {
    "近30天": ["近30天活跃", "高活跃"],
    "近60天": ["近60天活跃"],
    "近90天": ["近90天活跃"],
}

# 兴趣关键词→查询词扩展映射（仅保留通用同义词扩展，不硬编码行业知识）
# 行业相关的扩展词应配置在 references/synonyms_map.json 中，通过trigger命中自动扩展
INTEREST_EXPAND = {
    # 通用同义词/别名
    "护肤": ["护肤", "护肤品"],
    "美妆": ["美妆", "化妆品"],
    "彩妆": ["彩妆"],
    "美妆个护": ["美妆个护"],
    "高消费": ["高消费", "高收入", "轻奢"],
    "中高消费": ["中高消费", "轻奢"],
    "旅游": ["旅游", "旅行"],
    "美食": ["美食", "餐饮"],
    "运动": ["运动", "健身"],
    "汽车": ["汽车", "汽车消费"],
    "3C": ["3C消费", "数码"],
    "房产": ["房产消费", "房产"],
    "教育": ["教育", "教育培训"],
    "游戏": ["游戏"],
    "金融": ["金融", "理财", "投资"],
    "医疗": ["医疗消费", "健康"],
    "母婴": ["母婴"],
    "孕婴": ["孕婴"],
    "亲子育儿": ["亲子育儿"],
    "新妈": ["新妈"],
    "老妈": ["老妈"],
    "白领": ["白领", "新锐白领"],
}


def md5_str(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:12]


def _as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def _flatten_to_keywords(obj: Any) -> List[str]:
    """从任意嵌套结构中抽取可作为query的字符串（确定性：按发现顺序，后续统一排序）。"""
    out: List[str] = []
    if obj is None:
        return out
    if isinstance(obj, str):
        s = obj.strip()
        if s:
            out.append(s)
        return out
    if isinstance(obj, (int, float)):
        out.append(str(obj))
        return out
    if isinstance(obj, list):
        for it in obj:
            out.extend(_flatten_to_keywords(it))
        return out
    if isinstance(obj, dict):
        for k in sorted(obj.keys()):
            if k.startswith("_"):
                continue
            out.extend(_flatten_to_keywords(obj.get(k)))
        return out
    return out


def _normalize_full_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """兼容两种输入：
    1) 精简Schema（demographics/location/interest/activity/_raw_text）
    2) 10维业务Schema（market/objective/audience/.../_raw_text）

    输出为 build_queries.py 可识别的精简Schema结构。
    """
    if not isinstance(schema, dict):
        return {}

    # 已是精简Schema
    if any(k in schema for k in ("demographics", "location", "interest", "activity")) and "audience" not in schema:
        return schema

    aud = schema.get("audience", {}) or {}

    demos_src = aud.get("demographics", {}) or {}
    loc_src = aud.get("location", {}) or {}
    act_src = aud.get("activity", {}) or {}

    # interest：从interest/scene/behavior/lifestyle/industry_ext里抽取关键词（跨行业通用）
    interest_kws: List[str] = []
    for key in ("interest", "scene", "behavior", "lifestyle", "kol_koc"):
        interest_kws.extend(_flatten_to_keywords(aud.get(key)))
    interest_kws.extend(_flatten_to_keywords(schema.get("industry_ext")))

    # 兜底：把_raw_text也作为关键词来源之一（但_raw_text本身仍走专门抽取逻辑）
    raw_text = schema.get("_raw_text", "")

    # 活跃度字段名兼容：recent_active_window -> active_window
    active_window = None
    if isinstance(act_src, dict):
        raw_aw = act_src.get("active_window")
        if raw_aw:
            active_window = str(raw_aw)
        if not active_window:
            raw_aw = act_src.get("recent_active_window")
            if isinstance(raw_aw, dict):
                raw_aw = raw_aw.get("value")
            if raw_aw:
                active_window = str(raw_aw)

    # 城市级别字段名兼容：city_level/city_tier
    city_level = None
    if isinstance(loc_src, dict):
        for ck in ("city_level", "city_tier"):
            v = loc_src.get(ck)
            if isinstance(v, dict):
                v = v.get("value")
            if v:
                city_level = v
                break

    # 性别/年龄（尽量兼容，但不强行补全）
    gender = demos_src.get("gender")
    if isinstance(gender, dict):
        gender = gender.get("value")
    age = demos_src.get("age")
    if isinstance(age, dict):
        age = age.get("value")

    slim = {
        "demographics": {
            "gender": gender or "",
            "age": _as_list(age),
        },
        "location": {
            "city_level": _as_list(city_level),
        },
        "interest": [s for s in interest_kws if isinstance(s, str) and s.strip()],
        "activity": {
            "active_window": active_window or "",
        },
        "constraints": schema.get("constraints", {}) or {},
        "_raw_text": raw_text,
    }
    return slim


def build_queries_from_schema(schema: Dict[str, Any], synonyms_map: Dict[str, Any] = None) -> Dict[str, Any]:
    """从Schema确定性生成query列表和boost-words。

    返回的queries和boost_words都是按固定顺序排列的有序列表。
    """
    schema = _normalize_full_schema(schema)

    queries = []
    seen = set()

    def add(terms: List[str]):
        for t in terms:
            t = t.strip()
            if t and t not in seen:
                seen.add(t)
                queries.append(t)

    demos = schema.get("demographics", {}) or {}
    loc = schema.get("location", {}) or {}
    # interest 兼容列表格式和 {core:[], other:[]} 对象格式
    interest_raw = schema.get("interest", []) or []
    if isinstance(interest_raw, dict):
        interest = list(interest_raw.get("core", []) or []) + list(interest_raw.get("other", []) or [])
    else:
        interest = list(interest_raw)
    activity = schema.get("activity", {}) or {}
    constraints = schema.get("constraints", {}) or {}

    # 1. 性别查询词
    gender = demos.get("gender", "")
    if gender and gender in GENDER_MAP:
        add(GENDER_MAP[gender])

    # 2. 年龄查询词（精确范围展开，不超出用户指定范围）
    age_list = demos.get("age", []) or []
    if isinstance(age_list, str):
        age_list = [age_list]
    expanded_ages = set()
    for age_key in age_list:
        if not age_key:
            continue
        age_str = str(age_key).strip()
        if age_str in AGE_MAP:
            expanded_ages.add(age_str)
            continue
        # 解析范围字符串，如"18-30"、"25~35岁"
        range_match = re.match(r'^(\d{1,2})\s*[-~到至]\s*(\d{1,2})', age_str)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            # 1. 优先匹配合作伙伴合并段（18-24/25-34/35-44），与标签名完全一致
            merged_ranges = [(18,24,"18-24"), (25,34,"25-34"), (35,44,"35-44")]
            for ms, me, mlabel in merged_ranges:
                if mlabel in AGE_MAP and ms <= end and me >= start:
                    # 合并段与目标范围有足够重叠（重叠>=3年）才加入
                    overlap_start = max(ms, start)
                    overlap_end = min(me, end)
                    if overlap_end - overlap_start + 1 >= 3:
                        expanded_ages.add(mlabel)
            # 2. 添加5岁细段（明略标签），只加完全在范围内的段
            fine_ranges = [
                (15,17,"15-17"), (18,19,"18-19"), (20,24,"20-24"),
                (25,29,"25-29"), (30,34,"30-34"), (35,39,"35-39"),
                (40,44,"40-44"), (45,49,"45-49"), (50,54,"50-54"), (55,59,"55-59"),
            ]
            for fs, fe, flabel in fine_ranges:
                if flabel in AGE_MAP and fs >= start - 1 and fe <= end + 1:
                    # 细段与目标范围有实质重叠
                    if fs <= end and fe >= start:
                        expanded_ages.add(flabel)
    # 去重并添加查询词
    for age_key in sorted(expanded_ages):
        if age_key in AGE_MAP:
            add(AGE_MAP[age_key])

    # 3. 城市级别查询词（兼容 city_level 和 city_tier 字段名，兼容列表和字符串）
    city_raw = loc.get("city_level", []) or loc.get("city_tier", []) or []
    if isinstance(city_raw, str):
        city_list = [city_raw]
    else:
        city_list = list(city_raw)
    for city_key in city_list:
        if city_key in CITY_MAP:
            add(CITY_MAP[city_key])
        else:
            add([city_key])

    # 4. 兴趣查询词（核心关键词直接使用+同义词扩展，不硬编码行业知识）
    for kw in interest:
        if not kw or not str(kw).strip():
            continue
        kw_str = str(kw).strip()
        if kw_str in INTEREST_EXPAND:
            add(INTEREST_EXPAND[kw_str])
        else:
            add([kw_str])
            # 自动补充常见变体：不加"儿"/加"儿"、去后缀等
            if not kw_str.endswith("儿") and len(kw_str) >= 2:
                pass  # 不自动扩展避免噪声，依赖TF-IDF语义匹配兜底

    # 4.5 从raw_text中提取有意义的中文2~4字词作为补充查询词
    # 这使得脚本对任意行业都能工作，不依赖硬编码行业扩展表
    raw_text = schema.get("_raw_text", "")
    if raw_text:
        # 提取连续中文词（2~4字），过滤通用停用词
        stop_words = {"的", "了", "是", "在", "和", "与", "或", "及", "等", "为", "对",
                      "把", "被", "让", "给", "向", "从", "到", "以", "而", "但", "也",
                      "都", "就", "又", "再", "还", "能", "会", "要", "有", "没", "不",
                      "这个", "那个", "什么", "怎么", "为什么", "哪", "谁", "多少",
                      "投放", "覆盖", "核心", "最好", "比较", "最近", "这次", "主要",
                      "想", "做", "需要", "可以", "一个", "一些", "一批", "产品",
                      "扩新", "拉新", "活跃", "核心覆盖", "这次", "主要是", "比较"}
        # 提取所有连续中文字符段
        chinese_segments = re.findall(r'[\u4e00-\u9fff]{2,6}', raw_text)
        for seg in chinese_segments:
            if seg not in stop_words and len(seg) >= 2 and seg not in seen:
                # 跳过纯描述性词汇（"扩新""拉新""活跃"已在结构化字段处理）
                if seg in ("扩新", "拉新", "活跃", "投放", "覆盖", "核心", "一线城市"):
                    continue
                # 只添加有定向价值的词（不是动词/形容词/副词）
                # 简化策略：2-4字词且不是停用词就添加，TF-IDF会自然过滤掉泛词
                if 2 <= len(seg) <= 4:
                    add([seg])

    # 5. 活跃度查询词
    active_window = activity.get("active_window", "")
    if active_window and active_window in ACTIVE_MAP:
        add(ACTIVE_MAP[active_window])

    # 6. 如果提供了同义词映射表，且Schema中有模糊词命中了synonyms，补充扩展词
    if synonyms_map:
        raw_text = schema.get("_raw_text", "")
        if raw_text:
            for item in synonyms_map.get("items", []):
                trigger = item.get("trigger", "")
                if trigger in raw_text:
                    expand_terms = item.get("expand_terms", [])
                    add(expand_terms)

    # boost_words：所有query词都作为boost词（确定性，无额外挑选）
    # 但过滤掉太短（<2字符）或太泛的词
    boost_words = [q for q in queries if len(q) >= 2]

    # 确定性排序：按长度降序→字典序升序（保证相同元素永远相同顺序）
    queries.sort(key=lambda x: (-len(x), x))
    boost_words.sort(key=lambda x: (-len(x), x))

    schema_str = json.dumps(schema, sort_keys=True, ensure_ascii=False)
    queries_str = "|".join(queries)

    return {
        "queries": queries,
        "boost_words": boost_words,
        "query_count": len(queries),
        "boost_count": len(boost_words),
        "query_hash": md5_str(queries_str),
        "schema_hash": md5_str(schema_str),
    }


def main():
    ap = argparse.ArgumentParser(description="根据Schema确定性生成标签召回的query列表和boost-words")
    ap.add_argument("--schema", required=True, help="Schema JSON文件路径")
    ap.add_argument("--synonyms", default=None, help="synonyms_map.json路径（可选，用于模糊词扩展）")
    ap.add_argument("--out", required=True, help="输出文件路径")
    args = ap.parse_args()

    schema = json.load(open(args.schema, "r", encoding="utf-8"))
    synonyms_map = None
    if args.synonyms:
        synonyms_map = json.load(open(args.synonyms, "r", encoding="utf-8"))

    result = build_queries_from_schema(schema, synonyms_map)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "ok": True,
        "query_count": result["query_count"],
        "boost_count": result["boost_count"],
        "query_hash": result["query_hash"],
        "schema_hash": result["schema_hash"],
        "out": args.out,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
