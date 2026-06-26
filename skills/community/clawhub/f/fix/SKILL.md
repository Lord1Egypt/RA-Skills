---
metadata:
  author: es6kr
  version: "0.1.5"
name: fix
description: >-
  User behavior correction skill. Triggered by "fix:" prefix feedback (e.g., "fix: why didn't you commit?").
  Analyzes the mistake, improves the relevant prompt (skill/rule/agent/memory/hook) to prevent recurrence,
  then fixes the current issue. TodoWrite required for all steps.
  Use when "fix:", "fix this", "correct", "why not", "why missing", "behavior fix" is mentioned.
---

# Fix: Behavior Correction Skill

Activated when user gives feedback with "fix:" prefix. Finds the root cause of the mistake, improves the relevant prompt (skill/rule/agent/memory/CLAUDE.md/hook), and fixes the current issue.

## Trigger

- Messages with `fix:` prefix
- Behavior correction feedback: "fix this", "correct", "why not", "why missing"

## Options

- `--plan`: In Step 2, instead of modifying prompts directly, **emit only the modification plan** for user review before execution. Use for complex changes or changes spanning multiple files.

## Topic Dispatch

**When this skill is invoked with a topic specifier (e.g., `/fix step3-resume` or `Skill("fix", "step3-resume")`), load and follow only the matching topic file. Do not echo the Topics table or summarize other topics in the response.** The Topics table below is an index — for a normal `/fix` invocation, execute the Procedure below and Read each step's topic file when you reach that step.

## Topics

The core procedure (Step 0 → 4) lives below. Heavy step detail is split into topic files — **Read the matching topic before executing that step**.

| Topic | Description | Guide |
|-------|-------------|-------|
| step2-improvement | Step 2 detail: 4-filter gate, escalation matrix, `--plan`, Checkpoint | [step2-improvement.md](./step2-improvement.md) |
| step3-resume | Step 3 detail: intent inference, reject re-call, verification guard | [step3-resume.md](./step3-resume.md) |
| step4-wrapup | Step 4 detail: report format, medium separation, status-based prune | [step4-wrapup.md](./step4-wrapup.md) |
| behavior-discipline | Destructive-command gate, multi-repo tracking, chained-fix deps, anger→TDD switch | [behavior-discipline.md](./behavior-discipline.md) |

## Procedure

### Step 0. TodoWrite (MANDATORY — first action, no exceptions)

**Before any analysis or text output**, register TODO items.

**⚠️ CRITICAL — Do not delete prior fix tasks on chained /fix (HARD STOP)**:

When a new /fix arrives while a prior /fix's tasks are still pending/in_progress:
- **Do not delete** prior fix tasks — incomplete work (especially Resume) is lost
- **Insert 4 new fix tasks via TaskCreate**
- Include the prior fix's incomplete work in the new fix's Resume (fix-2)

**⚠️ CRITICAL — Preserve existing tasks when TaskCreate is unavailable (HARD STOP)**:

In sessions where TaskCreate is disconnected/unavailable, only TodoWrite is usable. **TodoWrite takes an array and overwrites the entire todo list on every call** — registering only 4 fix-* items will **wipe all existing todos**.

**Self-check immediately before calling**:
1. How many existing tasks (N) are registered in TodoWrite? (Confirm from prior call result or context)
2. Did you **include all N existing tasks in this call's array**?
3. Did you **append** the 4 fix-0/1/2/3 items after the existing N?

**Correct pattern** (pseudo-code; `...existing_8_tasks` is a placeholder for the actual array of existing tasks read from the prior TodoWrite/TaskList output — substitute the real entries verbatim):

```text
# If 8 existing tasks exist, call with a 12-item array adding fix-* 4
TodoWrite([
  ...existing_8_tasks,    # ← replace with the actual 8 existing task objects, not a literal spread
  { content: "🔍 fix: {summary} — root cause analysis", status: "in_progress" },
  { content: "🔧 Root cause fix", status: "pending" },
  { content: "🔄 Resume original work: {one-line summary of original work}", status: "pending" },
  { content: "📋 Wrap-up: report + task pruning", status: "pending" },
])
```

**Forbidden pattern** (data loss):
```text
# Ignoring existing tasks and registering only 4 fix-* → all existing tasks vanish
TodoWrite([
  { content: "🔍 fix: ...", status: "in_progress" },
  { content: "🔧 Root cause fix", status: "pending" },
  { content: "🔄 Resume original work: ...", status: "pending" },
  { content: "📋 Wrap-up: report + task pruning", status: "pending" },
])  # ❌ Existing task data is lost
```

**Default form (when no existing tasks)**:

```text
TodoWrite([
  { id: "fix-0", content: "🔍 fix: {user feedback summary} — root cause analysis", status: "in_progress" },
  { id: "fix-1", content: "🔧 Root cause fix", status: "pending" },
  { id: "fix-2", content: "🔄 Resume original work: {one-line summary of original work}", status: "pending" },
  { id: "fix-3", content: "📋 Wrap-up: report + task pruning", status: "pending" },
])
```

- **Antigravity (Gemini) Users**: Create or update the `task.md` artifact representing the TODO list above. This fulfills the TodoWrite requirement.

- In `fix-2`'s `{original work}`, list **the initial request plus everything in progress including the immediately preceding action**
  - Example: "Deploy workflow: image swap done, verification 3/5 in progress, PR body update pending"
  - Listing only the most recent action narrows the scope — go all the way back to the initial request and enumerate the full task list
- **[Measure 2] Dependency and Reference State Declaration (MANDATORY)**: When registering `fix-2`, you must explicitly declare the **preconditions (Depends on)** and the **base commit state (Reference commit)** required for the `Resume` task to run safely.
  - *Format Example*: `🔄 Resume original work: {summary} (Depends on: {preconditions}, Reference commit: {commit_sha})`
- fix-2 = "Complete the original work with the revised approach" — the goal is **the deliverable the user originally requested**, not skill/rule changes themselves
- Step 0 is **the first tool call** after /fix activation. Text output before TodoWrite = violation.

### 1. Root Cause Analysis (5-Why depth)

**No trivial exception (HARD STOP)**: Even when the symptom is fixable with a 1-line change, 5-Why analysis and the entire step-by-step procedure are mandatory. Bypassing or skipping any steps (Step 0 to Step 4) when `/fix` is triggered is strictly forbidden. Even for "simple typos / encoding issues / minor file copies", the procedure must be executed step-by-step.

| # | Don't | Do |
|---|-------|-----|
| 1 | Skip `/fix` step-by-step procedure when the correction seems simple or obvious | Always execute Step 0 (TodoWrite/task.md) first, followed sequentially by Step 1 (5-Why), Step 1.5, Step 2, Step 3, and Step 4 |
| 2 | Directly modify files or execute commands on a `/fix` trigger before initializing the task checklist | Ensure `task.md` or `TodoWrite` is initialized as the very first tool call in the turn |

**Recurrence pre-check (first step of Step 1) — MANDATORY 2-stage**:

**Stage 0 — RAG semantic search (if RAG receiver available)**:
- If the current environment has a registered RAG search tool (an MCP store with a find-style tool), call it with the fix pattern's core keywords **before** the grep step
- Semantic search catches paraphrased recurrences that exact-match grep misses (one pattern surfaces under different wordings)
- If RAG returns one or more archived/historical hits with similar semantic, classify as "Nth recurrence" even if the exact phrasing does not grep-match
- Receiver tool name is vendor-agnostic — `mcp__<vendor>__*-find` style. Caller picks whichever RAG store is registered in the current environment

**Stage 1 — exact-match grep (always run)**:
1. `Grep -r ~/.claude/skills/cleanup/data/` for prior records of the same pattern — **recursive search covers both HOT (`failed-attempts.md`) and archive (`archive/*.md`)**. Also grep `~/.agents/rules/*.md`.
2. If found in **HOT only** → classify as "Nth recurrence" → include in Why analysis "why prior fixes were ineffective"
3. If found in **archive only** → **invoke `Skill("cleanup", "fa-prune")` Step 7 restoration procedure** (cut section from archive → paste into HOT with recurrence label). Without restoration, the escalation rule (1st=rule / 2nd=hook review / 3rd=hook required) is silently invalidated.
4. If found in **both** → already in HOT (no restoration needed); just add recurrence note
5. If the rule already exists but wasn't followed → **do not stop at "existing rule not followed"; strengthen the rule** — rewrite rule text to be more specific/explicit, or design an enforcement mechanism (hook, PreToolUse guard). "Existing rule wasn't followed" is not a conclusion; the goal is **to analyze why it wasn't followed and make it followable**

**Why RAG + grep both (not RAG alone)**:
- RAG: semantic — catches paraphrased recurrences, misses exact-token rules
- grep: exact — catches rule violations, misses semantic recurrences
- Both required for full coverage. RAG-only = misses "existing rule wasn't followed" detections. grep-only = misses "Nth recurrence with different phrasing" detections

**Confirm existing rule coverage (CRITICAL — do not duplicate rules in fix.md)**:

The following general principles apply before entering the fix procedure. If your environment already enforces them as always-on rules, do not duplicate them into fix's own body — that creates location errors and duplication:

- **Forbid arbitrary action on unclear instructions** — when user instructions/statements admit multiple interpretations, AskUserQuestion is required (do not act on a guess)
- **Cross-verify state from multiple sources** — do not conclude from a single statement/output; verify at least 2 sources
- **Don't guess existing code's purpose/behavior — read it** — verify against primary sources (code, API, files)
- **Glob/Grep before claiming absence/necessity** — claims of "doesn't exist / is needed" must follow code verification

**If Why analysis identifies the above rules as root cause, the rules themselves do not need to be modified** — go deeper with Why 4-5 to ask "why was that rule ignored in the fix flow?". If the answer is "fix procedure forces a reactive flow" or "existing rules aren't applied automatically", do not trap the rule inside the fix skill — record it as a recurrence in failed-attempts.md (next candidate for hook automation).

Don't stop at the direct cause. Dig at least **3 levels deep**:

```
Why 1: What went wrong? (symptom — the immediate mistake)
Why 2: Why did I make that decision? (judgment — missing knowledge/rule)
Why 3: Why was that knowledge/rule missing? (structural — skill/rule gap)
```

- Fixing only Why 1 = patching a symptom. It recurs in a different form.
- Why 2-3 reveal **structural causes** (platform ignorance, DRY violation, etc.) — these go into rules/skills.
- Search for the responsible **skill/rule/hook** files (Grep/Glob)

**Completion gate — do NOT proceed to Step 1.5 until ALL of these are true:**
1. Each issue has **Why 1, Why 2, Why 3, Why 4, Why 5** written out explicitly — stopping at Why 3 fails the gate. Why 4 = "why it wasn't followed (procedural/structural defect)", Why 5 = "where that defect originates (skill flow, missing automation, etc.)"
2. Why 5 identifies a **specific target** (skill, rule, hook, agent prompt, project config, etc.) to fix
3. No AskUserQuestion or implementation actions during Step 1 — analysis only

### 1.5. Action plan per Why (MANDATORY — required before entering Step 2)

**This table MUST be physically emitted in your visible output before any Step 2 Edit/Write.** Knowing the targets mentally from the Why analysis is NOT a substitute — the table is the forcing function that surfaces "one Why → multiple fix spots". Skipping the emission silently leads to partial corrections (you fix the one spot you remember and miss the others).

**Iterate over all Whys and explicitly enumerate the action for each.** All entries in this list must be executed in Step 2 before Step 3 can proceed.

```text
| Why | Target file : spot | Action |
|-----|--------------------|--------|
| Why 1 | (current issue — resolved in Step 3) | Step 3 Resume |
| Why 2 | <rule-file> : staging section | Add rule: "Forbid alternative command selection on failure" |
| Why 3 | epic-bundle.md : Step 2 group line | by-theme → by-source-PR |
| Why 3 | epic-bundle.md : body template | per-PR section header |
| Why 3 | epic-bundle.md : Don't/Do table | add row |
| Why 3 | epic-bundle.md : self-check | add item |
| Why 5 | fix/SKILL.md : Step 2 Checkpoint | Add gate item |
```

**Multi-spot enumeration rule (HARD STOP)**: a single Why often maps to **multiple spots inside one file** (procedure step + output template + Don't/Do table + self-check). Enumerate **one row per spot**, not one row per file. "Target file : spot" granularity is mandatory — a single `epic-bundle.md` row that hides 4 spots is what produces "fixed the output but missed the procedure" partial corrections.

**Action types**:
- Edit/Write → execute in Step 2
- failed-attempts.md recording → execute in Step 2 (mandatory on recurrence)
- hook design/creation → execute in Step 2 (when escalation applies)
- Step 3 Resume → execute in Step 3

**Gate into Step 2 (HARD STOP — symmetric with the Completion gate into Step 1.5)**: do NOT perform any Step 2 Edit/Write until the table above is emitted in your visible output. The Completion gate already blocks entry *into* 1.5; this gate blocks exit *from* 1.5 into Step 2. Without it, a Step 1 → Step 2 fast-path skips the table.

**Step 2 Checkpoint verifies that every row in this table is completed.**

### 2. Prompt Improvement (Prevent Recurrence) — never skip

If Step 1 produced even one Why, Step 2 is **mandatory**. Default medium = `feedback` memory (1st-2nd recurrence); rule-file Edit only when the **4-filter gate** passes (3rd+ recurrence); hook implementation at 4th+ recurrence with a deterministic pattern. Minimize always-on rule context.

**Read [step2-improvement.md](./step2-improvement.md) before executing** — it holds the 4-filter gate, medium-priority table, escalation matrix, no-stage-skipping Don't/Do, `--plan` mode, and the Step 2 Checkpoint (verify every Why-level target from the Step 1.5 table was actually modified). Do not advance to Step 3 until the Checkpoint passes.

### 3. Resume Original Work (fix-2)

**The most important step.** Complete the user's original request — not just the fix. Infer user intent and pin the verification medium verbatim; re-call any rejected AskUserQuestion once its reject cause is resolved; resume existing in_progress tasks; reproduce verification through the exact user-reported medium (no detour).

**Read [step3-resume.md](./step3-resume.md) before executing** — it holds intent inference, missing-question identification, dismissal-signal handling, reject-cause classification + secondary-issue default, the verification-scope-reduction guard, and the Step 3 mandatory self-questions (PR Test Plan sync, architectural-finding record).

### 4. Wrap-up (Report + Task Pruning)

Report the fix (🔍 root cause / 🔧 improvement / 🔄 current fix / 📋 wrap-up), separate outstanding work by medium (actionable → TaskList, BLOCKED → fix_plan.md hold section), then status-prune **all** completed tasks created this session (fix-* + original work), preserving pending/in_progress.

**Read [step4-wrapup.md](./step4-wrapup.md) before executing** — it holds the chained-Resume integration gate, the report format + emoji mapping, the medium-separation principle, the status-based prune matrix, and the per-step self-checks.

## Anti-patterns

- Repeating "already fixed" without actually fixing the root cause
- Patching only the current issue without improving prompts (skill/rule/agent/memory/CLAUDE.md/hook)
- Text response without TodoWrite after /fix activation
- Recording in failed-attempts.md when the root cause is a skill defect (skill fix is 1st priority)
- **Stopping at Why 1** — fixing the symptom without asking Why 2-3 (structural cause)
- **Not cleaning up TODO/Task after completion** — must delete all fix TODOs when done
- **"User is right, so skip"** — even when the user's point is correct, Steps 0~4 must all execute. fix's value is not resolving the current issue but preventing recurrence. "You're right, executing right away" abandons Why analysis + rule modifications
- **"Fixing right now" / "I know the cause, skip"** — Step 1 Why analysis cannot be skipped, whether recurrence or trivial. Recurrence = evidence that prior fix's Why was insufficient, so go **deeper**. "Fix right now" is not a procedure that exists in the fix skill
- **Resume scope narrowing via auto-Reject classification** — When Resume produces an AskUserQuestion for option design, **all findings (Accept + Reject + Defer)** must appear as user-decidable options. Auto-Reject classification (`superpowers:receiving-code-review` "Push back when wrong" procedure) followed by excluding the Reject finding from options strips the user's override authority. The user typically phrases this as "fix them all together — why only X separately?". See consolidate/next.md "Reject finding option mandate" for the required option pattern (Accept-applied / Apply-ALL-override / Defer-all)
- **Option outcome must be pre-verified for path-based or cross-cutting tooling** — When AskUserQuestion options change a tool's behavior whose outcome depends on **path-based** or **commit-history** analysis (release-please, semantic-release, changesets, dependabot config, CI matrix rules, etc.), the option author must **dry-run / simulate / enumerate the outcome** before presenting options to the user. The user's authority is "decide between simulated outcomes," not "pick the option label and discover the real outcome only after merge." If options A and B both produce the same real-world outcome (e.g., still bumps every package because a cross-cutting `feat(...)` commit touches every package's path), state that fact in the option descriptions or merge the options. Failing this verification means the user invests effort in choosing an option that does not change the eventual result, then has to fix it after seeing the unchanged outcome. Specifically for release-please: enumerate `git log <proposed-base>..HEAD -- skills/<package>/` for every package before committing to a `last-release-sha` choice — if any cross-cutting `feat(...)` commit (e.g., monorepo-wide annotation, config bump touching every package) sits in that window, the chosen base will not block bumps.
