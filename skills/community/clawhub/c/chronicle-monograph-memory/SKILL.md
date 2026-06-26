# Hippocampus

> "AI is meant to FIX human memory flaws, why learn human decay?"

## Philosophy

**Traditional memory = Human memory imitation = DECAY = WRONG**

Hippocampus FIXES human memory flaws:
- Forgetting → Perfect recall
- Fuzzy matching → Precise timestamps
- Passive triggers → Proactive warnings
- Importance decay → Never lose anything

## Features

| Feature | Description |
|---------|-------------|
| **No Decay** | AI never forgets |
| **Micro-Macro Workflows** | Short command → full workflow |
| **Proactive Triggers** | Automatically loads relevant memory when keywords appear |
| **Checkpoints** | Know exactly where project left off |
| **Success Tracking** | Remember what works / fails |
| **Failure Warning** | Proactive pattern detection |
| **Knowledge Graph** | Networked memory |

## Setup (REQUIRED!)

After installing, run initialization:

```bash
cd /path/to/hippocampus
python3 scripts/memory.py init
```

Then verify:

```bash
python3 scripts/memory.py status
```

## Commands

| Command | Description |
|---------|-------------|
| `/hippo init` | Initialize DB and directories |
| `/hippo status` | View memory status |
| `/hippo save` | Save current context |
| `/hippo recall <keyword>` | Precise recall |
| `/hippo checkpoint` | Save project state |
| `/hippo warn` | Check failure patterns |
| `/hippo graph` | View knowledge graph |
| `/hippo learn-workflow` | Register a micro→macro workflow |
| `/hippo workflows` | List all registered workflows |
| `/hippo forget-workflow` | Remove a workflow |
| `/hippo triggers` | List keyword triggers |
| `/hippo add-trigger` | Add a proactive trigger |
| `/hippo remove-trigger` | Remove a trigger |
| `/hippo readingbetweenthelines` | 察言观色 status and config |
| `/hippo readingbetweenthelines-stat` | Show current word counts |
| `/hippo readingbetweenthelines-clear` | Reset word counts |
| `/hippo add-instant` | Add instant trigger |
| `/hippo remove-instant` | Remove instant trigger |
| `/hippo add-threshold` | Add threshold trigger |
| `/hippo remove-threshold` | Remove threshold trigger |
| `/hippo config` | Show / reload config |
| `/hippo analyze` | Analyze all memory |

## Micro-Macro Workflows

Teach hippocampus your shortcuts:

```
/hippo learn-workflow deploy -> When I say "deploy", run: git push, then run tests, then notify team via slack
/hippo learn-workflow send report -> When I say "send report", compile weekly data, format as markdown, send via email
```

When you later say "deploy" or "send report", hippocampus will retrieve the full workflow automatically.

List all registered workflows:
```
/hippo workflows
```

## Proactive Keyword Triggers

Configure hippocampus to automatically load relevant memories when you mention certain topics:

```
/hippo add-trigger database -> database-architecture
/hippo add-trigger api -> api-design
```

Now when your message contains "database" or "api", hippocampus loads the associated memory before answering — no need to manually recall.

List active triggers:
```
/hippo triggers
```

Configure triggers manually in USER_CONFIG.md:
```
PROACTIVE_KEYWORDS = database->database-architecture,api->api-design
```

## 察言观色 — ReadingBetweenTheLines

Proactive memory loading based on sustained conversation patterns.
When you discuss a topic repeatedly, hippocampus automatically loads relevant memories.

**Two trigger types**:

Instant: fires immediately when a high-signal keyword appears (error, deploy, database...)
Threshold: fires only after a word appears N times within a sliding window (project→5, api→4, config→4...)

**Commands**:
```
/hippo readingbetweenthelines         Show status and config
/hippo readingbetweenthelines-stat    Show current word counts in window
/hippo readingbetweenthelines-clear   Reset word counts
/hippo add-instant error -> error-patterns     Add instant trigger
/hippo add-threshold project -> 5              Add threshold trigger
```

**How it works**:
Heartbeat runs every N minutes (default 1). Analyzes recent user messages, removes stop words, counts meaningful words. If a trigger keyword meets its condition, the associated memory is loaded before answering.

**Configuration** (USER_CONFIG.md):
```
READINGBETWEENTHELINES_ENABLED = true
INSTANT_TRIGGERS = error->error-patterns,database->database-architecture
THRESHOLD_TRIGGERS = project->5,api->4,config->4
TRIGGER_COOLDOWN = 5   # minutes before reloading same memory
```

## Two Memory Types

**Chronicle** — Temporal memory for everyday interactions
- Auto-saves session content, indexed by time

**Monograph** — Important topics with rich metadata
- Stores significant decisions, workflows, patterns
- Created via `/hippo checkpoint` or `/hippo recall` saves

## Proactive Recall (How It Works)

When `PROACTIVE_TRIGGERS_ENABLED = true` in USER_CONFIG.md:

1. Before each response, hippocampus scans your message
2. If a trigger keyword is found, it loads the associated memory file
3. The loaded memory is prepended to context for this response
4. You get relevant context without asking for it

This is configured via `PROACTIVE_KEYWORDS` in USER_CONFIG.md.

## Version

1.0.3
