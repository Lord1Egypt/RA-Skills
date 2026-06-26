#!/usr/bin/env python3
"""
Amazon Listing Analyzer - handler.py
不依赖实时API，所有数据来自内置规则库和模板。
"""

import json
import re
from typing import Dict, List, Any, Optional

# ============================================================
# 内置数据：关键词数据库（模拟，非实时数据）
# ============================================================

KEYWORD_DB: Dict[str, Dict[str, str]] = {
    "wireless headphones": {"volume": "High", "competition": "High", "relevance": "5"},
    "bluetooth headphones": {"volume": "High", "competition": "High", "relevance": "5"},
    "noise cancelling headphones": {"volume": "High", "competition": "Medium", "relevance": "4"},
    "noise cancellation headphones": {"volume": "High", "competition": "Medium", "relevance": "4"},
    "headphones": {"volume": "High", "competition": "High", "relevance": "5"},
    "earphones": {"volume": "High", "competition": "High", "relevance": "4"},
    "long battery life headphones": {"volume": "Medium", "competition": "Low", "relevance": "4"},
    "comfortable headphones": {"volume": "Medium", "competition": "Medium", "relevance": "3"},
    "gaming headphones": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "sports headphones": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "waterproof headphones": {"volume": "Medium", "competition": "Low", "relevance": "4"},
    "over ear headphones": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "on ear headphones": {"volume": "Medium", "competition": "Medium", "relevance": "3"},
    "portable speakers": {"volume": "High", "competition": "High", "relevance": "5"},
    "bluetooth speaker": {"volume": "High", "competition": "High", "relevance": "5"},
    "smart watch": {"volume": "High", "competition": "High", "relevance": "5"},
    "fitness tracker": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "running shoes": {"volume": "High", "competition": "High", "relevance": "5"},
    "casual shoes": {"volume": "High", "competition": "High", "relevance": "4"},
    "laptop stand": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "phone case": {"volume": "High", "competition": "High", "relevance": "5"},
    "charging cable": {"volume": "High", "competition": "High", "relevance": "5"},
    "usb cable": {"volume": "High", "competition": "High", "relevance": "5"},
    "power bank": {"volume": "High", "competition": "High", "relevance": "5"},
    "external battery": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "wireless charger": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "desk lamp": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "led lamp": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "kitchen knife": {"volume": "Medium", "competition": "Medium", "relevance": "4"},
    "cooking pot": {"volume": "Medium", "competition": "Low", "relevance": "4"},
}

# 禁止词/过敏词库
FORBIDDEN_WORDS = [
    "fake", "replica", "knockoff", "counterfeit", "clone",
    "miracle", "cure", "treats", "heals", "prevents disease",
    ".weight loss", "lose weight", "burn fat",
    "best", "top rated", "number 1", "#1", "most popular",
]

# 竞品模板库
COMPETITOR_TEMPLATES = {
    "B00XXXXXXXX": {
        "title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones",
        "price_range": "$300-$350", "rating": "4.7", "reviews": "50000+",
        "core_features": ["Industry-leading noise cancellation", "30hr battery", "Multipoint connection"],
    },
    "B0BYXXXXXXXX": {
        "title": "Apple AirPods Pro 2nd Gen",
        "price_range": "$220-$250", "rating": "4.8", "reviews": "100000+",
        "core_features": ["Active noise cancellation", "Adaptive transparency", "Personalized spatial audio"],
    },
    "B09JQMJXYZ": {
        "title": "Bose QuietComfort 45",
        "price_range": "$270-$300", "rating": "4.6", "reviews": "30000+",
        "core_features": ["QuietComfort technology", "24hr battery", "Lightweight design"],
    },
}


# ============================================================
# 核心分析模块
# ============================================================

def score_title(title: str) -> Dict[str, Any]:
    """评估标题质量"""
    issues = []
    score = 80  # 基准分

    if not title:
        return {"score": 0, "issues": ["标题为空"]}

    title_len = len(title)
    if title_len < 50:
        score -= 20
        issues.append("标题过短（<50字符），建议80-200字符")
    elif title_len > 200:
        score -= 10
        issues.append("标题过长（>200字符），可能被截断")

    words = title.split()
    if len(words) < 5:
        score -= 15
        issues.append("标题词数过少")

    # 品牌词检测
    if title and title[0].isupper() and len(title.split()[0]) > 2:
        pass  # 首词大写通常是品牌词，正常
    else:
        score -= 5
        issues.append("标题可能缺少品牌词或品牌词位置不规范")

    # 关键词覆盖（简单检测）
    title_lower = title.lower()
    if "headphone" not in title_lower and "earphone" not in title_lower and "earbud" not in title_lower:
        score -= 10
        issues.append("标题缺少产品核心词（headphone/earphone/earbud）")

    score = max(0, min(100, score))
    return {"score": score, "issues": issues}


def score_bullets(bullets: List[str]) -> Dict[str, Any]:
    """评估五点描述质量"""
    issues = []
    score = 80

    if not bullets:
        return {"score": 0, "issues": ["五点描述为空"]}

    count = len(bullets)
    if count < 5:
        score -= (5 - count) * 8
        issues.append(f"五点描述不完整（{count}/5）")

    for i, bullet in enumerate(bullets):
        blen = len(bullet)
        if blen < 20:
            score -= 3
            issues.append(f"第{i+1}条卖点过短（<20字符），缺乏信息量")
        if blen > 500:
            score -= 5
            issues.append(f"第{i+1}条卖点过长（>500字符）")

    score = max(0, min(100, score))
    return {"score": score, "issues": issues}


def score_description(description: str) -> Dict[str, Any]:
    """评估产品描述质量"""
    issues = []
    score = 70

    if not description:
        return {"score": 0, "issues": ["产品描述为空"]}

    dlen = len(description)
    if dlen < 100:
        score -= 15
        issues.append("描述过短（<100字符），缺少品牌故事和使用场景")
    elif dlen > 2000:
        score -= 5
        issues.append("描述过长（>2000字符），可能包含过多冗余信息")

    # 段落结构检测
    sentences = re.split(r'[.\n]', description)
    if len(sentences) < 3:
        score -= 10
        issues.append("描述缺少段落结构，建议分段说明产品特点和使用场景")

    score = max(0, min(100, score))
    return {"score": score, "issues": issues}


def score_keywords(search_terms: str, backend: str) -> Dict[str, Any]:
    """评估关键词填充"""
    issues = []
    score = 75

    total = (search_terms or "") + (backend or "")
    if not total.strip():
        return {"score": 0, "issues": ["Search Terms 和 Backend Keywords 均为空"]}

    words = total.split()
    word_count = len(words)

    if word_count < 5:
        score -= 15
        issues.append("Search Terms 关键词数量不足（<5个）")
    elif word_count > 250:
        score -= 10
        issues.append("Backend Keywords 词数过多（>250）")

    # 重复检测
    seen = set()
    duplicates = []
    for w in words[:50]:  # 只检查前50个词
        wl = w.lower()
        if wl in seen:
            duplicates.append(w)
        seen.add(wl)
    if duplicates:
        score -= 5
        issues.append(f"存在重复关键词: {', '.join(set(duplicates))}")

    score = max(0, min(100, score))
    return {"score": score, "issues": issues}


def score_compliance(title: str, bullets: List[str], description: str) -> Dict[str, Any]:
    """合规性检查"""
    issues = []
    score = 100

    all_text = title + " " + " ".join(bullets) + " " + description
    all_lower = all_text.lower()

    for word in FORBIDDEN_WORDS:
        if word in all_lower:
            score -= 15
            issues.append(f"发现禁止词/违规词: '{word}'")

    score = max(0, min(100, score))
    return {"score": score, "issues": issues}


def health_score(input_data: Dict) -> Dict:
    """Listing健康度评分"""
    title = input_data.get("product_title", "")
    bullets = input_data.get("bullet_points", [])
    description = input_data.get("product_description", "")
    search_terms = input_data.get("search_terms", "")
    backend = input_data.get("backend_keywords", "")

    title_result = score_title(title)
    bullets_result = score_bullets(bullets)
    desc_result = score_description(description)
    kw_result = score_keywords(search_terms, backend)
    comp_result = score_compliance(title, bullets, description)

    # 加权平均
    weights = {"title": 0.25, "bullets": 0.25, "description": 0.20, "keywords": 0.15, "compliance": 0.15}
    total = (
        title_result["score"] * weights["title"] +
        bullets_result["score"] * weights["bullets"] +
        desc_result["score"] * weights["description"] +
        kw_result["score"] * weights["keywords"] +
        comp_result["score"] * weights["compliance"]
    )
    total = round(total)

    if total >= 80:
        summary = "Listing 健康度良好，各项指标达标，继续保持优化节奏。"
    elif total >= 60:
        summary = "Listing 健康度中等偏上，主要改进空间在标题关键词精准度和五点描述的具体性。"
    elif total >= 40:
        summary = "Listing 健康度偏低，需要系统性优化标题、五点描述和关键词布局。"
    else:
        summary = "Listing 健康度较差，建议优先完善基础信息（标题+五点），再逐步优化其他维度。"

    return {
        "total": total,
        "dimensions": {
            "title": title_result,
            "bullets": bullets_result,
            "description": desc_result,
            "keywords": kw_result,
            "compliance": comp_result,
        },
        "summary": summary,
    }


def keyword_analysis(input_data: Dict) -> Dict:
    """关键词分析"""
    features = input_data.get("product_features", [])
    category = input_data.get("product_category", "")
    title = input_data.get("product_title", "")
    bullets = input_data.get("bullet_points", [])

    # 生成种子关键词
    seed_keywords = set()

    # 从features提取
    for f in features:
        seed_keywords.add(f.lower().strip())
        if "headphone" in f.lower() or "speaker" in f.lower() or "watch" in f.lower():
            seed_keywords.add(f"{f.lower()}".replace(" ", " ").strip())

    # 从category提取核心词
    if category:
        cat_words = re.findall(r'\b\w+\b', category.lower())
        for w in cat_words:
            if len(w) > 3:
                seed_keywords.add(w)

    # 从title/bullets提取
    all_text = title + " " + " ".join(bullets)
    for word in re.findall(r'\b[a-z]+\b', all_text.lower()):
        if len(word) > 3:
            seed_keywords.add(word)

    # 查询内置DB
    matrix = []
    priority = []
    long_tail = []

    for kw in sorted(seed_keywords):
        if kw in KEYWORD_DB:
            info = KEYWORD_DB[kw]
            matrix.append({
                "keyword": kw,
                "volume": info["volume"],
                "competition": info["competition"],
                "relevance": int(info["relevance"]),
            })
            if int(info["relevance"]) >= 4 and info["volume"] in ("High", "Medium"):
                priority.append(kw)
        else:
            # 模糊匹配
            for db_kw, info in KEYWORD_DB.items():
                if kw in db_kw or db_kw in kw:
                    matrix.append({
                        "keyword": db_kw,
                        "volume": info["volume"],
                        "competition": info["competition"],
                        "relevance": int(info["relevance"]) - 1,
                    })
                    break
            else:
                matrix.append({
                    "keyword": kw,
                    "volume": "Unknown",
                    "competition": "Unknown",
                    "relevance": 2,
                })

    # 生成long-tail
    if len(priority) >= 2:
        long_tail.append(f"{priority[0]} {priority[1]}")
    if len(features) >= 1:
        long_tail.append(f"{features[0].lower()} headphones")

    # 去重
    priority = list(dict.fromkeys(priority))[:10]
    matrix = matrix[:20]

    return {
        "matrix": matrix,
        "priority_keywords": priority,
        "long_tail_keywords": long_tail,
    }


def competitor_benchmark(input_data: Dict) -> Dict:
    """竞品对标分析"""
    competitor_asin = input_data.get("competitor_asin", "")
    product_title = input_data.get("product_title", "")
    bullets = input_data.get("bullet_points", [])

    # 匹配竞品
    competitor = COMPETITOR_TEMPLATES.get(competitor_asin, {
        "title": "某头部竞品（ASIN: " + competitor_asin + "）",
        "price_range": "$50-$200",
        "rating": "4.5",
        "reviews": "10000+",
        "core_features": ["知名品牌", "稳定评分", "大量真实评论"],
    })

    comparisons = [
        {
            "dimension": "标题结构",
            "you": product_title[:60] + "..." if len(product_title) > 60 else product_title,
            "competitor": competitor["title"],
            "opportunity": "参考竞品标题结构：品牌+核心词+特性+型号",
        },
        {
            "dimension": "价格区间",
            "you": "待定价（未提供）",
            "competitor": competitor["price_range"],
            "opportunity": "建议定价参考竞品区间，结合成本和毛利确定",
        },
        {
            "dimension": "评分",
            "you": "待积累（新品或无评分）",
            "competitor": f"{competitor['rating']} ({competitor['reviews']} 条评论)",
            "opportunity": "提升产品力和服务，争取更多高质量评论",
        },
        {
            "dimension": "核心卖点",
            "you": "; ".join(bullets[:3]) if bullets else "待完善",
            "competitor": "; ".join(competitor["core_features"][:3]),
            "opportunity": "提炼差异化卖点，避免同质化",
        },
    ]

    gaps = [
        "缺少竞品评分和评论数对比数据（需手动调研）",
        "差异化卖点不够突出，建议结合用户痛点提炼",
        "标题关键词覆盖不如竞品全面",
    ]

    return {
        "comparisons": comparisons,
        "gaps": gaps,
    }


def full_optimization(input_data: Dict) -> Dict:
    """生成完整优化建议包"""
    health = health_score(input_data)
    keywords = keyword_analysis(input_data)

    title = input_data.get("product_title", "")
    bullets = input_data.get("bullet_points", [])
    description = input_data.get("product_description", "")

    # 标题优化
    title_suggested = title
    title_priority = "high"
    if health["dimensions"]["title"]["score"] < 75:
        title_suggested = f"{title} - Wireless, Premium Sound, Comfortable Fit" if title else "[品牌词] [核心产品词] [特性词] [型号/规格]"
        title_priority = "high"
    elif health["dimensions"]["title"]["score"] < 90:
        title_suggested = f"{title} [增强关键词]" if title else title
        title_priority = "medium"
    else:
        title_priority = "low"

    # 五点优化
    bullet_suggestions = []
    for i, b in enumerate(bullets):
        suggested = b
        if len(b) < 30:
            suggested = f"{b} - [补充具体数据和功效描述]"
        bullet_suggestions.append({
            "current": b,
            "suggested": suggested,
            "priority": "high" if len(b) < 30 else "medium",
        })

    while len(bullet_suggestions) < 5:
        bullet_suggestions.append({
            "current": "",
            "suggested": "[新增卖点：具体化数字/功效/场景]",
            "priority": "high",
        })

    # 描述优化
    desc_suggested = description
    desc_priority = "low"
    if health["dimensions"]["description"]["score"] < 70:
        desc_suggested = (
            f"{description}\n\n"
            "[品牌故事段落]\n"
            "[使用场景描述]\n"
            "[产品保修/售后信息]"
        )
        desc_priority = "high"

    # 关键词建议
    missing = [kw["keyword"] for kw in keywords["matrix"] if kw["volume"] == "Unknown"]
    redundant = []
    suggested_kws = keywords["priority_keywords"][:5]

    return {
        "title": {"current": title, "suggested": title_suggested, "priority": title_priority},
        "bullets": bullet_suggestions,
        "description": {"current": description, "suggested": desc_suggested, "priority": desc_priority},
        "keywords": {
            "missing": missing[:5],
            "redundant": redundant,
            "suggested": suggested_kws,
        },
    }


# ============================================================
# 入口函数
# ============================================================

def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    主分析入口，根据 intent 分派到对应模块。
    """
    # 输入长度校验
    raw_str = json.dumps(input_data, ensure_ascii=False)
    if len(raw_str) > 10000:
        return {
            "status": "error",
            "module": "input_validation",
            "result": {},
            "errors": [f"输入数据过长（{len(raw_str)}字符），超过10000字符限制"],
        }

    intent = input_data.get("intent", "")

    if intent == "health_score":
        module = "health_score"
        result = {"health_score": health_score(input_data)}
    elif intent == "keyword_analysis":
        module = "keyword_analysis"
        result = {"keyword_analysis": keyword_analysis(input_data)}
    elif intent == "competitor_benchmark":
        module = "competitor_benchmark"
        result = {"competitor_benchmark": competitor_benchmark(input_data)}
    elif intent == "full_optimization":
        module = "full_optimization"
        result = {
            "health_score": health_score(input_data),
            "keyword_analysis": keyword_analysis(input_data),
            "competitor_benchmark": competitor_benchmark(input_data),
            "optimization_package": full_optimization(input_data),
        }
    else:
        # 默认执行健康度评分
        module = "health_score"
        result = {"health_score": health_score(input_data)}

    return {
        "status": "success",
        "module": module,
        "result": result,
    }


# ============================================================
# CLI 入口（自测）
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Amazon Listing Analyzer - 自测模式")
    print("=" * 60)

    # 测试用例1：健康度评分
    print("\n[Test 1] 健康度评分")
    test1 = {
        "intent": "health_score",
        "product_title": "Premium Wireless Bluetooth Headphones with Noise Cancellation",
        "bullet_points": [
            "High quality sound",
            "30-hour battery life",
            "Comfortable fit",
            "Fast charging",
            "Foldable design",
        ],
        "product_description": "Experience music like never before with our premium wireless headphones.",
        "search_terms": "wireless headphones bluetooth noise cancellation",
    }
    result1 = analyze(test1)
    print(json.dumps(result1, ensure_ascii=False, indent=2))

    # 测试用例2：关键词分析
    print("\n[Test 2] 关键词分析")
    test2 = {
        "intent": "keyword_analysis",
        "product_category": "Electronics > Headphones",
        "product_features": ["wireless", "noise cancellation", "bluetooth", "long battery life", "comfortable"],
    }
    result2 = analyze(test2)
    print(json.dumps(result2, ensure_ascii=False, indent=2))

    # 测试用例3：竞品对标
    print("\n[Test 3] 竞品对标")
    test3 = {
        "intent": "competitor_benchmark",
        "competitor_asin": "B00XXXXXXXX",
        "product_title": "Generic Brand Wireless Headphones",
        "bullet_points": ["Good sound", "10hr battery", "Lightweight"],
    }
    result3 = analyze(test3)
    print(json.dumps(result3, ensure_ascii=False, indent=2))

    # 测试用例4：完整优化
    print("\n[Test 4] 完整优化建议包")
    test4 = {
        "intent": "full_optimization",
        "product_title": "Wireless Headphones",
        "bullet_points": ["Good sound", "10hr battery"],
        "product_description": "Great headphones.",
        "search_terms": "headphones",
        "product_features": ["wireless", "bluetooth"],
    }
    result4 = analyze(test4)
    print(json.dumps(result4, ensure_ascii=False, indent=2))

    # 测试用例5：输入超长检测
    print("\n[Test 5] 输入超长校验")
    test5 = {"intent": "health_score", "product_title": "x" * 15000}
    result5 = analyze(test5)
    print(json.dumps(result5, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("自测完成，所有用例执行成功。")
    print("=" * 60)
