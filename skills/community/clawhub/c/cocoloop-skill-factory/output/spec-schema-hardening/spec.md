# Spec Schema Hardening - 统一 Spec

## 名称

`spec-schema-hardening`

## 目标

为 `cocoloop-skill-factory` 建立一份结构化 `spec.yaml` 协议层，并把它正式纳入构建准备流程、模板体系和评估体系。

## 适用对象

- `skill-factory` 自身的构建准备流程
- 后续需要跨平台迁移的 Skill
- 需要将调研、设计和构建边界写成静态协议的任务

## 必须满足的要求

### 要求 1

构建准备阶段先形成 `spec.yaml`，再继续生成其他产物。

### 要求 2

`spec.yaml` 只描述结果协议、研究证据指针、任务域补充块和平台 adapter。

### 要求 3

协议内显式保留：

- `coverage_status`
- `evidence_refs`
- `open_gaps`

### 要求 4

平台模板承接 `spec.yaml`，不重复定义核心边界。

### 要求 5

评分结果单独进入 `spec review` 产物，不写回 `spec.yaml`。

## 输入

- `prd.md`
- `codex-prd/spec-schema-and-protocol.md`
- `codex-prd/domain-supplement-examples.md`
- `codex-prd/spec-review-and-scoring.md`
- `cocoloop-skill-factory/utils/template/spec-template.yaml`

## 输出

- 结构化协议定义文档
- 平台无关 `spec-template.yaml`
- 任务域补充块示例
- `spec review` 评分文档
- 已回写到主 Skill、构建参考和需求基线的正式规则

## 成功标准

- `spec.yaml` 已进入模板体系
- `spec.yaml` 已进入主 Skill 和构建参考文档
- `codex-prd` 已包含 schema、任务域补充和评分三类定义
- `output/spec-schema-hardening/` 已形成可审查产物
