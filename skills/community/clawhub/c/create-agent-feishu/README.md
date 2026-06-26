# openclaw-create-agent

在 OpenClaw 中创建和管理 Agent 智能体的 Skill。

## 功能

- 创建新的 Agent 智能体
- 配置 workspace 目录结构
- 设置记忆系统文件
- 配置 openclaw.json
- 绑定飞书 channel
- 配置多 agent 协作权限

## 快速开始

### 创建 Agent

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace/agents/myagent/{memory,diary,output,.openclaw}

# 2. 写入人格文件
cp templates/IDENTITY.md ~/.openclaw/workspace/agents/myagent/
cp templates/SOUL.md ~/.openclaw/workspace/agents/myagent/
cp templates/AGENTS.md ~/.openclaw/workspace/agents/myagent/

# 3. 注册到 openclaw.json
# 在 agents.list 中添加：
{
  "id": "myagent",
  "name": "myagent",
  "workspace": "/root/.openclaw/workspace/agents/myagent",
  "agentDir": "/root/.openclaw/agents/myagent",
  "memorySearch": { "enabled": true },
  "subagents": {
    "allowAgents": ["*"]
  }
}

# 4. 配置飞书账号并绑定
# 5. 重启 Gateway
openclaw gateway restart
```

## 目录结构

```
~/.openclaw/workspace/agents/<agent-name>/
├── AGENTS.md              # 工作规范
├── IDENTITY.md            # 身份档案
├── SOUL.md                # 灵魂定义
├── MEMORY.md              # 长期记忆
├── USER.md                # 用户档案
├── TOOLS.md               # 工具备忘
├── HEARTBEAT.md           # 心跳任务
├── memory/                # 每日记忆
├── diary/                 # 私密日记
├── output/                # 任务输出
└── .openclaw/
    └── workspace-state.json
```

## 重要配置说明

### 模型配置（v1.1.0 更新）

**不在单个 agent 中配置模型**，而是通过全局默认模型统一设置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      }
    }
  }
}
```

所有 agent 继承 `agents.defaults.model.primary` 指定的默认模型。

### 多 Agent 协作配置（v1.2.0 更新）

配置 `subagents.allowAgents` 控制 agent 能否 spawn 其他 agents：

```json
{
  "subagents": {
    "allowAgents": ["*"]      // 允许 spawn 任何 agent
    // "allowAgents": ["player", "writer"]  // 白名单模式
    // "allowAgents": []  // 只能 spawn 自己
  }
}
```

| 配置值 | 效果 |
|--------|------|
| `["*"]` | `agents_list` 返回所有 agents，可 spawn 任何 agent |
| `["player", "writer"]` | 只返回指定的 agents，只能 spawn 这些 agent |
| `[]` 或未配置 | 只返回自己，只能 spawn 自己 |

## 版本历史

### v1.2.0
- 新增 `subagents.allowAgents` 配置
- 支持多 agent 发现与协作
- 更新快速开始示例

### v1.1.0
- 移除 agent 级别的 `model` 字段配置
- 模型统一通过 `agents.defaults.model` 设置
- 完善文档结构

### v1.0.0
- 初始版本
- 支持 Agent 创建、飞书绑定、目录结构初始化
