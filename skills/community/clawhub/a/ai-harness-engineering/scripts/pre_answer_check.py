#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 回答前自检脚本
每次回答前自动查询错误台账，规避已记录的错误
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import List, Optional, Tuple

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
ERRORS_FILE = DATA_DIR / "error_ledger.jsonl"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"


def load_errors() -> list:
    """加载所有错误记录"""
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


def extract_keywords(question: str) -> List[str]:
    """从问题中提取关键词"""
    # 移除标点符号
    question = re.sub(r'[^\w\s]', ' ', question)
    # 分词
    words = question.split()
    # 过滤短词和停用词
    stop_words = {'的', '是', '在', '了', '和', '与', '或', '有', '没有', '如何', '怎么', '什么', '哪个', '哪一', 'the', 'a', 'an', 'is', 'are', 'to', 'of', 'in', 'for'}
    keywords = [w for w in words if len(w) >= 2 and w.lower() not in stop_words]
    return keywords[:10]  # 最多10个关键词


def calculate_similarity(question1: str, question2: str) -> float:
    """计算两个问题的相似度"""
    keywords1 = set(extract_keywords(question1))
    keywords2 = set(extract_keywords(question2))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    # Jaccard 相似度
    intersection = len(keywords1 & keywords2)
    union = len(keywords1 | keywords2)
    
    return intersection / union if union > 0 else 0.0


def find_similar_errors(question: str, threshold: float = 0.3) -> List[dict]:
    """查找相似错误"""
    errors = load_errors()
    similar = []
    
    for error in errors:
        # 只检查未修复和已规避的错误
        if error.get('fix_status') == '未修复':
            similarity = calculate_similarity(question, error.get('question', ''))
            if similarity >= threshold:
                error['similarity'] = similarity
                similar.append(error)
    
    # 按相似度排序
    similar.sort(key=lambda x: x.get('similarity', 0), reverse=True)
    return similar


def find_high_frequency_errors() -> List[dict]:
    """查找高频错误（recurrence_count >= 3）"""
    errors = load_errors()
    high_freq = []
    
    for error in errors:
        if error.get('recurrence_count', 1) >= 3:
            high_freq.append(error)
    
    return high_freq


def check_question(question: str) -> dict:
    """检查问题是否涉及已记录的错误"""
    # 1. 查找相似错误
    similar_errors = find_similar_errors(question, 0.3)
    
    # 2. 查找高频错误
    high_freq_errors = find_high_frequency_errors()
    
    # 3. 构建检查结果
    result = {
        "has_warning": False,
        "similar_errors": [],
        "high_frequency_errors": [],
        "avoidance_hint": "",
        "reference_error_id": None
    }
    
    if similar_errors:
        result["has_warning"] = True
        result["similar_errors"] = [
            {
                "error_id": e.get("error_id"),
                "error_type": e.get("error_type"),
                "question": e.get("question", "")[:60],
                "correct_answer": e.get("correct_answer", "")[:100],
                "similarity": e.get("similarity", 0)
            }
            for e in similar_errors[:3]
        ]
        result["reference_error_id"] = similar_errors[0].get("error_id")
        
        # 生成规避提示
        best_match = similar_errors[0]
        result["avoidance_hint"] = f"[⚠️ 规避历史错误: {best_match.get('error_id')}] {best_match.get('correct_answer', '')[:80]}"
    
    if high_freq_errors:
        result["high_frequency_errors"] = [
            {
                "error_id": e.get("error_id"),
                "error_type": e.get("error_type"),
                "question": e.get("question", "")[:60],
                "recurrence_count": e.get("recurrence_count", 1)
            }
            for e in high_freq_errors[:3]
        ]
        if not result["has_warning"]:
            result["has_warning"] = True
    
    return result


def pre_answer_check(question: str) -> str:
    """回答前自检主函数"""
    result = check_question(question)
    
    if result["has_warning"]:
        output = []
        
        # 添加错误警告
        if result["similar_errors"]:
            output.append("【错误规避检查】")
            for e in result["similar_errors"]:
                output.append(f"⚠️ 发现相似错误: {e['error_id']} [{e['error_type']}]")
                output.append(f"   正确回答: {e['correct_answer'][:60]}...")
                output.append("")
        
        if result["high_frequency_errors"]:
            output.append("【高频错误警告】")
            for e in result["high_frequency_errors"]:
                output.append(f"⚠️ 高频错误: {e['error_id']} (出现{e['recurrence_count']}次)")
        
        return '\n'.join(output)
    else:
        return ""


def main():
    # 解决 Windows 输出编码问题
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description='回答前自检')
    parser.add_argument('--question', required=True, help='用户问题')
    parser.add_argument('--format', default='text',
                       choices=['text', 'json'],
                       help='输出格式')
    
    args = parser.parse_args()
    
    if args.format == 'json':
        result = check_question(args.question)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        output = pre_answer_check(args.question)
        print(output)


if __name__ == '__main__':
    main()