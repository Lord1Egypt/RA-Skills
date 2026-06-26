# Memory Template - Cursor

Create `~/cursor/memory.md` with this structure:

```markdown
# Cursor Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user uses Cursor for and why -->
<!-- Example: repo-aware implementation and review with local CLI only, no Background Agents -->

## Activation Boundaries
<!-- When this skill should activate automatically and when it should stay quiet -->

## Repo Defaults
<!-- Approved repos, verification expectations, and git-safety posture -->

## Rules Strategy
<!-- Preferred use of .cursor/rules, repo agent guidance, and legacy cleanup decisions -->

## Privacy and Remote Work
<!-- Indexing, Background Agent, GitHub, Bugbot, and MCP boundaries -->

## Surface Preferences
<!-- Editor Agent, Ask, Manual, custom modes, CLI, Background Agent, Bugbot -->

## Notes
<!-- Durable operational observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining durable Cursor defaults |
| `complete` | Stable surfaces and trust posture are clear | Reuse defaults unless the environment changes |
| `paused` | User wants less overhead | Save only critical changes |
| `never_ask` | User rejected persistence | Operate statelessly |

## Key Principles

- Store workflow boundaries, not full prompts, full diffs, or private transcripts.
- Keep repo approvals, remote-workflow approvals, and MCP approvals explicit.
- Record which Cursor surfaces are preferred and which are prohibited.
- Update `last` on each meaningful Cursor session.
