## Description: <br>
Recognizes common enterprise expense invoices, travel receipts, tax documents, and medical invoices, then returns structured OCR data through the Sugon-Scnet OCR service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, finance teams, and agent developers use this skill to extract structured fields from invoices, receipts, tax records, transportation tickets, and related reimbursement documents. It is intended for workflows where the user has permission to send the selected document to Scnet's OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected invoice, receipt, tax, travel, or medical billing documents are sent to Scnet's external OCR API. <br>
Mitigation: Use only documents the user is authorized to share with Scnet and avoid sending sensitive records outside approved workflows. <br>
Risk: The skill requires a Scnet API key. <br>
Mitigation: Store SCNET_API_KEY in a protected environment or config file and do not paste API keys into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/expense-invoice-ocr) <br>
- [Sugon-Scnet OCR API documentation](references/api-docs.md) <br>
- [OCR field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [Structured JSON on standard output, with plain text error messages on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output fields vary by OCR type; the skill requires a local document path and SCNET_API_KEY.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter, skill.yaml, release metadata, CHANGELOG released 2025-05-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
