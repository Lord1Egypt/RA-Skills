#!/usr/bin/env python3
"""
验证核心流程（整合模块）
输入：question + answer
输出：完整验证报告
"""

import os
import json
import argparse
import sys
import tempfile
from pathlib import Path

# 导入各模块（假设在同一目录）
from decompose import decompose
from verify import verify_facts
from consistency import check_consistency
from score import calc_score, format_output


def run_verification(question: str, answer: str, sources: list = None) -> dict:
    """
    完整验证流程
    """
    print("🔍 开始验证...", file=sys.stderr)

    # Step 1: 获取多源参考答案
    print("  [1/5] 获取多源参考答案...", file=sys.stderr)
    from fetch_answers import fetch_answers
    ref_results = fetch_answers(question, sources)
    references = [r["answer"] for r in ref_results]

    if not references:
        return {
            "verdict": "unknown",
            "score": 0,
            "summary": "无法获取任何参考答案，验证中止",
            "details": {}
        }

    # Step 2: 原子事实分解
    print("  [2/5] 分解原子事实...", file=sys.stderr)
    facts = decompose(answer)

    if not facts:
        return {
            "verdict": "unknown",
            "score": 0,
            "summary": "无法分解原子事实，验证中止",
            "details": {}
        }

    # Step 3: 逐事实验证
    print(f"  [3/5] 验证 {len(facts)} 个事实...", file=sys.stderr)
    verification_results = verify_facts(facts, references)

    # Step 4: 内部一致性检测
    print("  [4/5] 检测内部一致性...", file=sys.stderr)
    consistency_result = check_consistency(answer)

    # Step 5: 综合评分
    print("  [5/5] 计算综合评分...", file=sys.stderr)
    score_result = calc_score(verification_results, consistency_result)

    # 整合输出
    return {
        "verdict": score_result["verdict"],
        "score": score_result["score"],
        "summary": score_result["summary"],
        "details": {
            "facts": verification_results,
            "consistency": consistency_result,
            "sources": [r["source"] for r in ref_results]
        }
    }


def main():
    parser = argparse.ArgumentParser(description="验证AI回答是否正确")
    parser.add_argument("--question", type=str, help="问题文本")
    parser.add_argument("--answer", type=str, help="待验证的回答")
    parser.add_argument("--qfile", type=str, help="从文件读取问题")
    parser.add_argument("--afile", type=str, help="从文件读取回答")
    parser.add_argument("--sources", type=str, default="openai,anthropic,gemini",
                        help="数据源（逗号分隔）")
    parser.add_argument("--format", choices=["json", "text"], default="text",
                        help="输出格式")
    args = parser.parse_args()

    # 读取输入
    if args.qfile:
        with open(args.qfile, "r", encoding="utf-8") as f:
            question = f.read()
    elif args.question:
        question = args.question
    else:
        print("请提供 --question 或 --qfile 参数", file=sys.stderr)
        sys.exit(1)

    if args.afile:
        with open(args.afile, "r", encoding="utf-8") as f:
            answer = f.read()
    elif args.answer:
        answer = args.answer
    else:
        print("请提供 --answer 或 --afile 参数", file=sys.stderr)
        sys.exit(1)

    sources = [s.strip() for s in args.sources.split(",")]
    result = run_verification(question, answer, sources)

    # 输出结果
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 使用 score.py 中的格式化函数
        from score import format_output
        facts = result["details"].get("facts", [])
        formatted = format_output(result, facts)
        print(formatted)


if __name__ == "__main__":
    main()
