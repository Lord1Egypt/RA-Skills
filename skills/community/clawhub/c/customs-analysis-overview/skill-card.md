## Description:

Retrieves country-level supplier and buyer counts for customs analysis reports through the UpKuaJing Open Platform API, with cursor-based pagination for overview results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, market researchers, import-export professionals, and developers use this skill to compare supplier and buyer activity by country for a customs analysis overview. It helps identify active trading countries and supports market assessment workflows that need paginated country-level results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a paid UpKuaJing API account and can trigger fee-incurring overview queries.

Mitigation: Confirm every paid query or top-up action with the user before execution and use the linked pricing source or price_info helper for current pricing.

Risk: The skill reads and stores the UpKuaJing API key in the user's local ~/.upkuajing/.env file.

Mitigation: Do not print the contents of ~/.upkuajing/.env, restrict the file to the local user, and avoid sharing the API key in prompts, logs, or reports.

Risk: Error reports may include request or response details from failed API calls.

Mitigation: Send error reports only after user confirmation and avoid including sensitive request or response data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/customs-analysis-overview)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed price description](https://www.upkuajing.com/web/openapi/price.html)
- [Customs Analysis Overview API reference](references/customs-analysis-overview-api.md)
- [Skill Error Report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Overview results include a paginated list of country codes, supplier counts, buyer counts, latest trade dates, fee information, and request identifiers.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
