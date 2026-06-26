#!/usr/bin/env python3
"""API Cost Tracker — Analyze and optimize AI API spending across providers."""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path

# Pricing per 1M tokens (input/output) — March 2026
MODEL_PRICING = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-4": (30.00, 60.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    "o1": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    "o1-pro": (150.00, 600.00),
    "o3": (10.00, 40.00),
    "o3-mini": (1.10, 4.40),
    "o4-mini": (1.10, 4.40),
    "gpt-4.1": (2.00, 8.00),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    # Anthropic
    "claude-opus-4": (15.00, 75.00),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-haiku-3.5": (0.80, 4.00),
    "claude-3-opus": (15.00, 75.00),
    "claude-3.5-sonnet": (3.00, 15.00),
    "claude-3-haiku": (0.25, 1.25),
    # Google
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.5-flash": (0.15, 0.60),
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.5-flash": (0.075, 0.30),
    # DeepSeek
    "deepseek-chat": (0.14, 0.28),
    "deepseek-reasoner": (0.55, 2.19),
    # Meta
    "llama-3.3-70b": (0.18, 0.18),
    "llama-3.1-405b": (1.79, 1.79),
    "llama-3.1-70b": (0.18, 0.18),
    "llama-3.1-8b": (0.055, 0.055),
    # Mistral
    "mistral-large": (2.00, 6.00),
    "mistral-small": (0.10, 0.30),
    "codestral": (0.30, 0.90),
}

# Cheaper alternatives for optimization suggestions
MODEL_ALTERNATIVES = {
    "gpt-4o": ["gpt-4o-mini", "gemini-2.5-flash", "claude-haiku-3.5"],
    "gpt-4-turbo": ["gpt-4o", "claude-sonnet-4", "gemini-2.5-pro"],
    "gpt-4": ["gpt-4o", "claude-sonnet-4"],
    "claude-opus-4": ["claude-sonnet-4", "gemini-2.5-pro", "gpt-4o"],
    "claude-3-opus": ["claude-sonnet-4", "gpt-4o"],
    "claude-3.5-sonnet": ["claude-haiku-3.5", "gpt-4o-mini", "gemini-2.5-flash"],
    "claude-sonnet-4": ["claude-haiku-3.5", "gpt-4o-mini", "gemini-2.5-flash"],
    "o1": ["o3-mini", "deepseek-reasoner"],
    "o1-mini": ["o3-mini", "deepseek-reasoner"],
    "o1-pro": ["o1", "o3-mini"],
    "gemini-2.5-pro": ["gemini-2.5-flash", "gpt-4o-mini"],
    "gemini-1.5-pro": ["gemini-2.5-flash", "gemini-1.5-flash"],
}


def normalize_model_name(name):
    """Normalize model identifiers to match pricing keys."""
    name = name.lower().strip()
    # Strip provider prefixes (openrouter style)
    for prefix in ["openai/", "anthropic/", "google/", "meta-llama/", "mistralai/", "deepseek/"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    # Strip date suffixes
    for suffix_pattern in ["-20", ":20"]:
        idx = name.find(suffix_pattern)
        if idx > 0 and idx < len(name) - 2:
            rest = name[idx + 1:]
            if rest[:4].isdigit():
                name = name[:idx]
    # Common aliases
    aliases = {
        "gpt-4o-2024-08-06": "gpt-4o",
        "gpt-4-0613": "gpt-4",
        "claude-3-5-sonnet": "claude-3.5-sonnet",
        "claude-3-5-haiku": "claude-haiku-3.5",
        "claude-3.5-haiku": "claude-haiku-3.5",
    }
    return aliases.get(name, name)


def get_pricing(model):
    """Get (input_per_1M, output_per_1M) for a model."""
    normalized = normalize_model_name(model)
    if normalized in MODEL_PRICING:
        return MODEL_PRICING[normalized]
    # Fuzzy match
    for key in MODEL_PRICING:
        if key in normalized or normalized in key:
            return MODEL_PRICING[key]
    return None


def calculate_cost(model, input_tokens, output_tokens):
    """Calculate cost for a single request."""
    pricing = get_pricing(model)
    if not pricing:
        return None
    input_cost = (input_tokens / 1_000_000) * pricing[0]
    output_cost = (output_tokens / 1_000_000) * pricing[1]
    return input_cost + output_cost


class UsageEntry:
    __slots__ = ("timestamp", "model", "input_tokens", "output_tokens", "cost", "metadata")

    def __init__(self, timestamp, model, input_tokens, output_tokens, cost=None, metadata=None):
        self.timestamp = timestamp
        self.model = model
        self.input_tokens = int(input_tokens)
        self.output_tokens = int(output_tokens)
        self.cost = cost if cost is not None else calculate_cost(model, self.input_tokens, self.output_tokens)
        self.metadata = metadata or {}


def parse_openrouter(data):
    """Parse OpenRouter activity JSON."""
    entries = []
    items = data if isinstance(data, list) else data.get("data", data.get("activity", []))
    for item in items:
        ts = item.get("created_at") or item.get("timestamp") or item.get("date")
        model = item.get("model", "unknown")
        usage = item.get("usage", {})
        inp = usage.get("prompt_tokens", 0) or item.get("prompt_tokens", 0) or item.get("tokens_prompt", 0)
        out = usage.get("completion_tokens", 0) or item.get("completion_tokens", 0) or item.get("tokens_completion", 0)
        cost = item.get("total_cost") or item.get("cost")
        if cost is not None:
            cost = float(cost)
        try:
            timestamp = datetime.fromisoformat(str(ts).replace("Z", "+00:00")) if ts else datetime.now()
        except (ValueError, TypeError):
            timestamp = datetime.now()
        entries.append(UsageEntry(timestamp, model, inp, out, cost))
    return entries


def parse_openai(data):
    """Parse OpenAI billing/usage export."""
    entries = []
    items = data if isinstance(data, list) else data.get("data", [])
    for item in items:
        ts = item.get("timestamp") or item.get("aggregation_timestamp")
        model = item.get("snapshot_id") or item.get("model", "unknown")
        inp = item.get("n_context_tokens_total", 0) or item.get("input_tokens", 0)
        out = item.get("n_generated_tokens_total", 0) or item.get("output_tokens", 0)
        cost = item.get("cost") or item.get("value")
        try:
            timestamp = datetime.fromtimestamp(int(ts)) if ts and str(ts).isdigit() else datetime.fromisoformat(str(ts))
        except (ValueError, TypeError):
            timestamp = datetime.now()
        entries.append(UsageEntry(timestamp, model, inp, out, float(cost) if cost else None))
    return entries


def parse_anthropic(data):
    """Parse Anthropic usage data."""
    entries = []
    items = data if isinstance(data, list) else data.get("data", [])
    for item in items:
        ts = item.get("created_at") or item.get("timestamp")
        model = item.get("model", "unknown")
        inp = item.get("input_tokens", 0)
        out = item.get("output_tokens", 0)
        cost = item.get("cost")
        try:
            timestamp = datetime.fromisoformat(str(ts).replace("Z", "+00:00")) if ts else datetime.now()
        except (ValueError, TypeError):
            timestamp = datetime.now()
        entries.append(UsageEntry(timestamp, model, inp, out, float(cost) if cost else None))
    return entries


def parse_generic_csv(filepath):
    """Parse generic CSV: timestamp,model,input_tokens,output_tokens[,cost]."""
    entries = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row.get("timestamp") or row.get("date") or row.get("time")
            model = row.get("model", "unknown")
            inp = int(row.get("input_tokens", 0) or row.get("tokens_in", 0) or 0)
            out = int(row.get("output_tokens", 0) or row.get("tokens_out", 0) or 0)
            cost = float(row["cost"]) if "cost" in row and row["cost"] else None
            try:
                timestamp = datetime.fromisoformat(str(ts)) if ts else datetime.now()
            except (ValueError, TypeError):
                timestamp = datetime.now()
            entries.append(UsageEntry(timestamp, model, inp, out, cost))
    return entries


def load_data(provider, filepath):
    """Load and parse usage data from file."""
    if filepath.endswith(".csv"):
        return parse_generic_csv(filepath)

    with open(filepath) as f:
        data = json.load(f)

    parsers = {
        "openrouter": parse_openrouter,
        "openai": parse_openai,
        "anthropic": parse_anthropic,
        "auto": None,
    }

    if provider == "auto":
        # Try to auto-detect
        if isinstance(data, list) and data:
            sample = data[0]
        elif isinstance(data, dict):
            for key in ("data", "activity", "usage"):
                if key in data and isinstance(data[key], list) and data[key]:
                    sample = data[key][0]
                    break
            else:
                sample = data
        else:
            sample = {}

        if "tokens_prompt" in sample or "total_cost" in sample:
            provider = "openrouter"
        elif "n_context_tokens_total" in sample or "snapshot_id" in sample:
            provider = "openai"
        elif "input_tokens" in sample and "output_tokens" in sample:
            provider = "anthropic"
        else:
            provider = "openrouter"  # fallback

    parser = parsers.get(provider, parse_openrouter)
    return parser(data)


def filter_entries(entries, days=None, since=None):
    """Filter entries by time range."""
    if not days and not since:
        return entries
    cutoff = datetime.now() - timedelta(days=days) if days else since
    if cutoff.tzinfo is None:
        return [e for e in entries if e.timestamp.replace(tzinfo=None) >= cutoff]
    return [e for e in entries if e.timestamp >= cutoff]


def aggregate_by(entries, dimension):
    """Group entries by dimension and compute aggregates."""
    groups = defaultdict(lambda: {"count": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0})

    for e in entries:
        if dimension == "model":
            key = normalize_model_name(e.model)
        elif dimension == "day":
            key = e.timestamp.strftime("%Y-%m-%d")
        elif dimension == "week":
            key = e.timestamp.strftime("%Y-W%W")
        elif dimension == "hour":
            key = e.timestamp.strftime("%Y-%m-%d %H:00")
        else:
            key = "total"

        g = groups[key]
        g["count"] += 1
        g["input_tokens"] += e.input_tokens
        g["output_tokens"] += e.output_tokens
        g["cost"] += e.cost or 0

    return dict(sorted(groups.items(), key=lambda x: x[1]["cost"], reverse=True))


def compute_trends(entries):
    """Compute spending trends."""
    if len(entries) < 2:
        return {}

    by_day = aggregate_by(entries, "day")
    days = sorted(by_day.keys())
    costs = [by_day[d]["cost"] for d in days]

    if len(costs) < 2:
        return {}

    avg_daily = sum(costs) / len(costs)
    recent_avg = sum(costs[-7:]) / min(7, len(costs[-7:]))
    projected_monthly = avg_daily * 30

    # Trend direction
    if len(costs) >= 7:
        first_half = sum(costs[:len(costs) // 2]) / (len(costs) // 2)
        second_half = sum(costs[len(costs) // 2:]) / (len(costs) - len(costs) // 2)
        if second_half > first_half * 1.1:
            direction = "increasing"
        elif second_half < first_half * 0.9:
            direction = "decreasing"
        else:
            direction = "stable"
    else:
        direction = "insufficient data"

    # Find peak day
    peak_day = max(by_day.items(), key=lambda x: x[1]["cost"])

    return {
        "avg_daily_cost": avg_daily,
        "recent_7d_avg": recent_avg,
        "projected_monthly": projected_monthly,
        "direction": direction,
        "peak_day": peak_day[0],
        "peak_day_cost": peak_day[1]["cost"],
        "total_days": len(days),
    }


def compute_optimization(entries):
    """Suggest model substitutions to reduce costs."""
    by_model = aggregate_by(entries, "model")
    suggestions = []

    for model, stats in by_model.items():
        if model not in MODEL_ALTERNATIVES:
            continue
        current_cost = stats["cost"]
        if current_cost < 0.01:
            continue

        for alt in MODEL_ALTERNATIVES[model]:
            alt_pricing = get_pricing(alt)
            if not alt_pricing:
                continue
            alt_cost = (stats["input_tokens"] / 1_000_000) * alt_pricing[0] + \
                       (stats["output_tokens"] / 1_000_000) * alt_pricing[1]
            savings = current_cost - alt_cost
            if savings > 0.01:
                suggestions.append({
                    "current_model": model,
                    "alternative": alt,
                    "current_cost": current_cost,
                    "alternative_cost": alt_cost,
                    "savings": savings,
                    "savings_pct": (savings / current_cost) * 100 if current_cost else 0,
                })

    return sorted(suggestions, key=lambda x: x["savings"], reverse=True)


def format_cost(amount):
    """Format dollar amount."""
    if amount < 0.01:
        return f"${amount:.4f}"
    return f"${amount:.2f}"


def format_tokens(count):
    """Format token count with K/M suffixes."""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    if count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def output_terminal(entries, args):
    """Print analysis to terminal."""
    total_cost = sum(e.cost or 0 for e in entries)
    total_input = sum(e.input_tokens for e in entries)
    total_output = sum(e.output_tokens for e in entries)

    print(f"\n{'=' * 60}")
    print(f"  API Cost Analysis — {len(entries)} requests")
    print(f"{'=' * 60}")
    print(f"  Total Cost:     {format_cost(total_cost)}")
    print(f"  Input Tokens:   {format_tokens(total_input)}")
    print(f"  Output Tokens:  {format_tokens(total_output)}")
    print(f"  Avg per Request: {format_cost(total_cost / len(entries)) if entries else '$0.00'}")
    print()

    # Breakdown
    dimension = args.by or "model"
    groups = aggregate_by(entries, dimension)
    print(f"  Breakdown by {dimension}:")
    print(f"  {'─' * 56}")
    print(f"  {'Key':<25} {'Requests':>8} {'Input':>8} {'Output':>8} {'Cost':>10}")
    print(f"  {'─' * 56}")
    for key, stats in groups.items():
        print(f"  {key:<25} {stats['count']:>8} {format_tokens(stats['input_tokens']):>8} "
              f"{format_tokens(stats['output_tokens']):>8} {format_cost(stats['cost']):>10}")
    print()

    # Top expensive requests
    if args.top:
        sorted_entries = sorted(entries, key=lambda e: e.cost or 0, reverse=True)[:args.top]
        print(f"  Top {args.top} Most Expensive Requests:")
        print(f"  {'─' * 56}")
        for i, e in enumerate(sorted_entries, 1):
            ts = e.timestamp.strftime("%m-%d %H:%M") if hasattr(e.timestamp, 'strftime') else str(e.timestamp)[:16]
            model = normalize_model_name(e.model)[:20]
            print(f"  {i:>3}. {ts}  {model:<20} {format_tokens(e.input_tokens):>6}in "
                  f"{format_tokens(e.output_tokens):>6}out  {format_cost(e.cost or 0)}")
        print()

    # Trends
    if args.trends:
        trends = compute_trends(entries)
        if trends:
            print(f"  Trends ({trends['total_days']} days):")
            print(f"  {'─' * 40}")
            print(f"  Avg daily:        {format_cost(trends['avg_daily_cost'])}")
            print(f"  Recent 7d avg:    {format_cost(trends['recent_7d_avg'])}")
            print(f"  Projected monthly: {format_cost(trends['projected_monthly'])}")
            print(f"  Direction:        {trends['direction']}")
            print(f"  Peak day:         {trends['peak_day']} ({format_cost(trends['peak_day_cost'])})")
            print()

    # Optimization
    if args.optimize:
        suggestions = compute_optimization(entries)
        if suggestions:
            total_savings = sum(s["savings"] for s in suggestions)
            print(f"  Optimization Suggestions (potential savings: {format_cost(total_savings)}):")
            print(f"  {'─' * 56}")
            for s in suggestions[:10]:
                print(f"  {s['current_model']:<20} -> {s['alternative']:<20} "
                      f"saves {format_cost(s['savings'])} ({s['savings_pct']:.0f}%)")
            print()

    # Budget
    if args.budget:
        trends = compute_trends(entries)
        projected = trends.get("projected_monthly", 0) if trends else 0
        if projected > args.budget:
            print(f"  !! BUDGET WARNING: Projected ${projected:.2f}/mo exceeds ${args.budget:.2f} budget !!")
        else:
            print(f"  Budget OK: Projected ${projected:.2f}/mo within ${args.budget:.2f} budget")
        print()


def output_markdown(entries, args):
    """Output analysis as markdown."""
    total_cost = sum(e.cost or 0 for e in entries)
    total_input = sum(e.input_tokens for e in entries)
    total_output = sum(e.output_tokens for e in entries)

    print(f"# API Cost Report")
    print(f"\n**Period:** {entries[0].timestamp.strftime('%Y-%m-%d') if entries else 'N/A'} "
          f"to {entries[-1].timestamp.strftime('%Y-%m-%d') if entries else 'N/A'}")
    print(f"**Total Requests:** {len(entries)}")
    print(f"**Total Cost:** {format_cost(total_cost)}")
    print(f"**Total Tokens:** {format_tokens(total_input)} in / {format_tokens(total_output)} out\n")

    dimension = args.by or "model"
    groups = aggregate_by(entries, dimension)
    print(f"## Breakdown by {dimension.title()}\n")
    print(f"| {dimension.title()} | Requests | Input | Output | Cost |")
    print(f"|---|---:|---:|---:|---:|")
    for key, stats in groups.items():
        print(f"| {key} | {stats['count']} | {format_tokens(stats['input_tokens'])} | "
              f"{format_tokens(stats['output_tokens'])} | {format_cost(stats['cost'])} |")

    if args.trends:
        trends = compute_trends(entries)
        if trends:
            print(f"\n## Trends\n")
            print(f"- **Avg daily:** {format_cost(trends['avg_daily_cost'])}")
            print(f"- **Recent 7d:** {format_cost(trends['recent_7d_avg'])}")
            print(f"- **Projected monthly:** {format_cost(trends['projected_monthly'])}")
            print(f"- **Direction:** {trends['direction']}")

    if args.optimize:
        suggestions = compute_optimization(entries)
        if suggestions:
            total_savings = sum(s["savings"] for s in suggestions)
            print(f"\n## Optimization (potential savings: {format_cost(total_savings)})\n")
            print(f"| Current | Alternative | Savings | % |")
            print(f"|---|---|---:|---:|")
            for s in suggestions[:10]:
                print(f"| {s['current_model']} | {s['alternative']} | "
                      f"{format_cost(s['savings'])} | {s['savings_pct']:.0f}% |")


def output_json(entries, args):
    """Output analysis as JSON."""
    dimension = args.by or "model"
    result = {
        "summary": {
            "total_requests": len(entries),
            "total_cost": sum(e.cost or 0 for e in entries),
            "total_input_tokens": sum(e.input_tokens for e in entries),
            "total_output_tokens": sum(e.output_tokens for e in entries),
        },
        "breakdown": aggregate_by(entries, dimension),
    }
    if args.trends:
        result["trends"] = compute_trends(entries)
    if args.optimize:
        result["optimization"] = compute_optimization(entries)
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="API Cost Tracker — Analyze AI API spending")
    parser.add_argument("provider", choices=["openrouter", "openai", "anthropic", "auto", "generic"],
                        help="API provider or 'auto' to detect")
    parser.add_argument("--file", "-f", required=True, help="Usage data file (JSON or CSV)")
    parser.add_argument("--by", choices=["model", "day", "week", "hour", "total"], default="model",
                        help="Aggregation dimension (default: model)")
    parser.add_argument("--days", type=int, help="Only analyze last N days")
    parser.add_argument("--top", type=int, help="Show top N most expensive requests")
    parser.add_argument("--trends", action="store_true", help="Show spending trends")
    parser.add_argument("--optimize", action="store_true", help="Show optimization suggestions")
    parser.add_argument("--budget", type=float, help="Monthly budget threshold for alerts")
    parser.add_argument("--output", "-o", choices=["terminal", "markdown", "json", "csv"], default="terminal",
                        help="Output format (default: terminal)")
    parser.add_argument("--pricing", help="Custom pricing JSON file")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Load custom pricing
    if args.pricing:
        with open(args.pricing) as f:
            custom = json.load(f)
        MODEL_PRICING.update({k: tuple(v) for k, v in custom.items()})

    # Parse data
    entries = load_data(args.provider, args.file)
    if not entries:
        print("No usage entries found.", file=sys.stderr)
        sys.exit(1)

    # Sort by timestamp
    entries.sort(key=lambda e: e.timestamp)

    # Filter by time
    if args.days:
        entries = filter_entries(entries, days=args.days)

    if not entries:
        print("No entries match the specified filters.", file=sys.stderr)
        sys.exit(1)

    # Output
    output_funcs = {
        "terminal": output_terminal,
        "markdown": output_markdown,
        "json": output_json,
    }
    output_funcs.get(args.output, output_terminal)(entries, args)


if __name__ == "__main__":
    main()
