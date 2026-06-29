# Format

Schema and structure for `fix_plan.md` / `checklist.md` files. Section layout, item-marker syntax, state-change conventions, section-consistency check, default execution flow, forbidden actions.

## File structure

```markdown
# Fix Plan

## Progress

- [ ] Pending item description
  - Sub-step or status note

- [x] Completed item (not yet moved to Completed)
  - Detailed log…

## Completed

- 2026-06-07 12:00 — One-line summary (PR #N, Session xxxxxxxx)

---

## Notes

- Project-specific rules
```

Top-level sections:

| Section | Purpose | Behavior |
|---------|---------|----------|
| `## Progress` | Active and recently-completed items | Always present. Never empty — if no items, keep `(none)` placeholder |
| `## Completed` | Historical one-line summaries | Append-only chronological. New entries inserted at sort position |
| `## Hold` (optional) | External-response BLOCKED items separate from active Progress | Used when Progress would otherwise be cluttered with un-actionable items |
| `## Notes` | Project conventions, project-specific guard rails | Not modified by this skill |

## Marker syntax

| Marker | Meaning | Where allowed |
|--------|---------|---------------|
| `- [ ]` | Pending | `## Progress`, `## Hold` |
| `- [x]` | Completed (pending move to Completed) | `## Progress` |
| `- [BLOCKED]` | Skipped by Ralph autonomous loop (human resolution needed) | `## Progress`, `## Hold` |
| `- [BLOCKED:P0-P3:reason]` | Priority-annotated BLOCKED (see [priority.md](./priority.md)) | `## Progress`, `## Hold` |
| `-` followed by space, no checkbox | Already-summarised historical line | `## Completed` only |
| `- [REPEAT]` | Persistent recurring item (Ralph-specific — see ralph/periodic.md) | `## REPEAT` section only (out of scope for this skill) |

## Item state changes

When an item completes, change `- [ ]` → `- [x]` and append session ID + timestamp to the title line.

Format: `(YYYY-MM-DD HH:mm completed: Session xxxxxxxx, commit <hash>)` or for merged PRs: `(YYYY-MM-DD HH:mm completed: Session xxxxxxxx, PR #N)`.

- Session ID: first 8 chars from `.ralph/.claude_session_id` (Ralph environment) or current session ID
- Timestamp: 24-hour `YYYY-MM-DD HH:mm` of the completion moment
- Add `**complete**` markers to inner sub-steps where useful

## Section-consistency check (HARD STOP)

When editing a fix_plan item, the post-edit state must match the section's meaning. Item state and section semantics drift apart if items are edited in-place across status transitions.

| # | Don't | Do |
|---|-------|-----|
| 1 | In-place edit a BLOCKED item in the Hold section into an active item without moving it back to Progress | When BLOCKED is resolved, **delete** the item from Hold and **insert** it into Progress as an active `- [ ]` (or `[x]` if already done) |
| 2 | Change item content without checking which section it's in | Before Edit, grep for `^##` to identify the item's parent section; verify the new content matches that section's semantics |

Self-check before Edit:

1. Which section (`## Progress` / `## Hold` / `## Completed`) does the target item live in?
2. Does the post-edit state (active / blocked / completed) match the section?
3. If not, move the item to the right section in the same edit

## Default execution flow

When this skill's main entry point is invoked, run these four steps in order:

1. **Sync** — call [sync](./sync.md) to poll GitHub state for `[ ]` items containing `PR #N` / `#N`: auto-`[x]` on MERGED PRs and CLOSED issues; PRs CLOSED-without-merge convert to `[BLOCKED:P2:external]` per the sync contract
2. **Move completed** — apply [move](./move.md) to relocate `[x]` items with no follow-up notes into the Completed section as one-line summaries
3. **External RAG dispatch (optional)** — if the caller supplied `--rag=<skill>:<topic>`, dispatch Completed entries to the receiver for semantic indexing
4. **Add new items** — if the user instructed new work, append `- [ ]` items per [add](./add.md) authoring rules

Order matters: sync first (state truth) → move (clean up Progress) → optional dispatch → add (new work). Reordering breaks the truth-then-cleanup-then-grow chain.

## Recording-topic ask-skip (HARD STOP)

This skill is a **recording / management** skill. After completing add / move / state-change operations, do not autonomously trigger a next-action AskUserQuestion proposing follow-up workflows.

Why:

- `/fix-plan <topic>` invocation intent = state change in the tracker file only. Follow-up workflow entry is a separate user instruction
- Topic-end autonomous next-action ask → user picks an option → unintended workflow auto-enters against the user's actual intent
- AskUserQuestion is for genuine user-decision branching. Simple recording-topic completion is not a branch point

| # | Don't | Do |
|---|-------|-----|
| 1 | After recording completes, call the `next` skill → present "/code-workflow entry?" ask | Report recording completion only. Wait for explicit user follow-up instruction |
| 2 | "Should I proceed with the highest-priority item recorded?" auto-proposal | Wait until the user instructs the next task. No autonomous priority judgement |
| 3 | "Should I handle deliverables (plan authoring, issue registration, …)?" follow-up ask | Deliverable handling = a separate topic/skill invocation. Wait for explicit user instruction |
| 4 | When Stop hook auto-triggers `next`, unconditionally call AskUserQuestion | Even if `next` is entered, if it's right after a recording-topic completion, skip the ask (per `next` skill's recording-topic ask-skip rule) |

Self-check after every topic completion:

1. Was the user message recording-intent only? If yes, autonomous ask is forbidden
2. Did the user explicitly express follow-up intent (e.g. "record then proceed with X")? If no, just report
3. Does the response end with "Should I enter /X?" If yes, it's a violation — remove and end the report

Exceptions:

- User explicitly expressed follow-up intent — ask allowed
- BLOCKED item resolution requires user decision — separate ask allowed

## Forbidden actions

- Do not empty the `## Progress` section — always keep `(none)` or actual items
- Do not arbitrarily delete or modify existing entries in `## Completed`
- Do not touch the `## Notes` section
- **Do not add AI behavior constraints (e.g. version-change prohibitions, test-bypass prohibitions) to this file or to `fix_plan.md`** — these belong in `.ralph/PROMPT.md` (Ralph environment) or `~/.agents/rules/*.md` (global). `fix_plan.md` is a **task list + completion-log artefact only**

## See also

- [priority.md](./priority.md) — `[BLOCKED:P0-P3:reason]` annotation convention
- [add.md](./add.md) — new item authoring schema
- [move.md](./move.md) — `[x]` → Completed summary rules + subtree-move
- [sync.md](./sync.md) — GitHub PR/Issue state polling
- [issue-drafts.md](./issue-drafts.md) — draft file lifecycle
