#!/usr/bin/env python3
"""
enrich_bids.py - 从标题提取公司/预算信息并计算优先级
"""
import json
import re
import sys
import os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

# 从标题提取公司名的模式
COMPANY_PATTERNS = [
    # 明确的中标/入围公司（精确匹配）
    r'海博思创',
    r'亿纬',
    r'星辰储能',
    r'大唐',
    r'中能建',
    r'中电建',
    r'中国电建',
    r'川投',
    r'比亚迪',
    r'海辰',
    r'瑞浦兰钧',
    r'楚能',
    r'时代',
    # 通用公司模式
    r'([\u4e00-\u9fa5]{2,6})(?:能源|电力|储能|建设)(?:有限公司)?',
]

# 预算匹配模式
BUDGET_PATTERNS = [
    (r'(\d+)\s*MW\s*/\s*(\d+)\s*MWh', lambda m: f"{m.group(1)}MW/{m.group(2)}MWh"),
    (r'(\d+[.,]?\d*)\s*亿', lambda m: f"{m.group(1)}亿"),
    (r'(\d+)\s*万', lambda m: f"{m.group(1)}万"),
    (r'(0\.[\d]+)\s*元/Wh', lambda m: f"{m.group(1)}元/Wh"),
]


def extract_company(title):
    """从标题提取公司名 - 使用精确匹配"""
    if not title:
        return ""
    
    # 已知的公司列表（精确匹配）
    known_companies = [
        '海博思创', '亿纬', '星辰储能', '大唐', '中能建', '中国电建', '川投',
        '比亚迪', '海辰', '瑞浦兰钧', '楚能', '时代', '中电建',
    ]
    
    for c in known_companies:
        if c in title:
            return c
    
    # 泛化模式：XX能源/XX电力等
    m = re.search(r'([\u4e00-\u9fa5]{2,6})(?:能源|电力|储能)(?:有限公司)?', title)
    if m:
        return m.group(1)
    
    return ""


def extract_budget(title):
    """从标题提取预算"""
    if not title:
        return ""
    # 检查 MWh 格式
    m = re.search(r'(\d+)\s*MW\s*/\s*(\d+)\s*MWh', title, re.IGNORECASE)
    if m:
        return f"{m.group(1)}MW/{m.group(2)}MWh"
    # 检查金额
    for pat, func in BUDGET_PATTERNS:
        m = re.search(pat, title)
        if m:
            return func(m)
    return ""


def enrich_bid(bid):
    """补充单条招标信息"""
    title = bid.get('title', '') or bid.get('desc', '')
    
    # 提取公司
    if not bid.get('company') or bid.get('company') in ['未知', '']:
        company = extract_company(title)
        if company:
            bid['company'] = company
    
    # 提取预算
    if not bid.get('budget') or bid.get('budget') in ['未知', '']:
        budget = extract_budget(title)
        if budget:
            bid['budget'] = budget
    
    # 计算优先级
    score = 0
    budget_val = bid.get('budget', '')
    if budget_val and budget_val not in ['未知', '']:
        score += 1
        # 大项目加分
        if any(kw in budget_val for kw in ['亿', 'MW', 'MWh', 'GWh']):
            score += 1
    
    # 关键词加分
    title_kw = title.lower()
    if any(kw in title_kw for kw in ['储能', '锂电', '动力电池', '锂电池', '电池']):
        score += 1
    
    if score >= 4:
        bid['优先级'] = 'S'
    elif score >= 3:
        bid['优先级'] = 'A'
    elif score >= 2:
        bid['优先级'] = 'B'
    else:
        bid['优先级'] = 'C'
    
    # 相关性
    bid['相关性'] = '高' if score >= 2 else '低'
    
    return bid


def enrich_all(input_file=None, output_file=None):
    """批量处理所有数据"""
    if input_file is None:
        input_file = DATA_DIR / "bids_raw_latest.json"
    else:
        # 转换为 Path 对象
        input_file = Path(input_file)
    
    if not input_file.exists():
        print(f"错误: 文件不存在 {input_file}")
        return False
    
    if output_file is None:
        output_file = DATA_DIR / "bids_parsed_enriched.json"
    else:
        output_file = Path(output_file)
    
    # 读取数据
    with open(input_file, encoding='utf-8') as f:
        data = json.load(f)
    
    bids = data if isinstance(data, list) else data.get('bids', [])
    
    print(f"��始数据: {len(bids)} 条")
    
    # 逐条处理
    enriched = []
    for b in bids:
        e = enrich_bid(b)
        # 统一字段名
        if 'desc' in e and 'title' not in e:
            e['title'] = e['desc']
        enriched.append(e)
    
    # 保存
    result = {'bids': enriched, 'total': len(enriched)}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"已保存: {output_file}")
    
    # 统计
    priority_counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}
    for b in enriched:
        p = b.get('优先级', 'C')
        priority_counts[p] = priority_counts.get(p, 0) + 1
    
    print(f"优先级分布: {priority_counts}")
    
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="输入JSON文件")
    parser.add_argument("--output", "-o", help="输出JSON文件")
    args = parser.parse_args()
    
    input_file = Path(args.input) if args.input else DATA_DIR / "bids_raw_latest.json"
    output_file = Path(args.output) if args.output else None
    
    enrich_all(input_file, output_file)