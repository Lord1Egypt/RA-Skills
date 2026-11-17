## Description:

Invoice Analyzer helps process invoices, extract structured fields, validate amounts and taxes, flag anomalies, support reconciliation, and summarize financial insights from invoice data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, procurement, and accounts payable teams can use this skill to extract invoice fields, validate totals and taxes, compare vendor and payment details, identify anomalies, and prepare reconciliation or routing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present automatic invoice approval or payment-readiness recommendations in finance workflows.

Mitigation: Use outputs only for extraction, validation, anomaly detection, and routing suggestions; require human approval and maintain segregation-of-duties controls before payment actions.

Risk: Invoice analysis can expose sensitive banking, tax, vendor, and payment information.

Mitigation: Redact or limit sensitive fields unless the runtime environment is approved for that data.

## Reference(s):

- [Invoice Analyzer code examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports with tables and optional JSON-style structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted invoice fields, confidence scores, validation status, fraud risk scores, reconciliation results, and review recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
