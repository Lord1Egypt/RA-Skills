#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试最终版招聘搜索技能
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试最终版招聘搜索技能...")
print("=" * 60)

try:
    from final_searcher import FinalJobSearcher
    
    # 创建搜索器
    searcher = FinalJobSearcher()
    
    # 测试用例
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州"),
        ("测试工程师", "深圳"),
        ("运维", "杭州"),
    ]
    
    for keyword, city in test_cases:
        print(f"\n测试: {keyword} - {city}")
        print("-" * 40)
        
        # 执行搜索
        results = searcher.search_with_guarantee(keyword, city, max_results=12)
        
        # 统计
        total = sum(len(jobs) for jobs in results.values())
        real = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
        
        print(f"结果: {total} 个岗位 ({real} 真实, {total-real} 模拟)")
        
        # 显示各平台结果
        for platform, jobs in results.items():
            if jobs:
                real_count = sum(1 for job in jobs if job.source == "real")
                print(f"  {platform}: {len(jobs)} 个 ({real_count} 真实)")
    
    # 测试保存功能
    print("\n" + "=" * 60)
    print("测试保存功能...")
    
    # 执行一次搜索
    results = searcher.search_with_guarantee("Python", "北京", 10)
    
    # 保存为JSON
    json_file = searcher.save_results(results, "test_final.json")
    
    # 保存为CSV
    csv_file = searcher.export_to_csv(results, "test_final.csv")
    
    # 检查文件
    if os.path.exists(json_file):
        import json
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"JSON文件包含 {len(data)} 条记录")
    
    if os.path.exists(csv_file):
        import csv
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        print(f"CSV文件包含 {len(rows)-1} 条记录（含标题行）")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("\n使用说明:")
    print("  1. 命令行使用: python final_searcher.py [关键词] [城市] [数量]")
    print("     示例: python final_searcher.py Python 北京 20")
    print("     示例: python final_searcher.py Java 上海")
    print("  2. 在OpenClaw中集成:")
    print("     from skills.job_search.final_searcher import FinalJobSearcher")
    print("     searcher = FinalJobSearcher()")
    print("     results = searcher.search_with_guarantee('Python', '北京', 15)")
    print("  3. 输出格式: JSON和CSV，便于进一步处理")
    
except ImportError as e:
    print(f"导入失败: {e}")
    print("请安装依赖: pip install requests beautifulsoup4 fake-useragent")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()