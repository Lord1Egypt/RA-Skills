## Description:

Extracts structured JSON from W-2s, 1099s, 1040s, and other tax forms, including payer, recipient, wage, withholding, box-level amounts, confidence, and review signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and tax, lending, accounting, or payroll teams use this skill to send selected tax-document PDFs or scans to DeepRead and receive typed extraction results for filing, income verification, ingestion, or audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete tax documents may be sent to DeepRead's service, exposing highly sensitive PII to a third party.

Mitigation: Use only explicitly selected files, confirm DeepRead retention and privacy terms before use, and avoid uploading documents beyond the required workflow.

Risk: Remote redaction may be mistaken for local pre-upload redaction.

Mitigation: Treat the redaction endpoint as another upload to DeepRead and redact locally or obtain approval before sending full documents when policy requires local-only handling.

Risk: Extracted tax values may be incorrect despite review flags.

Mitigation: Review needs_review fields and verify extracted values against source forms before using results in filings, underwriting, or audits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-tax-forms)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with cURL commands and JSON extraction examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and selected tax document files; extracted fields include needs_review flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
