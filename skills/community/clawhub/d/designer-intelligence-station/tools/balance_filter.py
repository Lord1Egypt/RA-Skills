#!/usr/bin/env python3
"""
设计师情报站 - 内容均衡筛选器（v2.1.4）

根据领域均衡配置，对抓取内容进行筛选，确保各领域占比合理。

使用方式:
    python3 tools/balance_filter.py /tmp/all_items.json --output /tmp/balanced_items.json
"""

import json
import sys
import argparse
from collections import defaultdict

# 领域均衡配置
DOMAIN_CONFIG = {
    'ai': {'target': 0.275, 'min': 0.20, 'max': 0.35, 'priority': 'P0'},
    'design': {'target': 0.275, 'min': 0.20, 'max': 0.30, 'priority': 'P0'},
    'hardware': {'target': 0.225, 'min': 0.15, 'max': 0.30, 'priority': 'P1'},
    'mobile': {'target': 0.125, 'min': 0.08, 'max': 0.20, 'priority': 'P1'},
    'other': {'target': 0.10, 'min': 0.05, 'max': 0.15, 'priority': 'P2'},
}

# 领域关键词
DOMAIN_KEYWORDS = {
    'design': ['design', 'designer', 'ux', 'ui', 'typography', 'visual', 'graphic', 'brand', 
               'aesthetic', 'color', 'layout', 'illustration', 'art direction', 'creative', 
               'studio', 'architecture', 'interior', 'product design', 'industrial design', 
               'fashion', 'packaging', 'poster', 'logo', '字体', '平面', '视觉', '品牌', 
               '创意', '设计', '美学', '配色', '排版', '插画', '建筑', '室内', '工业', 
               '产品', '包装', '海报', '标志', 'dezeen', 'smashing', 'sidebar', 'wired'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'model', 'anthropic', 
           'openai', 'google ai', 'deepmind', 'claude', 'gpt', 'gemini', '人工智能', '大模型', '智能'],
    'hardware': ['hardware', 'device', 'chip', 'processor', 'sensor', 'robot', 'drone', 'iot', 
                 'wearable', 'smart home', 'ar', 'vr', 'headset', '硬件', '芯片', '处理器', 
                 '传感器', '机器人', '无人机', '物联网', '穿戴', '智能家居', '头显'],
    'mobile': ['iphone', 'android', 'smartphone', 'mobile', 'ios', 'pixel', 'samsung', 'xiaomi', 
               'oppo', 'vivo', 'huawei', 'apple', '手机', '移动', '终端'],
}


def classify_item(item: dict) -> str:
    """分类条目到领域"""
    title = (item.get('title', '') + ' ' + item.get('summary', '')).lower()
    source = item.get('source', '').lower()
    text = title + ' ' + source
    
    # 多领域匹配计数
    matches = defaultdict(int)
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                matches[domain] += 1
    
    if not matches:
        return 'other'
    
    # 返回匹配最多的领域
    return max(matches.keys(), key=lambda k: matches[k])


def get_item_priority(item: dict, domain: str) -> int:
    """获取条目优先级（1=S 级，2=A 级，3=B 级）"""
    title = item.get('title', '') + item.get('summary', '')
    source = item.get('source', '')
    
    # S 级：知名公司/重大事件
    s_level_keywords = ['苹果', '谷歌', '微软', 'anthropic', 'openai', '专利', '胜诉', '发布', '重大']
    if any(kw.lower() in title.lower() for kw in s_level_keywords):
        return 1
    
    # A 级：深度分析/工具/资源
    a_level_keywords = ['分析', '趋势', '洞察', '工具', '教程', '深度', '实测', '指南']
    if any(kw.lower() in title.lower() for kw in a_level_keywords):
        return 2
    
    # B 级：常规内容
    return 3


def balance_items(items: list[dict], target_total: int = 40) -> list[dict]:
    """均衡筛选条目"""
    # 分类所有条目
    classified = defaultdict(list)
    for item in items:
        domain = classify_item(item)
        priority = get_item_priority(item, domain)
        classified[domain].append({
            'item': item,
            'priority': priority,
            'domain': domain
        })
    
    # 按优先级排序
    for domain in classified:
        classified[domain].sort(key=lambda x: x['priority'])
    
    # 计算各领域目标数量
    config = DOMAIN_CONFIG
    total = min(target_total, len(items))
    
    result = []
    remaining_slots = total
    
    # 第一轮：按优先级分配（确保 P0 领域优先）
    for priority in [1, 2, 3]:
        if remaining_slots <= 0:
            break
            
        for domain in ['ai', 'design', 'hardware', 'mobile', 'other']:
            if remaining_slots <= 0:
                break
                
            domain_items = [x for x in classified[domain] if x['priority'] == priority]
            config_domain = config[domain]
            
            # 计算当前领域已选数量
            current_count = len([x for x in result if classify_item(x) == domain])
            max_allowed = int(total * config_domain['max'])
            
            # 可选数量
            available = min(
                len(domain_items),
                max_allowed - current_count,
                remaining_slots
            )
            
            if available > 0:
                for i in range(available):
                    result.append(domain_items[i]['item'])
                    remaining_slots -= 1
    
    # 确保达到下限（优先保障低占比领域）
    domains_by_gap = sorted(
        config.keys(),
        key=lambda d: len([x for x in result if classify_item(x) == d]) / total - config[d]['min']
    )
    
    for domain in domains_by_gap:
        config_domain = config[domain]
        min_required = int(total * config_domain['min'])
        current_count = len([x for x in result if classify_item(x) == domain])
        
        if current_count < min_required:
            domain_items = classified[domain]
            existing_ids = {id(x) for x in result}
            
            for item_data in domain_items:
                if id(item_data['item']) not in existing_ids and current_count < min_required:
                    result.append(item_data['item'])
                    current_count += 1
    
    return result


def main():
    parser = argparse.ArgumentParser(description='内容均衡筛选器')
    parser.add_argument('input', help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出 JSON 文件路径')
    parser.add_argument('--target', '-t', type=int, default=40, help='目标输出数量')
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    print(f"输入：{len(items)} 条")
    
    # 均衡筛选
    balanced = balance_items(items, args.target)
    
    print(f"输出：{len(balanced)} 条")
    
    # 统计领域分布
    domain_counts = defaultdict(int)
    for item in balanced:
        domain = classify_item(item)
        domain_counts[domain] += 1
    
    print("\n领域分布:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        pct = count / len(balanced) * 100
        config = DOMAIN_CONFIG[domain]
        print(f"  {domain}: {count} 条 ({pct:.1f}%) [目标：{config['target']*100:.0f}%, 范围：{config['min']*100:.0f}%-{config['max']*100:.0f}%]")
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(balanced, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到：{args.output}")
    else:
        print(json.dumps(balanced, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
