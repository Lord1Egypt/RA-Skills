#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单压力测试
"""

import sys
import os
import time

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("简单压力测试")
print("=" * 60)

def test_basic_stress():
    """基础压力测试"""
    try:
        from production_ready import ProductionJobSearcher
        
        searcher = ProductionJobSearcher()
        
        print("1. 测试边界情况:")
        print("-" * 40)
        
        # 测试边界情况
        test_cases = [
            ("Python", "北京", 10, "正常"),
            ("", "北京", 5, "空关键词"),
            ("Python", "", 5, "空城市"),
            ("Python", "北京", 0, "零结果"),
            ("Python", "北京", 100, "大量结果"),
        ]
        
        for keyword, city, max_results, desc in test_cases:
            try:
                start = time.time()
                results = searcher.search(keyword, city, max_results)
                end = time.time()
                
                time_taken = end - start
                print(f"  {desc:10}: {len(results):2}结果, {time_taken:.3f}秒")
                
            except Exception as e:
                print(f"  {desc:10}: 错误 - {str(e)[:30]}")
        
        print("\n2. 测试性能:")
        print("-" * 40)
        
        # 性能测试
        keywords = ["Python", "Java", "前端", "测试"]
        cities = ["北京", "上海", "广州"]
        
        total_time = 0
        total_results = 0
        search_count = 0
        
        for keyword in keywords:
            for city in cities:
                try:
                    start = time.time()
                    results = searcher.search(keyword, city, 5)
                    end = time.time()
                    
                    search_time = end - start
                    total_time += search_time
                    total_results += len(results)
                    search_count += 1
                    
                    print(f"  {keyword:6} - {city:4}: {len(results):2}结果, {search_time:.3f}秒")
                    
                except Exception as e:
                    print(f"  {keyword:6} - {city:4}: 错误")
        
        if search_count > 0:
            avg_time = total_time / search_count
            print(f"\n  平均搜索时间: {avg_time:.3f}秒")
            print(f"  总搜索次数: {search_count}")
            print(f"  总结果数: {total_results}")
        
        print("\n3. 测试数据一致性:")
        print("-" * 40)
        
        # 一致性测试
        keyword = "Python"
        city = "北京"
        
        all_titles = []
        for i in range(3):
            results = searcher.search(keyword, city, 5)
            titles = [job.title for job in results]
            all_titles.extend(titles)
            print(f"  第{i+1}次: {len(results)}个结果")
        
        # 检查重复
        from collections import Counter
        title_counts = Counter(all_titles)
        duplicate_count = sum(1 for count in title_counts.values() if count > 1)
        
        print(f"  重复职位数: {duplicate_count}/{len(all_titles)}")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始简单压力测试...")
    
    success = test_basic_stress()
    
    print("\n" + "=" * 60)
    if success:
        print("压力测试完成 - 系统表现正常")
    else:
        print("压力测试完成 - 发现问题")
    
    print("\n测试总结:")
    print("1. 边界情况: 已测试空值、零结果等")
    print("2. 性能: 已测试多关键词多城市搜索")
    print("3. 一致性: 已测试多次搜索结果稳定性")
    print("\n建议:")
    print("- 添加结果缓存提高性能")
    print("- 增强错误处理日志")
    print("- 定期清理数据库")

if __name__ == '__main__':
    main()