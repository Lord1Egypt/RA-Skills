---
name: daily-digest
description: "Generate a structured daily work digest from session logs and memory files. Use when the user asks for a daily summary, end-of-day recap, work log, or 'what did I do today'. Scans memory/*.md, session transcripts, and git activity to produce a human-readable digest with key accomplishments, decisions, and pending items."
metadata: {"emoji": "📰", "requires": ["session-logs"]}
---

# Daily Digest

Generate a structured, human-readable daily digest from OpenClaw session activity, memory files, and workspace state.

## When to use

- User asks "今天做了什么" / "daily summary" / "end of day recap"
- Periodic self-reporting or standup prep
- Reviewing a specific date's work activity

## Prerequisites

- `memory/` directory with daily notes (or empty if first run)
- `session-logs` skill available for transcript search
- Git repository in workspace (optional)

## Steps

### 1. Identify the target date

Default to today (local timezone). Accept explicit date arguments (YYYY-MM-DD).

### 2. Gather source material

Run these in parallel where possible:

```bash
# Daily memory note
cat memory/YYYY-MM-DD.md 2>/dev/null

# Recent memory files from the last 24h
find memory/ -name "*.md" -newermt "YYYY-MM-DD HH:MM" 2>/dev/null

# Git activity (if workspace is a repo)
git -C workspace log --since="YYYY-MM-DD 00:00" --until="YYYY-MM-DD 23:59" --oneline --all 2>/dev/null
```

### 3. Search session transcripts

Use the `session-logs` skill to search for key events:

```
Search session transcripts for today's date, looking for:
- Task completions (files created, published, deployed)
- Decisions made
- Errors resolved
- Questions answered
```

### 4. Classify and structure

Sort findings into these sections:

| Section | What goes there |
|---------|----------------|
| ✅ 完成事项 | Concrete deliverables, published content, resolved issues |
| 📝 决策记录 | Choices made, preferences confirmed, paths selected |
| ⚠️ 遗留问题 | Open blockers, deferred items, things to follow up |
| 🔄 进行中 | Tasks started but not finished |

### 5. Format and deliver

- If no activity found: state "今日无活动记录" clearly, do not fabricate.
- Keep the digest concise — aim for 5-15 lines.
- Use Chinese if sources are in Chinese; match the user's primary language.
- Optionally write the digest to `memory/digests/YYYY-MM-DD-digest.md` for future reference.

## Output format

```markdown
# 📰 每日工作摘要 — YYYY-MM-DD

## ✅ 完成事项
- [item]

## 📝 决策记录
- [decision]

## ⚠️ 遗留问题
- [blocker]

## 🔄 进行中
- [in-progress]
```

## Rules

1. **Never fabricate activity.** If sources are empty, say so.
2. **Cross-reference sources.** A claim should appear in at least one concrete source before inclusion.
3. **Deduplicate.** If the same event appears in memory and git and sessions, count it once.
4. **Respect privacy.** Do not include secrets, API keys, or personal data in the digest.
5. **Keep it scannable.** Bullet points over paragraphs. Three items per section max unless genuinely significant.

## Validation checklist

- [ ] Date is correct and matches sources
- [ ] Every item traces to a concrete source file or transcript
- [ ] No fabricated or inferred activity
- [ ] Privacy checks passed (no secrets leaked)
- [ ] Length is reasonable (not a wall of text)
