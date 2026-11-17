---
id: replace-with-stable-doc-id
doc_type: skill | runbook | project_context | reference | decision
title: Replace With Human Readable Title / 替换为人类可读标题
summary: One sentence describing the problem this document solves. / 用一句话说明本文解决的问题。
audience:
  - agent
  - human
aliases:
  - alternate name / 替代名称
  - abbreviation / 缩写
search_terms:
  - natural language query / 自然语言查询
  - technical keyword / 技术关键词
use_when:
  - Use this document when the task matches this situation. / 任务符合此场景时使用本文。
skip_when:
  - Do not use this document when the task matches this situation. / 任务符合此场景时不要使用本文。
source_paths:
  - Archived/path/to/original.ext
privacy: non_pii | pii | unknown_sensitive_name
retention: keep | review | delete | archive_only
asset_type: document | presentation | spreadsheet | pdf | visual | metadata_only | bundle
fidelity: text_structure | text_only_layout_lost | sampled_text_metadata | structured_sample | ocr_metadata_visual_pending
extraction_policy: How this asset was extracted and what was intentionally not expanded. / 本资产如何抽取，以及哪些内容被有意保留为按需展开。
related:
  - path/to/related-doc.md
version: 0.1.0
last_reviewed: YYYY-MM-DD
---

## Summary / 摘要

- Most important conclusion 1. / 最重要结论 1。
- Most important conclusion 2. / 最重要结论 2。
- Most important conclusion 3. / 最重要结论 3。

## Insight / 洞察

- Unique, non-consensus, or hard-to-reconstruct knowledge in this asset. / 这份资产中独特、非共识或难以重建的知识。
- Personal experience, project judgment, working method, takeaway, or retention value. / 个人经历、项目判断、工作方法、takeaway 或保留价值。
- Do not use filenames, directories, CSS, cover metadata, or a generic summary here. / 不要在这里填写文件名、目录、CSS、封面 metadata 或泛泛摘要。

## Details / 详情

EN: Expand the body in source order. Preserve original wording, section order, terminology, examples, TODOs, and author judgments. Apply only necessary Markdown, heading, table, formula, code-block, list, image-reference, image-sizing, grammar, and link repairs.
ZH-CN: 按来源顺序展开正文。保留原文措辞、章节顺序、术语、示例、TODO 和作者判断。仅进行必要的 Markdown、标题、表格、公式、代码块、列表、图片引用、图片尺寸、语法和链接修复。

EN: Omit `related` when no related documents exist. Do not emit `related: []` or an empty `related:` followed by `[]`. Add Obsidian width hints to images, formulas, and charts, for example `![[formula.png|420]]`, `![chart|560](https://example.com/chart.png)`, or `![[dense-table.png|620]]`.
ZH-CN: 没有相关文档时省略 `related`。不要输出 `related: []`，也不要在空 `related:` 后单独输出 `[]`。为图片、公式和图表添加 Obsidian 宽度提示，例如 `![[formula.png|420]]`、`![chart|560](https://example.com/chart.png)` 或 `![[dense-table.png|620]]`。

EN: Source headings inside Details start at H3. If Summary already incorporates a source summary, recap, conclusion, or key-points section, remove duplicated bullets from Details and omit that source subsection if it becomes empty. When a source summary exists, do not substitute cover metadata such as title, URL, publication date, word count, or duration.
ZH-CN: Details 内的来源标题从 H3 开始。如果 Summary 已吸收来源中的摘要、总结、结论或要点小节，应从 Details 删除重复 bullet；该来源小节变空时直接省略。原文存在摘要时，不要用标题、URL、发布日期、字数或时长等封面 metadata 替代摘要。

EN: Do not add Procedure or Decision Rules by default. Add them only when the source is a runbook, operating guide, or rule table, or when the user explicitly requests procedure or rule extraction.
ZH-CN: 默认不要添加 Procedure 或 Decision Rules。只有来源是 runbook、操作手册或规则表，或用户明确要求提取步骤或规则时才添加。

<!--
Optional traceability / 可选追溯：
Add a "Source Map / 来源映射" section only for multi-source merges, OCR/page/slide sources, archived originals, or explicit traceability requests.
Use a plain bullet list of article-level Obsidian wikilinks to archived originals. Do not use a table because wikilink aliases contain "|" and can break Markdown table parsing.
Example / 示例:
- [[Archived/path/source.md]]
-->

## Examples / 示例

### Good Input / 良好输入

```text
A realistic, high-quality input example. / 一个真实且高质量的输入样例。
```

### Expected Output / 期望输出

```text
The expected output shape. / 期望的输出形态。
```

## Edge Cases / 边界情况

- Edge case 1 and its handling. / 边界情况 1 及其处理方式。
- Edge case 2 and its handling. / 边界情况 2 及其处理方式。

<!--
Optional related documents / 可选相关文档：
Add a "Related Docs / 相关文档" section only when real related documents exist beyond the source itself.
Do not list the only source file as a related document.
-->
