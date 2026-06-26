# Workspace Isolation（Git Worktree per Agent）

## Problem

多个 agent 在同一工作目录下操作会互相干扰：agent A 的 `git checkout` 影响 agent B 看到的文件，agent A 的未提交改动污染 agent B 的 `git diff` 输出。共享工作目录是多 agent 冲突的根源。

## Solution

每个 worker agent 使用独立的 git worktree。Worktree 共享同一个 .git 仓库（提交历史、对象存储共享），但有独立的工作目录和 index。Agent 在自己的 worktree 中自由操作，完成后通过 merge/cherry-pick 合并结果。

## Implementation

1. Coordinator 为每个 worker 创建 worktree

```bash
# 从当前 HEAD 创建 worktree
WORKER_ID="worker-parser"
git worktree add ".worktrees/${WORKER_ID}" -b "work/${WORKER_ID}" HEAD

# Worker 在 .worktrees/worker-parser/ 中工作
# 独立的文件系统，独立的 git index
```

2. Worker agent 启动时 cd 到自己的 worktree

```bash
claude -p --cwd ".worktrees/${WORKER_ID}" \
  "在当前目录中完成以下任务：修改 parser.ts..."
```

3. 任务完成后合并结果

```bash
# 方案 A：merge（保留 commit 历史）
git merge "work/${WORKER_ID}" --no-ff

# 方案 B：cherry-pick（只取最终结果）
git cherry-pick "work/${WORKER_ID}"

# 方案 C：diff-apply（最安全，人工 review）
git diff main..."work/${WORKER_ID}" > "${WORKER_ID}.patch"
```

4. 清理 worktree

```bash
git worktree remove ".worktrees/${WORKER_ID}"
git branch -d "work/${WORKER_ID}"
```

## Tradeoffs

- **Pro**: 彻底消除并发文件冲突——每个 agent 有完全独立的文件系统视图
- **Pro**: Git 原生支持，无需额外工具
- **Con**: 磁盘空间消耗（每个 worktree 是完整的工作目录副本）
- **Con**: Merge 冲突在合并阶段集中爆发，需要 coordinator 处理
- **Con**: 共享 .git/objects 下的 gc 和 prune 需要注意时机

## Source

Claude Code worktree 功能。Git worktree 官方文档。OMC Coordinator 模式的 workspace 隔离实践。
