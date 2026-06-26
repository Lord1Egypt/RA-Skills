---
name: agent-team-creator
version: 1.0.0
homepage: https://github.com/ryan-wuxl/agent-team-creator
description: Agent团队创建和管理工具 - 用于创建多Agent协作团队，分配角色和任务，协调复杂工作流。支持创建CEO、分析师、研究员等角色，实现智能任务分发和结果整合。
metadata:
  openclaw:
    emoji: 👥
    requires:
      bins: ["node"]
    tags: ["team", "agent", "orchestration", "multi-agent", "workflow"]
---

# Agent团队创建器

创建和管理多Agent协作团队，让复杂任务由多个专业Agent共同完成。

## 功能特点

- 👥 **多角色团队** - 创建CEO、分析师、研究员等专业角色
- 🎯 **任务分发** - 智能将任务分配给最适合的Agent
- 🔄 **结果整合** - 自动汇总多个Agent的分析结果
- 📊 **工作流管理** - 支持串行、并行、条件分支等复杂工作流
- 🎮 **实时协调** - CEO Agent实时协调团队成员

## 使用场景

- **投资分析团队**: CEO + 市场观察员 + 投资分析师 + 风控官
- **内容创作团队**: 主编 + 研究员 + 撰稿人 + 编辑
- **代码审查团队**: 技术负责人 + 安全专家 + 性能优化师

## 使用方法

### 创建团队

```bash
node scripts/create-team.mjs --name "投资分析团队" --roles "ceo,market-watcher,investment-analyst"
```

### 分配任务

```bash
node scripts/assign-task.mjs --team "投资分析团队" --task "分析英维克股票"
```

### 查看团队状态

```bash
node scripts/team-status.mjs --team "投资分析团队"
```

## 团队角色模板

| 角色 | 职责 | 适用场景 |
|------|------|---------|
| CEO | 决策中枢、任务分配、结果整合 | 所有团队 |
| 市场观察员 | 宏观分析、板块追踪 | 投资分析 |
| 投资分析师 | 个股研究、估值分析 | 投资分析 |
| 风控官 | 风险评估、止损建议 | 投资分析 |
| 主编 | 内容策略、质量把控 | 内容创作 |
| 研究员 | 资料收集、数据分析 | 内容创作、投资分析 |

## 示例：创建投资分析团队

```javascript
const team = {
  name: "投资分析团队",
  members: [
    { role: "ceo", agentId: "ceo", responsibility: "决策中枢" },
    { role: "market-watcher", agentId: "market-watcher", responsibility: "市场分析" },
    { role: "investment-analyst", agentId: "investment-analyst", responsibility: "个股研究" },
    { role: "risk-controller", agentId: "risk-controller", responsibility: "风险控制" }
  ],
  workflow: "parallel-analysis-then-decision"
};
```

## License

MIT
