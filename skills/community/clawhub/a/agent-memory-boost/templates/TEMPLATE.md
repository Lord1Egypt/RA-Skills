# Task Note Template

Use this template when creating or repairing a task folder. Every task folder must have all three files.

## RESUME.md

```markdown
# <Task Name> Resume

Last heartbeat: <YYYY-MM-DD HH:MM TZ>
Task: <one-line description of the task>
Current status: <active | stalled | complete>
Next action: <one concrete next step>
Key files:
- <relevant file paths>

Restart note: <what a fresh session needs to know to pick this up>
```

## CHECKLIST.md

```markdown
# <Task Name> Checklist

- [ ] Step 1: <describe the step>
- [ ] Step 2: <describe the step>
- [ ] Verification: confirm the work is correct
```

## DOCS.md

```markdown
# <Task Name> Docs

## Goal
<what this task is trying to achieve>

## Important decisions
<key choices made and why>

## Files that matter
<paths to the important files>

## Gotchas and failure modes
<things that can go wrong>

## Notes for the next session
<anything a fresh session should know>
```

## Rules

- Keep notes short and scannable.
- Always update `Last heartbeat` when touching an active task.
- Never leave a folder with only one or two of the three core notes.
- The validator will auto-create missing notes from this template.
