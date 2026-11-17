## Description:

Enterprise Intro generates professional Chinese-language enterprise insight reports from multi-dimensional company data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royyyyor](https://clawhub.ai/user/royyyyor)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, finance teams, legal professionals, transaction counterparties, and public readers use this skill to produce concise enterprise credit analysis, business research, investment diligence, and organization profile reports for mainland China entities.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill sends signed API requests containing queried enterprise names to a user-configured third-party endpoint.

Mitigation: Use it only after verifying CHINADAAS_BASE_URL is the official HTTPS Qibook endpoint, trusting the provider, and avoiding confidential enterprise queries.

Risk: The templates include wording intended to conceal AI involvement in generated reports.

Mitigation: Review and remove AI-concealment language before using generated reports in customer-facing or governed workflows.

Risk: API credentials are required for operation.

Mitigation: Store CHINADAAS_UID and CHINADAAS_KEY securely, restrict access to the runtime environment, and rotate credentials if exposure is suspected.

## Reference(s):

- [Qibook/企百科 homepage](https://qibook.com)
- [ClawHub skill page](https://clawhub.ai/royyyyor/skills/enterprise-intro)
- [Sample company report](artifact/examples/sample_company_report.md)
- [Company report template](artifact/templates/company.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, API Calls, Configuration]

**Output Format:** [Chinese-language Markdown enterprise or organization report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHINADAAS_UID, CHINADAAS_KEY, and CHINADAAS_BASE_URL; report length is capped by input data size.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
