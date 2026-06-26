#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试增强版
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("快速测试增强版招聘搜索")
print("=" * 60)

try:
    from enhanced_production_searcher import EnhancedProductionSearcher
    
    # 创建搜索器
    searcher = EnhancedProductionSearcher()
    
    # 简单测试
    print("\n测试1: Python开发 - 北京")
    results = searcher.search("Python开发", "北京", 5)
    print(f"找到 {len(results)} 个职位")
    
    if results:
        for i, job in enumerate(results[:3], 1):
            print(f"  {i}. {job.title}")
            print(f"     薪资: {job.salary} | 地点: {job.location}")
            print(f"     匹配分数: {job.match_score:.2f} | 类别: {job.category}")
    
    print("\n测试2: Java - 上海 (最低薪资20K)")
    results = searcher.search("Java", "上海", 4, min_salary=20)
    print(f"找到 {len(results)} 个职位")
    
    print("\n测试3: 前端 - 全国")
    results = searcher.search("前端", "全国", 3)
    print(f"找到 {len(results)} 个职位")
    
    # 显示统计
    stats = searcher.get_stats()
    print(f"\n系统统计:")
    print(f"  总职位数: {stats['total_jobs']}")
    print(f"  模拟职位: {stats['mock_jobs']}")
    print(f"  模拟类别: {stats['mock_categories']}")
    
    print("\n测试完成!")
    print("\n使用: python enhanced_production_searcher.py 关键词 城市 数量 最低薪资")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()