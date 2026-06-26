---
name: consolidate
depends-on:
  - git-repo
  - github-flow
  - superpowers
metadata:
  author: es6kr
  version: "0.3.1" # x-release-please-version
description: >-
  Consolidate and respond to external feedback on PRs/issues. Topics —
  pr (workflow entrypoint + skip conditions),
  collect (gather AI reviews + superpowers load),
  internal (Internal Code Review fallback + UI capture),
  classify (dual-label Type|Severity + diff scope check),
  decide (user decision: findings + Formal Review),
  post (Summary + Formal Review + status + deferred),
  next (post-summary next-action ask).
  Use when: "review consolidate", "PR review", "AI review", "CodeRabbit review", "Copilot review",
  "review check", "review summary", "merge ready", "internal review", "code-reviewer",
  "inline review", "line-level comment", "PR line review".
allowed-tools: [Agent, AskUserQuestion, Bash, Edit, Glob, Grep, Read, Write]
---

# Consolidate

Consolidate and respond to external feedback on PRs and issues.

## Options

| Flag | Default | Behavior |
|------|---------|----------|
| `--interactive` | off | Before each POST (Internal Review at Step 3.5.3 / Summary at Step 7), pause and `AskUserQuestion` the drafted body to the user. User can approve, request edits, or reject. Edits applied → re-ask. Reject → abort POST for that artifact. |

### Auto-activation by args keywords (HARD STOP)

When the consolidate caller passes args containing any of the following intent classes (any language — match by meaning, not literal token), **treat `--interactive` as implicitly set** even if the flag was not literal. The keyword expresses the user's intent for review-before-post.

| Intent class | Match signal |
|--------------|--------------|
| Explicit review request | Phrases requesting review of the draft before publishing — "review first", "review before post", "review the draft", localized equivalents (e.g., the Korean phrase meaning "review needed" / "after review") |
| Interactive mode request | Words like `interactive` (any language transliteration), or phrases meaning "conversational mode" / "step-by-step ask" |
| "Important decision ask" intent | Phrases stating that important decisions / important parts must be asked — e.g., "ask important parts", "ask the key decisions", localized equivalents |
| Author-style review request | Phrases stating the user wants to see / review the artifact themselves — "let me review", "let me see the draft", "after I check" |

When auto-activation fires, the caller MUST emit a one-line acknowledgement in chat before the first ask:

```
Interactive mode auto-activated by caller args (intent: <intent class>) — drafts will be reviewed before POST.
```

| # | Don't | Do |
|---|-------|-----|
| 1 | Treat args keyword as flavor text and continue deterministic POST | Match against the intent-class table above. On any match, enable `--interactive` for the entire workflow |
| 2 | Activate interactive only for the matched step (e.g., only the Summary) | Once activated, applies to ALL POST steps in this consolidate run (Internal Review + Summary + any inline edits). One match → all-step gating |
| 3 | Silent activation without chat acknowledgement | Emit the one-liner above so the user can confirm the intent was caught |
| 4 | Map "important decision ask" only to scope-decision axes (Step 5 Axis B / Step 8 next-action) | Body content of Internal Review / Summary is an "important decision" too — every POSTed artifact is subject to review-before-post |

### Interactive flow contract

When `--interactive` is on (literal or auto-activated), each artifact POST follows this contract:

1. **Draft** — author the body into `.tmp/<artifact>-draft.md` (per `file-operations.md` `.tmp/` policy)
2. **Present** — emit a chat summary of the draft (key sections, finding count, verdict line) + the `.tmp/` path
3. **Ask** — `AskUserQuestion` with options:
   - `Approve as-is` — POST immediately
   - `Edit (specify in Other)` — capture user edits → apply via Edit → re-present → re-ask
   - `Reject — do not POST` — skip POST for this artifact, record skip reason in chat
4. **POST** — only after Approve. Use existing medium decision (deterministic) for the POST mechanics.

### Edge cases

- **Already POSTed before interactive auto-activation realized**: see post.md "Damage control — Summary already posted in wrong medium" — content can be PATCHed in place. After `--interactive` auto-detection mid-flow, the caller asks the user whether to PATCH the already-posted artifacts with reviewed content.
- **Multiple artifacts in one consolidate run** (Internal Review + Summary): ask each separately; do not bundle the two drafts into one ask.
- **`--interactive` + `--inline` together**: inline annotation bodies are part of the Internal Review draft; review them in the same ask.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| classify | Step 4 Analyze and Classify (dual-label Type \| Severity, PR scope cross-check) | [classify.md](./classify.md) |
| collect | Step 3 Collect AI Reviews + Step 3.6 superpowers framework load | [collect.md](./collect.md) |
| decide | Step 5 User Decision (Axis A/B) + Step 6 Fix or Reject | [decide.md](./decide.md) |
| internal | Step 3.5 Internal Code Review Fallback (medium: review POST w/ inline when line-specific findings exist, else issue comment) + Step 4.5 UI capture verification | [internal.md](./internal.md) |
| next | Step 8 Post-Summary Next-Action Ask | [next.md](./next.md) |
| post | Step 7 Post Summary + Formal Review (unified vs separate) + Step 7.5 Status + Step 7.6 Deferred registration | [post.md](./post.md) |
| pr | Workflow entrypoint — PR identify, skip conditions, Copilot availability pre-check (auto-fallback, no ask), Copilot sequential, worktree checkout, Rules | [pr.md](./pr.md) |

## Topic Dependencies

```
pr (entry: identify → skip → worktree checkout)
  └─→ git-repo/worktree (Step 2.7: check out PR branch into a worktree — all review runs against real files)
collect → internal (code-reviewer dispatch operates in the Step 2.7 worktree)
```

- Step 2.7 worktree checkout runs on every review (after skip conditions) so the code-reviewer reads real files, CONFLICTING is detected locally, and inline line numbers match HEAD.

## Quick Reference

### PR Review Workflow

Review CodeRabbit/Copilot feedback on a PR, decide what to act on, and post an AI Review Summary comment.

Entry: [`pr.md`](./pr.md) (Workflow index + Step 1, 2, 2.4, 2.5, 2.6, 2.7 + Rules)

Step execution order:
1. **`pr.md`** Step 1 (Identify PR) + Step 2 (Skip Conditions) + **Step 2.4 (Copilot availability pre-check — auto-fallback to Internal Review on unavailable, no ask)** + Step 2.5 (Copilot sequential, multi-PR only — skipped on unavailable) + Step 2.6 (re-review trigger policy — first vs re-review) + Step 2.7 (checkout PR branch into a worktree — MANDATORY, all reviews)
2. **`collect.md`** Step 3 (Collect AI Reviews) + Step 3.6 (superpowers framework)
3. **`internal.md`** Step 3.5 (Internal Review Fallback, walkthrough only / on failure — medium decision: inline targets (Critical+Important line-specific; `--inline` = all) → single review POST (body = findings + comments[] = inline, re-review = new POST); no inline targets → issue comment (re-review = PATCH)) + Step 4.5 (UI capture verification)
4. **`classify.md`** Step 4 (Analyze and Classify)
5. **`decide.md`** Step 5 (Formal Review Decision — Axis B only) + Step 6 (Fix or Reject — only on explicit user instruction)
6. **`post.md`** Step 7 (Post Summary + Formal Review) + Step 7.5 (Status line) + Step 7.6 (Deferred registration)
7. **`next.md`** Step 8 (Post-Summary Next-Action Ask)
