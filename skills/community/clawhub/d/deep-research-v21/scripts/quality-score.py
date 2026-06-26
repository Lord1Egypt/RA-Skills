#!/usr/bin/env python3
"""
功能：对研究来源进行质量评分
用法：python3 quality-score.py <source_json>
"""

import json
import sys
from datetime import datetime

def calculate_quality_score(source_data):
    """计算来源质量评分"""
    
    # 解析数据
    pub_year = source_data.get('publication_year', source_data.get('year', 2000))
    journal = source_data.get('journal', source_data.get('publication', '')).lower()
    source_type = source_data.get('source_type', 'academic')
    sample_size = source_data.get('sample_size', 0)
    has_control = source_data.get('has_control_group', False)
    data_open = source_data.get('data_open', False)
    conflict_declared = source_data.get('conflict_declared', True)
    
    # 时效性分数 (0-2.5)
    current_year = datetime.now().year
    age = current_year - pub_year
    if age <= 1:
        time_score = 2.5
    elif age <= 3:
        time_score = 2.0
    elif age <= 5:
        time_score = 1.5
    else:
        time_score = 1.0
    
    # 权威性分数 (0-3)
    auth_score = 0
    if 'nature' in journal or 'science' in journal or 'lancet' in journal or 'cell' in journal:
        auth_score = 3.0
    elif 'nejm' in journal or 'jama' in journal or 'bmj' in journal:
        auth_score = 2.8
    elif 'pubmed' in journal or 'indexed' in journal:
        auth_score = 2.0
    else:
        auth_score = 1.5
    
    if source_type == 'industry':
        auth_score = min(auth_score + 0.5, 3.0)
    elif source_type == 'policy':
        auth_score = min(auth_score + 0.5, 3.0)
    
    # 方法论分数 (0-3)
    method_score = 0
    if sample_size and sample_size > 1000:
        method_score += 1.5
    elif sample_size and sample_size > 100:
        method_score += 1.0
    
    if has_control:
        method_score += 1.0
    
    if source_type == 'academic':
        method_score += 0.5
    
    # 可复现性分数 (0-1)
    repro_score = 0
    if data_open:
        repro_score += 1.0
    
    # 透明度分数 (0-0.5)
    trans_score = 0.5 if conflict_declared else 0
    
    # 总分
    total = time_score + auth_score + method_score + repro_score + trans_score
    
    # 证据等级
    if total >= 9:
        grade = 'A'
    elif total >= 7:
        grade = 'B'
    elif total >= 5:
        grade = 'C'
    else:
        grade = 'D'
    
    return {
        'total_score': round(total, 1),
        'max_score': 10,
        'grade': grade,
        'breakdown': {
            '时效性': round(time_score, 1),
            '权威性': round(auth_score, 1),
            '方法论': round(method_score, 1),
            '可复现': round(repro_score, 1),
            '透明度': round(trans_score, 1)
        }
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 quality-score.py <source_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except json.JSONDecodeError:
        # 尝试作为单行JSON解析
        source_data = json.loads(sys.argv[1])
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)
    
    result = calculate_quality_score(source_data)
    
    print("=" * 40)
    print("来源质量评分")
    print("=" * 40)
    print(f"标题: {source_data.get('title', 'N/A')[:50]}...")
    print(f"年份: {source_data.get('publication_year', 'N/A')}")
    print("-" * 40)
    print(f"总分: {result['total_score']}/{result['max_score']}")
    print(f"等级: {result['grade']}")
    print("-" * 40)
    print("评分明细:")
    for k, v in result['breakdown'].items():
        print(f"  {k}: {v}")
    print("=" * 40)
    
    # 输出JSON格式（供其他脚本使用）
    print("\n--- JSON Output ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
