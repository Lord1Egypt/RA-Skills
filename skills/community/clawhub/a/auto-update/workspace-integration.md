# Workspace Integration - Auto-Update

Only propose this snippet if the user wants install-time reminders in their workspace files. Show the exact lines first.

## AGENTS.md Snippet

```markdown
## Auto-Update Reminders

- After any `clawhub install`, ask whether the user wants a quick explanation of the new skill and whether it should auto-update or stay manual.
- Record the answer in `~/auto-update/skills.md`.
- If the user does not answer, inherit the default from `~/auto-update/memory.md`.
```

## When to Skip Integration

Do not push AGENTS changes when:
- the user wants the updater to stay local only
- they already have their own install-time workflow
- they are still testing whether they like auto-update behavior
