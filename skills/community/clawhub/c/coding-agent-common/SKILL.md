---
name: coding-agent
version: 1.0.0
description: |
  通用的编码代理技能，封装 Codex、Claude Code、OpenCode 等工具。
  使用场景：(1) 构建/创建新功能或应用 (2) 重构大型代码库 (3) Bug 修复 (4) 代码审查 (5) 迭代式编码。
  不适用于：简单的单行修改（直接用 edit），读取代码（用 read 工具）。
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      anyBins:
        - claude
        - codex
        - opencode
        - pi
---

# Coding Agent - 通用编码代理

通过后台进程将编码任务委托给 Codex、Claude Code 或 OpenCode 等代理。

## 🎯 快速选择指南

| 代理 | 特点 | 推荐场景 |
|------|------|----------|
| **Codex** | OpenAI 模型，速度快 | 快速原型、功能开发、Bug 修复 |
| **Claude Code** | Claude 模型，理解力强 | 复杂重构、架构设计、代码审查 |
| **OpenCode** | 开源方案 | 轻量级任务 |

## ⚙️ 执行模式配置

### Codex / OpenCode / Pi - 需要 PTY

```bash
# ✅ 正确用法（需要 pty:true）
exec pty:true command:"codex exec '你的任务描述'"
```

### Claude Code - 不需要 PTY

```bash
# ✅ 正确用法（使用 --print 模式）
exec command:"claude --permission-mode bypassPermissions --print '你的任务描述'"

# 后台执行
exec background:true command:"claude --permission-mode bypassPermissions --print '你的任务描述'"
```

## 🚀 常用命令模板

### 1. 快速一次性任务

```bash
# Codex（需要 git 目录）
exec pty:true workdir:/path/to/project command:"codex exec --full-auto '添加错误处理到 API 调用'"

# Claude Code
exec workdir:/path/to/project command:"claude --permission-mode bypassPermissions --print '添加错误处理到 API 调用'"
```

### 2. 后台长时间任务

```bash
# 启动后台任务
exec pty:true workdir:/path/to/project background:true command:"codex exec --full-auto '重构认证模块'"

# 返回 sessionId，可用于监控
```

### 3. 代码审查

```bash
# 审查当前分支变更
exec pty:true workdir:/path/to/project command:"codex review --base main"

# 审查 PR
exec pty:true workdir:/path/to/project command:"codex exec '审查 PR #130'"
```

### 4. 多任务并行

```bash
# 同时启动多个代理处理不同任务
exec pty:true workdir:/path/to/project background:true command:"codex exec '修复 issue #78'"
exec pty:true workdir:/path/to/project background:true command:"codex exec '修复 issue #99'"
```

## 📋 任务监控

### 查看后台进程

```bash
process action:list
```

### 查看输出日志

```bash
process action:log sessionId:<sessionId>
```

### 检查是否完成

```bash
process action:poll sessionId:<sessionId>
```

### 发送输入

```bash
# 发送文本 + 回车
process action:submit sessionId:<sessionId> data:"yes"

# 发送原始数据（无回车）
process action:write sessionId:<sessionId> data:"some input"
```

### 终止进程

```bash
process action:kill sessionId:<sessionId>
```

## 🔧 Codex CLI 参数

| 参数 | 效果 |
|------|------|
| `exec "prompt"` | 一次性执行，完成后退出 |
| `--full-auto` | 沙箱模式但自动批准工作区内的更改 |
| `--yolo` | 无沙箱，无批准（最快但最危险） |

## 🏗️ 工作目录规则

**重要：** 始终指定 `workdir`，让代理专注于特定目录：

```bash
# ✅ 正确 - 指定工作目录
exec pty:true workdir:/path/to/project command:"codex exec '任务'"

# ❌ 错误 - 无工作目录，代理可能读取不相关文件
exec pty:true command:"codex exec '任务'"
```

## 📝 任务提示词最佳实践

### 好的任务描述

```
构建一个 REST API 端点用于管理待办事项：
- GET /todos - 获取所有待办
- POST /todos - 创建待办
- PUT /todos/:id - 更新待办
- DELETE /todos/:id - 删除待办

要求：
1. 使用 Express.js
2. 添加输入验证
3. 添加错误处理
4. 完成后运行测试
```

### 不好的任务描述

```
写个 todo api
```

### 添加完成通知

对于长时间运行的后台任务，在提示词末尾添加通知命令：

```
...你的任务描述...

完成后运行此命令通知我：
openclaw system event --text "完成: [简要描述]" --mode now
```

## 🛡️ 安全规则

1. **不要在 `~/.openclaw/` 目录启动代理** - 可能读取敏感文件
2. **不要在 Live OpenClaw 实例目录切换分支**
3. **审查 PR 时使用临时目录或 git worktree**
4. **敏感项目使用 `--full-auto` 而非 `--yolo`**

## 🔄 Git Worktree 并行工作流

```bash
# 1. 为每个 issue 创建 worktree
exec command:"git worktree add -b fix/issue-78 /tmp/issue-78 main"
exec command:"git worktree add -b fix/issue-99 /tmp/issue-99 main"

# 2. 在每个 worktree 中启动代理
exec pty:true workdir:/tmp/issue-78 background:true command:"pnpm install && codex exec --full-auto '修复 issue #78'"
exec pty:true workdir:/tmp/issue-99 background:true command:"pnpm install && codex exec --full-auto '修复 issue #99'"

# 3. 监控进度
process action:list

# 4. 完成后创建 PR
exec workdir:/tmp/issue-78 command:"git push -u origin fix/issue-78 && gh pr create --title 'fix: ...' --body '...'"

# 5. 清理
exec command:"git worktree remove /tmp/issue-78"
```

## 📊 进度更新规则

启动后台代理时，保持用户知情：

1. **启动时** - 发送简短消息说明正在运行什么 + 在哪里
2. **更新时** - 只在有变化时更新：
   - 里程碑完成（构建完成、测试通过）
   - 代理提问/需要输入
   - 遇到错误或需要用户操作
   - 代理完成（说明改变了什么 + 在哪里）
3. **终止时** - 如果杀掉会话，立即说明原因

## 🧪 临时工作区（无 git 目录）

Codex 需要 git 目录。对于快速实验：

```bash
# 创建临时 git 目录
$SCRATCH = New-TempDir
exec workdir:$SCRATCH command:"git init"
exec pty:true workdir:$SCRATCH command:"codex exec '你的实验任务'"
```

## ⚠️ 常见问题

### 代理卡住无输出

检查是否忘记 `pty:true`（Codex/OpenCode/Pi 需要）

### Claude Code 过早退出

检查是否使用了 `--dangerously-skip-permissions`，改用 `--permission-mode bypassPermissions --print`

### 找不到文件

检查 `workdir` 是否正确设置

### 权限被拒绝

检查是否在正确的目录，或使用 `--full-auto` 模式

## 🎓 学习笔记（2026年1月）

- **PTY 至关重要** - 编码代理是交互式终端应用
- **需要 git 目录** - Codex 不在 git 目录外运行
- **exec 是好朋友** - `codex exec "prompt"` 运行后干净退出
- **submit vs write** - submit 发送输入 + 回车，write 发送原始数据

---

*让编码代理为你工作 🤖✨*
