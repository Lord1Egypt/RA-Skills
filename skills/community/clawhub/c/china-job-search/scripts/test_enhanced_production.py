#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强版生产就绪招聘搜索器
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试增强版生产就绪招聘搜索器")
print("=" * 70)

try:
    from enhanced_production_searcher import EnhancedProductionSearcher
    
    # 创建搜索器
    searcher = EnhancedProductionSearcher()
    
    print("1. 测试基本搜索功能:")
    print("-" * 50)
    
    # 测试搜索
    test_cases = [
        ("Python", "北京", 10, 0),
        ("Java", "上海", 8, 20),
        ("前端", "深圳", 6, 15),
        ("数据分析", "杭州", 8, 0),
        ("机器学习", "全国", 5, 25),
    ]
    
    for keyword, city, max_results, min_salary in test_cases:
        print(f"\n搜索: {keyword} - {city}")
        if min_salary > 0:
            print(f"最低薪资: {min_salary}K")
        
        results = searcher.search(keyword, city, max_results, min_salary=min_salary)
        
        print(f"找到 {len(results)} 个职位")
        
        if results:
            # 显示匹配分数统计
            avg_score = sum(job.match_score for job in results) / len(results)
            print(f"平均匹配分数: {avg_score:.2f}")
            
            # 显示前2个结果
            for i, job in enumerate(results[:2], 1):
                source = {'mock': '模拟', 'manual': '手动', 'api': 'API'}.get(job.source, '未知')
                print(f"  {i}. [{source}] {job.title} (分数: {job.match_score:.2f})")
                print(f"     公司: {job.company} | 薪资: {job.salary}")
                print(f"     地点: {job.location} | 类别: {job.category}")
    
    print("\n2. 测试城市薪资调整:")
    print("-" * 50)
    
    # 测试同一职位在不同城市的薪资
    keyword = "Python开发"
    cities = ["北京", "上海", "广州", "成都"]
    
    for city in cities:
        results = searcher.search(keyword, city, 3)
        if results:
            salaries = []
            for job in results:
                # 提取薪资数字
                import re
                numbers = re.findall(r'\d+', job.salary)
                if numbers:
                    avg = sum(map(int, numbers)) / len(numbers)
                    salaries.append(avg)
            
            if salaries:
                avg_salary = sum(salaries) / len(salaries)
                print(f"  {city}: 平均薪资 {avg_salary:.1f}K")
    
    print("\n3. 测试技能匹配:")
    print("-" * 50)
    
    # 测试不同技能的匹配
    skills = ["React", "Docker", "机器学习", "微服务"]
    
    for skill in skills:
        results = searcher.search(skill, "全国", 4)
        if results:
            avg_score = sum(job.match_score for job in results) / len(results)
            print(f"  {skill:10} -> {len(results)} 个职位，平均匹配分数: {avg_score:.2f}")
            
            # 显示技能分布
            all_skills = []
            for job in results:
                all_skills.extend(job.skills)
            
            from collections import Counter
            skill_counter = Counter(all_skills)
            if skill_counter:
                top_skills = skill_counter.most_common(3)
                print(f"    相关技能: {', '.join([s for s, _ in top_skills])}")
    
    print("\n4. 测试导出功能:")
    print("-" * 50)
    
    # 执行一次搜索并导出
    results = searcher.search("开发工程师", "全国", 12)
    
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
        if data:
            print(f"  第一条记录匹配分数: {data[0].get('match_score', 0):.2f}")
    
    if os.path.exists(csv_file):
        import csv
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        print(f"  CSV文件包含 {len(rows)-1} 条数据记录（含标题）")
    
    print("\n5. 查看系统统计:")
    print("-" * 50)
    
    stats = searcher.get_stats()
    print(f"  数据库总职位数: {stats['total_jobs']}")
    print(f"  模拟职位: {stats['mock_jobs']}")
    print(f"  手动添加职位: {stats['manual_jobs']}")
    print(f"  模拟类别: {stats['mock_categories']} 类")
    print(f"  模拟职位总数: {stats['total_mock_jobs']} 个")
    print(f"  技能分类: {stats['skill_categories']} 类")
    print(f"  技能总数: {stats['total_skills']} 种")
    
    print("\n" + "=" * 70)
    print("测试完成!")
    print("\n增强功能总结:")
    print("  ✓ 城市薪资自动调整")
    print("  ✓ 智能匹配分数计算")
    print("  ✓ 多条件筛选（薪资、经验）")
    print("  ✓ 技能分类和匹配")
    print("  ✓ 增强的模拟数据系统")
    
    print("\n使用说明:")
    print("  命令行: python enhanced_production_searcher.py Python 北京 15 20")
    print("  参数: 关键词 城市 数量 最低薪资(K)")
    print("  示例: python enhanced_production_searcher.py Java 上海 10 25")
    
except ImportError as e:
    print(f"导入失败: {e}")
    print("请确保已安装依赖并运行了 enhance_mock_data.py")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()