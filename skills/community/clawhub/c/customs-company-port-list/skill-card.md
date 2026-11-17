## Description:

Query paginated port-level trade statistics for a company from UpKuaJing customs data, including trade counts, amounts, quantities, weights, and percentages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and logistics teams use this skill to retrieve company-level port trade breakdowns for customs and logistics analysis. It supports paginated drill-down by company role, date range, product, HS code, country, and port filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an UpKuaJing API account and may read credentials from the UPKUAJING_API_KEY environment variable or local ~/.upkuajing files.

Mitigation: Use a scoped environment variable or a securely permissioned secret file, and do not ask the agent to print full secret files or API keys.

Risk: Customs queries and account top-up operations can affect billing or account balance.

Mitigation: Confirm every paid query, price lookup, recharge order, or payment action explicitly before execution.

Risk: Error reports can include request context, parameters, or response details.

Mitigation: Review the error report payload before sending it and remove secrets or unnecessary sensitive business data.

Risk: The skill performs automatic version checks and stores local state under ~/.upkuajing.

Mitigation: Review outbound UpKuaJing network access and local file permissions before installing in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-port-list)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Company Port List API Reference](references/customs-company-port-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and an UPKUAJING_API_KEY for authenticated API calls.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
