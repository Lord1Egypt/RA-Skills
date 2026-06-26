# Memory Template - Baidu

Create these baseline files inside `~/baidu/`.

## `memory.md`

```markdown
# Baidu Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- Auto-activate when:
- Stay silent when:
- Preferred output shape:

## Surface Defaults
- Primary Baidu surfaces:
- Default task type:
- Preferred docs language:
- Chinese-first sources allowed:

## Trust Rules
- Official domains to prioritize:
- Supporting sources allowed:
- Evidence floor for high-stakes answers:

## Notes
- Durable constraints and lessons
```

## `accounts.md`

```markdown
# Baidu Accounts

## Projects and Owners
- Product family:
  Account or project label:
  Owner:
  Region:
  Notes:

## Approval Boundaries
- Action type:
  Who must approve:
  What must stay manual:
```

## `regions.md`

```markdown
# Baidu Region Notes

## Defaults
- Primary geography:
- Cross-border constraints:
- Language preference:

## Repeated Constraints
- Constraint:
  Why it matters:
  Affected surfaces:
```

## `sources.md`

```markdown
# Baidu Source Notes

## Trusted
- Domain:
  Best use:
  Notes:

## Conditional
- Domain:
  Risk:
  Use only when:
```

## `decisions.md`

```markdown
# Baidu Decisions

## YYYY-MM-DD - Task title
- Request:
- Chosen surface:
- Recommended path:
- Rejected paths:
- Key assumptions:
- Open blockers:
- Confidence:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Ask only what changes routing or risk materially |
| `complete` | Stable defaults and trust rules exist | Focus on execution and verification |
| `paused` | Memory stays but setup is paused | Avoid setup prompts unless the task forces new context |
| `never_ask` | User wants no setup prompts | Use stored defaults unless a hard blocker requires confirmation |

## Rules

- Keep memory concise and Baidu-specific.
- Update `last` after meaningful changes in scope, regions, or trust rules.
- Save only what the user explicitly shares or approves for storage.
- Never store secrets, raw tokens, or copied billing data.
