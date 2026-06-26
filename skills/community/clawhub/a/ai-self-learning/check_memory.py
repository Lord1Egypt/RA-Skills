#!/usr/bin/env python3
"""
Self-Improving Agent - 记忆检索工具
执行前检查所有类型的相关记忆，支持模糊匹配和相关性评分
"""

import sys
import json
import os
import re
import argparse
from collections import Counter

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")

MEMORY_FILES = {
    "错误": "errors.jsonl",
    "纠正": "corrections.jsonl",
    "最佳实践": "best_practices.jsonl",
    "知识盲区": "knowledge_gaps.jsonl",
}

# 每种记忆类型的搜索字段
SEARCH_FIELDS = {
    "错误": ["command", "error", "fix"],
    "纠正": ["topic", "wrong", "correct", "context"],
    "最佳实践": ["category", "practice", "reason"],
    "知识盲区": ["topic", "outdated", "current", "source"],
}

# 显示字段配置
DISPLAY_CONFIG = {
    "错误": lambda m: [
        f"命令: {m.get('command', '?')[:60]}",
        f"错误: {m.get('error', '?')[:60]}",
        f"修复: {m.get('fix', '待分析')}" if m.get("fix") else None,
        f"优先级: {m.get('priority', 'medium')}",
    ],
    "纠正": lambda m: [
        f"主题: {m.get('topic', '?')}",
        f"错误做法: {m.get('wrong', '?')}",
        f"正确做法: {m.get('correct', '?')}",
        f"纠正次数: {m.get('count', 1)}" if m.get("count", 1) > 1 else None,
    ],
    "最佳实践": lambda m: [
        f"类别: {m.get('category', '?')}",
        f"实践: {m.get('practice', '?')}",
        f"原因: {m.get('reason', '')}" if m.get("reason") else None,
    ],
    "知识盲区": lambda m: [
        f"主题: {m.get('topic', '?')}",
        f"过时: {m.get('outdated', '?')}",
        f"当前: {m.get('current', '?')}",
        f"来源: {m.get('source', '')}" if m.get("source") else None,
    ],
}


def tokenize(text):
    """将文本分词为小写token集合"""
    if not text:
        return set()
    # 中文按字切分，英文按词切分
    tokens = set()
    # 英文单词
    tokens.update(re.findall(r"[a-zA-Z0-9_\-\.]+", text.lower()))
    # 中文字符（每个字 + 连续两字的bigram）
    cn_chars = re.findall(r"[\u4e00-\u9fff]", text)
    tokens.update(cn_chars)
    for i in range(len(cn_chars) - 1):
        tokens.add(cn_chars[i] + cn_chars[i + 1])
    return tokens


def score_relevance(query_tokens, entry, fields):
    """计算查询与记忆条目的相关性评分 (0-100)"""
    if not query_tokens:
        return 0

    entry_text = " ".join(str(entry.get(f, "")) for f in fields)
    entry_tokens = tokenize(entry_text)

    if not entry_tokens:
        return 0

    # Jaccard相似度 + 覆盖率加权
    intersection = query_tokens & entry_tokens
    if not intersection:
        return 0

    jaccard = len(intersection) / len(query_tokens | entry_tokens)
    coverage = len(intersection) / len(query_tokens)  # 查询词覆盖率

    # 覆盖率权重更高（用户的查询词都被匹配到更重要）
    score = (jaccard * 30 + coverage * 70)

    # 纠正类记忆加权（用户明确纠正过的最重要）
    if entry.get("type") == "correction":
        score *= 1.2
        # 多次纠正进一步加权
        score *= min(1 + (entry.get("count", 1) - 1) * 0.1, 1.5)

    # 高优先级错误加权
    if entry.get("priority") == "high":
        score *= 1.3
    elif entry.get("priority") == "low":
        score *= 0.8

    return min(score, 100)


def load_memories(memory_type):
    """加载指定类型的记忆"""
    filepath = os.path.join(MEMORY_DIR, MEMORY_FILES[memory_type])
    if not os.path.exists(filepath):
        return []
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def check_memory(query, types=None, min_score=15, limit=10):
    """检查与查询相关的所有记忆"""
    if not os.path.exists(MEMORY_DIR):
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results = []
    check_types = types or list(MEMORY_FILES.keys())

    for mem_type in check_types:
        if mem_type not in MEMORY_FILES:
            continue
        entries = load_memories(mem_type)
        fields = SEARCH_FIELDS[mem_type]
        for entry in entries:
            score = score_relevance(query_tokens, entry, fields)
            if score >= min_score:
                results.append((mem_type, score, entry))

    # 按评分降序排列
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]


def format_output(results, verbose=False):
    """格式化输出"""
    if not results:
        print("OK 未发现相关记忆，可以安全执行。")
        return

    print(f"!! 发现 {len(results)} 条相关记忆:\n")

    for mem_type, score, entry in results:
        timestamp = entry.get("timestamp", "")[:10]
        score_bar = "#" * int(score / 10)
        print(f"  [{mem_type}] {timestamp}  相关度: {score_bar} ({score:.0f}%)")

        display_fn = DISPLAY_CONFIG.get(mem_type)
        if display_fn:
            lines = display_fn(entry)
            for line in lines:
                if line:
                    print(f"      {line}")
        print()


def main():
    parser = argparse.ArgumentParser(description="检查与操作相关的记忆")
    parser.add_argument("--query", "-q", required=True, help="查询关键词（命令、主题等）")
    parser.add_argument("--type", "-t", action="append", choices=list(MEMORY_FILES.keys()),
                        help="只检查指定类型的记忆（可多次指定）")
    parser.add_argument("--min-score", type=int, default=15, help="最低相关度分数 (0-100)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="最多返回条数")
    parser.add_argument("--json", action="store_true", help="JSON格式输出（供程序调用）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")

    # 兼容旧版 --command 参数
    parser.add_argument("--command", help=argparse.SUPPRESS)

    args = parser.parse_args()
    query = args.query or args.command
    if not query:
        print("Usage: check_memory.py --query '关键词'")
        sys.exit(1)

    results = check_memory(query, types=args.type, min_score=args.min_score, limit=args.limit)

    if args.json:
        output = [{"type": t, "score": s, "entry": e} for t, s, e in results]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        format_output(results, verbose=args.verbose)


if __name__ == "__main__":
    main()
