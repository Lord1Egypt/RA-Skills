# Runner Usage Reference

## Current commands

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh list
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh status <task>
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh log <task>
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh result <task>
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh kill <task>
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh clean
```

## Validation parameters (all repeatable)

```bash
--expect-file <path>          # File must exist (repeatable)
--expect-contains <text>      # Binds to previous --expect-file (repeatable)
--expect-glob <pattern>       # Glob must match ≥1 file (repeatable)
```

## Recommended patterns

### Write task (single file)

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "my-task" "GLM-5.1" "/workdir" \
  --permission-mode bypassPermissions \
  --expect-file "/workdir/output.txt" \
  --expect-contains "expected content" \
  -- "Create output.txt with expected content"
```

### Multi-file validation

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "multi" "GLM-5.1" "/workdir" \
  --permission-mode bypassPermissions \
  --expect-file "/workdir/a.txt" \
  --expect-contains "alpha" \
  --expect-file "/workdir/b.txt" \
  --expect-glob "out/*.log" \
  -- "Create a.txt, b.txt, and out/*.log"
```

### Analysis task (no files, schema only)

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "analyze" "GLM-5.1" "/workdir" \
  --json-schema-file "/workdir/schema.json" \
  -- "Analyze the codebase and report findings"
```

### With retry/fallback

```bash
bash /Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh run \
  "safe-task" "GLM-5.1" "/workdir" \
  --permission-mode bypassPermissions \
  --fallback-model "minimax-m2.7" \
  --max-retries 1 \
  --expect-file "/workdir/output.txt" \
  -- "Create output.txt"
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | Model/runtime error |
| 2 | Artifact validation failed |
| 3 | Structured output reported failure |

## Known limitations

- Headless tasks without `--permission-mode bypassPermissions` may stall waiting for user approval on Bash/write commands
- `--expect-contains` must appear **after** its corresponding `--expect-file`; if no file precedes it, validation will fail
- Glob patterns are resolved relative to `workdir` unless absolute
- Sub-process cleanup relies on pid file; if the host restarts, stale pids show as "running" until `kill` or `clean`

## Binding semantics

```
--expect-file a.txt           → a.txt must exist
--expect-contains "hello"     → a.txt must contain "hello"
--expect-contains "world"     → a.txt must also contain "world"
--expect-file b.txt           → b.txt must exist (no content check)
--expect-glob "out/*.csv"     → glob must match ≥1 file
```

Each `--expect-contains` binds to the **most recent** `--expect-file` above it. Multiple contains for the same file are AND-ed.

## Task state location

All task metadata lives under `~/.openclaw/state/cc-tasks/<task-name>/`:
- `state.json` — status, exit_code, timestamps, validation errors
- `result.json` — raw Claude output (JSON)
- `prompt.txt` — the prompt that was sent
- `meta.json` — model, workdir, schema path, validation count
- `stderr.log` — stderr from claude process
- `pid` — background pid (deleted on completion)
