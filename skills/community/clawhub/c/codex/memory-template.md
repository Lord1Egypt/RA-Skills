# Memory Template - Codex

Create `~/codex/memory.md` with this structure:

```markdown
# Codex Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user is using Codex for and why -->
<!-- Example: PR-ready bugfixes in approved repos with explicit review evidence -->

## Safety Defaults
<!-- Preferred sandbox, approval posture, and no-go actions -->

## Repo Defaults
<!-- Approved repos, dirty-worktree rules, verification expectations, branch habits -->

## Surface Preferences
<!-- Interactive CLI, exec, review, resume, cloud, and local --oss preferences -->

## MCP and Auth Notes
<!-- Approved MCP servers, login preference, and token-handling boundaries -->

## Notes
<!-- Durable operational observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining Codex operating defaults |
| `complete` | Stable posture and approved repos are clear | Reuse defaults unless the environment changes |
| `paused` | User wants less overhead | Save only critical changes |
| `never_ask` | User rejected persistence | Operate statelessly |

## Key Principles

- Store operating boundaries, not full prompts or private chat transcripts.
- Keep repo approvals and MCP approvals explicit.
- Record when cloud or remote flows are allowed versus prohibited.
- Update `last` on each meaningful Codex session.
