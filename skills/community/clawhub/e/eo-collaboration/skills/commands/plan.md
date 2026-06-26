---
name: plan
source: eo-native
compatibility: full
description: 项目规划指令，调度 Planner 专家进行项目规划和任务分解
whenToUse: 当需要进行项目规划、任务分解、设置里程碑时使用
allowedTools: ["Read", "Write", "Edit", "Bash", "Glob"]
context: fork
expert: planner
aliases: ["/plan", "/规划", "/wbs"]
version: 1.0.1
---

# /plan - 项目规划指令

> **v1.0.1 新增**: 支持 `context: fork` 模式，可作为子代理并行执行

## 功能
调度 Planner 专家，进行项目规划和任务分解。

## 参数
```
/plan <任务描述> [options]

参数:
  <任务描述>      必填，项目或任务的文字描述
  --type <类型>   可选，项目类型 (web|miniprogram|algorithm|fullstack)
  --milestones   可选，是否生成里程碑 (true|false)
  --team-size    可选，团队规模 (数字)
```

## 执行流程（v1.0.1 Fork 模式）

```
用户输入 /plan "开发博客系统"
    │
    ▼
┌─────────────────────────────────────┐
│  registry.ts 解析 frontmatter        │
│  context: fork                      │
│  expert: planner                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  spawn-agent.ts → spawnExpertAgent  │
│  - agentType: planner               │
│  - isolation: worktree              │
│  - background: true                 │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────┴──────────┐
    │   Planner 子代理     │
    │  (独立工作目录)      │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Checkpoint 验证    │
    │  产出通过后返回结果  │
    └─────────────────────┘
```

## 输出格式

```markdown
# 📋 项目规划 - [项目名称]

## 🎯 项目概述
[任务描述]

## 📦 WBS 工作分解
### 模块1
- [ ] 任务1.1
- [ ] 任务1.2

### 模块2
- [ ] 任务2.1
- [ ] 任务2.2

## ⏱️ 里程碑
| 里程碑 | 预计完成 | 依赖 |
|--------|---------|------|
| M1: 架构设计 | Day 1-2 | - |
| M2: 核心功能 | Day 3-7 | M1 |
| M3: 集成测试 | Day 8-10 | M2 |

## 👥 建议团队配置
- 前端开发: X人
- 后端开发: X人
- 测试: X人

## 🔗 依赖关系
[依赖分析]
```

## 示例

```
用户: /plan "开发一个博客系统，包含文章发布、评论、用户管理"

我:
1. 解析 frontmatter → context=fork, expert=planner
2. 调用 spawnExpertAgent({ agentType: 'planner', isolation: 'worktree' })
3. Planner 子代理执行任务分解
4. Checkpoint 验证通过后输出完整项目计划
```

## 对应专家
- Planner (规划师)
- 关联 skill: `project-guidelines-example`, `blueprint`
