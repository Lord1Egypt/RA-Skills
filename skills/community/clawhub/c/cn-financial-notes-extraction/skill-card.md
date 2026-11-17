## Description:

提取中国 A 股上市公司年报 (PDF) 中的财务报表附注明细。适用于获取主表无法体现的深层数据（如 CapEx 明细、研发费用细分、应收账款账龄、关联方交易等）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, finance researchers, and developers use this skill to extract detailed financial-note tables from China A-share annual report PDFs for CapEx analysis, receivables aging, goodwill impairment review, related-party transaction review, and R&D expense breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned, older, or irregularly formatted annual report PDFs may produce incomplete or incorrect table extraction.

Mitigation: Validate extracted tables against the source PDF pages and use OCR or manual review when PDFs are scanned or table boundaries are unclear.

Risk: The workflow depends on trusted PDF acquisition and a Python environment with pdfplumber available.

Mitigation: Obtain PDFs from trusted sources, review files before parsing, and confirm the execution environment has the required PDF parsing dependency installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/cn-financial-notes-extraction)

## Skill Output:

**Output Type(s):** [guidance, code, markdown, structured data]

**Output Format:** [Markdown guidance with Python code examples and extracted tables represented as dictionaries, lists, or DataFrames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on annual report PDF text quality, table layout consistency, selected keywords, and pdfplumber availability.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
