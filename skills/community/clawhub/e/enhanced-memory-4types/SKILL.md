---
name: memory-system
description: 完整记忆系统 - 文件系统记忆 + 向量搜索 + 自动加载 + Memory Flush + 四类记忆分类
---

# Memory System 🧠

> 完整的记忆系统 - 文件系统记忆 + 向量搜索 + 自动加载 + 四类记忆分类 + Feedback 双向记录

## 特性

- 📁 **文件系统存储** - 基于 Markdown 文件，无数据库依赖，可读、可手动编辑、易备份
- 🔍 **支持搜索** - 支持语义搜索（需配置 Ollama）；未配置时自动降级为关键词匹配
- ⚡ **自动加载** - 会话启动时自动加载相关记忆，无需手动触发
- 🏠 **群组隔离** - 支持多群组独立记忆，群组之间数据互不干扰
- 💾 **Memory Flush** - 上下文接近阈值时自动持久化，防止信息丢失
- 📝 **四类记忆分类** - user / feedback / project / reference，规范存储结构
- 🔄 **Feedback 双向记录** - 同时记录纠正（负面）和确认（正面），形成完整反馈闭环

---

## 安装

```bash
clawhub install memory-system
```

---

## 核心概念：四类记忆

记忆分为四种类型，每种类型有明确的用途和保存时机：

### 1. User（用户）记忆
**作用域**：private（私密）
**内容**：关于用户本人的信息 - 角色、目标、偏好、知识背景
**保存时机**：了解用户任何细节时

```
## user/张三.md
- 用户是数据科学家，专注于可观测性/日志系统
- 用户有10年Go经验，但React是新手
```

### 2. Feedback（反馈）记忆 ⭐
**作用域**：private / team
**内容**：用户给的指导 - 既要记录纠正，也要记录确认
**保存时机**：用户纠正你 OR 确认你的做法时

```
## feedback/开发规范.md
### 集成测试必须用真实数据库
**Why:** 上一季度因为mock测试通过了但生产迁移失败
**How to apply:** 所有集成测试禁止mock数据库层

### 接受单PR而非多个小PR
**Type:** positive（确认）
**Why:** 拆分反而造成不必要的开销
**How to apply:** 重构类需求优先合并为大PR
```

### 3. Project（项目）记忆
**作用域**：team（团队）
**内容**：项目进展、目标、bug、决策
**保存时机**：了解"谁在做什么、为什么、截止时间"时

```
## project/auth重构.md
- auth中间件重写是由法务合规需求驱动，非技术债务
- 截止日期：2026-03-15
- 负责人：@张三
```

### 4. Reference（引用）记忆
**作用域**：team（团队）
**内容**：外部系统资源和指针
**保存时机**：了解外部系统入口和用途时

```
## reference/外部资源.md
- Bug追踪：Linear项目"INGEST"，所有pipeline bug在此跟踪
- 监控面板：grafana.internal/d/api-latency 是oncall使用的延迟看板
```

---

## Feedback 双向记录

Claude Code 的一个关键洞察：**Feedback 不仅要记录"不要做什么"，也要记录"什么做对了"**。

### 为什么需要双向？

| 类型 | 触发条件 | 示例 |
|------|---------|------|
| **negative** | 用户纠正你 | "不要mock数据库" |
| **positive** | 用户确认你 | "perfect，exactly" |

如果只记录纠正，你会避免错误但可能变得过于保守，忘记用户认可的做法。

### 保存格式

```markdown
### [规则名称]
**Type:** negative | positive
**Why:** [用户给出的原因]
**How to apply:** [何时何地应用这条规则]
**Date:** YYYY-MM-DD
```

### 如何识别 positive feedback？

留意这些信号：
- "完美"、"正是如此"、"继续保持"
- 接受了一个非显而易见的做法
- 没有纠正而是直接说"对"
- 在你选择后说"没错"

---

## 配置

在 `openclaw.json` 中配置：

```json
{
  "skills": {
    "memory-system": {
      "memoryDir": "~/.openclaw/workspace/memory",
      "flushMode": "safeguard",
      "softThresholdTokens": 300000,
      "vectorEnabled": true,
      "embeddingModel": "nomic-embed-text"
    }
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `memoryDir` | string | `~/.openclaw/workspace/memory` | 记忆文件存储目录 |
| `flushMode` | string | `safeguard` | Flush 触发模式 |
| `softThresholdTokens` | number | `300000` | 触发自动 Flush 的 token 软阈值 |
| `vectorEnabled` | boolean | `false` | 是否启用语义搜索 |
| `embeddingModel` | string | `nomic-embed-text` | Ollama 使用的嵌入模型 |

### flushMode 说明

| 值 | 行为 |
|----|------|
| `safeguard` | 上下文 token 超过阈值时自动持久化（推荐） |
| `manual` | 仅在显式调用 `memory_flush` 时触发 |
| `disabled` | 禁用 Flush |

---

## 工具

### memory_search

语义搜索记忆文件。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词或自然语言描述 |
| `type` | string | ❌ | 限定记忆类型（user/feedback/project/reference） |
| `group` | string | ❌ | 限定搜索的群组 |
| `topK` | number | ❌ | 返回结果数量，默认 `5` |

### memory_write

写入或追加内容到记忆文件。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | ✅ | 目标文件路径（相对于 `memoryDir`） |
| `content` | string | ✅ | 写入的 Markdown 内容 |
| `type` | string | ❌ | 记忆类型（auto-detect 或指定） |
| `mode` | string | ❌ | `overwrite`（覆盖）或 `append`（追加） |

### memory_flush

手动触发记忆持久化。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `group` | string | ❌ | 仅持久化指定群组 |

---

## 记忆目录结构

建议的目录结构：

```
memory/
├── MEMORY.md                    # 索引文件（所有记忆的入口）
├── user/                        # 用户记忆
│   └── [user-id].md
├── feedback/                    # 反馈记忆
│   ├── positive/               # 正面确认
│   └── negative/               # 纠正指导
├── project/                    # 项目记忆
│   └── [project-name].md
└── reference/                   # 引用记忆
    └── external-resources.md
```

### MEMORY.md 索引格式

```markdown
# Memory Index

## User
- [用户角色偏好](user/role.md) — 记录用户专业背景和沟通偏好

## Feedback
- [开发规范](feedback/dev-rules.md) — 集成测试、PR合并等规范
- [沟通风格](feedback/comm-style.md) — 回复长度、格式偏好

## Project
- [Auth重构进度](project/auth-refactor.md) — 当前项目状态

## Reference
- [外部系统](reference/external.md) — Linear、Grafana等入口
```

---

## 最佳实践

### 何时保存记忆？

**User**：了解用户任何个人细节时
- "我是数据科学家"
- "我有10年Go经验但React是新手"

**Feedback Negative**：用户纠正你时
- "不要那样做"
- "停止使用X方法"

**Feedback Positive**：用户确认你的非显而易见做法时
- "perfect keep doing that"
- 接受一个不常规的选择

**Project**：了解项目进展时
- "我们在做X项目"
- "截止日期是周四"

**Reference**：了解外部资源时
- "bug在Linear的INGEST项目跟踪"
- "Grafana面板在XXX"

### 如何写好记忆？

1. **使用绝对日期** - "上周" → "2026-03-25"
2. **包含 Why** - 记录原因比记录规则更有价值
3. **保持简洁** - 索引每条 <= 150 字符
4. **避免重复** - 更新已有记忆而非创建新的

---

## 搜索配置（可选）

语义搜索依赖本地 [Ollama](https://ollama.com)：

```bash
ollama pull nomic-embed-text
```

---

**作者**：团宝 (openclaw)  
**版本**：1.1.0  
**更新**：引入四类记忆分类 + Feedback 双向记录
