## Description:

Checks Chinese enterprise balance sheets, income statements, and tax returns by extracting OCR table data, normalizing units and currency, and reporting time, completeness, tax-accounting, and cross-table consistency findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Credit reviewers, financial due diligence teams, auditors, and risk analysts use this skill to extract structured financial statement data from PDFs or images and generate preliminary reconciliation checks across balance sheet, income statement, and tax return records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial PDFs or images may be sent to Tencent Cloud OCR.

Mitigation: Use the skill only in approved workspaces and confirm each selected file or URL before OCR is invoked.

Risk: Local file path inputs can allow unintended readable files to be encoded and transmitted.

Mitigation: Restrict execution to a scoped directory and avoid broad automatic invocation on sensitive records.

Risk: Tencent Cloud credentials are required for OCR calls.

Mitigation: Provide least-privilege credentials through environment variables and rotate or revoke them according to the deployment policy.

Risk: OCR-derived financial checks can be incomplete or incorrect.

Mitigation: Treat reports as preliminary review support and require human validation before credit, audit, tax, or compliance decisions.

## Reference(s):

- [Cross-check rules](references/cross-check-rules.md)
- [Field mapping](references/field-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON extraction results and Markdown audit reports, with shell commands for OCR setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use Tencent Cloud OCR on selected PDF or image inputs; reported figures are normalized to ten-thousand-unit amounts and CNY when possible.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
