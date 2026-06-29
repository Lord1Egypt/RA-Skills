#!/usr/bin/env python3
"""
Amazon产品研究员 - 主流程编排
8阶段全链路分析: 搜索→评论→打标→关键词→VOC→竞品→机会→报告
"""

import argparse
import sys
import os
import webbrowser
import random
import io
from datetime import datetime
from typing import Dict, List, Optional

# Windows GBK encoding fix
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 导入同目录模块
sys.path.insert(0, os.path.dirname(__file__))
from product_search import search_products
from fetch_reviews import fetch_reviews
from ai_tagging import tag_reviews_batch
from keyword_expansion import expand_keywords
from voc_clustering import cluster_voc
from competitor_analysis import analyze_competitors
from opportunity_analysis import analyze_opportunities
from generate_report import generate_html_report


def main():
    parser = argparse.ArgumentParser(
        description="Amazon产品研究员 - 一句话输入，全链路分析输出",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 体验模式（模拟数据，无需API Key）
  python research.py --query "bluetooth headphones noise cancelling" --use-mock

  # 完整分析（需要LLM API Key）
  python research.py --query "portable bluetooth speaker waterproof" --api-key sk-xxx

  # 使用DeepSeek（国内推荐）
  python research.py --query "yoga mat" --api-key sk-xxx --api-base https://api.deepseek.com/v1 --model deepseek-chat
        """
    )

    parser.add_argument("--query", required=True, help="搜索关键词/产品名/ASIN/描述")
    parser.add_argument("--market", default="US", help="市场区域（US/UK/DE/JP/FR/CA/IT/ES）")
    parser.add_argument("--max-products", type=int, default=5, help="最多分析产品数（默认5）")
    parser.add_argument("--max-reviews", type=int, default=100, help="每个产品最大评论数（默认100）")
    parser.add_argument("--api-key", help="LLM API Key")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="API Base URL")
    parser.add_argument("--model", default="gpt-4o-mini", help="模型名称")
    parser.add_argument("--output", help="输出报告路径")
    parser.add_argument("--rapidapi-key", help="RapidAPI Key（可选，用于真实数据）")
    parser.add_argument("--use-mock", action="store_true", help="使用模拟数据演示（无需API Key）")
    parser.add_argument("--debug", action="store_true", help="打印调试信息")

    args = parser.parse_args()

    # 判断是否使用LLM
    use_llm = bool(args.api_key)
    use_mock = args.use_mock or (not use_llm)

    # 打印标题
    print_banner(args.query, args.market)

    # ========== Stage 1: 产品搜索 ==========
    print_stage(1, "产品搜索")
    products = search_products(
        query=args.query,
        market=args.market,
        max_products=args.max_products,
        rapidapi_key=args.rapidapi_key,
        debug=args.debug
    )
    for i, p in enumerate(products, 1):
        print(f"  {i}. [{p['asin']}] {p['title'][:70]} | ⭐{p['rating']} | {p['price']}")
    print()

    # ========== Stage 2: 多产品评论采集 ==========
    print_stage(2, "评论采集")
    tagged_reviews = {}  # {asin: [{review, tags}, ...]}

    for i, product in enumerate(products, 1):
        asin = product["asin"]
        print(f"  [{i}/{len(products)}] {asin} - {product['title'][:50]}...")

        if use_mock:
            # 生成模拟评论
            reviews_data = generate_mock_reviews_for_product(product, args.max_reviews)
        else:
            reviews_data = fetch_reviews(
                asin=asin,
                market=args.market,
                max_reviews=args.max_reviews,
                rapidapi_key=args.rapidapi_key,
                debug=args.debug
            )

        reviews = reviews_data.get("reviews", [])
        print(f"    获取 {len(reviews)} 条评论")

        # ========== Stage 3: AI打标 ==========
        if use_llm and not use_mock:
            print(f"    AI打标 {len(reviews)} 条评论...")
            tagged = tag_reviews_batch(
                reviews=reviews,
                api_key=args.api_key,
                api_base=args.api_base,
                model=args.model,
                delay=0.5,
                debug=args.debug
            )
        else:
            # 模拟打标
            tagged = apply_mock_tags(reviews)

        tagged_reviews[asin] = tagged

    total_reviews = sum(len(r) for r in tagged_reviews.values())
    print(f"\n✅ 评论采集+打标完成: {total_reviews} 条评论\n")

    # ========== Stage 4-7: AI分析 ==========
    if use_llm and not use_mock:
        print_stage(4, "关键词扩展 + VOC聚类 + 竞品分析 + 机会分析")
        print("  正在进行AI综合分析（可能需要1-3分钟）...\n")

        # 4. 关键词扩展
        keyword_data = expand_keywords(
            products=products,
            tagged_reviews=tagged_reviews,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model,
            debug=args.debug
        )

        # 5. VOC聚类
        voc_data = cluster_voc(
            tagged_reviews=tagged_reviews,
            products=products,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model,
            debug=args.debug
        )

        # 6. 竞品分析
        competitor_data = analyze_competitors(
            products=products,
            tagged_reviews=tagged_reviews,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model,
            debug=args.debug
        )

        # 7. 机会分析
        opportunity_data = analyze_opportunities(
            products=products,
            tagged_reviews=tagged_reviews,
            voc_result=voc_data,
            competitor_result=competitor_data,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model,
            debug=args.debug
        )
    else:
        print_stage(4, "模拟分析")

        keyword_data = generate_mock_keywords(args.query)
        print(f"  🔑 关键词: {len(keyword_data.get('high_frequency_keywords', []))} 高频词 + {len(keyword_data.get('long_tail_keywords', []))} 长尾词")

        voc_data = generate_mock_voc()
        print(f"  🎯 VOC: {len(voc_data.get('clusters', []))} 个痛点类别")

        competitor_data = generate_mock_competitor(products, tagged_reviews)
        print(f"  📊 竞品: {len(competitor_data.get('comparison_matrix', []))} 个产品对比")

        opportunity_data = generate_mock_opportunity(args.query)
        print(f"  💡 机会: {len(opportunity_data.get('opportunities', []))} 个方向")

    print()

    # ========== Stage 8: 报告生成 ==========
    print_stage(8, "报告生成")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = args.output or f"./product_research_{timestamp}.html"
    output_path = os.path.abspath(output_path)

    generate_html_report(
        query=args.query,
        market=args.market,
        products=products,
        tagged_reviews=tagged_reviews,
        keyword_data=keyword_data,
        voc_data=voc_data,
        competitor_data=competitor_data,
        opportunity_data=opportunity_data,
        output_path=output_path,
        debug=args.debug
    )

    # 自动打开报告
    print("🌐 正在打开报告...")
    webbrowser.open(f"file://{output_path}")

    print()
    print("=" * 70)
    print(f"✅ 全链路分析完成！")
    print(f"   分析产品: {len(products)} 个")
    print(f"   分析评论: {total_reviews} 条")
    print(f"   报告路径: {output_path}")
    if use_mock:
        print(f"   ⚠️ 演示模式（模拟数据）- 提供 --api-key 获取AI分析")
    print("=" * 70)

    return 0


def print_banner(query: str, market: str):
    print()
    print("=" * 70)
    print("  🛍️  亚马逊产品研究员 | Amazon Product Research")
    print("=" * 70)
    print(f"  搜索词: {query}")
    print(f"  市场:   {market}")
    print(f"  时间:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()


def print_stage(stage: int, name: str):
    icons = ["", "🔍", "📝", "🤖", "🧠", "🧠", "🧠", "🧠", "📄"]
    icon = icons[stage] if stage < len(icons) else "📊"
    print(f"{icon} Stage {stage}/8: {name}")
    print("-" * 50)


# ========== Mock数据生成器 ==========

def generate_mock_reviews_for_product(product: Dict, max_reviews: int) -> Dict:
    """为单个产品生成模拟评论"""
    rating = product.get("rating", 4.0)

    # 模拟评论模板
    templates = [
        {"rating": 5, "title": "Excellent quality, highly recommend",
         "body": "This product exceeded my expectations. The quality is outstanding and it works perfectly. I've been using it for a month now and it's still like new. Highly recommended for anyone looking for a reliable product."},
        {"rating": 4, "title": "Good value for the price",
         "body": "Pretty good product for the price point. Does what it's supposed to do. A few minor issues but overall satisfied. Would buy again."},
        {"rating": 3, "title": "It's okay, nothing special",
         "body": "Average product. Does the job but doesn't stand out. Expected a bit more for the price. Wouldn't buy again but won't return it either."},
        {"rating": 2, "title": "Disappointed with quality",
         "body": "Not happy with this purchase. The quality is below expectations and it started showing issues after just a few weeks. The materials feel cheap and it doesn't work as described."},
        {"rating": 1, "title": "Waste of money, broke quickly",
         "body": "Terrible product. Stopped working after 2 weeks. Very poor build quality and customer service is unhelpful. Don't waste your money on this."},
        {"rating": 5, "title": "Perfect for what I needed",
         "body": "Exactly what I was looking for. The build quality is solid, it's easy to use, and the price is reasonable. Shipping was fast and packaging was great."},
        {"rating": 4, "title": "Solid product, minor flaws",
         "body": "Overall a good purchase. The main functionality works well, but there are a few design choices I don't love. Still, for the price, it's a solid buy."},
        {"rating": 3, "title": "Not bad, not great",
         "body": "It's a functional product that gets the job done. Nothing about it wows me, but nothing about it is terrible either. An average purchase."},
        {"rating": 5, "title": "Best purchase this year",
         "body": "Absolutely love this! The quality, design, and performance are all top-notch. I've recommended it to friends and family. Definitely worth every penny."},
        {"rating": 4, "title": "Works well, reasonably priced",
         "body": "Happy with this purchase. It works as expected and the price is fair. The packaging was nice and it came with clear instructions. Would recommend to others."},
        {"rating": 2, "title": "Not as described",
         "body": "The product doesn't match the description. The color is different, the size is off, and it doesn't have all the features listed. Very misleading listing."},
        {"rating": 1, "title": "Completely useless",
         "body": "This product is a complete waste. It doesn't work at all and the return process is a nightmare. Save yourself the trouble and buy something else."},
        {"rating": 5, "title": "Great product, fast shipping",
         "body": "Ordered this and it arrived in 2 days. The quality is excellent and it's exactly what I expected. Very happy with this purchase and will order again."},
        {"rating": 4, "title": "Good but room for improvement",
         "body": "I like this product overall but there are definitely areas for improvement. The battery life could be better and the instructions could be clearer. Still a good buy."},
        {"rating": 5, "title": "Incredible value",
         "body": "Can't believe the quality for this price point. It's comparable to products that cost twice as much. Very impressed and will be a repeat customer."},
    ]

    rating_buckets = {
        5: [0, 3, 5, 8, 11, 12, 14],  # 偏好评
        4: [1, 6, 7, 9, 13],
        3: [2, 7],
        2: [3, 10],
        1: [4, 11],
    }

    # 根据产品评分分配模板权重
    def pick_template():
        # 有偏差地选择模板
        if rating >= 4.2:
            weights = [30, 25, 10, 10, 5, 10, 10, 5, 5, 5, 3, 2, 5, 3, 5]
        elif rating >= 3.5:
            weights = [15, 20, 15, 15, 10, 10, 10, 10, 8, 8, 8, 8, 8, 8, 8]
        else:
            weights = [5, 10, 15, 20, 25, 5, 10, 15, 3, 10, 15, 20, 3, 10, 15]
        return random.choices(templates, weights=weights, k=1)[0]

    reviews = []
    for i in range(min(max_reviews, 50)):  # Mock 限制50条
        t = pick_template()
        review = {
            "id": f"mock_{product['asin']}_{i}",
            "rating": t["rating"],
            "title": f"{t['title']} (Review {i+1})",
            "body": t["body"],
            "author": f"AmazonCustomer{i+1}",
            "date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "verified_purchase": random.choice([True, True, True, False]),
            "helpful_votes": random.randint(0, 30),
            "_mock_tags": {
                "sentiment": "positive" if t["rating"] >= 4 else "negative" if t["rating"] <= 2 else "neutral",
                "pain_points": ["质量不稳定", "性价比低"] if t["rating"] <= 2 else [],
                "selling_points": ["质量好", "性价比高"] if t["rating"] >= 4 else [],
                "use_cases": ["日常使用"],
                "user_profile": "普通消费者",
                "improvement_suggestions": [],
                "summary": t["title"][:20]
            }
        }
        reviews.append(review)

    return {"product": product, "reviews": reviews, "total_reviews": len(reviews), "fetched_reviews": len(reviews)}


def apply_mock_tags(reviews: List[Dict]) -> List[Dict]:
    """应用模拟打标"""
    tagged = []
    for r in reviews:
        tags = r.pop("_mock_tags", {
            "sentiment": "neutral",
            "pain_points": [],
            "selling_points": [],
            "use_cases": [],
            "user_profile": "",
            "improvement_suggestions": [],
            "summary": ""
        })
        tagged.append({"review": r, "tags": tags})
    return tagged


def generate_mock_keywords(query: str) -> Dict:
    """生成模拟关键词"""
    words = query.split()

    high_freq = []
    for w in words[:3]:
        variants = [f"{w} pro", f"best {w}", f"{w} 2025", f"{w} premium", f"{w} wireless"]
        for v in variants[:3]:
            high_freq.append({
                "keyword": v,
                "frequency": "high",
                "source": "category",
                "monthly_searches_estimate": random.randint(5000, 50000)
            })

    long_tail = []
    for w in words[:2]:
        for suffix in ["under 50", "reviews 4 star", "for beginners", "professional grade", "with warranty", "best seller"]:
            long_tail.append({
                "keyword": f"{w} {suffix}",
                "volume": random.choice(["medium", "low"]),
                "competition": random.choice(["low", "medium"]),
                "conversion_potential": random.choice(["high", "medium"]),
                "monthly_searches_estimate": random.randint(500, 5000)
            })

    return {
        "high_frequency_keywords": high_freq,
        "long_tail_keywords": long_tail,
        "related_terms": [
            {"term": f"{query} accessories", "relation": "complement", "weight": 0.9},
            {"term": f"{query} replacement parts", "relation": "accessory", "weight": 0.7},
            {"term": f"cheap {query} alternative", "relation": "substitute", "weight": 0.8},
            {"term": f"{query} for travel", "relation": "use_case", "weight": 0.6},
            {"term": f"{query} gift set", "relation": "use_case", "weight": 0.5},
        ],
        "category_trends": [
            "消费者越来越关注产品的耐用性和售后服务",
            f"中端价位（$30-60）的{query}产品需求增长明显",
            "无线/蓝牙功能成为标配，缺失该功能的产品竞争力下降"
        ],
        "summary": f"建议重点关注长尾关键词和细分场景词。高频词竞争激烈，长尾词转化率高且竞争度相对较低。基于用户痛点优化关键词策略，将\"{query} durable\"等词作为重点。"
    }


def generate_mock_voc() -> Dict:
    """生成模拟VOC"""
    return {
        "clusters": [
            {
                "category": "产品质量不稳定",
                "severity": 9,
                "frequency": 125,
                "pain_points": ["容易损坏", "材料廉价感", "做工粗糙", "用几个月就出问题"],
                "typical_reviews": [
                    "用了不到一个月就开始出问题，质量太差了",
                    "材料感觉很cheap，不值这个价"
                ],
                "affected_products": ["B0XXXX", "B0YYYY"],
                "improvement_direction": "提升材料品质和品控标准"
            },
            {
                "category": "续航/电池问题",
                "severity": 8,
                "frequency": 98,
                "pain_points": ["续航太短", "充电时间长", "电池用一年就衰减"],
                "typical_reviews": [
                    "充一次电只能用2小时，太不方便了",
                    "用了半年电池就不行了"
                ],
                "affected_products": ["B0XXXX", "B0ZZZZ"],
                "improvement_direction": "升级电池容量或优化功耗"
            },
            {
                "category": "客服响应慢",
                "severity": 7,
                "frequency": 67,
                "pain_points": ["退货流程复杂", "客服不回复", "保修条款不清晰"],
                "typical_reviews": [
                    "联系客服3天都没人回，太气人了",
                    "退货还要自己出运费，很不合理"
                ],
                "affected_products": ["B0YYYY"],
                "improvement_direction": "建立快速响应的客服体系"
            },
            {
                "category": "产品与描述不符",
                "severity": 6,
                "frequency": 54,
                "pain_points": ["颜色差异大", "尺寸不准", "功能夸大"],
                "typical_reviews": [
                    "收到后发现颜色完全不一样",
                    "描述说防水，结果淋了一点雨就坏了"
                ],
                "affected_products": ["B0XXXX", "B0ZZZZ"],
                "improvement_direction": "更新产品描述，确保准确性"
            },
            {
                "category": "配件/包装简陋",
                "severity": 4,
                "frequency": 38,
                "pain_points": ["缺少说明书", "包装破损", "没有充电线"],
                "typical_reviews": [],
                "affected_products": ["B0YYYY"],
                "improvement_direction": "完善配件和包装"
            },
        ],
        "severity_summary": {
            "critical": [
                {"category": "产品质量不稳定", "severity": 9},
                {"category": "续航/电池问题", "severity": 8},
            ],
            "major": [
                {"category": "客服响应慢", "severity": 7},
                {"category": "产品与描述不符", "severity": 6},
            ],
            "minor": [
                {"category": "配件/包装简陋", "severity": 4},
            ]
        },
        "overall_summary": "该品类最大的痛点是产品质量不稳定和续航问题，这两个问题直接影响用户购买决策和复购意愿。客服响应慢也是重要问题，但相对容易解决。建议新手卖家重点关注品控，这是差异化竞争的核心切入点。"
    }


def generate_mock_competitor(products: List[Dict], tagged_reviews: Dict[str, List[Dict]]) -> Dict:
    """生成模拟竞品分析"""
    matrix = []
    positions = ["高端旗舰", "性价比之王", "中端全能", "入门爆款", "品质首选"]

    for i, p in enumerate(products[:5]):
        r = p.get("rating", 4)
        matrix.append({
            "asin": p["asin"],
            "title": p["title"][:40],
            "scores": {
                "quality": min(10, max(2, int(r * 2.2))),
                "value_for_money": min(10, max(2, random.randint(5, 9))),
                "features": min(10, max(2, random.randint(5, 9))),
                "customer_satisfaction": min(10, max(2, int(r * 2))),
                "brand_power": min(10, max(1, random.randint(3, 9)))
            },
            "strengths": ["性价比高", "用户评价好"][:2],
            "weaknesses": ["品牌知名度不足", "品类不够丰富"][:2],
            "positioning": positions[i % len(positions)],
            "target_audience": "大众消费者"
        })

    return {
        "comparison_matrix": matrix,
        "radar_dimensions": ["quality", "value_for_money", "features", "customer_satisfaction", "brand_power"],
        "market_gaps": [
            {"description": "$30-50价格区间缺少高品质产品", "opportunity_score": 9},
            {"description": "面向老年人的简易版产品缺失", "opportunity_score": 7},
            {"description": "环保材质产品几乎空白", "opportunity_score": 8},
            {"description": "支持App控制的智能产品不足", "opportunity_score": 6},
        ],
        "overall_summary": "市场竞争格局分明：高端市场由品牌产品主导，中端市场群雄混战，低端市场以价格战为主。$30-50区间的品质产品和环保材质品类是明显的市场空白。"
    }


def generate_mock_opportunity(query: str) -> Dict:
    """生成模拟机会分析"""
    return {
        "opportunities": [
            {
                "title": f"高品质入门款{query}",
                "description": f"当前市场$30-50区间缺少品质可靠的产品，针对首次购买者推出高品质入门款，主打工艺和材料，定价中端偏上。",
                "opportunity_score": 9,
                "target_market": "首次购买者，注重品质但预算有限",
                "estimated_demand": "高",
                "competitive_intensity": "中",
                "price_range": "$35-45",
                "key_differentiator": "大牌品质，中端价格",
                "risks": ["品牌信任度建立需要时间", "可能被大牌降价打压"],
                "entry_difficulty": "中"
            },
            {
                "title": f"环保材质{query}",
                "description": f"消费者环保意识增强，但目前品类中缺乏环保材质的产品。使用可回收/生物降解材料，吸引环保意识强的用户群体。",
                "opportunity_score": 8,
                "target_market": "环保意识强的年轻消费者",
                "estimated_demand": "中",
                "competitive_intensity": "低",
                "price_range": "$40-60",
                "key_differentiator": "100%可回收材料",
                "risks": ["环保材料成本高", "功能可能弱于传统产品"],
                "entry_difficulty": "中"
            },
            {
                "title": f"智能联动{query}",
                "description": f"增加App控制和智能联动功能，切入IoT赛道。通过App提供使用数据、电量提醒、固件升级等附加价值。",
                "opportunity_score": 7,
                "target_market": "科技爱好者、智能家居用户",
                "estimated_demand": "中",
                "competitive_intensity": "低",
                "price_range": "$50-80",
                "key_differentiator": "App智能控制",
                "risks": ["研发投入大", "App维护成本", "用户隐私顾虑"],
                "entry_difficulty": "高"
            },
        ],
        "top_recommendation": {
            "direction": f"高品质入门款{query} - 机会评分最高，风险可控",
            "reasoning": "该方向市场需求明确、竞争强度适中、进入壁垒合理。通过解决'质量不稳定'这一品类核心痛点，可快速建立品牌认知。建议先小批量试产（500-1000件），通过FBA快速验证市场反应。",
            "action_items": [
                "筛选2-3家优质供应商，对比样品质量和成本",
                "制定详细产品规格书，聚焦2-3个核心差异化功能",
                "准备5-10款Listing文案方案，A/B测试转化率",
                "制定关键词策略：主攻长尾词，逐步覆盖核心词",
                "首批试产500件，通过FBA快速入仓测试市场"
            ]
        },
        "risk_assessment": "整体风险中等。主要风险来自：1)供应链质量控制；2)大牌降价打压；3)广告成本上升。建议控制首批备货量，快速迭代优化。",
        "summary": f"基于对5个竞品品牌的分析，{query}品类存在3个明确的新品切入机会。最推荐'高品质入门款'方向——需求大、竞争适中、差异化空间明确。建议1-2个月内完成选品和首批试产。"
    }


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n\n⚠️ 分析被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
