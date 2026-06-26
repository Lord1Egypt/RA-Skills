# FounderClaw — Workspace Structure (Final v2)

## Company Model

```
CEO (FounderClaw Main) ←→ user (the client)
  │
  ├── gets projects from client
  ├── delegates to departments
  ├── writes all records (single source of truth)
  └── has access to everything
```

## Rules

1. **User always talks to CEO.** Never directly to a department.
2. **CEO is the single writer** of STATUS.md, current-tasks.md, and current-state.md. Departments report results to CEO. CEO writes the records.
3. **Departments don't maintain project status.** They do the work and tell CEO what they did.
4. **CEO syncs after every task.** After a department completes work, CEO updates STATUS.md.
5. **Departments reference skills.** processes.md says "when I do X, follow skills/X/SKILL.md."
6. **Manual mode:** all communication through CEO (hub).
7. **Auto mode:** departments can talk directly (pipeline). CEO gets notifications. Explicit switch only.

## Directory Structure

```
~/.openclaw/founderclaw/
│
├── ceo/                              ← CEO's private office
│   ├── AGENTS.md                     ← orchestration rules
│   ├── SOUL.md                       ← leadership personality
│   ├── IDENTITY.md                   ← "FounderClaw Main. 🎯"
│   ├── USER.md                       ← who the client is
│   ├── TOOLS.md                      ← tool settings
│   ├── MEMORY.md                     ← org-level learnings
│   ├── memory/
│   │   └── YYYY-MM-DD.md            ← daily logs
│   ├── dashboard.md                  ← aggregated view of all projects
│   ├── HEARTBEAT.md                  ← periodic checks
│   └── sessions/
│
├── projects/                         ← ALL PROJECTS (shared)
│   │
│   └── todo-app/                     ← ONE PROJECT
│       ├── README.md                 ← what is this project
│       ├── STATUS.md                 ← CEO-written. Single source of truth.
│       ├── current-tasks.md          ← CEO-written. Who's doing what RIGHT NOW.
│       │
│       ├── code/                     ← the product (all read, shipper writes)
│       │   ├── src/
│       │   ├── tests/
│       │   └── package.json
│       │
│       ├── design/                   ← strategy's output
│       │   ├── design.md
│       │   ├── architecture.md
│       │   └── decisions.md
│       │
│       ├── reviews/                  ← shipper's output
│       │   ├── review-report.md
│       │   ├── changelog.md
│       │   └── deploy-log.md
│       │
│       ├── qa/                       ← tester's output
│       │   ├── qa-report.md
│       │   ├── screenshots/
│       │   └── bugs.md
│       │
│       ├── security/                 ← safety's output
│       │   ├── audit.md
│       │   └── findings.md
│       │
│       └── history/                  ← observer's output
│           ├── retro.md
│           └── lessons.md
│
├── strategy-dept/                    ← DEPARTMENT DESK
│   ├── AGENTS.md                     ← "I do product thinking & design"
│   ├── SOUL.md                       ← "I am the product thinker"
│   ├── IDENTITY.md                   ← "Strategy. 📐"
│   ├── USER.md                       ← "I serve the CEO (FounderClaw Main)"
│   ├── TOOLS.md                      ← "Use vision sub-agent for screenshots"
│   ├── processes.md                  ← "I follow skills/office-hours/SKILL.md"
│   ├── MEMORY.md                     ← patterns, lessons, user preferences
│   ├── memory/
│   │   └── YYYY-MM-DD.md            ← daily work log
│   ├── current-state.md             ← CEO-written. BUSY/FREE + current task.
│   ├── HEARTBEAT.md                 ← "check pending design tasks"
│   └── sessions/
│
├── shipping-dept/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── IDENTITY.md                   ← "Shipper. 🚀"
│   ├── USER.md
│   ├── TOOLS.md
│   ├── processes.md                  ← "I follow skills/review/SKILL.md"
│   ├── MEMORY.md
│   ├── memory/
│   ├── current-state.md
│   ├── HEARTBEAT.md
│   └── sessions/
│
├── testing-dept/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── IDENTITY.md                   ← "Tester. 🔍"
│   ├── USER.md
│   ├── TOOLS.md                      ← "CONTAINER=1 for browse"
│   ├── processes.md                  ← "I follow skills/qa/SKILL.md"
│   ├── MEMORY.md
│   ├── memory/
│   ├── current-state.md
│   ├── HEARTBEAT.md
│   └── sessions/
│
├── security-dept/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── IDENTITY.md                   ← "Safety. 🛡️"
│   ├── USER.md
│   ├── TOOLS.md
│   ├── processes.md
│   ├── MEMORY.md
│   ├── memory/
│   ├── current-state.md
│   ├── HEARTBEAT.md
│   └── sessions/
│
├── history-dept/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── IDENTITY.md                   ← "Observer. 📊"
│   ├── USER.md
│   ├── TOOLS.md
│   ├── processes.md
│   ├── MEMORY.md
│   ├── memory/
│   ├── current-state.md
│   ├── HEARTBEAT.md
│   └── sessions/
│
├── company/                          ← COMPANY-WIDE SHARED CONFIG
│   ├── roster.md                     ← all agents, roles, model tiers
│   ├── project-list.md               ← active & completed projects
│   ├── models.md                     ← fast / best / vision model config
│   └── config.json                   ← tool policies, settings
│
└── skills/                           ← 29 founderclaw skills
    ├── office-hours/SKILL.md
    ├── review/SKILL.md
    ├── qa/SKILL.md
    └── ...29 total
```

## Department File Roles

| File | Standard? | Purpose | Writer |
|---|---|---|---|
| AGENTS.md | OpenClaw | Operating rules, how to behave | Department (once, rarely changes) |
| SOUL.md | OpenClaw | Personality, tone, boundaries | Department (once, rarely changes) |
| IDENTITY.md | OpenClaw | Name, emoji, vibe | Department (once) |
| USER.md | OpenClaw | "I serve the CEO" | Department (once) |
| TOOLS.md | OpenClaw | Tool-specific settings | Department (rarely changes) |
| processes.md | Custom | Methodology, which skills to use | Department (rarely changes) |
| MEMORY.md | OpenClaw | Curated long-term memory | Department (grows over time) |
| memory/*.md | OpenClaw | Daily work logs | Department (daily) |
| current-state.md | Custom | BUSY/FREE + current task | CEO (updates on task start/end) |
| HEARTBEAT.md | OpenClaw | Periodic availability check | Department (once, rarely changes) |
| sessions/ | Auto-managed | Conversation history | OpenClaw (automatic) |

## CEO Files

| File | Purpose |
|---|---|
| AGENTS.md | Orchestration rules, delegation logic, auto mode switch |
| SOUL.md | CEO personality — direct, decisive, organized |
| IDENTITY.md | "FounderClaw Main. 🎯 The CEO." |
| USER.md | Who the client is, their preferences |
| TOOLS.md | Tool settings for CEO |
| MEMORY.md | Org-level learnings across all projects |
| memory/*.md | Daily CEO logs |
| dashboard.md | Aggregated view: all projects, all departments, status at a glance |
| HEARTBEAT.md | "Check all departments for pending work. Update dashboard." |

## STATUS.md Format (CEO-written)

```markdown
# Project: todo-app
Updated: 2026-03-28 23:00 IST
Status: IN PROGRESS

## Completed
- [x] office-hours (strategy, Mar 28)
- [x] architecture approved (strategy, Mar 28)
- [x] code review (shipper, Mar 28)

## Active
- [ ] QA testing (tester, started Mar 28)

## Pending
- [ ] security audit (safety)
- [ ] deploy (shipper)
- [ ] retro (observer)

## Blockers
None

## CEO notes
User approved design on Mar 28. Shipper found 2 issues, fixed both.
```

## current-tasks.md Format (CEO-written)

```markdown
# Current Tasks — todo-app
Updated: 2026-03-28 23:00 IST

| Dept | Task | Status | Since |
|---|---|---|---|
| tester | QA suite | IN PROGRESS | Mar 28 |
| safety | Audit | WAITING | — |
```

## current-state.md Format (CEO-written, per department)

```markdown
# Strategy Department — State
Updated: 2026-03-28 23:00 IST

Status: BUSY
Task: Running office-hours for blog-platform
Project: blog-platform
Estimated: 20 min
Blocked: no
```

## Communication Flow

**Manual mode (default):**
```
User → CEO → Department → CEO → Department → ...
```

**Auto mode (explicit switch):**
```
User → CEO → Department → Department → Department → CEO (notification)
```

## Example Flow

```
1. User: "I want to build a todo app"
2. CEO: creates projects/todo-app/ with template
3. CEO: sets strategy/current-state.md → BUSY
4. CEO: spawns strategy → runs office-hours → saves to design/
5. CEO: updates STATUS.md, sets strategy/current-state.md → FREE
6. User: approves design
7. CEO: sets shipping/current-state.md → BUSY
8. CEO: spawns shipper → reviews code → saves to reviews/
9. CEO: updates STATUS.md, sets shipping/current-state.md → FREE
10. CEO: sets testing/current-state.md → BUSY
11. CEO: spawns tester → runs QA → saves to qa/
12. CEO: updates STATUS.md, sets testing/current-state.md → FREE
13. CEO: spawns shipper → deploys → updates deploy-log.md
14. CEO: updates STATUS.md → DEPLOYED
15. CEO: spawns observer → writes retro → saves to history/
```

CEO touches STATUS.md + current-state.md after EVERY step.

## Tool Policy (per agent)

| Tool | CEO | Strategy | Shipper | Tester | Safety | Observer |
|---|---|---|---|---|---|---|
| read | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| write | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| edit | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| exec | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| process | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| browser | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| image | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |
| web_search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| web_fetch | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| memory_search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| memory_get | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sessions_spawn | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| sessions_send | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| sessions_list | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| message | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| cron | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| gateway | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| nodes | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| canvas | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| tts | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| image_generate | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| apply_patch | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Rules:**
- Only CEO, Strategy, Shipper can write files
- Tester, Safety, Observer are read-only on code — they report, CEO decides
- CEO has everything (Full preset)
- Nobody gets: nodes, tts, image_generate, apply_patch (not needed)

## Vision Model

Default vision model: `openrouter/xiaomi/mimo-v2-omni`

Any agent that receives an image and cannot see it must:
1. Spawn a sub-agent with model: `openrouter/xiaomi/mimo-v2-omni`
2. Pass the image file path
3. Ask a specific question about the image
4. Use the answer in its work

Never hallucinate image descriptions. Either see it via sub-agent or say "I can't see this."
