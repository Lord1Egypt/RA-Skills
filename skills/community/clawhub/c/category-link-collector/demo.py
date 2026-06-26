#!/usr/bin/env python3
"""
Category Link Collector 技能演示
"""

import sys
import os
import pandas as pd

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.collect_categories import (
    extract_domain,
    extract_category_path,
    parse_category_hierarchy,
    collect_category_links
)

def demo_parsing():
    """演示分类路径解析"""
    print("=" * 60)
    print("分类路径解析演示")
    print("=" * 60)
    
    test_cases = [
        "woman-collection-dresses-summer",
        "man-collection-shirts-casual-longsleeve",
        "kids-collection-shoes-sneakers-running",
        "beauty-perfumes-women-floral",
        "woman-collection-co-ord-sets-beach",
        "kids-baby-0-18-months-collection-sweatshirts",
        "woman-collection-t-shirts-graphic-design",
    ]
    
    for path in test_cases:
        hierarchy = parse_category_hierarchy(path)
        print(f"\n分类路径: {path}")
        print(f"解析结果: {hierarchy}")
        print(f"层级数: {len(hierarchy)}")

def demo_full_processing():
    """演示完整处理流程"""
    print("\n" + "=" * 60)
    print("完整处理流程演示")
    print("=" * 60)
    
    # 模拟电商网站分类链接
    links = [
        "https://fashionstore.com/collections/women-clothing-dresses-summer-cotton",
        "https://fashionstore.com/collections/men-accessories-watches-digital-smart",
        "https://fashionstore.com/collections/kids-toys-educational-science-chemistry",
        "https://fashionstore.com/collections/home-living-furniture-sofas-leather",
        "https://fashionstore.com/collections/sports-fitness-equipment-weights-dumbbells",
    ]
    
    print(f"\n处理 {len(links)} 个分类链接...")
    
    # 处理链接
    csv_path = collect_category_links(links)
    
    print(f"\n生成的CSV文件: {csv_path}")
    
    # 显示结果
    df = pd.read_csv(csv_path)
    print("\n处理结果:")
    print(df.to_string(index=False))
    
    # 统计信息
    print("\n统计信息:")
    print(f"- 总链接数: {len(df)}")
    print(f"- 最大分类层级: {df.filter(like='级分类').shape[1]}")
    print(f"- 涉及域名: {df['域名'].unique().tolist()}")

def demo_url_parsing():
    """演示URL解析"""
    print("\n" + "=" * 60)
    print("URL解析演示")
    print("=" * 60)
    
    urls = [
        "https://example.com/collections/women-dresses-summer",
        "https://shop.test/collections/men-shirts-formal",
        "https://store.demo/collections/kids-shoes-sneakers",
    ]
    
    for url in urls:
        domain = extract_domain(url)
        category_path = extract_category_path(url)
        hierarchy = parse_category_hierarchy(category_path)
        
        print(f"\nURL: {url}")
        print(f"  域名: {domain}")
        print(f"  分类路径: {category_path}")
        print(f"  分类层级: {hierarchy}")

def main():
    """主函数"""
    print("🦞 Category Link Collector 技能演示")
    print("支持多级分类提取的电商链接采集工具")
    
    demo_parsing()
    demo_url_parsing()
    demo_full_processing()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n技能特点:")
    print("✅ 支持无限级分类提取")
    print("✅ 动态生成CSV列")
    print("✅ 智能解析特殊格式")
    print("✅ 批量处理支持")
    print("✅ 自定义输出目录")

if __name__ == "__main__":
    main()