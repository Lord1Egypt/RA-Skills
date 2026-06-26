#!/usr/bin/env python3
"""
测试ZARA网站分类链接采集
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.collect_categories import collect_category_links

# 测试链接 - 从zaraoutlet.top网站提取的两个分类链接
test_links = [
    "https://zaraoutlet.top/collections/woman_1e641d06",
    "https://zaraoutlet.top/collections/man"
]

print("测试ZARA网站分类链接采集")
print("=" * 50)
print(f"测试链接数量: {len(test_links)}")
print()

# 采集数据
output_dir = "/Users/zhangqirong/工作/caiji"
csv_path = collect_category_links(test_links, output_dir)

print()
print("测试完成!")
print(f"CSV文件路径: {csv_path}")

# 显示采集的数据
import pandas as pd
df = pd.read_csv(csv_path)
print("\n采集的数据:")
print(df.to_string(index=False))