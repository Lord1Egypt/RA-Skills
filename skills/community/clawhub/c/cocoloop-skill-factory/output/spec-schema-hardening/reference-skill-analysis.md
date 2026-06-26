# Spec Schema Hardening - 参考方案分析

## 分析目标

本次不分析某个外部业务 Skill，重点是检查 `skill-factory` 现有构建资料中是否已经具备承接结构化协议的落点。

## 本地参考范围

本次重点查看了这些本地资料：

- `cocoloop-skill-factory/SKILL.md`
- `cocoloop-skill-factory/ref/construction.md`
- `cocoloop-skill-factory/utils/template/index.md`
- `cocoloop-skill-factory/utils/template/*.md`
- `codex-prd/design-and-construction.md`
- `codex-prd/platforms-templates-and-structure.md`
- `codex-prd/benchmark-and-quality.md`

## 观察结果

### 1. 现有流程已经有统一 spec 的位置

主 Skill 和构建阶段文档一直在强调“统一 spec”和“构建说明”。
说明流程上已经有结构化协议的落位空间，只是之前还没有稳定的字段定义。

### 2. 模板体系缺少平台无关协议模板

已有模板主要是平台模板。
这意味着在平台差异之前，缺少一层统一的静态协议骨架。

### 3. 质量要求里缺少轻量自评环节

已有质量文档强调 benchmark 和整体质量。
但在 `spec.yaml` 形成后，还缺少一轮专门检查协议完整度和证据充分度的 `spec review`。

### 4. 搜索规则已经足够支撑 `research_evidence`

现有规则已经要求：

- 搜索候选方案
- 全量拉取本地分析
- 记录可复用能力和设计要点

这意味着把搜索结论下沉为 `research_evidence` 指针是顺滑的，不需要推翻原流程。

## 可复用做法

- 保留“统一 spec”作为构建准备的固定入口
- 将平台模板留在协议层之后
- 将搜索结果与本地分析结果转成可追溯证据指针
- 将评分结果从静态协议中分离出去

## 本次采用的改动方向

- 新增 `spec-schema-and-protocol.md`
- 新增 `spec-template.yaml`
- 新增 `spec-review-and-scoring.md`
- 新增 `domain-supplement-examples.md`
- 回写 `SKILL.md`、`ref/construction.md`、`prd.md` 和 `codex-prd` 需求基线
