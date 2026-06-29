# Draft

Records a **lightweight plan stub** when a piece of work needs planning but full planning is being **deferred**. Captures just enough to resume later, without doing the research → plan work now.

Invoked as `/fix-plan draft ...` (short keyword). The descriptive concept is "deferred plan draft", but the call stays short.

## When to Use

- A task surfaces that clearly needs a real plan (research + design), but you are deferring it — not now.
- You want the deferred intent **tracked** so it does not vanish from chat / the next session.
- Use for "defer this plan", "draft stub", "record plan draft", "plan-draft", "park this for later".

**Not for**: items ready to act on now (use `add`), or items blocked on an external dependency (use `priority` `[BLOCKED]`). Draft = "needs planning, deliberately postponed", not "blocked".

## Section + entry schema

Plan-draft stubs live in a dedicated `## Plan Drafts` section of the tracker (`fix_plan.md` / `checklist.md`), parallel to `## Issue Drafts`.

```markdown
## Plan Drafts

- [BLOCKED:P2:selfable] {Purpose — one line: what the eventual plan is for}
  - **Defer reason**: {why it is postponed (priority, missing input, scope unclear, …)}
  - **Resume trigger**: {when / what condition should promote this to a real plan}
  - **Expected deliverable**: research | plan | checklist
```

### Why `[BLOCKED]` (not `[ ]`)

Plan-draft entries are **always** `[BLOCKED]`. A draft represents work the user has deliberately deferred — promote requires a user decision, which an autonomous agent cannot make on its own. Marking the entry `[ ]` would let autonomous loops (e.g. Ralph) pick it up and try to act on it, contradicting the "deferred until trigger fires" semantics.

The reason is **always** `:selfable` because the body file (or inline stub) is prepared — the wait-state is on a user signal to promote, not on an external third party. Priority (`P0`-`P3`) ranks promote urgency relative to other drafts. See [priority.md](./priority.md) for the priority scale and triage workflow.

Default when uncertain: `[BLOCKED:P2:selfable]` (next-session promote candidate).

### Minimal fields (all required, keep terse)

| Field | Purpose | Example |
|-------|---------|---------|
| Purpose (title) | One line — what the future plan accomplishes | `Abstract the qdrant integration backend` |
| Defer reason | Why not planning now | `Other work first / missing input / scope undecided` |
| Resume trigger | What promotes it to a real plan | `After current PR merges / on user request / once X is decided` |
| Expected deliverable | Which output the promote will produce | `research` / `plan` / `checklist` |

Priority + `:selfable` reason go in the marker suffix (`[BLOCKED:P*:selfable]`), not as separate fields.

A stub is intentionally **small** — purpose + 3 fields. If the draft already needs more than a few lines, it is no longer a stub; promote it.

### Three storage modes (pick before writing)

Drafts have three storage modes, not a binary stub-or-promote choice. Pick the
mode by inspecting **what context already exists at draft time**, not by guessing
future expansion.

| Mode | When to pick | Where the body lives |
|------|-------------|---------------------|
| **Inline only** (default) | No substantive research/measurement has been gathered yet. Stub captures pure intent + 3 fields | `## Plan Drafts` entry |
| **Inline + body file** | Substantive research/measurement **already exists in this session's chat** (findings, numbers, classified results, methodology fixes) that would otherwise be lost when chat is compressed | Entry cites `plan-drafts/<slug>.md`; body file holds the findings |
| **Promote** | Body would exceed a few paragraphs **and** the user has not deferred — go straight to `code-workflow` research → plan | (no draft entry — real plan artifact instead) |

The middle mode (inline + body file) mirrors `issue-drafts/`. Default is inline
only, but **escalate to body file whenever this session has already produced
research that the inline 3 fields cannot hold**. Chat content is ephemeral; the
draft body file is the persistence medium.

## Lifecycle

A plan-draft follows three stages.

| Stage | Action | Owner |
|-------|--------|-------|
| 1. Write | Add a `- [BLOCKED:P*:selfable]` entry to `## Plan Drafts` (optionally a `plan-drafts/<slug>.md` body file) | This topic, when the user defers |
| 2. Promote | When the resume trigger fires, hand the stub to the planning workflow (research → plan) and convert the entry into active work | This topic → `code-workflow` |
| 3. Archive | When a stub is superseded / abandoned, move any body file to `plan-drafts/.bak/` and remove the entry | This topic |

### 1. Write

1. Confirm the item genuinely needs a plan and is being deferred (not act-now, not external-blocked).
2. Ensure a `## Plan Drafts` section exists; create it if absent (place after `## Progress`, near `## Issue Drafts` if present).
3. Pick a priority (`P0`-`P3`) reflecting promote urgency relative to other drafts (default `P2` when uncertain). The reason is always `:selfable` for Plan Drafts — see [priority.md](./priority.md).
4. Append the entry as `- [BLOCKED:P*:selfable] {Purpose}` with the four minimal fields underneath.

### 2. Promote

When the resume trigger is met:

1. Dispatch the stub to the planning workflow: `Skill("code-workflow", "steps")` (research → plan → user review) using the stub's Purpose + Expected deliverable as the seed.
2. After the real research/plan artifact exists, **remove the stub entry** from `## Plan Drafts` (its job is done — the artifact supersedes it).
3. If a `plan-drafts/<slug>.md` body file existed, archive it: `mkdir -p plan-drafts/.bak && mv plan-drafts/<slug>.md plan-drafts/.bak/`.

### 3. Archive (superseded / abandoned)

When a draft is no longer wanted (duplicated by another plan, scope dropped):

```bash
mkdir -p plan-drafts/.bak
mv plan-drafts/<slug>.md plan-drafts/.bak/   # only if a body file exists
```

Then remove the `## Plan Drafts` entry. **Order**: archive the file first, remove the entry second (same rule as `issue-drafts` — reverse order leaves an orphan file mis-read as pending).

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Write a full research/plan document when the user defers | Record only the stub (purpose + 3 fields). Full plan is produced at promote time via `code-workflow` |
| 2 | Use a long topic name in the invocation | Call `/fix-plan draft ...` — the topic keyword stays short regardless of descriptive name |
| 3 | Put a deferred-plan item in `## Progress` as a normal `[ ]` | Deferred-needs-planning items go in `## Plan Drafts`. Act-now items go in Progress (`add`); external-blocked go to `priority` `[BLOCKED]` |
| 4 | Leave a promoted stub in `## Plan Drafts` after the real plan exists | Remove the stub on promote — the plan artifact supersedes it |
| 5 | Archive the entry before the body file | File first, entry second (orphan-file avoidance) |
| 6 | Record only the inline 3-field stub when this session has already gathered substantive research/measurements (the chat contains numbers/tables/classified findings) | **Inline + body file mode** — write the findings to `plan-drafts/<slug>.md` first, then cite the file from the entry. Inline-only here loses the research when chat is compressed |
| 7 | Use `- [ ]` for Plan Draft entries | Use `- [BLOCKED:P*:selfable]`. `[ ]` lets autonomous loops (e.g. Ralph) try to act on the entry — but a deferred plan cannot be promoted by an agent on its own. `[BLOCKED]` ensures the entry is skipped until the user signals promote |
| 8 | Use `:external` reason on Plan Draft entries | Always `:selfable`. The body file / stub is prepared — the wait-state is on a user signal, not on a third party. `:external` is reserved for true external dependencies (`priority.md`) |

## Self-check (before recording a draft)

1. Does this item need real planning (research/design), or is it act-now? → act-now uses `add`, not `draft`.
2. Is it deferred by choice, or blocked on an external dependency? → external-blocked uses `priority` `[BLOCKED:P*:external]` in `## Progress`. Plan Drafts are always `:selfable`.
3. Are all four fields (purpose, defer reason, resume trigger, expected deliverable) filled with one terse value each?
4. **Has this session already produced substantive research / measurements / findings** that the inline 3 fields cannot hold? → **Inline + body file mode** (`plan-drafts/<slug>.md`). Do not let the research die in chat. Symptom: chat contains numbers, tables, classified results, or methodology fixes that the entry omits.
5. Is the stub small **and no body to preserve**? Then inline only. If the body would still exceed a few paragraphs **and** the user has not deferred, promote via `code-workflow` instead of stubbing.
6. Have you picked a priority (`P0`-`P3`)? → Default `P2` when unsure. Marker is `[BLOCKED:P*:selfable]`, never `[ ]`.

## See also

- [add.md](./add.md) — authoring act-now items (`## Progress`)
- [priority.md](./priority.md) — `[BLOCKED]` for external-blocked items
- [issue-drafts.md](./issue-drafts.md) — parallel draft-file lifecycle
- `code-workflow` (`steps` topic) — promote target: research → plan → user review
