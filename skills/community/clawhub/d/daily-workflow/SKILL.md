---
name: daily-workflow
description: Say 开工啦 or 收工啦 and get a resumable project note written for you, so tomorrow you or another AI can pick up without re-reading everything. Use when a user asks to resume a project, save progress, record a checkpoint, end a work session, prepare a handoff, switch to a new AI session, or reconcile stale working notes. Typical triggers include 开工啦, 中段检查, 吃饭啦, 收工啦, 交接, 记一下进度, 存个档, 明天接着做, 换个 AI 继续, 上下文快满了, start work, checkpoint, wrap up, handoff, save progress, resume tomorrow, and switch to a new agent session. Reads existing project authority first, preserves dirty worktrees and governance evidence, avoids competing state files, archives rather than deletes history, and records commands, final outcomes, blockers, risks, and exact next actions without claiming unverified completion or QA acceptance.
---

# Daily Workflow / 项目记忆工作流

Version: 4.1.0

Use this skill to make work resumable. Record only the compact factual state needed by the user or next agent; do not turn project memory into a second project-management system.

Respond in the user's language. Keep machine-readable status values in English.

## Scope And Ownership

This skill owns session continuity only: orientation, checkpoint summaries, wrap-up records, and handoffs.

- `cms-project-governance` owns formal targets, Programs, Work Orders, Controller/QA decisions, and acceptance state.
- `agent-loop-engineering` owns active coding-loop evidence, stop gates, evaluation, and loop records.
- `project-lifecycle-navigator` owns lifecycle analysis and rebaseline proposals.
- `web-search-rules` owns research intake and source rules.
- `ai-workflow-os` may route here but must not create a parallel memory state.

When another system already owns a field, read and summarize it; do not overwrite it.

## Trigger And Authorization

Use this skill when the user explicitly asks to:

- start or resume work;
- save progress or create a checkpoint;
- wrap up or end work;
- prepare a handoff;
- reconcile or migrate workflow notes.

Common phrases include `开工啦`, `中段检查`, `吃饭啦`, `收工啦`, `交接`, `start work`, `checkpoint`, `wrap up`, and `handoff`.

A casual mention of one phrase is not enough when intent is ambiguous. Inspect read-only first. Persist files only when the request clearly asks to initialize or update project memory, or when an established project workflow already defines the trigger as a write command.

## Read-Only Orientation First

Before writing:

1. resolve the actual workspace and repository root, including nested repositories;
2. inspect Git branch, commit, and dirty state without modifying it;
3. locate governing files and determine current authority precedence;
4. locate product scope, entrypoints, build/test commands, and runtime surfaces relevant to the session;
5. read existing memory files and compatible aliases;
6. identify contradictions, missing evidence, and ownership conflicts.

Do not use `git reset`, `git clean`, broad deletion, or ambiguous process termination. Existing changes belong to the user unless proven otherwise.

## Choose A Memory Profile

### Existing Governance Profile

Use when project-owned governance or loop files already exist. Follow that project's names and authority. Do not create duplicate `Docs/` files merely because this skill has default templates.

### Lightweight Profile

Use only when no authoritative workflow exists and persistence is requested. Start with the smallest useful set:

```text
Docs/STATUS.md
Docs/NEXT_ACTIONS.md
```

Add files only when their information has a distinct owner:

```text
Docs/PROJECT.md       project identity and metadata
Docs/TARGET.md        Owner-confirmed target, scope, Non-Goals, success criteria
Docs/COMPLETED.md     append-only historical completion log
Docs/PENDING.md       current queue, blockers, and decisions
Docs/HANDOFF.md       standalone handoff only when requested or too large to embed
Docs/CONFIG.md        explicit local workflow preferences
Docs/archive/YYYY-MM.md
```

Do not create `TARGET.md` from an AI guess. If the target is unclear, record a proposed summary in `STATUS.md` as `TBD - Owner Confirmation Required`.

### Legacy Migration Profile

Detect legacy files read-only. If old and new forms coexist, show the conflict and ask before merging. Never delete legacy files automatically.

Compatibility mappings:

```text
PROJECT_TARGET.md  -> TARGET.md
PROJECT_STATUS.md  -> STATUS.md
COMPLETED_JOBS.md  -> COMPLETED.md
PENDING_JOBS.md    -> PENDING.md
NEXT_STEPS.md      -> NEXT_ACTIONS.md
SCHEDULE.md        -> NEXT_ACTIONS.md compatibility alias
```

## Evidence Vocabulary

Use precise states:

- `implemented`: source or artifact exists;
- `verified`: a relevant current check passed;
- `partial`: only part of the intended behavior exists;
- `unverified`: required evidence was not run or observed;
- `unusable`: present but the real user flow cannot complete;
- `documentation-conflict`: current records disagree;
- `not-executed`: a scenario was not run;
- `blocked`: progress requires authority, user input, or an unavailable dependency;
- `accepted`: only when the authorized independent acceptance role has recorded it.

Never promote Developer self-report, historical logs, a health endpoint, compilation, a narrow test, or a screenshot into broader acceptance.

For each verification record, preserve:

- exact command or manual scenario;
- relevant environment or data boundary;
- final exit, timeout, interruption, or not-executed state;
- result summary;
- evidence/artifact path when useful;
- residual risk.

## Canonical Record Structure

### STATUS.md

Keep a current snapshot plus short history:

```markdown
# Project Status

## Current State
- Status:
- Current goal:
- Active scope:
- Latest verified behavior:
- Blockers:
- Residual risks:

## Latest Verification
- Command or scenario:
- Final result:
- Evidence boundary:
- Evidence path:
- Not executed / deferred:

## Compressed Context
- User intent:
- Decisions:
- Completed since last checkpoint:
- Pending:
- Files touched:
- Dirty worktree notes:
- Exact next action:

## Update History
### YYYY-MM-DD HH:mm [start|checkpoint|wrap-up|handoff|migration]
- Factual change and evidence.
```

### NEXT_ACTIONS.md

Keep exactly one current continuation plan:

```markdown
# Next Actions

## Immediate Next Action
1. [Action with context and acceptance condition]

## Then
1. [Ordered action]

## Blockers And Owner Decisions
- [Decision or blocker]

## Handoff Snapshot
- Current state:
- Completed:
- Pending:
- Risks:
- Files/artifacts:
- Commands and final results:
- Exact next action:
```

## Start Work

1. Orient read-only.
2. Determine the memory profile and authority.
3. Summarize target, current state, latest verified evidence, dirty changes, pending work, blockers, and exact next action.
4. Reconcile stale notes against current repository/runtime evidence.
5. Write a start entry only when persistence is authorized.
6. Do not create speculative targets or mark historical completion as current verification.

## Checkpoint

1. Compress only the context required to continue.
2. Record actual completed work and current evidence.
3. Record failed, timed-out, interrupted, deferred, and unrun checks explicitly.
4. Update the current queue without dropping unresolved blockers or Owner decisions.
5. Refresh the single exact next action.
6. Preserve governance and coding-loop fields owned by other skills.

## Wrap Up

1. Record the final state observed in this session.
2. Append completed history only for work that actually occurred.
3. Keep current status aligned with the latest verified state; preserve earlier failed attempts in history with timestamps.
4. List unfinished work, blockers, residual risks, and deferred scenarios.
5. Do not change the target unless the Owner explicitly changed it.
6. Prepare a resumable next action.

## Handoff

Create a self-contained handoff that includes:

- product/architecture context necessary to continue;
- current authoritative decisions and scope;
- exact artifacts and files;
- completed work and what evidence supports it;
- unverified or not-executed scenarios;
- blockers, risks, and Owner decisions;
- commands/tests with final outcomes;
- exact next actions and prohibited actions.

Do not rely on chat history. Do not include hidden reasoning or a full transcript.

## Atomic Update Rules

When several memory files describe one state transition, update them as one coherent change and re-read them afterward. If interrupted, report which files changed and which did not.

- One current fact should have one authoritative home.
- Append historical records; rewrite current snapshots intentionally.
- Preserve unresolved blockers.
- Preserve external ownership fields such as acceptance evidence, QA decisions, loop evaluations, and `LOOP_RUNS.jsonl`.
- Archive older status entries by moving them to `Docs/archive/YYYY-MM.md`; never delete history automatically.
- Use UTF-8 for all Markdown and JSONL files.
- Report absolute paths to the user.

## Memory Bloat Control

Session memory must stay cheap enough to be read at the start of the next session.

- Keep the live memory set small: a current snapshot plus one continuation plan. Everything older moves to `Docs/archive/YYYY-MM.md`.
- Never annotate a live file with `Superseded`, `CURRENT OVERRIDE`, or `this section is void`. If the target changed, write a new `REBASELINE-<date>.md` and archive the previous one in the same pass. A reader should never have to reconstruct which layer is current.
- Do not create a new file for information that already has an owner elsewhere. Summarize and link instead.
- If the memory directory grows while verified behavior does not, report that imbalance as the checkpoint finding rather than adding another note.

## Before A Bulk Restructure

A checkpoint or handoff that precedes a rename, split, migration, or bulk deletion must first confirm a clean commit or an out-of-workspace backup exists. Record the backup location in the checkpoint. Back up first, then change code.

## Safety

Never record API keys, tokens, passwords, cookies, private keys, `.env` values, browser sessions, real personal contact data, counterparty-confidential details, full private customer records, confidential source bodies, large logs, or sensitive exploit detail. A handoff is frequently pasted into a new session, a chat, or an issue tracker, so treat it as a document that travels.

Summarize sensitive context safely and reference only an appropriate non-secret source location.

## User-Facing Summary

Keep the response compact:

```text
Project memory updated.
- Current state: Needs Fix
- Verified: 2 checks passed; browser flow not executed
- Updated: STATUS.md, NEXT_ACTIONS.md
- Preserved: active QA and loop evidence
- Blocker: Owner decision on target scope
- Next: reproduce the failing user-visible flow with the current data boundary
```
