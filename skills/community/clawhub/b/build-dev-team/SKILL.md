---
name: build_development_team
description: >
  Builds and configures a complete AI software development team inside OpenClaw,
  including the full project folder structure, agent coordination workflow, and
  vision-capable model handoffs for mockup-driven UI work. Use this skill whenever
  someone says "build a software development team", "set up my dev team",
  "configure the agent team", "set up a project", "add a project to my team",
  "how do agents work together on a project", "set up project coordination",
  "create a project folder", "wire up Asana for my team", "add mockup support
  to my dev team", or anything similar — even if they don't use the word "skill"
  or explicitly ask for setup. Also trigger when someone is troubleshooting a
  multi-agent dev setup, asking how PM/engineer/QA/devs should coordinate, or
  asking about sprint workflow, branch conventions, queue files, or project-lock
  state. This skill covers the full setup: safety snapshot, agent creation, model
  selection (with hallucination-aware picks and per-agent vision configuration),
  skills installation, Asana project setup, GitHub repo wiring, agent-to-agent
  communication, mockup storage convention (Asana attachments primary, project
  workspace fallback), and the complete project folder structure that coordinates
  agents across sprints — including PROJECT.md, project.json, queue files, shared
  workspace, spec versioning, decision logging, and sprint open/close procedures.
  Requires the openclaw-administrator skill (EncryptShawn) to be loaded.
  Recommends openclaw-recovery-manager (EncryptShawn) for safety.
  This skill does not make Asana or GitHub API calls itself — those are delegated
  to separately installed Asana and Git dependency skills.
  This skill does not read or store any credentials or secret values.
---

# Build a Software Development Team

This skill sets up a complete AI-powered software development team inside your OpenClaw instance. It covers two layers:

1. **Agent setup** — creating and configuring each agent (models, skills, routing, workspace files)
2. **Project setup** — creating the project folder structure that coordinates agents across sprints

Both layers are required for a fully working team. Use the table of contents below to jump to the relevant section.

---

## Contents

- [Credential and Security Model](#credential-and-security-model)
- [Heartbeat Scheduling](#heartbeat-scheduling)
- [Agent Workspace Files](#agent-workspace-files)
- [Before You Start](#before-you-start--required-skills)
- [Step 0 — Safety First](#step-0--safety-first)
- [Step 1 — Gather Project Information](#step-1--gather-project-information)
- [Step 2 — Model Selection](#step-2--model-selection)
- [Step 3 — Skills Selection Per Agent](#step-3--skills-selection-per-agent)
- [Step 4 — Agent Configuration](#step-4--agent-configuration)
- [Step 5 — Asana Project Setup](#step-5--asana-project-setup)
- [Step 6 — Write Agent Workspace Files](#step-6--write-agent-workspace-files)
- [Step 7 — Create Project Folder Structure](#step-7--create-project-folder-structure)
- [Step 8 — Credential Verification](#step-8--credential-verification)
- [Step 9 — Enable Chat Completions](#step-9--enable-chat-completions)
- [Step 10 — Smoke Test](#step-10--smoke-test)
- [Step 11 — Post-Setup Snapshot](#step-11--post-setup-snapshot)
- [Step 12 — Handoff Summary](#step-12--handoff-summary)
- [Project Workflow Reference](#project-workflow-reference)
- [Sprint Management](#sprint-management)
- [If Anything Goes Wrong](#if-anything-goes-wrong)

Reference files (read when needed):
- `references/project-files.md` — Full specification of every project folder file, its format, and its content rules
- `references/workflow.md` — Complete agent workflow: all phases, escalation rules, queue formats, git conventions

---

## Credential and Security Model

**This skill does not read, store, request, or transmit any credentials or secret values.**

All credential handling is performed by:
- The **openclaw-administrator** skill, which uses OpenClaw's own config management to wire agent settings
- The **Asana dependency skill** installed on each agent, which holds and uses the Asana PAT
- The **Git dependency skill** installed on each agent, which holds and uses the GitHub PAT
- The **Email dependency skill** installed on the PM agent, which holds and uses email credentials

This skill collects only the *names* of env vars (e.g., `TA_ASANA_PAT`) — never their values. Those env var names are passed to the dependency skills so they know which credential to pull from the agent runtime environment.

Credentials must be stored in your secret management system (Kubernetes ConfigMap/Secret, .env file, or equivalent) before setup begins.

---

## Heartbeat Scheduling

The 30-minute agent heartbeats configured in this setup are scheduled and triggered by the **OpenClaw platform**, not by this skill. This skill instructs the openclaw-administrator skill to set the heartbeat interval in each agent's OpenClaw config. This skill does not self-invoke, set timers, or persist between sessions.

### Heartbeat Model Selection

Heartbeat runs must use the **cheapest available model**, not the agent's primary model. The selection priority is:

1. **If OpenRouter is configured** → use `openrouter/minimax/minimax-m2.7` (cheapest viable heartbeat model)
2. **If OpenRouter is NOT configured** → use the **cheapest model defined in that agent's config** — this must be identified during Step 4 and recorded in HEARTBEAT.md

> **Why this matters:** Running a heartbeat on a primary model (e.g. Gemini 3.1 Pro or GLM-5.1) every 30 minutes burns significant credits for what is designed to be a near-stateless, fast check. The heartbeat model must be set independently of the agent's active/fallback models.

### Heartbeat Reasoning Level

Heartbeat reasoning must be kept minimal. **Do not add a reasoning/thinking config key to openclaw.json** — that is not a supported heartbeat field. Instead, control reasoning level through the heartbeat prompt. Every HEARTBEAT.md must begin with:

```
/think:minimal
```

This forces the lightest reasoning path the model supports and prevents the agent from treating heartbeat like an active work session.

### Heartbeat Failure — Fail Cheap, Never Escalate to Primary

If a heartbeat check fails (Asana unreachable, bad model config, tool error, etc.), the heartbeat **must stop immediately and fail cheaply**. It must NOT:

- Retry using the agent's primary model
- Spawn a troubleshooting loop
- Use `sessions_send` to self
- Continue reasoning about what might have gone wrong

**The correct behavior on heartbeat failure:** log the failure (if logging is available), reply with a failure notice, and stop. The next scheduled heartbeat will try again. Do not spend primary model credits diagnosing heartbeat problems — those failures are almost always config issues (bad model path, credential not set, Asana connection error) that the operator must fix, not the agent.

This must be documented in each agent's HEARTBEAT.md explicitly.

---

## Agent Workspace Files

This setup process creates and populates the following operator-managed workspace files for each agent:
- **USER.md** — project list, Asana GIDs, repo URLs, team roster. No secret values.
- **TOOLS.md** — available dependency skills and env var name labels each one uses.
- **HEARTBEAT.md** — what to check on each heartbeat run. No secret values.
- **AGENTS.md** — role instructions including active project references and queue check rules.

These are plain text files in each agent's workspace directory. Created once during setup; updated by the operator when projects change.

---

## Before You Start — Required Skills

**Required (install before running this skill):**
- `openclaw-administrator` (EncryptShawn) — performs all agent creation, model assignment, routing config, and workspace file writes.

**Strongly recommended:**
- `openclaw-recovery-manager` (EncryptShawn) — provides config snapshots and emergency rollback.

---

## Step 0 — Safety First

Before touching any configuration:

1. **Check if openclaw-recovery-manager is installed.** If yes, take a snapshot:
   > "Taking a pre-setup configuration snapshot before we begin."
   Label it: `pre-dev-team-setup-[today's date]`

2. If NOT installed, ask:
   > "I recommend installing openclaw-recovery-manager (EncryptShawn on ClawHub) before we proceed. Want to install it first, or proceed without it?"

---

## Step 1 — Gather Project Information

Ask the user for the following. Collect all answers before configuring anything:

```
I need a few details to set up the team correctly.

1. Project name?
   (e.g., talent_avatar — used as the project identifier throughout)

2. Asana workspace GID?
   (Found in your Asana workspace settings or URL)

3. Does an Asana project board already exist for this project?
   - Yes → What is the Asana project GID? (from the board URL)
   - No → I'll guide you through creating one

4. GitHub repository SSH URLs (private repos, SSH access only):
   - Frontend repo: (e.g., git@github.com:org/repo-fe.git)
   - Backend repo: (e.g., git@github.com:org/repo-be.git)
   - Any additional repos?

5. Credential env var names only — do not share token values here.
   What are the names of the env vars in your secret store for:
   - Asana PAT: (e.g., TA_ASANA_PAT)
   - GitHub PAT: (e.g., TA_GITHUB_PAT)
   - Dev Manager email address: (e.g., TA_DEV_MANAGER_EMAIL)

6. PM agent ID for this project?
   (Convention: project_manager_[project_name])
   Press enter to accept the suggested convention.
```

After collecting answers, confirm back with the user before doing anything.

---

## Step 2 — Model Selection

Present model recommendations. Tell the user they can accept or change any agent's model.

**Note: OpenRouter is strongly recommended for access to the full model range.**

**Heartbeat model rule:** If OpenRouter is configured, all agents use `openrouter/minimax/minimax-m2.7` for heartbeat regardless of their primary model. If OpenRouter is NOT available, use the cheapest model in the agent's config — confirm this during agent setup and record it explicitly in HEARTBEAT.md.

```
RECOMMENDED MODEL ASSIGNMENTS
Based on April 2026 SWE-bench Pro and AA-Omniscience hallucination data:

Agent          | Primary                  | Fallback         | Heartbeat            | Vision
---------------|--------------------------|------------------|----------------------|------------------
project_manager| GLM-5.1                  | MiniMax M2.7     | MiniMax M2.7         | —
               | $1.00/$3.20 per 1M       |                  | (OpenRouter)         |
               | 34% H% — lowest of all   |                  | or cheapest avail.   |
engineer       | Gemini 3.1 Pro           | Claude Opus 4.7  | MiniMax M2.7         | Native (primary)
               | $2/$12 per 1M            | (escalation)     | (OpenRouter)         |
dev-fe         | GLM-5.1                  | Qwen 3.6 Plus    | MiniMax M2.7         | Gemini 3.1 Pro
               | $1/$3.20 per 1M          |                  | (OpenRouter)         | (mockup tasks)
dev-be         | GLM-5.1                  | Qwen 3.6 Plus    | MiniMax M2.7         | —
qa             | Gemini 3.1 Pro           | GPT-5.5          | MiniMax M2.7         | Native (primary)
n8n_engineer   | GLM-5.1 (active)         | Qwen 3.6 Plus    | MiniMax M2.7         | —
               | MiniMax M2.7 (heartbeat) |                  | (OpenRouter)         |

Heartbeat model rule:
- All agents use openrouter/minimax/minimax-m2.7 for heartbeat IF OpenRouter is configured.
- If OpenRouter is NOT configured, use the cheapest model in that agent's config.
  Confirm which model that is during agent setup and record it in HEARTBEAT.md.
- Heartbeat reasoning is controlled via /think:minimal at the top of HEARTBEAT.md —
  not via any openclaw.json config key.

Why these picks:
- PM: GLM-5.1 has the lowest hallucination rate (34%) of all 10 frontier models.
  A PM that confidently misrepresents client or engineer statements is dangerous.
  MiniMax M2.7 (39% H%, $0.30/$1.20) is the cheap heartbeat/fallback model.
- Engineer + QA: Gemini 3.1 Pro has native vision — critical for reading mockups,
  rendered UI screenshots, and HTML/CSS visual diffs.
- FE Dev: GLM-5.1 is the default coding model, but switches to Gemini 3.1 Pro
  when a task involves a mockup. See "Vision Tasks" below.
- DeepSeek V4 Pro excluded despite strong benchmarks — 94% hallucination rate
  makes it unsuitable for any agent in this team.

Accept these recommendations? Or tell me which to change.
```

### Vision Tasks (FE Dev and QA)

The FE dev and QA agent both need vision capability for tasks that involve visual
references — mockups, design comps, rendered UI comparisons. Configure them so
Gemini 3.1 Pro is used **only when the task requires vision**, not as the primary
default (which would be more expensive than necessary for non-visual work).

**Configuration approach (via openclaw-administrator):**
- FE dev primary model: GLM-5.1
- FE dev vision model: Gemini 3.1 Pro
- QA primary model: Gemini 3.1 Pro (already vision-capable)
- QA fallback non-vision: GPT-5.5

The FE dev should switch to vision mode when the Asana task description references
a mockup or attached image. The PROJECT.md instructs the FE dev to do this. QA
should use vision mode whenever a PR includes UI changes that need to be compared
against the mockup.

### Mockup Storage

Mockups must be accessible to the engineer (during planning), FE dev (during
implementation), and QA (during review). Two storage paths, in priority order:

1. **Asana attachments (preferred)** — if the Asana skill supports attachment
   upload/retrieval, mockups attach directly to the relevant Asana task. Each
   agent retrieves them via the Asana skill.
2. **Project workspace fallback** — `~/.openclaw/projects/[project_name]/workspace/mockups/`
   - File naming: `[task-id]-[short-description].[ext]` (e.g. `1234-navbar-redesign.png`)
   - The Asana task description must reference the filename so devs and QA can find it
   - This path is pre-created by this skill during Step 7

This mockup convention is documented in PROJECT.md so all agents know the rule.

Wait for confirmation. Record final selections.

---

## Step 3 — Skills Selection Per Agent

Check what's already installed using the openclaw-administrator skill.

### Dependency Skills (Required — Install First)

```
DEPENDENCY SKILLS — install these first on each agent:

All agents:
  - Asana skill (for Asana task management)

Agents that touch code (engineer, dev-fe, dev-be, qa, n8n_engineer):
  - Git skill (for repository operations)

PM agent only:
  - Email skill (for Dev Manager completion alerts)

Search ClawHub for the best-rated version of each if not already installed.
```

### EncryptShawn Workflow Skills (All Agents)

```
- openclaw-administrator
- openclaw-recovery-manager
- approved-self-improver
```

### Role-Specific Workflow Skills

```
project_manager_[project]: dev-project-manager (EncryptShawn)
engineer:                  dev-project-engineer (EncryptShawn)
dev-fe, dev-be, n8n:       project-dev (EncryptShawn)
```

### Tech Stack Skills

```
Tech stack questions:

1. Frontend: Next.js / Nuxt / React / Vue / Astro / Flutter / other?
2. Backend: NestJS / Node.js / Python / Golang / other?
3. Database: MySQL / PostgreSQL / MongoDB / ClickHouse / Redis / other?
4. Using Directus as CMS or API layer? Yes / No
5. Using AWS Cognito for auth? Yes / No
6. Using N8N for automation? Yes / No
7. Using Qdrant for vector search? Yes / No
```

Based on answers, recommend and install appropriate ClawHub skills per agent.

---

## Step 4 — Agent Configuration

Using the openclaw-administrator skill, configure each agent:

### project_manager_[project]
- Model (active): GLM-5.1 (or user choice from Step 2)
- Model (heartbeat): MiniMax M2.7 (cheap heartbeat loop)
- Fallback: MiniMax M2.7
- Heartbeat: every 30 minutes, isolated session, light context
- Repos: read-only access to all repos
- Agent-to-agent allow list: engineer, dev-fe, dev-be, qa, n8n_engineer (if applicable)
- Chat completions: ENABLED

### engineer
- Model (active): Gemini 3.1 Pro (native vision — required for mockup review)
- Fallback: Claude Opus 4.7 (escalation only)
- Heartbeat model: MiniMax M2.7 via OpenRouter (or cheapest available if no OpenRouter)
- Heartbeat: every 30 minutes
- Repos: read-only access to all repos (read/write only when explicitly helping a dev)
- Agent-to-agent allow list: [PM agent ID], dev-fe, dev-be, qa, n8n_engineer
- Chat completions: disabled

### dev-fe
- Model (primary): GLM-5.1
- Model (vision): Gemini 3.1 Pro — used when task involves mockup/image references
- Fallback: Qwen 3.6 Plus
- Heartbeat model: MiniMax M2.7 via OpenRouter (or cheapest available if no OpenRouter)
- Heartbeat: every 30 minutes
- Repos: frontend repo (read/write)
- Agent-to-agent allow list: [PM agent ID], engineer, qa
- Chat completions: disabled

### dev-be
- Model (primary): GLM-5.1
- Fallback: Qwen 3.6 Plus
- Heartbeat model: MiniMax M2.7 via OpenRouter (or cheapest available if no OpenRouter)
- Heartbeat: every 30 minutes
- Repos: backend repo (read/write)
- Agent-to-agent allow list: [PM agent ID], engineer, qa
- Chat completions: disabled

### qa
- Model (primary): Gemini 3.1 Pro (native vision — required for UI/mockup comparison)
- Fallback (non-vision): GPT-5.5
- Heartbeat model: MiniMax M2.7 via OpenRouter (or cheapest available if no OpenRouter)
- Repos: all repos (read-only, plus merge authority on operator instruction)
- Agent-to-agent allow list: [PM agent ID], engineer, dev-fe, dev-be
- Chat completions: disabled

### n8n_engineer (only if N8N confirmed in Step 3)
- Model (active): GLM-5.1
- Model (heartbeat): MiniMax M2.7
- Fallback: Qwen 3.6 Plus
- Repos: backend repo
- Agent-to-agent allow list: [PM agent ID], engineer, qa
- Chat completions: disabled

After all agents configured, verify:
```
openclaw agents list
Confirm all agents show configured status with correct models.
```

---

## Step 5 — Asana Project Setup

### If board does NOT exist yet

```
Create the Asana board manually:

1. Log into Asana → + New Project → name it: [project_name] → Board view
2. Create these columns in this exact order:
   - Backlog
   - PM Queue
   - Engineer Queue
   - Frontend Dev Queue
   - Backend Dev Queue
   - QA Queue
   [- N8N Engineer Queue — only if using N8N]
   - In Progress
   - QA Review
   - Complete
   - Blocked
3. Invite all agent Asana accounts as Members
4. Copy the project GID from the board URL
5. Share the GID here when ready
```

### Once GID is confirmed

Using the Asana dependency skill, add project description to the board:
```
Project: [project_name]
PM Agent: [pm_agent_id]
Repos: FE: [fe_repo] | BE: [be_repo]
Asana Project GID: [GID]
Dev Manager Email env var: [env_var_name — label only]
```

---

## Step 6 — Write Agent Workspace Files

Using the openclaw-administrator skill, write the following files for each agent.

**HEARTBEAT.md** (per agent — under 200 tokens):

Every HEARTBEAT.md must follow this exact template. Fill in the agent's specific project GID and queue/section GID during setup. The heartbeat must read these values directly — it must **not** perform Asana project discovery on every run.

```markdown
/think:minimal

# HEARTBEAT

## Asana Queue (read this, do not rediscover)
- Project: [project_name]
- Project GID: [asana_project_gid]
- Queue/Section: [Agent Role] Queue
- Queue/Section GID: [section_gid_if_known]

## On each heartbeat
1. Read the project GID and queue/section above — do not browse Asana to find your queue.
2. Query only that exact project + section.
3. Filter for tasks assigned to you only.
4. If no actionable task is assigned → reply HEARTBEAT_OK and stop.
5. If a task is assigned → report it and proceed per your role workflow.
6. If queue metadata above is missing or invalid → do one-time discovery, record the
   project GID and section GID here, then use that direct path from then on.

## Hard rules
- Never use sessions_send to message yourself.
- Never browse other projects, sections, or columns unless queue metadata is missing.
- Never reason about missed or old heartbeats.
- If this heartbeat fails (tool error, bad model config, Asana unreachable):
  log the failure and STOP. Do not retry. Do not escalate to your primary model.
  Do not troubleshoot. The next scheduled heartbeat will try again.
```

> **Note on section GID:** Retrieve the section GID during Step 5 when the Asana board is confirmed. Add it to HEARTBEAT.md at write time so the agent never has to discover it. If the GID isn't available at setup time, leave the field blank — the agent will do a one-time discovery on first heartbeat and write it in.

**USER.md** (per agent):
- Role and scope
- Active Projects table: project name, PM agent ID, Asana GID, repo URLs
- Repo access scope for this agent
- Env var name labels for credential references (not values)
- Team agent roster with agent IDs

**TOOLS.md** (per agent):
- Available dependency skills
- Env var name label each skill uses for its credential
- sessions_send allowed targets

**AGENTS.md** (per agent) — must include an Active Projects section:
```
## Active Projects
- [project_name] — I am the [role] on this project.
  - Full rules: ~/.openclaw/projects/[project_name]/PROJECT.md
  - My queue: ~/.openclaw/projects/[project_name]/queues/to-[role].md
  - Shared workspace: ~/.openclaw/projects/[project_name]/workspace/
  - Check my queue at the start of every session before doing anything else.
  - Check project-lock.json to understand what phase we are in before acting.
```

---

## Step 7 — Create Project Folder Structure

This is the coordination layer that makes agents work together across sprints. Read `references/project-files.md` for the full specification of each file's content and format.

Create the following structure for each project:

```
~/.openclaw/projects/[project_name]/
├── PROJECT.md                    ← Full team rulebook — every agent reads this
├── project.json                  ← Machine-readable config (agents, Asana, paths)
├── project-lock.json             ← Current phase and ownership
├── STATE.md                      ← Human-readable status at a glance
├── SHARED_MEMORY.md              ← Cross-agent knowledge not suited for Asana
├── DECISIONS.md                  ← Immutable log of all requirement decisions
├── KNOWN_ISSUES.md               ← Accepted technical debt and limitations
├── RUNBOOK.md                    ← How to run the project; branch and PR conventions
├── workspace/
│   ├── repo/                     ← The git repository (cloned here)
│   ├── mockups/                  ← Design mockups (fallback if Asana attachments unavailable)
│   ├── SPEC-CURRENT.md           ← Points to the active accepted spec
│   └── IMPLEMENTATION_GUIDE.md   ← Engineer's task-oriented implementation plan
└── queues/
    ├── to-pm.md
    ├── to-engineer.md
    ├── to-engineer-feasibility.md ← Requirements phase only — kept separate
    ├── to-qa.md
    └── to-operator.md
```

### Creating Each File

**project.json** — fill in from the details collected in Step 1:
```json
{
  "id": "[project_name]",
  "name": "[Project Display Name]",
  "asana": {
    "project_id": "[asana_project_gid]",
    "workspace_id": "[asana_workspace_gid]",
    "columns": {
      "backlog":     { "id": "[col_gid]", "purpose": "Work not yet started. PM creates tasks here." },
      "in_progress": { "id": "[col_gid]", "purpose": "Dev actively working on this." },
      "in_review":   { "id": "[col_gid]", "purpose": "PR submitted. QA should pick this up." },
      "qa":          { "id": "[col_gid]", "purpose": "QA is actively testing." },
      "completed":   { "id": "[col_gid]", "purpose": "QA passed. Awaiting operator merge and sign-off." },
      "blocked":     { "id": "[col_gid]", "purpose": "Waiting on client or external input. PM owns." }
    }
  },
  "participants": [
    { "agentId": "[pm_agent_id]", "workspace": "../../workspace-pm",     "role": "Project Manager" },
    { "agentId": "engineer",      "workspace": "../../workspace-main",   "role": "Lead Engineer" },
    { "agentId": "dev-fe",        "workspace": "../../workspace-dev0fe", "role": "Front-end Developer" },
    { "agentId": "dev-be",        "workspace": "../../workspace-dev0be", "role": "Back-end Developer" },
    { "agentId": "qa",            "workspace": "../../workspace-qa",     "role": "QA Engineer" }
  ],
  "shared_workspace": "./workspace",
  "repo_path": "./workspace/repo",
  "mockups_path": "./workspace/mockups",
  "shared_memory": "./SHARED_MEMORY.md",
  "decisions_log": "./DECISIONS.md",
  "known_issues": "./KNOWN_ISSUES.md",
  "runbook": "./RUNBOOK.md",
  "queues": {
    "pm":                   "./queues/to-pm.md",
    "engineer":             "./queues/to-engineer.md",
    "engineer_feasibility": "./queues/to-engineer-feasibility.md",
    "qa":                   "./queues/to-qa.md",
    "operator":             "./queues/to-operator.md"
  },
  "visual_assets": {
    "primary_storage": "asana_attachments",
    "fallback_storage": "./workspace/mockups",
    "naming_convention": "[task-id]-[short-description].[ext]",
    "vision_required_agents": ["engineer", "dev-fe", "qa"]
  },
  "escalation_rules": {
    "client_no_response_hours": 48,
    "dev_stuck_same_issue_escalations": 2,
    "dev_stuck_same_issue_hours": 24,
    "blocked_task_operator_escalation_hours": 48
  }
}
```

**project-lock.json** — initialize to idle:
```json
{
  "phase": "idle",
  "sprint_id": null,
  "sprint_opened": null,
  "waiting_on": null,
  "last_updated": "[today's date]",
  "last_updated_by": "operator",
  "context": "Project initialized. Ready to receive first requirements.",
  "blocked_tasks": []
}
```

**Initialize all queue files** as empty with a header comment:
```
# Queue: to-[role]
# Format: [YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: task-id or N/A]
# Queues are append-only. Archive at sprint close. Never delete entries.
```

**Initialize STATE.md**:
```markdown
# [Project Display Name] — Current State
**Phase:** Idle — Ready for first requirements
**Last updated:** [today's date] by operator
```

**Initialize SHARED_MEMORY.md, DECISIONS.md, KNOWN_ISSUES.md** with a header and empty body.

**Clone the repo and create mockups dir** in `./workspace/`:
```bash
cd ~/.openclaw/projects/[project_name]/workspace
git clone [repo_ssh_url] repo
mkdir -p mockups
```

**Write PROJECT.md** — read `references/project-files.md` for the full template and content rules. This is the most important file. Fill it in completely using the project details from Step 1 and the Asana column GIDs from Step 5.

**Write RUNBOOK.md** — stub it out now; the engineer fills in codebase details after their first session with the repo.

---

## Step 8 — Credential Verification

```
Credential check — confirm in your secret management system:

- [ASANA_PAT_ENV_VAR_NAME] — Asana personal access token
- [GITHUB_PAT_ENV_VAR_NAME] — GitHub personal access token
- [DEV_MANAGER_EMAIL_ENV_VAR_NAME] — Dev Manager email address

Confirm they exist before continuing. (yes / one or more missing)
```

---

## Step 9 — Enable Chat Completions

Using the openclaw-administrator skill, enable chat completions for the PM agent.

---

## Step 10 — Smoke Test

```
SMOKE TEST

Step 1: Create a test task in the Asana PM Queue:
  Title: [TEST] Smoke test — verify agent pickup
  Description: Test task. Agent should acknowledge and move task or add a comment.

Step 2: Wait up to 30 minutes for the PM agent's next heartbeat.
  Watch for: task gaining a comment, or task moving to another column.

Step 3: Once PM confirmed working, send via chat completions:
  "Bug report for [project_name]: Login throws a 500 error when
   email field is left blank. Expected: show a validation error."

Step 4: Watch for task creation in the Engineer Queue on the Asana board.

Step 5: Confirm engineer picks up the task and produces an assessment.

Step 6: Verify the project folder exists and queue files are accessible by agents.

Heartbeat confirmed working? (yes / no — describe what happened)
```

---

## Step 11 — Post-Setup Snapshot

If openclaw-recovery-manager is installed:
```
Taking post-setup snapshot.
Label: post-dev-team-setup-[today's date]-confirmed
```

---

## Step 12 — Handoff Summary

```
TEAM SETUP COMPLETE

Project: [project_name]
Asana Project GID: [GID]
PM Agent: [pm_agent_id] — chat completions ENABLED
Project folder: ~/.openclaw/projects/[project_name]/

AGENTS:
Agent            | Primary Model         | Fallback         | Heartbeat            | Vision
[pm_agent_id]    | GLM-5.1               | MiniMax M2.7     | MiniMax M2.7*        | —
engineer         | Gemini 3.1 Pro        | Claude Opus 4.7  | MiniMax M2.7*        | Native
dev-fe           | GLM-5.1               | Qwen 3.6 Plus    | MiniMax M2.7*        | Gemini 3.1 Pro
dev-be           | GLM-5.1               | Qwen 3.6 Plus    | MiniMax M2.7*        | —
qa               | Gemini 3.1 Pro        | GPT-5.5          | MiniMax M2.7*        | Native
[n8n_engineer]   | GLM-5.1               | Qwen 3.6 Plus    | MiniMax M2.7*        | —

* via OpenRouter. If OpenRouter not configured, cheapest available model as recorded in each agent's HEARTBEAT.md.

REPOS (SSH):
Frontend: [fe_repo]
Backend:  [be_repo]
Cloned to: ~/.openclaw/projects/[project_name]/workspace/repo/

HOW PROJECTS WORK:
- All agents read ~/.openclaw/projects/[project_name]/PROJECT.md for workflow rules
- Each agent checks their queue file at every session start
- Asana is the source of truth for task ownership and status
- project-lock.json tracks which phase the sprint is in
- One sprint at a time — PM does not accept new requirements until sprint is closed

TO START THE FIRST SPRINT:
  Send requirements to [pm_agent_id] via chat completions.
  The PM will open a feasibility discussion with the engineer,
  negotiate with the client, and open the sprint once requirements are accepted.

ADDING A NEW PROJECT:
- Run this skill again for the new project
- Add the new project to each shared agent's AGENTS.md Active Projects section
- Add the new PM to agent-to-agent allow lists
- Shared agents pick up new projects automatically on next heartbeat

RECOVERY:
Pre-setup:  pre-dev-team-setup-[date]
Post-setup: post-dev-team-setup-[date]-confirmed
```

---

## Project Workflow Reference

For the complete workflow that agents follow after setup, see:
- `references/workflow.md` — All phases (requirements through sprint close), escalation rules, queue message format, git and branch conventions, QA process, operator merge procedure

Read this file when:
- Troubleshooting agent behavior during a sprint
- Answering operator questions about how the team works
- Explaining why an agent stopped work or escalated

---

## Sprint Management

### Opening a Sprint
The PM opens a sprint automatically when requirements are accepted by both the engineer and client. The PM updates `project-lock.json` phase to `implementation` and creates Asana tasks from the implementation guide.

### During a Sprint
- Agents check `project-lock.json` phase before acting
- Devs work one branch per sprint, pushing updates — PR auto-updates each time
- QA re-reviews after each dev push
- Operator is notified via `to-operator.md` when QA passes all tasks

### Closing a Sprint (Operator-Led)
When `to-operator.md` shows all tasks QA-passed:

1. Operator reviews and pulls the branch locally
2. Operator tells QA agent: "Merge to main"
3. QA merges the PR to main
4. All affected repos rebase to main
5. Operator confirms rebase is clean
6. Operator tells PM: "Sprint closed — ready for next requirements"
7. PM clears Asana, archives queue entries, updates STATE.md to idle
8. `project-lock.json` resets to `idle`

**One sprint at a time.** PM does not accept new requirements until `project-lock.json` is `idle`.

---

## If Anything Goes Wrong

```
Option 1 — Recover using openclaw-recovery-manager:
  Restore: pre-dev-team-setup-[date]

Option 2 — Diagnose with openclaw-administrator:
  Run diagnostics and retry the failed step.

Option 3 — Describe what step failed and what error appeared.
  I can walk through the failed step again.
```
