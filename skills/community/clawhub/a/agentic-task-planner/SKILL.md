---
name: task_planner
description: 临床科研任务总调度器。将研究任务拆解为多步执行计划，依次调度证据检索、数据映射、统计分析、导出治理等步骤完成完整科研分析流程。当用户要求执行完整科研分析任务时触发。
---

# 任务编排与调度 Skill

## 何时使用

当用户要求执行一个**完整的**临床科研分析任务时使用本 skill，例如：
- 「帮我分析胃癌术后感染风险」
- 「执行科研可行性分析」
- 「运行完整的科研任务流程」

本 skill 是**总调度器**，会按 5 个步骤依次推进，每个步骤读取对应 mock 数据并向监控后台上报进度。

## 执行流程

**严格按以下顺序执行，每一步必须完成上报后再进入下一步。**

### 步骤 0：启动任务

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"task-planner","display_name":"任务编排与调度","status":"running","message":"开始拆解研究任务，规划 5 步执行计划..."}'
```

读取 `/home/ubuntu/workspace/demo/mock_data/task_workflow.json`，向用户展示：
- 任务 ID、标题、状态
- 5 个步骤的名称列表
- 每步将调用的 skills

然后告诉用户「现在开始依次执行各步骤」。

---

### 步骤 1：证据检索与 Grounding

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"evidence-retriever","display_name":"证据检索与 Grounding","status":"running","message":"正在检索 PubMed、指南库与试验注册信息..."}'
```

读取 `/home/ubuntu/workspace/demo/mock_data/evidence.json`，向用户展示：
- 证据来源统计（指南、PubMed、试验各多少条）
- 关键证据摘要（选 2-3 条代表性结果）
- Grounding 建议：推荐终点定义、时间窗、候选混杂因素

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"evidence-retriever","display_name":"证据检索与 Grounding","status":"completed","message":"已检索 6 条相关证据，完成研究边界 Grounding"}'
```

---

### 步骤 2：数据映射与队列分析

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"cohort-analyst","display_name":"数据映射与队列分析","status":"running","message":"正在连接院内数据字典，匹配变量与评估缺失率..."}'
```

读取 `/home/ubuntu/workspace/demo/mock_data/cohort.json`，向用户展示：
- 变量映射表（研究变量 → 院内字段 → 数据源 → 缺失率）
- Cohort 概览：候选病例数、时间范围、高质量/中等/高缺失变量数
- 风险提示（如 CRP 缺失率高等）
- 纳排标准草案

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"cohort-analyst","display_name":"数据映射与队列分析","status":"completed","message":"已完成 9 个变量映射，候选队列 1,284 例"}'
```

---

### 步骤 3：统计分析与论文框架

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"stats-analyzer","display_name":"统计分析与论文框架","status":"running","message":"正在进行描述性统计、组间比较与论文框架生成..."}'
```

读取 `/home/ubuntu/workspace/demo/mock_data/analysis.json`，向用户展示：
- 分析标题与总体样本量
- 各抗菌方案感染率对比（方案A/B/C 的样本量和感染率）
- 描述统计表（平均年龄、男性占比、手术时长、住院天数）
- 关键发现摘要（3 条）
- 论文框架：建议标题 + 章节列表

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"stats-analyzer","display_name":"统计分析与论文框架","status":"completed","message":"统计分析完成，已生成论文框架草案"}'
```

---

### 步骤 4：导出治理与审批

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"export-governance","display_name":"导出治理与审批","status":"running","message":"正在识别导出风险，应用脱敏规则..."}'
```

读取 `/home/ubuntu/workspace/demo/mock_data/governance.json`，向用户展示：
- 导出风险识别结果（是否含患者级数据、风险等级）
- 可选导出方式（聚合 PDF / 匿名 Excel / 仅图表）
- 脱敏规则
- 审批流信息（申请人、审批人、状态）
- 审计记录编号

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"export-governance","display_name":"导出治理与审批","status":"completed","message":"审批流已生成，审计记录 AUD-2026-0418-0021 已归档"}'
```

---

### 步骤 5：完成任务

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"task-planner","display_name":"任务编排与调度","status":"completed","message":"全部 4 个执行步骤已完成，科研可行性分析任务结束"}'
```

向用户输出任务完成总结：已完成的步骤、关键成果、下一步建议。

## 注意

- 每一步之间保持输出节奏，不要把所有内容一次性输出
- 每一步上报后再执行下一步，确保监控面板能看到逐步推进的过程
- 使用结构化格式展示结果，不要输出原始 JSON
