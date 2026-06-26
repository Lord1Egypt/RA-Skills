# dochub 实体类型定义

定义知识库中各类页面的 YAML frontmatter 规范和内容模板。

## 页面类型总览

| 类型 | 目录 | frontmatter `type` | 必填字段 | 用途 |
|------|------|-------------------|---------|------|
| 主编排索引 | `wiki/` | `index` | title, type, updated | 所有检索入口 |
| 操作日志 | `wiki/` | `log` | title, type, created | 审计追踪 |
| 知识库概览 | `wiki/` | `overview` | title, type, updated | 统计总览 |
| 源文档摘要 | `wiki/sources/` | `source-summary` | title, type, sources, domain, tags, created, updated, confidence | 每个源文档对应一个 |
| 概念页 | `wiki/concepts/` | `concept` | title, type, sources, domain, tags, created, updated, confidence, related | 跨文档主题 |
| 实体页 | `wiki/entities/` | `entity` | title, type, entityType, sources, domain, created, updated, confidence, related | 人物/组织/系统 |
| 对比页 | `wiki/comparisons/` | `comparison` | title, type, subjects, sources, created, updated, confidence, related | 对比分析 |
| Lint 报告 | `wiki/` | `lint-report` | title, type, date | 健康检查结果 |

## 1. 源文档摘要页 (source-summary)

```yaml
---
title: {文档标题，从文件名推导，去除扩展名}
type: source-summary
sources:
  - raw/{category}/{subdir}/{filename}.docx
domain: {从目录结构推导，如 "新进港货站", "设施设备"}
tags: [{从内容提取 3-5 个关键词}]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
---
```

**内容结构：**
```markdown
# {文档标题}

## 文档信息
- 原始文件: `raw/{path}`
- 文档类型: {报告/方案/计划/清单/...}
- 日期: {从内容或文件名提取}

## 摘要
{3-5 句话总结文档核心内容}

## 关键要点
- {要点 1}
- {要点 2}
- ...

## 涉及实体
- 人物/角色: [{列出}]
- 组织/部门: [{列出}]
- 系统/设备: [{列出}]
- 地点: [{列出}]

## 涉及概念
- [[concepts/{概念名}]]
- ...

## 关联文档
- [[sources/{path}/related-file]] — {关系说明}
```

## 2. 概念页 (concept)

```yaml
---
title: {概念名称}
type: concept
sources:
  - raw/{path}/file1.docx
  - raw/{path}/file2.docx
domain: {主要领域}
tags: [{关键词}]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
related:
  - "[[concepts/related-concept]]"
  - "[[entities/related-entity]]"
---
```

**内容结构：**
```markdown
# {概念名称}

## 定义
{概念的核心定义，如果从多文档归纳则标注来源}

## 关键信息
- {维度 1}: {内容} (来源: [[sources/{path}]])
- {维度 2}: {内容} (来源: [[sources/{path}]])

## 在不同文档中的体现
| 文档 | 涉及内容 | 视角 |
|------|---------|------|
| [[sources/{path}]] | {简述} | {该文档的视角} |

## 相关概念
- [[concepts/{related}]]
```

## 3. 实体页 (entity)

**实体子类型：**

| entityType | 说明 | 额外必填字段 |
|-----------|------|-------------|
| `person` | 人物 | role, organization |
| `organization` | 组织/部门 | parentOrg (可选) |
| `system` | 系统/平台 | vendor (可选), version (可选) |
| `location` | 地点 | address (可选) |
| `equipment` | 设备 | model (可选), manufacturer (可选) |
| `process` | 流程 | stages |
| `project` | 项目 | status, timeline |

```yaml
---
title: {实体名称}
type: entity
entityType: person | organization | system | location | equipment | process | project
sources:
  - raw/{path}/file.docx
domain: {主要领域}
tags: [{关键词}]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
related:
  - "[[entities/related-entity]]"
  - "[[concepts/related-concept]]"
---
```

**内容结构（以 system 为例）：**
```markdown
# {系统名称}

## 基本信息
- 类型: {系统类型}
- 用途: {一句话用途}
- 关联实体: [{相关组织/人员}]

## 在各文档中的描述
| 文档 | 描述角度 | 关键信息 |
|------|---------|---------|
| [[sources/{path}]] | {视角} | {关键信息摘要} |

## 与其他实体的关系
- 依赖于: [[entities/{dependency}]]
- 被使用于: [[entities/{consumer}]]

## 相关概念
- [[concepts/{concept}]]
```

## 4. 对比页 (comparison)

```yaml
---
title: {对比标题，如 "旧货站 vs 新进港货站流程对比"}
type: comparison
subjects:
  - {主体A}
  - {主体B}
sources:
  - raw/{path}/file1.docx
  - raw/{path}/file2.docx
domain: {领域}
tags: [{关键词}]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
related:
  - "[[concepts/{concept}]]"
---
```

**内容结构：**
```markdown
# {对比标题}

## 对比维度
| 维度 | {主体A} | {主体B} | 差异分析 |
|------|--------|--------|---------|
| {维度1} | {A 的描述} | {B 的描述} | {分析} |

## 综合结论
{总结对比结果，标注置信度}

## 来源
- [[sources/{path}]]
```

## 领域标签体系

根据文档内容动态建立，初始建议标签：

### 业务领域
- `进港业务` — 进港货站运营相关
- `设施设备` — 设备维护、维修相关
- `人员管理` — 排班、人力配置相关
- `搬迁项目` — 新货站搬迁相关
- `系统建设` — EMS、ETV 等系统项目

### 文档类型
- `报告` — 分析/评估/报告类
- `方案` — 运行预案/方案类
- `清单` — 任务清单/维修清单类
- `流程` — 操作流程/标准作业程序

### 置信度
- `high` — 来自正式文档，多方验证
- `medium` — 来自单一源或草案
- `low` — 推测、口头信息或过时内容

## 交叉引用规范

使用 Obsidian 风格的 [[wikilinks]]：

| 引用格式 | 含义 |
|---------|------|
| `[[concepts/进港流程]]` | 引用概念页 |
| `[[entities/EMS系统]]` | 引用实体页 |
| `[[sources/新进港货站/xxx/文件名]]` | 引用源文档摘要 |
| `[[comparisons/旧vs新流程]]` | 引用对比页 |

注意：[[wikilinks]] 中的路径相对于 `wiki/` 目录，文件名不含 `.md` 扩展名。
