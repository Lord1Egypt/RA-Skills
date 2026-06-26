#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 错误记录脚本
记录OpenClaw的错误到错误台账
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEDGER_FILE = DATA_DIR / "error_ledger.jsonl"
INDEX_FILE = DATA_DIR / "error_index.json"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LEDGER_FILE.exists():
        LEDGER_FILE.touch()
    if not INDEX_FILE.exists():
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump({"errors": [], "stats": {"total": 0}}, f, ensure_ascii=False, indent=2)


def generate_error_id(date_str: str) -> str:
    """生成错误ID: HE-YYYYMMDD-XXXX"""
    count = 1
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        if record.get('error_id', '').startswith(f"HE-{date_str}"):
                            count += 1
                    except json.JSONDecodeError:
                        continue
    return f"HE-{date_str}-{count:04d}"


def check_similar_errors(question: str, error_type: str, tags: List[str]) -> Optional[dict]:
    """检查是否有相似的错误记录"""
    if not LEDGER_FILE.exists():
        return None
    
    similar = None
    max_similarity = 0
    
    with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                similarity = 0
                
                # 类型匹配
                if record.get('error_type') == error_type:
                    similarity += 30
                
                # 标签匹配
                record_tags = set(record.get('tags', []))
                current_tags = set(tags)
                if record_tags and current_tags:
                    tag_overlap = len(record_tags & current_tags) / max(len(record_tags | current_tags), 1)
                    similarity += int(tag_overlap * 50)
                
                # 问题关键词匹配
                question_words = set(question.lower().split())
                record_words = set(record.get('question', '').lower().split())
                if question_words and record_words:
                    word_overlap = len(question_words & record_words) / max(len(question_words | record_words), 1)
                    similarity += int(word_overlap * 20)
                
                if similarity > max_similarity and similarity > 50:
                    max_similarity = similarity
                    similar = record
                    
            except json.JSONDecodeError:
                continue
    
    return similar


def update_index(record: dict):
    """更新错误索引"""
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        index_data = {"errors": [], "stats": {"total": 0}}
    
    index_entry = {
        "error_id": record["error_id"],
        "timestamp": record["timestamp"],
        "error_type": record["error_type"],
        "level": record["level"],
        "fix_status": record["fix_status"],
        "tags": record.get("tags", [])
    }
    
    index_data["errors"].append(index_entry)
    index_data["stats"]["total"] = len(index_data["errors"])
    
    # 按类型统计
    type_stats = {}
    for entry in index_data["errors"]:
        et = entry.get("error_type", "未知")
        type_stats[et] = type_stats.get(et, 0) + 1
    index_data["stats"]["by_type"] = type_stats
    
    # 按等级统计
    level_stats = {}
    for entry in index_data["errors"]:
        lv = entry.get("level", "未知")
        level_stats[lv] = level_stats.get(lv, 0) + 1
    index_data["stats"]["by_level"] = level_stats
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)


def record_error(
    scene: str,
    error_type: str,
    question: str,
    wrong_answer: str,
    correct_answer: str,
    reason: str,
    level: str,
    source: str = "用户纠正",
    tags: Optional[List[str]] = None
) -> dict:
    """记录错误到台账"""
    
    ensure_data_dir()
    
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    error_id = generate_error_id(date_str)
    
    # 检查相似错误
    similar = check_similar_errors(question, error_type, tags or [])
    recurrence_count = 1
    if similar:
        recurrence_count = similar.get('recurrence_count', 1) + 1
    
    record = {
        "error_id": error_id,
        "timestamp": now.isoformat(),
        "scene": scene,
        "error_type": error_type,
        "question": question,
        "wrong_answer": wrong_answer,
        "correct_answer": correct_answer,
        "reason": reason,
        "fix_status": "未修复",
        "level": level,
        "source": source,
        "tags": tags or [],
        "recurrence_count": recurrence_count,
        "similar_to": similar["error_id"] if similar else None,
        "first_seen": similar.get('first_seen', now.strftime("%Y-%m-%d")) if similar else now.strftime("%Y-%m-%d"),
        "last_seen": now.strftime("%Y-%m-%d")
    }
    
    # 写入台账
    with open(LEDGER_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    # 更新索引
    update_index(record)
    
    return {
        "status": "ok",
        "error_id": error_id,
        "message": "错误已记录到台账",
        "similar_error": similar["error_id"] if similar else None,
        "recurrence_count": recurrence_count
    }


def main():
    parser = argparse.ArgumentParser(description='记录错误到错题本')
    parser.add_argument('--scene', required=True, help='场景：问答|代码|规划|推理|创作|工具调用')
    parser.add_argument('--error-type', required=True, help='错误类型')
    parser.add_argument('--question', required=True, help='用户原始问题')
    parser.add_argument('--wrong-answer', required=True, help='错误回答内容')
    parser.add_argument('--correct-answer', required=True, help='正确答案')
    parser.add_argument('--reason', required=True, help='错误原因分析')
    parser.add_argument('--level', required=True, choices=['低', '中', '高', '严重'], help='错误等级')
    parser.add_argument('--source', default='用户纠正', help='错误来源')
    parser.add_argument('--tags', help='标签，逗号分隔')
    
    args = parser.parse_args()
    
    tags = []
    if args.tags:
        tags = [t.strip() for t in args.tags.split(',') if t.strip()]
    
    result = record_error(
        scene=args.scene,
        error_type=args.error_type,
        question=args.question,
        wrong_answer=args.wrong_answer,
        correct_answer=args.correct_answer,
        reason=args.reason,
        level=args.level,
        source=args.source,
        tags=tags
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()