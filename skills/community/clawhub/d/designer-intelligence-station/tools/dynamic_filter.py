#!/usr/bin/env python3
"""
设计师情报站 - 动态分布筛选器（v2.1.5）

根据内容质量动态筛选，不强制平衡各领域比例。
质量优先：优质内容多的领域多输出，优质内容少的领域少输出。

使用方式:
    python3 tools/dynamic_filter.py /tmp/all_items.json --output /tmp/filtered_items.json
"""

import json
import sys
import argparse
from collections import defaultdict

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


def get_item_score(item: dict) -> int:
    """
    获取条目质量分数（1-5 分）
    5 = S 级（重大事件/知名公司）
    4 = A+ 级（深度分析/重要工具）
    3 = A 级（有价值内容）
    2 = B 级（常规内容）
    1 = C 级（低价值，通常排除）
    """
    title = (item.get('title', '') + item.get('summary', '')).lower()
    source = item.get('source', '').lower()
    
    # 5 分：S 级 - 重大事件/法律/知名公司核心发布
    s_level = ['胜诉', '禁令', 'lawsuit', 'injunction', '发布', 'launch', '重大', 
               'anthropic', 'openai', '谷歌', '苹果', '微软', '专利', '专利']
    if any(kw in title for kw in s_level):
        return 5
    
    # 4 分：A+ 级 - 深度分析/趋势/重要工具
    a_plus_level = ['趋势', '分析', '洞察', '实测', '深度', '指南', 'strategy', 
                    'trend', 'analysis', 'insight', 'guide', 'tool', '工具']
    if any(kw in title for kw in a_plus_level):
        return 4
    
    # 3 分：A 级 - 有价值的内容
    a_level = ['更新', '新功能', '技巧', '教程', 'review', 'update', 'new feature',
               '周刊', '周报', '素材', 'resource']
    if any(kw in title for kw in a_level):
        return 3
    
    # 2 分：B 级 - 常规内容
    return 2


def dynamic_filter(items: list[dict], target_min: int = 35, target_max: int = 50) -> list[dict]:
    """
    动态筛选条目
    - 按质量分数排序
    - 达到 target_min 后，只采用 3 分以上内容
    - 达到 target_max 后停止
    """
    # 评分和分类
    scored_items = []
    for item in items:
        score = get_item_score(item)
        domain = classify_item(item)
        scored_items.append({
            'item': item,
            'score': score,
            'domain': domain
        })
    
    # 按分数降序排序
    scored_items.sort(key=lambda x: -x['score'])
    
    result = []
    
    # 筛选逻辑
    for item_data in scored_items:
        # 达到上限，停止
        if len(result) >= target_max:
            break
        
        # 达到下限后，只采用 3 分以上内容
        if len(result) >= target_min and item_data['score'] < 3:
            continue
        
        # 排除 1 分内容
        if item_data['score'] <= 1:
            continue
        
        result.append(item_data['item'])
    
    return result


def main():
    parser = argparse.ArgumentParser(description='动态分布筛选器')
    parser.add_argument('input', help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出 JSON 文件路径')
    parser.add_argument('--min', type=int, default=35, help='最小输出数量')
    parser.add_argument('--max', type=int, default=50, help='最大输出数量')
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    print(f"输入：{len(items)} 条")
    
    # 动态筛选
    filtered = dynamic_filter(items, args.min, args.max)
    
    print(f"输出：{len(filtered)} 条")
    
    # 统计领域分布
    domain_counts = defaultdict(int)
    score_counts = defaultdict(int)
    
    for item in filtered:
        domain = classify_item(item)
        domain_counts[domain] += 1
        
        score = get_item_score(item)
        score_counts[score] += 1
    
    print("\n领域分布（动态）:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        pct = count / len(filtered) * 100
        print(f"  {domain}: {count} 条 ({pct:.1f}%)")
    
    print("\n质量分布:")
    for score, count in sorted(score_counts.items(), key=lambda x: -x[0]):
        level = {5: 'S 级', 4: 'A+ 级', 3: 'A 级', 2: 'B 级'}.get(score, '?')
        print(f"  {level} ({score}分): {count} 条")
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到：{args.output}")
    else:
        print(json.dumps(filtered, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
