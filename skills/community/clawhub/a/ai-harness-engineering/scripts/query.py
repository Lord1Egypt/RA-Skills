#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 统一查询脚本
查询错误、学习、功能请求台账
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
ERRORS_FILE = DATA_DIR / "error_ledger.jsonl"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"
FEATURES_FILE = DATA_DIR / "feature_ledger.jsonl"


def load_errors() -> List[dict]:
    """加载错误记录"""
    errors = []
    if ERRORS_FILE.exists():
        with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return errors


def load_learnings() -> List[dict]:
    """加载学习记录"""
    learnings = []
    if LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        learnings.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return learnings


def load_features() -> List[dict]:
    """加载功能请求"""
    features = []
    if FEATURES_FILE.exists():
        with open(FEATURES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        features.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return features


def filter_by_keywords(items: List[dict], keywords: str) -> List[dict]:
    """按关键词过滤"""
    keyword_list = [k.lower() for k in keywords.split()]
    filtered = []
    for item in items:
        search_text = ' '.join([
            json.dumps(item, ensure_ascii=False)
        ]).lower()
        
        if all(kw in search_text for kw in keyword_list):
            filtered.append(item)
    return filtered


def filter_by_status(items: List[dict], status: str) -> List[dict]:
    """按状态过滤"""
    key = "fix_status" if items and "fix_status" in items[0] else "status"
    return [e for e in items if e.get(key) == status]


def filter_by_category(items: List[dict], category: str) -> List[dict]:
    """按类别过滤（学习记录）"""
    return [e for e in items if e.get('category') == category]


def filter_by_priority(items: List[dict], priority: str) -> List[dict]:
    """按优先级过滤"""
    return [e for e in items if e.get('priority') == priority]


def simplify_item(item: dict, item_type: str) -> dict:
    """简化输出项"""
    if item_type == "error":
        key = "error_id"
        fields = ["error_id", "timestamp", "scene", "error_type", "level", "fix_status", "tags"]
    elif item_type == "learning":
        key = "learning_id"
        fields = ["learning_id", "timestamp", "category", "summary", "status", "priority", "recurrence_count"]
    else:  # feature
        key = "feature_id"
        fields = ["feature_id", "timestamp", "feature_name", "complexity", "status", "priority", "frequency"]
    
    result = {"type": item_type}
    for f in fields:
        if f in item:
            result[f] = item[f]
    return result


def main():
    parser = argparse.ArgumentParser(description='查询台账')
    parser.add_argument('--type', required=True,
                       choices=['errors', 'learnings', 'features', 'all'],
                       help='查询类型')
    parser.add_argument('--keywords', help='关键词搜索（空格分隔）')
    parser.add_argument('--status', help='按状态过滤：pending/resolved/promoted')
    parser.add_argument('--category', help='按学习类别过滤')
    parser.add_argument('--priority', help='按优先级过滤')
    parser.add_argument('--limit', type=int, default=20, help='返回数量限制')
    
    args = parser.parse_args()
    
    results = {"errors": [], "learnings": [], "features": []}
    
    if args.type in ['errors', 'all']:
        errors = load_errors()
        if args.keywords:
            errors = filter_by_keywords(errors, args.keywords)
        if args.status:
            errors = filter_by_status(errors, args.status)
        if args.priority:
            errors = filter_by_priority(errors, args.priority)
        results["errors"] = [simplify_item(e, "error") for e in errors[:args.limit]]
    
    if args.type in ['learnings', 'all']:
        learnings = load_learnings()
        if args.keywords:
            learnings = filter_by_keywords(learnings, args.keywords)
        if args.status:
            learnings = filter_by_status(learnings, args.status)
        if args.category:
            learnings = filter_by_category(learnings, args.category)
        if args.priority:
            learnings = filter_by_priority(learnings, args.priority)
        results["learnings"] = [simplify_item(l, "learning") for l in learnings[:args.limit]]
    
    if args.type in ['features', 'all']:
        features = load_features()
        if args.keywords:
            features = filter_by_keywords(features, args.keywords)
        if args.status:
            features = filter_by_status(features, args.status)
        if args.priority:
            features = filter_by_priority(features, args.priority)
        results["features"] = [simplify_item(f, "feature") for f in features[:args.limit]]
    
    # 统计
    total = len(results["errors"]) + len(results["learnings"]) + len(results["features"])
    results["summary"] = {
        "total": total,
        "errors": len(results["errors"]),
        "learnings": len(results["learnings"]),
        "features": len(results["features"])
    }
    
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()