---
name: daily-note-helper
description: 整理零散日常记录、会议随手记、工作流水和个人复盘内容，输出清晰的每日摘要、待办事项、风险提醒和明日计划。Use when the user provides rough notes, chat fragments, meeting bullets, or end-of-day reflections and wants a concise organized daily note.
---

# Daily Note Helper

## Overview

Turn messy daily notes into a clean, practical summary. Keep the output brief, preserve concrete details, and make next actions easy to scan.

## Workflow

1. Identify the date, people, projects, decisions, blockers, and promised follow-ups.
2. Group similar fragments instead of repeating them.
3. Rewrite vague items into action-oriented bullets when enough context exists.
4. Mark uncertain items with `待确认` rather than inventing details.
5. Keep private or sensitive content neutral and avoid adding judgment.

## Output Format

Use this structure by default:

```markdown
## 今日概述
一到两句话总结今天的主线。

## 完成事项
- ...

## 待办事项
- [ ] ...

## 风险与阻塞
- ...

## 明日建议
- ...
```

If the user asks for a different language or format, follow that request.

## Style

- Prefer concise Chinese unless the source material is mainly English.
- Use short bullets and concrete verbs.
- Do not over-polish casual personal notes.
- Do not create fake metrics, deadlines, names, or decisions.
