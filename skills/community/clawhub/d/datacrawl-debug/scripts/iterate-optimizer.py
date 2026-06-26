#!/usr/bin/env python3
"""IterateOptimizer — 自我迭代优化引擎"""

import argparse
import json
import sys
from datetime import datetime


def analyze_run_history(runs: list) -> dict:
    """分析运行历史，识别优化方向"""
    if not runs:
        return {"error": "无运行历史数据"}

    total = len(runs)
    success = [r for r in runs if r.get("status") == "success"]
    failed = [r for r in runs if r.get("status") == "fail"]
    partial = [r for r in runs if r.get("status") == "partial"]

    success_rate = len(success) / total * 100 if total > 0 else 0
    partial_rate = len(partial) / total * 100 if total > 0 else 0
    fail_rate = len(failed) / total * 100 if total > 0 else 0

    # 错误聚类
    error_clusters = {}
    for r in failed + partial:
        error = r.get("error_type", r.get("error", "unknown"))
        error_clusters[error] = error_clusters.get(error, 0) + 1

    # 性能趋势
    durations = [r.get("duration_seconds", 0) for r in runs if r.get("duration_seconds")]
    avg_duration = sum(durations) / len(durations) if durations else 0

    records_per_run = [r.get("records_extracted", 0) for r in runs if r.get("records_extracted")]
    avg_records = sum(records_per_run) / len(records_per_run) if records_per_run else 0

    # 字段覆盖率
    field_coverage = {}
    for r in success:
        fields = r.get("fields", {})
        for k, v in fields.items():
            if k not in field_coverage:
                field_coverage[k] = {"filled": 0, "total": 0}
            field_coverage[k]["total"] += 1
            if v:
                field_coverage[k]["filled"] += 1

    # 优化建议
    suggestions = []
    if success_rate < 50:
        suggestions.append({
            "priority": "critical",
            "area": "稳定性",
            "issue": f"成功率仅{success_rate:.0f}%",
            "action": "先解决最频繁的错误: " + max(error_clusters, key=error_clusters.get) if error_clusters else "分析失败原因",
        })
    if fail_rate > 30:
        top_error = max(error_clusters, key=error_clusters.get) if error_clusters else "unknown"
        suggestions.append({
            "priority": "high",
            "area": "错误修复",
            "issue": f"主要错误类型: {top_error} ({error_clusters.get(top_error, 0)}次)",
            "action": "针对此错误类型添加重试逻辑和异常处理",
        })
    if avg_duration > 30:
        suggestions.append({
            "priority": "medium",
            "area": "性能",
            "issue": f"平均耗时{avg_duration:.1f}秒",
            "action": "考虑异步请求、缓存、减少不必要的等待",
        })
    for field, stats in field_coverage.items():
        cov = stats["filled"] / stats["total"] * 100 if stats["total"] > 0 else 0
        if cov < 70:
            suggestions.append({
                "priority": "medium",
                "area": "字段覆盖",
                "issue": f"字段'{field}'填充率仅{cov:.0f}%",
                "action": "检查该字段的选择器是否需要更新",
            })
    if not suggestions:
        suggestions.append({"priority": "low", "area": "持续优化", "issue": "运行状态良好", "action": "保持当前策略，关注页面结构变化"})

    # 趋势判断
    if len(runs) >= 3:
        recent_3 = runs[-3:]
        recent_rate = sum(1 for r in recent_3 if r.get("status") == "success") / 3 * 100
        if recent_rate > success_rate:
            trend = "improving"
        elif recent_rate < success_rate:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"

    return {
        "summary": {
            "total_runs": total,
            "success_rate": round(success_rate, 1),
            "partial_rate": round(partial_rate, 1),
            "fail_rate": round(fail_rate, 1),
            "avg_duration_seconds": round(avg_duration, 1),
            "avg_records_per_run": round(avg_records, 1),
            "trend": trend,
        },
        "error_clusters": dict(sorted(error_clusters.items(), key=lambda x: -x[1])),
        "field_coverage": {k: round(v["filled"] / v["total"] * 100, 1) for k, v in field_coverage.items() if v["total"] > 0},
        "suggestions": suggestions,
    }


def generate_improved_config(current_config: dict, run_analysis: dict) -> dict:
    """基于运行分析生成改进配置"""
    improved = dict(current_config)
    changes = []

    success_rate = run_analysis.get("summary", {}).get("success_rate", 100)
    avg_duration = run_analysis.get("summary", {}).get("avg_duration_seconds", 0)

    # 调整请求间隔
    if success_rate < 70:
        old_delay = improved.get("request_delay", 1)
        new_delay = min(old_delay * 2, 10)
        improved["request_delay"] = new_delay
        changes.append(f"请求间隔: {old_delay}s → {new_delay}s (成功率低，降低频率)")

    # 调整超时
    if avg_duration > 20:
        old_timeout = improved.get("timeout", 15)
        new_timeout = int(old_timeout * 1.5)
        improved["timeout"] = new_timeout
        changes.append(f"超时设置: {old_timeout}s → {new_timeout}s (响应慢，增加容错)")

    # 调整重试次数
    if success_rate < 80:
        old_retries = improved.get("max_retries", 1)
        new_retries = min(old_retries + 2, 5)
        improved["max_retries"] = new_retries
        changes.append(f"重试次数: {old_retries} → {new_retries}")

    # 建议切换模式
    error_clusters = run_analysis.get("error_clusters", {})
    if "selector_error" in error_clusters or "timeout" in error_clusters:
        if improved.get("mode") == "static":
            improved["mode"] = "dynamic"
            changes.append("处理模式: static → dynamic (页面可能需要JS渲染)")

    # 字段选择器更新建议
    field_coverage = run_analysis.get("field_coverage", {})
    for field, cov in field_coverage.items():
        if cov < 70:
            changes.append(f"字段'{field}'覆盖率{cov}%，建议更新选择器")

    improved["last_updated"] = datetime.now().isoformat()
    improved["iteration"] = improved.get("iteration", 0) + 1

    return {
        "improved_config": improved,
        "changes": changes,
        "iteration": improved["iteration"],
    }


def main():
    parser = argparse.ArgumentParser(description="IterateOptimizer - 自我迭代优化引擎")
    sub = parser.add_subparsers(dest="command")

    p_analyze = sub.add_parser("analyze", help="分析运行历史")
    p_analyze.add_argument("--input", type=str, required=True, help="运行历史JSON数据或文件路径")

    p_improve = sub.add_parser("improve", help="生成改进配置")
    p_improve.add_argument("--config", type=str, required=True, help="当前配置JSON")
    p_improve.add_argument("--analysis", type=str, required=True, help="运行分析结果JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    result = {}
    if args.command == "analyze":
        data = args.input
        if args.input.endswith(".json"):
            try:
                with open(args.input, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = json.loads(args.input)
        else:
            data = json.loads(args.input)
        result = analyze_run_history(data)
    elif args.command == "improve":
        config = json.loads(args.config)
        analysis = json.loads(args.analysis)
        result = generate_improved_config(config, analysis)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
