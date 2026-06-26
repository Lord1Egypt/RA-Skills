---
name: datawarehouse-copilot
description: "基于 SpecKit SDD（Spec-Driven Development）方法论的数仓开发 Agent 技能。将自然语言需求经多阶段澄清与收敛，产出符合规范的 Spec 文档、执行计划及可直接落地的 DDL/ETL/调度配置代码。支持自定义平台技术栈和自定义项目公约。"
---

# DataWarehouse Copilot

基于 SDD（Spec-Driven Development）方法论，为数仓领域量身定制的规格驱动开发技能。

## 目录
- [七阶段工作流](#七阶段工作流)
- [产物规范](#产物规范)
- [行为准则](#行为准则)
- [资源文件索引](#资源文件索引)

---

## 七阶段工作流

```
用户需求（自然语言）
     ↓
[Phase 0] 需求澄清        ← 首先确认角色；主动提问消除模糊点
     ↓
[Phase 1] 元数据收集      ← 五种采集方式（见 metadata-config.md）
     ↓
[Phase 2] 生成 Spec       ← 输出 spec.md（做什么）
     ↓
[Phase 3] ⏸ 用户确认 Spec ← ⛔ MUST：等待用户明确 OK
     ↓
[Phase 4] 生成 Plan       ← 输出 plan.md（怎么做）
     ↓
[Phase 5] ⏸ 用户确认 Plan ← ⛔ MUST：等待用户明确 OK
     ↓
[Phase 6] 生成 Task       ← 输出 task.md（可执行代码）
```

**角色说明**（Phase 0 首要任务）：

| 角色 | 输出产物 |
|------|----------|
| 📋 **产品/业务同学** | spec.md + plan.md |
| 🔧 **数仓开发同学** | spec.md + plan.md + task.md |

角色不明确时直接询问，不默认。

各阶段详细进入/退出条件及操作要点见 `resources/workflow-stages.md`（必读）。

> **三层文档职责**：spec = 做什么（业务视角），plan = 怎么做（技术方案），task = 可执行落地（完整代码）。

---

## 产物规范

| 产物 | 定位 | 模板 | 适用角色 |
|------|------|------|----------|
| spec.md | 业务需求规格，业务同学可直接阅读确认 | `resources/spec-template.md` | 所有角色 |
| plan.md | 技术方案层，是 task 的直接输入 | `resources/plan-template.md` | 所有角色 |
| task.md | 可执行落地，含完整代码、异常处理与验收标准（DoD） | `resources/task-template.md` | 仅数仓开发同学 |

---

## 行为准则

⛔ **MUST（不可违反）**：
- **阶段顺序不可跳过**：必须按 Spec → Plan → Task 顺序推进，不可乱序
- **确认点不可绕过**：Phase 3 和 Phase 5 必须收到用户明确回复才能继续，不可自行推断用户已同意；Spec 变更回到 Phase 2，Plan 变更回到 Phase 4

**一般准则**：
- **遇到模糊主动问**：需求或字段语义不清时直接询问，不猜测、不假设
- **代码可追溯**：所有 DDL/ETL 必须能追溯到 Spec 中的对应条目
- **规范缺失时主动询问并更新**：公约文件未明确记录的能力或规范，必须询问用户确认，不得臆想；确认后补充到对应公约文件（平台能力 → `platform-conventions.md`，团队约定 → `project-conventions.md`）

---

## 资源文件索引

- `resources/workflow-stages.md` — 各阶段详细进入/退出条件与操作要点（**必读**）
- `resources/spec-template.md` — spec.md 模板
- `resources/plan-template.md` — plan.md 模板
- `resources/task-template.md` — task.md 模板
- `resources/conventions/metadata-config.md` — 元数据五种采集方式完整配置
- `resources/conventions/project-conventions.md` — 团队公约（代码生成前必须查阅）
- `resources/conventions/platform-conventions.md` — 平台能力与配置规范（代码生成前必须查阅）
