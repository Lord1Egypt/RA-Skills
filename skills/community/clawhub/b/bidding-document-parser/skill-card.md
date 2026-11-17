## Description:

招标文件解析助手。自动解析招标文档（PDF/DOCX/TXT），提取资格审查项、废标项、评分标准、技术要求、装订要求、格式要求等6类关键信息，默认输出为结构化Word（DOCX）报告，带PDF原始页码标注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junqio](https://clawhub.ai/user/junqio)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, bid, and proposal teams use this skill to analyze Chinese bidding documents and extract qualification checks, disqualification clauses, scoring criteria, technical requirements, binding requirements, and format requirements. It helps produce structured Markdown and DOCX reports with original PDF page references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted tender text is inserted directly into the analysis prompt and may influence report content.

Mitigation: Use the skill on trusted documents or in a constrained workspace, treat source documents as untrusted input, and review extracted clauses before relying on the report.

Risk: Markdown validation and conversion helpers can rewrite report files or create output files at user-provided paths.

Mitigation: Confirm output paths before running conversion helpers and keep backups of important Markdown reports.

Risk: Generated reports may contain incorrect or incomplete procurement interpretations.

Mitigation: Have a qualified reviewer compare extracted requirements, disqualification clauses, and page references against the original tender document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junqio/skills/bidding-document-parser)
- [extraction_prompt.md](references/extraction_prompt.md)
- [report_format.md](references/report_format.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown report and DOCX report files with PDF page-number annotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses included Python helpers for PDF text extraction, Markdown table validation or repair, and Markdown-to-DOCX conversion.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
