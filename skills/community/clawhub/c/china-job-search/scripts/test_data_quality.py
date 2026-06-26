#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据质量和覆盖率
"""

import sys
import os
import json
from collections import Counter

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试招聘搜索技能的数据质量和覆盖率")
print("=" * 70)

def test_mock_data_coverage():
    """测试模拟数据覆盖率"""
    print("\n1. 测试模拟数据覆盖率")
    print("-" * 50)
    
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        # 测试关键词
        test_keywords = [
            "Python", "Java", "前端", "后端", "测试", "运维",
            "数据分析", "机器学习", "人工智能", "大数据",
            "产品经理", "UI设计", "运营", "市场"
        ]
        
        print("测试关键词覆盖率:")
        for keyword in test_keywords:
            results = searcher.search(keyword, "全国", 5, use_mock=True)
            mock_count = sum(1 for job in results if job.source == 'mock')
            print(f"  {keyword:10} -> {len(results)} 个结果 ({mock_count} 模拟)")
    
    except Exception as e:
        print(f"测试失败: {e}")

def test_city_coverage():
    """测试城市覆盖率"""
    print("\n2. 测试城市覆盖率")
    print("-" * 50)
    
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安", "重庆"]
    
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        print("测试各城市搜索结果:")
        for city in cities:
            results = searcher.search("开发工程师", city, 5)
            print(f"  {city:4} -> {len(results)} 个职位")
            
            if results:
                # 显示薪资范围
                salaries = []
                for job in results:
                    # 提取薪资数字
                    import re
                    numbers = re.findall(r'\d+', job.salary)
                    if numbers:
                        salaries.extend(map(int, numbers))
                
                if salaries:
                    avg = sum(salaries) / len(salaries)
                    print(f"        平均薪资: {avg:.1f}K")
    
    except Exception as e:
        print(f"测试失败: {e}")

def test_skill_coverage():
    """测试技能标签覆盖率"""
    print("\n3. 测试技能标签覆盖率")
    print("-" * 50)
    
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        # 搜索几个常见职位
        keywords = ["Python", "Java", "前端", "测试"]
        all_skills = []
        
        for keyword in keywords:
            results = searcher.search(keyword, "全国", 10)
            
            for job in results:
                all_skills.extend(job.skills)
        
        # 统计技能出现频率
        skill_counter = Counter(all_skills)
        
        print(f"总共收集到 {len(all_skills)} 个技能标签")
        print(f"去重后 {len(skill_counter)} 种不同技能")
        
        print("\n最常出现的技能:")
        for skill, count in skill_counter.most_common(15):
            print(f"  {skill:15} -> {count:2} 次")
    
    except Exception as e:
        print(f"测试失败: {e}")

def test_salary_distribution():
    """测试薪资分布"""
    print("\n4. 测试薪资分布")
    print("-" * 50)
    
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        # 测试不同职位的薪资
        positions = [
            ("Python开发", "Python"),
            ("Java开发", "Java"),
            ("前端开发", "前端"),
            ("测试工程师", "测试"),
            ("运维工程师", "运维")
        ]
        
        print("各职位薪资分布:")
        for position_name, keyword in positions:
            results = searcher.search(keyword, "北京", 8)
            
            if results:
                salaries = []
                for job in results:
                    import re
                    numbers = re.findall(r'\d+', job.salary)
                    if numbers:
                        # 取薪资范围的上限
                        max_salary = max(map(int, numbers))
                        salaries.append(max_salary)
                
                if salaries:
                    avg = sum(salaries) / len(salaries)
                    min_s = min(salaries)
                    max_s = max(salaries)
                    print(f"  {position_name:8} -> {min_s:2}-{max_s:2}K (平均: {avg:.1f}K)")
                else:
                    print(f"  {position_name:8} -> 无薪资数据")
    
    except Exception as e:
        print(f"测试失败: {e}")

def test_performance():
    """测试性能"""
    print("\n5. 测试性能")
    print("-" * 50)
    
    import time
    
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        # 测试搜索速度
        test_cases = [
            ("Python", "北京"),
            ("Java", "上海"),
            ("前端", "广州"),
            ("测试", "深圳")
        ]
        
        total_time = 0
        total_results = 0
        
        for keyword, city in test_cases:
            start_time = time.time()
            results = searcher.search(keyword, city, 10)
            end_time = time.time()
            
            search_time = end_time - start_time
            total_time += search_time
            total_results += len(results)
            
            print(f"  {keyword:6} - {city:4}: {len(results):2} 个结果, 耗时: {search_time:.2f}秒")
        
        avg_time = total_time / len(test_cases)
        avg_results = total_results / len(test_cases)
        
        print(f"\n平均每次搜索: {avg_time:.2f}秒, {avg_results:.1f}个结果")
        
        # 测试数据库加载速度
        print("\n测试数据库性能:")
        start_time = time.time()
        searcher2 = ProductionJobSearcher()
        end_time = time.time()
        print(f"  数据库加载: {end_time - start_time:.3f}秒")
        print(f"  数据库记录: {searcher2.stats['total_jobs']} 条")
    
    except Exception as e:
        print(f"测试失败: {e}")

def generate_improvement_report():
    """生成改进报告"""
    print("\n" + "=" * 70)
    print("数据质量改进报告")
    print("=" * 70)
    
    report = """
基于测试结果，建议的改进方向:

1. 数据丰富度改进:
   - 添加更多职位类别（产品、设计、运营等）
   - 增加更多技能标签
   - 完善各城市的薪资数据

2. 数据准确性改进:
   - 定期更新模拟数据，反映市场变化
   - 添加更多真实职位到数据库
   - 验证薪资数据的合理性

3. 性能优化:
   - 优化数据库查询速度
   - 添加缓存机制
   - 并行处理多个搜索

4. 功能扩展:
   - 添加高级筛选功能（薪资范围、经验要求等）
   - 实现职位对比功能
   - 添加收藏和关注功能

5. 用户体验:
   - 改进输出格式，更易阅读
   - 添加交互式搜索界面
   - 提供数据可视化图表

立即行动建议:
1. 手动添加20-30个真实职位到数据库
2. 扩展模拟数据覆盖更多职位类型
3. 测试并优化搜索性能
    """
    
    print(report)
    
    # 保存报告
    with open('data_quality_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("报告已保存到: data_quality_report.txt")

def main():
    """主函数"""
    print("开始测试数据质量和覆盖率...")
    
    # 执行各项测试
    test_mock_data_coverage()
    test_city_coverage()
    test_skill_coverage()
    test_salary_distribution()
    test_performance()
    
    # 生成改进报告
    generate_improvement_report()
    
    print("\n" + "=" * 70)
    print("数据质量测试完成")
    print("=" * 70)
    
    print("\n下一步:")
    print("1. 查看 data_quality_report.txt 获取改进建议")
    print("2. 根据报告改进模拟数据和数据库")
    print("3. 进行第二轮测试验证改进效果")

if __name__ == '__main__':
    main()