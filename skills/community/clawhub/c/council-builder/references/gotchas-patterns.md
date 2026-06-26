# Gotchas System

The most valuable file any agent can have. Gotchas are domain-specific pitfalls that Claude keeps hitting.

## Why Gotchas Matter

Claude has strong defaults, but every domain has traps where those defaults fail. A gotchas file catches these before they waste time. Start with 1-2 entries, grow over time. This file becomes the single highest-ROI artifact per agent.

## Structure

Every agent gets a `gotchas.md` in their root directory:

```
agents/[name]/gotchas.md
```

## Entry Format

```markdown
## [Short Title]

**What goes wrong:** One sentence describing the failure mode.

**The fix:** One sentence or a code snippet showing the correct approach.
```

Keep entries short. If it needs more than 3-4 lines, it belongs in `references/` instead.

## Examples by Role

### Research Agent
```markdown
## Stale API data

**What goes wrong:** X API free tier returns cached data up to 15 min old. Reports look outdated.

**The fix:** Always note "as of [timestamp]" and mention cache lag if data seems stale.
```

### Content Agent
```markdown
## Exclamation marks in Arabic content

**What goes wrong:** Claude defaults to using ! in enthusiastic Arabic text. User bans them.

**The fix:** Never use exclamation marks. Rewrite for emphasis without punctuation tricks.
```

### Dev Agent
```markdown
## Force push on shared branches

**What goes wrong:** Claude suggests `git push --force` to fix diverged branches.

**The fix:** Always use `git push --force-with-lease` or rebase + normal push. Never force push main/develop.
```

### Finance Agent
```markdown
## VAT assumption

**What goes wrong:** Claude uses 15% VAT (Saudi rate) but some items are zero-rated or exempt.

**The fix:** Always ask which VAT category applies before calculating. Check exemption list first.
```

### Ops Agent
```markdown
## Timezone in calendar events

**What goes wrong:** Claude creates events in UTC instead of user's timezone (Asia/Riyadh).

**The fix:** Always specify timezone explicitly. Never rely on system default.
```

## Growth Pattern

1. **Day 1**: Create gotchas.md with 1-2 known pitfalls for the role
2. **Week 1**: Add gotchas from `.learnings/ERRORS.md` entries that repeat
3. **Ongoing**: When the same mistake happens twice, it earns a gotcha entry
4. **Promotion**: If a gotcha applies to multiple agents, copy it to `shared/learnings/CROSS-AGENT.md`

## When to Read Gotchas

- Before starting any major task in the agent's domain
- After loading SOUL.md (gotchas.md should be the second file read)
- When working in an area where past mistakes occurred
