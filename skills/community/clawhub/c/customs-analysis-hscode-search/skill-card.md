## Description:

Searches customs trade data for HS codes matching a product name and HS code keyword so the resulting codes can be used in deeper trade analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, exporters, import-export professionals, and agents use this skill to locate relevant HS customs classification codes before running market research, competitor monitoring, or other customs-data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a billable UpKuaJing API key, and exposed credentials could allow unauthorized paid API usage.

Mitigation: Provide UPKUAJING_API_KEY through a controlled secret mechanism when possible, restrict permissions on any local key file, and avoid printing ~/.upkuajing/.env.

Risk: HS code lookups and account top-up actions can incur fees.

Mitigation: Require explicit user confirmation before fee-incurring queries, top-up orders, or error reports, and check official pricing before estimating costs.

## Reference(s):

- [HS Code Search API Reference](references/customs-analysis-hscode-search-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [UpKuaJing OpenAPI Endpoint](https://openapi.upkuajing.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns matching HS code strings, optional pagination cursor, fee information, and request identifiers from the UpKuaJing API.]

## Skill Version(s):

1.0.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
