## Description: <br>
Checks Chinese enterprise balance sheets, income statements, and tax returns by extracting table data from PDFs or images, normalizing units and currency, and producing reconciliation findings for financial review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial reviewers, credit-risk teams, due-diligence analysts, and agents use this skill to extract structured data from financial statement PDFs or images and compare balance sheet, income statement, and tax return values. It is intended for preliminary review and should be used with explicit approval before sending sensitive documents to Tencent Cloud OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zt1314p-design/financial-statement-check) <br>
- [Cross-check Rules](references/cross-check-rules.md) <br>
- [Field Mapping](references/field-mapping.md) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud OCR Purchase Page](https://buy.cloud.tencent.com/iai_ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Structured JSON for extracted financial data and Markdown audit reports with tables and reconciliation findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud OCR credentials and may upload financial statements, tax returns, or banking-review materials to Tencent Cloud; obtain explicit approval before OCR processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
