# Memory Template - Escalate

Create `~/escalate/memory.md` with this structure:

```markdown
# Escalate Memory

## Status
status: ongoing
version: 1.0.1
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Rules
- When this skill should auto-activate
- Whether it should step in on ambiguous autonomy, external actions, or proactive work

## Default Posture
- Conservative, balanced, or high-trust baseline
- Whether low-risk internal work should be silent, act-then-inform, or propose-first
- Preferred escalation prompt style

## Always Ask
- Categories that always need approval
- Hard blocks that remain escalated even after trust grows

## Safe To Handle
- Low-risk internal actions that can usually proceed
- Reversible tasks the agent may handle without waiting

## Domain Overrides
- Repo-, workflow-, or team-specific exceptions
- Cases where the default posture changes

## Notes
- Durable patterns that improve judgment
- Exceptions worth remembering
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Setup still evolving | Keep learning where autonomy helps vs hurts |
| `complete` | Stable escalation baseline | Reuse saved boundaries aggressively |
| `paused` | User wants less setup friction | Ask only when a real boundary matters |
| `never_ask` | User does not want setup prompts | Do not reopen setup unless asked |

## Local Files to Initialize

```bash
mkdir -p ~/escalate/domains
touch ~/escalate/{memory.md,decisions.md}
```

## Template for the Decisions Log

```markdown
# Escalation Decisions

- YYYY-MM-DD: situation -> acted | informed | proposed | asked
  - Why: short rationale
  - User follow-up: what changed the rule
```

## Rules

- Keep memory in natural language, not raw policy dumps.
- Store durable boundaries in `~/escalate/memory.md`, recent judgment calls in `~/escalate/decisions.md`, and domain-specific exceptions in `~/escalate/domains/`.
- Update `last` after each meaningful escalation session.
- Never persist credentials, secrets, or copied third-party private data.
