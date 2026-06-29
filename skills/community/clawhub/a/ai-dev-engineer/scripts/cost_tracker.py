#!/usr/bin/env python3
"""
Token Cost Tracker — AI应用成本追踪脚本

用法:
  python cost_tracker.py --model gpt-4o --input-tokens 1500 --output-tokens 500
  python cost_tracker.py --log-file api_calls.jsonl

配置文件:
  内置主流模型定价表, 支持 OpenAI / DeepSeek / DashScope / Anthropic
"""
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
from collections import defaultdict


# 模型定价表 (USD per 1M tokens)
PRICING = {
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00, "provider": "OpenAI"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "provider": "OpenAI"},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00, "provider": "OpenAI"},
    # DeepSeek
    "deepseek-chat": {"input": 0.14, "output": 0.28, "provider": "DeepSeek"},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19, "provider": "DeepSeek"},
    # DashScope (阿里云, ¥转$约 ÷7.2)
    "qwen-max": {"input": 0.35, "output": 1.39, "provider": "DashScope"},
    "qwen-plus": {"input": 0.11, "output": 0.42, "provider": "DashScope"},
    "qwen-turbo": {"input": 0.04, "output": 0.08, "provider": "DashScope"},
    # Anthropic
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00, "provider": "Anthropic"},
    "claude-3-haiku": {"input": 0.25, "output": 1.25, "provider": "Anthropic"},
    # Google
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00, "provider": "Google"},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30, "provider": "Google"},
    # Embedding
    "text-embedding-3-small": {"input": 0.02, "output": 0.0, "provider": "OpenAI"},
    "text-embedding-3-large": {"input": 0.13, "output": 0.0, "provider": "OpenAI"},
}


@dataclass
class ApiCall:
    """单次 API 调用记录"""
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    timestamp: str = ""


@dataclass
class CostReport:
    """成本分析报告"""
    total_cost: float = 0.0
    total_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    by_model: Dict[str, float] = None
    by_date: Dict[str, float] = None

    def __post_init__(self):
        self.by_model = self.by_model or defaultdict(float)
        self.by_date = self.by_date or defaultdict(float)


def calc_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """计算单次调用成本 (USD)"""
    if model not in PRICING:
        print(f"⚠️  未知模型 {model}, 使用默认定价 ($1/M input, $3/M output)")
        pricing = {"input": 1.0, "output": 3.0}
    else:
        pricing = PRICING[model]

    return (input_tokens / 1_000_000) * pricing["input"] + \
           (output_tokens / 1_000_000) * pricing["output"]


def estimate_daily_cost(
    dau: int, calls_per_user: int,
    input_tokens_per_call: int, output_tokens_per_call: int,
    model: str
) -> Tuple[float, float]:
    """估算日/月成本"""
    daily = dau * calls_per_user
    daily_cost = daily * calc_cost(model, input_tokens_per_call, output_tokens_per_call)
    return daily_cost, daily_cost * 30


def parse_log_file(log_path: str) -> CostReport:
    """解析 API 调用日志文件"""
    report = CostReport()

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                call = json.loads(line)
                model = call.get("model", "unknown")
                input_tokens = call.get("input_tokens", 0)
                output_tokens = call.get("output_tokens", 0)
                date = call.get("timestamp", "")[:10]

                cost = calc_cost(model, input_tokens, output_tokens)
                report.total_cost += cost
                report.total_calls += 1
                report.total_input_tokens += input_tokens
                report.total_output_tokens += output_tokens
                report.by_model[model] += cost
                if date:
                    report.by_date[date] += cost
            except (json.JSONDecodeError, KeyError):
                continue

    return report


def print_report(report: CostReport):
    """打印成本报告"""
    print(f"\n{'='*60}")
    print(f"📊 Token 成本分析报告")
    print(f"{'='*60}")
    print(f"  总调用次数:     {report.total_calls:,}")
    print(f"  总输入 Token:   {report.total_input_tokens:,}")
    print(f"  总输出 Token:   {report.total_output_tokens:,}")
    print(f"  总费用 (USD):   ${report.total_cost:.4f}")
    print(f"  月估费用 (USD): ${report.total_cost * 30:.2f}")

    if report.by_model:
        print(f"\n  📋 按模型分布:")
        for model, cost in sorted(report.by_model.items(), key=lambda x: -x[1]):
            pct = cost / report.total_cost * 100 if report.total_cost > 0 else 0
            print(f"     {model:25s}: ${cost:.4f} ({pct:.1f}%)")

    if report.by_date and len(report.by_date) > 1:
        print(f"\n  📅 按日期分布:")
        for date, cost in sorted(report.by_date.items()):
            print(f"     {date}: ${cost:.4f}")

    print(f"{'='*60}\n")


def print_pricing_table():
    """打印定价对比表"""
    print(f"\n{'='*70}")
    print(f"💰 模型定价对比 (USD per 1M tokens)")
    print(f"{'='*70}")
    print(f"  {'模型':<25s} {'提供商':<12s} {'输入':>8s} {'输出':>8s}")
    print(f"  {'-'*53}")
    for model, p in PRICING.items():
        print(f"  {model:<25s} {p['provider']:<12s} ${p['input']:>7.2f} ${p['output']:>7.2f}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Token Cost Tracker")
    parser.add_argument("--model", default="gpt-4o-mini", help="模型名称")
    parser.add_argument("--input-tokens", type=int, default=0, help="输入 Token 数")
    parser.add_argument("--output-tokens", type=int, default=0, help="输出 Token 数")
    parser.add_argument("--log-file", default="", help="API 调用日志文件 (JSONL)")
    parser.add_argument("--estimate", action="store_true", help="估算日/月成本")
    parser.add_argument("--dau", type=int, default=1000, help="日活用户数")
    parser.add_argument("--calls-per-user", type=int, default=10, help="每用户日均调用次数")
    parser.add_argument("--pricing", action="store_true", help="显示定价表")

    args = parser.parse_args()

    if args.pricing:
        print_pricing_table()
    elif args.log_file:
        report = parse_log_file(args.log_file)
        print_report(report)
    elif args.estimate:
        daily, monthly = estimate_daily_cost(
            args.dau, args.calls_per_user,
            args.input_tokens, args.output_tokens,
            args.model
        )
        print(f"\n{'='*60}")
        print(f"📈 成本估算")
        print(f"   模型: {args.model}")
        print(f"   DAU: {args.dau:,} × 平均 {args.calls_per_user} 次调用")
        print(f"   每次: {args.input_tokens} input + {args.output_tokens} output tokens")
        print(f"   日成本: ${daily:.2f}")
        print(f"   月成本: ${monthly:.2f}")
        print(f"   年成本: ${monthly * 12:,.2f}")
        print(f"{'='*60}\n")
    elif args.input_tokens > 0 or args.output_tokens > 0:
        cost = calc_cost(args.model, args.input_tokens, args.output_tokens)
        print(f"\n  单次调用成本: ${cost:.6f}")
        print(f"  千次调用成本: ${cost * 1000:.4f}\n")
    else:
        parser.print_help()
