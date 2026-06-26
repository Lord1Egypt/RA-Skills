---
name: forge
description: "Forge 🔨 — Repair-Inspect loop orchestrator. Automated code repair with independent inspection, dependency-aware parallel execution, protected file guardrails, and crash-recoverable state. Use when: fixing multiple code issues (bug fixes, review board recommendations, audit findings), need verified repairs with independent QA, want safe automated code changes with rollback protection. NOT for: simple one-line fixes, architecture decisions, prompt modifications."
---

# Forge 🔨 — 维修-监理自动循环

Automated repair-inspect loop with state persistence, dependency analysis, and safety guardrails.

## When to Use

- Multiple repair tasks from review board / audit / user instructions
- Need independent verification (not just "looks fixed")
- Want protected file safety + auto-commit on PASS

## Quick Start

```bash
cd /path/to/project

# 1. Initialize
python3 ~/clawd/skills/forge/scripts/forge.py init

# 2. Add tasks
python3 forge.py add "修复空值处理" --criteria "空输入不崩溃" --priority P0
python3 forge.py add "清理废弃代码" --criteria "无import报错" --depends task-001

# 3. See execution plan
python3 forge.py plan

# 4. Run (outputs spawn instructions)
python3 forge.py run

# 5. Execute spawns, then run again to check results
python3 forge.py run   # checks results, auto-loops on FAIL

# 6. When all done
python3 forge.py summary
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `init --workdir DIR` | Initialize forge session |
| `add "desc" --criteria "..." --depends task-001 --priority P0` | Add repair task |
| `plan` | Show dependency graph + parallel execution waves |
| `run` | Advance state machine (spawn or check results) |
| `status` | Show current progress |
| `check` | Pre-commit safety check (protected files, deletions) |
| `summary` | Generate completion report |
| `reset` | Clear state |

## How It Works

### State Machine (per task)

```
pending → repairing → inspecting → done
                ↑          │
                └── fail ──┘   (auto-loop, max 5 rounds)

inspecting → needs_human  (pause, escalate)
inspecting → escalated    (>5 rounds)
repairing  → needs_human  (all BLOCKED)
```

### Dependency-Aware Parallel Execution

Tasks without dependencies run in parallel. `forge.py plan` shows execution waves:

```
Wave 1: task-001, task-002, task-003  (并行)
Wave 2: task-004 ← task-001          (等task-001完成)
```

### Safety Guardrails (3 layers)

1. **Protected files** — `protected-files.txt` in project root. Listed files cannot be modified by repair agents. Touching them → BLOCKED → NEEDS_HUMAN.
2. **Pre-commit diff check** — `forge.py check` detects: file deletions, protected file modifications, abnormally large changes.
3. **Prompt constraints** — Repair engineer prompt explicitly forbids deletions, protected files, cron changes.

### Experience Accumulation

Each repair produces a `repair_pattern` with error classification and reusable solution templates. These are stored in `forge-reflections.jsonl` and the most recent 5 patterns are injected into future repair tasks as context.

## Integration with AI Agents

When the agent receives repair tasks (from code review, audit, or user):

```python
# 1. Init forge in project dir
exec("cd /path/to/project && python3 ~/clawd/skills/forge/scripts/forge.py init")

# 2. Add tasks
exec("python3 forge.py add 'Fix null handling in processor' --criteria 'No crash on empty input' --priority P0")

# 3. Run to get spawn instructions
exec("python3 forge.py run")
# → Script outputs spawn instructions

# 4. Execute spawns
sessions_spawn(task=read(task_file), label=label, model=model)

# 5. After spawn completes, run again
exec("python3 forge.py run")
# → Checks repair result → prepares inspector spawn
# → Or auto-loops on FAIL → prepares next repair spawn

# 6. On all PASS → git commit + notify
```

## File Layout

```
forge/
├── SKILL.md                           # This file
├── scripts/
│   └── forge.py                       # Core orchestrator
├── references/
│   └── protocol.md                    # Full protocol documentation
└── assets/
    └── templates/
        ├── repair-engineer.md         # Repair agent role reference
        └── inspector.md              # Inspector role reference
```

### Project-side files (created by forge)

```
project/
├── forge-state.json                   # State persistence (crash recovery)
├── forge-reflections.jsonl            # Project-specific experience (stays with project)
├── forge-output/                      # Task files and results
│   ├── task-001-repair-r1.task.md     # Repair spawn task
│   ├── task-001-repair-r1.json        # Repair result
│   ├── task-001-inspect-r1.task.md    # Inspect spawn task
│   └── task-001-inspect-r1.json       # Inspect result
└── protected-files.txt                # (optional) Protected file list
```

### Experience: Two-Layer Architecture
```
forge/reflections/patterns.jsonl       # Universal patterns (cross-project, stays with skill)
project/forge-reflections.jsonl        # Project-specific patterns (stays with project)
```

- **Universal layer** (`forge/reflections/patterns.jsonl`): Abstract lessons stripped of file paths and project context. Auto-extracted from project patterns after each repair. Deduped by pattern_name. Injected into ALL future repairs across any project.
- **Project layer** (`{project}/forge-reflections.jsonl`): Full detail with file names, paths, project-specific context. Only injected when working on that project.
- **Auto-extraction**: After each repair, `extract_universal_pattern()` checks if the pattern is generalizable (not too many project-specific paths). If so, it's added to the universal layer with dedup.

## Doc-Sync Check (文档同步检查)

Forge收尾时自动检查：修改的代码文件是否有关联文档需要同步更新。

### 工作原理
1. **优先运行 `scripts/tools/doc-sync-checker.py --json`**（如果存在）
2. **回退到 `references/doc-sync-manifest.yaml`**：交叉对比forge修改的文件与manifest中的authority→consumer映射

### 项目配置
在项目中创建 `references/doc-sync-manifest.yaml`：
```yaml
facts:
  api_config:
    authority: src/config.py
    consumers:
      - docs/api-reference.md
      - docs/deployment-guide.md
    last_synced: 2026-03-01
```

Forge完成报告会显示：
```
📄 文档同步检查 — 2 个文档可能需要更新:
  ⚠️ docs/api-reference.md 可能需要同步更新（api_config 的权威源 src/config.py 已修改）
```

## Configuration

Via `init` flags or `forge-state.json` config section:

| Key | Default | Description |
|-----|---------|-------------|
| `model` | `anthropic/claude-opus-4-6` | LLM model for agents |
| `max_rounds` | `5` | Max repair-inspect cycles before escalation |
| `repair_timeout` | `600` | Repair agent timeout (seconds) |
| `inspect_timeout` | `300` | Inspector timeout (seconds) |
| `auto_commit` | `true` | Auto git-commit on PASS |
