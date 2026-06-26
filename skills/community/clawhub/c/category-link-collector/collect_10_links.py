#!/usr/bin/env python3
"""
采集10个ZARA分类链接
"""

import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.collect_categories import collect_category_links

# 从页面内容中提取的10个分类链接
# 注意：这些链接是从web_fetch返回的内容中提取的
zara_links = [
    "https://zaraoutlet.top/collections/woman_1e641d06",      # 女性
    "https://zaraoutlet.top/collections/man",                 # 男性
    "https://zaraoutlet.top/collections/kids",                # 儿童
    "https://zaraoutlet.top/collections/beauty_45c3ae7a",     # 美妆
    "https://zaraoutlet.top/collections/woman-collection-blazers",  # 女性-西装外套
    "https://zaraoutlet.top/collections/woman-collection-bodies",   # 女性-连体衣
    "https://zaraoutlet.top/collections/woman-collection-cardigans-jumpers",  # 女性-开衫/套头衫
    "https://zaraoutlet.top/collections/woman-collection-co-ord-sets",  # 女性-套装
    "https://zaraoutlet.top/collections/woman-collection-dresses",  # 女性-连衣裙
    "https://zaraoutlet.top/collections/woman-collection-jackets"   # 女性-夹克
]

print("采集10个ZARA分类链接")
print("=" * 50)
print(f"链接数量: {len(zara_links)}")
print()

# 显示要采集的链接
print("要采集的链接:")
for i, link in enumerate(zara_links, 1):
    print(f"{i:2d}. {link}")

print()
print("开始采集...")

# 采集数据
output_dir = "/Users/zhangqirong/工作/caiji"
csv_path = collect_category_links(zara_links, output_dir)

print()
print("采集完成!")
print(f"CSV文件路径: {csv_path}")

# 显示采集的数据
import pandas as pd
df = pd.read_csv(csv_path)
print("\n采集的数据预览:")
print(df.to_string(index=False))

# 统计信息
print(f"\n统计信息:")
print(f"- 总记录数: {len(df)}")
print(f"- 最大分类层级: {df.filter(like='级分类').shape[1]}")
print(f"- 唯一域名: {df['域名'].nunique()}")