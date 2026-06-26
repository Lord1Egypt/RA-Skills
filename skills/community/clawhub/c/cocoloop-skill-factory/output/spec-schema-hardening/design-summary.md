# Spec Schema Hardening - 设计摘要

## 设计目标

给 `skill-factory` 增加一层稳定、可复用、可映射的结构化协议。
这层协议让不同平台模板、研究产物和后续构建计划都围绕同一份结果边界展开。

## 设计决策

### 1. 采用独立的 `spec.yaml`

协议不嵌入 `SKILL.md`。
单独文件更适合后续校验、迁移和平台映射。

### 2. 协议只描述结果，不描述实现

这让 `spec.yaml` 能长期稳定。
实现细节继续保留在设计摘要、构建计划和平台文档里。

### 3. 采用 `core + domain_supplements + adapters`

`core`
承接所有 Skill 共有的结果字段。

`domain_supplements`
承接不同任务域的补充要求。

`adapters`
承接不同平台对同一份协议的表达差异。

### 4. `research_evidence` 进入协议，但只放指针

这样协议能证明自己有研究支撑，同时又不把长分析正文塞进本体。

### 5. `spec review` 独立存在

评分和协议本体拆开。
协议负责稳定表达，评估产物负责反映当前准备度。

## 关键结构

本次收口后的顶层结构是：

- `spec_version`
- `skill_identity`
- `intent`
- `scope`
- `inputs`
- `outputs`
- `success_criteria`
- `failure_modes`
- `fallback_policy`
- `dependencies`
- `research_evidence`
- `primary_domain`
- `peer_domains`
- `domain_supplements`
- `adapters`

## 设计收益

- 让统一 spec 从概念变成可填写模板
- 让研究证据和平台适配进入静态协议层
- 让后续平台模板不再从零组织结果边界
- 让 `spec review` 有了明确评估对象
