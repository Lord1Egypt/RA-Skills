---
name: clawdoc
version: 0.12.0
description: "Diagnose OpenClaw agent failures, cost spikes, and performance issues with 14 pattern detectors. Use when: task failed unexpectedly, costs seem high, agent burned tokens, debugging session problems, want a health check, reviewing agent performance, agent forgot context, agent kept retrying, agent said commands but didn't execute them, cron jobs getting expensive, heartbeat costs too high, agent drifted off task after compaction, agent stuck reading without editing, agent running find/grep on entire filesystem, agent re-reading same file repeatedly."
user-invocable: true
metadata:
  openclaw:
    emoji: "🩻"
    requires:
      bins:
        - jq
        - bash
        - bc
---

# clawdoc

Examine agent sessions. Diagnose failures. Prescribe fixes.

## Invocation modes

### `/clawdoc` (slash command — default: headline mode)
Produces a compact, tweetable health check:
```
🩻 clawdoc — 3 findings across 12 sessions (last 7 days)
💸 $47.20 spent — $31.60 was waste (67% recoverable)
🔴 Retry loop on exec burned $18.40 in one session
🟡 Opus running 34 heartbeats ($8.20 → $0.12 on Haiku)
🟡 SOUL.md is 9,200 tokens — 14% of your context window
```
Run: `bash {baseDir}/scripts/headline.sh ~/.openclaw/agents/main/sessions`

### `/clawdoc full` or "give me a full diagnosis"
Runs all 14 pattern detectors and produces the complete diagnosis report with evidence and prescriptions.

### `/clawdoc brief` or "clawdoc one-liner for daily brief"
Single-line summary for morning cron integration:
```
Yesterday: 8 sessions, $3.40, 1 warning (cron context growth on daily-report)
```
Run: `bash {baseDir}/scripts/headline.sh --brief ~/.openclaw/agents/main/sessions`

### Natural language triggers
Also activates when user says: "what went wrong", "why did that fail", "debug", "diagnose", "why was that so expensive", "where are my tokens going", "cost breakdown", "health check", "check my agent", "what's wrong", "examine"

## Quick examination — most recent session

Find the most recent session file and run:
```
bash {baseDir}/scripts/examine.sh <session.jsonl>
```
This outputs a JSON summary with turns, cost, token counts, tool call frequency, and error count.

## Single-session diagnosis

Run all 14 pattern detectors against a specific session file:
```
bash {baseDir}/scripts/diagnose.sh <session.jsonl> | jq .
```

## Diagnosis with prescriptions

Pipe diagnose output into prescribe for a formatted report with fix recommendations:
```
bash {baseDir}/scripts/diagnose.sh <session.jsonl> | bash {baseDir}/scripts/prescribe.sh
```

## Cost breakdown

Show per-turn cost waterfall for a session:
```
bash {baseDir}/scripts/cost-waterfall.sh <session.jsonl> | jq '.[0:5]'
```

## Cross-session pattern recurrence

Analyze pattern recurrence across multiple sessions in a directory:
```
bash {baseDir}/scripts/history.sh <sessions-dir> | jq .
```

## Full diagnosis

When the user wants a comprehensive diagnosis, run the scripts above and synthesize findings into this report format:

### Diagnosis report format

```
## 🩻 Diagnosis — [date]

### Patient summary
- Sessions examined: N
- Period: [date range]
- Total spend: $X.XX
- Total tokens: XXk in / XXk out

### Findings

#### 🔴 Critical
[Infinite retry loops, context exhaustion, tool-as-text failures]
Each finding includes: what happened, evidence, estimated cost impact, and specific prescription.

#### 🟡 Warning
[Cost spikes, model routing waste, cron accumulation, compaction damage, workspace overhead]

#### 🟢 Healthy
[What's working well — efficient sessions, good model routing]

### Prescriptions (ranked by cost impact)
1. [Highest-impact fix with specific config change or command]
2. [Second highest]
3. [Third]

### Cost breakdown
[Per-day costs for the examination period]
[Top 3 most expensive sessions with root cause]
```

## Pattern reference

| # | Pattern | Severity | Key indicator |
|---|---------|----------|--------------|
| 1 | Infinite retry loop | 🔴 Critical | Same tool called 5+ times consecutively |
| 2 | Non-retryable error retried | 🔴 High | Validation error → identical retry |
| 3 | Tool calls as text | 🔴 High | Tool names in assistant text, no toolCall blocks |
| 4 | Context window exhaustion | 🟡-🔴 | inputTokens > 70% of contextTokens |
| 5 | Sub-agent replay | 🟡 Medium | Duplicate completion messages in parent |
| 6 | Cost spike | 🟡-🔴 | Session cost > 2x rolling average |
| 7 | Skill selection miss | 🟢 Low | "command not found" after skill activation |
| 8 | Model routing waste | 🟡 Medium | Premium model on heartbeat/cron |
| 9 | Cron context accumulation | 🟡 Medium | Growing inputTokens across cron runs |
| 10 | Compaction damage | 🟡 Medium | Post-compaction tool call repetition |
| 11 | Workspace token overhead | 🟡 Medium | Baseline > 15% of context window |
| 12 | Task drift | 🟡 Medium | Post-compaction directory divergence or 10+ reads without edits |
| 13 | Unbounded walk | 🟠 High | Repeated unscoped find/grep -r flooding output |
| 14 | Tool misuse | 🟡 Medium | Same file read 3+ times without edit, or identical search repeated |

## Self-improving-agent integration

To enable writing findings to `.learnings/LEARNINGS.md`, set `CLAWDOC_LEARNINGS=1` before running prescribe:
```
CLAWDOC_LEARNINGS=1 bash {baseDir}/scripts/diagnose.sh <session.jsonl> | bash {baseDir}/scripts/prescribe.sh
```

## Tips

- Session JSONL files are the ground truth for all diagnostics
- Use `jq -s` (slurp) for aggregations across all lines in a session file
- Filter `message.content[]` by `type=="text"` for readable content, `type=="toolCall"` for tool invocations
- When prescribing config changes, always show the exact JSON path and value
