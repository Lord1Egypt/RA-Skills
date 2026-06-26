#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 记录学习脚本
记录重要学习、纠正、知识差距、最佳实践
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LEARNINGS_FILE.exists():
        LEARNINGS_FILE.touch()


def generate_learning_id(date_str: str) -> str:
    """生成学习ID: LRN-YYYYMMDD-XXXX"""
    count = 1
    if LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        if record.get('learning_id', '').startswith(f"LRN-{date_str}"):
                            count += 1
                    except json.JSONDecodeError:
                        continue
    return f"LRN-{date_str}-{count:04d}"


def check_similar_learnings(summary: str, category: str, pattern_key: str = None) -> dict:
    """检查相似的学习记录"""
    if not LEARNINGS_FILE.exists():
        return None
    
    similar = None
    max_similarity = 0
    
    with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                similarity = 0
                
                # 类型匹配
                if record.get('category') == category:
                    similarity += 30
                
                # Pattern key 匹配
                if pattern_key and record.get('pattern_key') == pattern_key:
                    similarity += 50
                
                # 摘要关键词匹配
                summary_words = set(summary.lower().split())
                record_words = set(record.get('summary', '').lower().split())
                if summary_words and record_words:
                    word_overlap = len(summary_words & record_words) / max(len(summary_words | record_words), 1)
                    similarity += int(word_overlap * 20)
                
                if similarity > max_similarity and similarity > 40:
                    max_similarity = similarity
                    similar = record
                    
            except json.JSONDecodeError:
                continue
    
    return similar


def record_learning(
    category: str,
    summary: str,
    details: str,
    suggested_action: str,
    source: str = "conversation",
    pattern_key: str = None,
    priority: str = "medium",
    related_files: list = None
) -> dict:
    """记录学习到台账"""
    
    ensure_data_dir()
    
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    learning_id = generate_learning_id(date_str)
    
    record = {
        "learning_id": learning_id,
        "timestamp": now.isoformat(),
        "category": category,
        "summary": summary,
        "details": details,
        "suggested_action": suggested_action,
        "status": "pending",
        "priority": priority,
        "source": source,
        "pattern_key": pattern_key,
        "recurrence_count": 1,
        "first_seen": now.strftime("%Y-%m-%d"),
        "last_seen": now.strftime("%Y-%m-%d"),
        "promoted_to": "",
        "related_files": related_files or [],
        "see_also": []
    }
    
    # 检查相似学习
    similar = check_similar_learnings(summary, category, pattern_key)
    if similar:
        record["similar_to"] = similar["learning_id"]
        record["recurrence_count"] = similar.get("recurrence_count", 1) + 1
        record["last_seen"] = now.strftime("%Y-%m-%d")
    
    # 写入台账
    with open(LEARNINGS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    return {
        "status": "ok",
        "learning_id": learning_id,
        "message": "学习已记录到台账",
        "similar_learning": similar["learning_id"] if similar else None,
        "recurrence_count": record["recurrence_count"]
    }


def main():
    parser = argparse.ArgumentParser(description='记录学习到错题本')
    parser.add_argument('--category', required=True,
                       choices=['correction', 'best_practice', 'knowledge_gap', 'simplify_harden', 'workflow'],
                       help='学习类型')
    parser.add_argument('--summary', required=True, help='一句话摘要')
    parser.add_argument('--details', required=True, help='详细上下文')
    parser.add_argument('--suggested-action', dest='suggested_action', required=True, help='建议行动')
    parser.add_argument('--source', default='conversation', 
                       choices=['conversation', 'error', 'user_feedback', 'auto_detected'],
                       help='来源')
    parser.add_argument('--pattern-key', dest='pattern_key', help='模式键（用于重复检测）')
    parser.add_argument('--priority', default='medium',
                       choices=['low', 'medium', 'high', 'critical'],
                       help='优先级')
    parser.add_argument('--related-files', dest='related_files', help='相关文件，逗号分隔')
    
    args = parser.parse_args()
    
    related_files = []
    if args.related_files:
        related_files = [f.strip() for f in args.related_files.split(',') if f.strip()]
    
    result = record_learning(
        category=args.category,
        summary=args.summary,
        details=args.details,
        suggested_action=args.suggested_action,
        source=args.source,
        pattern_key=args.pattern_key,
        priority=args.priority,
        related_files=related_files
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()