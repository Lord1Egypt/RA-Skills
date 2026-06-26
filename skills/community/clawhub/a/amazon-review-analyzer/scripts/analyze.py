#!/usr/bin/env python3
"""
Amazon评论深度分析 - 主分析脚本
串联评论采集、AI打标、报告生成全流程
"""

import argparse
import sys
import os
import webbrowser
from datetime import datetime
from typing import Optional

# 导入同目录下的模块
sys.path.insert(0, os.path.dirname(__file__))
from fetch_reviews import fetch_reviews
from ai_tagging import tag_reviews_batch
from generate_report import generate_html_report


def main():
    parser = argparse.ArgumentParser(
        description="Amazon评论深度分析助手 - 输入ASIN，输出洞察报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用OpenAI API
  python analyze.py --asin B08N5WRWNW --api-key sk-xxx
  
  # 使用DeepSeek API（国内推荐）
  python analyze.py --asin B08N5WRWNW --api-key sk-xxx --api-base https://api.deepseek.com/v1 --model deepseek-chat
  
  # 分析最多1000条评论
  python analyze.py --asin B08N5WRWNW --api-key sk-xxx --max-reviews 1000
        """
    )
    
    parser.add_argument("--asin", required=True, help="Amazon ASIN（产品ID）")
    parser.add_argument("--market", default="US", help="市场区域（US/UK/DE/JP/FR/CA/IT/ES），默认US")
    parser.add_argument("--max-reviews", type=int, default=500, help="最大评论数量（默认500）")
    parser.add_argument("--api-key", required=True, help="LLM API Key（OpenAI/DeepSeek/其他兼容API）")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="API Base URL（默认OpenAI）")
    parser.add_argument("--model", default="gpt-4o-mini", help="模型名称（默认gpt-4o-mini）")
    parser.add_argument("--output", help="输出报告路径（默认./review_analysis_{ASIN}.html）")
    parser.add_argument("--rapidapi-key", help="RapidAPI Key（可选，用于获取真实评论）")
    parser.add_argument("--debug", action="store_true", help="打印调试信息")
    parser.add_argument("--use-mock", action="store_true", help="使用模拟数据（不需要RapidAPI）")
    parser.add_argument("--use-mock-tags", action="store_true", help="使用模拟打标结果（不调用AI API，仅用于测试）")
    
    args = parser.parse_args()
    
    # 打印欢迎信息
    print("=" * 60)
    print("🛍️ Amazon评论深度分析助手")
    print("=" * 60)
    print(f"ASIN: {args.asin}")
    print(f"市场: {args.market}")
    print(f"最大评论数: {args.max_reviews}")
    print(f"模型: {args.model}")
    print(f"API: {args.api_base}")
    print("=" * 60)
    print()
    
    # 步骤1：获取评论数据
    if args.use_mock or not args.rapidapi_key:
        print("📝 使用模拟评论数据（如需真实数据，请提供 --rapidapi-key 或去掉 --use-mock）")
        reviews_data = _generate_mock_reviews(args.asin, args.max_reviews)
    else:
        print("🔍 正在获取真实评论数据...")
        reviews_data = fetch_reviews(
            asin=args.asin,
            market=args.market,
            max_reviews=args.max_reviews,
            rapidapi_key=args.rapidapi_key,
            debug=args.debug
        )
    
    product_info = reviews_data["product"]
    reviews = reviews_data["reviews"]
    
    if not reviews:
        print("❌ 未获取到评论数据，退出")
        return 1
    
    print(f"✅ 已获取 {len(reviews)} 条评论")
    print()
    
    # 步骤2：AI打标
    if args.use_mock_tags:
        print("🤖 使用模拟打标结果（不调用AI API）...")
        tagged_reviews = _apply_mock_tags(reviews)
    else:
        print("🤖 开始AI深度打标...")
        tagged_reviews = tag_reviews_batch(
            reviews=reviews,
            api_key=args.api_key,
            api_base=args.api_base,
            model=args.model,
            delay=0.5,  # API调用间隔0.5秒
            debug=args.debug
        )
    print()
    
    # 步骤3：生成报告
    output_path = args.output or f"./review_analysis_{args.asin}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_path = os.path.abspath(output_path)
    
    print("📄 正在生成HTML报告...")
    generate_html_report(
        product_info=product_info,
        tagged_reviews=tagged_reviews,
        output_path=output_path,
        debug=args.debug
    )
    print()
    
    # 步骤4：自动打开报告
    print("🌐 正在打开报告...")
    webbrowser.open(f"file://{output_path}")
    
    print()
    print("=" * 60)
    print(f"✅ 分析完成！报告已保存至：")
    print(f"   {output_path}")
    print("=" * 60)
    
    return 0


def _apply_mock_tags(reviews: list) -> list:
    """应用模拟打标结果（从模拟评论中提取预置打标）"""
    tagged_reviews = []
    for review in reviews:
        # 提取预置打标结果
        mock_tags = review.get("_mock_tags", {
            "sentiment": "neutral",
            "pain_points": [],
            "selling_points": [],
            "use_cases": [],
            "user_profile": "",
            "improvement_suggestions": [],
            "summary": ""
        })
        
        # 移除内部字段
        clean_review = {k: v for k, v in review.items() if not k.startswith("_")}
        
        tagged_reviews.append({
            "review": clean_review,
            "tags": mock_tags
        })
    
    print(f"  已应用 {len(tagged_reviews)} 条模拟打标结果")
    return tagged_reviews


def _generate_mock_reviews(asin: str, max_reviews: int) -> dict:
    """
    生成模拟评论数据（用于演示和测试）
    
    在实际使用中，应该通过RapidAPI获取真实评论
    """
    
    import random
    
    print("  生成模拟评论数据...")
    
    # 模拟产品信息
    product_info = {
        "asin": asin,
        "title": f"Sample Product ({asin})",
        "price": "$99.99",
        "rating": 4.2,
        "total_reviews": max_reviews,
        "image_url": "https://via.placeholder.com/300",
        "url": f"https://www.amazon.com/dp/{asin}"
    }
    
    # 模拟评论模板（中英文混合，模拟真实场景）
    mock_templates = [
        {
            "rating": 5,
            "title": "质量很好，推荐购买",
            "body": "收到货后非常满意，产品质量很好，做工精细。使用了一周，效果不错，值得推荐。",
            "pain_points": [],
            "selling_points": ["质量好", "做工精细", "效果好"],
            "use_cases": ["日常使用"],
            "user_profile": "注重品质的买家",
            "improvement_suggestions": []
        },
        {
            "rating": 1,
            "title": "质量太差，两天就坏了",
            "body": "非常失望，产品用了两天就坏了。质量控太差，不值这个价。退货还麻烦。",
            "pain_points": ["质量差", "容易坏", "退货麻烦"],
            "selling_points": [],
            "use_cases": [],
            "user_profile": "愤怒的消费者",
            "improvement_suggestions": ["提升质量控", "简化退货流程"]
        },
        {
            "rating": 3,
            "title": "性价比一般，价格偏高",
            "body": "产品还行，但感觉价格偏高。同类产品有更便宜的，功能也差不多。",
            "pain_points": ["价格高", "性价比低"],
            "selling_points": ["功能还行"],
            "use_cases": ["偶尔使用"],
            "user_profile": "价格敏感型买家",
            "improvement_suggestions": ["降低价格", "提升性价比"]
        },
        {
            "rating": 4,
            "title": "性价比不错，物流快",
            "body": "产品对得起价格，物流速度很快，包装完好。会考虑回购。",
            "pain_points": [],
            "selling_points": ["性价比高", "物流快", "包装好"],
            "use_cases": ["日常使用"],
            "user_profile": "理性消费者",
            "improvement_suggestions": []
        },
        {
            "rating": 2,
            "title": "和描述不符，尺寸不对",
            "body": "产品描述和实际收到的不一样。尺寸不对，颜色也有色差。感觉被误导了。",
            "pain_points": ["描述不符", "尺寸错误", "色差"],
            "selling_points": [],
            "use_cases": [],
            "user_profile": "被误导的买家",
            "improvement_suggestions": ["准确描述", "提供准确尺寸"]
        },
        {
            "rating": 5,
            "title": "Great product, love it!",
            "body": "This product is amazing! The quality is top-notch and it works perfectly. Highly recommended for everyone.",
            "pain_points": [],
            "selling_points": ["excellent quality", "works perfectly"],
            "use_cases": ["daily use", "gift"],
            "user_profile": "satisfied international buyer",
            "improvement_suggestions": []
        },
        {
            "rating": 1,
            "title": "Worst purchase ever",
            "body": "The product broke after 3 days. Very poor quality. Don't waste your money on this garbage.",
            "pain_points": ["poor quality", "breaks easily"],
            "selling_points": [],
            "use_cases": [],
            "user_profile": "angry buyer",
            "improvement_suggestions": ["improve durability"]
        }
    ]
    
    # 生成模拟评论
    reviews = []
    for i in range(max_reviews):
        template = random.choice(mock_templates)
        review = {
            "id": f"mock_{i}",
            "rating": template["rating"],
            "title": f"{template['title']} (Mock {i+1})",
            "body": template["body"],
            "author": f"User{i+1}",
            "date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "verified_purchase": random.choice([True, False]),
            "helpful_votes": random.randint(0, 50),
            # 预置打标结果（模拟AI打标）
            "_mock_tags": {
                "sentiment": "positive" if template["rating"] >= 4 else "negative" if template["rating"] <= 2 else "neutral",
                "pain_points": template["pain_points"],
                "selling_points": template["selling_points"],
                "use_cases": template["use_cases"],
                "user_profile": template["user_profile"],
                "improvement_suggestions": template["improvement_suggestions"],
                "summary": template["title"][:20]
            }
        }
        reviews.append(review)
    
    print(f"  已生成 {len(reviews)} 条模拟评论")
    print("  ⚠️  注意：这是模拟数据，用于演示流程。如需真实评论，请配置 --rapidapi-key")
    
    return {
        "product": product_info,
        "reviews": reviews,
        "total_reviews": len(reviews),
        "fetched_reviews": len(reviews)
    }


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  分析被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
