## Description:

图书智能解读系统对用户提供的书名、章节文本、笔记或 PDF 摘录进行多维度解读，产出包含核心内容、框架拆解、关键概念、应用价值、同类书推荐、Markdown 与 HTML 双格式报告的读书分析结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mongoliatooop](https://clawhub.ai/user/mongoliatooop)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, students, knowledge workers, and agent users use this skill to analyze books from a title or supplied excerpts and receive a structured Chinese reading report. It is suited for book summaries, reading guides, concept extraction, critical analysis, action planning, mind maps, and follow-on book recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates two local report files for each book analysis, which may overwrite or clutter existing outputs if the destination is unclear.

Mitigation: Confirm the output folder and overwrite behavior before generating reports for important material.

Risk: Broad natural-language triggers and Chinese-oriented defaults may produce reports when the user intended a narrower summary or a different language.

Mitigation: Clarify the requested scope, depth, and language before running the full 13-section report workflow.

Risk: Optional online Mermaid rendering can introduce a network dependency even though the HTML report is designed to work offline.

Mitigation: Use the self-contained HTML and plain-text mind map by default; allow online Mermaid rendering only when the user explicitly approves it.

Risk: When only a book title is supplied, book facts, quotations, and recommendations may be less reliable than analyses grounded in provided source text.

Mitigation: Prefer user-provided excerpts or notes for important work, label source status clearly, and downgrade uncertain quotations to paraphrases.

## Reference(s):

- [图书智能解读系统输出规范](artifact/references/report-spec.md)
- [ClawHub skill page](https://clawhub.ai/mongoliatooop/skills/book-analyst)
- [Publisher profile](https://clawhub.ai/user/mongoliatooop)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown report plus self-contained HTML file, with Mermaid mindmap syntax and a plain-text fallback where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces two local report files per analyzed book; users should clarify output folder, overwrite behavior, preferred language, and whether online Mermaid rendering is allowed.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
