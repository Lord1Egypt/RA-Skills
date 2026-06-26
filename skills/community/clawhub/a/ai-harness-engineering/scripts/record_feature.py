#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 记录功能请求脚本
跟踪用户想要但当前没有的功能
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
FEATURES_FILE = DATA_DIR / "feature_ledger.jsonl"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not FEATURES_FILE.exists():
        FEATURES_FILE.touch()


def generate_feature_id(date_str: str) -> str:
    """生成功能请求ID: FR-YYYYMMDD-XXXX"""
    count = 1
    if FEATURES_FILE.exists():
        with open(FEATURES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        if record.get('feature_id', '').startswith(f"FR-{date_str}"):
                            count += 1
                    except json.JSONDecodeError:
                        continue
    return f"FR-{date_str}-{count:04d}"


def check_similar_features(feature_name: str) -> dict:
    """检查相似的功能请求"""
    if not FEATURES_FILE.exists():
        return None
    
    similar = None
    
    with open(FEATURES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                # 名称相似度检查
                if feature_name.lower() in record.get('feature_name', '').lower():
                    similar = record
                    break
                if record.get('feature_name', '').lower() in feature_name.lower():
                    similar = record
                    break
            except json.JSONDecodeError:
                continue
    
    return similar


def record_feature(
    feature_name: str,
    user_context: str,
    complexity: str = "中等",
    priority: str = "medium",
    source: str = "user_request"
) -> dict:
    """记录功能请求到台账"""
    
    ensure_data_dir()
    
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    feature_id = generate_feature_id(date_str)
    
    # 检查相似功能请求
    similar = check_similar_features(feature_name)
    
    record = {
        "feature_id": feature_id,
        "timestamp": now.isoformat(),
        "feature_name": feature_name,
        "user_context": user_context,
        "complexity": complexity,
        "status": "pending",
        "priority": priority,
        "source": source,
        "similar_to": similar["feature_id"] if similar else None,
        "frequency": 1 if not similar else (similar.get("frequency", 1) + 1),
        "implementation_notes": "",
        "related_features": []
    }
    
    # 写入台账
    with open(FEATURES_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    return {
        "status": "ok",
        "feature_id": feature_id,
        "message": "功能请求已记录到台账",
        "similar_feature": similar["feature_id"] if similar else None,
        "frequency": record["frequency"]
    }


def main():
    parser = argparse.ArgumentParser(description='记录功能请求')
    parser.add_argument('--name', required=True, help='功能名称')
    parser.add_argument('--context', required=True, help='用户场景/为什么需要')
    parser.add_argument('--complexity', default='中等',
                       choices=['简单', '中等', '复杂'],
                       help='复杂度评估')
    parser.add_argument('--priority', default='medium',
                       choices=['low', 'medium', 'high', 'critical'],
                       help='优先级')
    parser.add_argument('--source', default='user_request',
                       help='请求来源')
    
    args = parser.parse_args()
    
    result = record_feature(
        feature_name=args.name,
        user_context=args.context,
        complexity=args.complexity,
        priority=args.priority,
        source=args.source
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()