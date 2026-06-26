---
name: automation-dedup-guard
description: "WorkBuddy 自动化任务去重守护。当用户的自动化任务出现重复时自动检测并清理。触发场景：自动化任务重复、任务列表膨胀、需要清理重复任务。支持 Windows/macOS/Linux，纯 Python 标准库，零依赖。"
---

# Automation Dedup Guard

## Overview

WorkBuddy 的自动化任务系统没有防重机制，每次新会话创建同名任务时不会检查是否已存在，导致同名任务不断累积。本 Skill 提供一个一键去重脚本，自动检测并清理重复的自动化任务，每组同名任务只保留最新创建的版本。

## When to Use

- 用户反馈自动化任务"重复出现"、"越来越多"、"一堆重复的"
- 需要检查或清理 WorkBuddy 自动化数据库中的冗余任务
- 想要配置定期自动去重守护

## Core Script

`scripts/automation_dedup_guard.py` is the main executable.

### Usage

```bash
# Safe preview (dry-run, no deletions)
python scripts/automation_dedup_guard.py --dry-run

# Execute cleanup
python scripts/automation_dedup_guard.py

# Specify custom database path
python scripts/automation_dedup_guard.py --db /custom/path/automations.db

# Verbose mode for debugging
python scripts/automation_dedup_guard.py --dry-run -v
```

### Exit Codes

- `0` — No duplicates found, all clean
- `1` — Duplicates detected (after cleanup, still returns 1 if any were found)

### Database Auto-Detection

The script automatically locates the WorkBuddy automations database:

| Priority | Source | Notes |
|----------|--------|-------|
| 1 | `--db` CLI argument | Manual override |
| 2 | `WORKBUDDY_DB_PATH` env var | For advanced users |
| 3 | OS default path | Auto-detected |

Default paths by OS:
- **Windows**: `%APPDATA%\WorkBuddy\automations\automations.db`
- **macOS**: `~/Library/Application Support/WorkBuddy/automations\automations.db`
- **Linux**: `~/.config/WorkBuddy\automations\automations.db`

### Dedup Strategy

1. **Group by name**: Tasks with the same `name` field are considered duplicates
2. **Keep newest**: Within each group, the task with the latest `created_at` is preserved
3. **Cascade delete**: Associated `automation_runs` records are also cleaned up
4. **No backup**: Deletions are permanent (back up the DB file manually if needed)

## Setup as Recurring Automation

To run automatically, register it as a WorkBuddy automation:

- **Name**: Automation Dedup Guard
- **Schedule**: Weekly (e.g., `FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=55`)
- **Prompt**:
  ```
  Run the dedup guard script: python [path-to]/scripts/automation_dedup_guard.py
  If output contains "[OK]" — no action needed.
  If output contains "[!]" — duplicates were auto-cleaned, confirm the count.
  If script errors — log the error, no other action.
  ```

## Requirements

- Python 3.6+
- No third-party dependencies (stdlib only: `sqlite3`, `sys`, `os`, `datetime`, `collections`)
