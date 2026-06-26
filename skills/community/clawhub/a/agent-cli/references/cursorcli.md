---
name: cursor-agent-core
version: 2.1.0
description: Cursor CLI 使用规范（高密度压缩版，适用于Agent调用）
author: optimized
---

# Cursor CLI 核心操作

---

## 1. 基础调用

### 交互模式

```bash
agent
agent "task"
```

### 非交互（CI）

```bash
agent -p "task"
agent --print "task"
```

---

## 2. 模型管理

```bash
agent models
agent --model gpt-5
```

交互内：

```
/models
```

---

## 3. Session 管理

```bash
agent ls
agent resume
agent --resume="[chat-id]"
```

---

## 4. 上下文注入

```
@file.ts
@dir/
```

---

## 5. Slash Commands

```
/models
/compress
/rules
/commands
/mcp enable xxx
/mcp disable xxx
```

---

## 6. 快捷键

* Shift+Enter → 多行输入
* Ctrl+D → 退出（双击）
* Ctrl+R → Review diff
* ↑ → 历史记录

---

## 7. 输出格式

```bash
agent -p "task" --output-format text
agent -p "task" --output-format json
agent -p "task" --output-format stream-json --stream-partial-output
```

---

## 8. 强制执行

```bash
agent -p "task" --force
```

说明：

* 跳过确认
* 自动修改代码

---

## 9. 多媒体输入

```bash
agent -p "analyze screenshot.png"
```

---

## ⚠️ 10. 自动化 / AI Agent（关键）

### 问题

无 TTY → agent 会卡死

---

### ❌ 错误方式

```bash
agent "task"
subprocess.run(["agent"])
```

---

### ✅ 正确方式（tmux）

```bash
# 创建 session
tmux kill-session -t cursor 2>/dev/null || true
tmux new-session -d -s cursor

# 进入项目目录
tmux send-keys -t cursor "cd /path/to/project" Enter
sleep 1

# 执行任务
tmux send-keys -t cursor "agent 'task'" Enter

# 首次信任 workspace
sleep 3
tmux send-keys -t cursor "a"

# 等待执行
sleep 60

# 获取输出
tmux capture-pane -t cursor -p -S -100
```

---

### 原理

* agent 是 TUI 程序
* 必须运行在 PTY（伪终端）
* tmux 提供 PTY

---

## 11. Rules 系统

自动加载：

* `.cursor/rules`
* `AGENTS.md`
* `CLAUDE.md`

编辑：

```
/rules
```

---

## 12. MCP

自动读取：

* `mcp.json`

控制：

```
/mcp enable xxx
/mcp disable xxx
```

---

## 13. 工作流模板

### Code Review

```bash
agent -p "review current branch vs main, focus security & performance"
```

### Refactor

```bash
agent -p "refactor code for readability and type safety"
```

### Debug

```bash
agent -p "analyze error log: xxx"
```

### Git 提交

```bash
agent -p "generate commit message (conventional commits)"
```

### CI / 批处理

```bash
agent -p "audit security" --output-format json --force
agent -p "run tests and generate coverage"
```

---

## 多文件分析

```
@src/api/
@src/models/

review consistency between API and models
```
