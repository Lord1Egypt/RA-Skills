---
name: game-dev-sprint
description: >
  Sprint-based game development workflow. Epic/story breakdown, sprint
  planning, dev-story workflow with story readiness and done criteria.
  Designed for solo devs and small teams using agile methodology adapted
  for game development.
triggers:
  - "plan a sprint"
  - "start development"
  - "break down tasks"
  - "sprint planning"
  - "agile gamedev"
  - "user stories"
  - "development workflow"
  - "epic breakdown"
---

# Game Dev Sprint — Agile Development Workflow

## 🎯 Purpose

Translate game design into actionable development work using sprint-based
agile methodology adapted for games. Epic/story breakdown, sprint planning,
daily workflow, and definition of ready/done.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for maintaining sprint boards and backlog as markdown files. Can create `sprint/` folder with evolving docs. |
| **Claude Code** | Can create task lists and mark files as done. Good for tracking in-IDE. |
| **Cursor/Windsurf** | Good for task tracking alongside code. |
| **GitHub Copilot** | Chat can help break down epics into tasks. Use GitHub Issues for actual tracking. |
| **Generic LLM Chat** | Output sprint plans and task breakdowns as lists. User copies to their tracker. |
| **Any AI** | All can help with planning and breakdown. Structured output (task lists, tables) works everywhere. |

**Integration note:** For real sprint tracking, consider linking to a proper
tool (GitHub Projects, Jira, Trello, Notion, HacknPlan). The AI can maintain
a text version and sync notes.

---

## 📂 Document Structure

Create in `game-dev-studio/sprint/`:

```
sprint/
├── backlog.md            ← Full backlog (epics + stories)
├── current-sprint.md     ← Active sprint
├── done.md               ← Completed work log
└── retrospective.md      ← Sprint retrospectives
```

---

## 📦 Phase 1: Epic & Story Breakdown

### Step 1.1 — Define Epics

Ask:
> **"What are the major features or systems?"**

**Epic** = A large body of work that spans multiple sprints.

Break your GDD systems into epics:

```
EPIC-001: Player Movement System
EPIC-002: Combat System
EPIC-003: Inventory System
EPIC-004: Level Design (Forest World)
EPIC-005: UI/HUD
EPIC-006: Audio Implementation
EPIC-007: Save/Load
```

### Step 1.2 — Break Epics Into Stories

A **story** should be:
- **INVEST:** Independent, Negotiable, Valuable, Estimable, Small, Testable
- **Size:** 1-3 days of work
- **Vertical slice:** touches multiple layers (code, data, art)

Example breakdown:

```
EPIC-001: Player Movement System
├── STORY-001: Implement basic movement (WASD + input smoothing)
├── STORY-002: Implement jump (variable height)
├── STORY-003: Implement dash mechanic
├── STORY-004: Implement wall jump
├── STORY-005: Add movement particles (dust, trail)
├── STORY-006: Implement movement state machine
└── STORY-007: Tutorial prompt for movement
```

### Step 1.3 — Story Template

```markdown
### STORY-[number]: [Short description]

**Epic:** [EPIC-XXX]

**Description:**
[As a player, I want to... so that...]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Technical Notes:**
- [Implementation details]
- [Files to modify]

**Dependencies:**
- [ ] Depends on STORY-XXX
- [ ] Blocking STORY-XXX

**Estimate:** [XS / S / M / L / XL] or [story points]
```

---

## 📅 Phase 2: Sprint Planning

### Step 2.1 — Sprint Parameters

Ask:
> **"Sprint length?"**
>
> ```
> 1) 1 week (fast iteration, solo dev)
> 2) 2 weeks (standard agile)
> 3) 3 weeks (if working part-time)
> ```

**For solo devs:** 1-week sprints recommended. Shorter feedback loops.

### Step 2.2 — Capacity Planning

For each sprint, calculate:

```
Available hours per week:    [hours]
Focus factor:                0.7 (admin, meetings, context switching)
Effective hours per sprint:  [hours/week × sprint weeks × 0.7]

Example: 20h/week × 1 week × 0.7 = 14 effective hours
```

Then select stories totaling ≤ effective hours.

### Step 2.3 — Sprint Goal

**One sentence goal:** *"This sprint, we implement the core combat loop
with basic enemy AI and damage numbers."*

### Step 2.4 — Sprint Board Template

```markdown
# Sprint [Number] — [Goal]

**Dates:** [YYYY-MM-DD] → [YYYY-MM-DD]
**Velocity:** [planned] points / [actual] points

## Sprint Backlog
| Story | Estimate | Status | Owner |
|-------|----------|--------|-------|
| STORY-001 | 3 pts | 🟢 Done | [name] |
| STORY-002 | 5 pts | 🟡 In Progress | [name] |
| STORY-003 | 2 pts | ⚪ To Do | [name] |
| STORY-004 | 8 pts | 🔵 Deferred | [name] |

## Definitions

### Story Ready (can start work)
- [ ] Acceptance criteria defined
- [ ] Dependencies met
- [ ] Design decisions made
- [ ] Estimated
- [ ] Team understands the work

### Story Done (can close)
- [ ] Code written
- [ ] Code reviewed (if team)
- [ ] Unit tests pass
- [ ] Manual QA pass
- [ ] Runs on target platform
- [ ] No regressions introduced
```

---

## 🏃 Phase 3: Dev-Story Workflow

For each story, use this workflow:

### Step 3.1 — Start Story

1. Move story to **In Progress**
2. Create a branch: `feature/STORY-XXX-short-name`
3. Read GDD section for context
4. Ask the AI: *"I'm starting STORY-XXX. Can you help me implement [feature]?"*

### Step 3.2 — Implementation Pattern

For each story, the AI should:

1. **Understand context** — Read GDD, architecture, and existing code
2. **Plan** — Ask: *"What's the implementation approach?"*
3. **Code** — Write the implementation
4. **Test** — Run or suggest test steps
5. **Commit** — *"Ready to commit. Message: '[meaningful commit message]'"*

### Step 3.3 — Daily Check-in

Ask each day:
> **"Progress update on STORY-XXX?"**
>
> ```
> 1) On track — expected to finish this sprint
> 2) Blocked — stuck on [issue]
> 3) Scope creep — found additional work needed
> ```

If blocked, ask: *"What's blocking you?"* and help resolve.

If scope creep, ask: *"Should we create a new story for this or is it in scope?"*

### Step 3.4 — Commit Messages

```
[STORY-XXX] Short description

- Detail 1
- Detail 2
```

Examples:
```
[STORY-001] Implement basic player movement

- Added InputHandler for WASD movement
- Added PlayerController with smoothing
- Added speed variable exposed in inspector
```

---

## ✅ Phase 4: Definition of Ready & Done

### Story Ready Checklist

Before a story enters a sprint:

- [ ] **Acceptance criteria defined** — measurable pass/fail
- [ ] **Design decisions made** — no open questions
- [ ] **Dependencies met** — no blocking epics
- [ ] **Estimated** — team agrees on size
- [ ] **Testable** — someone can verify it works
- [ ] **Vertical** — touches enough layers to be meaningful

### Story Done Checklist

For a story to be complete:

- [ ] **Code implemented** — all acceptance criteria met
- [ ] **Builds** — no compile errors
- [ ] **Self-tested** — basic QA passed
- [ ] **No regressions** — existing features still work
- [ ] **Asset integration** — art/audio/assets in place (or placeholder marked)
- [ ] **Committed** — code in version control with good commit message
- [ ] **Documentation** — any new API/system briefly documented

### Sprint Done Checklist

- [ ] All stories meet Definition of Done
- [ ] Build compiles and runs on target platform
- [ ] Smoke test passed (see `qa-test` skill)
- [ ] Backlog updated with any new stories discovered
- [ ] Retrospective completed

---

## 🔁 Phase 5: Sprint Review & Retrospective

### Sprint Review Template

```markdown
# Sprint [Number] Review

**Goal:** [sprint goal]

## Demo / Walkthrough
[What was built — describe the working features]

## Metrics
- **Planned:** [X] stories / [Y] points
- **Completed:** [X] stories / [Y] points
- **Velocity:** [points per sprint]
- **Burndown:** [on track / behind / ahead]

## What shipped
- STORY-XXX: [feature] — working
- STORY-XXX: [feature] — working

## What didn't ship
- STORY-XXX: [reason] — deferred to next sprint
```

### Retrospective Template

```markdown
# Sprint [Number] Retrospective

## What went well 🟢
- [ ]
- [ ]

## What could improve 🟡
- [ ]
- [ ]

## Action Items
- [ ] [Action 1] — owner
- [ ] [Action 2] — owner
```

Common retrospective questions:
- Did we estimate accurately?
- Were there surprises?
- Did we have enough context for stories?
- Was the Definition of Ready realistic?

---

## 📋 Phase 6: Ongoing Backlog Management

### Backlog Grooming

Every sprint, review and update the backlog:
- Remove obsolete stories
- Split large stories
- Reprioritize based on feedback
- Update estimates

### Backlog Template

```markdown
# Backlog

## Current (Next Sprint)
| Priority | Story | Epic | Estimate |
|----------|-------|------|----------|
| P0 | STORY-XXX | EPIC-XXX | 5 pts |
| P1 | STORY-XXX | EPIC-XXX | 3 pts |
| P2 | STORY-XXX | EPIC-XXX | 2 pts |

## Future
| Priority | Story | Epic | Estimate |
|----------|-------|------|----------|
| P3 | STORY-XXX | EPIC-XXX | 8 pts |

## Icebox (Someday)
| Story | Epic | Notes |
|-------|------|-------|
| STORY-XXX | EPIC-XXX | Too vague, needs design |
```

---

## 🚀 Phase 7: First Sprint Quick Start

For the first sprint, prioritize:

1. **Project setup** (from `setup-engine`)
2. **Core mechanic prototype** (from `prototype`)
3. **1 playable scene** with the core loop
4. **Basic input** with player controller
5. **Build and run** on target platform

Then subsequent sprints build from there.
