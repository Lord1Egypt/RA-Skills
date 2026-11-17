---
name: cross-material-consistency-auditor
slug: cross-material-consistency-auditor-skill
displayName: Cross-Material Consistency Auditor
version: "1.0.9"
description: This skill should be used when two or more materials on the same topic or event need to be compared for cross-material consistency before publication. It identifies mismatched numbers, product names, fact wording, terminology, source attributions, structural promises, and cross-platform expression drift across articles, press releases, slide decks, web pages, white papers, and social posts. It produces a diff matrix with severity ratings and recommended unified wording, without modifying originals. Trigger keywords: 口径审计, 跨材料核对, 多平台一致性, 口径不一致, consistency audit, cross-material check, PR vs 稿, 初稿 vs 通稿, multi-platform review, fact drift.
description_zh: 跨材料口径一致性审计
description_en: Cross-material consistency auditor
not_for:
  - Fact-checking a single document against primary sources (use claim-to-source-auditor)
  - Internal quality review of one standalone material (use a content-review skill)
  - Translation quality assessment or copy editing
  - Modifying or unifying the compared materials automatically
agent_created: true
---

# Cross-Material Consistency Auditor

对于同一主题或同一事件的多份材料，在发布前对比产品名、数字、事实表述、术语、来源标记、结构承诺和跨平台表达差异。只输出差异矩阵和统一口径建议，不自动修改原文。

## When to use

- 同一场发布会/活动的 PR 通稿、媒体约稿、产品稿和演讲稿之间存在数字或产品名不一致。
- 同一篇文章的中文版和英文版（微信、LinkedIn、Substack）表达、数据来源标注或重点存在差异。
- 系列文章在多篇之间的事实、术语或判断出现漂移。
- PPT、白皮书、网页和展厅物料中同一组数字或同一产品用不同名称。
- 需要生成标准化的"口径一致性核对表"供 PR/产品/编辑团队确认。

## Do not use

- 单篇文章的事实核验，由 `claim-to-source-auditor` 或 `content-compliance-reviewer` 处理。
- 单篇文章的格式、语法和客户脱敏检查。
- 选题评估，由 `editorial-topic-portfolio` 处理。
- 直接修改或重写任何原文。

## Input

```yaml
topic_or_event:
  brief:
materials:
  - path:
    label: PR通稿 | 媒体约稿 | PPT | 网页 | 白皮书 | 微信 | LinkedIn | Substack | 演讲稿
  - path:
    label:
reference_source:  # 以哪份材料为权威源，默认第一份
scope: [numbers, product_names, fact_wording, terminology, source_attribution, structural_promises, cross_platform_drift]
read_only: true
```

## Workflow

### Step 1: [Deterministic] Load all materials

1. 读取全部指定材料。
2. 标记每份材料的类型、日期和状态。
3. 记录明显的外部引用和无法解析的内容。

### Step 2: [Deterministic] Extract claims

对每份材料提取：

- 数字及其单位。
- 产品正式名称和简称。
- 事实表述。
- 来源归属。
- 章节级结构承诺。
- 术语和框架名称。

产品名监测词表由使用者自备（不随 Skill 内置任何具体产品清单）：优先读环境变量 `CONSISTENCY_PRODUCT_TERMS`（逗号分隔），其次读使用者自备的本地词表文件（每行一个，`#` 注释）；两者都没有时退化为通用启发式（驼峰复合词 + 大写缩写）。

输出 `01-extracted-claims.json`。

### Step 3: [LLM] Build the diff matrix

逐项对比，每条不一致记录：

- 维度。
- 材料 A 表述 vs 材料 B 表述。
- 差异类型：绝对化 vs 稳妥、归因不同、术语混用、来源混淆、结构丢失、跨平台缩减。
- 严重度：
  - **P0**：数字或法律状态错误；同一客户/产品用不同名称；正文与配图关键数据不同。
  - **P1**：来源归属不一致；跨平台核心判断表述改变；术语混用。
  - **P2**：非关键修辞差异；跨平台深度表达不匹配；下节承诺不在。
- 建议统一口径。
- 是否需要在正文修订后重新对比。

保留一致的项作为正面记录，但输出中不逐条列出。

### Step 4: [LLM] Recommend unified wording

对每个 P0/P1 差异给出精确的统一表述：

- 统一口径文字。
- 引用权威源。
- 统一理由。
- 需要在哪些材料中修改。
- 对系列文章，记录此表述是否需要在前后篇中也统一。

### Step 5: [Deterministic] Produce the audit report

复制 `templates/audit-report.template.md`，生成正式审计报告：

```markdown
# Cross-Material Consistency Audit

## Scope
- topic:
- materials:
- reference source:
- dimensions checked:

## Diff Matrix

| Dim | Material A | Material B | Issue | Severity | Unified wording | Affected files |
|---|---:|---|---|---|---|---|

### Severity grading (2026-10-23)

每条不一致附严重级别：`P0`（数字/事实/产品名冲突）、`P1`（版本/日期漂移）、`P2`（措辞差异）。`P0` 未清零不得进入发布流程；`P1` 需列出但可由作者拍板保留。

## Unified recommendations

| Original | Unified | Source | Reason | Apply to |
|---|---|---|---|---|

## Platform drift (if multi-platform)

| Fact | WeChat | LinkedIn | Substack | Issue | Resolution |
|---|---|---|---|---|---|

## Summary

- P0:
- P1:
- P2:
- consistent items (not listed):

## Revision tracking

For each applied change, record file, original wording, unified wording and source.
```

### Step 6: [Deterministic] Human confirmation

审计报告输出后暂停。确认内容：

- P0/P1 处置方案。
- 统一口径措辞。
- 是否需要回改已发布版本。
- 是否需要更新策划文档和元数据。

确认后由用户或相应的 Writer/Editor 执行修改。本 Skill 不自动修改原文。

## Hard Rules

1. Never modify any original material. Only output the diff matrix and unified wording.
2. Take the earliest or explicitly designated reference source as authoritative for resolving conflicts.
3. P0 mismatches block publication. Flag and require resolution.
4. P1 mismatches require human decision.
5. Same topic, same number, same product name, same terminology must be enforced across all materials.
6. Platform-specific expression differences are acceptable if the core judgment and key facts remain identical.
7. New wording cannot be created from thin air. Unified recommendations must reference an existing source.
8. The audit report is a checkpoint. Hands-off after delivery.

## Failure Handling

| Scenario | Action |
|---|---|
| Only one material provided | Stop; the task requires at least two materials |
| Key material unreadable | Mark the unreadable material and compare only the remaining ones |
| Reference source contains an obvious error | Flag the error and suggest a correction; do not propagate it |
| Complex embedded content (charts, images with text) | Flag as unparseable; request text extraction or manual check |
| Identical text across all materials | Report "no inconsistencies found" and pass |
| P0 mismatch detected in already-published material | Flag with additional severity and recommend a correction |
| A file was revised during the audit session | Re-extract and re-diff only the changed material |

## Output Format

```text
<run-dir>/
├── 01-extracted-claims.json
├── 02-diff-matrix.md
├── 03-audit-report.md
└── 04-unified-wording.json
```

## Verification

- [ ] Every pair of materials compared on all requested dimensions.
- [ ] Every P0 and P1 mismatch has a unified wording recommendation with a source.
- [ ] Reference source is used as arbitration for conflicting claims.
- [ ] Report contains no original-text modifications.
- [ ] Platform drift table covers all platforms.
- [ ] No P0 mismatch remains unresolved; publication stays blocked until every P0 has an applied or explicitly accepted fix.
- [ ] Human confirmation documented before the task is marked complete.

## Pitfalls

- Comparing materials from different publication dates without flagging version gaps.
- Treating a PR draft as authoritative for facts when the product specification is the actual source.
- Recommending unified wording that introduces a new error (correcting one mismatch to match another wrong source).
- Forgetting that PPT and web pages have different levels of precision by design; not every rounding is a mismatch.
- Blaming a ghostwriter for structure differences when the PR brief explicitly allowed adaptation.
- Relying on a single pass and missing PPT embedded charts or images that contain numbers not in the text.
