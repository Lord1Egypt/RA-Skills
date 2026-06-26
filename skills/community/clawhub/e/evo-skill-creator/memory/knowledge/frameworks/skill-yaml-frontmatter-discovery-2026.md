# SKILL.md YAML Frontmatter 与发现机制标准（2026）

> 来源：agentskills.io 标准 + skills.sh 生态 + Anthropic Claude Code 实践
> 学习时间：2026-04-01（深度学习）
> 类别：frameworks / skill-standard / discovery
> 波动性：medium（标准还在演进，但核心字段已稳定）
> 置信度：high（多平台采用的开放标准，已有生产实践）

## 核心概念

SKILL.md 的 YAML frontmatter 是 Agent Skill 生态的发现机制基础。采用"渐进式披露（Progressive Disclosure）"架构——启动时仅加载元数据，触发后才加载完整指令。

## Frontmatter 标准字段

```yaml
---
name: my-skill-name
description: >
  描述 skill 做什么以及什么时候使用。
  这是路由触发的主要机制，需包含触发短语。
  最大 1024 字符。
license: MIT
compatibility: Requires Python 3.10+, network access
metadata:
  version: "1.0.0"
  author: "creator-name"
  tags: ["agent-design", "self-evolving"]
---
```

### 字段规范

| 字段 | 必选 | 约束 |
|------|------|------|
| `name` | 是 | 1-64 字符，小写字母+数字+连字符，必须匹配父目录名 |
| `description` | 是 | 最大 1024 字符，描述功能+触发条件 |
| `license` | 否 | 许可证名称或引用 |
| `compatibility` | 否 | 最大 500 字符，环境要求 |
| `metadata` | 否 | 任意键值对（version/author/tags 等） |
| `allowed-tools` | 否 | 空格分隔的工具列表（实验性） |

### 关键设计决策

1. **无独立 triggers 字段**：触发逻辑完全依赖 `description` 的自然语言描述
   - 优点：灵活，Agent 可以语义理解
   - 缺点：不可预测性高，可能误触发或漏触发
   - **我们的实践**：在 description 中显式写明触发短语是最佳实践

2. **无独立 version 字段**：版本放在 `metadata.version`
   - 优点：元数据可扩展
   - 缺点：版本不是一等公民，工具支持不统一

3. **name 必须匹配目录名**：确保唯一性和文件系统友好

## 渐进式披露（Progressive Disclosure）

```
Level 1（启动时）：只加载 name + description
  → 作用：skill 路由决策（是否相关？）
  → 代价：几十个 token

Level 2（触发后）：加载完整 SKILL.md body
  → 作用：执行指令
  → 代价：几百到几千 token

Level 3（执行时）：按需加载 scripts/ references/ assets/
  → 作用：外部资源
  → 代价：按需，可控
```

**核心价值**：Token 成本最小化 + 上下文窗口利用率最大化。

## Skills.sh 生态

Skills.sh（Vercel 旗下）充当 Skill 的 npm-like 注册中心：
- **发现**：搜索社区创建的 skill
- **安装**：`npx skills add <package>`
- **分发**：支持跨平台（Claude Code、Cursor、Copilot CLI 等）

## 与我们的 evo-agent-model.md 对齐分析

### 当前差距

| 维度 | 标准要求 | 我们现状 | 差距 |
|------|---------|---------|------|
| Frontmatter | YAML frontmatter 必选 | 大部分子智能体无 frontmatter | **大差距** |
| name 字段 | 小写+连字符，匹配目录名 | 未规范 | 中差距 |
| description | 含触发短语，1024 字符内 | 触发逻辑散落在 settings.json | 中差距 |
| version | metadata.version | 在 agents-registry 中跟踪 | 小差距 |
| compatibility | 环境要求声明 | 未声明 | 中差距 |

### 建议行动

1. **立即**：为 evo-agent-model.md 的 SKILL.md 模板增加 frontmatter 章节
2. **短期**：为所有现有子智能体补充 frontmatter
3. **中期**：将 frontmatter 纳入创建规范检查清单
4. **长期**：评估 skills.sh 分发兼容性

### Frontmatter 模板（为自我进化智能体定制）

```yaml
---
name: agent-name
description: >
  角色一句话描述。触发条件列表。
  当用户提到"关键词1"、"关键词2"、"/agent-name"时触发。
license: MIT
compatibility: macOS/Linux, Claude Code CLI
metadata:
  version: "1.0.0"
  author: evo-skill-creator
  type: self-evolving-agent
  tags: ["domain-tag1", "domain-tag2"]
---
```

## 与已有知识的交叉

- **Anthropic Modular Skill Architecture**（#29）：官方支持 frontmatter 标准
- **AgentSkillOS**（#30）：能力树 + DAG 编排需要标准化的元数据
- **A2A Agent Card**（#14）：Agent Card 的简化版——frontmatter 是轻量级的能力声明
- **上下文工程**（#11）：frontmatter 是上下文工程中"最小必要上下文"的工程实践

## 核心抽象

> **YAML Frontmatter 的本质**：它是 Skill 的"名片"——用最少的 token 让 Agent 在启动时了解有哪些能力可用。这是上下文工程中"渐进式加载"原则的具体实现。

> **对我们的核心启示**：我们的 SKILL.md 应该从"只有指令"进化为"元数据（frontmatter）+ 指令（body）"的双层结构。这不仅提升了发现效率，也为未来的 skill 市场化分发打下基础。
