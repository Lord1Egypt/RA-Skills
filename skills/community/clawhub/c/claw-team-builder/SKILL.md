---
name: claw-team-builder
description: |
  Agent Team 规划与配置工具。通过多轮交互澄清需求，自动创建 Agent 配置、工作空间、Bootstrap 文件。

  触发场景：
  - 用户说"创建新 Agent" / "新建 bot" / "配置多个 bot"
  - 用户说"规划 agent team" / "我需要几个不同的 agent"
  - 用户说"添加一个 agent" / "帮我建一个新 agent"
  - 用户提到需要不同场景使用不同的 AI 角色

  功能：
  1. 需求澄清 - 引导用户描述使用场景和 Agent 定位
  2. 配置读取 - 自动读取现有 openclaw.json，分析已有配置
  3. 方案设计 - 推荐 Agent 配置方案，检测冲突
  4. 自动创建 - 创建目录、文件、更新配置
  5. 配置验证 - 确保配置正确可用
---

# Claw Team Builder

## 目的

帮助用户通过引导式对话规划并创建 Agent Team，降低多 Agent 配置的复杂度。

## 工作流程

### Phase 1: 需求澄清

通过多轮交互收集信息：

**必须收集的信息：**
1. Agent ID（或根据名称自动生成）
2. Agent 名称/昵称
3. Agent 定位/用途
4. Agent 性格风格

**可选信息（有默认值）：**
- 模型选择（默认继承 agents.defaults.model.primary）
- Channel 类型（默认 feishu）
- Channel 账户信息（如已有则复用）

### Phase 2: 配置读取与分析

**必须执行：**
```
读取 ~/.openclaw/openclaw.json，分析：
- agents.defaults: 默认模型、工作空间设置
- agents.list: 现有 Agent ID 列表（检测冲突）
- channels: 现有 Channel 账户配置
- bindings: 现有路由规则
- models.providers: 可用模型列表
```

**冲突检测：**
- Agent ID 是否重复
- 工作空间路径是否冲突
- Channel 账户是否已被占用

### Phase 3: 方案设计

基于收集信息 + 现有配置，生成：
1. Agent 配置片段
2. Channel 配置片段（如需要）
3. Binding 配置片段

展示配置预览，让用户确认或调整。

### Phase 4: 执行创建

1. 备份 openclaw.json
2. 创建目录结构
3. 生成 Bootstrap 文件 (IDENTITY.md, SOUL.md, USER.md)
4. 更新 openclaw.json
5. 运行 openclaw doctor --fix 验证

### Phase 5: 结果反馈

展示创建结果，提供后续操作建议。

## 可用工具

- `{baseDir}/scripts/create-agent.js` - Agent 创建脚本
- `{baseDir}/lib/config-builder.js` - 配置构建工具
- `{baseDir}/lib/validator.js` - 配置验证工具

## 模板文件

位于 `{baseDir}/templates/`:
- `IDENTITY.md.tmpl` - Agent 身份模板
- `SOUL.md.tmpl` - Agent 灵魂模板
- `USER.md.tmpl` - 用户信息模板

## 示例对话

```
用户: 我想创建一个新的 agent，专门处理工作任务

Agent: 好的，让我帮你规划。

首先让我读取一下现有配置... ✓

📍 **需求澄清**

这个 Agent 的主要用途是？
- 任务管理？
- 日程提醒？
- 文档处理？
- 其他？

用户: 任务管理和日程提醒

Agent: 明白了。给它起个名字？

用户: 启明

Agent: "启明"，很好！

它应该有什么样的性格？
1. 高效严肃型 - 专注执行
2. 亲切温和型 - 细致耐心
3. 其他风格

用户: 高效严肃型

Agent: 收到。让我看看你的 Channel 配置...

你现在有 2 个飞书账户：
- luna-bot (已绑定 main agent)
- qiming-bot (未使用)

要用现有的 qiming-bot 账户，还是配置新的？

用户: 用现有的 qiming-bot

Agent: 完美！配置方案如下：

📋 **配置预览**

| 项目 | 值 |
|------|-----|
| Agent ID | qiming |
| 名称 | 启明 |
| 工作空间 | ~/.openclaw/workspace-qiming |
| 模型 | bailian/MiniMax-M2.5 |
| Channel | feishu / qiming-bot |

确认创建？(确认/调整)
```

## 注意事项

1. **安全第一**：修改配置前必须备份
2. **幂等性**：支持重复执行，不破坏已有配置
3. **最小侵入**：只添加新配置，不修改已有配置
4. **用户友好**：尽量从现有配置推断，减少用户输入