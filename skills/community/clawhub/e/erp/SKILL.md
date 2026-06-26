---
name: erp
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [erp, tool, utility]
description: "Plan resources, track inventory, and coordinate departments with reporting. Use when allocating resources, managing stock, or tracking department KPIs."
---

# ERP

Enterprise resource planning productivity toolkit (v2.0.0). Log and track business activities across multiple categories — planning, tracking, reviews, reminders, priorities, archiving, tagging, timelines, reports, and weekly reviews. Each command records timestamped entries to its own log file, giving you a complete audit trail of all business operations.

## Commands

| Command | Description |
|---------|-------------|
| `erp add <input>` | Add a new entry to the general log. Without args, shows recent entries. |
| `erp plan <input>` | Record a planning note (resource allocation, project plan, etc.). Without args, shows recent plan entries. |
| `erp track <input>` | Track an activity, metric, or progress item. Without args, shows recent tracked entries. |
| `erp review <input>` | Log a review note (performance review, process review, etc.). Without args, shows recent reviews. |
| `erp streak <input>` | Record a streak milestone or daily streak entry. Without args, shows recent streaks. |
| `erp remind <input>` | Set a reminder or note something to follow up on. Without args, shows recent reminders. |
| `erp prioritize <input>` | Log a prioritization decision or rank items. Without args, shows recent priorities. |
| `erp archive <input>` | Archive a completed item or record. Without args, shows recent archived entries. |
| `erp tag <input>` | Tag or categorize an entry. Without args, shows recent tags. |
| `erp timeline <input>` | Add an event to the timeline. Without args, shows recent timeline entries. |
| `erp report <input>` | Log a report or summary. Without args, shows recent reports. |
| `erp weekly-review <input>` | Record a weekly review summary. Without args, shows recent weekly reviews. |
| `erp stats` | Show summary statistics: entry counts per category, total entries, data size, and earliest record date. |
| `erp export <fmt>` | Export all data to a file. Supported formats: `json`, `csv`, `txt`. |
| `erp search <term>` | Search across all log files for a keyword (case-insensitive). |
| `erp recent` | Show the 20 most recent entries from the activity history log. |
| `erp status` | Health check: version, data directory, total entries, disk usage, last activity. |
| `erp help` | Show the built-in help with all available commands. |
| `erp version` | Print the current version (v2.0.0). |

## Data Storage

All data is stored as plain-text log files in `~/.local/share/erp/`:

- **Per-command logs** — Each command (add, plan, track, etc.) writes to its own `.log` file (e.g., `add.log`, `plan.log`).
- **History log** — Every operation is also appended to `history.log` with a timestamp and command name.
- **Export files** — Generated in the same directory as `export.json`, `export.csv`, or `export.txt`.

Entries are stored in `timestamp|value` format, making them easy to grep, parse, or pipe into other tools.

## Requirements

- **Bash** 4.0+ (uses `set -euo pipefail`)
- **coreutils** — `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cut`
- No external dependencies, API keys, or network access required
- Works fully offline on any POSIX-compatible system

## When to Use

1. **Daily operational logging** — Track what happened across departments each day: sales calls, support tickets resolved, inventory received, tasks completed.
2. **Resource planning and prioritization** — Use `plan` and `prioritize` to record allocation decisions and rank items by importance before committing resources.
3. **Weekly business reviews** — Run `weekly-review` to summarize the week, then `stats` to see aggregate numbers and `export json` to share with stakeholders.
4. **Reminder and follow-up management** — Use `remind` to note items that need attention later, and `search` to quickly find past reminders by keyword.
5. **Audit trail and compliance** — Every action is timestamped and logged to `history.log`, providing a complete chronological record of all ERP activities for auditing purposes.

## Examples

```bash
# Add a new inventory item
erp add "Received 500 units of Widget-A from Supplier-X"

# Plan resource allocation for Q2
erp plan "Allocate 3 engineers to Project Alpha for Q2"

# Track a KPI
erp track "Customer satisfaction score: 4.7/5.0"

# Set a priority
erp prioritize "Ship feature-X before feature-Y — customer deadline March 30"

# Record a weekly review
erp weekly-review "Week 12: shipped 3 features, resolved 15 tickets, revenue +8%"

# Search for anything mentioning 'Widget'
erp search Widget

# Export everything to JSON for reporting
erp export json

# Check system health
erp status

# View summary statistics
erp stats
```

## Tips

- Run any data command without arguments to see recent entries (e.g., `erp add` shows the last 20 add entries).
- Use `erp recent` for a quick overview of all activity across all categories.
- Pipe exports to other tools: `cat ~/.local/share/erp/export.csv | column -t -s,`
- Back up your data by copying `~/.local/share/erp/` to your preferred backup location.

---
*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
