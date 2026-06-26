---
name: create-team
description: Builds a runnable Claude Code Agent Teams skill package — produces SKILL.md as a lead-operator playbook, agents/<role>.md subagent definitions for runtime spawning, references/<role>.md role specs with 8 sections (Scope/Inputs/Outputs/Boundaries + Spawn Prompt/Owned Paths/Task Template/Plan Approval), and optional hooks/. Use when the user wants a reusable multi-agent team that the team lead can spawn end-to-end, not just static role documentation.
metadata:
  version: "2.0"
  language: en
---

# Create A Runnable Agent Team Skill

## When To Use

Use this skill when the user needs a **runnable** team package that a Claude Code team lead can execute end-to-end:

- Spawn teammates via `Agent({subagent_type, team_name, name, prompt})` with prompts already templated
- Seed tasks with `blockedBy` dependencies pre-mapped
- Trust that file ownership across roles is conflict-free
- Tear down the team cleanly when done

If the user only needs pretty role docs (no intent to actually run a team), this skill is overkill — write plain markdown instead.

## Alignment With Agent Teams Runtime

Read [`../agent-teams.md`](../agent-teams.md) (or the live page at `code.claude.com`) for the runtime model. Key points this skill encodes:

- **Subagent definitions are reusable** — teammates can be spawned with `subagent_type: <role>` if a definition exists at `.claude/agents/<role>.md` (project) or `~/.claude/agents/<role>.md` (user). The definition's `tools` allowlist and `model` are honored at runtime.
- **3–5 teammates, 5–6 tasks each** — the documented sweet spot.
- **Avoid file conflicts** — two teammates editing the same file overwrite each other; design Owned Paths so they don't overlap.
- **Lead is fixed for team lifetime** — the SKILL.md plays the role of operating manual for that single lead.
- **Teardown order matters** — shut down each teammate before `TeamDelete`, or you'll leak resources.

## Output Structure

```text
<skill-root>/                      # same as `name`, lowercase-hyphen
├── SKILL.md                       # lead's operating playbook
├── agents/                        # source of truth for subagent definitions
│   ├── <role-a>.md                #   frontmatter: name/description/tools/model
│   └── <role-b>.md
├── references/
│   ├── member.md                  # role index + suggested invocation order
│   ├── <role-a>.md                # 8-section role spec
│   └── <role-b>.md
└── hooks/                         # optional quality gates
    ├── teammate-idle.sh
    └── task-completed.sh
```

`agents/*.md` are **source files**. To make them runtime-discoverable, the lead either copies or symlinks them into `.claude/agents/` (project scope) or `~/.claude/agents/` (user scope) — see Bootstrap step in the generated SKILL.md.

## Workflow

### 1. Preflight (clarify with user)

Confirm before writing anything:

- **Team domain and closed loop** — what end-to-end outcome the team owns.
- **Skill root and `name`** — must match exactly; lowercase-hyphen (e.g. `code-review-team`).
- **Role count and slugs** — target **3–5 roles**; if the user wants 1–2 roles, recommend subagents instead; if >6, propose merging.
- **Roles can run truly in parallel?** — if they all need the same files, this should be sequential, not a team.
- **Runtime preconditions** — note in SKILL.md that the lead must verify Claude Code ≥2.1.32 and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

### 2. Define each role (8 sections, not 4)

For every role, fill all 8 sections (full skeleton in [references/templates.md](references/templates.md)):

| # | Section | Purpose |
|---|---------|---------|
| 1 | Scope | What the role delivers |
| 2 | Inputs | What it needs from user/peers |
| 3 | Outputs | Artifacts produced |
| 4 | Boundaries | Explicit non-goals |
| 5 | **Spawn Prompt** | Verbatim text the lead pastes into `Agent({prompt})` |
| 6 | **Owned Paths** | File globs this role exclusively writes (cross-role overlap forbidden) |
| 7 | **Task Template** | 3–6 typical tasks with `blockedBy` edges |
| 8 | **Plan Approval** | `true` for risky/architectural roles, else `false` |

### 3. Generate dual-track artifacts per role

- `agents/<slug>.md` — subagent definition. Frontmatter: `name`, `description`, `tools` allowlist, `model`. Body = role's operating instructions (this is appended to the teammate's system prompt at spawn).
- `references/<slug>.md` — full 8-section spec. This is for humans and for the lead to reference; **not** loaded into teammate context automatically.

Keep them in sync — drift between `agents/` and `references/` is the #1 failure mode.

### 4. Write SKILL.md as a lead playbook

Required sections (skeleton in [references/templates.md](references/templates.md)):

1. **Preflight** — env var check, version check, `teammateMode` choice
2. **Install agents** — copy/symlink `agents/*.md` to `.claude/agents/` so `subagent_type` works
3. **Bootstrap** — concrete `TeamCreate` + per-role `Agent` calls with the spawn prompts wired up
4. **Task seeding** — `TaskCreate` calls with `addBlockedBy` mapped from each role's Task Template
5. **Steady state** — when to `SendMessage`, how to handle `plan_approval_request`, when to wait
6. **Teardown** — per-teammate `shutdown_request` loop, then `TeamDelete`
7. **Known Limits** — fixed lead, no `/resume` of in-process teammates, permissions set at spawn

### 5. (Optional) Add hooks/

For quality gates — see `references/templates.md` "Hooks" section. Wire them via project `.claude/settings.json`. Examples:

- `TeammateIdle` exit code 2 → block idle until tests pass
- `TaskCompleted` exit code 2 → block completion if acceptance artifact missing

### 6. Self-check

Run [references/checklist.md](references/checklist.md). The hardest constraint: **Owned Paths must have zero cross-role overlap**.

## Key Design Rules

1. **Dual-track or nothing** — every role gets both `agents/<slug>.md` and `references/<slug>.md`. One without the other is a half-built team.
2. **No file conflicts at design time** — overlapping Owned Paths = guaranteed runtime overwrite. Refactor roles until disjoint.
3. **Spawn prompts are self-contained** — a teammate doesn't read the references/ folder unless told to. The Spawn Prompt must include all task-specific context the teammate needs.
4. **Sized for runtime** — 3–5 roles, 5–6 tasks per role. More = coordination overhead eats the gains (see agent-teams.md).
5. **Teardown is part of the spec** — every team SKILL.md ends with a shutdown sequence. Skipping this leaks tmux sessions and team configs.

## References

- Skeletons (SKILL.md / agents/ / references/<role>.md / hooks): [references/templates.md](references/templates.md)
- Validation checklist (run before declaring done): [references/checklist.md](references/checklist.md)
- Worked example: `../code-review-team/` — a 3-person parallel PR review team

## Common Edge Cases

- **1–2 roles** — recommend [subagents](https://code.claude.com/docs/en/sub-agents) instead. Agent Teams overhead doesn't pay off below 3.
- **>6 roles** — merge until ≤5; coordination overhead grows superlinearly.
- **Roles share files** — split the file or merge the roles. Don't ship overlapping Owned Paths.
- **One role is the bottleneck** — split its Task Template into more granular tasks (5–6/role rule), or split into two roles with a clean handoff.
- **User has existing role docs** — normalize slugs/file names first, then backfill the 4 new sections (Spawn Prompt / Owned Paths / Task Template / Plan Approval) and generate `agents/`.
