## Description:

Recognizes and extracts structured data from 28 financial voucher scenarios, including VAT invoices, travel tickets, toll receipts, tax certificates, medical outpatient invoices, and other reimbursement documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Employees, finance operations teams, and agents use this skill to OCR explicitly specified reimbursement files and return structured voucher fields for expense processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reimbursement files may contain sensitive personal, financial, travel, tax, or medical information and are uploaded to Scnet's cloud OCR service.

Mitigation: Use the skill only for documents approved for third-party upload and only when the user has explicitly provided the file path and requested OCR.

Risk: A changed SCNET_API_BASE could send documents and the API key to an unintended service.

Mitigation: Before use, verify SCNET_API_BASE is the intended Scnet HTTPS API base and keep config/.env readable only by the owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/expense-voucher-ocr)
- [Sugon-Scnet OCR API documentation summary](artifact/references/api-docs.md)
- [Field summary template](artifact/assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON data on stdout with human-readable error text on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; uploads only the explicitly provided local file path to the configured Scnet OCR service.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
