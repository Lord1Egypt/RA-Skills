# 示例：Cron 巡检模式（完整工作流）

适合场景：正式项目，需要状态追踪和自动推进。

## 项目结构

```
my-project/
├── .codex-task-state.json    # 项目状态文件（自动生成）
├── tasks/
│   └── TASK-001/             # 任务目录
│       ├── prompt.md
│       ├── codex-result.md
│       └── acceptance.md
├── cron/
│   └── codex-task-waker.json # Cron Job 配置
└── src/                      # 源代码
```

## Step 1: 设置环境变量

```bash
cd /path/to/my-project

export OPENCLAW_AGENT_NAME="kimi-agent"
export OPENCLAW_AGENT_CHAT_ID="7936836901"
export OPENCLAW_AGENT_CHANNEL="telegram"

# 启用 Cron 模式
export OPENCLAW_PROJECT_STATE_FILE="$(pwd)/.codex-task-state.json"
export OPENCLAW_PROJECT_TASK_ID="TASK-001"
export OPENCLAW_PROJECT_TASK_DIR="$(pwd)/tasks/TASK-001"
```

## Step 2: 配置 Cron Job

创建 `cron/codex-task-waker.json`：

```json
{
  "name": "codex-task-waker",
  "agentId": "kimi-agent",
  "schedule": {
    "kind": "every",
    "everyMs": 600000,
    "anchorMs": 1772938800000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "请读取 /root/.openclaw/skills/codex-agent/tasks/codex-task-waker.prompt.md 并严格执行。"
  },
  "delivery": {
    "mode": "none"
  },
  "deleteAfterRun": false
}
```

**添加 Cron Job**：
```bash
openclaw cron add cron/codex-task-waker.json
```

## Step 3: 执行 Codex 任务

```bash
codex exec --full-auto "实现用户认证功能，包括登录、注册、JWT token 生成"
```

## Step 4: 观察流程

### 立即发生
- Telegram 收到通知：
  ```
  [KIMI-AGENT] 🔔 Codex 任务完成
  
  📁 /path/to/my-project
  💬 已完成：实现了用户认证功能...
  ```

### 10 分钟内（Cron 巡检）
- Cron 唤醒主会话
- 读取 `.codex-task-state.json`
- 检查 git 变更和输出质量
- 判断是否满意：
  - ✅ 满意 → 更新状态为 `committed`，汇报用户
  - ❌ 不满意 → 更新状态为 `blocked`，通知用户

## Step 5: 查看状态

```bash
# 查看当前状态
cat .codex-task-state.json | python3 -m json.tool

# 查看 Cron 执行日志
openclaw cron list
```

## 状态流转示例

```
初始状态:
{
  "activeTask": {
    "taskId": "TASK-001",
    "status": "codex_running",
    "runner": { "status": "running" }
  }
}

↓ Codex 完成

{
  "activeTask": {
    "taskId": "TASK-001",
    "status": "review_pending",
    "runner": {
      "status": "completed",
      "completedAt": "2026-03-08T11:00:00+08:00",
      "summary": "已完成..."
    }
  }
}

↓ Cron 检查满意

{
  "activeTask": null,
  "lastCommittedTask": "TASK-001"
}
```

---

**相关文件**：
- `../../hooks/on_complete.py` — Notify hook 实现
- `../../tasks/codex-task-waker.prompt.md` — Waker Prompt
- `../../docs/CONFIG_TEMPLATE.md` — 配置模板
