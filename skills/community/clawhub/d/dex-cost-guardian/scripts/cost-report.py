#!/usr/bin/env python3
"""
Cost Guardian — OpenClaw Usage & Cost Report
Reads session data and calculates estimated API costs.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Model pricing (per 1M tokens) — updated March 2026
MODEL_PRICING = {
    # Anthropic
    "claude-opus-4-6":           {"input": 15.00, "output": 75.00, "cached_input": 1.875},
    "claude-opus-4-20250514":    {"input": 15.00, "output": 75.00, "cached_input": 1.875},
    "claude-sonnet-4-20250514":  {"input": 3.00,  "output": 15.00, "cached_input": 0.30},
    "claude-sonnet-4":           {"input": 3.00,  "output": 15.00, "cached_input": 0.30},
    "claude-haiku-3.5":          {"input": 0.80,  "output": 4.00,  "cached_input": 0.08},
    # OpenRouter (estimate — varies by routed model)
    "openrouter/auto":           {"input": 3.00,  "output": 15.00, "cached_input": 0.30},
    # OpenAI
    "gpt-4o":                    {"input": 2.50,  "output": 10.00, "cached_input": 1.25},
    "gpt-4o-mini":               {"input": 0.15,  "output": 0.60,  "cached_input": 0.075},
    "gpt-4.1":                   {"input": 2.00,  "output": 8.00,  "cached_input": 0.50},
    "gpt-4.1-mini":              {"input": 0.40,  "output": 1.60,  "cached_input": 0.10},
    "gpt-4.1-nano":              {"input": 0.10,  "output": 0.40,  "cached_input": 0.025},
    # Fallback
    "unknown":                   {"input": 3.00,  "output": 15.00, "cached_input": 0.30},
}

def get_pricing(model):
    """Get pricing for a model, with fallback."""
    if model in MODEL_PRICING:
        return MODEL_PRICING[model]
    # Try partial match
    for key in MODEL_PRICING:
        if key in model or model in key:
            return MODEL_PRICING[key]
    return MODEL_PRICING["unknown"]

def calculate_cost(input_tokens, output_tokens, model, cached_tokens=0):
    """Calculate estimated cost for a session."""
    pricing = get_pricing(model)
    fresh_input = max(0, input_tokens - cached_tokens)
    input_cost = (fresh_input / 1_000_000) * pricing["input"]
    cached_cost = (cached_tokens / 1_000_000) * pricing["cached_input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + cached_cost + output_cost

def load_sessions(agent_id="main"):
    """Load session data from OpenClaw's session store."""
    home = Path.home()
    sessions_file = home / ".openclaw" / "agents" / agent_id / "sessions" / "sessions.json"
    
    if not sessions_file.exists():
        print(f"Error: Session file not found at {sessions_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(sessions_file) as f:
        return json.load(f)

def format_cost(cost):
    """Format cost with appropriate precision."""
    if cost < 0.01:
        return f"${cost:.4f}"
    elif cost < 1.00:
        return f"${cost:.3f}"
    else:
        return f"${cost:.2f}"

def generate_report(sessions, budget=None, period_hours=None):
    """Generate a cost report from session data."""
    now_ms = int(datetime.now().timestamp() * 1000)
    cutoff_ms = now_ms - (period_hours * 3600 * 1000) if period_hours else 0
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "period": f"Last {period_hours}h" if period_hours else "All time",
        "budget": budget,
        "models": {},
        "sessions": [],
        "total_cost": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_context_tokens": 0,
        "session_count": 0,
        "alerts": [],
        "recommendations": [],
    }
    
    for key, session in sessions.items():
        updated_at = session.get("updatedAt", 0)
        if period_hours and updated_at < cutoff_ms:
            continue
        
        input_tokens = session.get("inputTokens", 0)
        output_tokens = session.get("outputTokens", 0)
        total_tokens = session.get("totalTokens", 0)
        model = session.get("model", "unknown")
        
        if total_tokens == 0:
            continue
        
        # Estimate cached vs fresh (OpenClaw doesn't break this out in sessions.json,
        # but context tokens minus fresh input gives us an approximation)
        estimated_cached = max(0, total_tokens - input_tokens - output_tokens)
        cost = calculate_cost(input_tokens, output_tokens, model, estimated_cached)
        
        report["total_cost"] += cost
        report["total_input_tokens"] += input_tokens
        report["total_output_tokens"] += output_tokens
        report["total_context_tokens"] += total_tokens
        report["session_count"] += 1
        
        # Track by model
        if model not in report["models"]:
            report["models"][model] = {"tokens": 0, "cost": 0, "sessions": 0, "input": 0, "output": 0}
        report["models"][model]["tokens"] += total_tokens
        report["models"][model]["cost"] += cost
        report["models"][model]["sessions"] += 1
        report["models"][model]["input"] += input_tokens
        report["models"][model]["output"] += output_tokens
        
        # Track individual sessions (top spenders)
        label = session.get("label", key)
        report["sessions"].append({
            "key": key,
            "label": label,
            "model": model,
            "tokens": total_tokens,
            "input": input_tokens,
            "output": output_tokens,
            "cost": cost,
            "updated": datetime.fromtimestamp(updated_at / 1000).isoformat() if updated_at else "unknown",
        })
    
    # Sort sessions by cost descending
    report["sessions"].sort(key=lambda x: x["cost"], reverse=True)
    
    # Generate alerts
    if budget and report["total_cost"] > budget:
        report["alerts"].append(f"🔴 OVER BUDGET: {format_cost(report['total_cost'])} spent vs {format_cost(budget)} budget ({report['total_cost']/budget*100:.0f}%)")
    elif budget and report["total_cost"] > budget * 0.8:
        report["alerts"].append(f"🟡 WARNING: {format_cost(report['total_cost'])} spent — {report['total_cost']/budget*100:.0f}% of {format_cost(budget)} budget")
    
    # Generate recommendations
    if report["models"].get("claude-opus-4-6", {}).get("sessions", 0) > 0:
        opus_data = report["models"]["claude-opus-4-6"]
        opus_pct = opus_data["cost"] / max(report["total_cost"], 0.001) * 100
        if opus_pct > 50:
            sonnet_equiv_cost = calculate_cost(opus_data["input"], opus_data["output"], "claude-sonnet-4-20250514")
            savings = opus_data["cost"] - sonnet_equiv_cost
            report["recommendations"].append(
                f"💡 Opus is {opus_pct:.0f}% of your spend. Switching routine tasks (crons, email checks, heartbeats) to Sonnet would save ~{format_cost(savings)}"
            )
    
    # Check for cron sessions burning tokens
    cron_cost = sum(s["cost"] for s in report["sessions"] if "cron:" in s["key"])
    if cron_cost > report["total_cost"] * 0.3:
        report["recommendations"].append(
            f"💡 Cron jobs account for {format_cost(cron_cost)} ({cron_cost/max(report['total_cost'],0.001)*100:.0f}% of total). Consider using cheaper models for automated tasks."
        )
    
    return report

def print_report(report, format="text"):
    """Print the report in the requested format."""
    if format == "json":
        print(json.dumps(report, indent=2))
        return
    
    print(f"\n{'='*60}")
    print(f"  🛡️  COST GUARDIAN — Usage Report")
    print(f"  📅  {report['period']} | Generated {report['generated_at'][:19]}")
    print(f"{'='*60}\n")
    
    # Alerts first
    for alert in report["alerts"]:
        print(f"  {alert}\n")
    
    # Summary
    print(f"  💰 Estimated Cost:  {format_cost(report['total_cost'])}")
    if report["budget"]:
        remaining = report["budget"] - report["total_cost"]
        print(f"  📊 Budget:          {format_cost(report['budget'])} ({format_cost(remaining)} remaining)")
    print(f"  📝 Active Sessions: {report['session_count']}")
    print(f"  📥 Input Tokens:    {report['total_input_tokens']:,}")
    print(f"  📤 Output Tokens:   {report['total_output_tokens']:,}")
    print(f"  📦 Context Tokens:  {report['total_context_tokens']:,}")
    print()
    
    # By model
    print(f"  {'Model':<30s} {'Sessions':>8s} {'Tokens':>12s} {'Cost':>10s}")
    print(f"  {'-'*30} {'-'*8} {'-'*12} {'-'*10}")
    for model, data in sorted(report["models"].items(), key=lambda x: -x[1]["cost"]):
        print(f"  {model:<30s} {data['sessions']:>8d} {data['tokens']:>12,} {format_cost(data['cost']):>10s}")
    print()
    
    # Top 10 sessions by cost
    print(f"  Top Sessions by Cost:")
    print(f"  {'-'*55}")
    for s in report["sessions"][:10]:
        label = s["label"][:45] if len(s["label"]) > 45 else s["label"]
        print(f"  {format_cost(s['cost']):>8s}  {s['model']:<25s}  {label}")
    print()
    
    # Recommendations
    if report["recommendations"]:
        print(f"  Recommendations:")
        for rec in report["recommendations"]:
            print(f"  {rec}")
        print()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Cost Guardian — OpenClaw Usage & Cost Report")
    parser.add_argument("--budget", type=float, help="Daily budget in USD (triggers alerts)")
    parser.add_argument("--hours", type=int, default=24, help="Report period in hours (default: 24)")
    parser.add_argument("--all", action="store_true", help="Report on all time, not just recent")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--agent", default="main", help="Agent ID (default: main)")
    args = parser.parse_args()
    
    sessions = load_sessions(args.agent)
    period = None if args.all else (args.hours if args.hours > 0 else 1)
    report = generate_report(sessions, budget=args.budget, period_hours=period)
    print_report(report, format="json" if args.json else "text")

if __name__ == "__main__":
    main()
