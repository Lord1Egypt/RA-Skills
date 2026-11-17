## Description:

Query paginated national trade list data to retrieve country-level trade breakdowns with annual, quarterly, and monthly trade volumes for market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External export teams, market researchers, and trade analysts use this skill to compare import-export volumes across countries, analyze market penetration, and identify growth opportunities with paginated country-level customs data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API queries and top-up flows can spend account balance.

Mitigation: Confirm each paid query or top-up action in a separate user message before executing it.

Risk: The skill uses a paid-account API key and may read it from a plaintext local `.env` file.

Mitigation: Prefer a secret manager or tightly permissioned environment variable, and do not print or paste the API key into chat.

Risk: Error reports may include request context or payload details.

Mitigation: Review the error report payload and send it only after explicit user confirmation.

Risk: The skill performs automatic version-check traffic to the publisher service.

Mitigation: Run it only in environments where outbound version-check requests to UpKuaJing are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-trade-list)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Trade List API Reference](references/customs-overview-trade-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated country-level trade records include annual, quarterly, and monthly trade totals, supplier and buyer counts, fee details, and request identifiers when API calls succeed.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
