---
name: api-cost-tracker
description: Track, analyze, and optimize AI API costs across OpenAI, Anthropic, OpenRouter, Google, and other LLM providers. Parses billing data, usage logs, or API responses to produce cost breakdowns by model, feature, and time period. Identifies optimization opportunities (model downgrades, caching, prompt compression). Use when asked to analyze API costs, track AI spending, optimize LLM usage, create cost reports, find expensive API calls, compare model pricing, set budget alerts, or audit API usage. Triggers on "API costs", "how much am I spending", "optimize API usage", "cost breakdown", "LLM spending", "token usage", "billing analysis", "reduce API costs", "budget tracking".
---

# API Cost Tracker

Analyze and optimize AI API costs across multiple providers with detailed breakdowns, trend detection, and actionable savings recommendations.

## Quick Start

```bash
# Analyze OpenRouter usage (from activity page export)
python3 scripts/api_cost_tracker.py openrouter --file activity.json

# Analyze OpenAI usage (from billing export)
python3 scripts/api_cost_tracker.py openai --file usage.json

# Analyze from environment (auto-detect provider from API keys)
python3 scripts/api_cost_tracker.py auto --days 30

# Cost breakdown by model
python3 scripts/api_cost_tracker.py openrouter --file activity.json --by model

# Cost breakdown by day with trend analysis
python3 scripts/api_cost_tracker.py openrouter --file activity.json --by day --trends

# Find most expensive requests
python3 scripts/api_cost_tracker.py openrouter --file activity.json --top 20

# Compare current vs optimized (model substitution analysis)
python3 scripts/api_cost_tracker.py openrouter --file activity.json --optimize

# Set budget alert threshold
python3 scripts/api_cost_tracker.py openrouter --file activity.json --budget 50.00

# Output as markdown report
python3 scripts/api_cost_tracker.py openrouter --file activity.json --output markdown

# Output as JSON
python3 scripts/api_cost_tracker.py openrouter --file activity.json --output json
```

## Supported Providers

| Provider | Input Format | Auto-detect |
|----------|-------------|-------------|
| OpenAI | Billing CSV/JSON export, API responses | OPENAI_API_KEY |
| Anthropic | Usage API, console export | ANTHROPIC_API_KEY |
| OpenRouter | Activity JSON, API responses | OPENROUTER_API_KEY |
| Google AI | Billing export | GOOGLE_AI_API_KEY |
| Generic | CSV with columns: timestamp, model, tokens_in, tokens_out, cost | N/A |

## Analysis Features

1. **Cost Breakdown** — by model, day, week, feature/tag, request type
2. **Trend Detection** — spending velocity, anomaly detection, projected monthly cost
3. **Optimization Report** — model substitution suggestions, caching opportunities, prompt compression candidates
4. **Budget Alerts** — daily/weekly/monthly thresholds with projected overrun warnings
5. **Top Spenders** — most expensive individual requests or sessions
6. **Model Comparison** — cost-per-quality analysis using common benchmarks

## Output Formats

- **Terminal** (default) — colored tables and charts
- **Markdown** — report suitable for documentation
- **JSON** — structured data for programmatic use
- **CSV** — spreadsheet-compatible export

## How It Works

The script:
1. Reads usage data from the specified source (file, API, or environment)
2. Normalizes all entries to a common format (timestamp, model, input_tokens, output_tokens, cost)
3. Applies current provider pricing to calculate/verify costs
4. Groups and aggregates by the requested dimension
5. Runs optimization analysis comparing current models to cheaper alternatives
6. Generates the report in the requested format

## Pricing Database

Built-in pricing for 50+ models (updated March 2026). Override with `--pricing custom_prices.json`.

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
