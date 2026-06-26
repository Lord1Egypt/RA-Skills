---
name: agent-cli
version: 3.0.0
description: 代码编辑 CLI 工具集合：Cursor CLI（agent）与 Qoder CLI（qodercli）。当用户需要修改代码、重构、Code Review、自动化代码任务时使用。
---

# Agent CLI — 代码编辑工具路由

## 工具选择

| 工具 | 命令 | 适用场景 | 详细文档 |
| :--- | :--- | :--- | :--- |
| **Cursor CLI** | `agent` | 代码重构、Review、Debug、Git 提交信息、自动化 CI | `references/cursorcli.md` |
| **Qoder CLI** | `qodercli` | 交互式代码开发、MCP 集成、多任务并行（worktree）、子 Agent 调度 | `references/qodercli.md` |

## 何时使用

- **写代码 / 改代码 / 重构** → 必须用 Cursor CLI 或 Qoder CLI（禁止直接 exec 改代码）
- **启动前告知用户**：「我打算用 Cursor/Qoder 来处理」
- 保持透明，让用户知道任务去向

## 选择逻辑

1. **已有 Cursor 登录 / 项目有 `.cursor/` 配置** → 优先 Cursor
2. **需要 MCP 集成 / worktree 并行 / 子 Agent** → 用 Qoder
3. **简单代码修改** → 两者均可，默认 Cursor
4. **用户明确指定** → 按用户要求

## 调用方式

两个 CLI 都是 **TUI 程序**，在自动化场景下必须通过 tmux 提供 PTY：

```bash
tmux kill-session -t agent 2>/dev/null || true
tmux new-session -d -s agent
tmux send-keys -t agent "cd /path/to/project" Enter
sleep 1
tmux send-keys -t agent "agent '你的任务'" Enter   # 或 qodercli
```

> ⚠️ 直接 `agent "task"` 或 `qodercli "task"` 会卡死（无 TTY）

## 参考文档

- 详细操作手册 → `references/cursorcli.md`（Cursor）、`references/qodercli.md`（Qoder）
- 安装 / PATH / 登录入口 → `references/README.md`
