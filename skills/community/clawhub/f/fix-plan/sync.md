# Sync

GitHub PR/Issue state polling. Reads `[ ]` items in fix_plan, finds PR/Issue number references, queries GitHub, and auto-checks `[x]` on MERGED PRs and CLOSED issues. PRs CLOSED-without-merge convert to `[BLOCKED:P2:external]` — see the rules table below.

## When to use

- Routine fix_plan housekeeping (run before [move](./move.md) to catch newly-merged work)
- Explicit `/fix-plan sync` invocation
- Stop-hook driven supervisor checks ("any PR merged since last loop?")

## Procedure

### 1. Extract PR/Issue numbers from `[ ]` items

Grep fix_plan for `PR #N`, `Issue #N`, or bare `#N` near a known issue/PR keyword. For each match, capture the number.

### 2. Query GitHub state

For each captured number:

```bash
gh pr view <N> --json state,mergedAt -q '{state: .state, mergedAt: .mergedAt}'
gh issue view <N> --json state,closedAt -q '{state: .state, closedAt: .closedAt}'
```

(Try `gh pr view` first; on "not found" fall back to `gh issue view`. Both error → skip the entry.)

### 3. Auto-check rules

| GitHub state | fix_plan action |
|--------------|-----------------|
| PR `MERGED` | `[ ]` → `[x]` + timestamp from `mergedAt` |
| Issue `CLOSED` | `[ ]` → `[x]` + timestamp from `closedAt` |
| PR `OPEN` / Issue `OPEN` | No change |
| PR `CLOSED` without merge | `[ ]` → `[BLOCKED:P2:external]` with reason note "PR closed without merge — needs decision" |

### 4. Timestamp format

Use the same format as [format.md](./format.md) item state changes: `(YYYY-MM-DD HH:mm completed: sync)`. The `sync` keyword indicates this state change came from automated GitHub polling rather than a session-driven completion.

### 5. Chain into move

Items just synced to `[x]` are immediate candidates for the next [move](./move.md) cycle. The recommended sequence is `sync` → `move` so the freshly-merged items roll into Completed in the same pass.

## Sync-specific prohibitions

| # | Don't | Do |
|---|-------|-----|
| 1 | Auto-`[x]` an `OPEN` PR / Issue | Only act on MERGED / CLOSED state |
| 2 | On GitHub API error, mark the item BLOCKED | Do not change the item's state on uncertain input; include the API error as a separate line in the sync report so the user can see what failed |
| 3 | Run sync without reporting how many items changed | Report changed-item count to the user. Zero changes → "no changes" |
| 4 | Re-sync items already `[x]` | Sync only operates on `[ ]` entries |

## Report format

```text
Sync result:
- 3 items auto-`[x]` (PR #41 MERGED, PR #44 MERGED, Issue #23 CLOSED)
- 1 item converted to BLOCKED (PR #38 closed without merge)
- 2 items unchanged (PR #45 OPEN, PR #47 OPEN)
```

## See also

- [github-flow](../github-flow/) (depends-on) — `gh` CLI conventions
- [format.md](./format.md) — marker semantics
- [move.md](./move.md) — chain target for `[x]` entries produced here
