#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 错误查询脚本
从错误台账中查询错误记录
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

# 获取skill目录
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEDGER_FILE = DATA_DIR / "error_ledger.jsonl"


def load_errors() -> List[dict]:
    """加载所有错误记录"""
    errors = []
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return errors


def filter_by_keywords(errors: List[dict], keywords: str) -> List[dict]:
    """按关键词过滤"""
    keyword_list = [k.lower() for k in keywords.split()]
    filtered = []
    for error in errors:
        text = ' '.join([
            error.get('question', ''),
            error.get('wrong_answer', ''),
            error.get('correct_answer', ''),
            error.get('reason', ''),
            ' '.join(error.get('tags', []))
        ]).lower()
        
        if all(kw in text for kw in keyword_list):
            filtered.append(error)
    
    return filtered


def filter_by_type(errors: List[dict], error_type: str) -> List[dict]:
    """按错误类型过滤"""
    return [e for e in errors if e.get('error_type') == error_type]


def filter_by_level(errors: List[dict], level: str) -> List[dict]:
    """按错误等级过滤"""
    return [e for e in errors if e.get('level') == level]


def filter_by_status(errors: List[dict], status: str) -> List[dict]:
    """按修复状态过滤"""
    return [e for e in errors if e.get('fix_status') == status]


def filter_by_scene(errors: List[dict], scene: str) -> List[dict]:
    """按场景过滤"""
    return [e for e in errors if e.get('scene') == scene]


def filter_by_date(errors: List[dict], days: int) -> List[dict]:
    """按日期范围过滤（最近N天）"""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for error in errors:
        try:
            ts = datetime.fromisoformat(error.get('timestamp', ''))
            if ts >= cutoff:
                filtered.append(error)
        except (ValueError, TypeError):
            continue
    return filtered


def format_output(errors: List[dict], limit: Optional[int] = None) -> dict:
    """格式化输出"""
    if limit:
        errors = errors[:limit]
    
    # 简化输出（不显示完整的wrong_answer和correct_answer）
    simplified = []
    for e in errors:
        simplified.append({
            "error_id": e.get("error_id"),
            "timestamp": e.get("timestamp"),
            "scene": e.get("scene"),
            "error_type": e.get("error_type"),
            "question": e.get("question")[:100] + "..." if len(e.get("question", "")) > 100 else e.get("question"),
            "level": e.get("level"),
            "fix_status": e.get("fix_status"),
            "tags": e.get("tags", [])
        })
    
    return {
        "total": len(errors),
        "errors": simplified
    }


def main():
    parser = argparse.ArgumentParser(description='查询错题本')
    parser.add_argument('--keywords', help='关键词搜索（空格分隔，AND逻辑）')
    parser.add_argument('--type', dest='error_type', help='按错误类型过滤')
    parser.add_argument('--level', help='按错误等级过滤：低|中|高|严重')
    parser.add_argument('--status', help='按修复状态过滤：未修复|已修复|已规避')
    parser.add_argument('--scene', help='按场景过滤')
    parser.add_argument('--days', type=int, help='最近N天的错误')
    parser.add_argument('--limit', type=int, default=20, help='返回数量限制')
    parser.add_argument('--all', action='store_true', help='显示所有错误（简化输出）')
    
    args = parser.parse_args()
    
    # 加载错误
    errors = load_errors()
    
    if not errors:
        print(json.dumps({"total": 0, "errors": [], "message": "暂无错误记录"}, ensure_ascii=False, indent=2))
        return
    
    # 应用过滤条件
    if args.keywords:
        errors = filter_by_keywords(errors, args.keywords)
    if args.error_type:
        errors = filter_by_type(errors, args.error_type)
    if args.level:
        errors = filter_by_level(errors, args.level)
    if args.status:
        errors = filter_by_status(errors, args.status)
    if args.scene:
        errors = filter_by_scene(errors, args.scene)
    if args.days:
        errors = filter_by_date(errors, args.days)
    
    # 输出结果
    result = format_output(errors, args.limit if not args.all else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
