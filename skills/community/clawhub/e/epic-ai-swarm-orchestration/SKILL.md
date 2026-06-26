---
name: epic-ai-swarm-orchestration
description: Production playbook and portable runtime for parallel AI coding swarms using Codex, Gemini, DeepSeek, and optional Claude. Use when orchestrating multi-agent coding work, packaging/installing the swarm on another OpenClaw host, spawning parallel builders with review/integration loops, managing duty-table model rotation, or diagnosing swarm runtime health. Triggers on phrases like "run the swarm", "spawn agents", "AI swarm", "multi-agent build", "package the swarm", "install swarm", "duty table", "model rotation", "parallel coding agents".
---

# Epic AI Swarm Orchestration v3.3.0

Portable OpenClaw skill + runtime for running parallel AI coding agents with tmux worktrees, duty-table model selection, token-limit fallback, review loops, integration watcher, and heartbeat notifications.

## Use this skill when

- The human/operator asks to “swarm” coding/build/review/integration work.
- Another OpenClaw needs the same swarm system installed.
- You need to inspect/fix `~/workspace/swarm`, duty tables, model fallback, pulse checks, or pending notifications.

## Hard rule for swarm work

Do **not** bypass the runtime scripts. For real swarm work use:

- Single task: `~/workspace/swarm/spawn-agent.sh`
- Parallel tasks: `~/workspace/swarm/spawn-batch.sh`
- Status/pulse: `~/workspace/swarm/check-agents.sh`, `~/workspace/swarm/pulse-check.sh`

Do not use bare background `claude`, `codex`, `gemini`, `deepseek`, or OpenClaw subagents as a substitute for the swarm pipeline unless explicitly debugging the runtime itself.

## Plug-and-play install on another OpenClaw host

From the installed skill directory:

```bash
bash install.sh
bash doctor.sh
```

Default install target: `~/workspace/swarm`.

What `install.sh` does:

1. Copies bundled runtime scripts into `~/workspace/swarm/`.
2. Creates clean local state/config files from `templates/` without bundling secrets.
3. Installs `roles/swarm-lead/{ROLE.md,TOOLS.md,HEARTBEAT.md}` into the OpenClaw workspace.
4. Adds `swarm-lead` to `roles/active.json` unless `--no-activate` is used.
5. Backs up existing role/config files before replacing them.

Useful installer options:

```bash
bash install.sh --dry-run
bash install.sh --target /custom/swarm/path --workspace /custom/openclaw/workspace
bash install.sh --force          # replace config/state templates after backup
bash install.sh --no-role        # scripts only
bash install.sh --no-activate    # copy role but do not activate it
```

Then authenticate provider CLIs on that host and run:

```bash
~/workspace/swarm/assess-models.sh --dry-run
~/workspace/swarm/assess-models.sh
```

`doctor.sh --probe-models` runs live provider probes; skip it unless the operator is okay spending provider quota.

## Prerequisites

Required CLIs on PATH:

- `bash`, `python3`
- `git` — worktrees, branches, commits
- `tmux` — isolated agent sessions

Recommended integrations:

- `gh` — GitHub status/CI/release checks
- `openclaw` — local notification delivery where configured

Model CLIs: install/authenticate at least one of:

- `codex`
- `gemini`
- `deepseek`
- `claude` optional legacy fallback in some watcher paths

Credentials are host-local. This package intentionally does **not** bundle API keys, OAuth tokens, Telegram targets, duty-table state, logs, endorsements, or task history.

## Runtime layout

```text
~/workspace/swarm/
  spawn-agent.sh
  spawn-batch.sh
  notify-on-complete.sh
  integration-watcher.sh
  queue-watcher.sh
  pulse-check.sh
  check-agents.sh
  assess-models.sh
  fallback-swap.sh
  model-fallback.sh
  try-model.sh
  duty-table.json
  swarm.conf
  active-tasks.json
  pending-notifications.txt
  logs/
  endorsements/
```

Bundled resources:

- `scripts/` — runtime scripts copied by `install.sh`
- `templates/` — clean config/state defaults
- `roles/swarm-lead/` — OpenClaw role files
- `references/workflow.md` — 3-phase workflow
- `references/tools.md` — command syntax
- `references/duty-table.md` — model rotation/fallback details
- `references/eor-template.md` — end-of-run report template

## Workflow

### Phase 1 — Plan

1. Inspect project state, git, CI, ESR/history, and relevant notes.
2. Split work into independent task IDs/prompts.
3. Present the task plan to the human/operator.
4. Wait for endorsement before spawning.

### Phase 2 — Build + Review

Use role-based tasks so the duty table chooses the actual model:

```bash
~/workspace/swarm/spawn-batch.sh /path/to/project batch-id "Batch description" /tmp/tasks.json
```

Example `tasks.json`:

```json
[
  {"id":"fix-auth", "description":"Fix login redirect", "role":"builder", "reasoning":"high"},
  {"id":"ui-polish", "description":"Polish mobile layout", "role":"builder"}
]
```

Each task runs in its own tmux session/worktree. `notify-on-complete.sh` launches reviewer/fixer loops and records handoff logs.

### Phase 3 — Integrate + Ship

`spawn-batch.sh` starts `integration-watcher.sh`, which waits for all sessions, merges branches, runs verification, persists work logs/ESR, and writes notifications.

## Heartbeat handling

On heartbeat, the swarm-lead role should:

1. Read `~/workspace/swarm/pending-notifications.txt`.
2. Send each pending line to the human/operator, then clear the file.
3. Run `~/workspace/swarm/pulse-check.sh`.
4. Check `tmux ls` for active/completed agent sessions.
5. Only reply `HEARTBEAT_OK` if nothing is actionable.

## Safety and quality gates

- Human endorsement before spawn.
- 30-second cooldown for single-task endorsement.
- `SWARM_MAX_CONCURRENT` queueing for large batches.
- Max 3 reviewer/fixer loops.
- Token/rate-limit fallback via `model-fallback.sh`.
- Stuck-agent detection via `pulse-check.sh`.
- Final merge/build verification by integration watcher.

## References

Read only what you need:

- Workflow details: [references/workflow.md](references/workflow.md)
- Spawn command syntax: [references/tools.md](references/tools.md)
- Duty table/fallback: [references/duty-table.md](references/duty-table.md)
- EOR report format: [references/eor-template.md](references/eor-template.md)
