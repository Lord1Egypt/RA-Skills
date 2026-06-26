#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试生产就绪版招聘搜索
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试生产就绪版招聘搜索技能...")
print("=" * 60)

try:
    from production_ready import ProductionJobSearcher
    
    # 创建搜索器
    searcher = ProductionJobSearcher()
    
    print("1. 测试基本搜索功能:")
    print("-" * 40)
    
    # 测试搜索
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州"),
        ("数据分析", "深圳"),
    ]
    
    for keyword, city in test_cases:
        print(f"\n搜索: {keyword} - {city}")
        results = searcher.search(keyword, city, max_results=8)
        
        print(f"  找到 {len(results)} 个职位")
        
        if results:
            # 显示前2个结果
            for i, job in enumerate(results[:2], 1):
                source = {'mock': '模拟', 'manual': '手动', 'api': 'API'}.get(job.source, '未知')
                print(f"  {i}. [{source}] {job.title}")
                print(f"     公司: {job.company} | 薪资: {job.salary}")
                print(f"     地点: {job.location} | 技能: {', '.join(job.skills[:3])}")
    
    print("\n2. 测试手动添加功能:")
    print("-" * 40)
    
    # 手动添加一个职位
    manual_job = {
        'platform': 'BOSS直聘',
        'title': '高级Python开发工程师',
        'company': '某科技公司',
        'salary': '30-50K·15薪',
        'location': '北京·朝阳区',
        'experience': '5-8年',
        'education': '本科',
        'skills': ['Python', 'Django', 'Redis', '微服务', 'K8s'],
        'description': '负责核心业务系统开发，参与架构设计和技术选型',
        'url': 'https://www.zhipin.com/job1',
        'posted_date': '2024-01-01'
    }
    
    job_id = searcher.add_manual_job(manual_job)
    print(f"  手动添加职位成功，ID: {job_id}")
    
    # 搜索手动添加的职位
    print("\n3. 搜索手动添加的职位:")
    print("-" * 40)
    
    results = searcher.search("高级Python", "北京", max_results=5)
    manual_count = sum(1 for job in results if job.source == 'manual')
    print(f"  找到 {len(results)} 个职位，其中 {manual_count} 个手动添加")
    
    print("\n4. 测试导出功能:")
    print("-" * 40)
    
    # 执行一次搜索并导出
    results = searcher.search("开发工程师", "全国", max_results=10)
    
    # 导出为JSON
    json_file = searcher.export_results(results, 'json')
    print(f"  JSON导出: {json_file}")
    
    # 导出为CSV
    csv_file = searcher.export_results(results, 'csv')
    print(f"  CSV导出: {csv_file}")
    
    # 检查文件
    if os.path.exists(json_file):
        import json
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  JSON文件包含 {len(data)} 条记录")
    
    if os.path.exists(csv_file):
        import csv
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        print(f"  CSV文件包含 {len(rows)-1} 条数据记录（含标题）")
    
    print("\n5. 查看统计信息:")
    print("-" * 40)
    
    stats = searcher.get_stats()
    print(f"  数据库总职位数: {stats['total_jobs']}")
    print(f"  模拟职位: {stats['mock_jobs']}")
    print(f"  手动添加职位: {stats['manual_jobs']}")
    print(f"  API职位: {stats['api_jobs']}")
    print(f"  最后更新时间: {stats['last_updated']}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("\n使用说明:")
    print("  1. 命令行搜索: python production_ready.py Python 北京 20")
    print("  2. 手动添加职位: searcher.add_manual_job(job_data)")
    print("  3. 导出数据: searcher.export_results(results, 'csv')")
    print("\n优势:")
    print("  ✓ 始终有结果（模拟数据保证）")
    print("  ✓ 可手动添加真实职位")
    print("  ✓ 支持JSON/CSV导出")
    print("  ✓ 易于扩展真实API")
    
except ImportError as e:
    print(f"导入失败: {e}")
    print("请安装依赖: pip install requests beautifulsoup4 fake-useragent")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()