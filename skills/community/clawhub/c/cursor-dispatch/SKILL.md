---
name: cursor-dispatch
description: "Orchestrate Cursor Agent CLI for coding tasks with concurrency control, timeout recovery, and multi-task coordination. Use when: (1) dispatching coding tasks to cursor agent via CLI, (2) analyzing code before modifying (plan mode), (3) running parallel batch coding tasks with concurrency limits, (4) coordinating multi-step code changes with review gates, (5) recovering from stuck/timeout cursor processes. Triggers: cursor dispatch, plan then execute, code analysis pipeline, batch coding tasks, cursor agent orchestration, parallel coding, concurrent tasks."
---

# Cursor Agent CLI Dispatch

Orchestrate `cursor agent` CLI with concurrency control, timeout recovery, and retry.

## Hard Constraints (from testing)

| Constraint | Value | Source |
|-----------|-------|--------|
| PTY required | `pty: true` mandatory | No output without PTY |
| Max safe concurrency | 6 parallel tasks | Tested 8 OK, 6 is safe margin |
| Plan timeout (single file) | 60-120s | Tested on .gd files |
| Plan timeout (multi-file) | >180s, WILL timeout | Don't attempt |
| Execute timeout | 60-90s typical | Up to 180s for complex |
| `--output-format json` | BROKEN in PTY | Use text format only |
| Empty output = failure | Check output size > 20 bytes | Retry if empty |

## Command Template

```
exec(
  command: "cd <project> && cursor agent -p --trust [FLAGS] --model auto --workspace . '<prompt>'",
  pty: true,
  timeout: <seconds>
)
```

| Mode | Flags | Timeout | Use |
|------|-------|---------|-----|
| Plan | `--plan` | 180s | Read-only analysis |
| Execute | `--yolo` | 180s | Auto-approve changes |
| Ask | `--mode ask` | 120s | Q&A, no changes |

## Concurrency Control Protocol

### State Tracking

Before launching cursor tasks, track them via `process(action=list)`. Each running exec session with cursor agent counts toward the limit.

### Launch Rules

```
1. Check: process(action=list) → count sessions with "cursor agent" in command
2. If count >= MAX_CONCURRENT (default 4, max 6): WAIT or QUEUE
3. Launch: exec(command=..., pty=true, timeout=T, background=true)
4. Record: sessionId + taskId + startTime
5. Poll: process(action=poll, sessionId=X, timeout=T*1000)
```

### Concurrency Limits by Task Type

| Scenario | Max Concurrent | Why |
|----------|---------------|-----|
| Plan-only (read) | 6 | No file conflicts |
| Execute (write) | 3 | Avoid git/file conflicts |
| Mixed plan+execute | 4 | Balance safety and speed |
| Same-file tasks | 1 (serial only) | NEVER parallel on same file |

## Timeout & Recovery Protocol

### Detection

A task is stuck when:
- `process(action=poll, timeout=T)` returns with process still running after timeout
- Exit code 143 (SIGTERM) or 137 (SIGKILL) = was killed by timeout
- Output is empty (< 20 bytes) after completion = silent failure

### Recovery Steps

```
1. DETECT: poll returns "still running" or exit 143/137 or empty output
2. KILL: process(action=kill, sessionId=X)
3. WAIT: 3 seconds cooldown (avoid API rate limits)
4. SIMPLIFY: reduce prompt scope (fewer files, simpler question)
5. RETRY: relaunch with simplified prompt, same or higher timeout
6. MAX RETRIES: 2 attempts total. After 2 failures → report to user
```

### Simplification Strategy

When a task times out, simplify before retrying:

| Original | Simplified |
|----------|-----------|
| "Scan all dungeon scripts for bugs" | "Scan dungeon_manager.gd for null refs" |
| "Fix 5 issues in this file" | "Fix issue #1 and #2 only" |
| "Analyze architecture of combat system" | "List all functions in arpg_monster.gd" |

## Cleanup Protocol

### When to Clean Up

- Before starting a new batch of tasks
- After any task failure
- On session start (check for orphans)

### How to Clean Up

```
1. process(action=list) → find all cursor-related sessions
2. For each: check if still running
3. If running > 10 minutes: process(action=kill, sessionId=X)
4. Verify: ps aux | grep "cursor agent -p" | grep -v grep
5. Nuclear option: pkill -f "cursor agent -p" (kills ALL cursor CLI agents)
```

### Orphan Detection

Cursor agent processes that outlive their exec session become orphans:
```bash
# Find orphan cursor agent processes
ps aux | grep "cursor agent -p" | grep -v grep
# Kill specific orphan
kill <PID>
```

## Four Dispatch Chains

### Chain A: Direct Execute

For simple tasks (1-3 files, clear logic). Single exec call.

```
exec(
  command: "cd <project> && cursor agent -p --trust --yolo --model auto --workspace . '<task>'",
  pty: true, timeout: 180
)
→ poll → verify output not empty → done
```

### Chain B: Plan → Review → Execute ⭐

For complex tasks. Most reliable chain.

```
Step 1 — PLAN (pty:true, timeout:180):
  "检查 <file> 中会导致运行时崩溃的问题。重点：<specific concerns>。只列会崩溃的。"

Step 2 — REVIEW (agent decides):
  Parse output → grade 🔴🟠🟡🟢 → select fixes for this round

Step 3 — EXECUTE (pty:true, timeout:180):
  "修复 <file> 中 N 个问题：[paste selected items with line numbers and fix code]。
   修复后运行：<verify command>。确认无错误后 git commit。"

Step 4 — VERIFY:
  Run headless build/test to confirm
```

### Chain C: Parallel Batch

For independent tasks across different files. Use background exec.

```
# Launch (respect concurrency limit)
exec(cmd="cursor agent ... task1", pty:true, background:true) → session1
exec(cmd="cursor agent ... task2", pty:true, background:true) → session2
exec(cmd="cursor agent ... task3", pty:true, background:true) → session3

# Monitor
process(action=poll, sessionId=session1, timeout=180000)
process(action=poll, sessionId=session2, timeout=180000)
process(action=poll, sessionId=session3, timeout=180000)

# Verify all
Run headless build/test
```

Rules:
- Max 4 parallel execute tasks (6 for plan-only)
- NEVER parallel on same file
- Check for git conflicts after all complete
- If any fails: kill remaining → fix conflict → retry failed ones

### Chain D: Plan Global → Serial Execute

For large refactors with dependencies.

```
1. Plan pass on each file (can parallel, up to 6)
2. Collect all findings → sort by dependency
3. Execute in dependency order (serial)
4. Verify after each execute before next
5. If verify fails: stop, fix, re-plan remaining
```

## Prompt Engineering for Cursor Agent

### Plan Prompts (what works)

Good: "检查 scripts/dungeon/dungeon_manager.gd 中所有可能返回 null 的函数调用，以及调用方是否有 null 检查"
Good: "列出 <file> 中所有 func 的名字"
Bad: "扫描所有文件找出所有问题" (too broad, will timeout)

### Execute Prompts (what works)

Good: Include exact line numbers + expected code change + verify command + git commit
Bad: Vague "fix the bugs" without specifics

### Template

```
Plan: "检查 <file> 中 <specific concern>。只列会崩溃/卡死的问题，给出行号和修复方案。"
Execute: "修复 <file> 中 N 个问题：
1. 第 X 行：<current code> → <fixed code>
2. 第 Y 行：<current code> → <fixed code>
修复后运行：<verify command>
确认无错误后 git commit -m '<message>'。"
```

## Model Selection

| Task | Model | Timeout |
|------|-------|---------|
| Default | `auto` | — |
| Simple edits | `auto` | 120s |
| Complex analysis | `auto` + `--plan` | 180s |
| Code review | `auto` + `--mode ask` | 120s |

`auto` routes to best available model (typically opus-4.6-thinking). Don't override unless needed.

## Session Resume

```bash
cursor agent ls                              # List past sessions
cursor agent -p --trust --continue "..."     # Continue last
cursor agent -p --trust --resume <id> "..."  # Resume specific
```

## Timing Benchmarks

### v2.6.12 (tested 2026-03-06 evening, cursor 2.6.12)

| Task Type | Time | Concurrency Tested |
|-----------|------|--------------------|
| List functions (small file <50 lines) | 8-14s | 6/6 parallel ✅ |
| List functions (medium file ~600 lines) | 17s | single ✅ |
| List functions (large file ~1000 lines) | 40s | single ✅ |
| Simple execute (add comment, 1 file) | 16-19s | 3/3 parallel ✅ |
| Ask mode (simple Q&A) | 8s | single ✅ |
| Complex analysis (null-check scan, 660 lines) | 84s | single ✅ |
| Long complex prompt (3+ concerns, multi-file ref) | >180s | TIMEOUT ⚠️ |
| Execute with broad prompt (3 bugs, multi-concern) | >180s | TIMEOUT ⚠️ |

### Key Findings (v2.6.12)

- **Simple tasks (list/comment/ask) are MUCH faster** than v2026.02.27 (8-40s vs 55-120s)
- **Complex analysis still takes 60-120s** — similar to old version
- **Broad prompts (3+ separate concerns) STILL timeout** — must split into 1-concern-per-task
- **Silent failures (empty output) reduced** but still occur on timeout
- **6 parallel plan = all pass** in ~53s wall clock (individual 8-14s each)
- **3 parallel execute = all pass** in ~25s wall clock (individual 16-19s each)

### Failure Mode: Prompt Complexity (NOT concurrency)

Timeouts correlate with **prompt complexity**, not concurrency:
- 6 simple tasks parallel → all pass in <20s each
- 1 complex task with 3+ concerns → timeout at 180s
- **Solution**: ALWAYS split multi-concern prompts. One concern per cursor task.

### Previous version (v2026.02.27, tested 2026-03-06 morning)

| Task Type | Time | Concurrency Tested |
|-----------|------|--------------------|
| List functions (1 file) | 15s | 8/8 passed |
| Null-check scan (1 file) | 80-120s | 4/4 parallel ✅ |
| Execute fix (1 file, 1-4 issues) | 55-90s | 3/3 parallel ✅ |
| Multi-file analysis | >180s | TIMEOUT |

## Validated Workflows

### Workflow 1: Parallel Plan → Review → Parallel Execute (2026-03-06)

```
Round 1 (Chain B serial): 3 files × plan→execute = 9 fixes, 3 commits
Round 2 (Chain C parallel): 4 files × plan (parallel) → review → 3 files × execute (parallel) = 3 fixes, 3 commits
Total: 12 runtime crash risks fixed, 6 commits, Godot headless zero errors
```

### Workflow 2: Skip Plan, Direct Execute (2026-03-06 evening)

When you already know exactly what to change, skip Plan and go straight to Execute:
```
3 parallel Execute (different files) = all pass, 16-19s each
Pre-requisite: dispatcher already analyzed the code and wrote precise prompts
```

Key insight: Plan can always be parallelized (read-only). Execute can be parallelized
only when tasks touch different files. Review is always serial (agent decides).
**Critical**: Keep prompts focused — 1 file, 1 concern, specific line numbers.

For model list and CLI parameters, see [references/models-and-params.md](references/models-and-params.md).
