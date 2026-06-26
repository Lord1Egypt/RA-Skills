---
name: conversation-analyzer
description: Intelligent conversation analysis, summarization, and conclusion recording. Analyzes user personality, tracks tasks, checks incomplete tasks, and writes to memory files.
version: 1.0.0
author: opendolph
source: https://github.com/opendolph/skills/tree/main/conversation-analyzer
---

# Conversation Analyzer 🧠

> Intelligent conversation analysis, summarization, and conclusion recording

---

## Core Features

### 1. User Personality Analysis

**Analysis Dimensions:**
- **Personal Traits**: Personality, communication style, decision-making patterns
- **Preferences**: Technical preferences, tool choices, content types
- **Skills**: Tech stack, professional capabilities, familiar domains
- **Experience**: Career path, project experience, growth trajectory
- **Background**: Work environment, team role, industry background
- **Emotional State**: Stress level, satisfaction, focus areas
- **Current Activities**: Current projects, key tasks, daily activities
- **Future Goals**: Goals, plans, expectations

**Execution:**
- Read existing USER.md records
- Merge new analysis results
- Update USER.md
- Call appropriate skill tools if needed

### 2. Conversation Task & Demand Analysis

**Analysis Dimensions:**
- **Requested Tasks**: Specific tasks, completion status
- **Predicted Future Needs**: Predict next steps based on patterns
- **Error Records**: Understanding deviations, execution errors, improvement points

**Execution:**
- Read "Conversation Analysis" records in MEMORY.md
- Incrementally write new analysis results
- Call appropriate skill tools if needed

### 3. Incomplete Task Detection

**Check Scope:**
- Todo items mentioned in conversation
- Promised but incomplete items
- Exclude tasks marked as "not needed" in MEMORY.md

**Execution:**
- List incomplete tasks
- Send inquiry messages via Feishu
- If no incomplete tasks, send "No incomplete tasks found"

---

## Trigger Conditions

| Scenario | Trigger Method |
|----------|----------------|
| Auto-trigger | Every 10 conversations (via HEARTBEAT.md counter) |
| Scheduled trigger | Daily at 12:00 and 24:00 (cron) |
| Manual trigger | User inputs "analyze conversation", "summary", "check tasks" |

---

## Analysis Workflow

### Every 10 Conversations

```
Conversation counter +1
    ↓
Counter >= 10?
    ↓ YES
Reset counter
    ↓
Execute 3 analysis tasks
    ↓
Update memory files
```

### Daily Scheduled Analysis (12:00, 24:00)

```
Cron trigger
    ↓
Analyze all conversations from 00:00 to current time
    ↓
Execute 3 analysis tasks
    ↓
Update memory files
    ↓
Send Feishu notification for incomplete tasks
```

---

## File Operations

### Input Files
- `HEARTBEAT.md` - Conversation counter, task tracking
- `USER.md` - User profile records
- `MEMORY.md` - Long-term memory, conversation analysis history
- `SESSION-STATE.md` - Current session state
- Chat history (via sessions_history tool)

### Output Files
- `USER.md` - Updated user profile
- `MEMORY.md` - Appended conversation analysis
- `HEARTBEAT.md` - Reset conversation counter
- Feishu messages - Task notifications

---

## Usage

```bash
# Manual trigger analysis
node skills/conversation-analyzer/scripts/analyze.js

# Check incomplete tasks only
node skills/conversation-analyzer/scripts/check-tasks.js

# Daily full analysis (0:00 to now)
node skills/conversation-analyzer/scripts/daily-analysis.js
```

---

## Cron Configuration

### Add to crontab

```bash
# Daily analysis at 12:00 and 24:00
0 12,0 * * * cd ~/.openclaw/workspace && node skills/conversation-analyzer/scripts/daily-analysis.js > /dev/null 2>&1
```

### Or use OpenClaw cron

```bash
openclaw cron add "0 12,0 * * *" "conversation-analyzer/daily-analysis"
```

---

## Integration with HEARTBEAT.md

The skill reads and updates HEARTBEAT.md:

```markdown
## Conversation Counter
- Current count: 0
- Last analysis: 2026-03-24 21:00
- Threshold: 10 conversations
```

When counter reaches 10:
1. Execute personality analysis
2. Execute task analysis
3. Execute incomplete task check
4. Reset counter to 0

---

## Task Status Definitions

| Status | Meaning |
|--------|---------|
| Queue | Waiting to start |
| Active | In progress |
| Waiting | Blocked/Waiting |
| Done | Completed |
| Aborted | Cancelled |
| NotNeeded | Explicitly marked as not required |

---

*Transform passive responses into proactive insights 🎯*
