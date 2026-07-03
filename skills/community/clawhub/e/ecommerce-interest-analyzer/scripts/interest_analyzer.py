#!/usr/bin/env python3
"""
电商商品兴趣度分析引擎
- 多维度行为数据加权评分
- NLP文案质量分析
- 价格/文案/综合诊断
- 输出结构化分析结果 JSON
"""

import json
import math
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# ============================================================
# 数据模型
# ============================================================

@dataclass
class ProductData:
    product_id: str
    product_name: str
    product_price: float
    product_description: str
    category: str = ""
    # 行为数据 (聚合后的单条记录)
    view_count: int = 0
    view_duration_avg: float = 0.0  # 秒
    detail_page_view_rate: float = 0.0  # 0-1
    scroll_depth_avg: float = 0.0  # 0-100
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    add_to_cart_rate: float = 0.0  # 0-1
    favorite_rate: float = 0.0  # 0-1
    revisit_rate: float = 0.0  # 0-1
    purchase_rate: float = 0.0  # 0-1 (转化率)
    total_users: int = 0  # 样本量

@dataclass
class InterestScore:
    product_id: str
    total_score: float  # 0-100
    sub_scores: Dict[str, float] = field(default_factory=dict)
    interest_level: str = ""  # high/medium/low

@dataclass
class CopyAnalysis:
    product_id: str
    word_count: int
    keyword_density: Dict[str, float] = field(default_factory=dict)
    has_cta: bool = False  # Call to Action
    has_selling_point: bool = False
    sentiment_score: float = 0.0  # -1 to 1
    readability_score: float = 0.0  # 0-100
    suggestions: List[str] = field(default_factory=list)

@dataclass
class Diagnosis:
    product_id: str
    product_name: str
    interest_score: float
    interest_level: str
    conversion_rate: float
    primary_issue: str  # price/copy/both/none/comprehensive
    price_suggestion: str
    copy_suggestion: str
    action_priority: str  # price_first/copy_first/both/none
    confidence: float  # 0-1
    detailed_findings: List[str] = field(default_factory=list)


# ============================================================
# 行为数据标准化参数 (用于归一化)
# ============================================================

# 各维度最大参考值（超过此值按1处理）
NORM_PARAMS = {
    "view_count": 10000,
    "view_duration_avg": 120,  # 秒
    "like_count": 500,
    "comment_count": 100,
    "share_count": 200,
    "revisit_rate": 0.5,
}

# 各维度权重
WEIGHTS = {
    "view": 0.10,        # 浏览
    "duration": 0.20,    # 停留时长
    "detail": 0.10,      # 详情页
    "scroll": 0.10,      # 浏览深度
    "like": 0.10,        # 点赞
    "comment": 0.05,     # 评论
    "share": 0.10,       # 分享
    "cart": 0.15,        # 加购
    "favorite": 0.10,    # 收藏
    "revisit": 0.10,     # 复访
}


# ============================================================
# 兴趣度计算
# ============================================================

def normalize(value: float, max_val: float) -> float:
    """Min-Max归一化到 0-1"""
    if max_val <= 0:
        return 0.0
    return min(value / max_val, 1.0)


def calculate_interest_score(product: ProductData) -> InterestScore:
    """多维度加权计算兴趣度"""
    scores = {}

    scores["view"] = normalize(product.view_count, NORM_PARAMS["view_count"]) * 100
    scores["duration"] = normalize(product.view_duration_avg, NORM_PARAMS["view_duration_avg"]) * 100
    scores["detail"] = product.detail_page_view_rate * 100
    scores["scroll"] = product.scroll_depth_avg  # 已经是百分比
    scores["like"] = normalize(product.like_count, NORM_PARAMS["like_count"]) * 100
    scores["comment"] = normalize(product.comment_count, NORM_PARAMS["comment_count"]) * 100
    scores["share"] = normalize(product.share_count, NORM_PARAMS["share_count"]) * 100
    scores["cart"] = product.add_to_cart_rate * 100
    scores["favorite"] = product.favorite_rate * 100
    scores["revisit"] = normalize(product.revisit_rate, NORM_PARAMS["revisit_rate"]) * 100

    total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)

    # 确定兴趣等级
    if total >= 70:
        level = "high"
    elif total >= 40:
        level = "medium"
    else:
        level = "low"

    return InterestScore(
        product_id=product.product_id,
        total_score=round(total, 2),
        sub_scores={k: round(v, 2) for k, v in scores.items()},
        interest_level=level,
    )


# ============================================================
# 文案分析 (NLP)
# ============================================================

# 电商文案常用关键词/卖点词
SELLING_KEYWORDS = [
    "限时", "折扣", "爆款", "热卖", "新品", "独家", "专享",
    "正品", "保证", "售后", "包邮", "免费", "赠品", "买一送一",
    "品质", "精选", "高端", "性价比", "好评", "回购", "推荐",
    "限量", "秒杀", "特价", "清仓", "新品首发",
    "官方", "旗舰", "授权", "认证", "检测",
]

CTA_PATTERNS = [
    r"(立即|马上|赶快|赶紧|快快).*(购买|下单|抢购|入手)",
    r"点击.*(购买|链接|下单)",
    r"不要错过",
    r"数量有限",
    r"手慢无",
    r"错过.*等.*年",
]


def analyze_copy(text: str, product_id: str) -> CopyAnalysis:
    """文案质量NLP分析"""
    if not text:
        return CopyAnalysis(product_id=product_id, word_count=0)

    # 清洗文本
    clean_text = re.sub(r'<[^>]+>', '', text)
    clean_text = re.sub(r'\s+', '', clean_text)
    word_count = len(clean_text)

    # 关键词密度
    keywords_found = {}
    for kw in SELLING_KEYWORDS:
        count = text.count(kw)
        if count > 0:
            keywords_found[kw] = count / max(len(text), 1) * 1000  # 每千字密度

    # CTA检测
    has_cta = any(re.search(pattern, text) for pattern in CTA_PATTERNS)

    # 卖点检测
    has_selling_point = len(keywords_found) >= 3

    # 简易情感分析 (正向词 vs 负向词)
    positive_words = ["好", "赞", "棒", "完美", "优秀", "惊喜", "满意", "喜欢",
                      "超值", "划算", "好用", "实用", "方便", "舒适", "漂亮"]
    negative_words = ["差", "烂", "坑", "后悔", "失望", "不行", "垃圾", "差劲",
                      "不推荐", "不值", "难用", "麻烦"]

    pos_count = sum(text.count(w) for w in positive_words)
    neg_count = sum(text.count(w) for w in negative_words)

    total_sentiment = pos_count + neg_count + 1  # 避免除0
    sentiment_score = (pos_count - neg_count) / total_sentiment

    # 可读性评分 (基于句子长度)
    sentences = re.split(r'[。！？.!?\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        avg_len = sum(len(s) for s in sentences) / len(sentences)
        # 理想电商文案句子长度 15-30 字
        if 15 <= avg_len <= 30:
            readability = 90
        elif 10 <= avg_len <= 40:
            readability = 70
        else:
            readability = max(30, 100 - abs(avg_len - 22) * 3)
    else:
        readability = 50

    # 生成建议
    suggestions = []
    if word_count < 50:
        suggestions.append("文案过短（<50字），建议丰富商品描述，至少200字以上")
    if len(keywords_found) < 3:
        suggestions.append(f"卖点词覆盖不足（当前{len(keywords_found)}个），建议增加品质/优惠/稀缺性关键词")
    if not has_cta:
        suggestions.append("缺少行动号召（CTA），建议添加「立即购买」「限时抢购」等引导语")
    if sentiment_score < 0.1:
        suggestions.append("文案情感倾向偏负面或中性，建议增强正向描述")
    if readability < 60:
        suggestions.append("文案可读性偏低，建议优化句子长度，每条15-30字为佳")
    if word_count > 2000:
        suggestions.append("文案过长（>2000字），建议精简核心卖点，控制在500-1000字")

    return CopyAnalysis(
        product_id=product_id,
        word_count=word_count,
        keyword_density=keywords_found,
        has_cta=has_cta,
        has_selling_point=has_selling_point,
        sentiment_score=round(sentiment_score, 3),
        readability_score=round(readability, 1),
        suggestions=suggestions,
    )


# ============================================================
# 诊断引擎
# ============================================================

def diagnose(product: ProductData, interest: InterestScore, copy_analysis: CopyAnalysis) -> Diagnosis:
    """
    综合诊断：根据兴趣度和转化率判断核心问题
    """
    score = interest.total_score
    level = interest.interest_level
    conv = product.purchase_rate * 100  # 转为百分比

    # --- 诊断矩阵 ---
    findings = []
    primary_issue = "none"
    price_suggestion = ""
    copy_suggestion = ""
    action_priority = "none"
    confidence = 0.0

    if level == "high":
        if conv < 10:
            primary_issue = "price"
            price_suggestion = f"🔥 用户兴趣度极高（{score}分），但转化率仅{conv:.1f}%。强烈建议降价或设置限时优惠，当前价格 ¥{product.product_price:.2f} 可能是核心阻力。"
            copy_suggestion = "文案表现良好，无需大幅调整。"
            action_priority = "price_first"
            confidence = 0.85
            findings.append("高兴趣 + 低转化 → 典型的价格障碍")
            findings.append(f"建议降价幅度：参考同类竞品价格区间，可尝试降 10%-20% 测试")
            findings.append("也可采用「首单优惠」「满减券」等柔性降价策略")

        elif conv >= 10 and conv < 30:
            primary_issue = "copy"
            price_suggestion = f"当前价格 ¥{product.product_price:.2f} 基本合理，转化率 {conv:.1f}% 有提升空间。"
            copy_suggestion = "兴趣度高但转化中等，文案需要强化信任背书和紧迫感。增加用户评价/实拍图/限时优惠等元素。"
            action_priority = "copy_first"
            confidence = 0.70
            findings.append("高兴趣 + 中等转化 → 文案/信任问题")
            findings.append("建议：增加真实用户好评展示、权威认证标识、售后保障说明")
            findings.append("可尝试A/B测试不同文案版本")

        else:
            primary_issue = "none"
            price_suggestion = f"表现优秀！当前价格 ¥{product.product_price:.2f} 和转化率 {conv:.1f}% 均表现良好，无需调整。"
            copy_suggestion = "文案和策略表现良好，保持即可。"
            action_priority = "none"
            confidence = 0.90
            findings.append("高兴趣 + 高转化 → 商品表现优秀")

    elif level == "medium":
        if conv < 10:
            primary_issue = "both"
            price_suggestion = f"用户有一定兴趣（{score}分）但转化率低（{conv:.1f}%）。建议：先优化文案增强吸引力，再配合适度降价（¥{product.product_price - product.product_price * 0.1:.2f}）。"
            copy_suggestion = "文案需全面优化：增强卖点描述、添加CTA、补充信任元素。"
            action_priority = "both"
            confidence = 0.75
            findings.append("中等兴趣 + 低转化 → 综合问题，需同时优化文案和定价")
            findings.append("优先顺序：文案优化 → 观察1-2周 → 如果转化仍低，再降价")

        elif conv >= 10 and conv < 30:
            primary_issue = "copy"
            price_suggestion = f"价格 ¥{product.product_price:.2f} 基本合理，转化率 {conv:.1f}% 中等。"
            copy_suggestion = "建议重点优化文案：增加差异化卖点、强化场景化描述、提升内容质量。"
            action_priority = "copy_first"
            confidence = 0.65
            findings.append("中等兴趣 + 中等转化 → 文案仍有优化空间")
            findings.append("可尝试不同风格文案：故事型/数据型/痛点型，分别测试")

        else:
            primary_issue = "price"
            price_suggestion = f"兴趣度中等（{score}分）但转化率高（{conv:.1f}%），可能价格偏低。可考虑将价格上调至 ¥{product.product_price * 1.15:.2f} 测试利润空间。"
            copy_suggestion = "覆盖率尚可，如果提价需同步升级文案（增加高端感、品质感描述）。"
            action_priority = "price_first"
            confidence = 0.60
            findings.append("中等兴趣 + 高转化 → 价格可能偏低，有提价空间")
            findings.append("建议小幅提价（5%-15%）并监控转化率变化")

    else:  # level == "low"
        if conv < 5:
            primary_issue = "copy"
            price_suggestion = f"兴趣度低（{score}分），不是价格问题。即使降价可能也难以提升转化。"
            copy_suggestion = "文案吸引力严重不足，建议重新定位商品：调整标题、重写描述、更换头图/主图。"
            action_priority = "copy_first"
            confidence = 0.80
            findings.append("低兴趣 + 极低转化 → 商品选品或文案定位问题")
            findings.append("建议：重新审视目标用户画像，调整商品卖点和描述")
            findings.append("可考虑更换头图/主视频，用更吸引人的场景化展示")

        elif conv >= 5 and conv < 20:
            primary_issue = "copy"
            price_suggestion = f"转化率 {conv:.1f}% 在低兴趣商品中尚可，可能存在特定受众。"
            copy_suggestion = "建议重新包装商品：找到精准受众的痛点，用针对性文案触达。"
            action_priority = "copy_first"
            confidence = 0.55
            findings.append("低兴趣 + 中等转化 → 存在特定受众群体")
            findings.append("建议：定位细分人群，做精准文案")

        else:
            primary_issue = "price"
            price_suggestion = f"兴趣度低但转化率高（{conv:.1f}%），性价比可能是主要驱动力。可尝试小幅提价（¥{product.product_price * 1.05:.2f}）测试。"
            copy_suggestion = "文案需升级以匹配准备提价后的品牌调性。"
            action_priority = "price_first"
            confidence = 0.50
            findings.append("低兴趣 + 高转化 → 性价比驱动型商品")
            findings.append("提价需谨慎，建议搭配文案升级同步进行")

    # 合并文案分析的建议
    if copy_analysis.suggestions:
        findings.extend(copy_analysis.suggestions)

    # 样本量小则降低可信度
    if product.total_users < 100:
        confidence *= 0.7
        findings.append(f"⚠️ 样本量较小（{product.total_users}人），分析结果仅供参考")

    return Diagnosis(
        product_id=product.product_id,
        product_name=product.product_name,
        interest_score=score,
        interest_level=level,
        conversion_rate=round(conv, 2),
        primary_issue=primary_issue,
        price_suggestion=price_suggestion,
        copy_suggestion=copy_suggestion,
        action_priority=action_priority,
        confidence=round(confidence, 2),
        detailed_findings=findings,
    )


# ============================================================
# 数据接口 (从CSV/JSON加载)
# ============================================================

def load_from_csv(filepath: str) -> List[ProductData]:
    """从CSV加载产品数据"""
    import csv
    products = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = ProductData(
                product_id=row.get('product_id', ''),
                product_name=row.get('product_name', ''),
                product_price=float(row.get('product_price', 0)),
                product_description=row.get('product_description', ''),
                category=row.get('category', ''),
                view_count=int(row.get('view_count', 0)),
                view_duration_avg=float(row.get('view_duration_avg', 0)),
                detail_page_view_rate=float(row.get('detail_page_view_rate', 0)),
                scroll_depth_avg=float(row.get('scroll_depth_avg', 0)),
                like_count=int(row.get('like_count', 0)),
                comment_count=int(row.get('comment_count', 0)),
                share_count=int(row.get('share_count', 0)),
                add_to_cart_rate=float(row.get('add_to_cart_rate', 0)),
                favorite_rate=float(row.get('favorite_rate', 0)),
                revisit_rate=float(row.get('revisit_rate', 0)),
                purchase_rate=float(row.get('purchase_rate', 0)),
                total_users=int(row.get('total_users', 0)),
            )
            products.append(p)
    return products


def load_from_json(filepath: str) -> List[ProductData]:
    """从JSON加载产品数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    products = []
    for item in data:
        p = ProductData(**{k: v for k, v in item.items()
                          if k in ProductData.__dataclass_fields__})
        products.append(p)
    return products


def run_analysis(products: List[ProductData]) -> Dict:
    """执行完整分析流程，返回结果字典"""
    results = {
        "products": [],
        "summary": {
            "total_products": len(products),
            "price_issues": 0,
            "copy_issues": 0,
            "both_issues": 0,
            "no_issues": 0,
        }
    }

    for product in products:
        interest = calculate_interest_score(product)
        copy_analysis = analyze_copy(product.product_description, product.product_id)
        diagnosis = diagnose(product, interest, copy_analysis)

        product_result = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "category": product.category,
            "interest_score": interest.total_score,
            "interest_level": interest.interest_level,
            "sub_scores": interest.sub_scores,
            "conversion_rate": product.purchase_rate * 100,
            "total_users": product.total_users,
            "copy_analysis": {
                "word_count": copy_analysis.word_count,
                "has_cta": copy_analysis.has_cta,
                "has_selling_point": copy_analysis.has_selling_point,
                "sentiment_score": copy_analysis.sentiment_score,
                "readability_score": copy_analysis.readability_score,
                "suggestions": copy_analysis.suggestions,
            },
            "diagnosis": {
                "primary_issue": diagnosis.primary_issue,
                "price_suggestion": diagnosis.price_suggestion,
                "copy_suggestion": diagnosis.copy_suggestion,
                "action_priority": diagnosis.action_priority,
                "confidence": diagnosis.confidence,
                "detailed_findings": diagnosis.detailed_findings,
            }
        }

        results["products"].append(product_result)

        # 汇总统计
        if diagnosis.primary_issue == "price":
            results["summary"]["price_issues"] += 1
        elif diagnosis.primary_issue == "copy":
            results["summary"]["copy_issues"] += 1
        elif diagnosis.primary_issue == "both":
            results["summary"]["both_issues"] += 1
        else:
            results["summary"]["no_issues"] += 1

    return results


# ============================================================
# CLI入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="电商商品兴趣度分析引擎")
    parser.add_argument("--input", "-i", required=True,
                        help="输入数据文件路径 (CSV/JSON)")
    parser.add_argument("--output", "-o", default="analysis_result.json",
                        help="输出JSON结果路径 (默认: analysis_result.json)")
    args = parser.parse_args()

    # 加载数据
    filepath = args.input
    ext = Path(filepath).suffix.lower()
    if ext == '.csv':
        products = load_from_csv(filepath)
    elif ext == '.json':
        products = load_from_json(filepath)
    else:
        print(f"不支持的文件格式: {ext}，请使用 CSV 或 JSON")
        sys.exit(1)

    if not products:
        print("错误: 未加载到任何产品数据")
        sys.exit(1)

    print(f"✅ 加载 {len(products)} 个商品数据")

    # 执行分析
    results = run_analysis(products)

    # 输出结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 分析完成，结果输出到 {args.output}")
    print(f"\n📊 分析摘要:")
    print(f"   总商品数: {results['summary']['total_products']}")
    print(f"   价格问题: {results['summary']['price_issues']}")
    print(f"   文案问题: {results['summary']['copy_issues']}")
    print(f"   综合问题: {results['summary']['both_issues']}")
    print(f"   表现优秀: {results['summary']['no_issues']}")

    for p in results["products"]:
        icon = {"price": "💰", "copy": "📝", "both": "🔧", "none": "✅"}.get(
            p["diagnosis"]["primary_issue"], "❓")
        print(f"\n{icon} [{p['product_name']}] "
              f"兴趣度: {p['interest_score']}分 ({p['interest_level']}) | "
              f"转化率: {p['conversion_rate']:.1f}% | "
              f"问题: {p['diagnosis']['primary_issue']}")
