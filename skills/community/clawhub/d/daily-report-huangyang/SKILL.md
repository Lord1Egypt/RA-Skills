---
name: daily-report
description: Generate structured daily reports for the user, summarizing completed tasks, ongoing work, pending items, and notable notes. Use when user asks for daily reports, status summaries, or wants to track daily progress and pending work. Triggers include 日报, 今天干了什么, daily report, 今日总结, 今天完成了什么.
license: mit
version: 2.0.0
---

# Daily Report

## Overview

This skill generates structured daily reports that help users:
- Review what was accomplished today
- Track ongoing work and progress
- Identify pending items and blockers
- Maintain a record of daily activities

## Report Format

Generate reports in the following structure:

### 📋 今日完成

- [Task 1] Description + Status (✅/进行中/⏸️)
- [Task 2] Description + Status

### ⏳ 进行中

- [Task A] Current progress + Estimated completion time
- [Task B] Pending confirmation items + What's needed from user

### 📝 待办/未完成

- [Todo 1] Reason/Blocker
- [Todo 2] Priority level

### 💡 备注

- Items needing special attention
- Issues or risks discovered

## Data Sources

When generating a daily report, check these sources:

1. **Today's memory file** (`memory/YYYY-MM-DD.md`) - Primary source for today's tasks
2. **Yesterday's memory file** (`memory/YYYY-MM-DD.md`) - For carryover context
3. **Recent conversation history** - If needed for clarification
4. **Project files** (e.g., TODO.md, PROJECTS.md) - If relevant

## Generation Process

1. Read today's memory file to identify completed tasks
2. Check for ongoing work and pending items
3. Identify any blockers or areas needing user attention
4. Format according to the report structure above
5. Highlight critical items (deadlines, blockers, user decisions needed)

## Customization

Adjust the report format or sections based on user feedback. Common variations:
- Add time tracking (hours spent per task)
- Add next-day priorities
- Include links to relevant files or commits
- Add metrics (tasks completed, tasks in progress, etc.)

## Triggers

Generate a daily report when:
- User asks for "日报", "今天干了什么", "daily report", "今日总结", "今天完成了什么"
- User wants to review daily progress
- User asks "what did you do today" or similar
- User requests a status summary

## Notes

- Keep reports concise and actionable
- Prioritize highlighting blockers and decisions needed
- Use clear status indicators (✅, 🔄, ⏸️, ❌)
- Update memory files with the generated report for future reference