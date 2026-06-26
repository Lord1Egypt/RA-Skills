# Cost Monitor - Detailed Guide

## Overview

Cost Monitor is an OpenClaw skill that provides real-time token usage and cost tracking. It automatically appends a one-line cost summary after every assistant reply, giving users immediate visibility into their API consumption.

## Architecture

```
User Message → Agent Reply → cost.py → Transcript → Balance Update
                                    ↓
                              Display appended to reply
```

The skill reads usage data directly from the session transcript (which contains API response metadata), calculates costs using configured pricing, and updates the balance file.

## How It Works

### Per-Turn Flow

1. Agent generates reply (API returns usage data)
2. Usage data is written to session transcript
3. `cost.py` reads the last assistant message from transcript
4. Calculates cost based on model and pricing
5. Deducts from balance in `balance.json`
6. Returns formatted string for display

### Data Sources

- **Transcript**: Contains `input`, `output`, `cacheRead` tokens per turn
- **pricing.json**: Official pricing from provider websites
- **balance.json**: User-managed balance tracking

## Configuration

### pricing.json

Stores official pricing data. Update when providers change rates.

```json
{
  "_source": "https://platform.xiaomimimo.com/docs/zh-CN/price/",
  "_updated": "2026-06-07",
  "plans": {
    "mimo": {
      "standard": {
        "monthly_rmb": 99,
        "credits": 11000000000,
        "discount_first": 0.88,
        "nighttime_coefficient": 0.8
      }
    }
  },
  "credits_per_token": {
    "mimo-v2.5": {"input": 100, "cache": 2, "output": 200}
  },
  "rmb_per_million_tokens": {
    "deepseek-v4-flash": {"input": 1.00, "cache": 0.02, "output": 2.00}
  }
}
```

### balance.json

Tracks current balance. Updated automatically by cost.py.

```json
{
  "deepseek": {
    "balance_rmb": 18.00
  },
  "mimo": {
    "plan": "standard",
    "total_credits": 11000000000,
    "consumed_credits": 4250108284,
    "discount_applied": 0.88
  }
}
```

## Scripts

### cost.py

Core calculation engine. Called after every reply.

```bash
# Basic usage
python3 cost.py <transcript.jsonl> <model>

# With balance reset
python3 cost.py <transcript.jsonl> <model> --set-balance <amount>
```

### calibrate.py

Balance calibration tool. Syncs with provider backends.

```bash
# MiMo (manual input from backend)
python3 calibrate.py mimo <transcript.jsonl> <consumed> <total>

# DeepSeek (automatic API query)
python3 calibrate.py deepseek <transcript.jsonl> [api_key]
```

### set-balance.sh

Quick balance setter for common operations.

```bash
# Set MiMo balance
set-balance mimo 4,250,108,284 / 11,000,000,000

# Set DeepSeek balance
set-balance deepseek 18.00
```

## Nighttime Discount

MiMo Token Plan includes a 0.8× coefficient during off-peak hours:
- **Time**: Beijing Time 00:00-08:00
- **Effect**: Credits consumed are 80% of normal rate
- **Automatic**: No user action needed

## Troubleshooting

### Balance not updating

1. Check `balance.json` exists in skill directory
2. Run calibration to sync with backend
3. Verify file permissions (should be writable by OpenClaw)

### Wrong pricing

1. Check `pricing.json` for correct rates
2. Verify `_source` URL is current
3. Update manually if provider changed rates

### Display not appearing

1. Verify skill is installed: `clawhub list`
2. Check AGENTS.md or SOUL.md has cost monitoring rule
3. Restart gateway after installation

### Cache hit rate anomalies

- After model switch: cache rebuilds over several turns
- After gateway restart: cache is cleared
- After compaction: cache is rebuilt from summary

## FAQ

**Q: Does this add extra API calls?**
A: No. It reads from existing transcript data and runs a local Python script.

**Q: Can I disable it?**
A: Remove the cost monitoring rule from AGENTS.md/SOUL.md.

**Q: Does it work with all models?**
A: Currently supports MiMo and DeepSeek. Add new models to pricing.json.

**Q: What about currency conversion?**
A: MiMo uses Credits (converted to RMB via plan pricing). DeepSeek uses direct RMB.
