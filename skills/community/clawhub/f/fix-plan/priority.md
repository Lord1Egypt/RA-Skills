# Priority — BLOCKED P0-P3 + Reason Classification

GitHub priority label-aligned BLOCKED suffix syntax and reason classification. Surfaces self-progressable items that would otherwise be buried under a blanket `[BLOCKED]` tag.

## Why

Plain `[BLOCKED]` doesn't tell you:

- How urgent the resolution is — is this blocking everything (P0) or merely nice-to-have (P3)?
- Whether the item actually requires an external response, or whether it could be done right now if someone picked it up (the "self-progressable" case)

Without these axes, triage becomes guesswork. `selfable` items get treated like blocked ones and sit untouched.

## Syntax

```markdown
- [BLOCKED:P0]                                  # Priority only
- [BLOCKED:P0:external]                         # Priority + reason
- [BLOCKED:P0:external] PR #45 user merge       # Full example
- [BLOCKED:P1:selfable] consolidate Step 2.4 PR create (branch + body ready)
- [BLOCKED:P2:external] Reviewer response on PR #43 Important 1-2
- [BLOCKED:P3:external] Optional nitpick clarification (low value)
```

Suffix format: `[BLOCKED:<priority>]` or `[BLOCKED:<priority>:<reason>]`.

## Priority scale — GitHub-aligned (P0 highest)

| Priority | Meaning | GitHub label analog |
|----------|---------|---------------------|
| **P0** | Highest — blocks all other work | `priority:0`, `priority/P0`, `critical` |
| **P1** | High — should resolve this session/cycle | `priority:1`, `priority/P1` |
| **P2** | Medium — next session is OK | `priority:2`, `priority/P2` |
| **P3** | Low — optional / nice-to-have | `priority:3`, `priority/P3` |

GitHub's priority labelling convention starts at P0 (not P1). Align with that — typing `P1` as your highest priority will collide with `priority:1` on issue boards.

| # | Don't | Do |
|---|-------|-----|
| 1 | Use P1 / P2 / P3 numbering (starts at 1) | Use **P0 / P1 / P2 / P3** — GitHub convention starts at P0. `priority:0` is your highest label |

## Reason classification (HARD STOP)

The reason distinguishes true blockers from items that look blocked but are actually progressable now. Without this, P0 selfable items get filed alongside external waits and forgotten.

| Reason | Meaning | Action |
|--------|---------|--------|
| `external` | True external dependency — user decision, bot response, CI completion, teammate input | Cannot proceed without the external response |
| `selfable` | Marked BLOCKED but progressable now — branch + body ready, refactor available, pure code work | Should be processed in the next P-ranked work cycle; **not actually blocked** |

| # | Don't | Do |
|---|-------|-----|
| 1 | Tag every wait-state as `[BLOCKED]` without a reason | Always annotate `:external` or `:selfable` — `selfable` items get P-ranked into immediate work |
| 2 | Assign P0 to a `:selfable` item to "remind myself it's easy" | P0 = blocker for all other work. `:selfable` means do it now anyway — the P-rank is for ordering, not for hiding it |
| 3 | Omit the reason on `:external` | Always include the reason on new `[BLOCKED]` items. Reasonless items can't be triaged |
| 4 | Treat `:selfable` as a permanent classification | Reclassify on every triage — once the item is in flight, it's no longer BLOCKED |

## Triage workflow

When the user asks "extract priority from BLOCKED" or "pick what to do next":

0. **Sync external state FIRST (HARD STOP)** — before scanning, invoke the [sync](./sync.md) topic on every `[BLOCKED]` / `[ ]` / `[x]` entry that references a PR / Issue / CI run. `gh pr view <N> --json state,mergedAt` + `gh issue view <N> --json state,closedAt`. MERGED PR / CLOSED issue → auto `[x]` (no longer BLOCKED). PR CLOSED-without-merge → re-tag `[BLOCKED:P2:external]`. **Without this step, triage classifies stale state** — items whose external dependency already resolved still show up as `[BLOCKED]` and get sorted as if they were live blockers
1. **Scan** the remaining `[BLOCKED]` entries (post-sync) in fix_plan.md / checklist.md
2. **Extract** the `:P*` and `:reason` suffix from each. If missing, propose adding (do not auto-fill — the user may want different values)
3. **Sort** in this order:
   1. P0 `:selfable` (immediate action — actually doable now)
   2. P0 `:external` (highest-stakes external wait — escalate the response)
   3. P1 `:selfable`
   4. P1 `:external`
   5. P2 `:selfable`
   6. P2 `:external`
   7. P3 `:selfable`
   8. P3 `:external`
4. **Report** the top-3 candidates suitable for immediate action — typically P0 + P1 `:selfable`. Surface the priority + reason in the report so the user can override

### Don't / Do — stale state classification (HARD STOP)

| # | Don't | Do |
|---|-------|-----|
| 1 | Classify a `[BLOCKED]` / `[ ]` entry referencing a PR/Issue without running `gh pr view` / `gh issue view` first | Step 0: sync external state. MERGED PR → `[x]` (Completed), not `[BLOCKED]` |
| 2 | "Item text says 'awaiting user merge' so it's still BLOCKED" — trusting tracker text over external state | Tracker text is a snapshot from when the item was authored. External state polling = primary source. Tracker stale ≠ item still blocked |
| 3 | "PR #N user merge decision" stays `[BLOCKED:P1:external]` for days/weeks after merge because no one ran sync | Every triage run starts with sync. The same item that triages as `P1:external` today should be `[x]` and harvestable to Completed by the next triage, not perpetually re-listed |
| 4 | Report sorted output without noting which entries were auto-checked by sync this run | Step 4 report must surface "N entries auto-resolved via sync (PR #X MERGED, Issue #Y CLOSED)" alongside the remaining live BLOCKERs |

## Self-check when adding a `[BLOCKED]` tag

1. Is this item truly blocked, or is it `:selfable`? — If selfable, P-rank it for immediate action instead of stashing it
2. What's the priority axis: blocker-for-others (P0), session blocker (P1), next-session (P2), nice-to-have (P3)?
3. Does the reason annotation match? — `:external` if waiting on user / bot / CI; `:selfable` if just deferred
4. Did you write the reason? — Reasonless `[BLOCKED]` annotations re-create the original problem

## Self-check when running Triage (HARD STOP — before reporting sorted output)

1. Did Step 0 sync run on every entry that references a `#NN` (PR/Issue) or CI run? — If no, abort + run sync
2. Did sync produce any auto-resolutions (`[x]`) this run? — If yes, those entries leave the BLOCKED list (do not include them in sorted output)
3. Are any items in the sorted output > 7 days old without sync verification? — Mark them with the date of last sync; consider them suspect until re-synced
4. Did the report surface "N entries auto-resolved" before listing live BLOCKERs? — Without that line, the user cannot tell whether triage actually checked external state

## Compatibility

The plain `[BLOCKED]` form remains valid (no priority, no reason) — readers/parsers must treat it as `:P2:external` by default. New items should adopt the suffixed form; back-fill of existing entries is at the user's discretion.

Ralph's autonomous loop continues to skip `[BLOCKED]` regardless of suffix — the suffix is for human triage, not loop control.

### Plan Drafts (`## Plan Drafts` section)

Entries in `## Plan Drafts` are **always** `[BLOCKED:P*:selfable]`, never `[ ]` — see [draft.md](./draft.md) for the rationale. The marker pieces decompose as:

| Piece | Plan Drafts value | Why |
|-------|-------------------|-----|
| `[BLOCKED]` | always | Promote requires a user decision; autonomous loops must skip |
| `:P*` | `P0`-`P3`, default `P2` | Ranks promote urgency relative to other drafts |
| `:selfable` | always | Body file / stub is prepared; wait-state is on a user signal, not on a third party. `:external` is reserved for items in `## Progress` waiting on real third-party dependencies |

Default when uncertain: `[BLOCKED:P2:selfable]`.

## See also

- [format.md](./format.md) — marker syntax and section semantics
- [add.md](./add.md) — authoring schema
- [draft.md](./draft.md) — Plan Drafts section uses `[BLOCKED:P*:selfable]` exclusively
- Ralph autonomous-loop integration (when a Ralph wrapper is in use): the wrapper skips `[BLOCKED]` items regardless of the `:P*:reason` suffix — the suffix is for human triage, not loop control
