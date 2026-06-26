#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘搜索技能测试
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openclaw_integration import JobSearchSkill


def test_basic_commands():
    """测试基本命令"""
    print("=" * 60)
    print("招聘搜索技能测试")
    print("=" * 60)
    
    skill = JobSearchSkill()
    
    # 测试1：基础搜索命令
    print("\n1. 测试基础搜索命令...")
    result = skill.handle_command("搜索 Python 北京")
    print(f"结果长度: {len(result)} 字符")
    print(f"结果预览: {result[:200]}...")
    
    # 测试2：指定平台搜索
    print("\n2. 测试指定平台搜索...")
    result = skill.handle_command("搜索 boss Java 上海")
    print(f"结果长度: {len(result)} 字符")
    
    # 测试3：获取统计信息
    print("\n3. 测试统计功能...")
    stats = skill.get_stats()
    print(f"找到岗位总数: {stats.get('total', 0)}")
    print(f"平台分布: {stats.get('platforms', {})}")
    
    # 测试4：导出功能
    print("\n4. 测试导出功能...")
    export_result = skill.export_results('json')
    if export_result and not export_result.startswith("没有"):
        print("导出成功")
        # 保存测试文件
        with open('test_export.json', 'w', encoding='utf-8') as f:
            f.write(export_result)
        print("测试文件已保存: test_export.json")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


def test_platform_parsers():
    """测试各平台解析器"""
    print("\n测试各平台解析器...")
    
    from job_searcher import JobSearcher
    
    searcher = JobSearcher()
    
    platforms = ['boss', 'zhilian', 'qiancheng']
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州")
    ]
    
    for platform in platforms:
        print(f"\n{platform.upper()} 解析器测试:")
        
        for keyword, city in test_cases[:1]:  # 只测试第一个用例
            try:
                print(f"  搜索: {keyword} - {city}")
                jobs = searcher.search(keyword, city, platforms=[platform], max_results=3)
                
                if jobs:
                    print(f"  成功获取 {len(jobs)} 个岗位")
                    for job in jobs[:2]:  # 显示前2个
                        print(f"    - {job.title[:30]}... | {job.salary} | {job.company[:20]}")
                else:
                    print("  未获取到岗位")
                    
            except Exception as e:
                print(f"  错误: {e}")


if __name__ == '__main__':
    test_basic_commands()
    test_platform_parsers()
    
    print("\n使用说明:")
    print("1. 命令行搜索: python job_searcher.py '关键词' -c 城市")
    print("2. OpenClaw集成: python openclaw_integration.py")
    print("3. 在OpenClaw中调用: from skills.job_search import JobSearchSkill")