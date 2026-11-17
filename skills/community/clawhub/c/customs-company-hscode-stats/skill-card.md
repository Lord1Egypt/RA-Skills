## Description:

Query company customs trade statistics by HS code dimension to analyze HS code distribution, trade volume breakdown, and monthly trade trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trade-data analysts use this skill to query UpKuaJing customs data for a company's supplier or buyer HS code distribution, product-category concentration, import-export classification patterns, and monthly trade trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses and persists an UpKuaJing API key.

Mitigation: Store the key with restrictive permissions or a secret manager, and do not let an agent print ~/.upkuajing/.env.

Risk: The skill can make paid API calls after user confirmation.

Mitigation: Require explicit confirmation before fee-incurring calls and check current pricing through the documented pricing source or script.

Risk: The skill includes account top-up and payment URL flows.

Mitigation: Review payment URLs before opening them and proceed only through trusted UpKuaJing account workflows.

Risk: Error reports may include request or response details.

Mitigation: Approve error reports only after removing sensitive request, response, or account information.

Risk: The skill performs update-check behavior during API request handling.

Mitigation: Review the update-check behavior before installation in environments with strict outbound network controls.

## Reference(s):

- [Company HS Code Trade Statistics API](references/customs-company-hscode-stats-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-hscode-stats)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses include HS code distribution, monthly trade trends, fee information, and request identifiers.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
