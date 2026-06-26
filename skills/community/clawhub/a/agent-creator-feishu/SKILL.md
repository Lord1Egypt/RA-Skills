---
name: agent-creator
description: 创建新的 OpenClaw Agent 并绑定到飞书群聊。当用户说"创建新 agent"、"新建 agent"、"创建一个机器人"、"新建机器人"、"添加 agent 到群聊"、"帮我搭建一个 agent"、"我想做一个新的 agent" 时使用此技能。也适用于"绑定飞书群聊"、"配置 agent 权限"等场景。
---

# agent-creator Skill

引导创建新 Agent 并绑定到飞书群聊。

## 执行流程

### 1️⃣ 需求收集

用 5W2H 方法论搞清需求。读取模板发给用户：
```
references/AGENT-CARD-TEMPLATE.md
```

**交互式（推荐）**：先问 Why/What，再问 Who/Where，然后 When/How，最后确认。也可直接让用户填模板。

**必须收集**：名称、目标、群组 ID、人设风格、核心能力、红线边界、权限规则。

### 2️⃣ 确认 Agent Card（⚠️ 必须等用户确认）

整理成 Agent Card 发给用户确认，包含：
- 📌 基本信息：名称、目标、绑定群组
- 🎭 人设风格：是谁、什么性格、怎么说话
- ✅ 核心能力：能做什么
- ❌ 红线边界：不能做什么
- 🔐 权限规则：管理员 vs 普通用户

**不要跳过这一步直接生成配置。**

### 3️⃣ 生成配置文件

| 文件 | 放什么 |
|------|--------|
| **IDENTITY.md** | 名片：名称、定位、emoji |
| **SOUL.md** | 灵魂：人设、语气、风格、边界（短而有力） |
| **AGENTS.md** | 规则：系统信息、权限控制 |
| **SKILL.md** | 指令：具体能/不能做什么 |
| **config.json** | 配置：模型、thinking 等（可选） |

详细模板和写法参考：
```
references/AGENT-CREATION-GUIDE.md
```

### 4️⃣ 创建并绑定

> **管理员 ID**：从当前消息的 `sender_id` 获取，填入 AGENTS.md 的权限控制部分。

```bash
# 1. 创建工作区
openclaw agents add <name> --workspace ~/.openclaw/workspace-<name>

# 2. 写入配置文件（IDENTITY.md / SOUL.md / AGENTS.md / SKILL.md / config.json）

# 3. 确保群组在白名单（参考 GUIDE.md 中的白名单配置）

# 4. 绑定到群聊
openclaw agents bind --agent <name> --bind "feishu:<群组ID>"
```

⚠️ **绑定必须使用 `peer` 对象**（参考 GUIDE.md 中的正确/错误示例）。

配置热加载，无需重启 gateway。

### 5️⃣ 测试 & 记录

在群聊测试，确认行为符合预期。完成后更新 `~/.openclaw/workspace/MEMORY.md`。

## 参考文件

- 需求模板：`references/AGENT-CARD-TEMPLATE.md`
- 操作指南：`references/AGENT-CREATION-GUIDE.md`
- 示例 Agent：`~/.openclaw/workspace-daily-ai-news/`
