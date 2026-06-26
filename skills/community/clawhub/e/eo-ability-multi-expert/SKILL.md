---
name: eo-ability-multi-expert
description: 多专家编排能力(Multi-Expert Orchestrator)，协调多个专家并行/串行工作，结果自动汇流
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-multi-expert

> 多专家编排能力 (Multi-Expert Orchestrator) - 协调多个专家并行/串行工作

## 一句话介绍

EO核心编排能力，多专家并行启动、结果自动汇流、依赖管理、冲突解决。

## 核心功能

- **多专家并行**: 多个专家同时启动
- **结果汇流**: 专家输出自动合并
- **依赖管理**: 专家执行顺序控制
- **冲突解决**: 多专家结果冲突处理
- **Checkpoint**: 每N个专家后自动Checkpoint

## 使用方法

```bash
# 启动多专家协作
/dream "开发博客系统"

// 或通过 Team Manager
创建团队: 博客开发团队
添加专家: Architect, Backend, Frontend, QA
启动协作: parallel
```

## 与EO插件的协同

- 被所有 eo-workflow-* 调用
- 是 EO 的核心差异化能力

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 真实多Agent并行、sessions API调用、结果汇流 |
| **无插件（基础）** | LLM模拟多专家、串行执行 |

## 执行流程

```
用户: /dream "开发博客系统"
           │
           ▼
┌─────────────────────────────────────┐
│  Multi-Expert Orchestrator           │
│  解析任务 → 分解 → 调度             │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐
│Architect│  │Backend │  │Frontend│
│  Agent  │  │  Agent │  │  Agent │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  ▼
         ┌──────────────┐
         │  Result Merge │
         │  + Checkpoint │
         └──────────────┘
```

## Interface

### Input

```typescript
interface MultiExpertInput {
  experts: ExpertRequest[]
  strategy: 'parallel' | 'sequential' | 'pipeline'
  checkpointAfter?: number      // 每 N 个专家后 Checkpoint
  timeout?: number              // 超时时间（ms）
}
```

### Output

```typescript
interface MultiExpertOutput {
  results: ExpertResult[]
  checkpoints: CheckpointResult[]
  summary: string
  duration: number
}
```

---

*🦞⚙️ 钢铁龙虾军团*
