# Skill Domain Landscape - 构建计划

## 目标

把“Skill 常见任务域与执行面地图”沉淀成后续可直接复用的研究输入。

## 构建目录

```text
skill-domain-landscape/
├── research-summary.md
├── reference-skill-analysis.md
├── design-summary.md
├── spec.md
└── build-plan.md
```

## 当前已完成动作

### 1. 调研官方生态

已核对：

- OpenAI Codex Skills 文档与仓库
- Anthropic Skills 文档与仓库
- Gemini CLI Skills 与 Extensions 资料
- Agent Skills 开放标准资料

### 2. 抽样分析代表性方向

已覆盖：

- 工程交付
- 前端设计
- 浏览器自动化
- 文档办公
- 文档检索
- 业务系统集成
- 部署平台
- 安全场景

### 3. 形成正式产物

已在 `output/skill-domain-landscape/` 中生成：

- 研究摘要
- 参考 Skill 与执行面分析
- 设计摘要
- 统一 spec
- 构建计划

## 后续建议动作

### 1. 在 `codex-prd` 建立正式需求页

把这次研究进一步整理成产品基线，方便后续接入主 Skill。

### 2. 把高优先级任务域接进调研流程

优先接入：

- 代码仓库与工程交付
- 浏览器自动化与 UI 测试
- 前端、设计与设计到代码
- 文档、文件与办公产物
- 文档检索、知识问答与研究

### 3. 为每个任务域补单独参考包

后续每个高优先级任务域都适合再补：

- 本地 Skill 全量分析
- 原子能力目录
- 构建模板
