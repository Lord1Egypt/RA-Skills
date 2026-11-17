## Description:

Pull trade-partner distribution, HS-code details, product breakdowns, and monthly trade records by company ID to support customs-based supply-chain analysis across global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Export teams, sourcing agents, and trade analysts use this skill to identify trade counterparts, inspect partner composition, review HS-code and product mixes, and map company-level supply-chain relationships from customs records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an UpKuaJing API key stored in the local environment or ~/.upkuajing/.env.

Mitigation: Do not ask the agent to print the .env file or API key, and protect ~/.upkuajing/.env with restrictive file permissions.

Risk: Normal customs-data queries and account top-up flows can incur fees.

Mitigation: Require explicit user confirmation in a separate message before running fee-incurring queries or creating top-up orders.

Risk: Error reports may include business context or request details.

Mitigation: Send error reports only after user confirmation and avoid including sensitive business data unless it is necessary for troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-partner-stats)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Company Trade Partner Trends API](artifact/references/customs-company-partner-stats-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; successful paid queries return customs-data payloads with fee metadata and a requestId.]

## Skill Version(s):

1.0.2 (source: evidence.json release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
