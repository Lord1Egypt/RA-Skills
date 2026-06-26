#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终演示 - 展示招聘搜索技能的完整功能
"""

import sys
import os
import json

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("招聘搜索技能 - 完整功能演示")
print("=" * 70)

def demo_production_version():
    """演示生产就绪版"""
    print("\n1. 演示生产就绪版 (production_ready.py)")
    print("-" * 50)
    
    try:
        from production_ready import ProductionJobSearcher
        
        # 创建搜索器
        searcher = ProductionJobSearcher()
        
        # 演示搜索
        print("搜索: Python开发工程师 - 北京")
        results = searcher.search("Python开发工程师", "北京", 10)
        
        print(f"找到 {len(results)} 个职位")
        
        if results:
            # 显示不同类型的结果
            mock_count = sum(1 for job in results if job.source == 'mock')
            manual_count = sum(1 for job in results if job.source == 'manual')
            api_count = sum(1 for job in results if job.source == 'api')
            
            print(f"  模拟数据: {mock_count} 个")
            print(f"  手动添加: {manual_count} 个")
            print(f"  API数据: {api_count} 个")
            
            # 显示前3个结果
            print("\n前3个职位:")
            for i, job in enumerate(results[:3], 1):
                source_map = {'mock': '模拟', 'manual': '手动', 'api': 'API'}
                source = source_map.get(job.source, '未知')
                print(f"  {i}. [{source}] {job.title}")
                print(f"     公司: {job.company} | 薪资: {job.salary}")
                print(f"     地点: {job.location} | 经验: {job.experience}")
        
        # 演示手动添加
        print("\n演示手动添加功能:")
        job_data = {
            'platform': '智联招聘',
            'title': '全栈开发工程师',
            'company': '某互联网公司',
            'salary': '25-45K·14薪',
            'location': '上海·浦东新区',
            'experience': '3-6年',
            'education': '本科',
            'skills': ['Python', 'React', 'Node.js', 'MySQL', 'Docker'],
            'description': '负责全栈开发，参与产品设计和架构',
            'url': 'https://www.zhaopin.com/job1',
            'posted_date': '2024-01-15'
        }
        
        job_id = searcher.add_manual_job(job_data)
        print(f"  手动添加成功，职位ID: {job_id}")
        
        # 演示导出
        print("\n演示数据导出:")
        if results:
            json_file = searcher.export_results(results, 'json')
            csv_file = searcher.export_results(results, 'csv')
            print(f"  JSON文件: {json_file}")
            print(f"  CSV文件: {csv_file}")
        
        return True
        
    except Exception as e:
        print(f"  演示失败: {e}")
        return False

def demo_final_version():
    """演示最终版"""
    print("\n2. 演示最终版 (final_searcher.py)")
    print("-" * 50)
    
    try:
        from final_searcher import FinalJobSearcher
        
        # 创建搜索器
        searcher = FinalJobSearcher()
        
        # 演示搜索
        print("搜索: Java开发 - 上海")
        results = searcher.search_with_guarantee("Java开发", "上海", 8)
        
        # 获取格式化输出
        output = searcher.format_results(results, show_details=False)
        
        # 显示部分输出
        lines = output.split('\n')
        print("\n搜索结果预览:")
        for line in lines[:15]:  # 显示前15行
            print(f"  {line}")
        
        if len(lines) > 15:
            print("  ... (更多内容)")
        
        return True
        
    except Exception as e:
        print(f"  演示失败: {e}")
        return False

def demo_practical_version():
    """演示实用版"""
    print("\n3. 演示实用版 (practical_searcher.py)")
    print("-" * 50)
    
    try:
        from practical_searcher import PracticalJobSearcher
        
        # 创建搜索器
        searcher = PracticalJobSearcher()
        
        # 演示搜索
        print("搜索: 前端开发 - 广州")
        results = searcher.search_with_mixed_strategy("前端开发", "广州", 6)
        
        # 简单统计
        total = sum(len(jobs) for jobs in results.values())
        real = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
        
        print(f"找到 {total} 个职位 ({real} 真实, {total-real} 模拟)")
        
        # 显示各平台结果
        for platform, jobs in results.items():
            if jobs:
                real_count = sum(1 for job in jobs if job.source == "real")
                print(f"  {platform}: {len(jobs)} 个 ({real_count} 真实)")
        
        return True
        
    except Exception as e:
        print(f"  演示失败: {e}")
        return False

def show_usage_summary():
    """显示使用总结"""
    print("\n" + "=" * 70)
    print("使用总结")
    print("=" * 70)
    
    print("""
推荐使用顺序:

1. 新手开始 → 使用 production_ready.py
   优点: 功能最全，支持手动添加，数据库存储
   命令: python production_ready.py Python 北京 15

2. 快速搜索 → 使用 final_searcher.py  
   优点: 保证有结果，简单直接
   命令: python final_searcher.py Java 上海

3. 基础需求 → 使用 practical_searcher.py
   优点: 轻量级，易于理解
   命令: python practical_searcher.py

在OpenClaw中集成:

```python
# 推荐方式
from skills.job_search.production_ready import ProductionJobSearcher
searcher = ProductionJobSearcher()
results = searcher.search("Python", "北京", 20)
print(searcher.format_results(results))
```

数据管理:

1. 手动添加真实职位到数据库
2. 定期导出CSV在Excel中分析
3. 根据分析结果调整搜索策略

下一步行动:

1. 立即测试: python production_ready.py "你的职位" "你的城市"
2. 手动添加5-10个真实职位
3. 集成到OpenClaw工作流中
4. 设置定时搜索任务
    """)

def main():
    """主函数"""
    print("开始演示招聘搜索技能的完整功能...")
    
    # 演示各版本
    success_count = 0
    
    if demo_production_version():
        success_count += 1
    
    if demo_final_version():
        success_count += 1
    
    if demo_practical_version():
        success_count += 1
    
    # 显示总结
    show_usage_summary()
    
    print("\n" + "=" * 70)
    print(f"演示完成: {success_count}/3 个版本演示成功")
    
    if success_count >= 2:
        print("✅ 技能准备就绪，可以开始使用!")
    else:
        print("⚠️  部分功能需要检查，请查看错误信息")
    
    print("\n立即开始:")
    print("  cd C:\\Users\\yuks\\.openclaw\\workspace\\skills\\job-search")
    print("  python production_ready.py Python 北京")
    print("=" * 70)

if __name__ == '__main__':
    main()