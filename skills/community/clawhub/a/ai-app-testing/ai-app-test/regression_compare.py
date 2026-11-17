#!/usr/bin/env python3
"""Regression Compare — baseline vs current comparison, diff analysis, regression alarms"""

import json, time, statistics, sys, os, re
from datetime import datetime
from typing import Optional

REGRESSION_METRICS_DEF = {
    "accuracy_rate": {"name":"准确率","unit":"%","higher_is_better":True,"threshold":5.0},
    "latency_p50": {"name":"延迟P50","unit":"s","higher_is_better":False,"threshold":0.5},
    "latency_p95": {"name":"延迟P95","unit":"s","higher_is_better":False,"threshold":1.0},
    "success_rate": {"name":"成功率","unit":"%","higher_is_better":True,"threshold":2.0},
    "hallucination_rate": {"name":"幻觉率","unit":"%","higher_is_better":False,"threshold":3.0},
    "tool_accuracy": {"name":"工具调用准确率","unit":"%","higher_is_better":True,"threshold":5.0},
}

SAMPLE_BASELINE = {
    "timestamp": "2026-07-25T10:00:00",
    "model": "deepseek/deepseek-v4-flash",
    "version": "1.0.0",
    "metrics": {
        "accuracy_rate": 92.5,
        "latency_p50": 1.2,
        "latency_p95": 3.8,
        "success_rate": 99.2,
        "hallucination_rate": 1.5,
        "tool_accuracy": 88.0,
    }
}

SAMPLE_CURRENT = {
    "timestamp": datetime.now().isoformat(),
    "model": "deepseek/deepseek-v4-flash",
    "version": "1.1.0",
    "metrics": {
        "accuracy_rate": 90.2,
        "latency_p50": 1.5,
        "latency_p95": 4.2,
        "success_rate": 98.5,
        "hallucination_rate": 2.8,
        "tool_accuracy": 85.0,
    }
}

class RegressionComparator:
    def __init__(self, baseline_path: Optional[str] = None):
        self.baseline_path = baseline_path

    def load_baseline(self, data: Optional[dict] = None, path: Optional[str] = None) -> dict:
        """Load baseline from dict, file, or fallback to sample"""
        if data: return data
        if path or self.baseline_path:
            p = path or self.baseline_path
            with open(p) as f: return json.load(f)
        return SAMPLE_BASELINE

    def compare(self, baseline: dict, current: dict) -> dict:
        """Compare current metrics against baseline"""
        bm = baseline.get("metrics", {})
        cm = current.get("metrics", {})
        diffs = {}
        alarms = []
        improvements = []

        for key, meta in REGRESSION_METRICS_DEF.items():
            b_val = bm.get(key)
            c_val = cm.get(key)
            if b_val is None or c_val is None:
                diffs[key] = {"baseline": b_val, "current": c_val, "diff": None, "status": "N/A"}
                continue

            diff = round(c_val - b_val, 2)
            pct_change = round((c_val - b_val) / b_val * 100, 1) if b_val != 0 else 0
            higher_better = meta["higher_is_better"]
            threshold = meta["threshold"]

            # Determine regression or improvement
            if higher_better:
                if diff < -threshold:
                    alarms.append({"metric": key, "name": meta["name"], "diff": diff,
                                   "pct_change": pct_change, "message": f"{meta['name']}下降{pct_change}%"})
                    status = "REGRESSION"
                elif diff > threshold:
                    improvements.append({"metric": key, "name": meta["name"], "diff": diff,
                                         "pct_change": pct_change})
                    status = "IMPROVED"
                else:
                    status = "OK"
            else:
                if diff > threshold:
                    alarms.append({"metric": key, "name": meta["name"], "diff": diff,
                                   "pct_change": pct_change, "message": f"{meta['name']}增加{diff}{meta['unit']}"})
                    status = "REGRESSION"
                elif diff < -threshold:
                    improvements.append({"metric": key, "name": meta["name"], "diff": diff,
                                         "pct_change": pct_change})
                    status = "IMPROVED"
                else:
                    status = "OK"

            diffs[key] = {
                "baseline": b_val, "current": c_val, "diff": diff,
                "pct_change": pct_change, "threshold": threshold,
                "higher_is_better": higher_better, "status": status,
                "unit": meta["unit"], "name": meta["name"]
            }

        overall = "PASS" if len(alarms) == 0 else "REGRESSION_DETECTED"

        return {
            "baseline_info": {"ts": baseline.get("timestamp"),"version": baseline.get("version")},
            "current_info": {"ts": current.get("timestamp"),"version": current.get("version")},
            "overall": overall,
            "alarms": alarms,
            "improvements": improvements,
            "metrics_diff": diffs,
            "summary": {
                "total_metrics": len(diffs),
                "unchanged": sum(1 for v in diffs.values() if v.get("status") == "OK"),
                "regressions": len(alarms),
                "improvements": len(improvements)
            }
        }

    def compare_with_file(self, current_path: str, baseline_path: Optional[str] = None) -> dict:
        """Compare current results file against baseline"""
        with open(current_path) as f: current = json.load(f)
        baseline = self.load_baseline(path=baseline_path)
        return self.compare(baseline, current)

    def save_baseline(self, data: dict, path: Optional[str] = None) -> str:
        """Save current result as new baseline"""
        p = path or self.baseline_path or "baseline_results.json"
        os.makedirs(os.path.dirname(p) if os.path.dirname(p) else ".", exist_ok=True)
        data["timestamp"] = datetime.now().isoformat()
        with open(p,"w") as f: json.dump(data, f, indent=2, ensure_ascii=False)
        return p

def generate_report(result: dict, path: Optional[str] = None) -> str:
    lines = [f"# 回归测试报告\n"]
    overall = result["overall"]
    icon = "✅" if overall == "PASS" else "❌"
    lines.append(f"整体结果: {icon} {overall}\n")
    lines.append(f"基线: {result['baseline_info']['ts']} (v{result['baseline_info']['version']})")
    lines.append(f"当前: {result['current_info']['ts']} (v{result['current_info']['version']})\n")
    lines.append("## 指标对比\n")
    lines.append("| 指标 | 基线 | 当前 | 差值 | 变化% | 阈值 | 状态 |")
    lines.append("|------|------|------|------|-------|------|------|")
    for key, m in result["metrics_diff"].items():
        status = {"OK":"✅","REGRESSION":"❌","IMPROVED":"📈","N/A":"➖"}.get(m.get("status",""),"➖")
        lines.append(f"| {m['name']} | {m['baseline']}{m['unit']} | {m['current']}{m['unit']} | "
                     f"{m['diff']:+.2f} | {m['pct_change']:+.1f}% | {m['threshold']}{m['unit']} | {status} |")
    if result.get("alarms"):
        lines.append("\n## 回归告警\n")
        for a in result["alarms"]:
            lines.append(f"  ❌ {a['message']}")
    if result.get("improvements"):
        lines.append("\n## 改进项\n")
        for imp in result["improvements"]:
            lines.append(f"  📈 {imp['name']}: {imp['pct_change']:+.1f}%")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

if __name__ == "__main__":
    import sys
    comparator = RegressionComparator()
    baseline = SAMPLE_BASELINE
    current = SAMPLE_CURRENT

    # Allow override from files
    if len(sys.argv) >= 3:
        with open(sys.argv[1]) as f: baseline = json.load(f)
        with open(sys.argv[2]) as f: current = json.load(f)
    elif len(sys.argv) >= 2:
        with open(sys.argv[1]) as f: current = json.load(f)

    result = comparator.compare(baseline, current)
    print(generate_report(result))
    sys.exit(0 if result["overall"] == "PASS" else 1)
