---
name: export_governance
description: 识别导出风险、应用脱敏规则、生成审批流程与审计记录。当用户需要导出研究结果或提交审批时触发。
---

# 导出治理与审批 Skill

## 何时使用

当用户需要**单独执行**结果导出或审批流程时使用，例如：
- 「帮我导出分析结果」
- 「提交审批」
- 「看一下脱敏规则」

如果是完整任务流程的一部分，则由 task-planner 调度。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"export-governance","display_name":"导出治理与审批","status":"running","message":"正在识别导出风险，应用脱敏规则..."}'
```

### 2. 读取数据并输出

读取 `/home/ubuntu/workspace/demo/mock_data/governance.json`，向用户展示：

- **风险识别结果**：是否包含患者级数据、风险等级、建议
- **导出选项**（表格）：导出类型、说明、是否需要审批
- **脱敏规则**：如果数据中有 `desensitization_rules`
- **导出策略**：如果数据中有 `export_strategy`
- **审批流信息**：申请编号、申请人、审批人、审批人角色、提交时间
- **审计记录**：审计编号、操作、操作人、时间戳、追踪状态

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"export-governance","display_name":"导出治理与审批","status":"completed","message":"审批流已生成，审计记录 AUD-2026-0418-0021 已归档"}'
```
