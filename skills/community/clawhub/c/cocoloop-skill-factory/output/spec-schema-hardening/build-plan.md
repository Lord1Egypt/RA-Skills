# Spec Schema Hardening - 构建计划

## 目标

把结构化 `spec.yaml` 从讨论结果变成仓库中的正式构建基线。

## 构建目录

```text
spec-schema-hardening/
├── research-summary.md
├── reference-skill-analysis.md
├── design-summary.md
├── spec.md
├── build-plan.md
├── spec-review.md
└── spec.yaml
```

## 构建动作

### 1. 建立 schema 主文档

新增 `codex-prd/spec-schema-and-protocol.md`，定义：

- 顶层结构
- 字段语义
- 研究证据规则
- 任务域结构
- 平台适配结构

### 2. 建立补充文档

新增：

- `codex-prd/domain-supplement-examples.md`
- `codex-prd/spec-review-and-scoring.md`

### 3. 建立模板落点

新增：

- `cocoloop-skill-factory/utils/template/spec-template.yaml`

并将其写入模板索引。

### 4. 回写基线文档

至少更新：

- `prd.md`
- `codex-prd/benchmark-and-quality.md`
- `codex-prd/platforms-templates-and-structure.md`
- `codex-prd/search-capabilities-and-dependencies.md`
- `codex-prd/source-requirements-map.md`
- `cocoloop-skill-factory/SKILL.md`
- `cocoloop-skill-factory/ref/construction.md`

### 5. 生成输出产物

在 `output/spec-schema-hardening/` 中保留一组可审查样例。

## 交付检查

- [x] 已形成 schema 主文档
- [x] 已形成补充文档
- [x] 已形成平台无关模板
- [x] 已回写主 Skill 与构建参考
- [x] 已形成 output 样例产物

## 当前限制

- 还没有自动化校验脚本
- `spec review` 仍是文档规则，不是执行器
- 平台 adapter 还缺更多真实案例
