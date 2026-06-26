# Memory Template - Decide

Create `~/decide/memory.md` with this structure:

```markdown
# Decide Memory

## Status
status: ongoing
version: 1.0.1
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Rules
- When this skill should step in for consequential branching choices
- Which decision families always deserve a deliberate review

## Always Ask
- Decision categories that must never become autonomous without explicit fresh approval
- High-stakes exceptions and no-go areas

## Required Components
- The minimum context needed before a major decision can be reused
- Signals that make the context incomplete

## Confirmed Defaults
- Component patterns the user explicitly approved as defaults
- The choice that should be proposed or applied when the pattern fully matches

## Domain Overrides
- Project-, client-, or domain-specific rules that beat the generic default

## Notes
- Durable decision guidance
- Warnings about overgeneralization
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Decision model still evolving | Ask often and keep logging |
| `complete` | Stable decision baseline exists | Reuse only clearly validated patterns |
| `paused` | User wants less setup friction | Ask only when a real branching choice appears |
| `never_ask` | User does not want setup prompts | Do not reopen setup unless requested |

## Local Files to Initialize

```bash
mkdir -p ~/decide/domains
touch ~/decide/{memory.md,decisions.md}
```

## Template for `decisions.md`

```markdown
# Decision Log

- YYYY-MM-DD: [domain] question
  - Components: client=__, surface=__, project=__, constraints=__
  - Options: option A | option B | option C
  - Chosen: __
  - Why: __
  - Confidence: missing | partial | close | validated | confirmed-default
  - Outcome: accepted | corrected | pending
```

## Rules

- Keep durable decision policy in `~/decide/memory.md`.
- Keep individual decision records in `~/decide/decisions.md`.
- Keep domain-specific component models and exceptions in `~/decide/domains/`.
- Never persist credentials, secrets, or copied third-party private data.
