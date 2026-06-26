---
name: chc
description: Claw Help Claude - OpenClaw manages Claude Code CLI lifecycle. Use when: (1) starting Claude Code CLI sessions, (2) managing multiple Claude Code instances, (3) multi-turn conversations with Claude Code, (4) user mentions "claude code", "chc", "启动claude", or wants to use Claude Code through OpenClaw.
---

# CHC - Claw Help Claude

OpenClaw 管理 Claude Code CLI 的完整生命周期，实现用户与 Claude Code 的双向通信。

## 两种模式

| 模式 | 推荐 | 输出质量 | 多轮支持 | 使用场景 |
|------|------|----------|----------|----------|
| **ACP** | ⭐ 优先 | ✅ 干净文本 | ✅ 自动持久化 | 正常工作、多轮对话 |
| **PTY** | 备选 | ⚠️ ANSI 噪音 | ✅ 手动管理 | ACP 不可用时 |

**优先使用 ACP 模式**，PTY 作为降级方案。

---

## ACP 模式（推荐）

通过 acpx CLI 驱动 Claude Code，输出干净、支持多轮对话。

### 前置检查

```bash
# 检查 acpx 是否安装
~/.openclaw/npm/node_modules/.bin/acpx --version

# 如果没有，安装
npm install acpx --prefix ~/.openclaw/npm
```

### 会话生命周期

```bash
ACPX_CMD="$HOME/.openclaw/npm/node_modules/.bin/acpx"
PROJECT_DIR="/path/to/project"
SESSION_NAME="my-project"

# 1. 创建持久会话
$ACPX_CMD --cwd $PROJECT_DIR claude sessions new --name "$SESSION_NAME"

# 2. 发送消息（多轮）
$ACPX_CMD --cwd $PROJECT_DIR claude -s "$SESSION_NAME" "分析这个项目结构"
$ACPX_CMD --cwd $PROJECT_DIR claude -s "$SESSION_NAME" "继续深入分析配置文件"
$ACPX_CMD --cwd $PROJECT_DIR claude -s "$SESSION_NAME" "帮我优化这段代码"

# 3. 关闭会话
$ACPX_CMD --cwd $PROJECT_DIR claude sessions close "$SESSION_NAME"
```

**关键点：**
- `-s "$SESSION_NAME"` 指定会话名称，实现多轮对话
- `--cwd` 必须每次指定相同目录
- 会话自动保持上下文，Claude 会记住之前的对话

### 输出格式

ACP 输出干净、有标记：

```
[thinking] 用户想知道项目结构...
[tool] ls -la (completed)
[tool] find . -name "*.json" (completed)
[done] end_turn
```

### 常用操作

```bash
# 查看所有会话
$ACPX_CMD --cwd $PROJECT_DIR claude sessions

# 查看会话状态
$ACPX_CMD --cwd $PROJECT_DIR claude status -s "$SESSION_NAME"

# 取消正在执行的命令
$ACPX_CMD --cwd $PROJECT_DIR claude cancel -s "$SESSION_NAME"
```

### sessions_spawn ACP（one-shot）

也可以用 `sessions_spawn`，但这是 **one-shot 模式**，执行完就结束：

```json
{
  "runtime": "acp",
  "agentId": "claude",
  "cwd": "/path/to/project",
  "label": "task-name",
  "task": "一次性任务描述"
}
```

**适用场景：** 单次任务，不需要后续对话。

---

## PTY 模式（备选）

直接通过 PTY 运行 Claude Code CLI，ACP 不可用时使用。

### 启动交互式会话

```bash
# 启动 PTY 会话
exec(command="claude", pty=true, cwd="/path/to/project")
```

返回 session ID，如 `fast-glade`。

### 发送消息

```
process(action=write, sessionId="fast-glade", data="你的问题")
process(action=send-keys, keys=["Enter"])
```

### 接收响应

```
process(action=poll, sessionId="fast-glade", timeout=120000)
```

**注意：** PTY 输出包含 ANSI 控制字符，需要过滤解析：
```
[2D[3B[2K[G[1A[2C[2A你好[7m ... ← ANSI 噪音
```

### 多轮对话

```
# 第一轮
process(action=write, sessionId="xxx", data="问题1")
process(action=send-keys, keys=["Enter"])
process(action=poll, sessionId="xxx", timeout=120000)

# 第二轮（同一 session）
process(action=write, sessionId="xxx", data="问题2")
process(action=send-keys, keys=["Enter"])
process(action=poll, sessionId="xxx", timeout=120000)
```

### 结束会话

```
process(action=kill, sessionId="xxx")
```

---

## 实例管理

### 查看运行的会话

```bash
# ACP 会话
~/.openclaw/npm/node_modules/.bin/acpx --cwd ~/project claude sessions

# PTY 会话
process(action=list)
```

### 多实例场景

| 场景 | 建议 |
|------|------|
| 单项目开发 | 保持单一会话 |
| 多项目并行 | 每项目独立会话（不同 SESSION_NAME） |
| PR 审查 + 开发 | 分离两个会话 |

### 会话命名建议

使用语义化名称：
- `hope-main` - Hope 项目主会话
- `coding-pr` - PR 审查专用
- `quick-test` - 临时测试

---

## 常见问题

### Q: ACP spawn 失效？
检查 `~/.acpx/config.json`，删除错误的配置：
```bash
rm ~/.acpx/config.json
```

然后用 npx 默认方式。

### Q: Claude Code 无响应？
ACP：尝试 `claude cancel -s "$SESSION_NAME"`
PTY：发送空消息唤醒，或 kill 重启

### Q: 如何切换项目？
启动新会话指向新目录：
```bash
$ACPX_CMD --cwd /new/project claude sessions new --name "new-project"
```

### Q: 会话历史丢失？
- ACP：会话自动持久化，重新连接即可
- PTY：检查 `~/.claude/sessions/` 中的 JSON 文件

---

## 配置文件

- `~/.claude/settings.json` - Claude Code API 配置
- `~/.claude/sessions/*.json` - 会话持久化
- `~/.acpx/config.json` - acpx 自定义配置（可选）

## 参考文档

- Claude Code CLI: https://docs.anthropic.com/claude-code
- ACP 协议: https://github.com/agentclientprotocol