## Description:

Extracts and calculates key financial indicators from audit report text and provides Q&A guidance for preparing bid-related financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longtel-skill](https://clawhub.ai/user/longtel-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, audit, and bid-preparation users can use this skill to locate financial metrics, apply documented formulas, and generate an Excel extraction result from locally prepared audit-report text. Users should manually verify extracted figures before relying on them in bids, filings, or other formal submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted financial figures may be incomplete or incorrect because local text extraction and regex matching can miss values or select the wrong table context.

Mitigation: Manually verify all extracted and calculated figures against the source audit report before using them in bids, filings, or business decisions.

Risk: The Excel output path selected by the user may overwrite an existing local file.

Mitigation: Review the output path before running the extraction command and save to a new filename when preserving prior results matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longtel-skill/skills/audit-financial-data-extraction)
- [Financial metric extraction Q&A](artifact/references/2025年度审计报告重点财务数据提取问答.md)
- [Contact and maintainer information](artifact/CONTACT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and optional Excel file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-selected local text file and can write an Excel workbook containing extracted and calculated financial indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
