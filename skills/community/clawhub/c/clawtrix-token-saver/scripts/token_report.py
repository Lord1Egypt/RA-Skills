#!/usr/bin/env python3
"""
token_report.py — ClawBrain Token Saver cost report generator.

Fetches usage data from the Anthropic API and generates a cost breakdown
report. Requires ANTHROPIC_API_KEY in environment.

Usage:
    python3 token_report.py [--days N] [--format text|json]
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("ERROR: Python stdlib not available", file=sys.stderr)
    sys.exit(1)

# Pricing per 1M tokens (March 2026)
PRICING = {
    "claude-opus-4-6": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
    "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.00},
}

DEFAULT_PRICING = {"input": 3.00, "output": 15.00}  # Sonnet as fallback


def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    return key


def fetch_usage(api_key, days=7):
    """Fetch usage stats from Anthropic API."""
    url = f"https://api.anthropic.com/v1/usage?days={days}"
    req = urllib.request.Request(
        url,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"WARNING: Anthropic usage API returned {e.code}: {body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARNING: Could not reach Anthropic usage API: {e}", file=sys.stderr)
        return None


def calc_cost(tokens_in, tokens_out, model):
    pricing = PRICING.get(model, DEFAULT_PRICING)
    cost_in = (tokens_in / 1_000_000) * pricing["input"]
    cost_out = (tokens_out / 1_000_000) * pricing["output"]
    return cost_in + cost_out


def estimate_from_env(days):
    """
    Generate a rough estimate when the API is unavailable.
    Based on typical OpenClaw agent usage patterns.
    """
    heartbeats_per_day = 48  # every 30 min
    haiku_tokens_per_heartbeat = 200
    sonnet_tokens_per_turn = 1500
    daily_turns = 20

    heartbeat_tokens = heartbeats_per_day * days * haiku_tokens_per_heartbeat
    daily_tokens = daily_turns * days * sonnet_tokens_per_turn

    return {
        "estimated": True,
        "days": days,
        "models": {
            "claude-haiku-4-5": {
                "input_tokens": heartbeat_tokens // 2,
                "output_tokens": heartbeat_tokens // 2,
                "requests": heartbeats_per_day * days,
            },
            "claude-sonnet-4-6": {
                "input_tokens": daily_tokens // 2,
                "output_tokens": daily_tokens // 2,
                "requests": daily_turns * days,
            },
        },
    }


def format_text_report(data, days):
    lines = []
    sep = "─" * 45
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    estimated = data.get("estimated", False)

    lines.append(sep)
    lines.append(f"TOKEN SAVER COST REPORT — {now}")
    if estimated:
        lines.append("(ESTIMATED — Anthropic usage API unavailable)")
    lines.append(f"Period: last {days} days")
    lines.append(sep)
    lines.append("")

    total_cost = 0.0
    total_requests = 0
    model_rows = []

    models = data.get("models") or data.get("usage", {})
    if not models and "data" in data:
        # Reshape if API returns list format
        for entry in data["data"]:
            model = entry.get("model", "unknown")
            if model not in models:
                models[model] = {"input_tokens": 0, "output_tokens": 0, "requests": 0}
            models[model]["input_tokens"] += entry.get("input_tokens", 0)
            models[model]["output_tokens"] += entry.get("output_tokens", 0)
            models[model]["requests"] += entry.get("request_count", 1)

    for model, stats in sorted(models.items()):
        t_in = stats.get("input_tokens", 0)
        t_out = stats.get("output_tokens", 0)
        reqs = stats.get("requests", stats.get("request_count", 0))
        cost = calc_cost(t_in, t_out, model)
        total_cost += cost
        total_requests += reqs
        model_rows.append((model, t_in, t_out, reqs, cost))

    lines.append("MODEL BREAKDOWN:")
    lines.append("")
    for model, t_in, t_out, reqs, cost in model_rows:
        lines.append(f"  {model}")
        lines.append(f"    Requests: {reqs:,}")
        lines.append(f"    Input:    {t_in:,} tokens")
        lines.append(f"    Output:   {t_out:,} tokens")
        lines.append(f"    Cost:     ${cost:.4f}")
        lines.append("")

    lines.append(sep)
    lines.append(f"TOTAL COST ({days}d):  ${total_cost:.4f}")
    lines.append(f"TOTAL REQUESTS:    {total_requests:,}")
    projected_monthly = (total_cost / days) * 30
    lines.append(f"PROJECTED MONTHLY: ${projected_monthly:.2f}")
    lines.append(sep)
    lines.append("")

    # Waste flags
    lines.append("WASTE FLAGS:")
    lines.append("")
    flags = []

    for model, t_in, t_out, reqs, cost in model_rows:
        if "opus" in model and reqs > 0:
            flags.append(f"  🔴 Opus usage detected ({reqs} requests) — verify complex tasks only")
        if "sonnet" in model and reqs > 100:
            flags.append(
                f"  🟡 High Sonnet volume ({reqs} req/{days}d) — check if heartbeats use Haiku"
            )

    if not flags:
        flags.append("  ✅ No obvious waste patterns detected")

    lines.extend(flags)
    lines.append("")
    lines.append("Run 'token-saver diagnose' in your agent for a full playbook analysis.")
    lines.append(sep)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Token Saver cost report generator")
    parser.add_argument("--days", type=int, default=7, help="Days of history to fetch (default: 7)")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format (default: text)"
    )
    args = parser.parse_args()

    api_key = get_api_key()
    data = fetch_usage(api_key, args.days)

    if data is None:
        data = estimate_from_env(args.days)

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print(format_text_report(data, args.days))


if __name__ == "__main__":
    main()
