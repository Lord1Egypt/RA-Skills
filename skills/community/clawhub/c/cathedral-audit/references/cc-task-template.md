# CC Task Briefing Template

Use this format when writing task briefings for Claude Code sessions.

```markdown
# Task: [Short title]

[1-2 sentence context: what audit finding this addresses and why]

## Items

### 1. [Item name]
- File(s): `path/to/file.cs`
- Problem: [What's wrong]
- Fix: [What to do]

### 2. [Item name]
...

## Constraints
- Verify with `dotnet build` after all changes
- Grep for references before any deletion
- NO architectural changes unless explicitly stated
- Report what you did for each item
```

## Guidelines

- **Be specific.** File paths, method names, property names. CC works best with exact targets.
- **State the problem AND the fix.** Don't make CC figure out the solution — you already know it from the audit.
- **Group by theme.** One briefing per priority tier, not per item.
- **Include constraints.** Always include `dotnet build` verification. Add "grep before delete" for removal tasks.
- **Scope appropriately.** Each briefing should be completable in one CC session (5-20 min). If it's bigger, split it.
- **No ambiguity on code changes vs spec changes.** Explicitly state "NO code changes" for spec-only tasks, or "spec updates only" etc.
