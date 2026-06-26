#!/usr/bin/env python3
"""
测试多级分类功能
"""

import sys
sys.path.insert(0, '.')

from scripts.collect_categories import (
    parse_category_hierarchy,
    collect_category_links
)

# 测试用例 - 根据最终解析逻辑更新期望值
test_cases = [
    # (分类路径, 期望的层级)
    ("woman-collection-dresses", ["Women", "Dresses"]),
    ("woman-collection-dresses-summer", ["Women", "Dresses", "Summer"]),
    ("woman-collection-dresses-summer-2024", ["Women", "Dresses", "Summer", "2024"]),
    ("man-collection-shirts-casual", ["Men", "Shirts", "Casual"]),
    ("kids-collection-shoes-sneakers", ["Kids", "Shoes", "Sneakers"]),
    ("beauty-perfumes-women", ["Beauty", "Perfumes", "Women"]),
    ("woman-collection-co-ord-sets", ["Women", "Co-ord", "Sets"]),
    ("woman_1e641d06", ["Women", "1E641D06"]),
    ("beauty_45c3ae7a", ["Beauty", "45C3Ae7A"]),
    ("kids-baby-0-18-months-collection-sweatshirts-view-all", ["Kids", "Baby", "0-18 Months", "Sweatshirts"]),
    ("kids-baby-0-18-months", ["Kids", "Baby", "0-18 Months"]),
    ("woman-collection-t-shirts-graphic", ["Women", "T-shirts", "Graphic"]),
    ("man-collection-t-shirts-basic-cotton", ["Men", "T-shirts", "Basic", "Cotton"]),
]

print("测试多级分类解析功能")
print("=" * 60)

all_passed = True
for i, (category_path, expected) in enumerate(test_cases, 1):
    result = parse_category_hierarchy(category_path)
    
    if result == expected:
        print(f"✅ 测试 {i}: {category_path}")
        print(f"   结果: {result}")
    else:
        print(f"❌ 测试 {i}: {category_path}")
        print(f"   期望: {expected}")
        print(f"   实际: {result}")
        all_passed = False
    print()

# 测试实际链接处理
print("\n测试实际链接处理")
print("=" * 60)

test_links = [
    "https://zaraoutlet.top/collections/woman-collection-dresses-summer",
    "https://zaraoutlet.top/collections/man-collection-shirts-casual-longsleeve",
    "https://zaraoutlet.top/collections/kids-collection-shoes-sneakers-running",
    "https://zaraoutlet.top/collections/beauty-perfumes-women-floral",
    "https://zaraoutlet.top/collections/woman-collection-co-ord-sets-beach",
]

csv_path = collect_category_links(test_links)

print(f"\n生成的CSV文件: {csv_path}")

# 显示结果
import pandas as pd
df = pd.read_csv(csv_path)
print("\n处理结果:")
print(df.to_string(index=False))

if all_passed:
    print("\n✅ 所有测试通过！")
else:
    print("\n❌ 部分测试失败，请检查代码。")
    sys.exit(1)