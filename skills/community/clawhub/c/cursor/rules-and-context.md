# Rules And Context - Cursor

Use this file when Cursor seems inconsistent, over-general, or blind to repo conventions.

## Rule Hierarchy

Current Cursor setups should prefer:
1. `.cursor/rules` for project rules
2. repo-level agent guidance when it already exists
3. user rules only for durable personal defaults
4. `.cursorrules` only as legacy material that may need migration

## `.cursor/rules` Strategy

Treat rules as scoped tools, not as one giant policy dump.
Useful rule categories:
- repo conventions
- framework-specific constraints
- dangerous-action guardrails
- review and verification expectations

Keep rules short enough to load intentionally and specific enough to change behavior.

## Attachment Modes

Cursor supports different rule attachment patterns. Treat them as separate tools:
- always-on rules for universal repo safety
- auto-attached rules for specific file or context triggers
- agent-requested rules for optional deep guidance
- manual rules for operator-controlled loading

If too many rules attach at once, Cursor becomes noisy and less predictable.

## Context Hygiene

- Start with the smallest relevant folder or file set.
- Use indexing and references deliberately instead of assuming the full repo should always load.
- If Cursor is ignoring conventions, inspect the rule layout before rewriting the prompt.

## Legacy Cleanup

- `.cursorrules` is legacy, not the target design for new setups.
- Migrate only when the repo is ready and you can preserve intent.
- Do not leave duplicate instructions spread across `.cursorrules`, `.cursor/rules`, and repo-level agent guidance unless the overlap is deliberate.
