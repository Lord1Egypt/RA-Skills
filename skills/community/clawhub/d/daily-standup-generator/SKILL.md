---
name: daily-standup-generator
description: Generate a daily standup report from task lists, chat logs, or project management tools. Trigger: "生成每日站会报告"、"standup"
---

# Daily Standup Generator

Generate a structured daily standup report for team communication.

## When to Use
- User asks for daily standup report
- User wants to summarize yesterday's work
- User needs to prepare for team meeting

## Output Format

```markdown
## 昨日完成 (Completed Yesterday)
- [Task 1]
- [Task 2]

## 今日计划 (Today's Plan)
- [Task 1]
- [Task 2]

## 遇到问题 (Blockers)
- [Issue or "无"]
```

## Data Sources
1. Check memory files for recent tasks
2. Read conversation history for work context
3. Ask user for specific tasks if unclear

## Tips
- Keep it brief (3-5 bullet points max)
- Use emoji for quick scanning 🎯 ✅ 🚧
- If no data available, ask user instead of making up
