---
name: feishu-work-review-timemachine
description: Summarize a user's recent Feishu work into a concise weekly review or "time machine" recap by reading Feishu docs, meeting notes, and related materials, then separating the user's real work from meeting noise. Use when the user asks for a recent work summary, weekly/monthly review, time-machine recap, work retrospective, month-in-review, or wants a Feishu doc created/updated with the result.
---

# Feishu Work Review Timemachine

## Overview

Create a compact, high-signal review of a user's recent work from Feishu materials. Focus on what the user actually drove or owned, not everything discussed in meetings.

## Workflow

### 1. Define scope first

Clarify or infer:
- time range: last week / last month / specific dates
- output form: concise recap / weekly breakdown / monthly summary / boss-facing version
- destination: chat reply only, or create/update a Feishu doc

If the user already gave a clear scope, do not ask again.

### 2. Gather source materials from Feishu

Prefer this order:
1. Search the user's recent docs/wiki nodes
2. Prioritize docs created by or owned by the user
3. Read key docs in full only when needed
4. Prefer summaries / structured notes first, then raw transcript docs for validation

Useful source types:
- meeting notes and transcripts
- work-in-progress docs
- project plans
- technical方案 / design docs
- quality / metrics docs
- wiki pages tied to ongoing initiatives

Do not try to read everything. Read enough to identify repeated themes and evidence of ownership.

### 3. Separate real work from meeting noise

Do **not** treat every meeting mention as the user's work.

Use these signals to infer stronger ownership:
- the user is the doc owner / creator / primary editor
- the user is the main speaker framing goals, tradeoffs, or next steps
- action items are explicitly assigned to the user
- the user is pushing the plan, organizing follow-up, or coordinating POCs
- the same initiative appears across multiple docs with the user in a central role

Treat these as weaker signals:
- the user merely attended the meeting
- another person's project status appears in notes
- broad team discussion without assigned ownership
- AI-generated meeting summary claims not supported elsewhere

When uncertain, downshift wording:
- use “参与推动 / 协同推进 / 讨论并判断”
- avoid overstating as “主导完成”

### 4. Extract only the core themes

Compress the material into a few workstreams, usually 3-5:
- platform / product / project track
- AI / efficiency / technical exploration track
- metrics / governance / methodology track
- cross-team coordination track

For each workstream, capture only:
- what changed
- what the user specifically drove
- why it mattered

Delete or skip:
- optional commentary
- long caveats
- repeated explanations
- every subtask from meeting minutes
- alternate interpretations unless the user asked for analysis

### 5. Write in layers

Default output order:
1. one-paragraph core conclusion
2. 3-5 core workstreams
3. weekly breakdown if requested
4. one-sentence summary

If the user says “keep only the core”, reduce to:
- core conclusion
- core workstreams
- optional one-line weekly view

## Output pattern

### Compact monthly review

Use this structure:

```markdown
# 时光机回顾｜过去一月主要工作总结

## 核心结论
[1 short paragraph]

## 核心主线
### 1. [主线]
- [核心动作]
- [核心动作]

### 2. [主线]
- [核心动作]

## 按周回顾
### 第 1 周：[关键词]
[1-3 lines]

### 第 2 周：[关键词]
[1-3 lines]

## 一句话总结
[1 sentence]
```

### Boss-facing version

Make it shorter and more outcome-oriented:
- progress
- scope / influence
- cross-team traction
- next-step signal

Avoid process-heavy wording.

## Feishu doc creation/update

When the user asks to create or write a Feishu doc:
- create the doc once a solid draft exists
- if permissions block the action, tell the user to complete the authorization card and then resume
- once created, prefer overwriting the draft if the user asks to simplify aggressively
- when refining, keep the same doc unless the user asks for a new one

## Style rules

- Write in concise Chinese unless the user asks otherwise
- Prefer short sections over long prose
- Remove “可选项” and hedging text unless uncertainty is material
- Use strong verbs for high-confidence ownership, softer verbs for medium-confidence involvement
- Default to fewer bullets, not more
- Keep the final document skimmable in under 1-2 minutes unless the user asked for depth

## Anti-patterns

Do not:
- dump a list of all meetings
- copy AI meeting summaries verbatim
- equate attendance with ownership
- preserve every nuance when the user wants a crisp recap
- keep “next-step suggestions” if the user asked for a finished summary

## Final check

Before delivering, verify:
- Is this mostly about the user's actual work, not everyone else's?
- Did I collapse repeated themes into a few clear workstreams?
- If asked to simplify, did I remove optional sections rather than just shorten sentences?
- Would the user immediately recognize this as accurate and useful?
