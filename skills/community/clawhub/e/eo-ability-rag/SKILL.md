---
name: eo-ability-rag
description: RAG知识共享能力，跨项目共享专家经验和最佳实践，基于语义搜索快速检索
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-rag

> RAG 知识共享能力 - 跨项目共享知识，避免重复造轮子

## 一句话介绍

基于RAG架构的知识共享能力，跨项目共享专家经验和最佳实践，语义搜索快速检索。

## 核心功能

- **知识索引**: 自动索引专家经验和最佳实践
- **语义搜索**: 自然语言查询相关知识
- **经验共享**: 跨项目共享成功经验
- **持续学习**: 从使用中自动更新知识库

## 使用方法

### 索引知识

```bash
# 自动索引（由 EO 自动触发）
索引: "Architect 专家在博客系统项目中的架构设计经验"
索引: "最佳实践：电商平台的缓存策略"

# 手动索引
/索引 "安全审计的 PCI-DSS 检查清单"
```

### 搜索知识

```bash
# 搜索相关知识
搜索: "博客系统的架构设计模式"
搜索: "学术论文的方法论设计"
搜索: "电商营销的内容策略"

# 基于专家搜索
搜索: "小红书策略师的种草内容经验"
```

### 共享知识

```bash
# 标记为可共享
共享: "本次项目中学到的架构设计经验"
来源: "博客系统项目"
专家: "Architect"
```

## 与EO插件的协同

- 被所有 eo-workflow-* 调用
- 使用 LanceDB（插件版）或简单索引（独立版）
- 被案例3（电商营销运营）使用

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | LanceDB向量索引、语义搜索、跨会话知识持久化 |
| **无插件（基础）** | 简单关键词索引、基础全文搜索 |

## 示例

```typescript
// 用户需要设计博客系统架构
const knowledge = await eo_ability_rag({
  action: 'search',
  query: '博客系统架构设计最佳实践'
})
// → 返回相关的架构模式、设计经验

// 使用知识辅助设计
const arch = await eo_ability_architect({
  task: '设计博客系统',
  useKnowledge: knowledge.results
})
```

## Interface

### Input

```typescript
interface RAGInput {
  action: 'index' | 'search' | 'share' | 'learn' | 'stats'
  content?: string           // 要索引的内容
  query?: string            // 搜索查询
  expert?: string           // 专家领域
  project?: string          // 项目名称
}
```

### Output

```typescript
interface RAGOutput {
  results: KnowledgeEntry[]
  relevance: number[]
  sources: string[]
  totalIndexed: number
}
```

---

*🦞⚙️ 钢铁龙虾军团*
