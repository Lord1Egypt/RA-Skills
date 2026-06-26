---
name: openclaw-create-agent
version: 1.2.0
description: 在 OpenClaw 中创建一个新的 Agent 智能体，包括 workspace 目录结构、记忆系统文件、openclaw.json 配置修改、飞书 channel 与 binding 设置。适用于新增 AI 分身、多角色管理等场景。
---

## 使用场景

当用户需要以下操作时激活此 Skill：
- "帮我创建一个新智能体"
- "新增一个 agent"
- "配置一个飞书机器人"
- "给我的小说角色/助手/分身创建一个 agent"
- "openclaw 怎么加 agent"

## 核心概念

### 两个目录的分工

| 目录 | 用途 | 是否手动维护 |
|------|------|--------------|
| `~/.openclaw/workspace/agents/<agent>/` | **灵魂工作区**（人格、记忆、日记、规范） | ✅ 手动创建和维护 |
| `~/.openclaw/agents/<agent>/` | **运行时数据**（session 历史、models.json） | ❌ 系统自动生成 |

> **原则：永远不要在 `~/.openclaw/agents/` 里手动创建文件。**

## Agent 目录标准结构

创建 agent 时，在 `~/.openclaw/workspace/agents/<agent-name>/` 下建立以下文件和目录：

```
~/.openclaw/workspace/agents/<agent-name>/
├── AGENTS.md              # 工作规范、安全策略、心跳行为
├── IDENTITY.md            # 身份档案（名字、物种、气质、签名台词、emoji）
├── SOUL.md                # 灵魂定义（核心性格、说话方式、价值观锚点）
├── MEMORY.md              # 长期记忆（职责、配置、重要决策的蒸馏记录）
├── USER.md                # 关于用户的人类档案（只存在于 main session）
├── TOOLS.md               # 本地工具备忘（设备昵称、SSH、偏好声音等）
├── HEARTBEAT.md           # 心跳任务清单（为空则跳过）
├── BOOTSTRAP.md           # 首次启动引导（可选，完成后可删除）
├── memory/                # 每日记忆文件（`YYYY-MM-DD.md`）
├── diary/                 # 私密日记（碎片、观察、未请求的思考）
├── saves/                 # 游戏/项目存档（如适用）
├── output/                # 任务/项目输出文件（详见 AGENTS.md 规范）
└── .openclaw/
    └── workspace-state.json   # 状态标记
```

### Output 文件夹规范（重要）

**核心原则：所有任务/项目的输出文件必须结构化存放在 `output/` 目录下。**

```
output/
├── task-001-description/     # 任务子目录
│   ├── README.md            # 任务说明和上下文
│   ├── files...             # 任务相关文件
│   └── result/              # 最终输出
├── project-name/            # 项目子目录
│   ├── src/                 # 源代码
│   ├── assets/              # 资源文件
│   └── docs/                # 文档
└── ...
```

**执行规则：**
1. **每个新任务/项目** → 在 `output/` 下创建一个子目录
2. **子目录命名** → 使用 `task-序号-简短描述` 或 `项目名称` 格式
3. **默认创建** → 执行文件操作前，先创建 `output/` 目录（如不存在）
4. **文件归属** → 所有生成的文件、下载的内容、脚本输出都放入对应子目录

**为什么重要：**
- 避免工作区根目录混乱
- 任务可追踪、可回溯
- 便于清理和归档
- 支持多任务并行

### 必备文件清单（最小可运行集）

| 文件 | 作用 | 必填 |
|------|------|------|
| `AGENTS.md` | 定义 Every Session 行为、记忆规则、安全边界 | ✅ |
| `IDENTITY.md` | 定义 "我是谁" | ✅ |
| `SOUL.md` | 定义 "我如何思考与表达" | ✅ |
| `MEMORY.md` | 长期记忆的容器 | ✅ |
| `USER.md` | 用户档案（main agent 强烈建议，其他可选） | 建议 |
| `TOOLS.md` | 环境专属备忘 | 建议 |
| `HEARTBEAT.md` | 周期性检查任务 | 可选 |
| `.openclaw/workspace-state.json` | 标记 onboarding 完成 | 建议 |
| `memory/` | 存放每日记忆 | ✅ |
| `diary/` | 私密日记空间 | 建议 |

## 配置文件修改：`~/.openclaw/openclaw.json`

### 第 1 步：注册 Agent

在 `agents.list` 数组中添加：

```json
{
  "id": "<your-agent-id>",
  "name": "<your-agent-name>",
  "workspace": "/root/.openclaw/workspace/agents/<your-agent-id>",
  "agentDir": "/root/.openclaw/agents/<your-agent-id>",
  "memorySearch": {
    "enabled": true
  },
  "subagents": {
    "allowAgents": ["*"]
  }
}
```

> **占位符说明**：
> - `<your-agent-id>`: Agent 的唯一标识，如 `writer`, `assistant`, `novelist`
> - `<your-agent-name>`: 显示名称（可选，默认等于 id）

**字段说明**：
- `id`: Agent 的唯一标识符，全系统唯一，不能与其他 agent 重复
- `name`: 显示名称（可选），在日志和回复中显示
- `workspace`: **灵魂工作区路径**，系统会从这里读取人格文件（`IDENTITY.md`, `SOUL.md` 等）
- `agentDir`: **运行时路径**，系统会自动创建 `sessions/` 和 `models.json`
- `memorySearch.enabled`: 是否开启向量记忆检索，建议开启
- `subagents.allowAgents`: 允许该 agent spawn 的其他 agent 列表，`["*"]` 表示允许 spawn 任何 agent

> **关于模型配置**：模型不在 agent 级别单独配置，而是通过全局 `agents.defaults.model` 统一设置，所有 agent 继承默认模型。如需为特定 agent 指定不同模型，可在 `openclaw.json` 的 `agents.defaults.models` 中定义别名引用。

### 关于 `subagents.allowAgents`

`subagents.allowAgents` 配置控制该 agent 能否通过 `sessions_spawn` 启动其他 agent，以及在 `agents_list` 中能看到哪些 agent。

| 配置值 | 含义 | `agents_list` 效果 |
|--------|------|-------------------|
| `["*"]` | 允许 spawn 任何 agent | `allowAny: true`，显示所有 agents |
| `["player", "writer"]` | 白名单模式 | 只显示指定的 agents |
| `[]` 或未配置 | 只能 spawn 自己 | 只返回自己 |

**建议**：对于需要多 agent 协作的场景，设置为 `["*"]` 以启用完整的 agent 发现能力。

### 第 2 步：配置飞书 Channel 账号

在 `channels.feishu.accounts` 下添加账号（与 `agents` 配置独立，可复用给多个 agents）：

```json
"<your-feishu-account-id>": {
  "appId": "<your-app-id>",
  "appSecret": "<your-app-secret>",
  "dmPolicy": "pairing",
  "groupPolicy": "pairing",
  "allowFrom": [],
  "groupAllowFrom": []
}
```

> **占位符说明**：
> - `<your-feishu-account-id>`: 飞书账号标识，任意字符串，如 `mybot`, `writer-feishu`
> - `<your-app-id>`: 从飞书开放平台获取的 AppID（格式如 `cli_xxxxxxxx`）
> - `<your-app-secret>`: 从飞书开放平台获取的 AppSecret

**Channel 策略详细说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `appId` | string | ✅ | 飞书应用的 AppID，从[飞书开放平台](https://open.feishu.cn/app)获取 |
| `appSecret` | string | ✅ | 飞书应用的 AppSecret，与 AppID 配对 |
| `dmPolicy` | string | ✅ | 私聊策略，见下表 |
| `groupPolicy` | string | ✅ | 群聊策略，见下表 |
| `allowFrom` | string[] | 可选 | 私聊白名单，仅这些 open_id 可私聊 |
| `groupAllowFrom` | string[] | 可选 | 群聊白名单，仅这些 open_id 可在群中@机器人 |
| `requireMention` | boolean | 可选 | 群聊中是否需要@机器人才响应 |

**Policy 策略类型详解**：

| 策略值 | 含义 | 使用场景 |
|--------|------|----------|
| `"pairing"` | 需要先完成配对 | 私密 agent，需要控制访问权限 |
| `"open"` | 任何人都可以交互 | 公开 agent，如客服、信息查询 |
| `"allowlist"` | 仅白名单用户可交互 | 特定人群使用，结合 `allowFrom` 配置 |

**注意事项**：
- 首次使用 `pairing` 策略时，私聊会收到配对码提示，需要在 Kimi Claw Web 设置页查看配对码并输入
- `allowFrom` 和 `groupAllowFrom` 中填写的是用户的 open_id（格式 `ou_xxxxxxxx`）

### 第 3 步：绑定 Agent 到飞书账号（Bindings）

在 `bindings` 数组中添加，将 agent 与飞书 channel 账号关联：

```json
{
  "agentId": "<your-agent-id>",
  "match": {
    "channel": "feishu",
    "accountId": "<your-feishu-account-id>"
  }
}
```

> **绑定逻辑说明**：
> - `agentId`: 指向 `agents.list` 中定义的 agent id
> - `match.channel`: 渠道类型，这里是 `feishu`
> - `match.accountId`: 指向 `channels.feishu.accounts` 中定义的账号 key

**绑定匹配规则**：

当飞书 channel 收到消息时，OpenClaw 按以下顺序匹配：

1. 确定消息来源的飞书账号（`accountId`）
2. 在 `bindings` 中查找 `match.accountId` 匹配的条目
3. 根据 `agentId` 找到对应的 agent 配置
4. 将消息路由到该 agent 的 workspace 处理

**一对一 vs 一对多**：

- **一对一绑定**（推荐）：一个飞书账号绑定一个 agent
  ```json
  { "agentId": "writer", "match": { "channel": "feishu", "accountId": "writer-feishu" } }
  ```

- **一对多绑定**：多个飞书账号可以绑定到同一个 agent
  ```json
  { "agentId": "assistant", "match": { "channel": "feishu", "accountId": "assistant-bot-1" } }
  { "agentId": "assistant", "match": { "channel": "feishu", "accountId": "assistant-bot-2" } }
  ```

- **多对一绑定**：一个飞书账号根据条件路由到不同 agents（需要高级匹配规则）

## 完整创建流程（以创建 writer agent 为例）

以下示例假设你要创建一个名为 `writer` 的 agent，绑定到飞书账号 `writer-feishu`：

### Step 1: 创建目录

```bash
mkdir -p /root/.openclaw/workspace/agents/writer/{memory,diary,output,.openclaw}
```

> **注意**：`output/` 目录用于存放所有任务/项目的输出文件，遵循 AGENTS.md 中的 Output 文件夹规范。

### Step 2: 写入人格文件

创建以下文件（内容根据人设定制）：
- `IDENTITY.md` — 名字、气质、signature line、emoji
- `SOUL.md` — 核心性格、说话方式、品味与厌恶
- `AGENTS.md` — 工作规范、记忆规则、心跳行为、**Output 文件夹规范**
- `MEMORY.md` — 长期记忆起始页（职责、变更记录）
- `USER.md` — 用户档案模板
- `TOOLS.md` — 环境备忘模板
- `HEARTBEAT.md` — 可先留空或写注释

### Step 3: 写入状态文件

```bash
cat > /root/.openclaw/workspace/agents/writer/.openclaw/workspace-state.json << 'EOF'
{
  "version": 1,
  "onboardingCompletedAt": "2026-04-14T02:46:05.000Z"
}
EOF
```

### Step 4: 修改 `~/.openclaw/openclaw.json`

**① 注册 agent**（添加到 `agents.list`）：

```json
{
  "id": "writer",
  "name": "writer",
  "workspace": "/root/.openclaw/workspace/agents/writer",
  "agentDir": "/root/.openclaw/agents/writer",
  "memorySearch": {
    "enabled": true
  }
}
```

> **注意**：模型不在 agent 级别配置，而是继承全局默认模型或通过 `agents.defaults.model` 统一设置。

**② 配置飞书 channel**（添加到 `channels.feishu.accounts`）：

```json
"writer-feishu": {
  "appId": "cli_xxxxxxxxxxxxxxxx",
  "appSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "dmPolicy": "pairing",
  "groupPolicy": "pairing",
  "allowFrom": [],
  "groupAllowFrom": []
}
```

> ⚠️ 替换 `cli_xxxxxxxxxxxxxxxx` 和 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 为你从飞书开放平台获取的真实凭证。

**③ 绑定 agent 到飞书**（添加到 `bindings`）：

```json
{
  "agentId": "writer",
  "match": {
    "channel": "feishu",
    "accountId": "writer-feishu"
  }
}
```

### Step 5: 重启 Gateway

```bash
openclaw gateway restart
```

> **必须在执行前明确告知用户："我现在将重启 OpenClaw Gateway 以应用新配置。"**

### Step 6: 验证连接

查看日志确认 WebSocket 已建立：

```bash
cat /root/.openclaw/logs/openclaw.log | grep "feishu\[writer-feishu\]"
```

预期输出：
```
feishu[writer-feishu]: starting WebSocket connection...
feishu[writer-feishu]: received message from ...
```

## 常见错误与排查

### 1. "Channel is required when multiple channels are configured"
- 如果为 agent 创建了 cron job，但没有显式指定 `channel`，会报此错
- 解决：在 cron 配置中添加 `"channel": "feishu"` 和 `"accountId": "writer-feishu"`

### 2. 飞书消息没有路由到新 agent
- 检查 `bindings` 中的 `accountId` 是否与 `channels.feishu.accounts` 的 key 一致
- 检查 `agentId` 是否与 `agents.list` 中的 `id` 一致
- 检查 `openclaw.json` 语法是否合法（逗号、括号匹配）
- 检查 `channels.feishu.enabled` 是否为 `true`

### 3. 配对失败
- 如果 `dmPolicy` 是 `pairing`，首次私聊需要配对码
- 配对码可通过 Kimi Claw Web 设置页查看，或让已配对用户转发

### 4. "appId or appSecret not configured"
- 检查飞书应用的凭证是否正确填写
- 检查飞书应用是否在[开放平台](https://open.feishu.cn/app)启用并发布了版本

## 完整最小配置示例

以下是一个完整可运行的 `openclaw.json` 片段，展示 agent、channel、bindings 三者的关联：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      }
    },
    "list": [
      {
        "id": "writer",
        "name": "writer",
        "workspace": "/root/.openclaw/workspace/agents/writer",
        "agentDir": "/root/.openclaw/agents/writer",
        "memorySearch": { "enabled": true },
        "subagents": {
          "allowAgents": ["*"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "writer",
      "match": { "channel": "feishu", "accountId": "writer-feishu" }
    }
  ],
  "channels": {
    "feishu": {
      "enabled": true,
      "domain": "feishu",
      "requireMention": false,
      "defaultAccount": "main-bot",
      "accounts": {
        "writer-feishu": {
          "appId": "cli_xxxxxxxxxxxxxxxx",
          "appSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          "dmPolicy": "pairing",
          "groupPolicy": "pairing",
          "allowFrom": [],
          "groupAllowFrom": []
        }
      }
    }
  }
}
```

> **注意**：
> - 模型配置在 `agents.defaults.model` 中统一设置，所有 agent 继承此默认模型
> - `subagents.allowAgents: ["*"]` 启用完整的 agent 发现和多 agent 协作能力

**关键对应关系图解**：

```
┌─────────────────────────────────────────────────────────────┐
│  Message arrives at Feishu (appId: cli_xxxxxxxx)            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Channel: channels.feishu.accounts["writer-feishu"]         │
│  → Identified accountId: "writer-feishu"                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Binding: bindings.find(b => b.match.accountId === "writer-feishu")
│  → Found: { agentId: "writer", ... }                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent: agents.list.find(a => a.id === "writer")            │
│  → Found: { workspace: "/root/.openclaw/workspace/agents/writer" }
│  → Load SOUL.md, IDENTITY.md, MEMORY.md from this path      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent "writer" processes the message and replies           │
└─────────────────────────────────────────────────────────────┘
```
