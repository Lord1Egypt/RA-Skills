#!/usr/bin/env python3
"""
Meal to Intervals.icu - 饮食记录工具（精简版）
将饮食数据同步到 intervals.icu wellness 记录

支持：
- 自然语言输入（中文）
- JSON 文件输入
- 自动营养计算（OpenFoodFacts API + 中文规则库）
- 交互式询问（当食物无法识别时）
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 导入 API 客户端和营养估算引擎
sys.path.insert(0, str(Path(__file__).parent))
from intervals_api_client import create_client, IntervalsICUClient
from nutrition_estimator import NutritionEstimator

# 餐次关键词
MEAL_KEYWORDS = {
    "breakfast": ["早餐", "早饭", "早上"],
    "lunch": ["午餐", "午饭", "中午", "中餐"],
    "dinner": ["晚餐", "晚饭", "晚上", "晚餐"],
    "snack": ["加餐", "零食", "下午茶", "夜宵"],
}

def detect_meal_type(text: str) -> str:
    """根据文本检测餐次"""
    text_lower = text.lower()
    for meal_type, keywords in MEAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return meal_type
    return "snack"

def upload_meal_to_intervals(client: IntervalsICUClient, meal_data: dict, dry_run: bool = False) -> bool:
    """上传饮食数据到 intervals.icu"""
    date = meal_data["date"]
    
    # 获取现有 wellness 数据
    existing = client.get_wellness(date)
    
    # 构建更新数据（累加营养）- 使用正确的 API 字段名
    update_data = {}
    if existing:
        # 累加营养（API 字段名）
        update_data["kcalConsumed"] = (existing.get("kcalConsumed") or 0) + meal_data["nutrition"]["calories"]
        update_data["protein"] = (existing.get("protein") or 0) + meal_data["nutrition"]["protein"]
        update_data["carbohydrates"] = (existing.get("carbohydrates") or 0) + meal_data["nutrition"]["carbs"]
        update_data["fatTotal"] = (existing.get("fatTotal") or 0) + meal_data["nutrition"]["fat"]
    else:
        # 首次上传
        update_data["kcalConsumed"] = meal_data["nutrition"]["calories"]
        update_data["protein"] = meal_data["nutrition"]["protein"]
        update_data["carbohydrates"] = meal_data["nutrition"]["carbs"]
        update_data["fatTotal"] = meal_data["nutrition"]["fat"]
    
    # 添加备注（使用 comments 字段，累加）
    existing_comments = existing.get("comments") or ""
    new_comment = f"[{meal_data['meal_type']}] {meal_data['notes']}"
    if existing_comments:
        update_data["comments"] = f"{existing_comments}; {new_comment}"
    else:
        update_data["comments"] = new_comment
    
    if dry_run:
        print(f"\n🔍 干跑模式 - 将上传以下数据:")
        print(f"  日期：{date}")
        print(f"  餐次：{meal_data['meal_type']}")
        print(f"  备注：{meal_data['notes']}")
        print(f"  营养：{json.dumps(update_data, indent=2, ensure_ascii=False)}")
        return True
    
    # 上传数据
    success = client.update_wellness(date, update_data, locked=False)
    
    if success:
        print(f"\n✅ 饮食数据已同步到 intervals.icu")
        print(f"  日期：{date}")
        print(f"  餐次：{meal_data['meal_type']}")
        print(f"  备注：{meal_data['notes']}")
    else:
        print(f"\n❌ 上传失败")
    
    return success

def main():
    """主程序入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="饮食记录工具 - 同步到 intervals.icu")
    parser.add_argument("--text", "-t", type=str, help="自然语言描述，如'早餐吃了两个鸡蛋和全麦面包'")
    parser.add_argument("--input", "-i", type=str, help="JSON 文件路径")
    parser.add_argument("--dry-run", "-n", action="store_true", help="干跑模式（不上传）")
    parser.add_argument("--date", "-d", type=str, help="日期（YYYY-MM-DD），默认今天")
    parser.add_argument("--no-off", action="store_true", help="禁用 OpenFoodFacts API")
    parser.add_argument("--interactive", "--ask", action="store_true", help="交互式询问（无法识别时）")
    
    args = parser.parse_args()
    
    # 创建营养估算引擎
    estimator = NutritionEstimator(
        use_off_api=not args.no_off,
        interactive=args.interactive
    )
    
    # 创建 API 客户端
    client = create_client()
    if not client:
        print("❌ 无法创建 API 客户端")
        sys.exit(1)
    
    # 测试连接
    if not client.test_connection():
        print("❌ API 连接失败")
        sys.exit(1)
    
    meal_data = None
    
    # 处理 JSON 文件输入
    if args.input:
        with open(args.input) as f:
            json_data = json.load(f)
            meal_data = {
                "date": json_data.get("meal_time", args.date or datetime.now().strftime("%Y-%m-%d"))[:10],
                "meal_type": json_data.get("meal_name", "snack"),
                "notes": json_data.get("notes", ""),
                "nutrition": {
                    "calories": sum(item.get("calories", 0) for item in json_data.get("items", [])),
                    "protein": sum(item.get("protein_g", 0) for item in json_data.get("items", [])),
                    "carbs": sum(item.get("carbs_g", 0) for item in json_data.get("items", [])),
                    "fat": sum(item.get("fat_g", 0) for item in json_data.get("items", [])),
                }
            }
    
    # 处理自然语言输入
    elif args.text:
        text = args.text
        meal_type = detect_meal_type(text)
        
        # 使用新的营养估算引擎解析
        foods = estimator.parse_food_quantity(text)
        
        if not foods:
            print(f"⚠️ 未识别到食物，使用默认值")
            foods = [{"name": "混合食物", "grams": 300}]
        
        # 计算营养
        nutrition = estimator.calculate_meal_nutrition(foods)
        
        meal_data = {
            "date": args.date or datetime.now().strftime("%Y-%m-%d"),
            "meal_type": meal_type,
            "notes": text,
            "nutrition": nutrition
        }
        
        print(f"\n📝 解析结果:")
        print(f"  餐次：{meal_type}")
        print(f"  食物：{len(foods)} 种")
        for food in foods:
            print(f"    - {food['name']}: {food['grams']:.0f}g")
        
        print(f"\n🔬 营养总计:")
        print(f"    热量：{nutrition['calories']:.0f} kcal")
        print(f"    蛋白质：{nutrition['protein']:.1f}g")
        print(f"    碳水：{nutrition['carbs']:.1f}g")
        print(f"    脂肪：{nutrition['fat']:.1f}g")
        
        # 显示数据来源
        if 'sources' in nutrition:
            print(f"\n📚 数据来源:")
            for source in set(nutrition['sources']):
                print(f"    - {source}")
    
    else:
        print("❌ 请提供 --text 或 --input 参数")
        parser.print_help()
        sys.exit(1)
    
    # 上传数据
    if meal_data:
        upload_meal_to_intervals(client, meal_data, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
