---
name: improvement-executor
category: tool
description: "当需要把已批准的改进候选应用到目标文件、回滚之前的变更、或预览变更效果时使用。支持 4 种 action（append/replace/insert_before/update_yaml），每次变更前自动备份。不用于打分（用 improvement-discriminator）或门禁验证（用 improvement-gate）。"
license: MIT
triggers:
  - apply improvement
  - execute candidate
  - rollback change
  - 执行变更
  - 回滚
version: 0.1.0
author: OpenClaw Team
---

# Improvement Executor

Applies accepted candidates with automatic backup and rollback.

## When to Use

- 把已批准的改进候选应用到目标文件
- 回滚之前的变更（通过 receipt）
- 用 `--dry-run` 预览变更

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`
- **门禁验证** → use `improvement-gate`
- **全流程编排** → use `improvement-orchestrator`

## CLI

```bash
# Apply a candidate (requires ranking artifact + candidate ID)
python3 scripts/execute.py \
  --input ranking.json \           # REQUIRED: ranking artifact from discriminator
  --candidate-id cand-01-docs \    # REQUIRED: which candidate to execute
  --state-root /path/to/state \    # default: lib/state_machine.DEFAULT_STATE_ROOT
  --output result.json \           # default: {state-root}/executions/{run-id}-{candidate-id}.json
  --force                          # execute even if recommendation != accept_for_execution

# Rollback a previous change
python3 scripts/rollback.py --receipt receipt.json [--dry-run]
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--input` | (required) | Always: path to ranking artifact JSON from discriminator |
| `--candidate-id` | (required) | Always: the `id` field of the candidate to execute |
| `--force` | false | Use to execute candidates with recommendation=hold (bypasses critic check) |
| `--output` | auto | Set for custom output location |

## 4 Action Types

| Action | Trigger | Behavior |
|--------|---------|----------|
| `append_markdown_section` | `execution_plan.action` | Appends heading + bulleted content lines at EOF. **No-op** if heading already exists |
| `replace_markdown_section` | `execution_plan.action` | Finds section by heading match, replaces all lines until next same-or-higher-level heading |
| `insert_before_section` | `execution_plan.action` | Inserts content lines before a matched heading |
| `update_yaml_frontmatter` | `execution_plan.action` | Merges `frontmatter_updates` dict into YAML frontmatter (requires PyYAML) |

## Backup Mechanism

Every execution creates a backup at `{state-root}/executions/backups/{run-id}/{candidate-id}-{filename}` BEFORE modifying the target. The backup path is stored in `result.rollback_pointer.backup_path` for gate-driven rollback.

## Safety Guards

1. **Recommendation check**: refuses to execute if `recommendation != accept_for_execution` (use `--force` to override)
2. **Category check**: only `EXECUTOR_SUPPORTED_CATEGORIES` (docs, reference, guardrail) are auto-executable; others return `status=unsupported`
3. **File existence**: target file must exist, otherwise SystemExit
4. **Execution trace**: every run captures a structured `execution_trace` dict with action, status, diff_summary for GEPA feedback loop

<example>
正确: 执行一个 docs 类候选
$ python3 scripts/execute.py --input ranking.json --candidate-id cand-01-docs --state-root ./state
→ Backup: ./state/executions/backups/run001/cand-01-docs-README.md
→ Appended "## Operator Notes" section
→ stdout: ./state/executions/run001-cand-01-docs.json
</example>

<anti-example>
错误: 跳过 discriminator 直接执行 medium-risk candidate
$ python3 scripts/execute.py --input ranking.json --candidate-id cand-04-prompt --force
→ category=prompt 不在 EXECUTOR_SUPPORTED_CATEGORIES → status=unsupported
→ medium/high risk 必须经 gate 走 pending_promote → 人工审批
</anti-example>

## Output Artifact

```json
{"stage": "executed", "status": "success", "candidate_id": "cand-01-docs",
 "result": {"status": "success", "modified": true, "diff": "--- a/...",
   "backup_path": "...", "rollback_pointer": {"method": "restore_backup_file",
     "backup_path": "...", "target_path": "..."}},
 "execution_trace": {"type": "execution_trace", "action": "append_markdown_section", ...},
 "next_step": "apply_gate", "next_owner": "gate"}
```

## Related Skills

- **improvement-discriminator**: Scores candidates → executor only runs `accept_for_execution` ones
- **improvement-gate**: Validates execution results → may trigger rollback via `rollback_pointer`
- **improvement-orchestrator**: Calls executor as stage 4, passes ranking artifact + candidate ID
