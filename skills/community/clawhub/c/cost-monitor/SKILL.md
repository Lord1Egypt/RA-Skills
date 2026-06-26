---
name: cost-monitor
slug: cost-monitor
version: 1.0.0
description: "Real-time token usage and cost tracking for OpenClaw agents. Supports MiMo Token Plan (Credits) and DeepSeek pay-as-you-go (RMB). Shows per-turn consumption and remaining balance after every reply."
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"],"configPaths":["~/.openclaw/skills/cost-monitor/"]}}
---

## When to Use

This skill activates automatically on **every assistant reply**. No user trigger needed.

- After each API response, calculate token consumption and cost
- Append a one-line summary to the reply showing balance and usage
- Support both MiMo (Token Plan Credits) and DeepSeek (RMB) billing models

## Quick Start

**Install:**
```bash
clawhub install cost-monitor
```

**Zero configuration.** Works out of the box with default settings.

**First-time setup (optional):**
```bash
# Set your MiMo balance (copy from backend: consumed / total)
set-balance mimo 4,250,108,284 / 11,000,000,000

# Set your DeepSeek balance (RMB)
set-balance deepseek 18.00
```

## Display Format

**MiMo (Token Plan):**
```
MiMo：61.4% | 603.5k · in 333+264.9kcached(99%) · out 202
```

**DeepSeek (Pay-as-you-go):**
```
DeepSeek：¥18.00 | ¥0.0045 · in 111+198.0kcached(99%) · out 192
```

## What Each Field Means

| Field | Description |
|-------|-------------|
| `61.4%` / `¥18.00` | Remaining balance (percentage for MiMo, RMB for DeepSeek) |
| `603.5k` / `¥0.0045` | Cost of this turn (Credits or RMB) |
| `in X+Ycached(Z%)` | New input tokens + cached tokens (cache hit rate) |
| `out X` | Output tokens generated |

## Supported Models

| Model | Billing | Auto-detected |
|-------|---------|:---:|
| `xiaomi/mimo-v2.5` | Token Plan Credits | ✅ |
| `xiaomi/mimo-v2.5-pro` | Token Plan Credits | ✅ |
| `deepseek/deepseek-v4-flash` | RMB (pay-as-you-go) | ✅ |
| `deepseek/deepseek-v4-pro` | RMB (pay-as-you-go) | ✅ |
| `moonshot/kimi-k2.6` | RMB (pay-as-you-go) | ✅ |

## Calibration

**MiMo:** Copy `consumed / total` from the backend:
```
校准 mimo 4,250,108,284 / 11,000,000,000
```

**DeepSeek:** Automatic via API:
```
校准 deepseek
```

Both automatically deduct the current turn's consumption.

## File Structure

```
cost-monitor/
├── SKILL.md              # This file
├── pricing.json          # Official pricing (auto-updated)
├── balance.json          # Balance tracking (auto-updated)
├── scripts/
│   ├── cost.py           # Core calculation engine
│   ├── calibrate.py      # Balance calibration
│   └── set-balance.sh    # Quick balance setter
└── references/
    └── detailed-guide.md # Full documentation
```

## Nighttime Discount

MiMo Token Plan includes a 0.8× coefficient during off-peak hours (Beijing Time 00:00-08:00). This is automatically applied.

## Troubleshooting

**Balance not updating?**
- Ensure `balance.json` exists in the skill directory
- Run calibration to sync with backend

**Wrong model pricing?**
- Update `pricing.json` with official rates from provider websites
- The `_source` field in pricing.json tracks the data origin

**Display not appearing?**
- Check that the skill is installed: `clawhub list`
- Verify AGENTS.md or SOUL.md contains the cost monitoring rule
