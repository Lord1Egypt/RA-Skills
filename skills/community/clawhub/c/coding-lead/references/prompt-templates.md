# Prompt Templates & Examples

## Context File Template

Write to `<project>/.openclaw/context-<task-id>.md` before spawning:

```markdown
# Task Context: <task-id>

## Project
- Path: /path/to/project
- Stack: Laravel 10 + React 18 + TypeScript + Inertia.js
- Architecture: Action-based (not Service layer)
- Note: Project has CLAUDE.md with full standards — don't repeat here

## Historical Context
- [From memory recall] 2026-02-20: Switched to Action pattern
- [From memory lessons] PlatformLink has 6 types — use enum not magic strings
- [Known pitfall] common/ module auth: reuse CommonAuthTrait

## Long-term Knowledge Boundary
- Preserve only durable decisions, reusable lessons, and stable architecture facts
- Do not promote transient debugging noise, temporary paths, or one-off guesses

## Relevant Code (from qmd)
- app/Actions/UserAction.php — example of Action pattern
- app/Models/User.php — existing user model
- database/migrations/ — migration naming convention

## Related Lessons
- "Including DB schema upfront helps ACP get it right first try"
- "Always include existing test patterns as reference"
```

## Medium Task: Lean Prompt

```
Read .openclaw/context-feat-favorites.md for full project context.

## Task
Add a "favorites" feature: users can favorite items.
Need: migration, model, action, controller, API resource, React component.

## Acceptance Criteria
- [ ] Migration creates user_favorites pivot table
- [ ] Action handles add/remove/check
- [ ] Controller under 20 lines, delegates to Action
- [ ] React component with optimistic update
- [ ] Uses existing auth from common/
- [ ] Existing tests pass

Before finishing:
1. Run linter if available
2. Run tests if available
3. Include results in output

When finished: openclaw system event --text "Done: favorites feature" --mode now
```

**Note how small this is (~20 lines) vs the old approach (~60+ lines with embedded context.** The context file does the heavy lifting.

## Complex Task: Research Phase

```
Read .openclaw/context-refactor-collectors.md for project context.

Investigate app/Services/Collectors/ for refactoring.

DO NOT make changes. Only report:
1. All collector files and their responsibilities
2. How Aggregator calls each collector
3. Error handling and retry patterns
4. Code duplication between collectors
5. Test coverage

Use grep/find to explore. Report findings in structured format.
```

## Complex Task: Execute Phase (after plan confirmed)

```
Read .openclaw/context-refactor-collectors.md for project context.

## Confirmed Plan
- Extract shared HttpClientTrait from 3 collectors
- Do NOT change the collector interface
- Only refactor internal implementation

## Task
1. Create app/Traits/HttpClientTrait.php with shared retry/timeout logic
2. Refactor PaymentCollector, InventoryCollector, ShippingCollector to use trait
3. Keep Aggregator unchanged
4. Run existing tests

## Acceptance Criteria
- [ ] HttpClientTrait with configurable retry (default 3)
- [ ] All 3 collectors use trait, no duplicate HTTP logic
- [ ] Aggregator works unchanged
- [ ] Tests pass, no new dependencies

Before finishing: run linter + tests, include results.
When finished: openclaw system event --text "Done: collector refactor" --mode now
```

## Cross-Session Continuity

Session 1 ends → agent records to memory:
```bash
# [memory] Record progress (skip if smart-agent-memory not installed)
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js remember "favorites feature day 1: backend done (migration, model, action). Frontend started (FavoriteButton.tsx). Blocked on Zustand vs TanStack Query. TODO: finish frontend + tests" --tags code,myapp,favorites 2>/dev/null || echo "memory skip: smart-agent-memory not found"
```

Session 2 → agent recalls and spawns:
```
Read .openclaw/context-feat-favorites.md for project context.

## Continuing: favorites feature (day 2)
Previous session completed backend. Frontend component started at FavoriteButton.tsx.
Decision: use TanStack Query mutation for optimistic update (confirmed).

## Task
1. Complete FavoriteButton.tsx with TanStack Query optimistic mutation
2. Add toggle animation
3. Add to detail page
4. Write 2 unit tests for the Action

When finished: openclaw system event --text "Done: favorites frontend" --mode now
```

## ACP Fallback: Direct Execution

When ACP is unavailable, the agent does it directly. Example thought process:

```
ACP spawn failed (timeout after 60s).
Task: Add email field to UserProfile.

Fallback plan:
1. read app/Models/User.php → check existing fields
2. read database/migrations/ → find latest migration
3. write new migration: add email column
4. edit app/Models/User.php → add to fillable
5. edit resources/js/Pages/UserProfile.tsx → add email input
6. exec "php artisan migrate" → apply
7. exec "php artisan test" → verify

Recording (skip if unavailable): node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js learn --action "ACP timeout, completed directly" --context "myapp" --outcome negative --insight "ACP was slow, 3-file task done directly in 2 minutes" 2>/dev/null || true
```

## Parallel Spawn Template

```bash
# Write shared context once
# → <project>/.openclaw/context-feat-dashboard.md

# Spawn parallel (both read same context file)
sessions_spawn(runtime: "acp", task: "Read .openclaw/context-feat-dashboard.md. Build DashboardChart React component...", cwd: "<project>", mode: "run")
sessions_spawn(runtime: "acp", task: "Read .openclaw/context-feat-dashboard.md. Build /api/dashboard endpoint...", cwd: "<project>", mode: "run")

# Wait for both, then review
```
