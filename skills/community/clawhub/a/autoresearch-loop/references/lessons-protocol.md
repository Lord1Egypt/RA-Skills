# Lessons Protocol

## When to Extract Lessons

| Event | Lesson type |
|-------|-------------|
| Every kept iteration | Positive — what worked and why |
| Every PIVOT decision | Strategic — what failed and why, what to try instead |
| Run completion | Summary — overall findings, best approach found |
| Safety stop | Boundary — what approval, scope, or measurement was missing |

## Lesson Format

```markdown
## [type] — [date] — iteration [N]
- **What:** [one sentence describing the change]
- **Result:** metric went from X to Y (delta: Z)
- **Why it worked / failed:** [concise explanation]
- **Reuse:** [when to apply this lesson again, or what to avoid]
- **Scope:** [approved files/directories touched]
```

## Storage

- File: `autoresearch-lessons.md` in the working repo root unless the user chooses another path
- Do not commit this file unless the user explicitly asks
- Read at the start of every run — consult before picking hypotheses
- Capacity: about 50 entries. When over capacity, summarise older entries over 30 days into a single paragraph, preserving current-run lessons verbatim.

## How to Use Lessons When Picking Hypotheses

Before picking a hypothesis:
1. Check if a similar approach has been tried before
2. If it failed previously, skip it or apply the lesson to do it differently
3. If it succeeded, try related variants first
4. Positive lessons bias toward proven approaches
5. Strategic lessons bias away from known dead ends
6. Boundary lessons prevent repeating unsafe scope, rollback, or measurement assumptions

## Time Decay

Lessons older than 90 days are summarised and compressed. The summary preserves:
- What general strategies worked
- What general strategies failed
- Any hard constraints discovered, such as guard-file boundaries or metric limitations

Current-run lessons are always kept verbatim regardless of date.
