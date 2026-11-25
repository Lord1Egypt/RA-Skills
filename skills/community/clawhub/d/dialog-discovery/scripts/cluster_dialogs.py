#!/usr/bin/env python3
"""
种子分桶聚类分析脚本

用途：
- 按 weak supervision 的 seed_label 分桶
- 分析 good_seed / bad_seed / gray_* 的共性信号
- 为规则提取和人工校准提供结构化输入
"""
import argparse
import json
from datetime import datetime
from typing import Any, Dict, List


def load_scores(input_path: str) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("results", [])


def cluster_by_seed(scores: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    clusters = {
        "good_seed": [],
        "bad_seed": [],
        "gray": [],
        "gray_high_risk": [],
        "gray_potential_good": [],
    }
    for item in scores:
        seed_label = item.get("seed_label")
        if seed_label in clusters:
            clusters[seed_label].append(item)
        else:
            clusters["gray"].append(item)
    return clusters


def summarize_signal_counts(cluster: List[Dict[str, Any]], signal_group: str) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = {}
    if not cluster:
        return []
    for item in cluster:
        for signal in item.get("signals", {}).get(signal_group, []):
            counts[signal] = counts.get(signal, 0) + 1
    return sorted(
        [{"name": k, "count": v, "pct": round(v / len(cluster) * 100, 1)} for k, v in counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:8]


def analyze_cluster(cluster: List[Dict[str, Any]], cluster_name: str) -> Dict[str, Any]:
    if not cluster:
        return {
            "name": cluster_name,
            "count": 0,
            "avg_good_score": 0,
            "avg_bad_score": 0,
            "avg_confidence": 0,
            "common_positive": [],
            "common_negative": [],
            "common_risk": [],
            "common_quality": [],
        }

    avg_good = sum(i.get("scores", {}).get("good_score", 0) for i in cluster) / len(cluster)
    avg_bad = sum(i.get("scores", {}).get("bad_score", 0) for i in cluster) / len(cluster)
    avg_confidence = sum(i.get("scores", {}).get("confidence", 0) for i in cluster) / len(cluster)

    return {
        "name": cluster_name,
        "count": len(cluster),
        "avg_good_score": round(avg_good, 2),
        "avg_bad_score": round(avg_bad, 2),
        "avg_confidence": round(avg_confidence, 3),
        "common_positive": summarize_signal_counts(cluster, "positive"),
        "common_negative": summarize_signal_counts(cluster, "negative"),
        "common_risk": summarize_signal_counts(cluster, "risk"),
        "common_quality": summarize_signal_counts(cluster, "quality"),
    }


def cluster_analysis(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    clusters = cluster_by_seed(scores)
    analysis = {name: analyze_cluster(items, name) for name, items in clusters.items()}

    total = len(scores)
    stats = {"total": total}
    for name, items in clusters.items():
        stats[name] = len(items)
        stats[f"{name}_pct"] = round(len(items) / total * 100, 1) if total else 0

    print("\n📊 Seed 分桶统计:")
    for name in ["good_seed", "bad_seed", "gray_high_risk", "gray_potential_good", "gray"]:
        print(f"  {name}: {stats.get(name, 0)} 条 ({stats.get(f'{name}_pct', 0)}%)")

    return {
        "stats": stats,
        "clusters": clusters,
        "analysis": analysis,
    }


def save_results(cluster_result: Dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "stats": cluster_result["stats"],
                "analysis": cluster_result["analysis"],
                "created_at": datetime.now().isoformat(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"✅ 结果已保存: {output_path}")

    clusters_path = output_path.replace(".json", "-clusters.json")
    with open(clusters_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                **cluster_result["clusters"],
                "created_at": datetime.now().isoformat(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"✅ 分桶对话已保存: {clusters_path}")


def main():
    parser = argparse.ArgumentParser(description="基于 seed_label 的分桶聚类分析")
    parser.add_argument("--scores", required=True, help="评分/弱标签结果文件（json）")
    parser.add_argument("--scene", required=True, help="场景名称")
    parser.add_argument("--output", required=True, help="输出聚类结果文件（json）")
    args = parser.parse_args()

    scores = load_scores(args.scores)
    print(f"✅ 已加载结果: {len(scores)} 条")

    cluster_result = cluster_analysis(scores)
    save_results(cluster_result, args.output)


if __name__ == "__main__":
    main()
