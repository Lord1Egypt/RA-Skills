# cron-task

[![Stars](https://img.shields.io/github/stars/EdwardWason/cron-task?style=flat-square)](https://github.com/EdwardWason/cron-task)
[![License](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-cron--task-orange?style=flat-square)](https://clawhub.ai/skills/cron-task)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)

🇨🇳 中文版: [README.md](README.md)

> _「Debug done. Say one word, get a daily runner with 9-point readiness check, three-destination archiving, and Feishu IM notification.」_

**cron-task** is not a general-purpose task orchestrator, is a focused workflow that converts a debugged task into a stable scheduled task with readiness validation, script generation, and multi-destination archiving.

## Navigation

[See Effect](#example) · [Quick Start](#quick-start) · [Core Features](#core-features) · [Known Limitations](#known-limitations) · [License](#license)

## Quick Start

```bash
# Install via ClawHub
clawhub install cron-task

# Or clone from GitHub
git clone https://github.com/EdwardWason/cron-task.git
```

After installation, trigger with: **"创建定时任务"** or **"定时任务创建"**

## Core Features

- **9-Point Readiness Check** — Script independence, env vars, data source reachability, IM credentials, archive paths, idempotency, fallback chain, schedule frequency, output quality
- **Executor Script Generation** — Auto-generates a standalone Python script with env checking, main logic, three-destination archiving, and IM notification
- **Schedule Prompt Writing** — Writes self-contained Schedule messages with execution commands, failure fallback, and archiving instructions
- **Three-Destination Archiving** — Feishu Cloud Drive + Obsidian Inbox + IMA Knowledge Base, unified Markdown + YAML metadata header
- **Feishu IM Notification** — Sends Interactive Card via lark-im skill with task name, status, summary, and detail link

## Suitable / Not Suitable

### Suitable
- Converting a debugged data pipeline to daily auto-run
- Setting up periodic skill execution with result archiving
- Creating scheduled workflows with multi-step fallback

### Not Suitable
- One-time script execution
- Manual-triggered tasks
- Non-periodic workflows
- Cron failure diagnosis (use cron-doctor instead)

## Example

```
User: 创建定时任务

AI: [Scans context...]
    [Runs 9-point readiness check...]

## Readiness Check Report
| # | Check Item | Status | Notes |
|---|-----------|--------|-------|
| 1 | Script independence | ✅ | executor.py tested |
| ... | ... | ... | ... |
| 5 | Archive paths | ⚠️ | Feishu folder not confirmed |

⚠️ #5: Feishu Drive folder not specified
→ Suggestion: Create folder via lark-drive

[After user confirms...]

✅ Script generated: scripts/clawhub_daily_executor.py
✅ Schedule prompt written
✅ Schedule task created (cron: 0 9 * * *, timezone: Asia/Shanghai)
```

## Directory Structure

```
cron-task/
├── SKILL.md                          # Main entry (agent workflow)
├── references/
│   ├── readiness-checklist.md        # 9-point check methodology
│   ├── schedule-prompt-template.md   # Schedule message template
│   └── archiving-guide.md            # Three-destination archiving guide
├── assets/
│   ├── executor_template.py          # Executor script template
│   └── metadata_header.md            # Archive metadata header template
├── README.md                         # Chinese docs
├── README.en.md                      # English docs
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT-0
└── .gitignore
```

## Known Limitations

- **TRAE Schedule only**: Uses TRAE's Schedule tool, not system cron. Minimum interval is 10 minutes.
- **Feishu IM only**: Currently only supports Feishu Interactive Card for notifications. Email and WeChat are future extensions.
- **Requires pre-configured env vars**: FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_USER_OPEN_ID, IMA credentials must be set beforehand.
- **Python 3.10+**: Executor scripts use modern Python features.
- **Windows-first**: Tested on Windows with PowerShell 5.1. Linux/macOS may need path adjustments.

## License

MIT-0 © 2026 EdwardWason
