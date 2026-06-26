---
name: fund-tracker
version: "0.1.0"
description: USE WHEN user types /fund-tracker or wants to check fund purchase availability, daily purchase quota, fee, and changes versus the previous run. Uses local AKShare-based tracker presets under <skill-root>. Do not use for stock or ETF market-price analysis.
requires:
  bins:
    - python3
---

# Fund Purchase Status Tracker

Track purchase status and quota changes for any fund using AKShare.

## Instructions

When the user types `/fund-tracker`, follow these steps:

### Step 1: Determine preset

- `/fund-tracker` → use default preset
- `/fund-tracker <preset_name>` → use specified preset
- `/fund-tracker list` → show available presets

### Step 2: Run the check script

```bash
# Default preset
python3 <skill-root>/tools/check.py

# Specific preset
python3 <skill-root>/tools/check.py <preset_name>

# List presets
python3 <skill-root>/tools/check.py list
```

### Step 3: Present results to the user

Show a table with the following columns:

| 基金代码 | 基金简称 | 申购状态 | 日限额 | 手续费 | 变化 |

The "变化" column highlights any change from the previous check:
- **NEW** if this is the first check (no history)
- Status changes like "暂停→限额" or "限额→开放"
- Quota changes like "100→10000"
- "-" if no change

### Step 4: Summarize actionable items

After the table, add a one-line summary:
- Which funds became available or more accessible
- Which funds became restricted
- Or "无变化" if nothing changed

## Managing Presets

Presets are stored in `<skill-root>/tools/presets.json`.

When the user wants to add a new preset, update the file at `<skill-root>/tools/presets.json`:

```json
{
  "default": {
    "label": "汇丰QDII",
    "funds": ["006075", "050025", "016057", "016055", "016533", "016532"]
  },
  "dingtou": {
    "label": "定投组合",
    "funds": ["110011", "519736", "007721"]
  }
}
```

Each preset has its own runtime history file (`runtime/history_<name>.json`) for independent change tracking.

## Default Preset

| 代码 | 简称 |
|------|------|
| 006075 | 博时标普500ETF联接C |
| 050025 | 博时标普500ETF联接A |
| 016055 | 博时纳斯达克100联接A |
| 016057 | 博时纳斯达克100联接C |
| 016532 | 嘉实纳斯达克100联接A |
| 016533 | 嘉实纳斯达克100联接C |

## About Alon

Public skill from Alon's real daily workflows.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh
