## Description:

合并 Excel/PDF 企业报表、填充 Word 模板，并在用户明确要求时生成财务分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlinbeard000](https://clawhub.ai/user/merlinbeard000)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external finance users, and agents supporting finance or operations teams use this skill to merge enterprise report files, extract PDF tables, fill Word templates, and create review-ready financial analysis documents when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial reports and can produce trusted-looking Excel or Word outputs with incorrect financial adjustments, OCR-derived values, or generated risk analysis.

Mitigation: Install in an isolated environment with reviewed, pinned dependencies; use trusted source reports; choose unique output paths; and manually review consolidation elimination entries, OCR-derived values, generated risk analysis, and final documents before relying on or sharing them.

Risk: Generated Excel files may contain formula content or external links that require review before distribution.

Mitigation: Inspect generated workbooks for formulas and external links before relying on or sharing the files.

## Reference(s):

- [图片型 PDF 处理指南](references/image_pdf_guide.md)
- [合并模式参考文档](references/merge_modes.md)
- [PDF 表格提取指南](references/pdf_extraction.md)
- [标准贷后分析报告模板规范](references/standard_report_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Excel or Word files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates formatted Excel workbooks and Word documents from user-supplied report files; generated analysis text and extracted values are intended for review before use.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
