## Description:

Gets monthly customs-trade breakdowns by company ID to help analyze seasonal shifts and long-term trade trends for supplier monitoring and global market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Export teams, analysts, and supply-chain managers use this skill to query monthly customs trade trends for a company and monitor shipment frequency, product quantity, gross weight, transaction value, seasonal patterns, and longer-term trade activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles UpKuaJing API keys and may read or store credentials in a local .env file.

Mitigation: Avoid printing credential files, avoid pasting API keys into chat or logs, prefer a safer secret mechanism, and verify local credential file permissions before use.

Risk: Some account actions can create persistent credentials or payment-related URLs.

Mitigation: Run credential creation and top-up order commands only after explicit user confirmation and after explaining their account impact.

Risk: Funded accounts can be charged because customs trend API calls incur fees.

Mitigation: Check current pricing through the documented pricing flow and require separate explicit confirmation before fee-incurring queries.

## Reference(s):

- [Company Trade Trends API Reference](references/customs-company-trends-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; fee-incurring queries require explicit user confirmation before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
