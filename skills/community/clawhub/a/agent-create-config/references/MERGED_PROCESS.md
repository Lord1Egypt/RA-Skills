# Agent 创建与配置融合流程文档

> 本文档整合了一人一公司 Agent 和通用 Agent 生成器的工作流程，为 CEO 提供完整的 Agent 创建操作指南。

---

## 阶段 1：收集需求

### 1.1 确认 Agent 类型

| Agent 类型 | 用途 | 配置文件路径 |
|-----------|------|-------------|
| `one-person-company` | 一人公司专用 Agent | `~/.openclaw/workspace/skills/one-person-company/` |
| `agentgener` | 通用 Agent 生成器 | `~/.openclaw/workspace/skills/agentgener/` |

### 1.2 收集信息清单

```
□ Agent 名称（name）
□ Agent 角色类型（type）
□ 核心功能描述
□ 使用的 LLM 模型
□ 需要的 Skills 列表
□ 飞书绑定需求（是/否）
□ 多账号需求（是/否）
```

---

## 阶段 2：创建工作区

### 2.1 标准工作区结构

```
~/.openclaw/workspace/
├── SOUL.md          # Agent 灵魂/人格定义
├── AGENTS.md        # 工作区说明
├── USER.md          # 用户信息
├── TOOLS.md         # 工具配置
├── IDENTITY.md      # Agent 身份定义
└── memory/          # 记忆目录
    └── YYYY-MM-DD.md
```

### 2.2 创建命令

```bash
# 创建工作区目录
mkdir -p ~/.openclaw/workspace-coder

# 创建基础配置文件
touch ~/.openclaw/workspace-coder/SOUL.md
touch ~/.openclaw/workspace-coder/AGENTS.md
touch ~/.openclaw/workspace-coder/USER.md
touch ~/.openclaw/workspace-coder/TOOLS.md
touch ~/.openclaw/workspace-coder/IDENTITY.md
mkdir -p ~/.openclaw/workspace-coder/memory
```

---

## 阶段 3：生成配置文件

### 3.1 SOUL.md 模板

```markdown
# SOUL.md - Agent 灵魂定义

## 核心身份

你是公司 CEO（薛总）的**编程专家员工**，专长是代码实现和技术方案。

## 工作职责

- 接收 CEO 分配的任务，高效执行
- 主动汇报进度，没结果也要说明在做什么
- 任务完成后**从 MEMORY.md 中提取本次学到的偏好/方法，更新到长期记忆**

## 沟通原则

- 用【员工汇报】格式回复
- 状态格式：`✅ 完成 | 🔄 进行中 | ⏳ 待确认`
- 轮次标注：`X/5`
- 说话简洁，不绕弯子

## CEO 偏好（从长期记忆读取）

（详见 MEMORY.md，每次任务开始前先读）
```

### 3.2 AGENTS.md 模板

```markdown
# AGENTS.md - 工作区说明

## 首次运行

如果 `BOOTSTRAP.md` 存在，这是你的出生证明。按照它执行，搞清楚你是谁，然后删除它。

## 会话启动

在做任何事情之前：

1. 读取 `SOUL.md` — 这是你是谁
2. 读取 `USER.md` — 这是你在帮助谁
3. 读取 `memory/YYYY-MM-DD.md`（今天 + 昨天）获取最近上下文
4. **如果是主会话**：也要读取 `MEMORY.md`

不要问许可，直接做。

## 记忆

你每次会话都是全新的。以下文件是你的连续性：

- **每日笔记：** `memory/YYYY-MM-DD.md` — 每日工作日志
- **长期记忆：** `MEMORY.md` — 重要记忆

## 写下来

- **记忆是有限的** — 如果你想记住什么，写到文件里
- 文件是可靠的
- 学到新东西 → 更新 MEMORY.md
```

### 3.3 USER.md 模板

```markdown
# USER.md - 用户信息

- **Name:** 薛总
- **称呼:** 哥哥
- **Pronouns:** 他
- **Timezone:** Asia/Shanghai
- **Notes:** 35岁程序员，技术专家，喜欢研究新技术，对 AI Agents 感兴趣
```

### 3.4 IDENTITY.md 模板

```markdown
# IDENTITY.md - 我是谁

- **名字：** 大叔
- **类型：** OpenClaw Agent（编程专家）
- **Emoji：** 👨‍💻
- **称呼：** 大叔
- **年龄/风格：** 35岁资深程序员
- **风格：** 严谨、专业、有原则、可信赖
```

### 3.5 TOOLS.md 模板

```markdown
# TOOLS.md - 工具配置

## 已安装技能

- github - GitHub 操作（issues, PR 等）
- gh-issues - GitHub Issues 管理
- Code review 相关能力

## 常用工具

- Git - 代码版本控制
- 代码分析 - 代码审查和优化建议
- 问题诊断 - Bug 定位和修复建议

## 注意事项

- coder Agent 专注于编程任务
- 不知道就说不知道
- 三思而后行
```

---

## 阶段 4：注册 Agent

### 4.1 Agent 注册配置

注册新的 OpenClaw Agent，需要在 `~/.openclaw/agents/` 目录下创建配置文件：

```bash
# 创建 Agent 配置目录
mkdir -p ~/.openclaw/agents/coder

# 创建 Agent 配置文件
cat > ~/.openclaw/agents/coder/config.yaml << 'EOF'
name: coder
type: agent
description: 编程专家 Agent
workspace: /Users/mac/.openclaw/workspace-coder
runtime: local
model: minimax-cn/MiniMax-M2.7
skills:
  - github
  - gh-issues
  - coding-agent
channels:
  - feishu
EOF
```

### 4.2 Agent 配置文件说明

| 配置项 | 说明 | 示例值 |
|-------|------|-------|
| `name` | Agent 名称 | `coder` |
| `type` | Agent 类型 | `agent` |
| `description` | Agent 描述 | `编程专家 Agent` |
| `workspace` | 工作区路径 | `/Users/mac/.openclaw/workspace-coder` |
| `runtime` | 运行时环境 | `local` |
| `model` | 默认使用模型 | `minimax-cn/MiniMax-M2.7` |
| `skills` | 启用的技能列表 | `["github", "gh-issues"]` |
| `channels` | 通信渠道 | `["feishu"]` |

---

## 阶段 5：绑定飞书/多账号

### 5.1 飞书绑定配置

```bash
# 配置飞书渠道
openclaw config set channel.feishu.enabled true
openclaw config set channel.feishu.bot_token <飞书_BOT_TOKEN>
openclaw config set channel.feishu.app_id <飞书_APP_ID>
openclaw config set channel.feishu.app_secret <飞书_APP_SECRET>
```

### 5.2 多账号配置

```bash
# 为不同 Agent 配置不同账号
openclaw config set agents.coder.account_id <账号1>
openclaw config set agents.other.account_id <账号2>
```

### 5.3 飞书多账号绑定矩阵

| Agent 名称 | 飞书 App | 账号类型 | 权限级别 |
|-----------|---------|---------|---------|
| `coder` | 主应用 | 主账号 | 管理员 |
| `agent_xxx` | 从应用 | 子账号 | 普通成员 |

---

## 阶段 6：重启生效

### 6.1 重启 Gateway 服务

```bash
# 查看 Gateway 状态
openclaw gateway status

# 重启 Gateway
openclaw gateway restart

# 验证重启成功
openclaw gateway status
```

### 6.2 验证 Agent 正常运行

```bash
# 测试 Agent 连接
openclaw agent ping coder

# 查看 Agent 日志
openclaw agent logs coder --tail 50
```

### 6.3 常见问题排查

| 问题 | 解决方案 |
|-----|---------|
| Agent 无法连接 | 检查 Gateway 状态，重启服务 |
| 飞书消息无响应 | 检查 BOT Token 和 App Secret |
| 配置文件加载失败 | 检查 YAML 语法和文件权限 |

---

## 阶段 7：交付确认

### 7.1 交付检查清单

```
□ Agent 已成功注册
□ 配置文件已正确生成
□ 飞书绑定已完成
□ Gateway 重启成功
□ Agent 可正常响应消息
□ 所有 Skills 已正确加载
□ 交付文档已生成
```

### 7.2 交付文档模板

```markdown
# Agent 创建交付报告

## 基本信息

- **Agent 名称：** coder
- **创建时间：** YYYY-MM-DD HH:mm
- **工作区路径：** /Users/mac/.openclaw/workspace-coder
- **使用的模型：** minimax-cn/MiniMax-M2.7

## 配置状态

| 配置项 | 状态 |
|-------|------|
| 工作区创建 | ✅ 完成 |
| 配置文件生成 | ✅ 完成 |
| Agent 注册 | ✅ 完成 |
| 飞书绑定 | ✅ 完成 |
| Gateway 重启 | ✅ 完成 |

## 使用说明

1. 启动 Gateway：`openclaw gateway start`
2. 查看 Agent 状态：`openclaw agent status`
3. 测试发送消息到飞书群

## 后续维护

- 配置文件位置：`~/.openclaw/agents/coder/config.yaml`
- 日志位置：`~/.openclaw/logs/`
- 记忆文件：`~/.openclaw/workspace-coder/memory/`
```

---

## 附录 A：配置文件行数限制

| 配置文件 | 最大行数 | 建议行数 | 备注 |
|---------|---------|---------|-----|
| SOUL.md | 500 | 50-100 | 保持简洁 |
| AGENTS.md | 300 | 50-80 | 核心指令 |
| USER.md | 100 | 20-30 | 基本信息 |
| IDENTITY.md | 100 | 20-30 | 身份定义 |
| TOOLS.md | 200 | 30-50 | 工具列表 |
| config.yaml | 无限制 | 50-100 | 保持精简 |

---

## 附录 B：Agent 类型差异对比

| 特性 | one-person-company | agentgener |
|-----|-------------------|------------|
| **定位** | 一人公司专用 | 通用 Agent 生成 |
| **技能** | 飞书、提醒、订单等 | 依赖生成配置 |
| **配置复杂度** | 中等 | 高 |
| **适用场景** | 日常运营管理 | 多场景定制 |
| **SKILL.md 位置** | `skills/one-person-company/` | `skills/agentgener/` |

---

## 附录 C：支持的大模型参考表

| 模型 ID | 提供商 | 上下文长度 | 适用场景 |
|--------|-------|-----------|---------|
| `minimax-cn/MiniMax-M2.7` | MiniMax | 32K | 默认首选 |
| `claude-3-5-sonnet-20241022` | Anthropic | 200K | 复杂推理 |
| `gpt-4o` | OpenAI | 128K | 通用对话 |
| `deepseek-chat` | DeepSeek | 64K | 中文优化 |

---

## 附录 D：Skills 技能清单

| 技能名称 | 功能描述 | 触发关键词 |
|---------|---------|----------|
| `github` | GitHub 操作 | issues, PR, CI |
| `gh-issues` | Issues 管理 | /gh-issues |
| `coding-agent` | 代码任务委托 | 编程任务 |
| `feishu-doc` | 飞书文档操作 | 飞书文档 |
| `feishu-wiki` | 飞书知识库 | 知识库, wiki |
| `weather` | 天气查询 | 天气 |
| `apple-reminders` | 苹果提醒 | 提醒, 日程 |

---

## 附录 E：目录结构参考

```
~/.openclaw/
├── agents/                    # Agent 配置目录
│   └── coder/
│       └── config.yaml        # Agent 配置文件
├── workspace-coder/          # Agent 工作区
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── USER.md
│   ├── TOOLS.md
│   ├── IDENTITY.md
│   └── memory/
│       └── YYYY-MM-DD.md
├── skills/                   # 技能目录
│   ├── one-person-company/
│   │   └── SKILL.md
│   └── agentgener/
│       └── SKILL.md
└── logs/                     # 日志目录
    └── gateway.log
```

---

> 📌 **最后更新：** 2026-03-21  
> **版本：** v2.0  
> **维护者：** coder Agent（大叔）
