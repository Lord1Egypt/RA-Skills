# Project Files Reference

Full specification of every file in the `~/.openclaw/projects/[project_name]/` folder.

---

## Table of Contents

- [PROJECT.md — The Team Rulebook](#projectmd--the-team-rulebook)
- [project.json — Machine Config](#projectjson--machine-config)
- [project-lock.json — Phase Tracker](#project-lockjson--phase-tracker)
- [STATE.md — Human Status](#statemd--human-status)
- [SHARED_MEMORY.md — Cross-Agent Knowledge](#shared_memorymd--cross-agent-knowledge)
- [DECISIONS.md — Decision Log](#decisionsmd--decision-log)
- [KNOWN_ISSUES.md — Accepted Limitations](#known_issuesmd--accepted-limitations)
- [RUNBOOK.md — Project Setup Guide](#runbookmd--project-setup-guide)
- [workspace/SPEC-CURRENT.md](#workspacespec-currentmd)
- [workspace/IMPLEMENTATION_GUIDE.md](#workspaceimplementation_guidemd)
- [Queue Files](#queue-files)
- [File Responsibility Matrix](#file-responsibility-matrix)

---

## PROJECT.md — The Team Rulebook

**The most important file in the project folder.** Every participating agent has this injected into their context via their AGENTS.md. It is the single source of truth for how the team operates.

### Who reads it
All agents, at every session start (referenced from their AGENTS.md).

### Who writes it
Created by operator during setup. Updated by operator only when workflow rules change.

### Full Template

```markdown
# Project: [Project Display Name]

## The Team
- **PM Agent ([pm_agent_id])** — Client-facing. Owns requirements negotiation,
  Asana task creation, client communication, and sprint open/close.
- **Lead Engineer (engineer)** — Technical authority. Reviews feasibility, writes
  implementation guides, handles all technical escalations.
- **FE Dev (dev-fe)** — Implements front-end tasks from Asana. Escalates to Lead Engineer.
- **BE Dev (dev-be)** — Implements back-end tasks from Asana. Escalates to Lead Engineer.
- **QA Agent (qa)** — Validates PRs against the accepted spec. Merges on operator instruction.
- **Operator (Human)** — Final authority. Merges approval, unresolvable escalations, client engagement.

## Source of Truth

| What | Where |
|---|---|
| Task ownership and status | Asana |
| Accepted requirements | `workspace/SPEC-CURRENT.md` |
| Implementation approach | `workspace/IMPLEMENTATION_GUIDE.md` |
| Cross-agent knowledge | `SHARED_MEMORY.md` |
| Decision history | `DECISIONS.md` |
| Accepted limitations | `KNOWN_ISSUES.md` |
| Project setup / branch conventions | `RUNBOOK.md` |
| Current phase and ownership | `project-lock.json` |
| Human-readable status | `STATE.md` |

## Asana Columns

| Column | Meaning | Owner |
|---|---|---|
| Backlog | Work not yet started | PM creates tasks here |
| In Progress | Dev actively working | Dev owns |
| In Review | PR submitted, awaiting QA | QA picks up |
| QA | QA actively testing | QA owns |
| Completed | QA passed, awaiting operator | Operator reviews and merges |
| Blocked | Waiting on client/external | PM owns, escalates per rules |

## Git and Branch Convention

- **One repo copy** lives at `./workspace/repo/`
- **One active branch per dev per sprint**
  - Format: `[project-id]/[sprint-id]/[task-id]-[short-description]`
  - Example: `ezbi/sprint-3/1234-navbar-redesign`
- **After completing each task:** push to branch, PR opens (first task) or auto-updates (subsequent)
- **QA re-reviews after every push**
- **No new branches mid-sprint** unless operator explicitly approves a hotfix

## Mockups and Visual Assets

When a task involves a mockup, design comp, or visual reference:

- **Primary storage:** Asana task attachments. The Asana skill retrieves these.
- **Fallback storage:** `./workspace/mockups/` — used if Asana attachment retrieval is not available
- **Naming convention:** `[task-id]-[short-description].[ext]` (e.g. `1234-navbar-redesign.png`)
- **Task description must reference the mockup filename** so devs and QA can locate it

**Vision-required agents:**
- **Engineer** — uses vision (Gemini 3.1 Pro, native) when reviewing mockups during planning
  to write accurate implementation guides
- **FE Dev** — switches to its vision model (Gemini 3.1 Pro) when picking up a task whose
  Asana description references a mockup. Returns to GLM-5.1 for non-visual coding work.
- **QA** — uses vision (Gemini 3.1 Pro, native) when a PR includes UI changes that need to
  be compared visually against the mockup. QA is expected to compare rendered output to mockup.

If the FE dev cannot retrieve a referenced mockup from either Asana or `./workspace/mockups/`,
this is treated as a blocker — escalate to engineer per normal escalation rules.

## Workflow

### Phase 1: Requirements & Feasibility
1. PM receives or drafts client requirements
2. PM writes draft to `workspace/SPEC-v[N]-[YYYY-MM-DD].md`, updates `SPEC-CURRENT.md`
3. PM posts to `queues/to-engineer-feasibility.md` — "New spec draft ready"
4. Engineer reviews, posts all issues (numbered) to `queues/to-engineer-feasibility.md`
5. PM translates issues to non-technical language, sends to client via email or posts to
   `queues/to-operator.md` if email not configured
6. Client responds to each numbered issue: Accept / Provide solution / Descope
7. PM logs client response in `DECISIONS.md` verbatim with date
8. Engineer evaluates client solutions. Loop repeats until all issues resolved.
9. Engineer marks spec ACCEPTED in `SPEC-CURRENT.md`. PM logs in `DECISIONS.md`.
10. `project-lock.json` → phase: `planning`

**Client no-response rule:**
- No response in 48h → PM sends follow-up email
- Still no response → PM posts to `queues/to-operator.md`, task moves to Blocked

### Phase 2: Planning
1. Engineer writes `workspace/IMPLEMENTATION_GUIDE.md`
   - Task-oriented: each numbered section = one Asana task
   - Detailed enough to implement without ambiguity — no full code
   - Note items for `KNOWN_ISSUES.md`
2. Engineer updates `KNOWN_ISSUES.md` with accepted limitations
3. Engineer posts to `queues/to-pm.md` — "Implementation guide ready"
4. PM creates Asana tasks from guide, assigns to agents, places in Backlog
5. PM posts to `queues/to-engineer.md` — "Tasks created. Sprint [N] open."
6. `project-lock.json` → phase: `implementation`, sprint_id set

### Phase 3: Implementation
1. Dev picks up task from Backlog → moves to In Progress
2. Dev implements against `IMPLEMENTATION_GUIDE.md` and `RUNBOOK.md`
3. Dev checks `queues/to-[their-role].md` at session start

**Dev escalation rules:**
- If blocked: post to `queues/to-engineer.md` with task ID, what was tried, specific question
- Engineer responds in `queues/to-[dev-agent].md`
- If same issue escalated **2 times** to engineer without resolution, OR dev stuck **24 hours**:
  - Dev **stops work immediately**
  - Dev posts full summary to `queues/to-pm.md`
  - PM posts to `queues/to-operator.md`
  - Task moves to Blocked in Asana
  - **No further AI cycles on this task until operator resolves**

When task complete:
- Push to sprint branch. Open PR (first task) or PR auto-updates (subsequent).
- Move Asana task to In Review
- Post to `queues/to-qa.md` — task ID, PR link, brief description of changes

### Phase 4: QA
1. QA picks up tasks from In Review → moves to QA
2. QA reviews PR against:
   - `workspace/SPEC-CURRENT.md` — meets accepted requirements?
   - `KNOWN_ISSUES.md` — don't file failures against accepted limitations
   - `workspace/IMPLEMENTATION_GUIDE.md` — matches planned approach?
3. **Pass:** Move to Completed. Post to `queues/to-operator.md` — task ID, PR link, "QA passed."
4. **Fail:** Post specific numbered failures to `queues/to-engineer.md`. Move back to In Progress.

### Phase 5: Operator Review and Merge
1. Operator checks `queues/to-operator.md`
2. Operator pulls branch, reviews locally
3. If satisfied: tells QA — "Merge to main"
4. QA merges PR to main
5. QA/devs rebase all affected repos to main
6. Operator confirms rebase is clean
7. `project-lock.json` → phase: `sprint-close`

### Phase 6: Sprint Close
1. PM verifies all sprint tasks are Completed in Asana
2. PM archives completed tasks in Asana
3. PM verifies `DECISIONS.md` has full requirement decision record
4. PM verifies `KNOWN_ISSUES.md` is current
5. PM writes sprint summary to `SHARED_MEMORY.md`
6. PM updates `STATE.md` — "Sprint [N] closed. Ready for next requirements."
7. PM archives queue file entries (marks READ, does not delete)
8. `project-lock.json` → phase: `idle`
9. PM posts to `queues/to-operator.md` — "Sprint closed. Ready for next requirements."

**One sprint at a time. PM does not accept new requirements until project-lock.json is idle.**

## Escalation Rules Summary

| Situation | Action | Threshold |
|---|---|---|
| Client not responding | PM emails, then escalates to operator | 48h |
| Dev stuck on same task | Escalate to Lead Engineer | — |
| Same issue escalated 2x or 24h stuck | Stop work, PM escalates to operator | 24h |
| Task blocked with no movement | PM escalates to operator | 48h |

**No agent continues spending cycles on a blocked path. Stop, surface, wait.**

## Communication Protocol

All inter-agent messages go through the queue files in `queues/`.

**Message format — every entry must use this format:**
```
[YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: asana-task-id or N/A]
Message body. Be specific. Include task IDs, file names, error messages where relevant.
---
```

- Queues are **append-only**. Never delete entries.
- Archive at sprint close (mark entries READ, do not remove lines).
- Each agent checks their queue at the **start of every session, before anything else**.
- Feasibility discussions go to `to-engineer-feasibility.md` only — separate from escalations.
```

---

## project.json — Machine Config

Machine-readable project configuration. Agents read this to resolve file paths,
Asana GIDs, and participant details without relying on hardcoded values.

### Who reads it
All agents.

### Who writes it
Created by operator during setup. Updated by operator only when structure changes.

### Notes
- All file paths use relative paths from the project root folder
- Asana column GIDs must be filled in from the actual Asana board after creation
- Escalation thresholds here are the canonical values — PROJECT.md references these conceptually but agents read the numbers from this file

---

## project-lock.json — Phase Tracker

Prevents agents from acting out of phase or moving forward when waiting on another agent or the operator.

### Who reads it
All agents check this at session start before taking any action.

### Who writes it
PM (most phase transitions), Engineer (planning → implementation), QA (after merge), Operator (sprint-close → idle).

### Valid phase progression
`idle` → `requirements` → `planning` → `implementation` → `qa` → `sprint-close` → `idle`

### Format
```json
{
  "phase": "idle",
  "sprint_id": null,
  "sprint_opened": null,
  "waiting_on": null,
  "last_updated": "YYYY-MM-DD",
  "last_updated_by": "agent-id or operator",
  "context": "Human-readable description of current state",
  "blocked_tasks": []
}
```

### Agent behavior rules
- If `phase` does not match the agent's expected action → stop and post to relevant queue
- If `waiting_on` is not null and is this agent → act immediately on session start
- If `blocked_tasks` is non-empty and contains this agent's task → treat as stopped

---

## STATE.md — Human Status

The operator's one-file status check. Updated by agents at key moments so the operator
can understand project state without digging through Asana or queue files.

### Who reads it
Operator primarily. Agents may read it for context.

### Who writes it
All agents update it when they complete a significant action.

### Format
```markdown
# [Project Name] — Current State
**Phase:** [phase] ([sprint_id if applicable])
**Last updated:** [YYYY-MM-DD HH:MM] by [agent-id]

## Sprint Progress
- ✅ Task [ID] — [description] (merged)
- 🔄 Task [ID] — [description] (in progress, [agent])
- ⏳ Task [ID] — [description] (backlog)
- 🚫 Task [ID] — [description] (blocked — [reason])

## Operator Queue Summary
[List of items in to-operator.md awaiting action]
```

---

## SHARED_MEMORY.md — Cross-Agent Knowledge

A living document for project knowledge that needs to persist across sessions
but doesn't belong in Asana.

### What goes here
- Codebase quirks and patterns relevant to this project
- Client preferences and communication style notes
- Things learned mid-sprint that other agents should know
- Sprint-close summaries (added by PM at close)

### What does NOT go here
- Task status → Asana
- Accepted requirements → SPEC files
- Implementation approach → IMPLEMENTATION_GUIDE.md
- Decisions and client acceptances → DECISIONS.md

### Format
Free-form markdown. Agents append new information with a date prefix:
```markdown
## [YYYY-MM-DD] [agent-id] — [topic]
Content here.
```

---

## DECISIONS.md — Decision Log

An **immutable, append-only** record of every significant decision made during
requirements negotiation. Never edit or delete existing entries.

### Who reads it
PM, Engineer, Operator. QA references when filing failures.

### Who writes it
PM only. Written during requirements phase as decisions are made.

### Purpose
When a client later says "we never agreed to that," this file is the record.
It captures what was proposed, what issue was surfaced, what the client said, and what was accepted.

### Format
```markdown
## [YYYY-MM-DD] — [Sprint ID]: [Decision Topic]

**Issue surfaced by engineer:** [description of technical issue or conflict]

**Client response (received [date]):** [exact client words or paraphrase, clearly attributed]

**Resolution:** [Accept as known outcome / Client-proposed alternative / Descoped]

**Accepted by:** [Client name], [engineer agent], [pm agent]
**Logged by:** [pm agent]
---
```

---

## KNOWN_ISSUES.md — Accepted Limitations

Documents accepted technical debt and known limitations so QA does not file
failures against intentional decisions, and clients cannot later claim ignorance.

### Who reads it
QA (before every test run), all agents for context, operator.

### Who writes it
Engineer, updated during planning phase and as new limitations are accepted.

### Format
```markdown
## [Sprint ID] — [Issue Title]
- **Accepted:** [date]
- **Context:** [why this limitation exists and what decision led to it]
- **Impact:** [what users or developers will experience as a result]
---
```

---

## RUNBOOK.md — Project Setup Guide

Written and maintained by the Lead Engineer. Devs and QA read this before
starting work on any task to avoid unnecessary escalations.

### Who reads it
All agents before starting work, operator for deployment reference.

### Who writes it
Engineer creates initial stub during setup. Engineer fills in details after
their first session with the repo. Engineer updates as patterns evolve.

### Minimum contents
```markdown
# [Project Name] Runbook

## Local Setup
[How to install dependencies and run the project locally]

## Branch Naming Convention
[project-id]/[sprint-id]/[task-id]-[short-description]
Example: ezbi/sprint-3/1234-navbar-redesign

## PR Conventions
- Title: [[PROJECT-task-id]] Short description
- Body must include: task ID, what changed, how to test, Asana task link

## Known Codebase Patterns
[Common patterns in use — component structure, API conventions, etc.]

## Known Gotchas
[Things that trip up developers — quirky dependencies, env requirements, etc.]

## Deployment Notes
[Steps needed to deploy after merge if applicable]
```

---

## workspace/SPEC-CURRENT.md

A reference that always points to (or contains) the currently active accepted specification.

### Versioning rules
- Every new requirements draft gets its own versioned file: `SPEC-v[N]-[YYYY-MM-DD].md`
- Specs are **never overwritten** — always increment the version number
- `SPEC-CURRENT.md` is updated to point to or contain the latest accepted spec
- The version history is the audit trail

### Status markers
Engineer adds one of these markers at the top when reviewing:
```
STATUS: DRAFT — Under feasibility review
STATUS: ACCEPTED — [date] — [engineer agent] + [pm agent]
```

---

## workspace/IMPLEMENTATION_GUIDE.md

Written by the Lead Engineer after spec is accepted. The task-oriented blueprint
for what needs to be built and how.

### Format rules
- Each numbered section = one Asana task
- Describe approach, files affected, edge cases, dependencies, acceptance criteria
- No full code — approach-level only
- Reference `KNOWN_ISSUES.md` items created from this guide

### Structure
```markdown
# Implementation Guide — [Sprint ID]

## Task 1: [Task Title]
**Assigned to:** [agent role]
**Asana task:** [created by PM after this guide is written]

### What to build
[Description]

### Files affected
[List of files or components]

### Approach
[How to implement it — no full code]

### Acceptance criteria
[How QA will verify this is complete]

### Notes / edge cases
[Anything the dev should know]
---

## Task 2: ...
```

---

## Queue Files

Located in `queues/`. One file per recipient.

| File | Purpose |
|---|---|
| `to-pm.md` | Messages for PM — from engineer (issues ready), from QA (task failures), from devs (stuck escalations) |
| `to-engineer.md` | Messages for Lead Engineer — dev escalations, PM implementation requests |
| `to-engineer-feasibility.md` | Requirements phase only — keeps feasibility back-and-forth separate from escalations |
| `to-qa.md` | Messages for QA — dev task completions with PR links |
| `to-operator.md` | Messages for human operator — QA passes, blocks, client no-response, unresolvable escalations |

### Queue message format (required for every entry)
```
[YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: asana-task-id or N/A]
Message body. Be specific. Include task IDs, file names, error messages.
---
```

### Queue rules
- Append-only — never delete entries
- Mark entries READ (prepend `[READ]`) when processed — do not remove lines
- Archive at sprint close
- Check your own queue at the start of every session, before any other action

---

## File Responsibility Matrix

| File | Created by | Updated by | Read by | Mutable? |
|---|---|---|---|---|
| `PROJECT.md` | Operator | Operator only | All agents | Rarely |
| `project.json` | Operator | Operator only | All agents | On structure change |
| `project-lock.json` | Operator | PM, Engineer, QA, Operator | All agents | Every phase change |
| `STATE.md` | Operator | All agents | Operator, all agents | Frequently |
| `SHARED_MEMORY.md` | Operator | All agents (append) | All agents | Frequently |
| `DECISIONS.md` | PM | PM only (append) | PM, Engineer, Operator | Append-only |
| `KNOWN_ISSUES.md` | Engineer | Engineer (append) | QA, all agents | Append-only |
| `RUNBOOK.md` | Engineer | Engineer | Devs, QA | As patterns evolve |
| `SPEC-vN-*.md` | PM | Never | PM, Engineer | Immutable |
| `SPEC-CURRENT.md` | PM | PM (points to latest) | All agents | Per sprint |
| `IMPLEMENTATION_GUIDE.md` | Engineer | Engineer | All devs, QA | Per sprint |
| `queues/to-*.md` | Operator (init) | Named sender (append) | Named recipient | Append-only |
