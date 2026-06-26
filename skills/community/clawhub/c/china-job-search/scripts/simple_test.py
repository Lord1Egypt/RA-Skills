#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试实用版招聘搜索
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试实用版招聘搜索技能...")

try:
    from practical_searcher import PracticalJobSearcher
    
    # 创建搜索器
    searcher = PracticalJobSearcher()
    
    # 测试搜索
    print("\n1. 测试 Python 北京:")
    results = searcher.search_with_mixed_strategy("Python", "北京", max_results=10)
    
    # 简单统计
    total = sum(len(jobs) for jobs in results.values())
    real = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
    
    print(f"  找到 {total} 个岗位")
    print(f"  其中 {real} 个真实数据，{total-real} 个模拟数据")
    
    # 显示部分结果
    print("\n  部分岗位:")
    count = 0
    for platform, jobs in results.items():
        if jobs:
            print(f"  {platform}:")
            for job in jobs[:2]:  # 每个平台显示前2个
                source = "真实" if job.source == "real" else "模拟"
                print(f"    [{source}] {job.title[:20]}... | {job.salary} | {job.company[:10]}...")
                count += 1
                if count >= 4:  # 总共显示4个
                    break
        if count >= 4:
            break
    
    # 测试保存
    print("\n2. 测试保存功能:")
    filename = searcher.save_results(results, "test_output.json")
    print(f"  结果已保存到: {filename}")
    
    # 检查文件
    if os.path.exists(filename):
        import json
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  文件包含 {len(data)} 条记录")
    
    print("\n3. 测试前程无忧单独搜索:")
    qiancheng_jobs = searcher.search_qiancheng("Java", "上海", max_results=5)
    print(f"  找到 {len(qiancheng_jobs)} 个岗位")
    
    if qiancheng_jobs:
        real_count = sum(1 for job in qiancheng_jobs if job.source == "real")
        print(f"  真实数据: {real_count}, 模拟数据: {len(qiancheng_jobs)-real_count}")
        
        for i, job in enumerate(qiancheng_jobs[:2], 1):
            source = "真实" if job.source == "real" else "模拟"
            print(f"    {i}. [{source}] {job.title}")
            print(f"       公司: {job.company} | 薪资: {job.salary}")
    
    print("\n测试完成!")
    print("\n使用说明:")
    print("  命令行: python practical_searcher.py [关键词] [城市]")
    print("  示例: python practical_searcher.py Python 北京")
    print("  示例: python practical_searcher.py Java 上海")
    
except ImportError as e:
    print(f"导入失败: {e}")
    print("请确保已安装依赖: pip install requests beautifulsoup4 fake-useragent")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()