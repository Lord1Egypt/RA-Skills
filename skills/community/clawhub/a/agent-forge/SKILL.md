---
name: agent-forge
description: Create independent OpenClaw agents via interviews. Use when: (1) creating dedicated agent with isolated workspace, (2) generating personality files (SOUL/AGENTS/USER/HEARTBEAT), (3) configuring channel bindings, (4) setting up tool permissions. Updates AGENTS.md team registry. ALWAYS interview requirements, verify configs, test before deploy.
---

## 触发方式

用户说以下任意短语时，启动 Agent Forge：
- "用agent forge skill创建一个子代理"
- "@agent-forge"
- "创建一个agent"
- "新建一个agent"

---

# Agent Forge v2

## Overview
Agent Forge 通过 11 步访谈创建完整、独立、可运行的 OpenClaw agent。

**v2 核心改进：**
- SOUL.md / AGENTS.md / IDENTITY.md 由 Claude 根据访谈结果直接生成（不走脚本模板）
- 自动更新 gateway config（allowAgents + agentToAgent）
- 完整性自检：Claude 对比访谈结果验证文件，不完整则就地修复

---

## 11-Step Workflow

### Step 1: 命名
问: "这个 agent 叫什么名字？"
- Agent ID（小写 + 连字符，如 `code-reviewer`、`sales-bot`）
- 决定 workspace 路径：`~/.openclaw/workspace-{id}/`

### Step 2: 模型选择
问: "用哪个模型？"
选项：
- `minimax-portal/MiniMax-M2.5` — 快速廉价，默认首选
- `kimi-coding/k2p5` — 编程/推理
- `google/gemini-3.1-pro-preview` — 研究/长文本
- `anthropic/claude-sonnet-4-6` — 复杂推理（贵）
- `openrouter/auto` — 自动选最优

### Step 3: 核心职责
问: "这个 agent 的核心职责是什么？"
- 主要任务描述
- 成功指标
- 关键交付物

### Step 4: 频道
问: "监听哪些频道？"
- `telegram`、`discord`、`feishu`，可多选

### Step 5: 工具权限
根据角色推荐工具集，向用户确认：
- 基础：`read`, `write`, `memory_search`, `memory_get`
- 执行：`exec`
- 网络：`web_search`, `web_fetch`
- 通信：`sessions_spawn`, `sessions_send`, `sessions_list`, `message`
- 高级：`browser`, `cron`, `session_status`, `subagents`, `image`

### Step 6: Sandbox 策略
问: "Sandbox 级别？"
- `exec-only` — 仅 exec 受限（推荐默认）
- `all` — 完全隔离
- `none` — 无限制（仅可信 agent）

### Step 7: 个性与风格
问: "这个 agent 的性格/风格？"
- 精炼关键词（如：sharp、autonomous、data-driven）
- 核心使命一句话

### Step 8: Skill 路径
问: "这个 agent 需要哪些专属 skill？存放路径？"
- 记录 skill 路径，写入 AGENTS.md

### Step 9: 生成核心文件（Claude 直接写，不走脚本）

**先执行脚本创建目录和 scaffold：**
```bash
bash ~/.openclaw/workspace/skills/agent-forge/scripts/deploy-agent.sh \
  "{agent-id}" \
  "{model}" \
  "{role}" \
  "{tools}" \
  "{channels}" \
  "{sandbox}" \
  "{personality}"
```

**然后 Claude 根据访谈结果直接写以下三个文件：**

#### IDENTITY.md
写入路径：`~/.openclaw/workspace-{agent-id}/IDENTITY.md`

必须包含：
- `**Name:**` — agent 的名字/昵称
- `**Creature:**` — 角色定位（如 Autonomous Research Engine）
- `**Role:**` — 职责一句话
- `**Vibe:**` — 3-5 个性格关键词
- `**Emoji:**` — 专属 emoji
- `**Mission:**` — 核心使命

#### SOUL.md
写入路径：`~/.openclaw/workspace-{agent-id}/SOUL.md`

必须包含：
- `## Core Identity` — Role、Model、Mission、Tone
- `## Execution Rules` — 执行风格、决策原则、错误处理
- `## Reporting Style` — ❌错误示例 / ✅正确示例
- `## Revenue Orientation` — 如何将职责转化为收入
- `## Boundaries` — 禁止事项
- `## Continuity` — 每次启动读哪些文件

#### AGENTS.md
写入路径：`~/.openclaw/workspace-{agent-id}/AGENTS.md`

必须包含：
- `## About This Agent` — ID、Model、Role、Workspace、Channels
- `## Session Startup` — 启动序列（读哪些文件，按什么顺序）
- `## Skills` — skill 名称 + 路径 + 用途
- `## 跨 Agent 通信协议` — 见下方模板
- `## Team Registry` — 可以联系的其他 agent（从 main AGENTS.md 同步）

**跨 Agent 通信协议模板（必须包含）：**

```markdown
## 跨 Agent 通信协议

### 何时用 sessions_spawn vs sessions_send

| 场景 | 方法 | 原因 |
|------|------|------|
| 当前回合必须拿到最终结果 | 阻塞式路径：`sessions_send(timeoutSeconds>0)` 或 `subagents` | 不把 fire-and-forget 当同步执行 |
| 派发独立后台任务（允许稍后完成） | `sessions_spawn(agentId="target-id", task="...")` | 仅用于真正异步的后台工作 |
| 向已活跃 agent 发消息 | `sessions_send(sessionKey="...", message="...")` | 需要目标 agent 有活跃 session |

### 查找目标 agent 的 sessionKey
1. 调用 `sessions_list()` 查看所有活跃 session
2. 找到 label 匹配目标 agent ID 的 session
3. 取其 `sessionKey` 传入 `sessions_send`

### 注意事项
- `sessions_spawn` 受 `subagents.allowAgents` 控制
- `sessions_send` 受 `tools.agentToAgent` 控制
- 两者都需要目标 agent ID 在相应白名单中
- 不要默认优先 `sessions_spawn`。只有后台异步工作才使用它。

### 可联系的 Agent
（从 main AGENTS.md Team Registry 同步当前团队列表）
```

### Step 10: Gateway Config 自动更新

文件写入完成后，立即调用 `gateway config.patch` 更新：

1. **`agents.list[main].subagents.allowAgents`** — 追加新 agent ID
2. **`tools.agentToAgent.allow`** — 追加新 agent ID
3. **`tools.sessions.visibility`** — 确保为 `"all"`

示例 patch（以 `new-agent` 为例）：
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": ["executor", "research-master", "content-master", "new-agent"]
        }
      }
    ]
  },
  "tools": {
    "sessions": { "visibility": "all" },
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "content-master", "research-master", "new-agent"]
    }
  }
}
```

⚠️ **注意：** `config.patch` 使用深度合并，`agents.list` 数组合并规则是按 `id` 匹配更新。只传需要修改的字段即可，不会覆盖其他 agent 配置。

### Step 11: 完整性自检

Claude 读取生成的三个文件，对比访谈结果逐项检查：

**检查清单：**

| 文件 | 必须包含 | 检查方式 |
|------|---------|---------|
| IDENTITY.md | Name/Creature/Role/Vibe/Emoji/Mission 全部非空 | 逐行检查 |
| SOUL.md | 5个必须 section 全部存在且有实质内容 | 检查 ## 标题 + 内容长度 |
| AGENTS.md | 跨 agent 通信协议表格存在、Session Startup 存在、Skills 存在 | 检查关键字 |

**自检结果：**
- ✅ 全部通过 → 输出文件摘要给用户确认
- ⚠️ 有缺失 → 就地修复，修复后重新自检，然后输出摘要

**输出摘要格式：**
```
✅ Agent [{agent-id}] 部署完成

📁 文件状态：
- IDENTITY.md ✅ — {name}, {emoji}, {vibe关键词}
- SOUL.md ✅ — {mission一句话}
- AGENTS.md ✅ — {skill数量} skills, 跨 agent 协议 ✓
- USER.md ✅ — 从 main 复制 + agent 差异化
- HEARTBEAT.md ✅
- MEMORY.md ✅
- TOOLS.md ✅

⚙️ Gateway Config：
- allowAgents: {完整列表}
- agentToAgent.allow: {完整列表}
- sessions.visibility: all

📋 下一步（需要手动完成）：
1. 在 openclaw.json 中为此 agent 添加完整配置（model、workspace、tools）
2. 如需 Telegram 频道：添加 botToken 到 channels.telegram.accounts
3. 添加 channel binding：agentId + match.accountId
```

---

## 生成文件目录结构

```
~/.openclaw/
├── agents/
│   └── {agent-id}/
│       └── agent/
│           └── config.json
└── workspace-{agent-id}/
    ├── SOUL.md        ← Claude 写（访谈驱动）
    ├── AGENTS.md      ← Claude 写（访谈驱动）
    ├── IDENTITY.md    ← Claude 写（访谈驱动）
    ├── USER.md        ← 脚本写（从 main 复制 + agent diff）
    ├── HEARTBEAT.md   ← 脚本写
    ├── MEMORY.md      ← 脚本写
    ├── TOOLS.md       ← 脚本写
    └── memory/
```

---

## Best Practices

1. **SOUL/AGENTS/IDENTITY 必须由 Claude 写** — 脚本模板太通用，无法体现 agent 个性
2. **访谈完成后立即写文件** — 不要"记在脑子里"再写
3. **写完立即自检** — 不等用户问
4. **Gateway config 必须更新** — 否则 main 无法 spawn 新 agent
5. **自检摘要给用户确认** — 这是 agent 上线前最后一道门

---

## Resources

| File | Purpose |
|------|---------|
| `scripts/deploy-agent.sh` | 创建目录 + scaffold 文件（USER/HEARTBEAT/MEMORY/TOOLS） |
| `scripts/remove-agent.sh` | 删除 agent 及清理 |
| `references/openclaw-multi-agent.md` | 架构参考 |
