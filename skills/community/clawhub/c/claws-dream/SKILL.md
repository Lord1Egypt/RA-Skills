---
name: claws-dream
description: "⚠️ DEPRECATED — OpenClaw 2026.4.5+ has official Dreaming (memory-core) built-in. This skill is no longer maintained. Use the official /dreaming slash command instead. Retired 2026-04-06."
---

# 🦐 Nightly Dream — Memory Consolidation System

> "While you sleep, your memories consolidate. Now your AI does too."

A biologically-inspired memory consolidation system. Every night, fragments of your interactions are distilled into structured long-term knowledge — duplicates merged, insights captured, stale memories gracefully archived.

## Features

- 🌙 **Four-Stage Dream Cycle**: Orient → Gather → Consolidate → Prune
- 📊 **5-Metric Health Score**: Freshness, Coverage, Coherence, Efficiency, Reachability
- 🎯 **Importance Scoring**: Base weight × recency × reference boost
- 🗑️ **Forgetting Curve**: Automatic archival of stale, low-importance entries
- 🔗 **Knowledge Graph**: Related entries tracked via index.json
- 📈 **Milestones**: First dream, streaks, entry count milestones
- 🏥 **Smart Skip**: No new content? Still delivers value with memory recall
- 📊 **Dashboard**: Auto-generated HTML health dashboard
- 🔔 **Rich Notifications**: Growth metrics, highlights, insights, stale threads

## Memory Architecture

```
workspace/
├── MEMORY.md              # Structured long-term knowledge
└── memory/
    ├── index.json         # Entry metadata + health stats
    ├── procedures.md       # Workflow preferences
    ├── archive.md         # Archived entries (faded)
    ├── dream-log.md       # Consolidation reports
    ├── dashboard.html     # Generated health dashboard
    ├── YYYY-MM-DD.md      # Daily interaction logs
    └── episodes/          # Project narratives
```

## Quick Start

### Manual Trigger
```
"Run dream" / "Consolidate memory" / "Dream now"
```

### Automatic (Cron)
Pre-configured cron job runs at 03:00 daily.

## Dream Cycle Flow

### Step 0: Smart Skip
Checks for unconsolidated logs. If none → still delivers value via memory recall.

### Step 1: Collect
Reads unconsolidated daily logs. Extracts decisions, facts, lessons, todos.

### Step 2: Consolidate
Compares with MEMORY.md. Semantic dedup. New → append, Updated → modify, Duplicate → skip.

### Step 3: Score & Prune
Computes health score (5 metrics). Archives stale entries below importance threshold.

### Step 4: Notify
Sends rich notification with growth metrics, highlights, insights, and suggestions.

## Health Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| Freshness | 25% | Entries referenced in last 30 days |
| Coverage | 25% | Sections updated in last 14 days |
| Coherence | 20% | Entries with relation links |
| Efficiency | 15% | MEMORY.md line count (concise) |
| Reachability | 15% | Connected components in graph |

## Importance Markers

| Marker | Effect |
|--------|--------|
| 🔥 HIGH | 2x importance weight |
| 📌 PIN | Exempt from archival |
| ⚠️ PERMANENT | Never archive or modify |

## Archival Rules

Entry archived when ALL true:
- 90+ days since last referenced
- Importance < 0.3
- Not marked PIN or PERMANENT
- Not in episodes/

## Manual Commands

| Command | Action |
|---------|--------|
| "Dream now" | Run full consolidation |
| "Memory status" | Show health score + stats |
| "Memory dashboard" | Generate dashboard.html |
| "Memory export" | Export memories to JSON |

## ⚠️ Timeout Configuration (Critical!)

**This skill requires a longer timeout to run properly.** Add this to your `openclaw.json` under `agents.defaults`:

```json
"agents": {
  "defaults": {
    "timeoutSeconds": 300
  }
}
```

Without this, the dream consolidation will timeout and fail. The skill scans many files and needs time to read, analyze, and write memory.

## Cron Configuration (macOS launchd)

Create `~/Library/LaunchAgents/com.openclaw.claws-dream.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.claws-dream</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/clawliu/.openclaw/workspace/skills/claws-dream/scripts/dream.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/Users/clawliu/.openclaw/workspace/logs/claws-dream.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/clawliu/.openclaw/workspace/logs/claws-dream.err</string>
</dict>
</plist>
```

Load with:
```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.claws-dream.plist
```

### Linux (systemd timer)

Create `/etc/systemd/system/claws-dream.service`:

```ini
[Unit]
Description=claws-dream nightly memory consolidation

[Service]
Type=oneshot
ExecStart=/bin/bash /home/user/.openclaw/workspace/skills/claws-dream/scripts/dream.sh
User=user
```

Create `/etc/systemd/system/claws-dream.timer`:

```ini
[Unit]
Description=Run claws-dream daily at 3 AM

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable with:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now claws-dream.timer
```

### Linux (cron)

```bash
0 3 * * * /bin/bash /home/user/.openclaw/workspace/skills/claws-dream/scripts/dream.sh >> /home/user/.openclaw/workspace/logs/claws-dream.log 2>&1
```

### Windows (WSL)

```batch
:: Run via Windows Task Scheduler pointing to WSL
wsl bash -c "bash /mnt/c/Users/you/.openclaw/workspace/skills/claws-dream/scripts/dream.sh"
```

Or create a `.bat` file:
```batch
@echo off
wsl bash -c "bash /home/you/.openclaw/workspace/skills/claws-dream/scripts/dream.sh"
```

### Windows (PowerShell Task Scheduler)

```powershell
$action = New-ScheduledTaskAction -Execute 'bash' -Argument '-c "bash /home/you/.openclaw/workspace/skills/claws-dream/scripts/dream.sh"'
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -TaskName 'claws-dream' -Action $action -Trigger $trigger -RunLevel Limited
```

---

## Reference Files

- `references/dream-prompt.md` — Full consolidation prompt

- `references/first-dream-prompt.md` — First run initialization
- `references/scoring.md` — Health score algorithms
- `references/memory-template.md` — File templates
- `references/dashboard-template.md` — HTML dashboard template

## Safety Rules

1. **Never delete daily logs** — only mark with `<!-- consolidated -->`
2. **Never remove ⚠️ PERMANENT items** — user-protected
3. **Safe changes** — if MEMORY.md changes >30%, save .bak first
4. **Scope** — only read/write memory/ directory and MEMORY.md

---

_Version 2.2 — Built with 🦐 by Crayfish Liu_
