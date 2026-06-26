---
name: failure-memory
description: "Automatic failure pattern recording and recall system. Prevents repeating the same mistakes by logging errors with context, root cause, and resolution. Use when: (1) a command/task fails and you want to record why, (2) starting a new task and want to check for known pitfalls, (3) reviewing accumulated failure patterns for learning, (4) agent makes an error and needs to log it for future prevention. Triggers: 'log failure', 'check failures', 'failure report', 'what went wrong', 'mistake log', or any error/failure during agent work."
---

# Failure Memory

Record failures. Learn from them. Never repeat them.

## Core Concept

Every failure has three parts:
1. **What happened** (error message, symptom)
2. **Why it happened** (root cause)
3. **How to fix/avoid it** (resolution)

This skill stores them in a searchable markdown file and provides a recall mechanism before starting similar tasks.

## File Structure

```
memory/
└── failures.md      # All failure records (append-only log)
```

## Recording a Failure

When an error occurs during work, append to `memory/failures.md`:

```markdown
## [YYYY-MM-DD HH:mm] <short title>

- **Category:** <build|deploy|config|api|permissions|data|logic|network|dependency>
- **Context:** <what you were trying to do>
- **Error:** `<exact error message or symptom>`
- **Root Cause:** <why it happened>
- **Resolution:** <what fixed it>
- **Prevention:** <how to avoid next time>
- **Tags:** <comma-separated keywords for search>
```

### When to Record

Record AUTOMATICALLY when:
- A shell command exits non-zero and you identify why
- An API call fails and you find the cause
- A config/setup step fails and you resolve it
- You catch yourself repeating a previously-solved mistake
- A sub-agent reports an error with resolution

Do NOT record:
- Transient network timeouts (unless pattern emerges)
- Intentional test failures
- User-cancelled operations

## Pre-Task Recall

**Before starting any significant task**, search failures for relevant history:

```bash
grep -i "<keyword>" memory/failures.md
```

Or use `memory_search` if vector search is available:
```
memory_search query="<task description> failure error"
```

If matches found, mention them briefly:
> ⚠️ Known pitfall: [title] — [prevention tip]

## Failure Report

When asked for a failure report or review, generate a summary:

1. Read `memory/failures.md`
2. Group by category
3. Identify repeat patterns (same root cause appearing multiple times)
4. Suggest systemic fixes for patterns

### Report Format

```markdown
# Failure Report — YYYY-MM-DD

## Stats
- Total: N failures recorded
- Top category: <category> (N occurrences)
- Repeat offenders: N patterns seen 2+ times

## Repeat Patterns
### <pattern name>
- Seen: N times
- Root cause: <shared cause>
- Systemic fix: <recommendation>

## Recent Failures (last 7 days)
- [date] <title> — <resolution>
```

## Initialization

Run `scripts/init.sh` to set up the failures file:

```bash
bash scripts/init.sh [memory_dir]
```

Default memory_dir: `./memory`

## Best Practices

1. **Be specific** — "EACCES on /var/run/docker.sock" beats "permission error"
2. **Include the exact error** — Future grep depends on it
3. **Tag generously** — More tags = better recall
4. **Review monthly** — Patterns reveal systemic issues
5. **Link to fixes** — Reference commits, PRs, or config changes when possible
