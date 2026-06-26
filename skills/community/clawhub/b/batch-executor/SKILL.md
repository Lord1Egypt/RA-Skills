---
name: batch-executor
version: 1.0.0
description: Full batch processor for corpus-scale task execution. Handles Google Drive dumps, ChatGPT exports, Apple Notes, or any large collection of mixed content (ideas + instructions + references + noise). Classifies items, spawns sub-agents for heavy work, checkpoints progress, and never loses input. Option C of the task management system. Use for 20+ items or when input is a file/folder dump rather than a chat message.
---

# Batch Executor

Corpus-scale processing: classify → prioritize → spawn → checkpoint → reconcile.

Unlike task-extractor (for 3-12 inline tasks) or batch-cognition (for idea analysis), this skill EXECUTES at scale with sub-agent parallelism.

## When to Use

- Google Drive folder dump (mixed docs, notes, spreadsheets)
- ChatGPT conversation export (3K+ prompts)
- Apple Notes dump (years of ideas)
- Any input > 20 items or > 10K tokens of raw content
- File-based input (not inline chat messages — use task-extractor for those)

## Architecture

```
INPUT (any scale)
    ↓
PHASE 1: INGEST — save raw to disk, never lose
    ↓
PHASE 2: CLASSIFY — type each item, estimate effort
    ↓
PHASE 3: TRIAGE — score by value, group by dependency
    ↓
PHASE 4: EXECUTE — spawn sub-agents (max 3 concurrent)
    ↓
PHASE 5: RECONCILE — verify completions, retry failures
    ↓
PHASE 6: REPORT — value stack, patterns, action items
```

## Phase 1: INGEST

Save ALL raw input to `systems/batch-executor/corpus/YYYY-MM-DD-SOURCE.md` BEFORE any processing.

For file inputs:
- PDF → extract text via `pdf` tool
- CSV/JSON → parse, one item per row/object
- Markdown → split on `## ` headers or `---` separators
- ChatGPT export → parse `conversations.json`, group by chain_id
- Google Drive → process each file, flatten into items

Create the manifest:
```markdown
# Corpus Manifest: [source] [date]
# Total items: [N]
# Raw file: [path]
# Status: INGESTED

| # | First 80 chars | Type | Effort | Status |
|---|---------------|------|--------|--------|
| 1 | ... | ? | ? | INGESTED |
```

## Phase 2: CLASSIFY

For each item, assign:

| Type | Description | Action |
|------|-------------|--------|
| TASK | Has a clear action verb + deliverable | EXECUTE |
| IDEA | Speculative, "what if", product concept | SCORE (ICE) |
| REFERENCE | Link, citation, spec, documentation | CATALOG |
| DECISION | "We decided X", "going with Y" | RECORD |
| HALF_THOUGHT | Fragment, incomplete, trails off | COMPLETE then re-classify |
| MODEL_OUTPUT | AI-generated, assistant voice | EXTRACT core idea, discard wrapper |
| DUPLICATE | Same as item #X | MERGE |
| NOISE | Test, filler, meta-commentary | SKIP |

Effort per item:
- **TRIVIAL** (< 1 min): file rename, note capture, config change
- **QUICK** (1-5 min): web search, small edit, API call
- **MEDIUM** (5-30 min): build a page, write a doc, research topic
- **HEAVY** (30+ min): full app build, deep research, multi-step workflow
- **BLOCKED**: needs human input, credentials, or external dependency

Update manifest with Type + Effort columns.

## Phase 3: TRIAGE

Score each TASK and IDEA using quick ICE:
- **I (Impact)**: 1-5 — how much does this move the needle?
- **C (Cost)**: 1-5 — how cheap/fast to do? (inverted: 5 = trivial)
- **E (Exploit)**: 1-5 — how quickly does this produce value?
- **Score** = I × C × E (max 125)

Sort by score descending. Group by dependency chains.

Create execution plan:
```markdown
# Execution Plan

## Wave 1 (parallel, no dependencies)
- Item #14 (ICE: 100) — HEAVY → sub-agent
- Item #3 (ICE: 80) — MEDIUM → sub-agent
- Item #7 (ICE: 75) — QUICK → inline

## Wave 2 (depends on Wave 1)
- Item #9 (depends on #14) — MEDIUM → after #14 completes

## Skip (NOISE/DUPLICATE)
- Items #2, #5, #11 — reason: [...]

## Blocked (needs human)
- Item #8 — needs API key from Ryan
```

## Phase 4: EXECUTE

Rules:
1. **Max 3 sub-agents concurrent.** Wait for one to complete before spawning another.
2. **QUICK items: execute inline** (no sub-agent overhead for < 5 min tasks).
3. **MEDIUM/HEAVY items: spawn sub-agent** with clear task description + acceptance criteria.
4. **Each sub-agent gets**: the item content, relevant context from other items, and the target artifact path.
5. **Track in manifest**: status → EXECUTING, then ✅ DONE / ❌ FAILED / ⚠️ PARTIAL.

Sub-agent spawn template:
```
Task: [item summary]
Context: [relevant items from this corpus]
Deliverable: [specific file/artifact expected]
Acceptance: [how to verify it's done]
Workspace: [path]
```

Checkpoint every 5 completed items:
- Update manifest
- Report to user: "[X]/[N] done. [Y] in progress. Top findings so far: [...]"
- If user is idle (no response in 30s), continue
- Commit progress to git

## Phase 5: RECONCILE

After all waves complete (or all sub-agents return):
1. Re-read manifest
2. For each ❌ FAILED: log reason, decide retry or escalate
3. For each 🔄 sub-agent still running: check status, kill if stale (> 30 min no progress)
4. For each ⚠️ PARTIAL: note what's left
5. Retry failed items once (different approach if possible)

## Phase 6: REPORT

Generate final report at `systems/batch-executor/reports/YYYY-MM-DD-SOURCE-report.md`:

```markdown
# Corpus Report: [source]
# Processed: [date]
# Total: [N] items
# Results: [done] ✅ | [failed] ❌ | [partial] ⚠️ | [skipped] ⏭️ | [blocked] 🔒

## Value Stack (top items by impact)
1. [item] — [outcome] — [next step]
2. ...

## Patterns Discovered
- [theme or connection across items]

## Action Items (immediate)
- [ ] [task from corpus that needs follow-up]

## Parked (valuable but not now)
- [item] — reason: [why later]

## Blocked (needs human)
- [item] — needs: [what]

## Statistics
- Items by type: TASK [x], IDEA [x], REFERENCE [x], NOISE [x]
- Items by effort: TRIVIAL [x], QUICK [x], MEDIUM [x], HEAVY [x]
- Sub-agents spawned: [x]
- Total execution time: [x min]
```

Append to `systems/batch-cognition/value-stack.md` (shared with batch-cognition skill).
Log learnings to `.learnings/LEARNINGS.md`.

## Commands

`status` — show manifest progress
`pause` — stop spawning, let running agents finish
`resume` — continue from where we left off (re-read manifest)
`skip [#]` — skip item number
`retry [#]` — retry failed item
`block [#] [reason]` — mark as blocked
`priority [#]` — move item to top of queue
`done` — trigger report even if items remain

## Key Rules

1. **INGEST FIRST.** Raw content hits disk before ANY processing.
2. **Max 3 concurrent sub-agents.** More = chaos, dropped results, context confusion.
3. **Checkpoint every 5.** Git commit progress. User update.
4. **Never mark ✅ without artifact evidence.** File exists, build passes, URL responds.
5. **NOISE is not failure.** Skipping noise is correct behavior. Report it transparently.
6. **Corpus items cross-reference.** Item #14 may be context for item #27. Pass relevant context to sub-agents.
7. **Resume is first-class.** If session dies, `resume` re-reads manifest and continues from last checkpoint.
8. **ICE scoring is fast.** 30 seconds per item max. Don't overthink triage — execute.

## Integration with Other Skills

- **task-extractor**: For inline chat messages (3-12 items). Batch-executor is for file/corpus scale (20+).
- **batch-cognition**: For idea analysis (THINK-heavy). Batch-executor is for execution (PLAY-heavy).
- **orchestrator**: Batch-executor can be invoked BY the orchestrator when it detects a corpus dump.
- **recorder**: After batch-executor completes, route to recorder to update STATUS.md.
