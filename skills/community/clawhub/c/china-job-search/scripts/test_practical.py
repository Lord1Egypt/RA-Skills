#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实用版招聘搜索技能
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from practical_searcher import PracticalJobSearcher


def test_practical_search():
    """测试实用搜索"""
    print("=" * 70)
    print("测试实用版招聘搜索技能")
    print("=" * 70)
    
    # 创建搜索器
    searcher = PracticalJobSearcher()
    
    # 测试用例
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州"),
        ("测试", "深圳"),
    ]
    
    for keyword, city in test_cases:
        print(f"\n{'='*70}")
        print(f"测试搜索: {keyword} - {city}")
        print(f"{'='*70}")
        
        try:
            # 执行混合策略搜索
            results = searcher.search_with_mixed_strategy(keyword, city, max_results=15)
            
            # 格式化输出
            output = searcher.format_results(results)
            print(output)
            
            # 保存结果
            filename = searcher.save_results(results, f"test_{keyword}_{city}.json")
            print(f"详细结果已保存到: {filename}")
            
            # 显示统计信息
            total_jobs = sum(len(jobs) for jobs in results.values())
            real_jobs = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
            
            print(f"\n搜索统计:")
            print(f"  关键词: {keyword}")
            print(f"  地点: {city}")
            print(f"  总岗位数: {total_jobs}")
            print(f"  真实数据: {real_jobs}")
            print(f"  模拟数据: {total_jobs - real_jobs}")
            
        except Exception as e:
            print(f"搜索失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 等待一下
        import time
        time.sleep(2)


def test_individual_platforms():
    """测试各平台单独搜索"""
    print("\n" + "=" * 70)
    print("测试各平台单独搜索")
    print("=" * 70)
    
    searcher = PracticalJobSearcher()
    
    # 测试前程无忧（最可能工作的平台）
    print("\n1. 测试前程无忧（真实数据）:")
    print("-" * 50)
    
    try:
        jobs = searcher.search_qiancheng("Python", "北京", max_results=5)
        print(f"找到 {len(jobs)} 个岗位")
        
        real_count = sum(1 for job in jobs if job.source == "real")
        print(f"  真实数据: {real_count}")
        print(f"  备用数据: {len(jobs) - real_count}")
        
        if jobs:
            print("\n前3个岗位:")
            for i, job in enumerate(jobs[:3], 1):
                source = "真实" if job.source == "real" else "模拟"
                print(f"  {i}. [{source}] {job.title}")
                print(f"     公司: {job.company} | 薪资: {job.salary}")
                print(f"     地点: {job.location}")
        
    except Exception as e:
        print(f"前程无忧搜索失败: {e}")
    
    # 测试模拟数据
    print("\n2. 测试模拟数据备用方案:")
    print("-" * 50)
    
    try:
        # 获取备用数据
        fallback_jobs = searcher._get_fallback_data("Python", "北京", "BOSS直聘", 3)
        print(f"生成 {len(fallback_jobs)} 个模拟岗位")
        
        for i, job in enumerate(fallback_jobs, 1):
            print(f"  {i}. {job.title}")
            print(f"     公司: {job.company} | 薪资: {job.salary}")
            print(f"     技能: {', '.join(job.skills[:3])}")
        
    except Exception as e:
        print(f"模拟数据生成失败: {e}")


def demo_usage():
    """演示使用方式"""
    print("\n" + "=" * 70)
    print("使用方式演示")
    print("=" * 70)
    
    print("""
1. 基础使用:
   ```python
   from practical_searcher import PracticalJobSearcher
   
   searcher = PracticalJobSearcher()
   results = searcher.search_with_mixed_strategy("Python", "北京", 20)
   output = searcher.format_results(results)
   print(output)
   ```

2. 保存结果:
   ```python
   filename = searcher.save_results(results, "my_jobs.json")
   ```

3. 单独搜索前程无忧:
   ```python
   jobs = searcher.search_qiancheng("Java", "上海", 10)
   ```

4. 命令行使用:
   ```bash
   python practical_searcher.py
   ```

5. 在OpenClaw中集成:
   ```python
   # 在OpenClaw工作区创建脚本
   import sys
   sys.path.append("skills/job-search")
   from practical_searcher import PracticalJobSearcher
   
   def search_jobs(keyword, city="北京"):
       searcher = PracticalJobSearcher()
       return searcher.search_with_mixed_strategy(keyword, city, 20)
   ```
    """)


def main():
    """主函数"""
    print("开始测试实用版招聘搜索技能...")
    
    # 测试实用搜索
    test_practical_search()
    
    # 测试各平台
    test_individual_platforms()
    
    # 演示使用方式
    demo_usage()
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
    
    print("""
总结:
1. 当前版本使用混合策略:
   - 优先获取前程无忧的真实数据
   - 其他平台使用模拟数据作为备用
   - 确保始终有结果返回

2. 下一步优化:
   - 添加BOSS直聘的真实搜索（需要处理反爬）
   - 添加智联招聘的真实搜索
   - 实现Selenium浏览器自动化
   - 添加更多筛选条件

3. 立即使用:
   - 运行: python test_practical.py
   - 查看生成的JSON文件获取详细数据
   - 集成到OpenClaw工作流中
    """)


if __name__ == '__main__':
    main()