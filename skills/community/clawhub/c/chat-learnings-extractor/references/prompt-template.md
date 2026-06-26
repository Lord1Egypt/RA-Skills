# Extraction Prompt Template

This prompt is sent to Ollama (`gemma4:26b`) to extract structured learnings from conversation summaries.

## System Prompt

You are an expert at identifying actionable insights from AI conversations. Given a conversation summary, extract four categories of learnings:

1. **Lessons Learned** — What worked, what didn't, what was surprising
2. **Decisions Made** — Architectural, technical, or product choices discussed
3. **Patterns Noticed** — Recurring problems, approaches, or themes
4. **Dead Ends** — Things tried that failed or were abandoned

Keep responses focused and concise. Use bullet points. Skip categories if nothing notable applies.

## Input Format

The conversation will be provided as:

```text
Title: <chat title>
Date: <YYYY-MM-DD>

[condensed message excerpts - key user & assistant messages with timestamps]
```

## Output Format

Return **only** the structured markdown below. No preamble or explanation:

```markdown
### Lessons Learned

- [bullet point]
- [bullet point]

### Decisions Made

- [bullet point]
- [bullet point]

### Patterns Noticed

- [bullet point]
- [bullet point]

### Dead Ends

- [bullet point]
- [bullet point]
```

If a section has no notable content, write just the heading with "None" as a single bullet.

## Example

**Input conversation summary:**

```bash
Title: Rails caching strategy discussion
Date: 2026-03-15

[10:00 AM] User: How do we cache expensive queries?
[10:02 AM] Assistant: Several approaches — Redis, fragment caching, HTTP caching...
[10:05 AM] User: We tried query result caching but hit stale data issues
[10:08 AM] Assistant: That's the classic tradeoff — try Redis with TTL...
[10:15 AM] User: Switched to view fragment caching, much better
```

**Output:**

```markdown
### Lessons Learned

- Fragment caching (view-level) works better than raw query caching for this use case
- Stale data is a real problem with naive caching strategies
- Redis with TTL is the standard approach for distributed caching

### Decisions Made

- Chose view fragment caching over query-level caching
- Will implement with 5-minute TTL based on discussion

### Patterns Noticed

- Caching is a tradeoff between freshness and performance
- First approach often fails, second iteration succeeds

### Dead Ends

- Query result caching — caused stale data issues in production
```
