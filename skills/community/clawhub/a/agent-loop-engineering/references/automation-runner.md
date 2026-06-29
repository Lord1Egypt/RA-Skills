# Automation Runner

This reference defines how to add automation around Agent Loop Engineering without making any specific AI product the source of truth. Automation may start the next loop, but project-local `Docs/` files remain the durable state.

## 中文快速说明

自动化 Runner 的职责不是替 Agent 做判断，而是重复触发一个有边界的编码循环，并在每轮后检查是否应该继续、完成或停止。

默认建议：

- 先使用本地半自动 Runner，不要一开始做无人值守自动开发。
- 每次只触发一个 bounded loop。
- 每轮结束必须读取 `Docs/EVALUATION.md` 或 `Docs/LOOP_RUNS.jsonl` 的最新状态。
- 只有最新状态是 `Continue` 且预算未超限时，才允许启动下一轮。
- 遇到 `Done`、`Done with Risk`、`Blocked`、硬门禁、连续失败或超时，必须停止。
- 不允许自动处理账号登录、密钥、生产数据、系统安装、不可逆操作、技术栈替换或目标冲突。

## Automation Levels

| Level | Mode | Use Case | Stop Responsibility |
| --- | --- | --- | --- |
| L1 | Manual next loop | Early validation, unclear goals, high-risk work | Human |
| L2 | Local runner loop | Personal development, bug fixes, bounded feature work | Runner plus agent state |
| L3 | CI or scheduler | Checks, reports, issue creation, reviewed repair PRs | CI policy plus human review |

Start with L1 or L2. Use L3 for verification and reporting first; only allow code-writing CI after the repository has clear branch, review, and permission rules.

## Runner Responsibilities

A runner may:

- Read `Docs/LOOP_CONFIG.md` for budgets and allowed project-local actions.
- Read `Docs/NEXT_ACTIONS.md` to create the one-loop agent prompt.
- Invoke a configured AI coding agent.
- Run configured verification commands when the runner owns verification.
- Capture sanitized command summaries and log paths.
- Read the latest loop result.
- Decide whether to schedule another loop.

A runner must not:

- Store the only copy of memory outside `Docs/`.
- Continue after `Done`, `Done with Risk`, or `Blocked`.
- Loosen hard stop rules.
- Retry indefinitely.
- Run multiple writers against the same `Docs/` state without a lock.
- Hide failed verification, missing evidence, or human-decision requirements.

## Minimum Local Runner Flow

```text
load Docs/LOOP_CONFIG.md or defaults
ensure Docs/TARGET.md and Docs/ACCEPTANCE.md exist
for loop_index from 1 to max_loops:
  stop if runtime budget is exhausted
  acquire project loop lock if locking is supported
  invoke selected agent with the one-loop prompt
  release lock
  read latest state from Docs/EVALUATION.md or Docs/LOOP_RUNS.jsonl
  stop if state is Done, Done with Risk, or Blocked
  stop if state is not Continue
  stop if consecutive failure budget is exhausted
stop as Blocked if max_loops or runtime budget is reached without Done
```

If the agent did not update the required loop files, treat the run as failed and stop or retry according to `max_consecutive_failures`.

## One-Loop Prompt Template

Use this as the stable prompt passed by the runner to any coding agent:

```text
Use $agent-loop-engineering.

Workspace: <absolute workspace path>

Run exactly one bounded AI coding loop.

Read the minimum required project state:
- Docs/LOOP_CONFIG.md
- Docs/TARGET.md
- Docs/ACCEPTANCE.md
- Docs/STATUS.md
- Docs/PENDING.md
- Docs/NEXT_ACTIONS.md

Do not rely on chat history.
Do not load full loop history unless needed; read only the latest 3-5 LOOP_RUNS records.
Do not continue if STOP_RULES.md or the built-in hard stops require human input.

At the end, update:
- Docs/EVALUATION.md
- Docs/STATUS.md
- Docs/ACCEPTANCE.md current evidence for touched criteria
- Docs/PENDING.md
- Docs/NEXT_ACTIONS.md
- Docs/LOOP_RUNS.jsonl
- Docs/COMPLETED.md when a user-visible or verification-backed item is complete

Report exactly one loop state:
- Continue
- Done
- Done with Risk
- Blocked
```

## Stop-State Parsing

Prefer machine-readable state from the latest `Docs/LOOP_RUNS.jsonl` record:

```json
{"loop_id":"2026-06-09T13:00:00Z-001","state":"Continue","verification":{"test":"pass","typecheck":"pass"},"next_action":"Run functional smoke check"}
```

If `LOOP_RUNS.jsonl` is missing or invalid, parse the latest decision section in `Docs/EVALUATION.md`. If neither source has a clear state, stop as `Blocked` and ask a human to repair the loop state.

Valid states:

| State | Runner Action |
| --- | --- |
| Continue | Start another loop only if budgets allow. |
| Done | Stop and report completion. |
| Done with Risk | Stop and report the named risks. |
| Blocked | Stop and ask for the named human input or permission. |

Unknown or missing state must be treated as `Blocked`.

## Failure Budget

Use `Docs/LOOP_CONFIG.md`:

```yaml
max_loops: 5
max_consecutive_failures: 2
max_runtime_minutes: 60
require_double_evidence_for_done: true
runner:
  type: local
  agent_command: null
  verification_owned_by_runner: false
  lock_file: Docs/.agent-loop.lock
```

Count a loop as failed when:

- The agent exits with a nonzero status and does not write a valid `Blocked` or `Done with Risk` decision.
- Required loop files were not updated.
- Core verification failed and no configured progress signal is present.
- The same root cause repeats without narrower evidence.

Do not count a loop as failed when the agent correctly stops as `Blocked` because human input is required. That is a safe stop, not an automation failure.

## Locking

Use sequential scheduling by default. If a runner may overlap with another runner, create a lock before invoking the agent.

Lock rules:

- Lock file path should default to `Docs/.agent-loop.lock`.
- The lock should include runner name, process ID if available, start time, and timeout.
- If a valid lock exists, do not start another writer.
- If the lock is stale beyond `max_runtime_minutes`, stop as `Blocked` unless a human approves cleanup.

## CI and GitHub Actions

CI should normally verify and report. It should not be the first automation layer for autonomous coding.

Recommended CI tasks:

- Run tests, type checks, lint, and builds.
- Upload sanitized logs.
- Open an issue with verification failure summaries.
- Create a repair PR only when branch and review rules are explicit.

CI must not:

- Self-merge.
- Force-push.
- Rewrite history.
- Run migrations against production.
- Use secrets for coding loops unless the user explicitly approved that exact run and scope.

## Human Stop Conditions

Automation must stop and ask for direction when any loop requires:

- Account login, OAuth, cookies, session reuse, or secrets.
- Production database access or real user data.
- Paid cloud resource creation or modification.
- System-level installation, administrator rights, drivers, or host configuration.
- Destructive delete, overwrite, force-push, reset, migration, or irreversible action.
- Technology-stack replacement or major framework upgrade.
- A direction that conflicts with `Docs/TARGET.md`.
- Context that cannot be safely compressed within budget.

## Handoff After Automation Stops

When the runner stops, the agent should leave a human-readable summary in the normal loop files. If a separate handoff is needed, write `Docs/HANDOFF.md` with:

- Final state.
- Reason for stopping.
- Latest verification evidence.
- Files changed.
- Remaining blockers.
- One recommended next action.

The chat or runner report may be brief, but the project files must be sufficient for another agent to resume.
