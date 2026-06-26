# clawdoc demo — v0.12.0

Run the interactive demo: `bash dev/demo.sh`

---

## 1. Healthy session — clean bill of health

```
$ bash scripts/diagnose.sh tests/fixtures/12-healthy-session.jsonl
[]
```

## 2. Infinite retry loop (Pattern 1) — critical

```
$ bash scripts/diagnose.sh tests/fixtures/01-infinite-retry.jsonl | jq '.[0]'
{
  "pattern": "infinite-retry",
  "severity": "critical",
  "evidence": "exec called 25 times consecutively with bash scripts/daily-report.sh",
  "cost_impact": 1.51617,
  "prescription": "Your agent called `exec` 25 times in a row, burning $1.52. Add `timeoutSeconds` to your cron payload, or restructure the task prompt to include explicit stop conditions."
}
```

## 3. Full pipeline: diagnose → prescribe

```
$ bash scripts/diagnose.sh session.jsonl 2>/dev/null | bash scripts/prescribe.sh

## 🩻 Diagnosis — 2026-03-14

### Patient summary
- Findings: 3
- Critical: 1 | High: 0 | Medium: 2 | Low: 0
- Estimated recoverable waste: $7.1975

### Findings

#### 🔴 Critical
**Pattern 1: infinite-retry**
- Evidence: exec called 11 times consecutively with bash scripts/deploy.sh
- Cost impact: $0.798540
- Prescription: Add `timeoutSeconds` or explicit stop conditions.

#### 🟡 Warning
**Pattern 4: context-exhaustion**
- Evidence: Session reached 106K tokens (82.8% of 128K context)

### Prescriptions (ranked by cost impact)
1. [🟡 MEDIUM — Pattern 4] Run /compact or use exec with tail/head
2. [🔴 CRITICAL — Pattern 1] Add stop conditions to task prompt
```

## 4. NEW — Task drift detection (Pattern 12)

### 4a. Post-compaction directory divergence

Agent was fixing an auth bug in `src/api/auth/`, then compaction hit.
After compaction, it forgot its task and started editing UI components:

```
$ bash scripts/diagnose.sh tests/fixtures/17-task-drift-compaction.jsonl | jq '.[] | select(.pattern_id == 12)'
{
  "pattern": "task-drift",
  "severity": "medium",
  "evidence": "After compaction at turn 9, agent drifted to new directories:
    docs/api, src/ui/components (8/8 post-compaction file operations
    in unseen directories)",
  "cost_impact": 0.9462,
  "prescription": "Agent forgot its original task after context compaction.
    Write key objectives to MEMORY.md before long sessions, or split
    complex tasks into sub-agent calls."
}
```

### 4b. Exploration spiral

Agent reads 10+ files without making a single edit — stuck exploring:

```
$ bash scripts/diagnose.sh tests/fixtures/18-task-drift-exploration.jsonl | jq '.[] | select(.pattern_id == 12)'
{
  "pattern": "task-drift",
  "severity": "medium",
  "evidence": "Agent made 10 consecutive read/search tool calls without
    any edits — exploration spiral",
  "cost_impact": 0.26178,
  "prescription": "Break complex tasks into smaller steps with explicit
    deliverables, or use a sub-agent for research."
}
```

### Real-world validation

Tested against 99 real Claude Code sessions:
- Pattern 12 detected in **23 sessions (23%)**
- Worst case: **75 consecutive reads** without a single edit ($2.99 wasted)
- Post-compaction drift found in **8 sessions**, one costing **$6.68**

## 5. Headline mode — the tweetable health check

```
$ bash scripts/headline.sh ~/.openclaw/agents/main/sessions/

🩻 clawdoc — 3 findings across 12 sessions (last 7 days)
💸 $47.20 spent — $31.60 was waste (67% recoverable)
🔴 Retry loop on exec burned $18.40 in one session
🟡 Opus running 34 heartbeats ($8.20 → $0.12 on Haiku)
🟡 SOUL.md is 9,200 tokens — 14% of your context window
```

Brief mode for daily crons:
```
$ bash scripts/headline.sh --brief ~/.openclaw/agents/main/sessions/
Yesterday: 8 sessions, $3.40, 1 warning (cron context growth on daily-report)
```
