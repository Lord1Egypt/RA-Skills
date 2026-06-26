# Operating Rules Reference

This is the full operating detail behind the short SKILL.md workflow.

## When to log

| Trigger | File |
|---|---|
| Command/tool failure | `errors.md` |
| User correction or agent discovery | `learnings.md` |
| Requested capability you do not have | `wishes.md` |
| Recurrent or critical lesson ready for human review | `promotion-queue.md` |

## Dedup process

1. Check for an existing `id:` first
2. If no ID match, grep by a stable keyword or command name
3. If found, update the existing line instead of appending a duplicate
4. Bump `count:N` and refresh the date when appropriate
5. Keep the original `source:` unless the original entry was wrong

## Review-queue triggers

Queue an item when either condition is true:
- `count:3+`
- `severity:critical`

Queue only a one-line prevention rule, not the whole incident report.

## Promotion model

Lifecycle:

```text
pending → approved → promoted
         ↘ rejected
```

Rules:
- Agents may add `status: pending`
- Humans decide `approved`, `promoted`, or `rejected`
- Do not auto-write to `SOUL.md`, `AGENTS.md`, `TOOLS.md`, or similar instruction files
- If something is promoted, note that on the source entry

Typical targets:
- behavior → `SOUL.md`
- workflow → `AGENTS.md`
- tool gotcha → `TOOLS.md`
- project-local convention → local instruction file

## Pre-task review

Before high-risk or previously-problematic work:

1. grep `.learnings/*.md` for the task keyword
2. name the relevant learning
3. state the adjustment you are making
4. after success, increment `prevented:N` if the learning actually changed behavior

Good times to do this:
- external sends
- cron edits
- flaky APIs
- sub-agent spawning
- any task with prior failures

## Detail files

Use a detail file only when the one-line entry is not enough:
- the fix is non-obvious
- environment or version matters
- several failed approaches are worth preserving

Suggested structure: `detail-template.md`

## Staleness and trimming

Recommended hygiene:
- add `expires:` for temporary workarounds
- quarterly, archive entries older than 6 months with `count:1` and `prevented:0`
- keep active files small enough to scan quickly
- if a file grows too large, archive resolved noise before adding process overhead

## Non-goals

This loop is not:
- a dashboard
- a registry
- a taxonomy project
- autonomous self-modification
- a replacement for human judgment on instruction changes
