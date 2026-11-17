## Description:

Query company customs trade statistics by region dimension to analyze trade volume, amount, monthly trends, and country distribution across global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, market intelligence teams, and agents use this skill to inspect a company's import-export country and region distribution, assess supplier market coverage, and monitor cross-border trade trends through the UpKuaJing Open Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid external customs-data API and account top-up flows.

Mitigation: Confirm each billed query or top-up action explicitly before execution and use the documented pricing source for current fees.

Risk: The skill can store a reusable API key in ~/.upkuajing/.env.

Mitigation: Prefer a secure secret mechanism for UPKUAJING_API_KEY, avoid displaying the .env file contents, and restrict file permissions on ~/.upkuajing and its .env file.

## Reference(s):

- [Company Area Trade Statistics API](references/customs-company-area-stats-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuaJing](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-area-stats)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; successful queries include customs statistics, fee information, and request identifiers.]

## Skill Version(s):

1.0.1 (source: server release and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
