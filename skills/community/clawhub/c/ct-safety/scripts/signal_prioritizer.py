#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
signal_prioritizer.py — 信号优先级排序与风险分级

P1 升级（2026-08-16，v0.1.38），基于 CIOMS PSUR / ICH E2C(R2) 要求。
多维度评分：临床严重程度、新颖性、报告频率、趋势、多源验证。
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional


# 临床严重程度映射
SEVERITY_MAP = {
    "death": 10,
    "life_threatening": 9,
    "hospitalization": 8,
    "disability": 7,
    "congenital_anomaly": 7,
    "important_medical_event": 6,
    "requires_intervention": 5,
    "moderate": 3,
    "mild": 1,
    "unknown": 0,
}

# 新颖性映射
NOVELTY_MAP = {
    "new_signal": 10,
    "refining_signal": 7,
    "confirmed_signal": 4,
    "expected_event": 2,
    "unknown": 0,
}

# 趋势映射
TREND_MAP = {
    "increasing": 10,
    "stable": 5,
    "decreasing": 2,
    "unknown": 0,
}

# 多源验证映射
MULTI_SOURCE_MAP = {
    "three_source": 10,
    "two_source": 7,
    "single_source": 3,
    "none": 0,
}


class SignalPrioritizer:
    """信号优先级排序器。"""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        参数：
            weights: 各维度权重，默认 [0.25, 0.2, 0.2, 0.15, 0.2]
        """
        if weights is None:
            weights = {
                "severity": 0.25,
                "novelty": 0.2,
                "frequency": 0.2,
                "trend": 0.15,
                "multi_source": 0.2,
            }
        self.weights = weights
    
    def compute_priority_score(self, signal: Dict) -> Dict:
        """计算单个信号的优先级得分。"""
        severity = signal.get("severity", "unknown")
        novelty = signal.get("novelty", "unknown")
        frequency = signal.get("frequency", 0)
        trend = signal.get("trend", "unknown")
        multi_source = signal.get("multi_source", "single_source")
        
        # 各维度得分（0-10）
        severity_score = SEVERITY_MAP.get(severity, 0)
        novelty_score = NOVELTY_MAP.get(novelty, 0)
        frequency_score = min(10, frequency / 10)  # 归一化到 0-10
        trend_score = TREND_MAP.get(trend, 0)
        multi_source_score = MULTI_SOURCE_MAP.get(multi_source, 0)
        
        # 综合评分
        composite = (
            self.weights["severity"] * severity_score +
            self.weights["novelty"] * novelty_score +
            self.weights["frequency"] * frequency_score +
            self.weights["trend"] * trend_score +
            self.weights["multi_source"] * multi_source_score
        )
        
        # 风险分级
        if composite >= 7:
            risk_level = "CRITICAL"
            action = "需立即行动"
        elif composite >= 5:
            risk_level = "HIGH"
            action = "需优先评估"
        elif composite >= 3:
            risk_level = "MEDIUM"
            action = "常规评估"
        else:
            risk_level = "LOW"
            action = "监测即可"
        
        return {
            "signal_id": signal.get("signal_id", ""),
            "drug": signal.get("drug", ""),
            "event": signal.get("event", ""),
            "priority_score": round(composite, 2),
            "risk_level": risk_level,
            "action_recommendation": action,
            "component_scores": {
                "severity": severity_score,
                "novelty": novelty_score,
                "frequency": round(frequency_score, 2),
                "trend": trend_score,
                "multi_source": multi_source_score,
            },
        }
    
    def prioritize(self, signals: List[Dict]) -> List[Dict]:
        """对信号列表进行优先级排序。"""
        results = [self.compute_priority_score(s) for s in signals]
        results.sort(key=lambda x: x["priority_score"], reverse=True)
        return results


def format_ascii(results: List[Dict]) -> str:
    """格式化输出。"""
    lines = []
    lines.append("=" * 70)
    lines.append("信号优先级排序结果")
    lines.append("=" * 70)
    
    header = f"{'排名':<4} {'药物':<15} {'事件':<20} {'得分':>6} {'风险等级':<10} {'行动建议'}"
    lines.append(header)
    lines.append("-" * len(header))
    
    for i, r in enumerate(results, 1):
        lines.append(
            f"{i:<4} {r['drug']:<15} {r['event']:<20} "
            f"{r['priority_score']:>6.2f} {r['risk_level']:<10} {r['action_recommendation']}"
        )
    
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="信号优先级排序")
    p.add_argument("--signals", type=str, default=None, help="信号列表 JSON 文件")
    p.add_argument("--format", choices=["json", "ascii"], default="ascii")
    p.add_argument("--output", type=str, default=None)
    
    args = p.parse_args()
    
    signals = []
    if args.signals:
        with open(args.signals, "r", encoding="utf-8") as f:
            signals = json.load(f)
    
    prioritizer = SignalPrioritizer()
    results = prioritizer.prioritize(signals)
    
    if args.format == "json":
        out = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        out = format_ascii(results)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入: {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
