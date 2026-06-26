#!/usr/bin/env python3
"""
测试 conditional-order-tool 的 5 个场景
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from conditional_order import generate_full_report, format_report_text

# 测试用例
test_cases = [
    {
        'name': '核心场景 - 黄金 ETF',
        'code': '518880',
        'capital': 50000,
        'risk': 'balanced',
    },
    {
        'name': '核心场景 - 宽基 ETF',
        'code': '510300',
        'capital': 10000,
        'risk': 'conservative',
    },
    {
        'name': '边缘场景 - 跨境 ETF',
        'code': '513100',
        'capital': 10000,
        'risk': 'balanced',
    },
    {
        'name': '复杂场景 - 50 万配置',
        'code': '518880',  # 先测一个，实际应该多代码
        'capital': 500000,
        'risk': 'balanced',
    },
    {
        'name': '错误输入 - 不存在代码',
        'code': '999999',
        'capital': 10000,
        'risk': 'balanced',
    },
]

results = []

for tc in test_cases:
    print(f"\n{'='*60}")
    print(f"测试：{tc['name']}")
    print(f"代码：{tc['code']}，资金：{tc['capital']}，风险偏好：{tc['risk']}")
    print('='*60)
    
    report = generate_full_report(tc['code'], tc['capital'], tc['risk'])
    text = format_report_text(report)
    
    print(text)
    results.append({
        'test': tc['name'],
        'report': report,
        'text': text,
    })
    
    # 保存结果
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'prompt-' + str(test_cases.index(tc) + 1))
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, 'output.txt'), 'w', encoding='utf-8') as f:
        f.write(text)

print(f"\n{'='*60}")
print("所有测试完成，结果已保存")
print('='*60)
