---
name: agent-recruiter
description: |
  招聘 Agent 工具 - 创建、配置和管理 OpenClaw Agent。
  参考 [agency-agents](https://github.com/msitarzewski/agency-agents) 的专业 agent 模板结构。
  
  **当以下情况时使用此 Skill**:
  (1) 需要创建新的 Agent（如 Tim、Mike 等）
  (2) 需要为 Agent 配置飞书群绑定
  (3) 需要复制现有 Agent 的配置模板
  (4) 用户提到"招聘 agent"、"创建 agent"、"配置 agent"
  
  **核心文件**:
  - 自动化脚本：`~/.openclaw/workspace-recruiter/skills/agent-recruiter/scripts/recruit-agent.sh`
  - 模板目录：`~/.openclaw/workspace-recruiter/skills/agent-recruiter/templates/`
---

# Agent Recruiter - 招聘 Agent 工具

## 🎯 一键招聘（推荐）

**用法**:
```bash
# 基础用法 - 创建常驻 Agent（绑定群聊）
~/.openclaw/workspace-recruiter/skills/agent-recruiter/scripts/recruit-agent.sh <agent_id> <agent_name> [群聊 ID]

# 示例：创建 Tim 维护专员，绑定到指定群
~/.openclaw/workspace-recruiter/skills/agent-recruiter/scripts/recruit-agent.sh tim "Tim 维护专员" <群聊 ID>
```

**脚本会自动完成**:
1. ✅ 创建 Agent 目录结构 (`~/.openclaw/agents/<id>/agent/` + `~/.openclaw/workspace-<id>/`)
2. ✅ 生成 agent.json 配置
3. ✅ 复制 models.json 和 auth-profiles.json
4. ✅ 生成 SOUL.md、AGENTS.md、IDENTITY.md 模板
5. ✅ 更新 openclaw.json（添加 agent 和 binding）
6. ✅ 重启 Gateway

---

## 📁 Agent 文件结构（参考 agency-agents）

每个 Agent 包含以下核心文件：

```
~/.openclaw/
├── agents/
│   └── <agent_id>/
│       └── agent/
│           ├── agent.json           # Agent 基本配置
│           ├── models.json          # 模型配置
│           └── auth-profiles.json   # 认证配置
│
├── workspace-<agent_id>/
│   ├── SOUL.md                      # ⭐ Agent 人格和身份（核心）
│   ├── AGENTS.md                    # 工作区规范
│   ├── IDENTITY.md                  # 名称、Emoji、Vibe
│   ├── TOOLS.md                     # 本地工具配置
│   ├── USER.md                      # 用户信息
│   ├── HEARTBEAT.md                 # 定期任务清单
│   └── memory/
│       ├── YYYY-MM-DD.md            # 每日日志
│       └── MEMORY.md                # 长期记忆
│
└── openclaw.json
    ├── agents.list[]                # Agent 注册列表
    └── bindings[]                   # 消息路由绑定
```

### 核心文件说明

| 文件 | 作用 | 必填 |
|------|------|------|
| **SOUL.md** | Agent 的人格、使命、工作流程、成功指标 | ⭐ 必填 |
| **AGENTS.md** | 工作区使用规范、记忆系统、工具指南 | ✅ 推荐 |
| **IDENTITY.md** | 名称、Emoji、Vibe、专业领域 | ✅ 推荐 |
| **agent.json** | OpenClaw 注册配置 | ⭐ 必填 |

---

## 📋 SOUL.md 模板结构（参考 agency-agents）

```markdown
# SOUL.md - Who You Are

## 🧠 Your Identity & Memory
- **Role**: [核心角色定位]
- **Personality**: [性格特点]
- **Memory**: [记住的成功模式]
- **Experience**: [经历过的案例]

## 🎯 Your Core Mission
### [核心职责 1]
- [具体任务]
- [可量化目标]

### [核心职责 2]
- [具体任务]
- [交付标准]

## 🚨 Critical Rules You Must Follow
### [规则类别 1]
- [必须遵守的规则]

## 📋 Your Technical Deliverables
### [交付物示例]
```code
// 代码或模板示例
```

## 🔄 Your Workflow Process
### Step 1: [阶段名]
- [行动]
- [产出]

## 💭 Your Communication Style
- **Be [特质]**: "示例表达"

## 📊 Your Success Metrics
You're successful when:
- [可量化指标 1]
- [可量化指标 2]
```

---

## 🚀 手动创建 Agent（学习用）

### 步骤 1: 创建目录结构
```bash
mkdir -p ~/.openclaw/agents/<agent_id>/agent
mkdir -p ~/.openclaw/workspace-<agent_id>
```

### 步骤 2: 创建 agent.json
```json
{
  "id": "<agent_id>",
  "name": "<agent_name>",
  "workspace": "/Users/junchen/.openclaw/workspace-<agent_id>",
  "agentDir": "/Users/junchen/.openclaw/agents/<agent_id>/agent",
  "model": "modelstudio/qwen3.5-plus"
}
```

### 步骤 3: 复制模型和认证配置
```bash
cp ~/.openclaw/agents/mike/agent/models.json ~/.openclaw/agents/<agent_id>/agent/
cp ~/.openclaw/agents/mike/agent/auth-profiles.json ~/.openclaw/agents/<agent_id>/agent/
```

### 步骤 4: 创建核心文件
```bash
# 使用模板
cp ~/.openclaw/workspace-recruiter/skills/agent-recruiter/templates/SOUL.md.template ~/.openclaw/workspace-<agent_id>/SOUL.md
cp ~/.openclaw/workspace-recruiter/skills/agent-recruiter/templates/AGENTS.md.template ~/.openclaw/workspace-<agent_id>/AGENTS.md
cp ~/.openclaw/workspace-recruiter/skills/agent-recruiter/templates/IDENTITY.md.template ~/.openclaw/workspace-<agent_id>/IDENTITY.md

# 编辑内容
vim ~/.openclaw/workspace-<agent_id>/SOUL.md
vim ~/.openclaw/workspace-<agent_id>/IDENTITY.md
```

### 步骤 5: 更新 openclaw.json
在 `agents.list` 添加：
```json
{
  "id": "<agent_id>",
  "name": "<agent_name>",
  "workspace": "/Users/junchen/.openclaw/workspace-<agent_id>",
  "agentDir": "/Users/junchen/.openclaw/agents/<agent_id>/agent",
  "model": "modelstudio/qwen3.5-plus"
}
```

在 `bindings` 添加（绑定群聊）：
```json
{
  "type": "route",
  "agentId": "<agent_id>",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "<群聊 ID>"
    }
  }
}
```

### 步骤 6: 重启 Gateway
```bash
openclaw gateway restart
```

---

## 📚 示例 Agent

### Tim - 维护专员
参考模板：`templates/examples/tim/SOUL.md` 和 `templates/examples/tim/IDENTITY.md`

**职责**:
- 每小时系统健康巡检
- cron/agent/skill 监控
- 异常告警和修复

**配置**:
```bash
# 创建 Tim
./scripts/recruit-agent.sh tim "Tim 维护专员" <群聊 ID>

# 自定义 SOUL.md
vim ~/.openclaw/workspace-tim/SOUL.md
```

---

## 🔧 工具函数

### 检查 Agent 是否存在
```bash
ls ~/.openclaw/agents/<agent_id>/agent/agent.json 2>/dev/null && echo "✅ 存在" || echo "❌ 不存在"
```

### 查看 Agent 配置
```bash
cat ~/.openclaw/agents/<agent_id>/agent/agent.json
cat ~/.openclaw/workspace-<agent_id>/SOUL.md
```

### 查看 Binding 路由
```bash
cat ~/.openclaw/openclaw.json | grep -A8 '"agentId": "<agent_id>"'
```

### 测试 Gateway 状态
```bash
openclaw gateway status
```

### 列出所有 Agent
```bash
cat ~/.openclaw/openclaw.json | jq '.agents.list[].id'
```

---

## ⚠️ 注意事项

1. **agent_id 必须唯一** - 不能与现有 agent 重复
2. **workspace 目录必须存在** - 否则 agent 启动会失败
3. **SOUL.md 是核心** - 定义 Agent 的人格和行为
4. **models.json 和 auth-profiles.json 必须配置** - 否则无法调用模型
5. **Binding 路由的群 ID 必须正确** - 否则消息无法路由
6. **修改 openclaw.json 后必须重启 Gateway** - 配置才能生效

---

## 📚 参考资源

- **agency-agents**: https://github.com/msitarzewski/agency-agents
  - 144 个专业化 Agent 模板
  - 涵盖 Engineering、Design、Marketing、Sales 等 12 个部门
  - 专业的 SOUL.md 结构和成功指标定义

- **Agent 目录**: `~/.openclaw/agents/`
- **Workspace 目录**: `~/.openclaw/workspace-<agent_id>/`
- **配置文件**: `~/.openclaw/openclaw.json`
- **Gateway 日志**: `/tmp/openclaw/openclaw-*.log`
- **OpenClaw 文档**: `/opt/homebrew/lib/node_modules/openclaw/docs`

---

## 🔄 优化现有 Agent 的 SOUL/IDENTITY

### 适用场景
- Agent 已创建，但 SOUL.md/IDENTITY.md 还是模板
- 需要根据具体职责定制人格和工作流程
- 参考 agency-agents 的 144 个专业模板来匹配角色

### 优化流程

#### Step 1: 读取现有配置
```bash
cat ~/.openclaw/workspace-<agent_id>/SOUL.md
cat ~/.openclaw/workspace-<agent_id>/IDENTITY.md
```
**识别**: 哪些是模板占位符（如 `[Agent 显示名称]`），哪些已有内容

#### Step 2: 参考 agency-agents 模板
- 浏览 https://github.com/msitarzewski/agency-agents
- 找最匹配的角色类别（Engineering、Sales、Marketing 等）
- 参考对应模板的 SOUL.md 结构

**常见角色参考**:
| 角色类型 | agency-agents 参考 |
|----------|-------------------|
| 系统维护/DevOps | engineering-devops-automator.md |
| 资讯分析师 | research-news-analyst.md |
| 金融分析师 | sales-sales-pipeline-analyst.md |
| 客服支持 | support-customer-success.md |

#### Step 3: 结合用户需求定制
- 问清楚 Agent 的具体职责（4 大板块以内）
- 确定使用的工具/技能（如 Tavily、cron、API 等）
- 明确输出格式和交付标准

#### Step 4: 更新 SOUL.md + IDENTITY.md
**保持 agency-agents 结构**:
- 🧠 Identity & Memory
- 🎯 Core Mission（分板块，每板块有默认要求）
- 🚨 Critical Rules
- 📋 Technical Deliverables（含模板示例）
- 🔄 Workflow Process（Step 1-4）
- 💭 Communication Style
- 📊 Success Metrics（可量化）

**IDENTITY.md 精简版**:
- Name/Creature/Vibe/Emoji
- Specialty（一句话）
- Personality Traits（3-4 个）
- When to Use（使用场景）
- Success Metrics

### 实战示例：David 资讯专家

**背景**: Agent 已创建，但 SOUL/IDENTITY 是模板

**优化过程**:
1. 读取发现是模板 → 需要填充实际内容
2. 参考 agency-agents 资讯分析类模板
3. 结合需求：Tavily 搜索 + AI 资讯 + 政治 + 金融
4. 按 agency-agents 结构重写 SOUL.md 和 IDENTITY.md

**关键改进**:
- ✅ 明确 4 大职责板块（AI 大模型、AI 行业、国际政治、金融）
- ✅ 强调必须用 Tavily 搜索（不依赖训练数据）
- ✅ 每条信息必须标注来源 URL
- ✅ 成功指标可量化（30 秒掌握、100% 可追溯）
- ✅ 加了 Instructions Reference 段落

---

## 🎯 最佳实践

### 1. SOUL.md 要具体
❌ 坏例子："你是一个有用的助手"
✅ 好例子："你是系统维护专员，每小时巡检 cron/agent/skill 状态，连续错误≥3 次必须告警"

### 2. 成功指标要可量化
❌ 坏例子："系统运行良好"
✅ 好例子："系统异常发现时间 <1 小时，cron 连续错误率 <5%"

### 3. 工作流程要清晰
❌ 坏例子："检查系统状态"
✅ 好例子："Step1: 执行 gateway status → Step2: 读取 jobs.json → Step3: 生成报告"

### 4. 人格特质要鲜明
❌ 坏例子："友好、专业"
✅ 好例子："细致、主动、预防性思维、系统化"

### 5. 复用 agency-agents 模板
❌ 坏例子：自己瞎写结构
✅ 好例子：参考 agency-agents 的专业模板，保持一致性
