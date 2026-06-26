---
name: eo-ability-plan
description: 项目规划能力，调用Planner专家生成WBS任务分解、里程碑计划、团队组成
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-plan

> 项目规划能力 - 调用 Planner 专家生成 WBS、里程碑、团队组成

## 一句话介绍

调用Planner专家进行项目规划，自动生成WBS任务分解、里程碑、团队组成，是多专家协作的起点。

## 核心功能

- **WBS任务分解**: 将复杂任务分解为可执行的小任务
- **里程碑计划**: 设定关键时间节点和交付物
- **团队组成**: 根据任务类型推荐专家组合
- **时间估算**: 估算项目总工期和阶段工期

## 使用方法

```bash
# 标准用法
/plan "开发博客系统 --type web --milestones true"

/plan "学术论文撰写流水线"

// 使用参数
使用 eo-ability-plan 规划一个[项目类型]项目
```

## 与EO插件的协同

- 被所有 eo-workflow-* 调用（是工作流的起点）
- 输出结果自动传递给 eo-ability-architect 进行架构设计

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 141专家库（27位Planner专家）、真实项目经验、WBS优化 |
| **无插件（基础）** | LLM生成WBS、通用任务分解模板 |

## 示例

```
📋 项目规划报告

## WBS 任务分解
1. 需求分析
   1.1 用户调研
   1.2 竞品分析
   1.3 需求文档
2. 架构设计
   2.1 技术选型
   2.2 系统架构
   2.3 数据库设计
3. 开发实施
   ...
```

## Interface

### Input

```typescript
interface PlanInput {
  task: string              // 任务描述
  type?: 'web' | 'mobile' | 'paper' | 'marketing' | 'security'
  milestones?: boolean      // 是否生成里程碑
  teamComposition?: boolean // 是否生成团队组成
  estimatedTime?: boolean   // 是否估算时间
}
```

### Output

```typescript
interface PlanOutput {
  wbs: TaskNode[]           // WBS 任务分解
  milestones: Milestone[]    // 里程碑列表
  teamComposition: Expert[] // 团队组成
  estimatedTime: string     // 预计时间
}
```

---

*🦞⚙️ 钢铁龙虾军团*
