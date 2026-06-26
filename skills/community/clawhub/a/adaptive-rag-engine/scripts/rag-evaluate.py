#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════
# rag-evaluate.py — CRAG 质量评估器
# 评估检索结果与查询的相关度，决定是否需要补搜
# 用法: python3 rag-evaluate.py --query "问题" --results "结果1|结果2|结果3"
# ═══════════════════════════════════════════════════════

import argparse
import json
import sys

# 简化版关键词匹配评分（后续可替换为 LLM 评分）
def keyword_relevance_score(query, result):
    """基于关键词重叠的相关度评分 (0.0 - 1.0)"""
    if not query or not result:
        return 0.0
    
    # 简单分词（中文按字符，英文按单词）
    query_chars = set(query.lower())
    query_words = set(query.lower().split())
    result_chars = set(result.lower())
    result_words = set(result.lower().split())
    
    # 字符级重叠
    char_overlap = len(query_chars & result_chars) / max(len(query_chars), 1)
    
    # 词级重叠
    word_overlap = len(query_words & result_words) / max(len(query_words), 1)
    
    # 综合评分 (词级权重更高)
    score = char_overlap * 0.3 + word_overlap * 0.7
    
    return min(score, 1.0)


def evaluate_results(query, results, threshold=0.3):
    """评估一组检索结果"""
    evaluations = []
    
    for i, result in enumerate(results):
        score = keyword_relevance_score(query, result)
        
        if score >= 0.8:
            action = "USE_DIRECT"
            label = "✅ 高度相关"
        elif score >= 0.5:
            action = "USE_WITH_NOTE"
            label = "⚠️  中等相关"
        elif score >= 0.3:
            action = "BACKGROUND"
            label = "📋 弱相关(背景参考)"
        else:
            action = "DISCARD_OR_REFETCH"
            label = "❌ 不相关"
        
        evaluations.append({
            "index": i,
            "score": round(score, 3),
            "action": action,
            "label": label,
            "preview": result[:100] + ("..." if len(result) > 100 else ""),
        })
    
    # 整体判断
    max_score = max([e["score"] for e in evaluations], default=0)
    if max_score < threshold:
        overall = "FETCH_NEEDED"
        overall_label = "🔍 建议触发 Tavily 补搜"
    elif max_score < 0.5:
        overall = "WEAK"
        overall_label = "⚠️  检索质量弱，建议补搜"
    else:
        overall = "OK"
        overall_label = "✅ 检索质量可用"
    
    return {
        "query": query,
        "threshold": threshold,
        "max_score": max_score,
        "overall_status": overall,
        "overall_label": overall_label,
        "result_evaluations": evaluations,
    }


def main():
    parser = argparse.ArgumentParser(description='CRAG 质量评估器')
    parser.add_argument('--query', required=True, help='用户查询')
    parser.add_argument('--results', required=True, help='检索结果（用 | 分隔）')
    parser.add_argument('--threshold', type=float, default=0.3, help='补搜阈值（默认0.3）')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    args = parser.parse_args()
    
    results = [r.strip() for r in args.results.split('|') if r.strip()]
    report = evaluate_results(args.query, results, args.threshold)
    
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n📊 CRAG 质量评估报告")
        print(f"   查询: {args.query}")
        print(f"   结果数: {len(results)}")
        print(f"   最高分: {report['max_score']:.3f}")
        print(f"   整体: {report['overall_label']}")
        print()
        for e in report['result_evaluations']:
            print(f"   [{e['label']}] #{e['index']} score={e['score']:.3f} → {e['preview']}")


if __name__ == "__main__":
    main()
