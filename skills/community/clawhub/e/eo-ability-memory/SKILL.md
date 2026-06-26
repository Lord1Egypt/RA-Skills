---
name: eo-ability-memory
description: 主动记忆能力(Proactive Memory)，跨会话延续用户偏好、项目上下文，记住导师要求和格式规范
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-memory

> 主动记忆能力 (Proactive Memory) - 记住用户偏好、项目上下文，跨会话延续

## 一句话介绍

跨会话主动记忆能力，记住用户偏好、导师要求、项目上下文，下次对话自动恢复。

## 核心功能

- **自动记忆**: 关键决策自动保存
- **跨会话恢复**: 下次对话自动加载相关记忆
- **偏好学习**: 根据用户反馈优化策略
- **遗忘机制**: 自动清理过期记忆

## 使用方法

### 保存记忆

```bash
# 自动保存（由 EO 自动触发）
保存: "导师偏好：方法论章节需要更详细的数学推导"
保存: "格式要求：双栏IEEE模板"
保存: "上次讨论焦点：价格谈判"
```

### 加载记忆

```bash
# 加载用户偏好
加载记忆: "用户偏好"

// 自动恢复
用户: "继续上次的研究"
→ 自动加载:
→   - "目标期刊Medical Image Analysis"
→   - "IEEE格式要求"
→   - "上次模型已经跑出初步结果"
```

### 搜索记忆

```bash
# 搜索相关记忆
搜索记忆: "关于价格的所有记忆"
搜索记忆: "导师的偏好"
```

## 与EO插件的协同

- 被所有 eo-workflow-* 调用
- 被案例2（学术论文研究）使用
- 被案例4（秘书行政工作）重点使用

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 跨会话持久化、LanceDB索引、语义搜索 |
| **无插件（基础）** | 当前会话记忆、无持久化 |

## 示例

```typescript
// 案例：学术论文
用户: "继续上次的研究，模型已经跑出初步结果"

// EO 自动执行：
const memory = await eo_ability_memory({
  action: 'load',
  context: '当前项目'
})
// → 加载: "用户偏好IEEE格式" + "目标期刊Medical Image Analysis"

// 完成论文撰写后
await eo_ability_memory({
  action: 'save',
  key: '论文进度',
  value: { phase: 'methodology', done: true }
})
```

## Interface

### Input

```typescript
interface MemoryInput {
  action: 'save' | 'load' | 'search' | 'forget' | 'update'
  key?: string
  value?: any
  context?: string
  tags?: string[]
}
```

### Output

```typescript
interface MemoryOutput {
  success: boolean
  data?: any
  related?: MemoryEntry[]
  memoryUsed?: number
}
```

---

*🦞⚙️ 钢铁龙虾军团*
