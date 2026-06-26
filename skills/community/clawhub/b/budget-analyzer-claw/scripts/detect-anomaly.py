#!/usr/bin/env python3
"""
detect-anomaly.py — 基于 Z-score 检测成本异常

用法：
  python3 detect-anomaly.py --current 450 --history 100 120 110 130 105 115

输出：
  NORMAL / WARNING / CRITICAL + 说明
"""
import argparse
import math


def detect_anomaly(current_cost, historical_costs):
    if len(historical_costs) < 3:
        return "UNKNOWN", "历史数据不足（需至少 3 个数据点）"

    n = len(historical_costs)
    mean = sum(historical_costs) / n
    variance = sum((x - mean) ** 2 for x in historical_costs) / n
    std = math.sqrt(variance)

    if std == 0:
        return "NORMAL", "成本稳定，无波动"

    z_score = (current_cost - mean) / std

    if z_score > 3:
        return "CRITICAL", f"成本异常激增 {z_score:.1f}σ，超出均值 {(current_cost/mean - 1)*100:.0f}%，疑似死循环或配置错误"
    elif z_score > 2:
        return "WARNING", f"成本偏高 {z_score:.1f}σ（均值 ¥{mean:.1f}，当前 ¥{current_cost:.1f}），建议关注"
    else:
        return "NORMAL", f"成本正常（均值 ¥{mean:.1f}，当前 ¥{current_cost:.1f}，{z_score:+.1f}σ）"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", type=float, required=True, help="当前成本（元）")
    parser.add_argument("--history", type=float, nargs="+", required=True, help="历史成本列表（元）")
    args = parser.parse_args()

    level, message = detect_anomaly(args.current, args.history)
    icon = {"NORMAL": "✅", "WARNING": "⚠️", "CRITICAL": "🚨", "UNKNOWN": "❓"}.get(level, "")
    print(f"{icon} [{level}] {message}")
    return 0 if level in ("NORMAL", "UNKNOWN") else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
