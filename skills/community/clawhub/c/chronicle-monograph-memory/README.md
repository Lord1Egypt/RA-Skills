# Hippocampus

> "AI is meant to FIX human memory flaws, why learn human decay?"

## Philosophy

Traditional memory systems mimic human memory—with decay, forgetting, and importance decay. 

**That's cute, humanized but inefficient, and quite the opposite of what we went this far for.**

**AI memory should FIX these flaws, not copy them.**

## Core Principles

1. **No Decay** — AI doesn't forget. Ever.
2. **Precise Retrieval** — Exact timestamps, not "recent"
3. **Success Tracking** — Remember what works / fails
4. **Project Checkpoints** — Know exactly where you left off
5. **Proactive Warning** — Alert before repeating mistakes
6. **Read Between the lines, literally** — Automatically loads relevant memories when conversation patterns emerge

---

## Two Memory Types

**Chronicle** — Temporal memory for everyday interactions

- Auto-saves session content, indexed by time
- Use case: "What did we discuss last Tuesday?"

**Monograph** — Important topics with rich metadata

- Stores significant decisions, workflows, patterns
- Long-term importance
- Use case: "What's the user's preferred communication style?"

---

## Installation

### Step 1: Initialize (REQUIRED!)

```bash
cd /path/to/hippocampus
python3 scripts/memory.py init
```

### Step 2: Verify

```bash
python3 scripts/memory.py status
```

### Step 3: Setup Cron Jobs

```bash
# Auto-save every 6 hours
openclaw cron add --name "hippocampus-autosave" \
  --schedule "0 */6 * * *" \
  --session-target isolated \
  --payload "Run: python3 /path/to/scripts/memory.py autocheck"

# Daily memory creation at 7 AM
openclaw cron add --name "hippocampus-daily" \
  --schedule "0 7 * * *" \
  --session-target isolated \
  --payload "Run: python3 /path/to/scripts/memory.py new daily-\$(date +\%Y-\%m-\%d)"

# Daily analysis at 11 PM
openclaw cron add --name "hippocampus-analyze" \
  --schedule "0 23 * * *" \
  --session-target isolated \
  --payload "Run: python3 /path/to/scripts/memory.py analyze"
```

---

## Commands

| Command                                    | Description                                |
| ------------------------------------------ | ------------------------------------------ |
| `/hippo init`                              | Initialize DB and directories (RUN FIRST!) |
| `/hippo status`                            | View memory status                         |
| `/hippo save`                              | Save current context                       |
| `/hippo recall <keyword>`                  | Precise recall                             |
| `/hippo checkpoint`                        | Save project state                         |
| `/hippo warn`                              | Check failure patterns                     |
| `/hippo graph`                             | View knowledge graph                       |
| `/hippo learn-workflow <micro> -> <macro>` | Register a micro→macro workflow            |
| `/hippo workflows`                         | List all workflows                         |
| `/hippo forget-workflow <micro>`           | Remove a workflow                          |
| `/hippo triggers`                          | List proactive triggers                    |
| `/hippo add-trigger <kw> -> <topic>`       | Add a trigger                              |
| `/hippo remove-trigger <keyword>`          | Remove a trigger                           |
| `/hippo readingbetweenthelines`            | 察言观色 status and config                     |
| `/hippo readingbetweenthelines-stat`       | Show current word counts                   |
| `/hippo readingbetweenthelines-clear`      | Reset word counts                          |
| `/hippo add-instant <kw> -> <topic>`       | Add instant trigger                        |
| `/hippo remove-instant <keyword>`          | Remove instant trigger                     |
| `/hippo add-threshold <kw> -> <count>`     | Add threshold trigger                      |
| `/hippo remove-threshold <keyword>`        | Remove threshold trigger                   |
| `/hippo config`                            | Show configuration                         |
| `/hippo analyze`                           | Analyze all memory                         |

---

## ReadingBetweenTheLines

Proactive memory loading based on sustained conversation patterns. When you discuss a topic repeatedly, hippocampus automatically loads relevant memories — no need to manually recall.

### Two Trigger Types

**Instant triggers** — fire immediately on first occurrence:

- `error` → loads error-patterns memory
- `database` → loads database-architecture memory
- `deploy` → loads deployment-checklist memory
- `api` → loads api-design memory
- `test` → loads test-strategy memory

**Threshold triggers** — fire after N occurrences in the sliding window:

- `project` fires after 5 mentions
- `api` fires after 4 mentions
- `config` fires after 4 mentions
- `feature` fires after 4 mentions
- `data` fires after 3 mentions

### How It Works

1. Heartbeat runs every N minutes (default: 1)
2. Reads recent user messages
3. Tokenizes: removes 123 stop words (the, a, is, that, etc.)
4. Counts meaningful word frequency
5. Checks instant triggers (immediate) and threshold triggers (N occurrences)
6. Loads associated monograph if triggered
7. Cooldown: does not reload the same memory within 5 minutes (default)

### Configuration (USER_CONFIG.md)

```yaml
READINGBETWEENTHELINES_ENABLED = true
INSTANT_TRIGGERS = error->error-patterns,database->database-architecture,api->api-design,deploy->deployment-checklist,test->test-strategy
THRESHOLD_TRIGGERS = project->5,api->4,config->4,feature->4,data->3
TRIGGER_COOLDOWN = 5   # minutes
```

---

## Micro-Macro Workflows

Teach hippocampus shortcuts for complex workflows:

```
/hippo learn-workflow deploy -> Run git push, then execute tests, then notify team via Slack
/hippo learn-workflow send report -> Compile weekly data, format as markdown, send via email
```

When you say "deploy" or "send report", hippocampus retrieves the full workflow automatically.

---

## Directory Structure

```
hippocampus/
├── README.md           ← This file (only README)
├── SKILL.md           ← Full command reference
├── skill.yaml         ← Version 1.0.3
├── USER_CONFIG.md     ← Configuration
└── scripts/
    └── memory.py      ← Core script

# After running init:
assets/hippocampus/
├── chronicle/         ← Temporal memory (auto-created)
├── monograph/         ← Important topics (auto-created)
├── index/            ← Keyword index (auto-created)
└── workflows/        ← Micro-Macro workflows (auto-created)
```

---

## v1.0.3 Release Notes

### New in v1.0.3

- **Micro-Macro Workflow Memory**: Register short commands that resolve to full workflows
- **ReadingBetweenTheLines**: Proactive memory loading via heartbeat + word frequency analysis
- **Proactive Keyword Triggers**: Automatically loads relevant memory when keywords appear
- **Command rename**: All commands now use `hippo` prefix (not `photon`)
- **14 new commands** total

### Upgrading from v1.0.2

1. Update USER_CONFIG.md with new configuration options
2. Run `/hippo init` to create the new workflows directory
3. Re-register any workflows (not preserved across versions)

---

## Version

- Hippocampus v1.0.3
- Author: gabe-luv-nancy@126.com
- License: MIT
