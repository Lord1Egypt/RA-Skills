# Execution Reference

## Model Management

### Cataloguing Procedure
1. **Discover** — Read OpenClaw config, probe endpoints, check provider APIs
2. **Interview** — Go through each uncatalogued model with the user
3. **Research** — Web search + fetch benchmarks
4. **Synthesize** — Combine into `orchestrator-data/models.json`
5. **Route** — Update routing rules

### Resource Awareness
Before spawning a subagent, check:
- Current model and usage (via `session_status`)
- Provider health and rate limits
- Fallback chain if primary model fails

## Project Onboarding

### Quick Start
```
# New project:
bash scripts/init-project.sh ~/projects/<name> "<Name>" "<stack>"

# Existing project (just add planning):
bash scripts/init-project.sh ~/projects/<name> "<Name>"
```

### Step-by-Step

#### 1. Project Info
Collect: path, name, tech stack, one-line summary, new vs existing.

#### 2. Scaffold
```
bash scripts/init-project.sh <path> "<Name>" "<stack>"

Creates .planning/:
├── CONFIG.md        — ports, env vars, build commands
├── STATE.md         — current state
├── ROADMAP.md       — planned work with priorities
├── REQUIREMENTS.md  — functional + non-functional
├── ADRs/            — architecture decision records
└── AUDIT.md         — audit findings
```

#### 3. Codebase Intelligence (existing projects)
```
exec find . -name '*.package.json' -o -name '*.py' -o -name '*.ts' | head -50
```
Detect tech stack from config files. List key directories and entry points. Note test framework, build system, deployment config.

#### 4. Requirements
Capture: what it does, who it's for, pain points, constraints.

#### 5. Architecture Documentation
Create ADRs for early decisions:
```
bash scripts/log-decision.sh <path> "<Title>" "<Context>" "<Decision>" "[Alternatives]" "[Consequences]"
```

Update CONFIG.md with ports, env vars, build commands, database URLs.

#### 6. Track
```
bash scripts/log-session.sh <project> "Project onboarding" "-" complete
```

## Planning & Design

### The Plan Tool
Always call `update_plan` for anything beyond a single read/edit.

### Work Sizing
- **Small** (1-3 files) → one-shot ACP agent
- **Medium** (3-8 files) → one-shot ACP agent with detailed spec
- **Large** (8+ files) → decompose into parallel waves

## Execution Details

### Cursor / ACP Agent Prompt Template
```
## Task: [TITLE]
**Project:** /path/to/project
**Context:** 2-3 sentences

### Files to modify:
- path/to/file — what to change

### Requirements:
1. Concrete requirements

### Constraints:
- Non-negotiables

### IMPORTANT RULES:
- READ files first
- DO NOT touch unrelated files
- Run build after changes

### Testing criteria:
- What to verify
```

### ACP Fallback Chain
1. ACP agent fails → fix prompt, retry
2. Still fails → CLI variant
3. Subscription exhausted → alternative ACP
4. All unavailable → manual `edit` tool

### Parallel Execution
Group independent tasks (no shared files). Max 4 concurrent. `sessions_yield` to wait. Fallback: serial.

## Verification

### Gate — NEVER SKIP
Build → Test → Lint → Typecheck. Show command output as evidence.

### Vision Q&A (UI changes)
Screenshot → vision analysis. Fallback: cloud vision → local → describe.

### Self-Review Checklist
```
[ ] Codebase understood first?
[ ] Used plan tool?
[ ] Build passes?
[ ] Tests pass?
[ ] Visual correct (if UI)?
[ ] Read agent output before trusting?
[ ] No side effects?
[ ] Logged to memory?
[ ] Updated STATE.md?
```

## Logging & Tracking

### Session Logging
```
bash scripts/log-session.sh <project> <task> <model> <status> [notes] [agent] [duration] [qa_done] [checked]
```

Arguments: project, task, model, status (complete|partial|failed|blocked), notes, agent (subagent|cursor|acp|shell), duration_min, qa_done (true|false), checked (true|false).

### Decision Logging
```
bash scripts/log-decision.sh <path> <title> <context> <decision> [alternatives] [consequences]
```

### State & Roadmap
Keep `.planning/STATE.md` and `.planning/ROADMAP.md` current after every session.

### Cross-Session Resume
Session state files in `orchestrator-data/sessions/` persist across OpenClaw sessions. Read the last session state file to continue where you left off.
