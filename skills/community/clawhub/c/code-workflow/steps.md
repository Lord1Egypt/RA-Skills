# Steps: Research → Plan → Review → Branch

The core 4-stage procedure (Steps 0-3). Step 4 (Implement) is in [implement.md](./implement.md).

> **`output-dir`**: All research/plan files are written to the configured `output-dir` (default: `docs/generated/`). Examples below use `{output-dir}` as placeholder.

## Step 0: Resume Check (Always First)

**Must be executed first when entering code-workflow (whether new or re-entry):**

1. Check if **research/plan files** already exist in `{output-dir}` for the target task
2. **Read** the corresponding file to understand the current progress
3. If the plan has a Phase order, check **up to which Phase has been completed currently**
4. If there is an incomplete Phase, **proceed from that Phase** — do not skip to subsequent Phases (merge, deploy, etc.)

4.5. **Resume RAG re-dispatch (optional, abstract contract)**: When the caller supplied a `--rag=<skill>:<topic>` flag (see "Research/plan artifact dispatch" below), re-invoke the receiver on every existing `research-*.md` / `plan-*.md` found in Step 0 (item 1). This refreshes any indexed content that may have drifted out of sync with the file. Idempotency is the receiver's responsibility.

   When no `--rag` flag is supplied — or no compatible receiver is available in the caller's environment — skip this step. Research/plan files in `{output-dir}` remain the primary deliverable; recall is via direct `Read` / `Grep`.

   Failure policy: receiver unreachable → warning + Step 0 continues. The file artifact preservation is primary.

5. **plan-to-issue check**: If the target item has a linked GitHub issue number (`#N`), verify if the plan content has been posted to the issue body/comment. If not posted, execute `github-flow/plan-to-issue` before proceeding to the next step.

6. **GitHub repo auto-load `github-flow`** (HARD STOP):

   ```bash
   git remote get-url origin
   ```

   If the URL contains `github.com` → **`github-flow` skill is the default companion** for this code-workflow run. All issue/PR/merge operations route through `github-flow` topics:

   | Operation | github-flow topic |
   |-----------|-------------------|
   | Plan → issue body/comment | `plan-to-issue` |
   | Issue → branch | step 3b: `gh issue develop` |
   | Sequential issue chain | `dependencies` (blocked-by/blocking) |
   | PR creation | `pr` |
   | PR review consolidation | (handled by `consolidate` skill) |
   | PR merge with all gates | `merge` (CI/Review/Test Plan/blockedBy) |
   | Mid-work scope expansion | `expand` |
   | PUBLIC repo data scrub | `sanitize` |

   For non-GitHub remotes (GitLab, Bitbucket, etc.) → skip `github-flow` topics, fall back to manual `gh`/`git` commands per remote conventions.

7. **blocked-by precondition check** (GitHub repos only):

   If the target task has a linked issue with `blockedBy` dependencies, verify all predecessors are CLOSED before starting Step 1 (Research). Open predecessors mean Step 1 should pause until they resolve, OR the Resume Check should switch to a predecessor first.

   ```bash
   GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
     query { repository(owner:"<owner>", name:"<repo>") {
       issue(number:<N>) {
         blockedBy(first:10) { nodes { number state title } }
       }
     } }
   '
   ```

   See `github-flow/dependencies.md` for the full procedure.

**Prohibited**: Deciding the next action by only looking at task checklist items without reading the research/plan files. A task list is a summary; the plan file contains detailed sequences and constraints.

**Examples**:
- Even if `[ ] PR #278 merge` is in the task list, if the plan states "Phase 1 Unit Test → Phase 2 Proxy Test → ... → PR merge", start from Phase 1
- Simple items with no plan file can be proceeded immediately
- If a plan linked to issue #123 is not posted on the issue → execute `github-flow/plan-to-issue` first
- If issue #N is `blockedBy: [#M]` and #M is OPEN → switch to #M first or report BLOCKED

## Step 1: Research (Read the Codebase)

Read and understand the relevant code **deeply**, then write findings to `{output-dir}/research-<issue-number>-<task-slug>.md`.

- **Naming Rule**: Always include the GitHub issue number (e.g., `research-176-login-lock.md`). If no issue exists, use `research-<task-slug>.md`.
- Do not skim a file and move on at the signature level
- Understand existing layers, ORM relationships, and duplicate API presence
- **Mandatory exploration of existing test files**: Find related `*.test.*`, `*.spec.*` files and understand what cases are already covered
- **Web Research Policy**: When external information gathering is needed, **prioritize using a mix of CLI tools like `curl` and `context7` MCP** for fast data retrieval. Use `browser_subagent` or browser tools only as a fallback when CLI tools are insufficient (e.g., sites requiring JavaScript to render content) because browser tools are extremely slow.
- Do not summarize in chat — **always write to a file**

### Research artifact dispatch (optional, abstract contract)

The `research-*.md` file is the **primary deliverable**. After every Write/Edit, the caller may optionally dispatch the artifact to a registered receiver (any RAG index, semantic store, memory service, doc cache, etc.) for cross-session discoverability — but this generic skill does not name a vendor.

#### Flag

```text
/code-workflow ... --rag=<skill>:<topic>
```

- `<skill>` — name of a registered skill that owns a research-dispatch topic
- `<topic>` — topic within that skill responsible for accepting the artifact
- When the flag is omitted, the file write is the only deliverable. No vendor is assumed
- When the flag is supplied, dispatch fires **after every Write/Edit** completion (not at Step 1 end). Receiver handles idempotency

#### Contract for receivers (vendor skills implement this)

Caller passes artifact via env vars; receiver chooses inline or file mode:

| Mode | Env vars set by caller | Use |
|------|------------------------|-----|
| inline | `CODEWORKFLOW_RAG_FILE` (absolute path), `CODEWORKFLOW_RAG_METADATA_JSON` (serialized metadata) | Single-file dispatch with small metadata |
| file   | `CODEWORKFLOW_RAG_INPUT_JSON` (path to JSON `{file_path, metadata}`) | Bulk dispatch or when caller needs to clean up afterwards |

Receivers consult vendor-side documentation for accepted metadata keys, chunking strategy, and idempotency rules. This skill does **not** define those.

#### Skip conditions

- No `--rag` flag supplied by caller
- Caller-specified `<skill>:<topic>` not available in the current environment — fail-non-blocking: warning + Step 1 continues
- File content unchanged (receiver decides via its own idempotency)

| # | Don't | Do |
|---|-------|-----|
| 1 | Hardcode a specific RAG vendor (URL, skill name, MCP tool name) in this generic skill | Use `--rag=<skill>:<topic>` flag at the call site; vendor skill implements the receiver protocol |
| 2 | Block Step 1 on dispatch failure | Warning + continue. Artifact preservation is primary |
| 3 | Defer dispatch to Step 1 completion when the flag is supplied | When `--rag` is set, dispatch after every Write/Edit. Receiver's idempotency keeps it cheap |
| 4 | Enumerate compatible receivers inside this skill | Caller knows which receivers are available; this skill declares only the abstract surface |

**Why abstract**: research recall paths vary by environment (different RAG vendors, context7 cache, project memory, etc.). Hardcoding a vendor in this generic skill couples it to one stack. The flag keeps coupling at the call site — the caller specifies the receiver vendor at invocation time, and the receiver skill implements the actual storage / index protocol.

## Step 2: Plan (Write Plan MD)

Write a detailed implementation plan in `{output-dir}/plan-<issue-number>-<task-slug>.md`.

**File creation is DEFAULT — never an ask option (HARD STOP, 2026-05-25)**:

Per the always-on rule "target-unspecified document artifacts = file save default", writing `plan.md` is the **default action**, not a user-selectable option. AskUserQuestion options must never include "write plan as `.md` file vs chat output" as a branch.

| # | Don't | Do |
|---|-------|-----|
| 1 | Present an AskUserQuestion option like "Write plan as standalone .md file first" | Write `plan-*.md` immediately on Step 2 entry. Chat output = path + 3~5 line summary only |
| 2 | Default to chat output, ask only on user request | File write = default. Chat output for plan body = forbidden |
| 3 | Branch options around the writing medium (file vs chat vs hold) | ask only on **scope/design decisions** (e.g., "apply approach A vs B"). The medium is decided by default rule |

If the user explicitly states the medium ("just write it in chat", "show me as text"), follow that. Otherwise: file is default.

- **Naming Rule**: Use the same issue number and slug as the research file (e.g., `plan-176-login-lock.md`).

### Plan Frontmatter (MANDATORY)

Every plan file MUST start with a YAML frontmatter block containing structured tracking metadata. Inline markdown metadata (e.g., `> **Posted to**: ...` or `- Related issue: ...`) is **forbidden** — all tracking info goes in frontmatter.

```yaml
---
title: <plan title>
status: draft              # draft | review | approved | implemented | closed
relates_to: "#<N>"         # GitHub issue number (e.g., "#7"). "none" if no issue
pr: null                   # PR number when implementation PR exists (e.g., 24)
research: <filename>       # research file basename (e.g., research-7-phase3-auto-publish.md)
posted_to: null            # URL if posted as issue comment (e.g., https://github.com/.../issues/7#issuecomment-xxx)
created: <YYYY-MM-DD>      # creation date
chain: []                  # optional: issue dependency chain (see github-flow/dependencies.md)
---
```

**Field naming rules (unified convention)**:
- Use `snake_case` for multi-word fields (e.g., `relates_to`, `posted_to`)
- `relates_to` = the primary GitHub issue this plan addresses (not `related_issue` or `issue`)
- `pr` = implementation PR number (not `pull_request` or `implementation_pr`)
- `research` = basename only, not a relative path or markdown link
- `status` lifecycle: `draft` → `review` → `approved` → `implemented` → `closed`

| # | Don't | Do |
|---|-------|-----|
| 1 | Put tracking info as inline markdown (`> **Posted to**: ...`, `- Related issue: #7`) | All tracking metadata in YAML frontmatter |
| 2 | Use inconsistent field names (`related_issue`, `issue`, `target_issue`) | Use `relates_to` for the primary issue reference |
| 3 | Leave `pr` empty after implementation PR is merged | Update `pr:` and `status: implemented` after merge |
| 4 | Omit frontmatter and write a bare `# Plan:` heading | Frontmatter is mandatory — plan is incomplete without it |

The plan body starts after the frontmatter with `# Plan: [Title]` heading. The heading title should match the frontmatter `title` field.

**Mandatory sections** (Plan is incomplete if any are missing):
1. **Approach** — Detailed explanation of the chosen approach
2. **Code snippets** — Code showing actual changes
3. **Files to modify** — List of file paths to be modified
4. **Trade-offs / Alternatives** — Comparison with other approaches, reasons for selection, known limitations. Even if there is only one approach, specify "why this is the best" and "what the drawbacks are". **Undecided items = mandatory AskUserQuestion after plan write (HARD STOP, see "Plan post-write ask" below)** — do not leave blank or "TBD" lines for the user to fill in passively

   | # | Don't | Do |
   |---|-------|-----|
   | 1 | Omit trade-offs when proposing a single approach | Honestly state the strengths AND the limits/risks of the single approach |
   | 2 | Multi-alternative comparison reduced to "this one is best" hand-wave | Pros, cons, cost, risk for each alternative — clear contrast/comparison |
   | 3 | Hide security or downtime risk in a deployment plan | Mark expected risks + impact scope as Warning/Caution explicitly |

5. **Verification plan** — Verification procedures, commands/URLs, and expected results for each change group.
   - **For regression cases**: manual commands (`curl`, `ssh`) are only auxiliary. **Independently runnable test code (Python, JS, etc.)** must be authored and included in the Plan.

   | # | Don't | Do |
   |---|-------|-----|
   | 1 | List only `curl` / `ssh` commands | Author a runnable **test script** |
   | 2 | "Verify by eye" | Automated verification code or Playwright script |
   | 3 | Substitute manual commands for a regression case | Test code that reproduces + verifies the regression is required |

6. **Related issue + target** — the GitHub issue/PR number and the target location for this plan:
   - `Relates to #N` — related issue number (if none, state "new issue to be created")
   - Target location: `body update` / `comment` / `new issue body`
   - If a tracker (e.g., fix_plan) entry is referenced, specify its path
7. **Human review questions** — AI prepares answers, user validates in Step 3:
   - **Why does this code exist?** — The purpose and business context of the code being changed
   - **What changes?** — Concrete behavioral differences before vs. after this change
   - **Blast radius on failure?** — What breaks if this change is wrong, and how far the impact reaches
   - **Who owns this?** — The responsible person/team for the code being modified
8. **Progress Checklist** — A `## Progress Checklist` section with one checkbox per phase/task, enabling at-a-glance progress tracking and a pre-archive completion gate. Author it **at plan creation time** with every item unchecked (`[ ]`); flip items to `[x]` as each lands. The frontmatter `status` is lifecycle-level (coarse); this checklist is the granular per-phase tracker.

   ```markdown
   ## Progress Checklist
   - [ ] Phase 1: <task>
   - [ ] Phase 2: <task>
   - [ ] Verification: <test / URL>
   ```

   | # | Don't | Do |
   |---|-------|-----|
   | 1 | Track progress only via frontmatter `status` (lifecycle-level, coarse) | Add a granular `## Progress Checklist` — `status` is lifecycle, the checklist is per-phase |
   | 2 | Author the plan without a checklist and bolt it on later | Create the checklist with the plan (all `[ ]`); update as work lands |
   | 3 | Archive a plan with unchecked items | Pre-archive gate (see Plan Lifecycle Update): all items `[x]` + `status: implemented`/`closed` before archiving |

### Plan artifact dispatch (optional, abstract contract)

The `plan-*.md` file is the **primary deliverable**. Same abstract contract as research dispatch above — caller supplies `--rag=<skill>:<topic>` flag, this skill stays vendor-agnostic. Receiver consumes via `CODEWORKFLOW_RAG_FILE` / `CODEWORKFLOW_RAG_METADATA_JSON` env vars or `CODEWORKFLOW_RAG_INPUT_JSON` file mode.

**Order relative to "Plan post-write ask"**: **ask first → dispatch**.

1. Plan Write/Edit complete (initial `plan-*.md` write OR revision update)
2. Run Plan post-write ask (below) — resolve undecided items
3. After ask answers received, apply decisions → Edit `plan-*.md`
4. If `--rag` flag is supplied, dispatch the post-ask plan version to the receiver
5. (If subsequent Edits occur, repeat from step 2 — receiver handles idempotency)

Rationale: ask-driven Edits typically resolve the largest unresolved decisions. Dispatching after ask captures the "settled" plan rather than an in-flight state.

| # | Don't | Do |
|---|-------|-----|
| 1 | Skip dispatch for in-flight plan revisions (only dispatch "final") | When `--rag` is supplied, every Write/Edit dispatches. Receiver's idempotency handles unchanged sections |
| 2 | Block the ask on dispatch success | Dispatch happens after ask. ask is the synchronous user-blocking step; dispatch is async-safe |
| 3 | Pick a default vendor when `--rag` is omitted | Omitted flag = file write only. No vendor is assumed |

### Plan post-write ask (HARD STOP — required immediately after writing/updating the plan file)

After writing or updating `plan-*.md`, **AI must actively scan the plan for undecided items and call AskUserQuestion** before reporting completion. Do not assume the user will read the file and fill in blanks autonomously — that is a partial-collaboration assumption that loses decision authority.

#### Undecided item triggers (scan plan body AND the original request for these)

| Pattern | Treatment |
|---------|-----------|
| **The original request itself poses an explicit either/or (e.g., "plan whether A or B", "one commit vs separate", "merge vs split")** | **PRIMARY mandatory question** — this is the decision the user explicitly asked you to plan. A prose "recommend X" recommendation does NOT satisfy it. Convert to AskUserQuestion with Recommended option |
| Trade-offs / Alternatives row with a forward-looking question mark (e.g., "is support needed?", "can this change?") | Convert to a question option |
| "User review memo" section with placeholder lines (`___`, "additional request: ___", "other format needed?") | Convert to a question option |
| "Out of scope" item that requires user confirmation to actually defer | Confirm via question |
| Verification step that requires backend choice or environment switch | Confirm via question |
| Any cell marked "TBD", "deferred", "decision required", or with a verbal alternative ("X vs Y"), **including plan section headings (e.g., "Decision point: one commit vs separate")** | Convert to a question option |
| Trade-off entries where multiple mitigations exist | Confirm chosen mitigation |
| A recommendation written as prose ("recommend X", "one commit feels natural") for a decision the user has not explicitly confirmed | A recommendation is NOT a decision. Convert to AskUserQuestion with X as the Recommended option |

#### Ask construction rules

- Use **AskUserQuestion `questions` array** (up to 4 per call). Each question covers one decision axis
- **Each option = a concrete choice the user can pick** (not "write plan as file vs chat" — that violates the always-on document-artifact default-save rule)
- Recommended option = the one Claude self-decides as best (with brief reason in description)
- Use "Other" (auto-provided) for free-text fallback
- Do not include "End session" or "Skip" as Recommended — see `next.md` rules

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Write plan with `___` placeholder lines and report "plan complete" | Scan placeholders → convert each to an AskUserQuestion option → ask before reporting complete |
| 2 | Leave Trade-off mitigations as "user decides" inline and stop | Each unresolved Trade-off → 1 question with 2-3 concrete options |
| 3 | Assume user will add inline memos and re-call the workflow | vibe-coding 3-stage cycle is **bidirectional**: user adds memos, AND AI actively asks on undecided items |
| 4 | Single question with 5+ mixed-axis options | Split into multiple questions (max 4) using `questions` array. Each question = one decision axis |
| 5 | Ask "Plan OK? proceed?" without enumerating undecided items | Enumerate each undecided item as its own question option |
| 6 | Use "save plan as file vs print in chat" as one of the options | Forbidden by the always-on rule "target-unspecified document artifacts = file save default". Medium is decided by default rule |

#### Self-check (every time after writing/updating plan file)

1. Does the **original request** pose an explicit either/or ("whether A or B")? → That decision is the PRIMARY mandatory question (a prose "recommend" does not satisfy it)
2. Did you Grep the plan body for `___`, `?`, "TBD", "deferred", "vs", "decision required", "recommend"?
3. Did each match become an option in an AskUserQuestion call?
4. Are the questions structured as **decision axes** (1 axis per question), not as a single mega-question?
5. Did you call AskUserQuestion **before** reporting "plan complete" in chat?
6. **After the user answers, did you reflect the decision back into the plan file (Edit) and save?** — ask without reflect+save = incomplete
7. If 0 undecided items found, did you state that explicitly in the report? ("No open decisions in plan revision N — ready for apply or further review")

#### Procedure (after every plan write/update) — ask → reflect → auto-save loop (HARD STOP)

```text
1. Write/update plan-*.md
2. Read back the file (Grep for undecided markers) + re-read original request for explicit either/or
3. Build AskUserQuestion `questions` array (max 4)
4. Call AskUserQuestion BEFORE reporting plan completion in chat
5. After user answers: REFLECT each decision into the plan file (Edit — mark "Decision: X" / remove the open "vs" framing) and SAVE. This is mandatory, not optional
6. Re-Grep the saved plan to confirm 0 remaining undecided markers
7. Then report completion / proceed to Step 3
```

**The loop is ask → reflect → save, all three (HARD STOP)**. Asking and then proceeding to Step 3 without writing the answer back into the plan loses the decision from the artifact. The plan file must reflect the confirmed decision (e.g., "one commit vs separate" heading → "Decision: one commit (user-approved 2026-05-27)") before the plan is considered complete.

### Plan Lifecycle Update (MANDATORY after implementation)

When implementation is complete (PR merged or changes landed), update the plan file's frontmatter:

1. Set `status: implemented`
2. Set `pr: <number>` with the merged PR number
3. If the plan was posted to an issue comment, verify `posted_to:` is populated

This ensures plan files remain accurate as living documents, not write-once artifacts.

```bash
# Self-check: find plan files with stale status after PR merge
grep -l '^status: draft\|^status: approved' {output-dir}/plan-*.md
```

### Pre-archive Completion Gate (MANDATORY before archiving a plan)

Before archiving a plan file (moving it to an archive dir, or marking the task done), verify completion:

1. Every `## Progress Checklist` item is `[x]`
2. Frontmatter `status:` is `implemented` or `closed`

An unchecked checklist item OR a non-terminal `status` means the work is **not** done — do not archive. The checklist makes completion verifiable at a glance.

```bash
# Self-check: plan files with unchecked items (not archive-ready)
grep -l '^- \[ \]' {output-dir}/plan-*.md
```

## Step 3: User Review & Branch Creation

1. **Report BLOCKED or Open Questions**: If there are any ambiguities, report them and wait for user feedback.
2. **Obtain Approval**: Wait for the user to approve the plan (e.g., "Proceed", "approved").
3. **Identify Primary Branch (HARD STOP)**:
   - Identify the repository's primary (default) branch via `git remote show origin` or `git branch -r`
   - Usually one of `master`, `main`, or `develop`. If unclear, AskUserQuestion.
4. **Fetch & Create Branch**:
   ```bash
   git fetch origin [primary-branch]
   git checkout -b [new-feature-branch] origin/[primary-branch]
   ```
   - If the branch already exists, `rebase` it onto the latest primary branch.
5. **Report Branch Status**: "Branch created from origin/[primary-branch]: [branch-name]". Example: `feat/256-session-expired-dialog` (created in an isolated worktree per Step 3c).

Items for the user to verify:
- Is the approach appropriate?
- Is the modification scope within the issue/PR scope?
- Does it match existing patterns/conventions?

On user feedback → revise plan and re-review. On approval → proceed to step 3b (if applicable) or step 4.

**plan-to-issue auto-trigger**: If the task is linked to a GitHub issue (e.g., "Issue #176"), run `github-flow/plan-to-issue` to post the plan as an issue comment **before** reporting to user. This ensures the plan is visible in the issue tracker, not just locally.

**dependencies auto-trigger** (when plan declares `chain:` frontmatter): If the plan file's frontmatter contains a `chain:` array declaring sequential issue dependencies (e.g., `#A → #B → #C`), invoke `github-flow/dependencies` after plan approval to apply the chain to GitHub via `addBlockedBy` mutations. Example frontmatter:

```yaml
---
plan: <name>
chain:
  - issue: 282
    blocked_by: [255]
  - issue: 253
    blocked_by: [282]
---
```

The dependencies topic will:
1. Fetch issue node IDs (Step 2 of dependencies.md)
2. Inspect existing `blockedBy` to detect already-applied relationships
3. Apply only the missing relationships, 1 at a time with user confirmation
4. Verify final state matches the chain

If the plan has no `chain:` frontmatter, this trigger is skipped — single-issue plans don't need dependency wiring.

**Prohibited: Immediate Implementation Offer**: When creating or updating an issue draft or plan document, **DO NOT offer to implement the code immediately** (e.g., "Shall we write the code now?"). Creating an issue draft means the task is being planned/scheduled. You must strictly wait for user approval or the explicit `Implement` command before proceeding to Step 3b/3c.

### Step 3b: Branch Creation (github-flow issue only)

When invoked with `github-flow issue #N`, create an issue branch after plan approval and before implementation:

1. `gh issue develop <N> --checkout --name "<tag>/<N>-<english-description>"`
2. Branch naming follows conventional commit tag + issue number + English description
3. If already on a feature branch for this issue, skip this step

### Step 3c: Worktree + Branch Creation (Mandatory)

**Must be executed after plan approval and before implementation:**

1. Call `Skill("superpowers:using-git-worktrees")` — Create an isolated workspace
2. Create a new feature branch (do not reuse already merged branches)
3. Proceed with implementation in the worktree

**If there is existing work** (unstaged/staged changes):
- `git stash` → create worktree → `git stash pop` in the worktree — move existing modifications to the worktree
- Or temporarily commit existing changes → `git cherry-pick` in the worktree branch
- **Do not discard existing work and rewrite from scratch** — double work is prohibited

**Prohibited**: Direct implementation in master/develop, adding commits to an already merged branch
