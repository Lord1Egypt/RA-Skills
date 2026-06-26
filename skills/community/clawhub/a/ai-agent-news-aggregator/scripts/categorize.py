#!/usr/bin/env python3
"""
categorize.py - 新闻分类

根据关键词将新闻分门别类（头条/框架/论文/公司/应用）。

用法:
    python categorize.py --input summarized.json --output categorized.json [--config sources.json]
"""

import json
import sys
from pathlib import Path

# 默认分类关键词
DEFAULT_CATEGORIES = {
    "headline": ["发布", "重磅", "major", "launch", "announced", "released"],
    "framework": ["LangChain", "AutoGen", "CrewAI", "LlamaIndex", "framework", "SDK"],
    "research": ["paper", "arXiv", "论文", "research", "study", "academic"],
    "company": ["Anthropic", "OpenAI", "Google", "Microsoft", "Meta", "Amazon", "公司", "融资"],
    "application": ["应用", "case study", "implementation", "落地", "product", "customer"]
}

def categorize_item(item, categories):
    """
    根据关键词将新闻项分类
    
    返回最匹配的类别，如果没有匹配则返回 "other"
    """
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    combined = (title + " " + snippet).lower()
    
    # 计分制：匹配关键词越多，分数越高
    scores = {}
    
    for category, keywords in categories.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in combined:
                score += 1
        if score > 0:
            scores[category] = score
    
    if not scores:
        return "other"
    
    # 返回分数最高的类别
    return max(scores, key=scores.get)

def categorize_items(items, categories=None):
    """
    对所有新闻项进行分类
    
    返回:
    {
        "items": [...],  # 添加 category 字段的原始列表
        "by_category": {  # 按类别分组
            "headline": [...],
            "framework": [...],
            ...
        },
        "counts": {  # 每类数量
            "headline": 5,
            ...
        }
    }
    """
    categories = categories or DEFAULT_CATEGORIES
    
    by_category = {}
    categorized_items = []
    
    for item in items:
        cat = categorize_item(item, categories)
        
        # 添加 category 字段
        item_with_cat = item.copy()
        item_with_cat["category"] = cat
        categorized_items.append(item_with_cat)
        
        # 分组
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item_with_cat)
    
    # 统计
    counts = {cat: len(items) for cat, items in by_category.items()}
    
    return {
        "items": categorized_items,
        "by_category": by_category,
        "counts": counts,
        "total": len(items)
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="新闻分类")
    parser.add_argument("--input", type=str, required=True,
                        help="输入文件路径 (JSON)")
    parser.add_argument("--output", type=str, default="",
                        help="输出文件路径")
    parser.add_argument("--config", type=str, default="",
                        help="配置文件路径 (读取自定义分类)")
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    # 加载自定义分类（如果指定）
    categories = DEFAULT_CATEGORIES
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        categories = config.get("categories", DEFAULT_CATEGORIES)
    
    # 分类
    result = categorize_items(items, categories)
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"分类完成：{result['total']} 条 → {len(result['by_category'])} 类", file=sys.stderr)
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
