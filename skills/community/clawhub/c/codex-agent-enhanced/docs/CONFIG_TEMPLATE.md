# Codex Agent 配置模板

## 环境变量配置

在你的项目中使用 codex-agent 时，需要设置以下环境变量：

### 必需变量
```bash
# Agent 名称（用于选择 bot 账号）
export OPENCLAW_AGENT_NAME="main"  # 或 kimi-agent / gpt-agent / glm-agent

# 通知目标
export OPENCLAW_AGENT_CHAT_ID="7936836901"  # 你的 Telegram Chat ID
export OPENCLAW_AGENT_CHANNEL="telegram"    # 通知渠道
```

### 可选变量（启用项目状态模式）
```bash
# 项目状态文件路径（设置后启用 Cron 巡检模式）
export OPENCLAW_PROJECT_STATE_FILE="/path/to/your/project/.codex-task-state.json"

# 任务 ID（用于状态追踪）
export OPENCLAW_PROJECT_TASK_ID="TASK-001"

# 任务目录
export OPENCLAW_PROJECT_TASK_DIR="/path/to/your/project"
```

---

## Codex 配置

在 `~/.codex/config.toml` 中添加 notify hook：

```toml
# 注意：路径需要根据实际安装位置调整
notify = ["python3", "<SKILL_PATH>/hooks/on_complete.py"]

[features]
multi_agent = true
fast_mode = true
```

**获取 SKILL_PATH**：
```bash
# 如果安装在 workspace/skills/
SKILL_PATH="$HOME/.openclaw/workspace/skills/codex-agent"

# 如果安装在系统 skills 目录
SKILL_PATH="$HOME/.openclaw/skills/codex-agent"
```

---

## Cron Job 配置模板

如果你使用 Cron 巡检模式，创建 `cron/codex-task-waker.json`：

```json
{
  "name": "codex-task-waker",
  "agentId": "<YOUR_AGENT_ID>",
  "schedule": {
    "kind": "every",
    "everyMs": 600000,
    "anchorMs": 1772938800000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "请读取 <WAKER_PROMPT_PATH> 并严格执行。"
  },
  "delivery": {
    "mode": "none"
  },
  "deleteAfterRun": false
}
```

**替换占位符**：
- `<YOUR_AGENT_ID>`: 你的 agent ID（如 `kimi-agent` / `gpt-agent`）
- `<WAKER_PROMPT_PATH>`: waker prompt 路径（如 `$HOME/.openclaw/workspace/skills/codex-agent/tasks/codex-task-waker.prompt.md`）

**添加 Cron Job**：
```bash
openclaw cron add cron/codex-task-waker.json
```

---

## 项目状态文件示例

`.codex-task-state.json`：

```json
{
  "project": "your-project-name",
  "sessionKey": "agent:main:main",
  "notificationRouting": {
    "channel": "telegram",
    "target": "7936836901",
    "accountId": "geq1fan_bot"
  },
  "activeTask": {
    "taskId": "TASK-001",
    "taskDir": "/path/to/task",
    "status": "review_pending",
    "runner": {
      "kind": "codex_exec",
      "completedAt": "2026-03-08T10:00:00+08:00",
      "summary": "任务完成摘要"
    }
  },
  "lastWakeKey": "",
  "updatedAt": "2026-03-08T10:00:00+08:00"
}
```

---

## 完整使用示例

### 1. 设置环境变量
```bash
cd /path/to/your/project
export OPENCLAW_AGENT_NAME="main"
export OPENCLAW_AGENT_CHAT_ID="7936836901"
export OPENCLAW_PROJECT_STATE_FILE="$(pwd)/.codex-task-state.json"
export OPENCLAW_PROJECT_TASK_ID="TASK-001"
```

### 2. 执行 Codex 任务
```bash
codex exec --full-auto "实现 XX 功能"
```

### 3. 等待通知
- Telegram 实时收到完成通知
- Cron 每 10 分钟巡检并推进状态

---

## 故障排查

### Notify 没触发
```bash
# 检查 Codex 配置
grep notify ~/.codex/config.toml

# 测试 notify hook
python3 <SKILL_PATH>/hooks/on_complete.py '{"type":"agent-turn-complete","last-assistant-message":"test"}'

# 查看日志
cat /tmp/codex_notify_log.txt
```

### Cron 没执行
```bash
# 检查 Cron 配置
openclaw cron list

# 查看 Cron 日志
cat /root/.openclaw/cron/logs/*.log | tail -50
```

---

## 日志隔离

Notify hook 的日志文件默认按 **Agent 名称** 隔离：

| Agent | 日志文件路径 |
|-------|-------------|
| `main` | `/tmp/codex_notify_main.log` |
| `kimi-agent` | `/tmp/codex_notify_kimi-agent.log` |
| `gpt-agent` | `/tmp/codex_notify_gpt-agent.log` |
| `glm-agent` | `/tmp/codex_notify_glm-agent.log` |

### 自定义日志路径

如果需要按项目隔离日志，设置：

```bash
export OPENCLAW_LOG_FILE="/path/to/your/project/codex-notify.log"
```

### 查看日志

```bash
# 查看特定 agent 的日志
cat /tmp/codex_notify_kimi-agent.log | tail -20

# 实时跟踪
tail -f /tmp/codex_notify_kimi-agent.log
```

---

## 📁 多项目并发隔离

**重要**：每个项目应该有**独立的 `.env` 文件**，避免参数冲突。

### 错误做法 ❌

```bash
# 全局 export，所有项目共用同一套配置
export OPENCLAW_AGENT_NAME="main"
export OPENCLAW_PROJECT_STATE_FILE="/tmp/state.json"

# 项目 A 和项目 B 同时运行时，参数会互相覆盖！
codex exec ...  # 用哪个项目的配置？
```

### 正确做法 ✅

```bash
# 项目 A
cd /path/to/project-a
source .env  # 加载项目 A 的配置
codex exec --full-auto "任务 A"

# 项目 B（同时运行，互不影响）
cd /path/to/project-b
source .env  # 加载项目 B 的配置
codex exec --full-auto "任务 B"
```

### 项目结构建议

```
project-a/
├── .env                        # 项目 A 专属配置
├── .codex-task-state.json      # 项目 A 状态文件
└── src/

project-b/
├── .env                        # 项目 B 专属配置
├── .codex-task-state.json      # 项目 B 状态文件
└── src/
```

**核心原则**：
- 每个项目独立的 `.env` 文件
- `source .env` 在 `codex exec` 前执行
- 状态文件放在项目目录内（`.codex-task-state.json`）
- 不要全局 export 配置
