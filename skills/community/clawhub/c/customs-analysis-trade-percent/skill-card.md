## Description:

Query company-level trade share data for a specified HS code using the UpKuaJing Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, sourcing agents, and market researchers use this skill to identify major companies trading a specified product, compare exporter or importer concentration, and discover potential trade partners from customs data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses paid UpKuaJing API access and each trade percent query can incur fees.

Mitigation: Require explicit user confirmation before running paid queries, and use the documented pricing check instead of estimating fees.

Risk: The skill reads UPKUAJING_API_KEY from the environment or ~/.upkuajing/.env.

Mitigation: Prefer a managed secret mechanism; if a local credential file is used, keep it owner-readable only and do not paste its contents into chat or logs.

Risk: Account support flows can query account details and create payment-order URLs.

Mitigation: Run account and top-up commands only for the intended user and present payment links only after the user requests or confirms the action.

Risk: Confirmed error reporting can send request context and response details to the platform.

Mitigation: Ask for explicit confirmation before reporting an error and avoid including unnecessary sensitive business context in the report.

Risk: API calls trigger a version check and can write a local version cache.

Mitigation: Review this behavior before use in environments with strict outbound-network or local-write controls.

## Reference(s):

- [Trade Percent API Reference](references/customs-analysis-trade-percent-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY. Query API calls are paid and should run only after explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
