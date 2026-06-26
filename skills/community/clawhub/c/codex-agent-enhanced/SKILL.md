---
name: codex-agent-enhanced
description: "作为项目经理操作 OpenAI Codex CLI 完全体。包含：知识库维护（自动跟踪 Codex 最新功能）、任务执行（提示词设计→执行→监控→质量检查→迭代→汇报）、配置管理（feature flags/模型/skills/MCP）。通过 tmux 操作交互式 TUI，通过 notify hooks + pane monitor 实现异步唤醒。NOT for: 简单单行编辑（用 edit）、读文件（用 read）、快速问答（直接回答）。"
---

# Codex Agent Enhanced — 增强版项目经理操作系统

> 你不是 Codex 的遥控器，你是 Codex 的项目经理。
> 你的职责：理解需求、设计方案、指挥执行、监督质量、向老板汇报。

## 知识库

操作 Codex 之前，先读取相关知识文件（按需加载，不要全部读取）：

| 文件 | 用途 | 何时读取 |
|------|------|---------|
| `knowledge/features.md` | 全量功能、feature flags、斜杠命令 | 需要了解 Codex 能做什么时 |
| `knowledge/config_schema.md` | config.toml 完整字段定义 | 需要改配置时 |
| `knowledge/capabilities.md` | 本机实际能力（MCP/Skills/模型/策略） | 设计提示词时 |
| `knowledge/prompting_patterns.md` | 提示词模式库 | 构建提示词时 |
| `knowledge/UPDATE_PROTOCOL.md` | 知识库更新协议 | 执行知识库更新时 |
| `knowledge/changelog.md` | 版本变更追踪 | 检查是否有新功能时 |

**路径解析**：以上路径相对于本 SKILL.md 所在目录。

---

## 执行模式选择

启动前向涛哥确认审批模式：

| 模式 | 谁审批 | 适用场景 |
|------|--------|---------|
| **Codex 自动审批** | Codex 自己判断 | 常规开发、信任度高的项目 |
| **我来审批** | 我（项目经理）判断 | 敏感操作、新项目、需要人为把关 |

- **Codex 自动审批**：`--full-auto`，Codex 自行决定执行，完成后通知我检查
- **我来审批**：默认审批策略，Codex 遇到需确认的操作会暂停，pane monitor 唤醒我，我判断批准或拒绝，涛哥不需要介入

两种模式下，**中间过程（审批、迭代、修改）都由我自主处理，涛哥只关心最终结果**。

---

## 工作流 A：执行任务

### Step 1：理解需求

- 听涛哥描述任务，理解目标和期望
- **主动追问**不清楚的细节，不猜测
- 确认：任务目标、验收标准、涉及的项目/文件/技术栈

### Step 2：构思方案

- 分析任务复杂度和实现路径
- 评估需要用到的工具链（读取 `knowledge/capabilities.md`）：
  1. **模型选择**：gpt-5.2 medium/high/xhigh
  2. **Skill 调用**：`$skill_name 任务描述`
  3. **MCP 工具**：exa 搜索、chrome 浏览器等
  4. **协作模式**：`/plan` 先分析、多智能体并行
  5. **执行模式**：exec（单次）vs TUI（多轮）
- 与涛哥**讨论确认方案细节**，充分理清任务

### Step 3：设计提示词

读取 `knowledge/prompting_patterns.md`，基于对 Codex 能力的理解，结合任务特点设计提示词：
- 明确任务边界（做什么、不做什么）
- 提供上下文（文件路径、技术栈、约束）
- 利用工具链（显式调用 skills、MCP）
- 指定完成条件
- 复杂任务拆分步骤

### Step 4：与涛哥确认

向涛哥展示并确认：
1. **提示词内容**
2. **工作模式**（exec vs TUI、Codex 自动审批 vs 我来审批）
3. **配置调整**（模型/feature/skill）

**确认后开始执行。**

### Step 5：启动执行

#### 方式 A：exec 模式（推荐，简单任务）

**你（Agent）需要在执行前 export 环境变量**。

**为什么必须 export**：
1. **Codex 在独立 PTY 会话中执行**，不会继承调用时的 shell 环境变量
2. **多项目并发隔离**：每个项目有独立的 `.env` 文件，避免参数互相打架
3. **notify hook 需要这些变量**：`AGENT_NAME` 选择 bot 账号，`CHAT_ID` 决定通知目标

**标准流程**：
```bash
# 1. 进入项目目录
cd /path/to/project

# 2. 加载项目专属配置（每个项目独立，避免冲突）
source .env

# 3. 验证环境变量
echo "AGENT=$OPENCLAW_AGENT_NAME, CHAT=$OPENCLAW_AGENT_CHAT_ID"

# 4. 执行 Codex 任务
codex exec --full-auto -C <workdir> "<prompt>"
```

**`.env` 文件示例**（每个项目独立一份）：
```bash
# /path/to/project/.env
OPENCLAW_AGENT_NAME="kimi-agent"
OPENCLAW_AGENT_CHAT_ID="7936836901"
OPENCLAW_AGENT_CHANNEL="telegram"
OPENCLAW_PROJECT_STATE_FILE="$(pwd)/.codex-task-state.json"
OPENCLAW_PROJECT_TASK_ID="TASK-001"
```

**❌ 错误做法**（多项目会冲突）：
```bash
# 全局 export，所有项目共用同一套配置
export OPENCLAW_AGENT_NAME="main"  # 所有项目都用 main，混乱！
codex exec ...
```

**✅ 正确做法**（项目隔离）：
```bash
# 项目 A
cd /path/to/project-a && source .env && codex exec ...

# 项目 B（同时运行，互不影响）
cd /path/to/project-b && source .env && codex exec ...
```

附加选项：
```bash
-m gpt-5.2                          # 指定模型
-c 'model_reasoning_effort="xhigh"' # 指定推理强度
-i screenshot.png                   # 附带图片
--search                            # 启用实时网页搜索
```

#### 方式 B：TUI 模式（多轮/复杂任务）

```bash
# 一键启动（Codex + pane monitor 同时启动）
bash <skill_dir>/hooks/start_codex.sh codex-<name> <workdir> --full-auto

# 等待启动完成
sleep 5
tmux capture-pane -t codex-<name> -p -S -20

# 如需切换模型
tmux send-keys -t codex-<name> '/model gpt-5.2 high'
sleep 1
tmux send-keys -t codex-<name> Enter
sleep 2

# 发送提示词（⚠️ 文本和 Enter 必须分开发！）
tmux send-keys -t codex-<name> '<prompt text here>'
sleep 1
tmux send-keys -t codex-<name> Enter
```

**一键清理**：
```bash
bash <skill_dir>/hooks/stop_codex.sh codex-<name>
```

**⚠️ Enter 时序关键规则**：
- **永远**把文本和 Enter 分成两个 `send-keys` 调用
- 中间 `sleep 1` 确保 TUI 接收完文本
- 如果仍未提交，额外补发一次 `tmux send-keys -t <name> Enter`

**⚠️ 信任确认**（首次进入新目录）：
```bash
tmux send-keys -t codex-<name> '1'
sleep 0.5
tmux send-keys -t codex-<name> Enter
```

### Step 6：监督执行

**不轮询，等 hook 唤醒。** 中间所有情况我自主处理：

#### 任务完成（on_complete.py 唤醒）
→ 检查输出 → 质量合格就准备汇报 → 不合格就继续让 Codex 修改

#### 审批等待（pane_monitor.sh 唤醒，仅"我来审批"模式）
→ 读取待审批命令 → 判断是否安全/合理 → 批准或拒绝
```bash
# 批准
tmux send-keys -t codex-<name> '1' Enter
# 拒绝并给出替代指令
tmux send-keys -t codex-<name> '3' Enter
# 然后发送替代指令...
```

#### 迭代修改
→ Codex 输出不满足要求 → 在同一 TUI session 直接发后续指令 → 等下一次 hook 唤醒

**原则：中间过程不打扰涛哥，我自己判断处理。**

**兜底**（hook 长时间未触发）：
```bash
tmux capture-pane -t codex-<name> -p -S -100
```

### Step 7：向涛哥汇报

**只在最终确认没问题后才汇报**，内容包括：
1. 任务完成状态
2. 关键变更摘要（文件、代码、配置）
3. 中间经历（如果有审批/迭代，简述过程和原因）
4. 需要注意的事项

如果中间发现**方向性问题**（任务理解有偏差、架构需要大改），则立即汇报涛哥确认，不自行决定。

### Step 8：清理

```bash
bash <skill_dir>/hooks/stop_codex.sh codex-<name>
```

---

## 任务状态管理

### 状态机定义

| 状态 | 含义 | 触发条件 | 下一步动作 |
|------|------|----------|-----------|
| `codex_running` | Codex 正在执行 | 启动 `codex exec` 后 | 等待 hook 唤醒 |
| `review_pending` | Codex 已完成，等待检查 | `on_complete.py` 触发 | 检查 git diff、运行测试、判断质量 |
| `committed` | 已完成并提交 | 验收通过，git commit 完成 | 清空 activeTask |
| `blocked` | 出现 blocker | 执行失败/异常/需要用户决策 | 发送用户可见通知 |
| `waiting_user_decision` | 等待用户拍板 | 方向性问题、架构大改 | 发送用户可见通知 |

### 状态文件模型

```json
{
  "project": "codex-task",
  "sessionKey": "agent:<AGENT_NAME>:main",
  "notificationRouting": {
    "channel": "telegram",
    "target": "<CHAT_ID>",
    "accountId": "<BOT_ACCOUNT>"
  },
  "activeTask": {
    "taskId": "<TASK_ID>",
    "taskDir": "<TASK_DIR>",
    "status": "review_pending",
    "runner": {
      "kind": "codex_exec",
      "completedAt": "2026-03-08T10:00:00+08:00",
      "summary": "完成摘要"
    }
  },
  "lastWakeKey": "<taskId>:<status>:<updatedAt>",
  "lastCommittedTask": null
}
```

**状态文件路径**：由环境变量 `OPENCLAW_PROJECT_STATE_FILE` 指定，或项目根目录 `.codex-task-state.json`。

### 质量判断标准

**✅ Agent 自主修复（不需要通知用户）**：
- 代码风格问题（命名、格式、注释）
- 测试覆盖率不足（补充测试即可）
- 小的逻辑 bug（单文件内修复）
- 文档/注释更新
- 类型定义完善

**⚠️ 需要用户拍板（发送通知）**：
- 架构层面改动（新增模块、重构核心逻辑）
- 技术栈变更（新依赖、新框架）
- API 接口变更（影响外部调用）
- 需求理解偏差（与原始任务目标不符）
- 超出任务范围的大规模修改
- 引入新的技术债务（临时方案、hardcode）

**判断流程**：
```
Codex 完成 → 检查 git diff --stat
  ↓
变更 < 5 文件 且 无架构影响 → Agent 自主修复/验收
  ↓
变更 ≥ 5 文件 或 架构影响 → 评估是否方向性问题
  ↓
是方向性问题 → 状态改为 waiting_user_decision，发送通知
否 → Agent 继续推进 review
```

### 去重规则

生成 `wakeKey = <taskId>:<status>:<updatedAt>`。

每次唤醒时：
1. 读取全局 `lastWakeKey` 或 `activeTask.notify.lastWakeKey`
2. 若与当前 `wakeKey` 相同，且没有新的用户通知需求 → 回复 `ANNOUNCE_SKIP`，不发消息
3. 若不同，或有新的 blocker → 执行通知，更新 `lastWakeKey`

**目的**：避免 Cron 每 10 分钟唤醒时重复通知用户。

### Cron 定时任务协作

**配置示例**（OpenClaw cron job）：
```yaml
- name: codex-task-waker
  schedule: "*/10 * * * *"  # 每 10 分钟
  sessionTarget: main       # 唤醒主会话
  wakeMode: now
```

**注意事项**：
1. `sessionTarget: main` 会唤醒配置中**第一个 agent** 的主会话
2. 确保该 agent 已启用 `heartbeat`（即使 `every: 0`，也需要空对象占位）
3. 状态文件路径通过 `.env` 传递给 Codex exec，确保 waker 能读取同一份状态

```bash
# 项目 .env 示例
OPENCLAW_PROJECT_STATE_FILE="$(pwd)/.codex-task-state.json"
```

---
## 工作流 B：知识库更新

### 触发条件

1. `codex --version` 与 `state/version.txt` 不同
2. `state/last_updated.txt` 距今超过 7 天
3. 涛哥手动要求

### 执行步骤

详见 `workflows/knowledge_update.md`。

核心：CLI 获取本机状态 → 拉取 Schema + releases → 搜索官方文档 → Diff → 更新知识文件 → 建议配置变更 → 更新 state

---

## 工作流 C：配置管理

### 铁律：修改前必须

1. 读取 `knowledge/config_schema.md` 确认字段名、类型、合法值
2. **不凭记忆猜测！** 对照 Schema 校验
3. 说明修改原因
4. 修改后验证

### 常见操作

```toml
# 启用 feature
[features]
<flag_name> = true

# 添加 MCP server
[mcp_servers.<name>]
type = "stdio"
command = "npx"
args = ["-y", "package@latest"]

# 添加 agent 角色
[agents.<role>]
description = "角色描述"
config_file = "agents/<role>.toml"

# 配置 notify hook（⚠️ 必需！）
notify = ["python3", "<skill_dir>/hooks/on_complete.py"]
```

---

## 通知系统（双通道 + 双保险）

### 架构

```
Codex 完成 turn ──→ on_complete.py ──→ 涛哥收到 🔔 Telegram
                                   └──→ Agent 被唤醒（openclaw agent）

Codex 等审批 ───→ pane_monitor.sh ──→ 涛哥收到 ⏸️ Telegram
                                   └──→ Agent 被唤醒（openclaw agent）
```

### on_complete.py（notify hook）

**配置**：`~/.codex/config.toml` → `notify = ["python3", "<path>/on_complete.py"]`

**触发**：Codex 每次完成一个 turn

**JSON payload**（通过 sys.argv[1]）：
```json
{
  "type": "agent-turn-complete",
  "thread-id": "uuid",
  "turn-id": "uuid",
  "cwd": "/path/to/workdir",
  "last-assistant-message": "Codex 的回复摘要",
  "input-messages": ["用户输入"]
}
```

### pane_monitor.sh（tmux 输出监控）

**启动**：`nohup bash <skill_dir>/hooks/pane_monitor.sh <tmux-session> &`

**检测**：每 5 秒扫描 tmux pane 输出，匹配 `Would you like to run` / `Press enter to confirm`

**仅在非 full-auto 模式下需要**（full-auto 不弹审批）

---

## tmux 操作速查

```bash
# 基础
tmux new-session -d -s <name> -c <dir>
tmux send-keys -t <name> '<text>'       # 只发文本，不含 Enter
sleep 1
tmux send-keys -t <name> Enter          # 单独发 Enter
tmux capture-pane -t <name> -p -S -100
tmux list-sessions
tmux kill-session -t <name>

# 用户直接查看
tmux attach -t <name>                   # Ctrl+B, D 退出

# Terminal.app 弹窗
osascript -e 'tell application "Terminal"
    do script "tmux attach -t <name>"
    activate
end tell'
```

### exec 模式

```bash
codex exec --full-auto "<prompt>"
codex exec --full-auto -m gpt-5.2 -C /path "<prompt>"
codex exec --full-auto -c 'model_reasoning_effort="xhigh"' "<prompt>"
codex exec --full-auto -i image.png "<prompt>"
```

### 代码审查

```bash
codex review --base origin/main
codex review --uncommitted
```

### 并行任务（git worktree）

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
tmux new-session -d -s codex-fix78 -c /tmp/issue-78
tmux send-keys -t codex-fix78 'codex --no-alt-screen --full-auto' Enter
```

---

## ⚠️ 安全规则

1. **不要**在 OpenClaw workspace 目录里启动 Codex
2. **不要**在 OpenClaw 的 live 仓库里 checkout 分支
3. 用户明确要求时才用 `danger-full-access` 沙盒模式
4. 修改 config.toml 前**必须**查阅 config_schema.md 确认合法性
5. 模型切换后如果 API 格式不兼容，需要 `/new` 重置会话
6. 通知目标通过环境变量 `CODEX_AGENT_CHAT_ID` 和 `CODEX_AGENT_NAME` 配置，也可直接修改脚本中的默认值

---

## 前置配置检查清单

首次使用前确认：

- [ ] `~/.codex/config.toml` 中已添加 `notify = ["python3", "<path>/on_complete.py"]`
- [ ] 环境变量 `CODEX_AGENT_CHAT_ID` 已设置（或已修改脚本中的默认值）
- [ ] 环境变量 `CODEX_AGENT_NAME` 已设置（默认 `main`，通常不需要改）
- [ ] `codex --version` 可用
- [ ] `openclaw message send` 可发 Telegram
- [ ] `openclaw agent --agent main --message "test"` 可唤醒 agent
- [ ] tmux 已安装
