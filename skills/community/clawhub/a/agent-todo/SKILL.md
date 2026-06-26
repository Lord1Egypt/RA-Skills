---
name: agent-todo
description: Local-first execution queue for OpenClaw agents. Use when an agent should turn promises into executable tasks, pick work during heartbeat, maintain its own queue inside its own workspace, or dispatch work to another registered agent workspace. Triggers: task queue, heartbeat execution, follow-up work, background tasks, multi-agent task routing.
---

# agent-todo Skill

Use this skill as an execution queue, not as a passive reminder list.

核心原则：每个 agent 只维护并消费自己 workspace 下的任务队列；需要跨 agent 分发时，再按 OpenClaw 已注册的 workspace 进行发现和投递。

## Core commands

```bash
bash ./script.sh add "Publish release" \
  --task-type publish \
  --source "forum:#19/reply:88" \
  --next-action "Push main to GitHub and publish ClawHub version" \
  --success-criteria "GitHub and ClawHub are both updated"

bash ./script.sh dispatch "Review release" \
  --to-agent reviewer \
  --task-type review \
  --source "chat:direct" \
  --next-action "Review release artifacts" \
  --success-criteria "Feedback delivered"

bash ./script.sh run-pending --claim
bash ./script.sh done <id> --note "what was completed"
bash ./script.sh report <id>
bash ./script.sh block <id> --reason "why blocked"
bash ./script.sh setup-heartbeat --write
bash ./script.sh setup-heartbeat --all --write
```

## Workflow

1. Add tasks with enough execution context:
   - `task_type`
   - `next_action`
   - `success_criteria`
   - `source`
2. For composite goals, prefer `plan` to split them into concrete steps.
3. During heartbeat, run:
   - `bash ./script.sh run-pending --claim`
4. If it returns `EXECUTE_NOW`, do the task immediately.
5. Prefer continuing a `running` task before opening a fresh `pending` one.
6. To assign work to another agent, use `dispatch --to-agent <agent_id>`.
7. After execution:
   - success → `done`
   - generate reply text → `report`
   - cannot continue → `block`
   - no longer needed → `cancel`

## Storage model

- Current workspace queue: `.agent-todo/tasks.json`
- Optional local identity: `.agent-todo/local.json`
- Workspace discovery source: `~/.openclaw/openclaw.json`
- Heartbeat wiring: managed block in `HEARTBEAT.md`

Do not hand-write workspace paths in normal usage. Let the script resolve the current workspace and discover registered workspaces from OpenClaw.

## Notes

- Single-workspace mode works out of the box after install.
- Multi-agent routing is opt-in: it only matters when you call `dispatch`.
- `setup-heartbeat --all --write` appends or updates a managed block for every discovered workspace instead of overwriting the full file.
- `report` generates different output shapes for forum sources and direct chat sources.
