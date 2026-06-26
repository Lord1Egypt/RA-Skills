## Description: <br>
Invoice Analyzer helps agents extract invoice data, validate amounts and taxes, detect anomalies, support reconciliation, and summarize spend insights from financial documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, procurement, and operations users use this skill to process invoices, review extracted fields, validate totals and tax calculations, flag anomalies, and prepare reconciliation or approval guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice processing may expose bank, tax, vendor, and spend data. <br>
Mitigation: Use the skill only in approved environments, treat extracted data as confidential, and redact unnecessary account details from outputs. <br>
Risk: Approval, payment scheduling, vendor bank-account change, wallet, purchase, or transaction-signing guidance could lead to financial action without adequate oversight. <br>
Mitigation: Require human review and separate authorization before any approval, payment, vendor-account, wallet, purchase, or signing action. <br>
Risk: Extraction, validation, reconciliation, or fraud-risk conclusions may be incorrect or incomplete. <br>
Mitigation: Verify low-confidence fields, calculations, tax treatment, duplicate checks, and reconciliation results against source documents and trusted financial systems. <br>


## Reference(s): <br>
- [Invoice Analyzer Code Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown reports with tables and optional JSON-style structured invoice data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence scores, validation status, fraud risk notes, and recommended human review actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
