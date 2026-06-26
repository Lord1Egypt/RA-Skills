---
name: eo-ability-architect
description: 架构设计能力，调用Architect专家设计系统架构、技术选型、风险评估
metadata:
  openclaw:
    requires: { bins: [] }
    install: []
---

# eo-ability-architect

> 架构设计能力 - 调用 Architect 专家设计系统架构、技术选型、风险评估

## 一句话介绍

调用Architect专家设计系统架构，输出架构图、技术栈、模块划分、风险评估。

## 核心功能

- **系统架构设计**: 整体架构图、模块划分、组件关系
- **技术选型**: 前端/后端/数据库/缓存等技术栈推荐
- **风险评估**: 技术风险识别、缓解方案
- **复杂度评估**: 系统规模评估、性能预估

## 使用方法

```bash
# 标准用法
/architect "设计日活10万电商平台 --scale large"

/architect "博客系统架构设计"
```

## 与EO插件的协同

- 被 eo-workflow-blog 调用
- 被 eo-workflow-miniprogram 调用
- 被 eo-workflow-security-audit 调用（威胁建模）

## 独立运行模式（有EO vs 无EO）

| 模式 | 能力 |
|------|------|
| **有EO插件** | 141专家库（18位Architect专家）、真实架构模式、风险预测 |
| **无插件（基础）** | LLM生成架构建议、通用设计模式 |

## 示例

```
🏗️ 架构设计报告

## 系统架构
┌─────────────────────────────────────┐
│            Load Balancer             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────┼───────────────────┐
│                 │                    │
│  ┌──────────┐  │  ┌──────────┐       │
│  │  API GW  │  │  │   CDN    │       │
│  └────┬─────┘  │  └──────────┘       │
│       │                               │
│  ┌────┴─────┐                         │
│  │  Backend │                         │
│  └────┬─────┘                         │
│       │                               │
│  ┌────┴─────┐                         │
│  │ Database │                         │
│  └──────────┘                         │
└─────────────────────────────────────┘

## 技术栈
- 前端: React + TypeScript
- 后端: Node.js + Express
- 数据库: PostgreSQL
- 缓存: Redis
```

## Interface

### Input

```typescript
interface ArchitectInput {
  task: string                    // 任务描述
  scale?: 'small' | 'medium' | 'large'  // 系统规模
  constraints?: string[]          // 约束条件
  existingArchitecture?: string   // 现有架构（如果是扩展）
}
```

### Output

```typescript
interface ArchitectOutput {
  architecture: ArchitectureDiagram  // 架构图
  techStack: TechStack               // 技术栈
  modules: Module[]                  // 模块划分
  risks: Risk[]                       // 风险评估
  estimatedComplexity: string        // 复杂度评估
}
```

---

*🦞⚙️ 钢铁龙虾军团*
