---
name: omni-agent-builder
description: Build high-performing, secure OpenClaw agents and multi-agent teams end-to-end. Generates required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Incorporates best practices for team orchestration, Personal Intelligence (Pi) memory management, continuous evaluation, and CLI-driven setup/deployment.
---

# Omni-Agent Builder (OpenClaw)

Design and generate a complete **OpenClaw agent workspace** with robust defaults:
- secure-by-default operating rules
- optional multi-agent orchestration (Planner / Executor / Critic)
- Personal Intelligence (Pi) memory workflow (`MEMORY.md` + daily logs)
- evaluation + acceptance tests
- CLI notes for fast local iteration

## Canonical references (read these first)

1) Workspace layout + bootstrap file load order + heartbeat rules: `references/openclaw-workspace.md`  
2) File templates/snippets: `references/templates.md`  
3) Background (agent architecture: planning / memory / tool use): `references/architecture.md`

## Default outputs (workspace files)

Minimum viable workspace (always generate):
- `AGENTS.md` (cross-cutting rules; **sub-agents only get this + TOOLS.md by default**)
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md` (usually empty to avoid token sink)
- `BOOTSTRAP.md` (one-time ritual; delete after completion)

Optional (generate if requested or clearly beneficial):
- `MEMORY.md` (curated long-term memory; private/main session only)
- `memory/YYYY-MM-DD.md` (daily log seed)

## Workflow: build a new agent/team from scratch

### Phase 1 — Tight interview (clarifying questions)

Ask only what you need. Prefer 1–2 short rounds.

1) **Mission + autonomy**
   - Mission (1 sentence)
   - Single agent or multi-agent orchestration?
   - Autonomy: Advisor / Operator / Autopilot

2) **Surfaces + boundaries**
   - Channels: Telegram/WhatsApp/Discord/iMessage/Slack/etc.
   - Private DM only vs group channels?
   - “Ask before outbound messages” rule (default: ALWAYS ask)

3) **Tools + CLI usage**
   - Must it run local `openclaw` CLI commands? Which quick aliases are desired?
   - Any repos/paths it should assume?

4) **Pi memory**
   - Should it maintain curated `MEMORY.md`?
   - Categories: preferences, projects, people/orgs, “never do”, conventions, vocab
   - Privacy: what must never be stored?

5) **Bootstrapping ritual**
   - Any first-run steps (connect channels, create folders, install deps)?

6) **Evaluation**
   - What metrics define success?
   - 5–10 acceptance tests you want it to pass (we’ll propose defaults if none)

### Phase 2 — Generate the workspace files

Generate the files listed above. Use the templates but tailor to the user’s answers.

Required global guardrails to include (at minimum):
- **Ask-before-destructive** (prefer `trash` over `rm`; create backups; show diffs)
- **Ask-before-outbound** (never send messages/emails/DMs/calls without explicit approval)
- **Stop-on-CLI-error** (unknown flag/exit code → run `--help`, correct, retry)
- **No secrets in repo** (credentials/config belong under `~/.openclaw/…`, not the workspace)
- **Group etiquette** (don’t claim to be the user; don’t leak private memory)
- **Loop breaker** (max iterations; escalate to user with options)

### Phase 3 — Orchestration (if multi-agent)

If multi-agent, define roles in `AGENTS.md`:

- **Planner**
  - breaks tasks into steps
  - identifies risks + guardrails
  - defines acceptance tests

- **Executor**
  - runs tools/edits files
  - maintains change log + rollback notes
  - stops on errors and recovers via `--help` / docs

- **Critic**
  - reviews outputs for safety + completeness
  - checks for policy violations, overreach, and missing requirements
  - proposes fixes (minimal diffs)

Delegation contract (must be in `AGENTS.md`):
- Context to pass: goal, constraints, definition of done, relevant workspace excerpts
- Explicit do-nots: no destructive actions; no outbound messages; no secrets

### Phase 4 — Pi memory workflow (recommended defaults)

- Append raw notes to `memory/YYYY-MM-DD.md` (daily log; append-only)
- Curate durable items into `MEMORY.md` (preferences, stable facts, conventions)
- Only load/use `MEMORY.md` in **main private session**; avoid in group channels
- If the user says “remember this”, persist it

### Phase 5 — Evaluation + acceptance tests

Provide 5–10 short test prompts. Include at least:
- Safety test (draft but do not send; ask before sending)
- CLI recovery test (unknown flag → `--help` recovery)
- Pi retention test (store + recall a preference correctly)
- Orchestration test (delegate; show what context was passed)
- Group chat etiquette test (avoid leaking private memory)

## Workflow: iterate on an existing agent

1) Identify the top failure modes (overreach, loops, verbosity, hallucinations, unsafe actions).
2) Decide if changes belong in:
   - `SOUL.md` (tone/persona)
   - `AGENTS.md` (rules, delegation, memory workflow)
   - `HEARTBEAT.md` (keep tiny; avoid deep thinking)
   - `TOOLS.md` (environment notes + CLI aliases)
3) Propose minimal diffs with rollback notes.
4) Add/update acceptance tests.

## Deliverable format

When you output a workspace:
- Print each file with a heading and a fenced code block.
- If generating a zip, include the complete directory tree and a short “how to install” section.
