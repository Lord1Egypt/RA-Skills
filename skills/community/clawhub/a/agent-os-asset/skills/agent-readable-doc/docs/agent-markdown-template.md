---
id: agent-readable-markdown-template
doc_type: reference
title: Agent-Readable Markdown Design Guide / Agent 可读 Markdown 设计指南
summary: >-
  EN: Design human-first Markdown that exposes stable retrieval and execution signals to agents without turning the body into a schema dump.
  ZH-CN: 设计 human-first Markdown，在不把正文变成 schema 堆积的前提下，为 Agent 提供稳定的检索与执行信号。
audience:
  - agent
  - human
aliases:
  - agent markdown template / Agent Markdown 模板
  - human-first agent document / human-first Agent 文档
search_terms:
  - design agent readable markdown / 设计 Agent 可读 Markdown
  - markdown retrieval metadata / Markdown 检索 metadata
  - context card procedure verification / Context Card 操作步骤 验证
use_when:
  - Designing a new document that both people and agents must retrieve and use. / 设计需要同时供人和 Agent 检索使用的新文档时。
  - Choosing frontmatter, sections, and verification rules for reusable Markdown. / 为可复用 Markdown 选择 frontmatter、小节和验证规则时。
skip_when:
  - Performing a structure-preserving conversion of an existing source; use the lighter conversion template instead. / 对现有来源做保留结构转换时；应使用更轻量的转换模板。
version: 0.1.0
last_reviewed: 2026-08-26
---

# Agent-Readable Markdown Design Guide / Agent 可读 Markdown 设计指南

EN: English is normative. Prose appears as `EN:` followed by `ZH-CN:`; compact labels use `English / 中文`.
ZH-CN: 英文是规范文本。段落以 `EN:` 后接 `ZH-CN:`，紧凑标签使用 `English / 中文`。

## Context Card / 上下文卡片

EN: One-line conclusion: use a human-first body while placing stable retrieval and execution signals in frontmatter, the Context Card, and a few predictable sections.
ZH-CN: 一句话结论：正文保持 human-first，同时把稳定的检索与执行信号放入 frontmatter、Context Card 和少量可预测小节。

EN: Use this guide when a document must be pleasant for people to scan and reliable for an agent to retrieve, place in context, and act on.
ZH-CN: 当文档既要便于人类扫读，又要让 Agent 能可靠检索、放入 context 并据此行动时，使用本指南。

EN: Do not use the full structure for a human-only essay, a machine-only schema, or a structure-preserving conversion that should retain the source shape.
ZH-CN: 面向纯人类的长文、纯机器 schema，或需要保留来源结构的转换，不要套用完整结构。

EN: Fast path: read frontmatter and this Context Card, then read Design Rules. For implementation, copy `../templates/agent-readable-doc-template.md`.
ZH-CN: 最快路径：先读 frontmatter 和本 Context Card，再读 Design Rules。落地时复制 `../templates/agent-readable-doc-template.md`。

## Summary / 摘要

- Put machine-facing signals early without harming the reading experience. / 将机器信号前置，但不要破坏阅读体验。
- `summary`, `aliases`, `search_terms`, `use_when`, and `skip_when` determine retrieval quality. / `summary`、`aliases`、`search_terms`、`use_when` 和 `skip_when` 决定检索质量。
- Context Card determines whether an agent or person should continue reading. / Context Card 帮助 Agent 或人判断是否继续阅读。
- Each H2 should remain understandable as an independent context chunk. / 每个 H2 都应能作为独立 context chunk 被理解。
- Behavioral documents need Procedure, Decision Rules, and Verification. / 行为型文档需要 Procedure、Decision Rules 和 Verification。
- Existing-source conversions stay lighter and prioritize source expression over uniform restructuring. / 既有来源转换采用更轻结构，并优先保留来源表达而不是强行统一重构。

## Design Rules / 设计规则

### 1. Frontmatter Is the Retrieval Interface / Frontmatter 是检索接口

EN: Frontmatter helps an agent and retrieval system decide whether a document is relevant. Keep it stable, short, and searchable rather than trying to explain every detail.
ZH-CN: Frontmatter 帮助 Agent 和检索系统判断文档是否相关。它应稳定、短小且可搜索，而不是解释所有细节。

| Field / 字段 | Purpose / 用途 |
| --- | --- |
| `id` | Stable identity that survives title changes / 不受标题变化影响的稳定标识 |
| `doc_type` | Distinguishes skill, runbook, project context, reference, and decision / 区分 skill、runbook、project context、reference 和 decision |
| `title` | Human-readable title / 人类可读标题 |
| `summary` | One sentence describing the problem solved / 一句话说明文档解决的问题 |
| `aliases` | Alternate names, abbreviations, and legacy names / 替代名称、缩写和旧称 |
| `search_terms` | Natural queries and technical terms / 自然语言查询和技术术语 |
| `use_when` | Situations that should retrieve the document / 应召回本文的场景 |
| `skip_when` | Situations that should not retrieve the document / 不应召回本文的场景 |
| `version` | Document contract or content version / 文档契约或内容版本 |
| `last_reviewed` | Most recent human review date / 最近人工复核日期 |

### 2. Context Card Routes Reading / Context Card 路由阅读

EN: Put the Context Card first in documents designed from scratch. It should tell a person within 30 seconds whether to continue and let an agent make the same decision with a small token budget.
ZH-CN: 对从零设计的文档，将 Context Card 放在正文首节。它应让人在 30 秒内判断是否继续阅读，也让 Agent 用较少 tokens 做出同样判断。

- One-line conclusion / 一句话结论
- Use when / 适用场景
- Do not use when / 不适用场景
- Fastest reading path / 最快读取路径

### 3. Write an Engineering Manual, Not a Field Dump / 正文像工程手册而不是字段清单

EN: Use natural headings, short paragraphs, and explicit actions. Keep machine fields such as keywords, entities, and routing hints out of the prose body.
ZH-CN: 使用自然标题、短段落和明确操作。不要把 keywords、entities 和 routing hints 等机器字段铺在正文里。

- Lead with the outcome, then details. / 先给结论，再给细节。
- Let each section solve one problem. / 每节只解决一个问题。
- Use tables for stable mappings or rules, not for dense explanation. / 表格用于稳定映射或规则，不用于堆积解释。
- Keep examples close to realistic input and output. / 示例应接近真实输入输出。

### 4. Make Every H2 Independently Useful / 让每个 H2 可独立使用

EN: An agent may receive only one chunk. Start each H2 with its purpose, avoid vague references such as "above," name referenced sections, and repeat critical constraints when omission would be unsafe.
ZH-CN: Agent 可能只拿到一个 chunk。每个 H2 开头应说明用途，避免“如上”之类模糊引用，引用其他小节时写明名称，并在遗漏会带来风险时重复关键约束。

### 5. Make Behavioral Documents Verifiable / 让行为型文档可验证

EN: A document that directs action should state Procedure, Decision Rules, and Verification so an agent can choose a branch and determine whether the result is correct.
ZH-CN: 指导行动的文档应明确 Procedure、Decision Rules 和 Verification，让 Agent 能选择分支并判断结果是否正确。

## Canonical Skeleton / 标准骨架

```markdown
---
id: stable-id
doc_type: reference
title: Human Readable Title / 人类可读标题
summary: One-sentence purpose. / 一句话用途。
aliases:
  - alternate name / 替代名称
search_terms:
  - natural query / 自然查询
use_when:
  - Use case. / 使用场景。
skip_when:
  - Exclusion case. / 排除场景。
version: 0.1.0
last_reviewed: YYYY-MM-DD
---

# Human Readable Title / 人类可读标题

## Context Card / 上下文卡片

EN: One-line conclusion.
ZH-CN: 一句话结论。

## Summary / 摘要

- Most important conclusion. / 最重要结论。

## Procedure / 操作步骤

1. First action. / 第一步操作。
2. Second check. / 第二步检查。
3. Final output. / 第三步输出。

## Decision Rules / 决策规则

| Condition / 条件 | Action / 动作 | Reason / 理由 |
| --- | --- | --- |
| Condition A / 条件 A | Action A / 动作 A | Core reason / 核心理由 |

## Details / 详情

EN: Add short, independently understandable sections for background, rationale, and cautions.
ZH-CN: 用短小且可独立理解的小节展开背景、原理和注意事项。

## Examples / 示例

EN: Provide one to three realistic input/output examples.
ZH-CN: 提供一到三个真实或接近真实的输入输出示例。

## Verification / 验证

EN: State how an agent or person can confirm correct use.
ZH-CN: 说明 Agent 或人如何确认本文被正确使用。
```

## Document-Type Guidance / 文档类型指南

### Skill Documents / Skill 文档

EN: Optimize for accurate triggering and stable execution. Emphasize `use_when`, `skip_when`, procedure order, tool boundaries, failure branches, and verification. Minimize generic background.
ZH-CN: 优先保证准确触发和稳定执行。强化 `use_when`、`skip_when`、步骤顺序、工具边界、失败分支和验证；减少泛化背景。

### Project Context Documents / Project Context 文档

EN: Reduce repository-reading cost. Cover entrypoints, runtime shape, important directories, main flows, common commands, invariants, tests, and release boundaries.
ZH-CN: 降低阅读仓库的成本。覆盖入口、运行形态、关键目录、主链路、常用命令、不变量、测试和发布边界。

### Knowledge Notes / Knowledge Note 文档

EN: Optimize for high-quality reuse. Emphasize core conclusions, applicability boundaries, evidence, counterexamples, and related concepts.
ZH-CN: 优先保证高质量复用。强化核心结论、适用边界、证据、反例和关联概念。

### Converted Sources / 转换来源文档

EN: Use the lighter `agent-readable-doc` contract: lean frontmatter, `Summary / 摘要`, `Insight / 洞察`, and `Details / 详情`; no repeated title H1; source headings below H3; no default Procedure, Decision Rules, Verification, or Related Docs; no empty optional frontmatter; width hints for images; deduplicated boilerplate; dry-run archival before explicit `--execute`; and article-level Source Map only when traceability matters.
ZH-CN: 使用更轻量的 `agent-readable-doc` 契约：精简 frontmatter、`Summary / 摘要`、`Insight / 洞察` 和 `Details / 详情`；不重复标题 H1；来源标题从 H3 开始；默认不添加 Procedure、Decision Rules、Verification 或 Related Docs；不保留空的可选 frontmatter；图片带宽度提示；样板内容去重；显式 `--execute` 前先 dry-run 归档；仅在需要追溯时添加文章级 Source Map。

### Decision Documents / Decision 文档

- `Decision / 决策`: what was selected / 选择了什么
- `Why / 原因`: core rationale / 核心理由
- `Alternatives / 替代方案`: rejected options / 被否选项
- `Consequences / 后果`: follow-up impact and risk / 后续影响和风险

## Quality Checklist / 质量清单

- Frontmatter contains retrieval fields and no malformed empty optionals. / Frontmatter 包含检索字段且没有格式错误的空可选项。
- Summary states the problem in one sentence. / Summary 用一句话说明问题。
- `skip_when` reduces false-positive retrieval. / `skip_when` 能降低误召回。
- The first 300 to 500 tokens support a continue-or-stop decision. / 前 300 到 500 tokens 足以支持继续或停止阅读的判断。
- Every H2 remains understandable outside the full document. / 每个 H2 脱离全文仍可理解。
- Behavioral documents include Procedure, Decision Rules, and Verification. / 行为型文档包含 Procedure、Decision Rules 和 Verification。
- Human scanning feels natural rather than database-like. / 人类扫读自然，不像阅读数据库字段。
- `version` and `last_reviewed` are current. / `version` 和 `last_reviewed` 已更新。

## Verification / 验证

EN: Test retrieval with five to ten natural-language queries plus near-miss queries that should be excluded by `skip_when`. Give an agent only frontmatter and Context Card to check routing, sample an H2 to test chunk independence, and ask a person to scan for 30 seconds and state the purpose and next action.
ZH-CN: 使用五到十个自然语言查询测试召回，并加入应被 `skip_when` 排除的近似错误查询。只给 Agent frontmatter 和 Context Card 检查路由，随机抽取一个 H2 测试 chunk 独立性，并让人扫读 30 秒后说明文档用途和下一步操作。

## Related Docs / 相关文档

- `../templates/agent-readable-doc-template.md` — Copyable conversion template / 可复制的转换模板
- `../SKILL.md` — Conversion execution entrypoint / 转换执行入口
