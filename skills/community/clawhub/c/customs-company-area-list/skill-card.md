## Description:

Query paginated trade-area data for a company to retrieve country and region breakdowns with trade counts, amounts, and percentages for market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Market analysts, customs-data researchers, and trade teams use this skill to retrieve paginated country and region trade breakdowns for a known company by supplier or buyer role. It supports import-export market analysis, regional drill-down, and follow-up filtering by date, product, HS code, country, or port.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if ~/.upkuajing/.env is printed, pasted, or stored with broad permissions.

Mitigation: Use UPKUAJING_API_KEY from a controlled environment or a tightly permissioned secret file, and avoid displaying the secret file contents.

Risk: Paid queries and top-up actions can incur charges.

Mitigation: Confirm any fee-incurring query or top-up action in a separate user message before running the relevant script.

Risk: Error reports may include request context or response data.

Mitigation: Review error-report content with the user before submitting it to the platform.

Risk: The skill contacts UpKuaJing services and keeps local state under ~/.upkuajing.

Mitigation: Install and run it only in environments where this external service access and local state are acceptable.

## Reference(s):

- [Company Area List API Reference](artifact/references/customs-company-area-list-api.md)
- [Skill Error Report API Reference](artifact/references/skill-error-report-api.md)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-area-list)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; paid query calls require separate confirmation and use cursor-based pagination.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
