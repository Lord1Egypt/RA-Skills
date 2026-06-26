# Workflow Reference

Complete agent workflow for projects managed under this team setup.
Read this when troubleshooting agent behavior, explaining the workflow to an operator,
or verifying an agent is acting correctly for the current phase.

---

## Table of Contents

- [Phase Overview](#phase-overview)
- [Phase 1: Requirements and Feasibility](#phase-1-requirements-and-feasibility)
- [Phase 2: Planning](#phase-2-planning)
- [Phase 3: Implementation](#phase-3-implementation)
- [Phase 4: QA](#phase-4-qa)
- [Phase 5: Operator Review and Merge](#phase-5-operator-review-and-merge)
- [Phase 6: Sprint Close](#phase-6-sprint-close)
- [Escalation Rules](#escalation-rules)
- [Git and Branch Conventions](#git-and-branch-conventions)
- [Queue Message Format](#queue-message-format)
- [Agent Session Start Checklist](#agent-session-start-checklist)

---

## Phase Overview

```
idle → requirements → planning → implementation → sprint-close → idle
                                       ↕
                                      qa
```

Each phase is tracked in `project-lock.json`. Agents check this file before acting.
If the current phase does not match the agent's intended action, the agent stops and
posts to their relevant queue rather than proceeding.

---

## Phase 1: Requirements and Feasibility

**Owner:** PM Agent  
**Lock phase:** `requirements`  
**Queue used:** `to-engineer-feasibility.md` (kept separate from implementation escalations)

### Steps

1. PM receives or drafts client requirements.
2. PM creates a new versioned spec file: `workspace/SPEC-v[N]-[YYYY-MM-DD].md`
   - Never overwrite an existing spec — always increment the version number
   - Updates `SPEC-CURRENT.md` to reference this draft
   - Marks file: `STATUS: DRAFT — Under feasibility review`
3. PM posts to `queues/to-engineer-feasibility.md`:
   ```
   [date] [FROM: pm] [TO: engineer] [TASK: N/A]
   New spec draft ready for feasibility review.
   File: workspace/SPEC-v[N]-[YYYY-MM-DD].md
   ---
   ```
4. Engineer reads the spec and reviews for:
   - Technical feasibility
   - Conflicts with existing architecture
   - Ambiguities that would block implementation
   - Missing information the devs would need
5. Engineer posts all issues to `queues/to-engineer-feasibility.md` — **numbered**, specific, with options where possible:
   ```
   [date] [FROM: engineer] [TO: pm] [TASK: N/A]
   Feasibility review complete. 3 issues to resolve before accepting.

   Issue 1: [title]
   [description of the technical issue, concrete impact, and options if available]

   Issue 2: ...
   ---
   ```
6. PM translates each issue into non-technical language.
   - If email is configured: sends to client directly
   - If not configured: posts to `queues/to-operator.md` with message ready for operator to relay
7. Client responds to each numbered issue:
   - **Accept as known outcome** — client accepts the limitation as-is
   - **Provide a solution** — client proposes an alternative
   - **Descope** — remove the requirement causing the issue
8. PM logs client response in `DECISIONS.md` verbatim with date (see format in project-files.md).
9. If client proposes a solution, engineer evaluates it. This loop repeats until all issues resolved.
10. When all issues resolved:
    - Engineer updates `SPEC-CURRENT.md`: `STATUS: ACCEPTED — [date] — [engineer] + [pm]`
    - PM logs final acceptance in `DECISIONS.md`
    - PM updates `project-lock.json` → `phase: planning`

### Client No-Response Rule
- No response in **48 hours** → PM sends follow-up via email
- Still no response → PM posts to `queues/to-operator.md`:
  ```
  [date] [FROM: pm] [TO: operator] [TASK: N/A]
  Client has not responded to feasibility issues for 48h. Follow-up sent.
  Please engage client directly. Issues are in queues/to-engineer-feasibility.md.
  ---
  ```
- Task moves to Blocked in Asana until resolved

---

## Phase 2: Planning

**Owner:** Lead Engineer  
**Lock phase:** `planning`

### Steps

1. Engineer writes `workspace/IMPLEMENTATION_GUIDE.md` (see format in project-files.md).
   - Each numbered section = one Asana task
   - Task-oriented and detailed enough to implement without ambiguity
   - No full code — approach, files affected, edge cases, acceptance criteria
   - Notes items for `KNOWN_ISSUES.md`
   - **If the spec includes mockups:** engineer uses its vision capability (Gemini 3.1 Pro)
     to review them. Each task that references a mockup must include the mockup filename
     in its task section so the FE dev and QA can locate it later.
2. Engineer updates `KNOWN_ISSUES.md` with any limitations accepted during requirements phase.
3. Engineer posts to `queues/to-pm.md`:
   ```
   [date] [FROM: engineer] [TO: pm] [TASK: N/A]
   Implementation guide ready. workspace/IMPLEMENTATION_GUIDE.md
   [N] tasks defined.
   ---
   ```
4. PM reviews guide for completeness (can each section become a clear Asana task?).
5. PM creates Asana tasks from guide:
   - One task per numbered section
   - Task description includes the relevant guide section text
   - Tasks placed in Backlog, assigned to appropriate agents
6. PM posts to `queues/to-engineer.md`:
   ```
   [date] [FROM: pm] [TO: engineer] [TASK: N/A]
   Sprint [N] open. [X] tasks created in Asana Backlog.
   ---
   ```
7. PM updates `project-lock.json`:
   ```json
   {
     "phase": "implementation",
     "sprint_id": "sprint-[N]",
     "sprint_opened": "[date]"
   }
   ```
8. PM updates `STATE.md` to reflect sprint open status.

---

## Phase 3: Implementation

**Owner:** Devs (their assigned tasks)  
**Escalation owner:** Lead Engineer  
**Lock phase:** `implementation`

### Dev Task Flow

1. Dev picks up assigned task from Backlog → moves to In Progress in Asana.
2. Dev reads:
   - `workspace/IMPLEMENTATION_GUIDE.md` — the relevant task section
   - `RUNBOOK.md` — codebase conventions and gotchas
   - Their queue (`queues/to-[role].md`) — any pending messages
3. **If the task references a mockup (FE dev only):**
   - Dev switches to its vision model (Gemini 3.1 Pro) for this task
   - Retrieves the mockup from Asana attachments (preferred) or `./workspace/mockups/`
   - If mockup cannot be retrieved from either source, treat as a blocker —
     escalate to engineer per normal escalation rules
4. Dev implements in the sprint branch:
   - Branch format: `[project-id]/[sprint-id]/[task-id]-[short-description]`
   - Dev works in `workspace/repo/` on their branch
5. When task is complete:
   - Push to sprint branch
   - **First task of sprint:** open a PR
   - **Subsequent tasks:** push updates — existing PR auto-updates
   - Move Asana task from In Progress → In Review
   - Post to `queues/to-qa.md`:
     ```
     [date] [FROM: dev-fe] [TO: qa] [TASK: 1234]
     Task 1234 complete. Branch: ezbi/sprint-3/1234-navbar-redesign
     PR: [PR URL]
     What changed: [brief description]
     ---
     ```
6. Dev moves on to next Backlog task if available.

### Dev Escalation Rules

**When blocked:**
- Post to `queues/to-engineer.md`:
  ```
  [date] [FROM: dev-fe] [TO: engineer] [TASK: 1234]
  Blocked on task 1234.
  Attempted: [what was tried]
  Question: [specific question]
  ---
  ```
- Engineer responds in `queues/to-[dev-agent].md`
- Dev waits for response before continuing on this specific issue

**Hard stop rule — triggers when EITHER condition is met:**
- Same issue escalated to engineer **2 times** without resolution, OR
- Dev has been actively stuck on the same issue for **24 hours**

**When hard stop triggers:**
1. Dev **stops work immediately** on that task
2. Dev posts full summary to `queues/to-pm.md`:
   ```
   [date] [FROM: dev-fe] [TO: pm] [TASK: 1234]
   HARD STOP — Task 1234 escalation limit reached.
   Issue: [description]
   Escalation history:
     [date] — First escalation to engineer: [question]
     [date] — Engineer response: [response]
     [date] — Second escalation to engineer: [question]
     [date] — Engineer response: [response]
   Still blocked because: [reason]
   Awaiting operator assistance before resuming.
   ---
   ```
3. Task moves to Blocked in Asana
4. PM posts to `queues/to-operator.md`
5. **No further AI cycles spent on this task until operator resolves**

---

## Phase 4: QA

**Owner:** QA Agent  
**Lock phase:** `implementation` (QA runs concurrently)

### QA Task Flow

1. QA picks up task from In Review → moves to QA in Asana.
2. QA reads:
   - `KNOWN_ISSUES.md` — do not file failures against accepted limitations
   - `workspace/SPEC-CURRENT.md` — accepted requirements
   - `workspace/IMPLEMENTATION_GUIDE.md` — planned approach for this task
3. **If the PR includes UI changes and the task references a mockup:**
   - QA uses its vision capability (Gemini 3.1 Pro, native) to compare
     rendered UI against the referenced mockup
   - Visual deviations from the mockup that are not noted in `KNOWN_ISSUES.md`
     are QA failures
   - Retrieve mockup via Asana attachment (preferred) or `./workspace/mockups/`
4. QA reviews the PR against all references.

### QA Pass
```
[date] [FROM: qa] [TO: operator] [TASK: 1234]
Task 1234 — QA PASSED.
PR: [PR URL]
Branch: [branch name]
Verified against: SPEC-CURRENT.md + IMPLEMENTATION_GUIDE.md task 1
No known issues flagged.
---
```
- Move task to Completed in Asana.

### QA Fail
```
[date] [FROM: qa] [TO: engineer] [TASK: 1234]
Task 1234 — QA FAILED. [N] issues found.

Issue 1: [specific description — what was tested, what was expected, what happened]
Issue 2: ...
---
```
- Move task back to In Progress in Asana.
- Dev addresses failures, re-pushes. PR auto-updates. QA re-reviews.

---

## Phase 5: Operator Review and Merge

**Owner:** Operator (Human)  
**Lock phase:** `sprint-close` (after merge)

### Flow

1. Operator reviews `queues/to-operator.md` for QA-passed tasks.
2. Operator pulls the branch locally and reviews.
3. If satisfied: Operator tells QA agent — "Merge to main."
4. QA agent merges the PR to main.
5. QA agent (or devs) rebase all affected repos to main:
   ```bash
   git checkout main
   git pull
   git checkout [sprint-branch]
   git rebase main
   ```
6. Operator confirms rebase is clean — no conflicts, CI passes.
7. Operator updates `project-lock.json` → `phase: sprint-close`.

---

## Phase 6: Sprint Close

**Owner:** PM Agent  
**Lock phase:** `idle` (after close)

### Close Checklist

1. PM verifies all sprint tasks are in Completed in Asana.
2. PM archives completed tasks in Asana (close/archive — do not delete).
3. PM verifies `DECISIONS.md` has a complete record for this sprint.
4. PM verifies `KNOWN_ISSUES.md` is current with all accepted limitations.
5. PM writes sprint summary to `SHARED_MEMORY.md`:
   ```markdown
   ## [YYYY-MM-DD] Sprint [N] Close — pm-agent
   What was built: [summary]
   Issues accepted: [reference to KNOWN_ISSUES entries]
   Client sign-off: [yes/no — how confirmed]
   Carry-over notes: [anything relevant for the next sprint]
   ```
6. PM updates `STATE.md`:
   ```markdown
   # [Project Name] — Current State
   **Phase:** Idle — Sprint [N] closed. Ready for next requirements.
   **Last updated:** [date] by [pm-agent]
   ```
7. PM archives queue entries — prepend `[READ]` to processed entries. Do not delete lines.
8. PM updates `project-lock.json`:
   ```json
   {
     "phase": "idle",
     "sprint_id": null,
     "sprint_opened": null,
     "waiting_on": null,
     "last_updated": "[date]",
     "last_updated_by": "[pm-agent]",
     "context": "Sprint [N] closed. Ready for next requirements.",
     "blocked_tasks": []
   }
   ```
9. PM posts to `queues/to-operator.md`:
   ```
   [date] [FROM: pm] [TO: operator] [TASK: N/A]
   Sprint [N] closed. Asana clean. All queues archived.
   Ready to receive next set of requirements.
   ---
   ```

**PM does not accept new requirements until project-lock.json phase is idle.**

---

## Escalation Rules

| Situation | Action | Threshold |
|---|---|---|
| Client not responding to requirements | PM emails, then posts to to-operator.md | 48h no response |
| Dev blocked on task | Dev posts to to-engineer.md | Immediately when blocked |
| Same issue escalated 2x to engineer | Dev hard stop, PM posts to to-operator.md | 2 escalations |
| Dev stuck same issue | Dev hard stop, PM posts to to-operator.md | 24h active stuck |
| Task in Blocked with no movement | PM posts to to-operator.md | 48h |
| QA failing same task repeatedly | QA posts to to-engineer.md; PM monitors | — |

**No agent continues spending AI cycles on a blocked path. Stop, surface, wait.**

---

## Git and Branch Conventions

### Branch naming
```
[project-id]/[sprint-id]/[task-id]-[short-description]
```
Examples:
```
ezbi/sprint-3/1234-navbar-redesign
ezbi/sprint-3/1235-settings-migration
ezbi/sprint-3/1236-avatar-dropdown
```

### One branch per dev per sprint
- Dev works all their sprint tasks on a single branch
- Push after completing each task — PR auto-updates
- QA reviews the PR again after each push

### Hotfix branches (operator approval required)
- Only when a fix must ship independently of the current sprint
- Operator explicitly approves before dev creates a new branch
- Goes through the same QA → operator → merge flow

### PR conventions
- Title: `[[PROJECT-task-id]] Short description`
- Body must include:
  - Task ID
  - Asana task link
  - What changed (brief)
  - How to test
- One PR per dev per sprint — it accumulates all tasks as dev pushes

### After merge
1. QA merges PR to main (on operator instruction)
2. All affected repos rebase to main
3. Operator confirms clean

---

## Queue Message Format

Every queue entry must use this exact format:

```
[YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: asana-task-id or N/A]
Message body. Be specific. Include task IDs, file names, error messages where relevant.
If multiple items, number them clearly.
---
```

### Rules
- Queues are append-only — never delete entries
- When processed, prepend `[READ]` to the entry — do not remove the line
- Archive at sprint close (mark READ, do not remove)
- Each agent checks their queue at session start before any other action
- `to-engineer-feasibility.md` is used **only** during requirements phase — keep it separate from escalations

---

## Agent Session Start Checklist

Every agent runs this at the start of every session:

1. Read `project-lock.json` — what phase are we in?
2. Read `queues/to-[my-role].md` — any pending messages?
3. If there are unread queue messages, address them before starting new work
4. If phase does not match my expected action, post to relevant queue and wait
5. If phase matches and no pending messages, proceed with current work

**The queue and phase check always comes before anything else.**
