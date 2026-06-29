# Runner Adapters

Runner adapters explain how different AI coding agents can run the same loop. They must not replace the shared `Docs/` state protocol.

## Universal Adapter Contract

Every runner must:

- Start by reading the minimum `Docs/` set.
- Execute one bounded loop.
- Respect hard and budget stop rules.
- Write `EVALUATION.md`, `STATUS.md`, `ACCEPTANCE.md`, `PENDING.md`, `NEXT_ACTIONS.md`, and `LOOP_RUNS.jsonl` before exiting.
- Avoid storing product-specific state as the only copy of project memory.

Minimum external loop contract:

```text
input: workspace path + prompt that says "run one Agent Loop Engineering loop"
must read: Docs/LOOP_CONFIG.md, TARGET.md, ACCEPTANCE.md, STATUS.md, PENDING.md, NEXT_ACTIONS.md
must write: EVALUATION.md, STATUS.md, ACCEPTANCE.md, PENDING.md, NEXT_ACTIONS.md, LOOP_RUNS.jsonl
must write when applicable: COMPLETED.md for completed acceptance items or user-visible deliverables; HANDOFF.md for standalone handoff triggers
continue behavior: exit after one loop; the scheduler may start the next loop only if state is Continue
budget exhausted: write Blocked, name the exhausted budget, and exit
```

Suggested adapter exit convention:

| State | Exit code | Meaning |
| --- | ---: | --- |
| Continue | 0 | One loop finished and another loop may be scheduled. |
| Done | 0 | Target completed; scheduler must not continue. |
| Done with Risk | 1 | Core target appears complete but user review is needed; scheduler must stop automatic loops. |
| Blocked | 2 | Human input, permission, or decision is required. |

If a runner cannot set exit codes, it must still write the state to `Docs/EVALUATION.md` and `Docs/LOOP_RUNS.jsonl`.

Do not run multiple writers concurrently against the same `Docs/` state. Use sequential scheduling or file locking. If concurrent runners are detected and no lock exists, stop as `Blocked` and ask the user to choose a single active runner.

## Codex

Use heartbeat or automation when available. Each wakeup should instruct Codex to:

```text
Use $agent-loop-engineering in this workspace. Read Docs/LOOP_CONFIG.md and Docs/NEXT_ACTIONS.md, run one bounded loop, then write evaluation and stop/continue status.
```

Blocked example: if a command needs GitHub login, write `Blocked` with needed login scope, update `PENDING.md`, and stop.

## Claude Code

Use scheduled prompts or loop workflows. Keep Claude-specific commands outside project state. The prompt should ask Claude to read `Docs/` first, run one loop, and stop on hard gates.

```text
Use the local Agent Loop Engineering protocol. Read only the minimum Docs/ files, run one bounded loop, update EVALUATION/PENDING/NEXT_ACTIONS/LOOP_RUNS, and stop on hard or budget gates.
```

## OpenCode

Use an external scheduler or command loop. The wrapper should call OpenCode with a prompt pointing to `Docs/NEXT_ACTIONS.md` and a maximum loop budget.

```text
Continue the project from Docs/NEXT_ACTIONS.md. Do one bounded implementation and verification loop. Do not continue after a hard stop; write Blocked state to Docs/.
```

Outer loop sketch:

```text
while last_state == Continue and loop_count < max_loops:
  run opencode with the one-loop prompt
  read latest state from Docs/EVALUATION.md
  stop unless state is Continue
```

## Cline

Use the VS Code workspace as the execution surface. Cline should treat `Docs/NEXT_ACTIONS.md` as the current task and `Docs/EVALUATION.md` as the stop report.

```text
Read Docs/TARGET.md, Docs/ACCEPTANCE.md, and Docs/NEXT_ACTIONS.md. Execute the next action in this workspace, then update the loop state files before ending.
```

## Qoder

Use project documents as persistent context. Ask Qoder to read only the minimum `Docs/` set and to update loop state before ending the task.

```text
Use project Docs/ as persistent state. Do not rely on prior chat memory. Run one loop, verify, and classify the result as Continue, Done, Done with Risk, or Blocked.
```

## CodeBuddy

Use task decomposition plus project state files. CodeBuddy should not continue from chat memory alone; it should resume from `Docs/STATUS.md` and `Docs/NEXT_ACTIONS.md`.

```text
Resume from Docs/STATUS.md and Docs/NEXT_ACTIONS.md. Keep the work inside Docs/TARGET.md and update EVALUATION.md with evidence before stopping.
```

## Trae

Use workspace tasks and check commands. Trae should run one bounded implementation/verification loop and write the same shared state files.

```text
Read the Agent Loop Engineering Docs/ files, execute the immediate next action, run discovered verification commands, and stop if any hard gate is triggered.
```

## Gemini CLI and Aider

Use an outer script, manual command, or scheduler. Limit each run by time and failure count. Keep all durable state in `Docs/`, not in CLI history.

```text
Run one bounded coding loop from Docs/NEXT_ACTIONS.md. Use Docs/LOOP_CONFIG.md budgets. Write all durable state back to Docs/ before exiting.
```

Do not let CLI history become the only memory source. If the wrapper sees exit code 2 or latest state `Blocked`, stop scheduling.

## GitHub Actions

Use for CI checks, scheduled diagnostics, issue creation, and repair PRs. Do not use GitHub Actions to access secrets, production resources, or perform destructive changes unless explicitly approved.

Suggested use:

```text
schedule -> run checks -> summarize failure -> open issue or PR -> stop for review
```

Minimal workflow shape:

```yaml
name: agent-loop-check
on:
  workflow_dispatch:
  schedule:
    - cron: "0 */6 * * *"
jobs:
  check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - name: Run project checks
        run: |
          echo "Run verification commands from Docs/LOOP_CONFIG.md here"
      - name: Summarize
        if: always()
        run: |
          echo "Write or upload sanitized check summary; do not access production secrets"
```

Actions should normally report, open an issue, or prepare a reviewed PR. They should not self-merge, force-push, rewrite history, or run migrations.

## Adapter Selection

Choose the runner in this order:

1. Runner explicitly configured in `Docs/LOOP_CONFIG.md`.
2. Runner explicitly requested by the user.
3. Runner already active in the current workspace/session.
4. Lowest-privilege runner that can read the needed files, make project-local edits, and run verification.

If no runner can safely continue, write `Blocked` and tell the user what setup is needed.
