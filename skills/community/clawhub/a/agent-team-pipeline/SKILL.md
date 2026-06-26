---
name: agent-team-pipeline
description: Use when needing to coordinate multiple AI agents in parallel for code development, testing, and review
---

# Agent Team Pipeline

## Overview

Coordinate OpenClaw as the brain dispatching multiple Codex instances in parallel: one for coding, one for testing, one for code review. Each agent works in an isolated git worktree to avoid conflicts.

## When to Use

- Need to implement a feature with separate code/test/review phases
- Want parallel execution of independent tasks
- Building a mini development team workflow

**Not for:**
- Single simple tasks (use single agent)
- Exploratory discussions requiring multi-round dialogue

## Core Pattern

```
User → OpenClaw (brain) → Codex Coder → Codex Tester → Codex Reviewer
                        → Codex Tester (parallel)
                        → Codex Reviewer (parallel)
```

## Setup

### 1. Create Isolated Worktrees

```bash
cd /Users/liuchang/.openclaw/workspace
git worktree add -b coder /Users/liuchang/agent-coder HEAD
git worktree add -b tester /Users/liuchang/agent-tester HEAD
git worktree add -b reviewer /Users/liuchang/agent-reviewer HEAD
```

### 2. Task Distribution Script

```bash
#!/bin/bash
CODER_DIR="/Users/liuchang/agent-coder"
TESTER_DIR="/Users/liuchang/agent-tester"
REVIEWER_DIR="/Users/liuchang/agent-reviewer"

case "$1" in
    coder)
        cd "$CODER_DIR" && codex exec "$2"
        ;;
    tester)
        cd "$TESTER_DIR" && codex exec "$2"
        ;;
    reviewer)
        cd "$REVIEWER_DIR" && codex exec "$2"
        ;;
esac
```

### 3. Workflow

1. **Coder** receives task, writes code to `agent-coder/`
2. **Tester** receives code, writes tests to `agent-tester/`
3. **Reviewer** reviews code, provides feedback
4. Loop: Coder addresses feedback → Reviewer confirms

## Quick Reference

| Role | Worktree | Command |
|------|----------|---------|
| Coder | `agent-coder` | `codex exec "implement X"` |
| Tester | `agent-tester` | `codex exec "test X"` |
| Reviewer | `agent-reviewer` | `codex exec "review X"` |

## Example

```bash
# Coder: Implement feature
codex exec "创建登录功能，使用 JWT"

# Tester: Write tests  
codex exec "为 ../agent-coder/login.py 写测试"

# Reviewer: Review code
codex exec "审查 ../agent-coder/login.py"
```

## Common Mistakes

- **No worktree isolation** → Use git worktree to prevent file conflicts
- **Sequential when parallel** → Coder+Tester+Reviewer can run in parallel
- **Skipping review loop** → Always verify fixes with reviewer before accepting

## Real-World Impact

Successfully implemented hello.py example:
- Coder created initial code
- Tester wrote pytest file  
- Reviewer suggested main() + `__main__` protection
- Coder applied fixes
- Reviewer confirmed compliance
