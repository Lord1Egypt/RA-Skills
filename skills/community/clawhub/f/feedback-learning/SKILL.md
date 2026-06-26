---
name: feedback-learning
version: 1.0.0
description: Zero-LLM feedback learning system for OpenClaw agents. Detects user feedback (emoji reactions, text signals like "переделай"/"круто"), logs events, discovers recurring patterns, auto-promotes rules, and generates weekly reports. Use when setting up agent self-improvement, configuring feedback detection, or building a learning pipeline. Supports Russian and English. No API keys needed — runs entirely on shell scripts and Python.
tags: [learning, feedback, self-improvement, patterns, analytics]
---

# Feedback Learning System

A complete pipeline for agents to learn from user feedback without spending tokens on analysis.

## Architecture

```
User feedback → detect-feedback.py → log-event.sh → events.jsonl
                                                         ↓
                          weekly-report.py ← analyze-patterns.py
                                                         ↓
                                                   patterns.json
                                                         ↓ (≥3 occurrences)
                                                    genes.json (promoted rules)
```

## Setup

### 1. Install files

Copy the skill contents to your shared learning directory:

```bash
DEST="$HOME/.openclaw/shared/learning"
mkdir -p "$DEST/reports"
cp scripts/* "$DEST/"
chmod +x "$DEST/log-event.sh"
touch "$DEST/events.jsonl"
```

### 2. Initialize data files

If they don't exist, create empty JSON stores:

```bash
cat > "$DEST/patterns.json" << 'EOF'
{"version": "2.0", "updated": "", "patterns": []}
EOF

cat > "$DEST/genes.json" << 'EOF'
{"version": "2.0", "rules": []}
EOF

cat > "$DEST/capsules.json" << 'EOF'
{"version": "2.0", "capsules": []}
EOF
```

### 3. Create LEARNINGS.md for each agent

Add to each agent's workspace:

```markdown
# LEARNINGS.md
**Last Updated:** YYYY-MM-DD
**Total:** 0

## 🟢 Что работает (положительный фидбек)
(пока пусто)

## 🔴 Что НЕ работает (отрицательный фидбек)
(пока пусто)

## 🧠 Извлечённые правила
(пока пусто)

## 🔁 Повторяющиеся паттерны
(пока пусто)

## 💡 Feature Requests
(пока пусто)
```

### 4. Add to AGENTS.md

Add this block to each agent's AGENTS.md boot sequence:

```markdown
## Feedback Learning
- On positive feedback (👍❤️🔥👏💯 or words like "круто","топ","зашло"):
  Run: `bash ~/.openclaw/shared/learning/log-event.sh <agent> positive user_emoji "<context>" "<signal>"`
- On negative feedback (👎🤦😤 or words like "фигня","переделай"):
  Run: `bash ~/.openclaw/shared/learning/log-event.sh <agent> correction user_nlp "<context>" "<signal>" "<hint>"`
- On exec errors:
  Run: `bash ~/.openclaw/shared/learning/log-event.sh <agent> error exec_fail "<context>" "<signal>" "<hint>"`
```

### 5. Set up crons

Pattern analysis (daily):

```
schedule: cron 30 3 * * * @ <timezone>
payload: python3 ~/.openclaw/shared/learning/analyze-patterns.py
```

Weekly report (Sundays):

```
schedule: cron 30 4 * * 0 @ <timezone>
payload: python3 ~/.openclaw/shared/learning/weekly-report.py
```

## Usage

### Log an event manually

```bash
bash log-event.sh anton error exec_fail "config update" "trailing comma in JSON" "Validate JSON before writing"
bash log-event.sh anton positive user_emoji "sent report" "🔥"
bash log-event.sh anton correction user_nlp "sent message" "переделай, не тот формат" "Confirm format before sending"
```

### Detect feedback from text (no LLM)

```bash
echo "круто, зашло!" | python3 detect-feedback.py
# → {"type": "positive", "source": "user_nlp", "signal": "круто", "confidence": 0.8}

python3 detect-feedback.py "переделай это"
# → {"type": "correction", "source": "user_nlp", "signal": "переделай", "confidence": 0.8}
```

### Run pattern analysis

```bash
python3 analyze-patterns.py
```

Outputs: pattern count, promotion status. Updates `patterns.json`. Auto-promotes to `genes.json` when a pattern hits ≥3 occurrences in 30 days.

### Generate weekly report

```bash
python3 weekly-report.py
```

Saves to `reports/WEEKLY_REPORT_YYYY_WNN.md` with stats by agent, source, top patterns, and newly promoted rules.

## Data Files

| File | Purpose |
|------|---------|
| `events.jsonl` | Append-only event log (all feedback) |
| `patterns.json` | Grouped recurring patterns with counts |
| `genes.json` | Promoted rules (≥3 occurrences → active rule) |
| `capsules.json` | Successful reasoning paths (avoid re-computation) |
| `reports/` | Weekly synthesis reports |

## Event Schema

```json
{
  "ts": "2026-03-20T12:00:00Z",
  "agent": "anton",
  "type": "error|correction|positive|pattern|requery",
  "source": "exec_fail|user_nlp|user_emoji|requery|auto",
  "context": "what agent was doing",
  "signal": "the trigger text or emoji",
  "hint": "suggested fix or rule",
  "heat": 1
}
```

## Promotion Flow

1. Events accumulate in `events.jsonl`
2. `analyze-patterns.py` groups similar events by signal text (≥60% similarity)
3. Patterns with ≥3 occurrences in 30 days are promoted to `genes.json`
4. Agents read `genes.json` at boot to apply learned rules
5. `weekly-report.py` synthesizes progress for human review

## Supported Languages

Feedback detection supports:
- **Russian**: 20+ negative triggers, 19+ positive triggers, correction patterns
- **English**: 10 negative, 8 positive triggers
- **Emoji**: Universal positive/negative reactions
