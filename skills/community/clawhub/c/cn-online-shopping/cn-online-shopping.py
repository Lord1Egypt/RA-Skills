#!/usr/bin/env python3
"""
cn-online-shopping.py - 中国电商平台购物指南 CLI

功能：
- recommend <product>: 根据商品推荐合适的中国电商平台
- categories: 列出支持的商品类别
- compare <platform1> <platform2>: 对比两个平台
"""

import json
import sys
import os
from pathlib import Path

# 获取数据目录路径
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"


def load_json(filename):
    """加载 JSON 数据文件"""
    filepath = DATA_DIR / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file '{filename}' not found at {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filename}': {e}")
        sys.exit(1)


def match_category(product_query):
    """根据商品关键词匹配类别"""
    categories_data = load_json("categories.json")
    product_lower = product_query.lower()
    
    matched_categories = []
    
    for cat_id, cat_info in categories_data["categories"].items():
        # 检查关键词匹配
        for keyword in cat_info["keywords"]:
            if keyword.lower() in product_lower:
                matched_categories.append((cat_id, cat_info))
                break
    
    return matched_categories


def get_platform_info(platform_id):
    """获取平台详细信息"""
    platforms_data = load_json("platforms.json")
    return platforms_data["platforms"].get(platform_id)


def recommend_platforms(product_query):
    """根据商品推荐平台"""
    categories_data = load_json("categories.json")
    platforms_data = load_json("platforms.json")
    
    # 匹配类别
    matched = match_category(product_query)
    
    if not matched:
        # 通用推荐
        print(f"\n🛒 购物推荐：'{product_query}'")
        print("=" * 60)
        print("\n📋 推荐平台（通用推荐）：")
        print("-" * 40)
        
        general_platforms = ["tmall", "jd", "taobao", "pdd"]
        for i, pid in enumerate(general_platforms, 1):
            platform = platforms_data["platforms"].get(pid)
            if platform:
                print(f"\n{i}. {platform['name']} ({platform['name_cn']})")
                print(f"   ⭐ 特点：{', '.join(platform['strengths'][:2])}")
                print(f"   💰 价格：{platform['price_level']} | 🚚 物流：{platform['shipping_speed']}")
        
        print("\n✅ 最佳选择：京东（综合保障最好）")
        print("\n⚠️ 注意事项：")
        print("   • 高价值商品建议选择京东自营保障售后")
        print("   • 追求低价可考虑拼多多百亿补贴")
        print("   • 注意查看店铺评分和商品评价")
        return
    
    # 使用第一个匹配的类别
    cat_id, cat_info = matched[0]
    
    print(f"\n🛒 购物推荐：'{product_query}'")
    print("=" * 60)
    print(f"\n📂 识别类别：{cat_info['name']}")
    
    print("\n📋 推荐平台：")
    print("-" * 40)
    
    recommended = cat_info["recommended_platforms"]
    for i, pid in enumerate(recommended, 1):
        platform = platforms_data["platforms"].get(pid)
        if platform:
            print(f"\n{i}. {platform['name']} ({platform['name_cn']})")
            print(f"   ⭐ 优势：{', '.join(platform['strengths'][:3])}")
            print(f"   💰 价格水平：{platform['price_level']}")
            print(f"   🚚 物流速度：{platform['shipping_speed']}")
            print(f"   🛡️ 正品保障：{platform['authenticity']}")
    
    # 最佳选择
    best = cat_info.get("best_choice", recommended[0] if recommended else "jd")
    best_platform = platforms_data["platforms"].get(best)
    if best_platform:
        print(f"\n✅ 最佳选择：{best_platform['name']} ({best_platform['name_cn']})")
        print(f"   理由：{cat_info.get('notes', '综合性价比最高')}")
    
    # 注意事项
    print("\n⚠️ 注意事项：")
    for pid in recommended:
        platform = platforms_data["platforms"].get(pid)
        if platform and platform["weaknesses"]:
            print(f"   • {platform['name']}：{platform['weaknesses'][0]}")
    
    if cat_info.get("notes"):
        print(f"   • {cat_info['notes']}")


def list_categories():
    """列出所有支持的类别"""
    categories_data = load_json("categories.json")
    
    print("\n📂 支持的购物类别：")
    print("=" * 60)
    
    # 按类别分组
    groups = {
        "服装": [],
        "电子": [],
        "家居": [],
        "其他": []
    }
    
    for cat_id, cat_info in categories_data["categories"].items():
        name = cat_info["name"]
        if any(x in cat_id for x in ["clothing", "shoes", "bags", "jewelry"]):
            groups["服装"].append(name)
        elif any(x in cat_id for x in ["electronics"]):
            groups["电子"].append(name)
        elif any(x in cat_id for x in ["home", "kitchen", "daily"]):
            groups["家居"].append(name)
        else:
            groups["其他"].append(name)
    
    for group, items in groups.items():
        if items:
            print(f"\n【{group}】")
            for item in sorted(items):
                print(f"  • {item}")
    
    print("\n💡 使用方式：")
    print(f"   python3 {sys.argv[0]} recommend <商品名称>")


def compare_platforms(p1, p2):
    """对比两个平台"""
    platforms_data = load_json("platforms.json")
    
    platform1 = platforms_data["platforms"].get(p1.lower())
    platform2 = platforms_data["platforms"].get(p2.lower())
    
    if not platform1:
        print(f"❌ 未知平台：'{p1}'")
        print(f"   支持的平台：{', '.join(platforms_data['platforms'].keys())}")
        sys.exit(1)
    
    if not platform2:
        print(f"❌ 未知平台：'{p2}'")
        print(f"   支持的平台：{', '.join(platforms_data['platforms'].keys())}")
        sys.exit(1)
    
    print(f"\n⚖️  平台对比：{platform1['name']} vs {platform2['name']}")
    print("=" * 70)
    
    # 表头
    print(f"\n{'对比项':<15} {platform1['name']:<25} {platform2['name']:<25}")
    print("-" * 70)
    
    # 各项对比
    print(f"{'中文名':<15} {platform1['name_cn']:<25} {platform2['name_cn']:<25}")
    print(f"{'价格水平':<15} {platform1['price_level']:<25} {platform2['price_level']:<25}")
    print(f"{'物流速度':<15} {platform1['shipping_speed']:<25} {platform2['shipping_speed']:<25}")
    print(f"{'正品保障':<15} {platform1['authenticity']:<25} {platform2['authenticity']:<25}")
    print(f"{'客服质量':<15} {platform1['customer_service']:<25} {platform2['customer_service']:<25}")
    print(f"{'退货政策':<15} {platform1['return_policy']:<25} {platform2['return_policy']:<25}")
    
    print(f"\n{'优势':<15}")
    print(f"  {platform1['name']}: {', '.join(platform1['strengths'])}")
    print(f"  {platform2['name']}: {', '.join(platform2['strengths'])}")
    
    print(f"\n{'劣势':<15}")
    print(f"  {platform1['name']}: {', '.join(platform1['weaknesses'])}")
    print(f"  {platform2['name']}: {', '.join(platform2['weaknesses'])}")
    
    print(f"\n{'适用场景':<15}")
    print(f"  {platform1['name']}: 适合购买 {', '.join(platform1['best_for'][:3])}")
    print(f"  {platform2['name']}: 适合购买 {', '.join(platform2['best_for'][:3])}")
    
    print(f"\n💡 选择建议：")
    # 简单的选择建议
    if platform1['price_level'] in ['极低', '低'] and platform2['price_level'] not in ['极低', '低']:
        print(f"   • 追求低价选 {platform1['name']}")
    elif platform2['price_level'] in ['极低', '低'] and platform1['price_level'] not in ['极低', '低']:
        print(f"   • 追求低价选 {platform2['name']}")
    
    if '快' in platform1['shipping_speed'] and '慢' in platform2['shipping_speed']:
        print(f"   • 追求速度选 {platform1['name']}")
    elif '快' in platform2['shipping_speed'] and '慢' in platform1['shipping_speed']:
        print(f"   • 追求速度选 {platform2['name']}")
    
    if platform1['authenticity'] == '高' and platform2['authenticity'] != '高':
        print(f"   • 追求正品保障选 {platform1['name']}")
    elif platform2['authenticity'] == '高' and platform1['authenticity'] != '高':
        print(f"   • 追求正品保障选 {platform2['name']}")


def show_help():
    """显示帮助信息"""
    print("""
🛒 全球在线购物指南

用法：
  python3 cn-online-shopping.py recommend <商品名称>   根据商品推荐平台
  python3 cn-online-shopping.py categories              列出支持的类别
  python3 cn-online-shopping.py compare <平台1> <平台2> 对比两个平台

示例：
  python3 cn-online-shopping.py recommend 手机
  python3 cn-online-shopping.py recommend iPhone case
  python3 cn-online-shopping.py compare tmall jd
  python3 cn-online-shopping.py compare taobao pdd

支持的平台：tmall, jd, taobao, pdd, douyin, xiaohongshu, suning, vip
""")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "recommend":
        if len(sys.argv) < 3:
            print("❌ 请提供商品名称")
            print(f"   用法: python3 {sys.argv[0]} recommend <商品名称>")
            sys.exit(1)
        product = " ".join(sys.argv[2:])
        recommend_platforms(product)
    
    elif command == "categories":
        list_categories()
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("❌ 请提供两个平台名称")
            print(f"   用法: python3 {sys.argv[0]} compare <平台1> <平台2>")
            print(f"   示例: python3 {sys.argv[0]} compare tmall jd")
            sys.exit(1)
        compare_platforms(sys.argv[2], sys.argv[3])
    
    elif command in ["help", "-h", "--help"]:
        show_help()
    
    else:
        print(f"❌ 未知命令: '{command}'")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()