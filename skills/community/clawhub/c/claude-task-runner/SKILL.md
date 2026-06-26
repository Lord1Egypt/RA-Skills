---
name: claude-task-runner
description: Run Claude Code tasks in headless mode with `claude -p` through the local `cc-task-runner.sh` wrapper, including model switching, JSON output capture, structured schema checks, multi-file artifact validation, and glob matching. Use when you need reliable non-interactive Claude Code execution for coding, review, analysis, report generation, or file-producing tasks. Triggers include headless runner, claude -p automation, scripted Claude Code tasks, JSON-schema validation, artifact verification, and GLM-5.1 / MiniMax-M2.7 task orchestration.
---

# Claude Task Runner

Use the local runner script instead of raw `claude -p` when the task needs any of these:
- model switching via `cc-switch`
- durable task state under `~/.openclaw/state/cc-tasks/`
- notification on completion/failure
- structured-output enforcement via JSON Schema
- multi-file artifact validation (`--expect-file`, `--expect-contains`, `--expect-glob`)

Primary script:
- `/Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh`

## Quick decision

Use this skill when:
- the user asks to run Claude Code non-interactively / in batch / in background
- you need a coding or analysis task to survive beyond a single shell command
- you want the result judged by actual outputs, not just model text
- tmux interaction is unnecessary or risky

Do not use this skill when:
- a direct `read` / `edit` is simpler
- the user explicitly wants a live interactive tmux session
- the task needs persistent interactive back-and-forth inside Claude Code

## Default workflow

1. Pick the model alias.
   - `GLM-5.1` for architecture / long-context reasoning
   - `minimax-m2.7` for deeper problem solving and robust headless runs
2. Decide whether the task needs validation.
3. If validation is needed, prefer both:
   - structured result validation with `--json-schema-file`
   - artifact validation with `--expect-file`, `--expect-contains`, `--expect-glob`
4. Run the task with `cc-task-runner.sh run` or `run-file`.
5. Inspect with `status`, then `log` if anything looks off.
6. Treat missing artifact or `structured_output.status=failure` as a real failure.

## Command patterns

### Minimal run

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "task-name" \
  "GLM-5.1" \
  "/abs/workdir" \
  -- "Your task prompt here"
```

### Write task with permission mode

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "task-name" \
  "GLM-5.1" \
  "/abs/workdir" \
  --permission-mode bypassPermissions \
  -- "Create /abs/workdir/output.txt with content: hello world"
```

### Multi-file validation

All `--expect-file`, `--expect-contains`, `--expect-glob` support **repeat** usage.
`--expect-contains` binds to the **most recent** `--expect-file` before it.

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "multi-check" \
  "GLM-5.1" \
  "/abs/workdir" \
  --permission-mode bypassPermissions \
  --expect-file "/abs/workdir/a.txt" \
  --expect-contains "alpha" \
  --expect-file "/abs/workdir/b.txt" \
  --expect-glob "out/*.log" \
  -- "Create a.txt with 'alpha ok', b.txt with 'bravo ok', and out/run.log"
```

Meaning:
- `a.txt` must exist AND contain "alpha"
- `b.txt` must exist (no content check)
- `out/*.log` glob must match at least one file

### Full combo: schema + multi-file + glob

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "full-check" \
  "GLM-5.1" \
  "/abs/workdir" \
  --permission-mode bypassPermissions \
  --json-schema-file "/abs/schema.json" \
  --expect-file "/abs/workdir/output.txt" \
  --expect-contains "expected text" \
  --expect-glob "logs/*.log" \
  -- "Your task prompt"
```

### Prompt from file

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run-file \
  "task-name" \
  "minimax-m2.7" \
  "/abs/workdir" \
  "/abs/prompt.txt" \
  --json-schema-file "/abs/schema.json"
```

### Inspect state

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh status "task-name"
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh log "task-name"
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh list
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh kill "task-name"
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh clean
```

## Validation parameters

| Parameter | Repeatable | Binds to | Description |
|-----------|-----------|----------|-------------|
| `--expect-file <path>` | ✅ yes | self | File must exist after task |
| `--expect-contains <text>` | ✅ yes | previous `--expect-file` | That file must contain text |
| `--expect-glob <pattern>` | ✅ yes | self | Glob must match ≥1 file |
| `--json-schema-file <file>` | ❌ no | self | Enforces structured output |
| `--permission-mode <mode>` | ❌ no | self | `bypassPermissions` or `acceptEdits` |
| `--fallback-model <alias>` | ❌ no | self | Retry with this model on failure |
| `--max-retries <n>` | ❌ no | self | Max retry attempts (default: 1) |

### Binding order example

```bash
--expect-file a.txt \
--expect-contains "hello" \
--expect-contains "world" \   # both "hello" AND "world" checked in a.txt
--expect-file b.txt \          # b.txt just needs to exist
--expect-glob "out/*.csv"      # independent glob check
```

## Validation rules

For tasks that must produce files, always provide at least one artifact check.

Preferred combinations:
- file creation only → `--expect-file`
- exact or critical content → `--expect-file` + `--expect-contains`
- one-or-more generated files → `--expect-glob`
- non-file report / analysis → `--json-schema-file`
- implementation task → schema + artifact checks together

**Permission mode**: Prefer `--permission-mode bypassPermissions` in trusted local environments when the task must write files or run Bash. Without it, Claude may ask for manual approval and the task will hang.

Do not trust plain language like "已完成" or "done" without validation.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Task completed, all validations passed |
| 1 | Model/runtime error |
| 2 | Artifact validation failed |
| 3 | Structured output reported failure |

## JSON schema guidance

Keep schemas small. Use them to force a machine-checkable result contract.

Good default schema for most tasks:
- `status`: `success|failure`
- `summary`: short text
- `files_changed`: optional array
- `error_category`: optional
- `suggestion`: optional

## Model notes

Current local environment supports `GLM-5.1` headless via:
- base URL: `https://open.bigmodel.cn/api/anthropic`
- model id: `glm-5.1`

The local `cc-switch` wrapper already special-cases this. Use the alias `GLM-5.1`, not a raw model id, when calling the runner.

## Failure handling

If a task fails:
1. run `status`
2. run `log`
3. identify which layer failed:
   - model/runtime error (exit 1)
   - artifact validation failure (exit 2)
   - structured schema failure (exit 3)
4. either rerun with a stricter prompt or fix the prompt/schema/expectations

If the model says success but artifact validation fails, trust the validator, not the prose.

## Files to read when needed

Read these only when you need deeper details:
- `references/runner-usage.md` for usage notes and patterns
- `references/task-schema-example.json` for a reusable schema template
- `scripts/run-task-example.sh` for a concrete invocation pattern
