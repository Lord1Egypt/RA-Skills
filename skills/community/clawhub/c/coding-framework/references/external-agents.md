# 外部编码代理委派模式

> 来源：coding-agent skill，适配 coding-framework
> 版本：10.1.0（v10.1 新增安全警告和冲突处理）

## 概述

当任务需要外部编码代理（Codex / Claude Code / Pi）时，使用本指南。

**核心原则**：coding-framework 负责质量治理，外部代理负责执行。

---

## 1. 代理选择

| 代理 | 调用方式 | 适用场景 |
|------|----------|----------|
| Claude Code | `claude --print 'task'` | 复杂重构、代码生成 |
| Codex | `bash pty:true command:"codex exec --full-auto 'task'"` | 快速修复、批量任务 |
| Pi | `bash pty:true command:"pi 'task'"` | 轻量任务 |

---

## 2. 调用模式

### Claude Code（非交互）

```bash
# 前台执行（推荐：使用权限白名单）
bash workdir:~/project command:"claude --allowedTools 'Read,Write,Edit' --print 'Your task'"

# 后台执行
bash workdir:~/project background:true command:"claude --allowedTools 'Read,Write,Edit' --print 'Your task'"
```

> ⚠️ **安全警告（v10.1 新增）**：
> 
> `--permission-mode bypassPermissions` 绕过所有权限检查，**仅适用于完全隔离的沙箱环境**（如 Docker 容器、临时 VM）。
> 
> **不推荐在本地开发环境使用**。生产环境请使用 `--allowedTools` 白名单模式。

### Codex（PTY 模式）

```bash
# 快速一次性任务
bash pty:true workdir:~/project command:"codex exec --full-auto 'Add error handling'"

# 后台长任务
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor auth module'"
```

**注意**：Codex 需要 Git 仓库环境，临时任务用 `mktemp -d && git init`。

---

## 3. Git Worktree 并行修复

用于同时修复多个 Issue，每个 worktree 独立工作目录：

```bash
# 1. 创建 worktree
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. 在每个 worktree 启动代理
bash pty:true workdir:/tmp/issue-78 background:true command:"codex --yolo 'Fix issue #78: <description>. Commit and push.'"
bash pty:true workdir:/tmp/issue-99 background:true command:"codex --yolo 'Fix issue #99. Commit and push.'"

# 3. 监控进度
process action:list
process action:log sessionId:XXX

# 4. 创建 PR
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --head fix/issue-78 --title "fix: ..." --body "..."

# 5. 清理
git worktree remove /tmp/issue-78
```

### Worktree 冲突处理（v10.1 新增）

**约束**：worktree 任务必须修改不相交的文件集。

**冲突检测脚本**：

```bash
#!/bin/bash
# check-worktree-conflict.sh
# 检查多个 worktree 是否修改了相同文件

WORKTREES=("$@")
CONFLICT_FILES=""

for wt in "${WORKTREES[@]}"; do
    files=$(cd "$wt" && git diff --name-only HEAD 2>/dev/null)
    for f in $files; do
        if echo "$CONFLICT_FILES" | grep -q "$f"; then
            echo "⚠️ 冲突文件: $f (在多个 worktree 中被修改)"
        else
            CONFLICT_FILES="$CONFLICT_FILES $f"
        fi
    done
done

if [ -z "$CONFLICT_FILES" ]; then
    echo "✅ 无文件冲突"
else
    echo "📋 已修改文件: $CONFLICT_FILES"
fi
```

**使用方式**：

```bash
# 启动 worktree 前检查
bash check-worktree-conflict.sh /tmp/issue-78 /tmp/issue-99

# 如果检测到冲突，调整任务分配
```

---

## 4. 完成自动通知

在任务 prompt 末尾追加通知命令：

```bash
codex --yolo exec 'Build a REST API.

When completely finished, run:
openclaw system event --text "Done: Built REST API with CRUD endpoints" --mode now'
```

效果：任务完成后立即触发 wake event，无需轮询。

> **依赖说明**：`openclaw` 命令需要在 PATH 中可用。如果使用其他通知方式，可替换为 webhook 或 OS 通知。

---

## 5. 进度更新协议

后台任务执行期间，按以下节奏更新用户：

| 时机 | 内容 |
|------|------|
| 启动时 | 1 条消息：运行什么、在哪里 |
| 里程碑完成 | 构建完成、测试通过等 |
| 需要输入 | 代理提问、需要确认 |
| 出错 | 错误信息、需要用户操作 |
| 完成 | 结果摘要、变更位置 |

---

## 6. 安全约束

- **不在 `~/.openclaw/` 启动外部代理**（会读取 soul docs）
- **不在 OpenClaw 实例目录切换分支**
- **PR 审查在临时目录或 worktree 进行**
- **bypassPermissions 仅在隔离沙箱中使用**（v10.1）
- **worktree 任务必须修改不相交文件集**（v10.1）

---

## 7. 与 coding-framework 集成

```
用户请求
    │
    ├─ 简单编码 → coding-framework 模式 1（快速编码）
    │
    ├─ 复杂编码 → coding-framework 模式 1 + 外部代理
    │   └─ 本指南的调用模式
    │
    ├─ 批量修复 → Git Worktree 并行 + 外部代理
    │   └─ 冲突检测 → 调整任务分配
    │
    └─ 代码审查 → coding-framework 模式 2（代理审查）
```

---

## 8. 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Git | 2.28+ | worktree 支持 |
| Claude Code | latest | `claude` 命令 |
| Codex | latest | `codex` 命令 |
| openclaw | latest | 通知命令（可选） |

**支持平台**：
- macOS
- Linux
- Windows (Git Bash)
