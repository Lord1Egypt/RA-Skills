---
name: agent-daily-review
description: Helps agents conduct structured end-of-day review, reflection, and documentation. Provides capabilities to scan today's records, categorize activities, perform reflective analysis, and generate review reports. Supports Cron auto-trigger for cumulative growth with each run.
---

# Agent Daily Review

## Overview

The Daily Review skill helps agents conduct systematic review and reflection at the end of the day, transforming fragmented daily records into structured growth accumulation.

**Core Capabilities:**
1. **Scan Records** - Automatically scan today's memory files, artifacts, and MEMORY.md entries
2. **Categorize Activities** - Classify activities into: Completed, In Progress, Issues/Blockers, Learning/Growth, Others
3. **Reflect and Analyze** - Calculate productivity score, identify highlights and challenges, generate improvement suggestions
4. **Generate Report** - Output structured review report and archive to long-term memory

**Use Cases:**
- User says "Do my daily review for today"
- User says "Summarize today"
- Cron scheduled task triggers (e.g., daily at 22:00)
- User wants to review work/learning status for a specific day

## Workflow

### 1. Scan Today's Records

Execute `scripts/daily_review.py` to scan the following:
- `memory/YYYY-MM-DD.md` - Today's journal entries
- `MEMORY.md` - Today's entries in long-term memory
- `workspace/*.md` - Artifact files generated today

### 2. Categorize Activities

Automatically identify and categorize:
- **Completed** - Contains keywords like "completed," "done," "resolved," ✅
- **In Progress** - Contains keywords like "in progress," "working on," 🔄
- **Issues/Blockers** - Contains keywords like "issue," "blocked," "bug," ❌
- **Learning/Growth** - Contains keywords like "learned," "researched," "understood"
- **Meetings/Communication** - Contains keywords like "meeting," "discussed," "sync"

### 3. Reflect and Analyze

Perform intelligent analysis based on categorization results:
- **Productivity Score** - Calculate based on record count and artifact count (0-100)
- **Today's Highlights** - Identify completed important tasks and decisions
- **Challenges Encountered** - Summarize issues and pending items
- **Improvement Suggestions** - Generate personalized recommendations based on data

### 4. Generate Report

Output structured report containing:
- Today's Overview (statistics)
- Completed Tasks List
- In Progress Tasks List
- Issues/Blockers
- Learning/Growth Records
- Highlights Summary
- Reflection and Suggestions
- Tomorrow's Plan Framework

### 5. Archive to Memory

- Save review report to `reviews/review_YYYY-MM-DD.md`
- Append review summary to `MEMORY.md`

## Usage

### Manual Execution

```bash
# Execute today's review
python scripts/daily_review.py

# Specify working directory
python scripts/daily_review.py -w /path/to/workspace

# Specify output file
python scripts/daily_review.py -o /path/to/output.md

# Review specific date
python scripts/daily_review.py -d 2024-01-15

# Do not save to MEMORY.md
python scripts/daily_review.py --no-memory
```

### Use as Module

```python
from scripts.daily_review import DailyReview

review = DailyReview("/path/to/workspace")
report = review.run(save_to_memory=True)
print(report)
```

### Cron Auto-Trigger

Set up automatic daily review at 22:00:

```bash
# Add scheduled task using openclaw cron
openclaw cron add --name "daily-review" \
  --schedule "0 22 * * *" \
  --command "python ~/.qclaw/skills/daily-review/scripts/daily_review.py"
```

Or using cron tool:

```json
{
  "name": "daily-review",
  "schedule": {"kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "Please perform today's review using the daily-review skill, scanning today's records and generating a review report."
  },
  "sessionTarget": "isolated"
}
```

## Report Format

Review reports use Markdown format with the following sections:

```markdown
# Daily Review Report - YYYY-MM-DD

## 📊 Today's Overview
- Date, Record Count, Artifact Count, Productivity Score

## ✅ Completed
- Task List

## 🔄 In Progress
- Pending List

## ⚠️ Issues/Blockers
- Issue List

## 📚 Learning/Growth
- Learning Records

## 🎯 Today's Highlights
- Highlights Summary

## 💭 Reflection and Suggestions
- Improvement Suggestions

## 📝 Tomorrow's Plan
- Plan Framework
```

## Directory Structure

```
workspace/
├── memory/
│   └── 2024-01-15.md          # Today's journal entries
├── reviews/
│   └── review_2024-01-15.md   # Review report
├── MEMORY.md                   # Long-term memory (review summary appended here)
└── *.md                        # Artifacts generated today
```

## Tips

1. **Cultivate Journaling Habit** - Record timestamped entries in `memory/YYYY-MM-DD.md` daily for better review results
2. **Use Keywords** - Use keywords like "completed," "learning," "encountered issue" when journaling to facilitate auto-categorization
3. **Periodic Review** - Review weekly/monthly review reports to discover growth trajectory
4. **Integrate with Cron** - Set up automatic review to ensure daily reflection is never missed

## Resources

- `scripts/daily_review.py` - Core review script
- `references/framework.md` - Detailed review framework explanation (optional reading)