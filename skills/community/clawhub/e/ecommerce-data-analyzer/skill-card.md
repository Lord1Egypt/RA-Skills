## Description:

E-commerce Data Analyzer helps sellers upload CSV sales data, generate sales trends, product rankings, channel revenue shares, profit analysis, inventory warnings, and downloadable PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operators use this skill to inspect sales CSVs, understand sales and channel performance, estimate inventory risk, and create business reports. Developers may also use it as a local Flask-based analytics utility after reviewing its payment and deployment configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an embedded SkillPay key.

Mitigation: Remove the key from the skill, rotate it before use, and load payment credentials from a private environment or secret store.

Risk: The Flask app is configured with a placeholder secret, debug mode, and a public host binding.

Mitigation: Replace the Flask secret, disable debug mode, and bind the service to localhost or another controlled interface before running it.

Risk: Uploaded CSVs and generated reports may contain business data and are stored locally by the app.

Mitigation: Add authorization checks plus clear retention and deletion controls for uploads, charts, and PDF reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/ecommerce-data-analyzer)
- [SkillPay billing API endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Web UI analysis with generated charts and downloadable PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes CSV sales data with required ecommerce columns and uses manually entered costs for profit calculations.]

## Skill Version(s):

2.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
