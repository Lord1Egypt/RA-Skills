---
name: inbox-triage
description: Automated message filtering, prioritization, and response drafting across all platforms. Use when: (1) Inbox/messages are overwhelming or unmanageable, (2) Need to categorize by priority (urgent/normal/spam), (3) Want daily digest summaries, (4) Require draft responses for low-priority items, (5) Need to filter notifications and alerts
---

# Inbox Triage Skill

Automate message management by categorizing, summarizing, and drafting responses to keep your inbox clean and actionable.

## Quick Start

```bash
# Install the skill
npx clawhub install inbox-triage

# Trigger
"Help me triage my inbox"
```

## Core Features

### 1. Message Categorization

Messages are classified into three categories:

- **Urgent**: Requires immediate attention (deadlines, direct questions, emergencies)
- **Normal**: Important but can wait (updates, newsletters, routine items)
- **Spam/Noise**: Can be ignored or deleted (promotions, notifications, irrelevant)

**Triggers for categorization:**
- Contains time-sensitive language ("ASAP", "urgent", "deadline")
- Direct questions or requests for action
- From known contacts with time constraints

### 2. Daily Digest Generation

Creates a consolidated summary of all messages received that day:

```
📧 Daily Inbox Digest - April 15, 2026

🔴 URGENT (2):
  - Meeting reminder: Team sync at 3PM today
  - Question from Sarah: Need approval on budget by EOD

🟡 NORMAL (5):
  - Newsletter: Weekly tech roundup
  - Update: Project milestone reached
  - ...

🟢 SPAM/NOISE (12):
  - Promotions, notifications, alerts
```

### 3. Draft Response Generation

Auto-drafts replies for normal-spam categories:

- **Acknowledgment**: "Thanks for reaching out, I'll review and get back to you."
- **Redirect**: "This is outside my scope - try reaching out to X."
- **Auto-reject**: Polite decline for spam/unsolicited requests

## When to Use This Skill

✅ Inbox/messages are overwhelming
✅ Need to sort through notifications and alerts
✅ Want to save time on routine responses
✅ Need daily summaries of important items
✅ Looking to filter spam automatically

❌ Not for high-stakes communication (legal, medical, financial advice)
❌ Not for creative work (writing, editing, brainstorming)
❌ Not for real-time conversations requiring immediate human response

## How It Works

### Input Processing

1. **Collect**: Gather all messages from configured sources
2. **Analyze**: Parse content, sender, timestamps, and context
3. **Categorize**: Apply priority rules and classification logic
4. **Summarize**: Generate digest or alert summaries
5. **Draft**: Create response options for review

### Configuration

```yaml
# Optional: ~/.inbox-triage/config.yaml
sources:
  - type: signal
    enabled: true
  - type: telegram
    enabled: true
  - type: discord
    enabled: false

rules:
  urgent_keywords:
    - "urgent"
    - "ASAP"
    - "deadline"
    - "important"
  spam_keywords:
    - "unsubscribe"
    - "promotion"
    - "offer"
  auto_draft_for:
    - "normal"
    - "spam"
```

## Output Formats

### JSON (machine-readable)
```json
{
  "timestamp": "2026-04-15T12:00:00Z",
  "digest": {
    "urgent": [...],
    "normal": [...],
    "spam": [...]
  },
  "drafed_responses": [...]
}
```

### Markdown (human-readable)
```markdown
# Daily Triage Report

## 🔴 URGENT
- [ ] Item 1
- [ ] Item 2

## 🟡 NORMAL
- Item 1
- Item 2

## 🟢 SPAM
- 12 items filtered
```

## Limitations

- **Accuracy**: Categorization is probabilistic, not perfect
- **Context**: May miss nuanced context in messages
- **Human review required**: Never auto-send without approval
- **Platform support**: Works best with text-based channels (Signal, Telegram, Discord, email)

## Iteration

Track which categorizations were correct/incorrect:

```bash
# Log correction
echo "CORRECT: urgent - meeting reminder" >> ~/.inbox-triage/corrections.log
echo "INCORRECT: spam - actually important" >> ~/.inbox-triage/corrections.log
```

The system learns from corrections over time.

---

## Integration Examples

### With Cron Manager
```bash
# Run triage every morning at 8AM
0 8 * * * clawhub run inbox-triage --output daily-digest.md
```

### With Weather Alert
```bash
# Send digest only when weather is clear
if [ "$(weather is-clear)" = "true" ]; then
  clawhub run inbox-triage --send-summary
fi
```

### With File Organizer
```bash
# Attach digest as daily log
clawhub run inbox-triage --format json | tee ~/logs/daily-triage-$(date +%Y-%m-%d).json
```
