# Memory Template — Atlassian Cloud APIs + CLIs

Create `~/atlassian/memory.md` with this structure:

```markdown
# Atlassian Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Primary deployment model: Cloud | Data Center | mixed
- Active products: Jira, Confluence, Bitbucket, Trello, Admin, Compass, Statuspage, Opsgenie
- Default sites and workspaces:
- Preferred auth modes by product:
- IDs to keep handy only if the user asked to remember them:
- Approval style for write actions:

## Notes
- Risky surfaces to double-check before writes
- Migration notes such as Opsgenie -> JSM/Compass
- Repeated failure patterns, missing scopes, or rate-limit issues

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the user's estate | Keep collecting defaults opportunistically |
| `complete` | Enough context to route most requests fast | Use saved sites and IDs by default |
| `paused` | User does not want more setup right now | Work with current context only |
| `never_ask` | User wants zero proactive setup questions | Never reopen setup unless they ask |

## Key Principles

- Never store tokens, keys, passwords, session cookies, or secrets
- Save product scope and only the IDs the user explicitly wants remembered
- Prefer natural-language notes over config-style switches
- Update `last` each time the skill is used
