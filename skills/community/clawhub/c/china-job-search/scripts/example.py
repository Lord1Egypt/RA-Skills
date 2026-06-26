#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘搜索技能使用示例
"""

import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.job_search.job_searcher import JobSearcher


def example_search():
    """示例搜索"""
    print("招聘搜索技能示例")
    print("=" * 50)
    
    # 创建搜索器
    searcher = JobSearcher()
    
    # 示例1：基础搜索
    print("\n1. 基础搜索 - Python开发 北京")
    jobs = searcher.search("Python开发", "北京", max_results=10)
    print(searcher.format_results(jobs, 'simple'))
    
    # 示例2：指定平台搜索
    print("\n2. 指定平台搜索 - BOSS直聘 Java开发 上海")
    jobs = searcher.search("Java开发", "上海", platforms=['boss'], max_results=5)
    print(searcher.format_results(jobs, 'list'))
    
    # 示例3：多平台搜索
    print("\n3. 多平台搜索 - 前端开发 广州")
    jobs = searcher.search("前端开发", "广州", max_results=15)
    print(searcher.format_results(jobs, 'table'))
    
    # 示例4：高级搜索（通过参数）
    print("\n4. 高级搜索 - 测试工程师 深圳")
    jobs = searcher.search("测试工程师", "深圳", max_results=8)
    
    # 手动筛选薪资>15K的岗位
    high_salary_jobs = []
    for job in jobs:
        # 简单解析薪资
        salary_text = job.salary
        if 'K' in salary_text or 'k' in salary_text:
            # 提取数字
            import re
            numbers = re.findall(r'\d+', salary_text)
            if numbers:
                max_salary = max(map(int, numbers))
                if max_salary >= 15:
                    high_salary_jobs.append(job)
    
    print(f"找到 {len(high_salary_jobs)} 个月薪15K以上的测试岗位：")
    for job in high_salary_jobs:
        print(f"  - {job.title} | {job.company} | {job.salary} | {job.location}")


def test_platforms():
    """测试各平台连接"""
    print("\n平台连接测试")
    print("=" * 50)
    
    searcher = JobSearcher()
    
    platforms = ['boss', 'zhilian', 'qiancheng']
    test_keyword = "Python"
    test_city = "北京"
    
    for platform in platforms:
        print(f"\n测试 {platform.upper()}...")
        try:
            jobs = searcher.search(test_keyword, test_city, platforms=[platform], max_results=3)
            if jobs:
                print(f"  成功获取 {len(jobs)} 个岗位")
                for job in jobs[:2]:  # 显示前2个
                    print(f"    - {job.title[:20]}... | {job.salary}")
            else:
                print("  未获取到岗位")
        except Exception as e:
            print(f"  测试失败: {e}")


if __name__ == '__main__':
    print("招聘搜索技能演示")
    print("=" * 50)
    
    # 运行示例
    example_search()
    
    # 运行平台测试
    test_platforms()
    
    print("\n" + "=" * 50)
    print("演示完成")
    print("\n使用说明：")
    print("1. 直接运行: python job_searcher.py '关键词' -c 城市")
    print("2. 指定平台: python job_searcher.py '关键词' -p boss,zhilian")
    print("3. 设置数量: python job_searcher.py '关键词' -n 30")
    print("4. 输出格式: python job_searcher.py '关键词' -f list")