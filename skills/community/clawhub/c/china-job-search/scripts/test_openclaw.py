#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 技能测试脚本
"""

import sys
import os
import json

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from run_search import parse_search_query

def test_parse_query():
    """测试查询解析"""
    test_cases = [
        ("Python开发 北京", {
            'platform': None,
            'keyword': 'Python开发',
            'location': '北京',
            'salary': None,
            'experience': None
        }),
        ("Java开发 上海 15-30K 3-5年", {
            'platform': None,
            'keyword': 'Java开发',
            'location': '上海',
            'salary': '15-30K',
            'experience': '3-5年'
        }),
        ("boss Python 北京", {
            'platform': 'boss',
            'keyword': 'Python',
            'location': '北京',
            'salary': None,
            'experience': None
        }),
        ("智联 前端 上海 20-40K", {
            'platform': '智联',
            'keyword': '前端',
            'location': '上海',
            'salary': '20-40K',
            'experience': None
        }),
    ]
    
    print("测试查询解析功能...")
    for query, expected in test_cases:
        result, error = parse_search_query(query)
        if error:
            print(f"[FAIL] 失败: {query}")
            print(f"   错误: {error}")
        elif result == expected:
            print(f"[PASS] 通过: {query}")
        else:
            print(f"[FAIL] 失败: {query}")
            print(f"   期望: {expected}")
            print(f"   实际: {result}")
    
    print("\n测试完成！")

def test_skill_structure():
    """测试技能结构"""
    print("检查技能结构...")
    
    required_files = [
        ('SKILL.md', '技能主文档'),
        ('package.json', '技能元数据'),
        ('scripts/run_search.py', '入口脚本'),
        ('scripts/job_searcher.py', '主搜索逻辑'),
        ('scripts/boss_parser.py', 'BOSS解析器'),
        ('scripts/zhilian_parser.py', '智联解析器'),
        ('scripts/qiancheng_parser.py', '前程无忧解析器'),
        ('scripts/config.json', '配置文件'),
        ('scripts/requirements.txt', '依赖列表'),
        ('references/API_REFERENCE.md', 'API文档'),
    ]
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    all_passed = True
    for file_path, description in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            print(f"[OK] {description}: {file_path}")
        else:
            print(f"[ERROR] 缺失: {description} ({file_path})")
            all_passed = False
    
    if all_passed:
        print("\n[OK] 技能结构完整！")
    else:
        print("\n[ERROR] 技能结构不完整，请检查缺失文件。")
    
    return all_passed

def main():
    print("=" * 60)
    print("OpenClaw 招聘搜索技能测试")
    print("=" * 60)
    
    # 测试技能结构
    structure_ok = test_skill_structure()
    
    print("\n" + "=" * 60)
    
    # 测试查询解析
    test_parse_query()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    
    if structure_ok:
        print("[OK] 技能结构完整，可以正常使用")
        print("\n使用方法:")
        print("1. 在 OpenClaw 中，智能体会自动识别以下命令:")
        print("   搜索 Python开发 北京")
        print("   搜索 Java开发 上海 15-30K 3-5年")
        print("   搜索 boss Python 北京")
        print("\n2. 确保已安装依赖:")
        print("   pip install -r scripts/requirements.txt")
    else:
        print("[ERROR] 技能结构不完整，请修复缺失文件")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()