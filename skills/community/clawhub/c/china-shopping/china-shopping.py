#!/usr/bin/env python3
"""
china-shopping - Chinese shopping website recommender
Version: 1.0.0

根据商品名称推荐最佳中国购物网站
"""

import json
import sys
import os
import argparse
from pathlib import Path

VERSION = "1.0.1"

# 数据文件路径
DATA_DIR = Path(__file__).parent / "data"
CATEGORIES_FILE = DATA_DIR / "categories.json"

# 产品关键词映射表
PRODUCT_KEYWORDS = {
    # 电子产品
    "手机": "electronics",
    "电脑": "electronics",
    "笔记本": "electronics",
    "平板": "electronics",
    "相机": "electronics",
    "耳机": "electronics",
    "数码": "electronics",
    "电视": "electronics",
    "家电": "electronics",
    "充电器": "electronics",
    "数据线": "electronics",
    "电子": "electronics",
    "智能手表": "electronics",
    "手环": "electronics",
    "游戏机": "electronics",
    "路由器": "electronics",
    "键盘": "electronics",
    "鼠标": "electronics",
    
    # 服装服饰
    "衣服": "clothing",
    "裤子": "clothing",
    "裙子": "clothing",
    "鞋子": "clothing",
    "包包": "clothing",
    "外套": "clothing",
    "T恤": "clothing",
    "衬衫": "clothing",
    "牛仔裤": "clothing",
    "运动服": "clothing",
    "内衣": "clothing",
    "袜子": "clothing",
    "帽子": "clothing",
    "围巾": "clothing",
    "手套": "clothing",
    "服装": "clothing",
    "穿搭": "clothing",
    "时装": "clothing",
    "鞋": "clothing",
    "靴": "clothing",
    "箱": "clothing",
    "包": "clothing",
    
    # 食品杂货
    "零食": "groceries",
    "水果": "groceries",
    "蔬菜": "groceries",
    "生鲜": "groceries",
    "牛奶": "groceries",
    "饮料": "groceries",
    "粮油": "groceries",
    "米": "groceries",
    "面": "groceries",
    "油": "groceries",
    "鸡蛋": "groceries",
    "肉": "groceries",
    "海鲜": "groceries",
    "面包": "groceries",
    "蛋糕": "groceries",
    "食品": "groceries",
    "食材": "groceries",
    "干货": "groceries",
    "调料": "groceries",
    "酱": "groceries",
    "醋": "groceries",
    "盐": "groceries",
    "糖": "groceries",
    "茶": "groceries",
    "咖啡": "groceries",
    "水": "groceries",
    
    # 美妆护肤
    "化妆品": "beauty",
    "护肤品": "beauty",
    "面膜": "beauty",
    "口红": "beauty",
    "粉底": "beauty",
    "眼影": "beauty",
    "香水": "beauty",
    "洗面奶": "beauty",
    "乳液": "beauty",
    "精华": "beauty",
    "面霜": "beauty",
    "眼霜": "beauty",
    "防晒": "beauty",
    "卸妆": "beauty",
    "美妆": "beauty",
    "护肤": "beauty",
    "彩妆": "beauty",
    "美甲": "beauty",
    "美发": "beauty",
    "洗发": "beauty",
    "护发": "beauty",
    "沐浴露": "beauty",
    "香皂": "beauty",
}


def load_categories():
    """加载商品分类数据"""
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到数据文件 {CATEGORIES_FILE}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：数据文件格式错误 - {e}", file=sys.stderr)
        sys.exit(1)


def match_category(product_name):
    """
    根据商品名称匹配分类
    返回分类ID或None
    """
    # 输入验证和清理
    if not product_name or not isinstance(product_name, str):
        return None
    
    # 限制长度防止异常输入
    if len(product_name) > 100:
        product_name = product_name[:100]
    
    product_lower = product_name.lower()
    
    # 直接匹配
    if product_name in PRODUCT_KEYWORDS:
        return PRODUCT_KEYWORDS[product_name]
    
    # 部分匹配（关键词包含在商品名中）
    for keyword, category in PRODUCT_KEYWORDS.items():
        if keyword in product_name or product_name in keyword:
            return category
    
    return None


def get_recommendations(product_name, categories_data, max_count=3):
    """
    获取商品推荐网站
    返回推荐的网站列表
    """
    category_id = match_category(product_name)
    
    if category_id is None:
        # 通用推荐
        return {
            "category": None,
            "category_name": "通用",
            "websites": get_general_recommendations(categories_data, max_count),
            "is_general": True
        }
    
    category_data = categories_data.get("categories", {}).get(category_id, {})
    websites = category_data.get("websites", [])
    
    # 限制推荐数量
    websites = websites[:max_count]
    
    return {
        "category": category_id,
        "category_name": category_data.get("name", "未知"),
        "icon": category_data.get("icon", "🛍️"),
        "websites": websites,
        "shopping_tips": category_data.get("shopping_tips", []),
        "is_general": False
    }


def get_general_recommendations(categories_data, max_count=3):
    """
    获取通用推荐（当无法匹配分类时）
    """
    # 从所有分类中收集高排名的网站
    all_websites = []
    seen_ids = set()
    
    for category_id, category_data in categories_data.get("categories", {}).items():
        for website in category_data.get("websites", []):
            website_id = website.get("id")
            if website_id not in seen_ids:
                seen_ids.add(website_id)
                all_websites.append(website)
    
    # 按排名排序并限制数量
    all_websites.sort(key=lambda x: x.get("rank", 999))
    return all_websites[:max_count]


def format_output(result, product_name):
    """
    格式化输出推荐结果
    """
    lines = []
    
    if result["is_general"]:
        lines.append(f"🛍️  {product_name} 推荐购物网站：")
        lines.append("")
        lines.append("💡 未找到该产品的具体分类，以下是通用购物平台推荐：")
    else:
        icon = result.get("icon", "🛍️")
        category_name = result["category_name"]
        lines.append(f"{icon} {product_name} ({category_name}) 推荐购物网站：")
    
    lines.append("")
    
    for i, website in enumerate(result["websites"], 1):
        name = website.get("name", "未知")
        reason = website.get("reason", "")
        url = website.get("url", "")
        tags = website.get("tags", [])
        
        if url:
            lines.append(f"{i}. {name} ({url})")
        else:
            lines.append(f"{i}. {name}")
        
        if reason:
            lines.append(f"   └─ {reason}")
        
        if tags:
            lines.append(f"   🏷️  {' | '.join(tags)}")
        
        lines.append("")
    
    # 添加购物提示
    if not result["is_general"] and result.get("shopping_tips"):
        lines.append("💡 购物提示：")
        for tip in result["shopping_tips"][:3]:  # 最多显示3条提示
            lines.append(f"   • {tip}")
        lines.append("")
    
    return "\n".join(lines)


def format_json_output(result, product_name):
    """
    格式化输出为JSON
    """
    output = {
        "product": product_name,
        "category": result["category_name"],
        "is_general": result["is_general"],
        "recommendations": []
    }
    
    for website in result["websites"]:
        output["recommendations"].append({
            "name": website.get("name"),
            "url": website.get("url"),
            "reason": website.get("reason"),
            "tags": website.get("tags", [])
        })
    
    return json.dumps(output, ensure_ascii=False, indent=2)


def list_categories(categories_data):
    """
    列出所有支持的商品类别
    """
    lines = []
    lines.append("🛍️  支持的产品类别：")
    lines.append("")
    
    for category_id, category_data in categories_data.get("categories", {}).items():
        icon = category_data.get("icon", "📦")
        name = category_data.get("name", category_id)
        description = category_data.get("description", "")
        lines.append(f"  {icon} {name}")
        lines.append(f"     └─ {description}")
        lines.append("")
    
    lines.append("💡 使用示例: china-shopping recommend \"手机\"")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="中国购物网站推荐工具 - 根据商品推荐最佳购物网站",
        prog="china-shopping"
    )
    
    parser.add_argument(
        "command",
        choices=["recommend", "推荐", "categories", "help"],
        nargs="?",
        default="help",
        help="命令: recommend/推荐 <商品>, categories, help"
    )
    
    parser.add_argument(
        "product",
        nargs="?",
        help="商品名称（用于 recommend 命令）"
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=3,
        help="推荐网站数量（默认: 3）"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式（默认: text）"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"china-shopping v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # 加载数据
    data = load_categories()
    
    if args.command in ["recommend", "推荐"]:
        if not args.product:
            print("错误：请提供商品名称", file=sys.stderr)
            print("用法: china-shopping recommend <商品名称>", file=sys.stderr)
            sys.exit(1)
        
        # 输入验证
        product = args.product.strip()
        if len(product) > 50:
            print("错误：产品名称过长（最多50个字符）", file=sys.stderr)
            sys.exit(1)
        
        # 检查危险字符
        dangerous_chars = ['<', '>', '|', '&', ';', '$', '`', '\\', '\x00']
        for char in dangerous_chars:
            if char in product:
                print("错误：产品名称包含无效字符", file=sys.stderr)
                sys.exit(1)
        
        result = get_recommendations(product, data, args.count)
        
        if args.format == "json":
            print(format_json_output(result, product))
        else:
            print(format_output(result, product))
    
    elif args.command == "categories":
        print(list_categories(data))
    
    else:  # help
        parser.print_help()
        print("\n示例:")
        print("  china-shopping recommend \"手机\"")
        print("  china-shopping 推荐 \"衣服\"")
        print("  china-shopping categories")
        print("  china-shopping recommend \"化妆品\" --format json")


if __name__ == "__main__":
    main()
