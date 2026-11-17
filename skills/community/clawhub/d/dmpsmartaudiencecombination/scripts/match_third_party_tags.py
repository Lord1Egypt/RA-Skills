#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""match_third_party_tags.py

Step 6.5 三方标签匹配脚本。
基于Schema中的关键词（行业/品类/兴趣/行为/消费力/城市等）在三方标签离线表中匹配推荐标签。

三方标签说明：
- 不参与DMP接口圈选（不进入MUST/PREFERRED/OPTIONAL/EXCLUDE）
- 仅作为推荐展示，引导用户申请开通
- 数据源：assets/third_party_tags.json

用法：
  python3 scripts/match_third_party_tags.py \
    --tp-tags assets/third_party_tags.json \
    --schema data/run/schema.json \
    --out data/run/third_party_matches.json
"""

import argparse
import json
import re
from typing import Dict, List, Any, Set, Tuple


# 通用停用词（避免匹配到无意义词）
STOP_WORDS = {
    "的", "了", "是", "在", "和", "与", "或", "及", "等", "为", "对",
    "把", "被", "让", "给", "向", "从", "到", "以", "而", "但", "也",
    "都", "就", "又", "再", "还", "能", "会", "要", "有", "没", "不",
    "投放", "覆盖", "核心", "最好", "比较", "最近", "这次", "主要",
    "想", "做", "需要", "可以", "一个", "一些", "一批", "产品",
    "圈", "想圈", "人", "人群", "批", "好", "点", "好点", "买好点",
    "平时", "爱买", "喜欢", "主要在", "大城市", "城市",
    "拉新", "扩新", "活跃", "新客", "老客",
}

# 结构化维度→关键词映射（从Schema结构化字段提取，比raw_text更精准）
DIMENSION_KW_MAP = {
    "gender": {
        "女": ["女性", "女", "女士", "妈妈", "宝妈", "她", "少女", "女生"],
        "男": ["男性", "男", "男士", "爸爸", "他", "男生", "男孩"],
    },
    "age": [],  # 年龄不直接匹配三方标签
    "city_tier": {
        "一线": ["一线城市", "一线", "北上广深"],
        "新一线": ["新一线城市", "新一线"],
        "二线": ["二线城市", "二线"],
    },
    "interest": [],  # 动态提取
    "consumption": {
        "高消费": ["高消费", "轻奢", "高端", "奢侈品", "高收入", "买好", "好点的"],
        "中高消费": ["中高消费", "轻奢", "高端"],
    },
    "industry": [],  # 动态提取
    "category": [],  # 动态提取
}


def _extract_schema_keywords(schema: Dict) -> Set[str]:
    """从Schema中提取所有有意义的关键词（结构化字段+raw_text分词）"""
    keywords = set()

    demos = schema.get("demographics", {}) or {}
    loc = schema.get("location", {}) or {}
    interest = schema.get("interest", {}) or {}
    consumption = schema.get("consumption", {}) or {}

    # 性别关键词
    gender = str(demos.get("gender", "")).strip().lower()
    if gender in ("女", "female", "f"):
        keywords.update(DIMENSION_KW_MAP["gender"]["女"])
    elif gender in ("男", "male", "m"):
        keywords.update(DIMENSION_KW_MAP["gender"]["男"])

    # 城市级别
    city_raw = loc.get("city_level") or loc.get("city_tier") or []
    if isinstance(city_raw, str):
        city_raw = [city_raw]
    if isinstance(city_raw, list):
        city_map = DIMENSION_KW_MAP["city_tier"]
        for c in city_raw:
            c = str(c).strip()
            if c in city_map:
                keywords.update(city_map[c])

    # 兴趣关键词（core + other）
    core_interest = interest.get("core", []) or []
    other_interest = interest.get("other", []) or []
    if isinstance(core_interest, dict):
        core_interest = core_interest.get("core", []) or []
    for kw in list(core_interest) + list(other_interest):
        if kw and str(kw).strip():
            keywords.add(str(kw).strip())

    # 行业/品类
    industry = schema.get("industry", "")
    category = schema.get("category", "")
    if industry:
        keywords.add(str(industry).strip())
    if category:
        keywords.add(str(category).strip())
        # 品类分词
        for seg in re.findall(r'[\u4e00-\u9fff]{2,6}', str(category)):
            if seg not in STOP_WORDS and len(seg) >= 2:
                keywords.add(seg)

    # 消费力
    cons_level = str(consumption.get("level", "")).strip()
    cons_map = DIMENSION_KW_MAP["consumption"]
    if cons_level in cons_map:
        keywords.update(cons_map[cons_level])
    for k, v in cons_map.items():
        if cons_level and k in cons_level:
            keywords.update(v)

    # raw_text中提取2-4字中文词（补漏）
    raw_text = schema.get("_raw_text", "")
    if raw_text:
        for seg in re.findall(r'[\u4e00-\u9fff]{2,4}', raw_text):
            if seg not in STOP_WORDS and len(seg) >= 2:
                # 过滤分词边界噪声（如"主要在一""买好点""圈精致宝"等）
                # 只保留有实际语义的词（在关键词索引或明确的行业词中）
                if seg.endswith("的") or seg.endswith("在") or seg.endswith("是"):
                    continue
                if seg.startswith("圈") or seg.startswith("买") or seg.startswith("想"):
                    continue
                keywords.add(seg)

    # 移除停用词
    keywords = {kw for kw in keywords if kw and kw not in STOP_WORDS and len(kw) >= 2}
    # 移除子串误匹配词（如"一线"会误匹配"二线/三线/新一线"，需要精确匹配）
    # 保留完整的"一线城市"而非单独"一线"（"一线"单独太泛）
    keywords.discard("一线")
    keywords.discard("二线")
    keywords.discard("三线")
    return keywords


def _match_ott_tag(tag: Dict, keywords: Set[str]) -> Tuple[bool, str]:
    """匹配OTT标签（l1/l2/l3三级结构）"""
    l1 = tag.get("l1", "")
    l2 = tag.get("l2", "")
    l3 = tag.get("l3") or ""
    full = f"{l1} {l2} {l3}"
    for kw in keywords:
        # 城市等级精确匹配：避免"一线"误匹配"二线/三线/新一线"
        if "城市" in kw or "线" in kw:
            if kw in full and not any(
                false_kw in full and kw in false_kw and kw != false_kw
                for false_kw in ["新一线城市", "二线城市", "三线城市", "四线城市", "新一线", "二线", "三线", "四线"]
            ):
                return True, f"{l1}-{l2}" + (f"/{l3}" if l3 else "")
        elif kw in full:
            return True, f"{l1}-{l2}" + (f"/{l3}" if l3 else "")
    return False, ""


def _match_jumu_tag(tag: Dict, keywords: Set[str]) -> Tuple[bool, str]:
    """匹配剧目偏好标签"""
    cat = tag.get("category", "")
    tname = tag.get("tag", "")
    full = f"{cat} {tname}"
    for kw in keywords:
        if kw in full:
            return True, f"{cat}-{tname}"
    return False, ""


def _match_travel_tag(tag: Dict, keywords: Set[str]) -> Tuple[bool, str]:
    """匹配OTA出行标签"""
    platform = tag.get("platform", "")
    scene = tag.get("scene", "")
    action = tag.get("action", "")
    full = f"{platform} {scene} {action}"
    for kw in keywords:
        if kw in full:
            return True, f"{platform}-{scene}({action})"
    return False, ""


def _match_jd_category(cat_name: str, subcats: Dict, keywords: Set[str], path: str = "") -> List[Dict]:
    """递归匹配京东品类标签（支持多级嵌套）"""
    matches = []
    current_path = f"{path}/{cat_name}" if path else cat_name

    # 检查当前品类名
    cat_match = False
    match_reason = ""
    for kw in keywords:
        if kw in cat_name:
            cat_match = True
            match_reason = kw
            break

    if cat_match:
        # 列出子品类摘要（最多5个）
        sub_summary = []
        if isinstance(subcats, dict):
            for sk, sv in list(subcats.items())[:6]:
                if isinstance(sv, list):
                    sub_summary.append(f"{sk}({len(sv)}项)")
                elif isinstance(sv, dict):
                    sub_summary.append(sk)
                else:
                    sub_summary.append(str(sk))
        matches.append({
            "source_key": "jd",
            "source_name": "京东品类标签",
            "tag_name": cat_name,
            "match_reason": f'关键词"{match_reason}"命中',
            "path": current_path,
            "sub_categories": sub_summary,
            "desc": f"京东品类-{cat_name}" + (f"，含{len(subcats)}个子类" if isinstance(subcats,dict) else ""),
        })

    # 递归子品类
    if isinstance(subcats, dict):
        for sub_name, sub_items in subcats.items():
            # 子品类名直接匹配
            sub_match = False
            sub_reason = ""
            for kw in keywords:
                if kw in sub_name:
                    sub_match = True
                    sub_reason = kw
                    break
            if sub_match:
                sub_path = f"{current_path}/{sub_name}"
                items_preview = []
                if isinstance(sub_items, list):
                    items_preview = sub_items[:5]
                matches.append({
                    "source_key": "jd",
                    "source_name": "京东品类标签",
                    "tag_name": sub_name,
                    "match_reason": f'关键词"{sub_reason}"命中',
                    "path": sub_path,
                    "sub_categories": items_preview if items_preview else [],
                    "desc": f"京东品类-{sub_name}",
                })
            # 三级标签匹配（叶子节点是list时）
            if isinstance(sub_items, list):
                for item in sub_items:
                    item_str = str(item)
                    for kw in keywords:
                        if kw in item_str:
                            matches.append({
                                "source_key": "jd",
                                "source_name": "京东品类标签",
                                "tag_name": item_str,
                                "match_reason": f'关键词"{kw}"命中',
                                "path": f"{current_path}/{sub_name}/{item_str}",
                                "sub_categories": [],
                                "desc": f"京东品类-{sub_name}-{item_str}",
                            })
                            break
            elif isinstance(sub_items, dict):
                matches.extend(_match_jd_category(sub_name, sub_items, keywords, current_path))

    return matches


def match_third_party_tags(tp_data: Dict, schema: Dict) -> Dict:
    """执行三方标签匹配，返回按来源分组的匹配结果"""
    keywords = _extract_schema_keywords(schema)
    catalog = tp_data.get("catalog", {})
    meta = tp_data.get("_meta", {})
    apply_url = meta.get("apply_url", "")

    results = {
        "apply_url": apply_url,
        "total_matches": 0,
        "matched_sources": [],
        "matches_by_source": {},
        "matched_keywords": sorted(list(keywords)),
    }

    # 1) OTT标签匹配
    ott_matches = []
    ott_catalog = catalog.get("miaozhen_ott", {})
    for tag in ott_catalog.get("tags", []):
        matched, label = _match_ott_tag(tag, keywords)
        if matched:
            ott_matches.append({"tag_name": label, "raw": tag})
    if ott_matches:
        results["matches_by_source"]["miaozhen_ott"] = {
            "source_name": "秒针OTT标签",
            "desc": "OTT端家庭结构/行业偏好/媒体偏好/城市等级标签",
            "tags": ott_matches,
        }
        results["matched_sources"].append("miaozhen_ott")

    # 2) 剧目偏好匹配
    jumu_matches = []
    jumu_catalog = catalog.get("miaozhen_jumu", {})
    for tag in jumu_catalog.get("tags", []):
        matched, label = _match_jumu_tag(tag, keywords)
        if matched:
            jumu_matches.append({"tag_name": label, "raw": tag})
    if jumu_matches:
        results["matches_by_source"]["miaozhen_jumu"] = {
            "source_name": "秒针剧目偏好标签",
            "desc": "动漫/电视剧/综艺节目的剧目内容偏好标签",
            "tags": jumu_matches,
        }
        results["matched_sources"].append("miaozhen_jumu")

    # 3) OTA出行匹配
    travel_matches = []
    travel_catalog = catalog.get("travel", {})
    for tag in travel_catalog.get("tags", []):
        matched, label = _match_travel_tag(tag, keywords)
        if matched:
            travel_matches.append({"tag_name": label, "raw": tag})
    if travel_matches:
        results["matches_by_source"]["travel"] = {
            "source_name": "出行旅游类标签（OTA）",
            "desc": "去哪儿/艺龙/同程/携程/途牛的酒店/旅游浏览与下单行为标签",
            "tags": travel_matches,
        }
        results["matched_sources"].append("travel")

    # 4) 京东品类匹配（递归）
    jd_matches = []
    jd_catalog = catalog.get("jd", {})
    jd_cats = jd_catalog.get("categories", {})
    for cat_name, subcats in jd_cats.items():
        jd_matches.extend(_match_jd_category(cat_name, subcats, keywords))
    # 去重（按path）
    seen_paths = set()
    unique_jd = []
    for m in jd_matches:
        p = m["path"]
        if p not in seen_paths:
            seen_paths.add(p)
            unique_jd.append(m)
    # 排序：路径短的（品类级别高的）在前
    unique_jd.sort(key=lambda x: (x["path"].count("/"), x["tag_name"]))
    if unique_jd:
        results["matches_by_source"]["jd"] = {
            "source_name": "京东品类标签",
            "desc": "京东全品类电商标签（57个一级品类，覆盖浏览/加购/购买等行为维度）",
            "tags": unique_jd,
        }
        results["matched_sources"].append("jd")

    results["total_matches"] = sum(
        len(s["tags"]) for s in results["matches_by_source"].values()
    )
    return results


def format_matches_text(result: Dict) -> str:
    """将匹配结果格式化为用户可读的文本"""
    lines = []
    lines.append("📎 除了上述可供圈选的标签，以下三方标签也符合您的需求，如有需要请填写链接申请哦~\n")
    lines.append("【匹配到的三方标签】\n")

    for src_key in result.get("matched_sources", []):
        src = result["matches_by_source"][src_key]
        lines.append(f"**{src['source_name']}**：{src['desc']}")
        for tag in src["tags"][:10]:  # 每个来源最多展示10个
            name = tag["tag_name"]
            reason = tag.get("match_reason", "")
            sub = tag.get("sub_categories", [])
            sub_str = ""
            if sub:
                sub_str = f"（含：{'、'.join(sub[:5])}{'…' if len(sub)>5 else ''}）"
            lines.append(f"   • {name}{sub_str}")
        if len(src["tags"]) > 10:
            lines.append(f"   • ……等共{len(src['tags'])}个相关标签")
        lines.append("")

    lines.append(f"🔗 申请链接：{result.get('apply_url','')}")
    lines.append("⚠️ 三方标签不可直接用于本次圈选组合，仅作为额外数据申请参考。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Step 6.5 三方标签匹配")
    ap.add_argument("--tp-tags", required=True, help="三方标签JSON路径(assets/third_party_tags.json)")
    ap.add_argument("--schema", required=True, help="Schema JSON路径")
    ap.add_argument("--out", required=True, help="输出匹配结果JSON")
    args = ap.parse_args()

    with open(args.tp_tags, "r", encoding="utf-8") as f:
        tp_data = json.load(f)
    with open(args.schema, "r", encoding="utf-8") as f:
        schema = json.load(f)

    result = match_third_party_tags(tp_data, schema)
    result["ok"] = True

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 输出摘要
    summary = {
        "ok": True,
        "total_matches": result["total_matches"],
        "matched_sources": result["matched_sources"],
        "matched_keywords": result["matched_keywords"],
        "out": args.out,
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
