# Preset System Hardening - 研究摘要

## 目标

把“任务域路由 + 协议治理 + 预设包”收口成正式规则，让前一轮任务域研究结果真正进入 `skill-factory` 主流程。

## 本次核实对象

- 当前主流程：`SKILL.md`
- 当前调研与设计阶段文档：`ref/research.md`、`ref/design.md`、`ref/construction.md`
- 当前兜底调研与构建子 Skill：`sub-skills/brainstorm/SKILL.md`、`sub-skills/skill-creator/SKILL.md`
- 当前协议层：`spec-schema-and-protocol.md`、`spec-review-and-scoring.md`、`spec-template.yaml`
- 前一轮研究结论：`codex-prd/skill-domain-landscape.md`

## 核实结果

### 1. 任务域已经被研究出来，但还没有进入主流程

当前仓库已经有任务域地图，也已经有 `primary_domain`、`peer_domains` 和 `domain_supplements`。
但调研阶段还没有把任务域识别当成硬门槛，主流程仍然偏通用收集。

### 2. 协议字段已经存在，但字段责任还不够明确

`spec.yaml` 已经能表达任务域和研究缺口。
问题在于：

- 何时必须填写
- 哪些字段会阻塞下一阶段
- 如何和 `output/` 目录关联

这些规则还没有正式写清楚。

### 3. 高频任务域还没有形成预设资产

第一层高频任务域已经清楚：

- 工程交付
- 前端与设计到代码
- 浏览器自动化与 UI 测试
- 文档与办公产物
- 文档检索与研究

但当前仓库里还没有固定的预设目录、问题包和执行面建议。

## 研究结论

这一轮最合理的落地方向是：

- 把任务域识别接进调研阶段
- 把任务域字段升级成协议 gate
- 把第一层高频任务域沉淀成正式预设包

## 结果

本轮收口后，需要新增三类固定资产：

- 一套任务域 taxonomy 和跨域判断规则
- 一套 `spec.yaml` 字段责任矩阵和 `output/` 契约
- 一组第一层高频任务域预设包
