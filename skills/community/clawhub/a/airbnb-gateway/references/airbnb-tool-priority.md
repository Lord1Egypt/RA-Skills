# Reference — Airbnb tool priority & role mapping

**This is the one file you customize per deployment.** It maps abstract tool
*roles* (used everywhere else in the skill) to the concrete tool names in your
environment. Everything else in the package is portable; edit here only.

## Tier order (universal — do not reorder)

1. **Airbnb endpoint** — first-class, structured, auth-aware. Default for every
   supported operation.
2. **Agent-browser** — navigate/inspect when no endpoint covers the op or an
   endpoint is hard-down.
3. **DevTools** — read-only DOM inspection / UI verification.
4. **Playwright** — last-resort automation for read-only or human-approved ops.

## Role → tool map (EDIT THIS for your deployment)

> The names below are the reference deployment's tools. Replace with yours.
> If a role has no tool in your environment, leave it blank — the skill will
> degrade to the next available tier and escalate if a *required* role is empty.

| Role | Reference deployment tool | Tier |
|---|---|---|
| Airbnb: list/read messages | `/tools/airbnb/messages` | 1 |
| Airbnb: list reservations | `/tools/airbnb/reservations` | 1 |
| Airbnb: read calendar | `/tools/airbnb/calendar` | 1 |
| Airbnb: send message | `/tools/airbnb/messages/send` | 1 |
| Browser: health/identity | `/tools/browser/status` | 2 |
| Browser: navigate | `/tools/browser/navigate` | 2 |
| DevTools: list tabs | `/tools/devtools/tabs` | 3 |
| DevTools: navigate | `/tools/devtools/navigate` | 3 |
| DevTools: evaluate (read-only) | `/tools/devtools/evaluate` | 3 |
| Playwright: fallback | (deployment-specific path) | 4 |

## When to drop a tier (decision rules)

- **Stay on tier 1** unless: (a) no tier-1 tool exists for this operation, or
  (b) a tier-1 call returns a *hard transport failure* (5xx / connection error /
  timeout) **twice in a row**. A single slow or empty response is not a drop
  trigger — retry once on tier 1 first.
- **Before dropping for "auth" reasons**, call the browser health/identity role.
  Airbnb auth is host-owned (provided by the host browser identity). Missing
  *local* browser/session state is NOT evidence the account is logged out.
- **DevTools is read-only in this skill.** Use `evaluate` to read/verify DOM,
  never to click a send button. A send happens only via the tier-1 send role (or
  an explicitly human-approved browser send).
- **Playwright only** when tiers 1–3 are all unavailable for the operation AND
  the operation is read-only or has explicit human approval. Log that you used
  it and why.

## Graceful degradation matrix

| Operation | tier-1 absent → | also tier-2 absent → | all absent → |
|---|---|---|---|
| read inbox / thread | agent-browser read | DevTools DOM read | escalate (required role missing) |
| read reservations | agent-browser read | DevTools DOM read | escalate |
| read calendar | agent-browser read | DevTools DOM read | escalate |
| send reply | human-approved browser send only | — | escalate; do NOT improvise |
| verify sent | re-read via any read role | DevTools DOM read | mark `unconfirmed`, escalate |

Sending is special: there is no silent fallback for a send. If the tier-1 send
role is unavailable, the only alternative is an explicitly human-approved
browser send, and verification is still mandatory.
