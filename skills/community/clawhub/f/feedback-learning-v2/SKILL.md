---
name: feedback-learning
version: 2.0.0
description: Zero-LLM feedback learning system for OpenClaw agents. Detects user feedback (emoji reactions, text signals like "переделай"/"круто"), logs events, tracks positive AND negative patterns, auto-promotes structured rules with behavioral delta test, and generates weekly reports. Supports Russian and English. No API keys needed — runs entirely on shell scripts and Python.
tags: [learning, feedback, self-improvement, patterns, analytics, zero-llm]
---

# Feedback Learning System v2

A complete, zero-LLM pipeline for agents to learn from user feedback. Track what works, catch what doesn't, promote durable rules.

## Architecture

```
User feedback / exec error
        ↓
detect-feedback.py   ←── error-catcher.sh (PostToolUse hook)
        ↓
  log-event.sh  ──────────────────────────────────────────→ events.jsonl
                                                                   ↓
                                            analyze-patterns.py (nightly)
                                                                   ↓
                                                          patterns.json
                                              (positive + negative patterns)
                                                                   ↓  (≥3 hits, delta test)
                                                             genes.json
                                                    (structured rules: condition→action)
                                                                   ↓
                                            weekly-report.py (Sundays)
                                                                   ↓
                                                          reports/WEEKLY_*.md
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| User gives positive feedback | `log-event.sh <agent> positive user_nlp "<ctx>" "<signal>"` |
| User corrects/complains | `log-event.sh <agent> correction user_nlp "<ctx>" "<signal>" "<lesson>"` |
| Exec command failed | `log-event.sh <agent> error exec_fail "<ctx>" "<stderr>" "<lesson>"` |
| Detect feedback from text | `python3 detect-feedback.py "переделай это"` |
| Run pattern analysis now | `python3 analyze-patterns.py` |
| Generate report now | `python3 weekly-report.py` |
| Check active rules (genes) | `python3 check-genes.py` |
| Mark gene as resolved | `python3 check-genes.py --resolve <gene_id>` |

## Setup

### 1. Install files

```bash
DIR="${FEEDBACK_LEARNING_DIR:-$HOME/.openclaw/shared/learning}"
mkdir -p "$DIR/reports"
cp scripts/* "$DIR/"
chmod +x "$DIR/log-event.sh" "$DIR/error-catcher.sh"
touch "$DIR/events.jsonl"
```

### 2. Initialize data files

```bash
DIR="${FEEDBACK_LEARNING_DIR:-$HOME/.openclaw/shared/learning}"

[ -f "$DIR/patterns.json" ] || cat > "$DIR/patterns.json" << 'EOF'
{"version": "2.1", "updated": "", "patterns": {"negative": [], "positive": []}}
EOF

[ -f "$DIR/genes.json" ] || cat > "$DIR/genes.json" << 'EOF'
{"version": "2.1", "rules": []}
EOF

[ -f "$DIR/capsules.json" ] || cat > "$DIR/capsules.json" << 'EOF'
{"version": "2.1", "capsules": []}
EOF
```

### 3. Add to AGENTS.md boot sequence

```markdown
## Feedback Learning
Before tasks: check `$FEEDBACK_LEARNING_DIR/genes.json` for applicable rules.

Auto-detect and log signals:
- Positive words/emoji → `bash $DIR/log-event.sh <agent> positive user_nlp "<ctx>" "<signal>"`
- Negative/correction → `bash $DIR/log-event.sh <agent> correction user_nlp "<ctx>" "<signal>" "<lesson>"`
- Exec fail (exit≠0) → `bash $DIR/log-event.sh <agent> error exec_fail "<ctx>" "<stderr[:200]>" "<lesson>"`
```

### 4. Set up crons

```
# Pattern analysis (nightly 3:30 AM)
schedule: cron 30 3 * * * @ Europe/Moscow
payload: python3 ~/.openclaw/shared/learning/analyze-patterns.py

# Weekly report (Sundays 4:00 AM)
schedule: cron 0 4 * * 0 @ Europe/Moscow
payload: python3 ~/.openclaw/shared/learning/weekly-report.py
```

### 5. (Optional) Hook integration for auto-error capture

For Claude Code / Codex hooks:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "bash ~/.openclaw/shared/learning/error-catcher.sh"}]
    }]
  }
}
```

## Usage

### Log events manually

```bash
DIR="${FEEDBACK_LEARNING_DIR:-$HOME/.openclaw/shared/learning}"

# Error
bash "$DIR/log-event.sh" anton error exec_fail \
  "updating openclaw.json" "SyntaxError: trailing comma" \
  "Always validate JSON with python3 -c before writing"

# Positive
bash "$DIR/log-event.sh" anton positive user_nlp \
  "generated weekly report" "🔥 огонь!"

# Correction
bash "$DIR/log-event.sh" anton correction user_nlp \
  "sent message in wrong format" "не так, в маркдауне давай" \
  "Confirm output format before sending to Telegram"
```

### Detect feedback from text (no LLM)

```bash
echo "круто, зашло!" | python3 detect-feedback.py
# → {"type": "positive", "source": "user_nlp", "signal": "круто", "confidence": 0.8}

python3 detect-feedback.py "переделай это, не тот формат"
# → {"type": "correction", "source": "user_nlp", "signal": "переделай", "confidence": 0.8}

# Pipe mode for hook usage
echo "$TOOL_OUTPUT" | python3 detect-feedback.py --pipe | bash log-event.sh auto
```

### Check active rules before a task

```bash
python3 check-genes.py
# Lists active rules, signals stale ones

python3 check-genes.py --filter exec_fail
# Filter by type

python3 check-genes.py --resolve gene_20260310_120000_0
# Mark a resolved rule as inactive
```

## Data Files

| File | Purpose |
|------|---------|
| `events.jsonl` | Append-only event log (all feedback), deduped by content hash |
| `patterns.json` | Grouped patterns: BOTH positive and negative, with counts |
| `genes.json` | Promoted structured rules (condition → action → context) |
| `capsules.json` | Successful reasoning paths to avoid re-computation |
| `reports/` | Weekly synthesis reports |

## Event Schema

```json
{
  "ts": "2026-03-20T12:00:00Z",
  "id": "sha256_first8",
  "agent": "anton",
  "type": "error|correction|positive|requery",
  "source": "exec_fail|user_nlp|user_emoji|requery|auto",
  "context": "what agent was doing",
  "signal": "the trigger text or emoji",
  "hint": "suggested fix or rule",
  "heat": 1
}
```

## Gene (Promoted Rule) Schema v2

```json
{
  "id": "gene_20260310_120000_0",
  "status": "active|stale|resolved|wont-fix",
  "origin": "original signal/pattern text",
  "type": "error|correction|positive",
  "condition": "When doing X",
  "action": "Do Y instead of Z",
  "context": "Additional context",
  "agents": ["anton"],
  "occurrences": 3,
  "last_seen": "2026-03-20T...",
  "promoted_at": "2026-03-20T...",
  "expires": null,
  "active": true
}
```

## Promotion Flow (v2)

1. Events accumulate in `events.jsonl` (deduped by hash)
2. `analyze-patterns.py` groups similar events (both positive AND negative)
3. Pattern hits ≥3 in 30 days → **Behavioral Delta Test**: would this rule change a future decision? If yes → promote.
4. Promoted gene has structured fields: `condition`, `action`, `context`
5. **Stagnation check**: if gene exists but same pattern keeps recurring → mark gene as `stale` and escalate
6. Genes auto-expire after 90 days of inactivity (no new events matching)
7. `weekly-report.py` includes gene health: active / stale / resolved counts

## Supported Languages

- **Russian:** 20+ negative, 19+ positive triggers, correction patterns
- **English:** 10 negative, 8 positive triggers
- **Emoji:** Universal positive/negative reactions

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Positive pattern tracking | ❌ skipped | ✅ tracked separately |
| Gene structure | `"AVOID: key_text"` | `condition → action → context` |
| Gene lifecycle | active only | active / stale / resolved / wont-fix |
| Behavioral Delta Test | ❌ | ✅ promotes only if rule changes future behavior |
| Stagnation detection | ❌ | ✅ re-occurring genes flagged as stale |
| Path configuration | hardcoded | `$FEEDBACK_LEARNING_DIR` env var |
| Event deduplication | ❌ | ✅ content hash |
| Hook integration | ❌ | ✅ error-catcher.sh for PostToolUse |
| Gene check utility | ❌ | ✅ check-genes.py |
| Gene expiry | ❌ | ✅ 90-day inactivity auto-expire |
