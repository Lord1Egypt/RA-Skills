#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 更新错误状态脚本
更新错误记录的修复状态
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

# 获取skill目录
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEDGER_FILE = DATA_DIR / "error_ledger.jsonl"
INDEX_FILE = DATA_DIR / "error_index.json"


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


def save_errors(errors: List[dict]):
    """保存所有错误记录"""
    with open(LEDGER_FILE, 'w', encoding='utf-8') as f:
        for error in errors:
            f.write(json.dumps(error, ensure_ascii=False) + '\n')


def update_index(error_id: str, new_status: str):
    """更新索引中的状态"""
    if not INDEX_FILE.exists():
        return
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    # 更新对应错误的状态
    for entry in index_data.get('errors', []):
        if entry.get('error_id') == error_id:
            entry['fix_status'] = new_status
            break
    
    # 重新计算状态统计
    status_counter = {}
    for entry in index_data.get('errors', []):
        st = entry.get('fix_status', '未知')
        status_counter[st] = status_counter.get(st, 0) + 1
    
    index_data['stats']['by_status'] = status_counter
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)


def update_error_status(error_id: str, new_status: str) -> dict:
    """更新错误状态"""
    errors = load_errors()
    
    found = False
    for error in errors:
        if error.get('error_id') == error_id:
            old_status = error.get('fix_status', '未知')
            error['fix_status'] = new_status
            found = True
            
            # 保存
            save_errors(errors)
            
            # 更新索引
            update_index(error_id, new_status)
            
            return {
                "status": "ok",
                "error_id": error_id,
                "old_status": old_status,
                "new_status": new_status,
                "message": f"错误状态已更新：{old_status} → {new_status}"
            }
    
    if not found:
        return {
            "status": "error",
            "message": f"未找到错误ID：{error_id}"
        }


def main():
    parser = argparse.ArgumentParser(description='更新错误修复状态')
    parser.add_argument('--error-id', required=True, help='错误ID')
    parser.add_argument('--status', required=True, 
                       choices=['未修复', '已修复', '已规避'],
                       help='新状态')
    
    args = parser.parse_args()
    
    result = update_error_status(args.error_id, args.status)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
