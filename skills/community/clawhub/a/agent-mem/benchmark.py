#!/usr/bin/env python3
"""
记忆系统基准测试
量化评估检索准确率，每次改动后跑一次对比
"""
import sys, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from memory_recall import BM25, MultiSignalFusion, MemoryRecall

TEST_CASES = [
    {"query": "广告投放", "expected": ["advertising", "投放", "千川"], "category": "调度"},
    {"query": "数据分析", "expected": ["数据", "分析", "报表", "日报"], "category": "调度"},
    {"query": "Agent升级", "expected": ["Agent", "升级", "修复"], "category": "技术"},
    {"query": "鱼缸养鱼", "expected": ["鱼缸", "养鱼", "水质", "水族"], "category": "兴趣"},
    {"query": "考试备考", "expected": ["考试", "复习", "学习", "备考"], "category": "学习"},
]

def test_bm25():
    """BM25检索测试"""
    scores = []
    corpus = [
        "广告投放ROI分析和千川投放策略",
        "数据分析报表日报异常监控",
        "Agent升级修复和系统优化",
        "鱼缸水质管理和养鱼经验",
        "考试备考复习计划和知识梳理",
    ]
    bm25 = BM25(corpus)
    for case in TEST_CASES:
        result = bm25.score(case["query"])
        best_idx = result.index(max(result))
        best_doc = corpus[best_idx]
        # 检查最佳文档是否包含预期关键词
        match = any(kw in best_doc for kw in case["expected"])
        scores.append(1 if match else 0)
    return sum(scores) / len(scores), scores

def test_fusion():
    """多信号融合测试"""
    fusion = MultiSignalFusion()
    base_v = [{"text": "广告投放分析", "source": "2026-05-17.md", "distance": 0.3}]
    base_k = [{"text": "广告投放策略", "source": "2026-05-16.md", "score": 2.0}]
    result = fusion.fuse(base_v, base_k)
    return 1.0 if len(result) > 0 else 0.0

def run():
    print("=" * 50)
    print("  记忆系统基准测试")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # BM25测试
    bm25_acc, bm25_scores = test_bm25()
    print(f"\n1️⃣ BM25准确率: {bm25_acc*100:.0f}%")
    for i, (case, s) in enumerate(zip(TEST_CASES, bm25_scores)):
        mark = "✅" if s else "❌"
        print(f"  {mark} {case['query']} ({case['category']})")
    
    # 融合测试
    fusion_acc = test_fusion()
    print(f"\n2️⃣ 融合成功率: {fusion_acc*100:.0f}%")
    
    # 总体
    overall = (bm25_acc + fusion_acc) / 2
    print(f"\n📊 综合得分: {overall*100:.1f}%")
    
    # 写结果
    result = {
        "date": time.strftime('%Y-%m-%d %H:%M'),
        "bm25_accuracy": bm25_acc,
        "fusion_success": fusion_acc,
        "overall": overall,
        "version": "V3.1 (BM25+融合+时序)"
    }
    json.dump(result, open(Path(__file__).parent.parent.parent / 'memory' / '.benchmark-result.json', 'w'), indent=2)
    print(f"\n✅ 结果已保存到 memory/.benchmark-result.json")

if __name__ == '__main__':
    run()
