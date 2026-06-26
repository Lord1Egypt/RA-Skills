# Templates

Replace `{PLACEHOLDERS}` as needed. Naming: `{SKILL_NAME}` and all `{ROLE_SLUG}` values must be `a-z 0-9 -`, no leading/trailing `-`, no `--`.

Placeholder keys:
- `{SKILL_ROOT}` — folder name, equal to `{SKILL_NAME}`
- `{SKILL_NAME}` — YAML `name`, must equal folder
- `{TEAM_TITLE}` — display title (e.g. "Code Review Team")
- `{DESCRIPTION}` — capability + trigger, ≤1024 chars
- `{ROLE_NAME}`, `{ROLE_SLUG}` — per role
- `{TOOLS_ALLOWLIST}` — comma-separated tool names (Read, Grep, Glob, Bash, Edit, Write, ...)
- `{MODEL}` — `opus` | `sonnet` | `haiku` | omit to inherit lead

---

## 1. `SKILL.md` skeleton (lead playbook)

```markdown
---
name: {SKILL_NAME}
description: {DESCRIPTION}
metadata:
  version: "1.0"
---

# {TEAM_TITLE}

## Team Positioning

(One sentence: what closed loop this team owns. List members. List covered phases.)

## Collaboration Principles

1. ... (e.g. file ownership is enforced via Owned Paths — never edit another role's files)
2. ... (e.g. cross-role conflicts escalate to lead via `SendMessage`)
3. ... (e.g. all artifacts land in `outputs/` with role-prefixed filenames)

## Preflight (lead runs once)

- Verify Claude Code version: `claude --version` ≥ 2.1.32
- Verify env: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` returns `1`
- Choose `teammateMode` in `~/.claude/settings.json` (`in-process` or `tmux`)

## Install Agents (one-time per project or user)

Copy or symlink subagent definitions so `subagent_type` resolves:

\```bash
# project scope
mkdir -p .claude/agents
cp {SKILL_ROOT}/agents/*.md .claude/agents/

# OR user scope (reusable across projects)
mkdir -p ~/.claude/agents
ln -sf "$PWD/{SKILL_ROOT}/agents/"*.md ~/.claude/agents/
\```

## Bootstrap

\```
TeamCreate({team_name: "{SKILL_NAME}", description: "..."})

Agent({
  team_name: "{SKILL_NAME}",
  name: "{ROLE_SLUG_A}",
  subagent_type: "{ROLE_SLUG_A}",
  prompt: "<paste from references/{ROLE_SLUG_A}.md §Spawn Prompt, with placeholders filled>"
})

Agent({
  team_name: "{SKILL_NAME}",
  name: "{ROLE_SLUG_B}",
  subagent_type: "{ROLE_SLUG_B}",
  prompt: "<paste from references/{ROLE_SLUG_B}.md §Spawn Prompt>"
})
\```

## Task Seeding

For each role, instantiate its Task Template:

\```
TaskCreate({subject: "...", description: "..."})  // returns id=1
TaskCreate({subject: "...", description: "..."})  // returns id=2
TaskUpdate({taskId: "2", addBlockedBy: ["1"], owner: "{ROLE_SLUG_B}"})
\```

## Steady State

- Teammate idle → check task list; assign next task or send instruction
- `plan_approval_request` from teammate → review against role's Plan Approval criteria; approve or reject with feedback
- Cross-role conflict → lead arbitrates via `SendMessage` (do not let teammates negotiate edits to disputed files)

## Teardown

\```
# 1. Shut each teammate down (wait for ack before next)
SendMessage({to: "{ROLE_SLUG_A}", message: {type: "shutdown_request"}})
SendMessage({to: "{ROLE_SLUG_B}", message: {type: "shutdown_request"}})

# 2. Only after all teammates are gone:
TeamDelete()
\```

## Known Limits

- No `/resume` for in-process teammates — restart spawns new ones
- Lead is fixed for team lifetime; cannot promote a teammate
- Permissions set at spawn time; per-teammate mode changes only after spawn
- Task status can lag — verify state before re-assigning
- One team per lead; clean up before creating another

## Members And References

- Member index: [references/member.md](references/member.md)
- Role specs (read on demand):
  - [references/{ROLE_SLUG_A}.md](references/{ROLE_SLUG_A}.md)
  - [references/{ROLE_SLUG_B}.md](references/{ROLE_SLUG_B}.md)
```

---

## 2. `agents/{ROLE_SLUG}.md` skeleton (subagent definition)

This is the **runtime** file. Body is appended to the spawned teammate's system prompt.

```markdown
---
name: {ROLE_SLUG}
description: {one-line role purpose; used by lead to pick subagent_type}
tools: {TOOLS_ALLOWLIST}
model: {MODEL}
---

You are the {ROLE_NAME} on the {TEAM_TITLE}.

## Your Responsibility

(2–4 lines, lifted from references/{ROLE_SLUG}.md §Scope.)

## Files You Own

You may edit only files matching:
- `path/glob/one/**`
- `path/glob/two/*.ext`

Never edit files outside this list. If you need a change there, message the owning teammate or escalate to the lead.

## Operating Rules

1. (e.g. always run `<test command>` before marking a task completed)
2. (e.g. write outputs to `outputs/{ROLE_SLUG}-<date>.md`)
3. (e.g. if blocked >5 minutes, message the lead with what's blocking)

## Plan Approval

{If true:} Before any code changes, submit a plan and wait for lead approval.
{If false:} Proceed directly to implementation; no plan approval needed.
```

**Notes**:
- `tools` is enforced — omitting a tool means the teammate can't call it. `SendMessage` and task tools are always available regardless.
- `model` overrides the lead's default; omit to inherit.
- The spawn `prompt` (passed via `Agent({prompt})`) is **separate** from this body. The prompt carries the specific task; this body carries the role's standing rules.

---

## 3. `references/{ROLE_SLUG}.md` skeleton (8-section role spec)

```markdown
# {ROLE_NAME} (`{ROLE_SLUG}`)

## 1. Scope

- Deliverable-level capability bullets.

## 2. Inputs

- What this role needs from users / other roles.

## 3. Outputs

- Artifacts produced; acceptance-facing deliverables.

## 4. Boundaries

- Explicit non-goals. What this role does NOT do.

## 5. Spawn Prompt

Lead pastes this verbatim into `Agent({prompt})`. Replace `{{PLACEHOLDERS}}` with task specifics.

\```text
You are the {ROLE_NAME} on the {TEAM_TITLE}.

Task: {{TASK_DESCRIPTION}}

Context:
- {{REPO_PATH_OR_PR}}
- {{CONSTRAINTS}}

Acceptance:
- {{HOW_LEAD_WILL_VERIFY}}

Coordinate via the shared task list. When you finish a task, call TaskUpdate to mark it completed and pick up the next available task. If you hit a blocker, message the lead.
\```

## 6. Owned Paths

This role exclusively writes:

- `path/glob/one/**`
- `path/glob/two/*.ext`

Cross-role overlap is forbidden — see SKILL.md collaboration principles.

## 7. Task Template

Typical tasks (3–6) the lead seeds at bootstrap. `blockedBy` lists peer slugs whose task must complete first.

| Task | Description | blockedBy |
|------|-------------|-----------|
| {ROLE_SLUG}-1 | ... | — |
| {ROLE_SLUG}-2 | ... | {ROLE_SLUG}-1 |
| {ROLE_SLUG}-3 | ... | {OTHER_ROLE_SLUG}-2 |

## 8. Plan Approval

- **Required**: `true` | `false`
- **If true, criteria the lead applies when reviewing**: ...
```

---

## 4. `references/member.md` skeleton

```markdown
# {TEAM_TITLE} — Member Index

This team has **N** Agents and covers the lifecycle: **{phases}**. All members are Claude Code teammates (no human-in-the-loop required by default).

| Role | Slug | Responsibility | Spec | Definition |
|------|------|----------------|------|------------|
| {ROLE_NAME_A} | `{ROLE_SLUG_A}` | ... | [{ROLE_SLUG_A}.md]({ROLE_SLUG_A}.md) | [../agents/{ROLE_SLUG_A}.md](../agents/{ROLE_SLUG_A}.md) |

## Suggested Invocation Order

- **First-time setup**: ...
- **Per-iteration**: ...

## Cross-Role Conflict Rule

If two roles' work conflicts (e.g. ownership boundary disputes, contradictory acceptance criteria), the **lead** arbitrates. Teammates do not negotiate edits to disputed files directly.
```

---

## 5. Hooks (optional)

Wire in project `.claude/settings.json`:

```json
{
  "hooks": {
    "TeammateIdle": [{"command": "{SKILL_ROOT}/hooks/teammate-idle.sh"}],
    "TaskCompleted": [{"command": "{SKILL_ROOT}/hooks/task-completed.sh"}]
  }
}
```

### `hooks/teammate-idle.sh` (block idle until tests pass)

```bash
#!/usr/bin/env bash
# Exit 2 sends feedback to teammate and keeps them working.
set -e
if ! npm test --silent; then
  echo "Tests failing — fix before going idle." >&2
  exit 2
fi
exit 0
```

### `hooks/task-completed.sh` (block completion if artifact missing)

```bash
#!/usr/bin/env bash
# Read the task ID from stdin (provided by hook context).
task_id="$1"
artifact_dir="outputs/"
if ! ls "$artifact_dir" | grep -q "task-${task_id}-"; then
  echo "Task ${task_id} marked complete but no artifact at ${artifact_dir}/task-${task_id}-*" >&2
  exit 2
fi
exit 0
```

Adapt to the team's actual quality bar. Hooks are **per-project** (project `.claude/settings.json`), so each install of the team can tune them.
